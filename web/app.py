from flask import Flask, render_template, Response
import cv2
import boto3
import time
app = Flask(__name__)

STREAM_NAME = "testing"
kvs = boto3.client("kinesisvideo", region_name='ap-southeast-1')

# Grab the endpoint from GetDataEndpoint
endpoint = kvs.get_data_endpoint(
    APIName="GET_HLS_STREAMING_SESSION_URL",
    StreamName=STREAM_NAME
)['DataEndpoint']

kvam = boto3.client("kinesis-video-archived-media", endpoint_url=endpoint)
url = kvam.get_hls_streaming_session_url(
    StreamName=STREAM_NAME,
    PlaybackMode="LIVE"
)['HLSStreamingSessionURL']

camera = cv2.VideoCapture(url)
# camera.set(cv2.CAP_PROP_BUFFERSIZE, 1)
# camera.set(cv2.CAP_PROP_FPS, 1)
rekognition = boto3.client('rekognition')
def labelDetection(frame):
    ret, buf = cv2.imencode('.jpg', frame) 
    response = rekognition.detect_custom_labels(
        # find project arn in console
        ProjectVersionArn='replace in here',
        Image={
            'Bytes': buf.tobytes(),
        },
        MinConfidence=95
    )
    return response

frame_rate = 0.25
prev = 0

def gen_frames(frame_rate, prev):  # generate frame by frame from camera
    count = 0
    while True:
        time_elapsed = time.time() - prev
        # res, image = cap.read()
        success, frame = camera.read()  # read the camera frame
        if time_elapsed > 1./frame_rate:
            prev = time.time()
        # Capture frame-by-frame
        
        # time.sleep(1)
            # if not success:
            #     break
            # else:
            try:
                if count % 2 == 0:
                    resp = labelDetection(frame)
                    count += 1
                else:
                    count +=1
                imgHeight, imgWidth, channels = frame.shape
                    # print(imgHeight,imgWidth)
                respones = resp['CustomLabels'][0]['Geometry']['BoundingBox']
                    # print(respones)
                    # draw the bounding box through cv2
                cv2.rectangle(frame, (int(respones['Left']*imgWidth),int(respones['Top']*imgHeight)),
                    (int((respones['Left']+respones['Width'])*imgWidth),
                    int((respones['Top']+respones['Height'])*imgHeight)), (0, 255, 0), 1)
            except:
                    # if model is not working or cannot find object in frame
                print('no label')

            ret, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()
            yield (b'--frame\r\n'
                    b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')  # concat frame one by one and show result

@app.route('/video_feed')
def video_feed():
    #Video streaming route. Put this in the src attribute of an img tag
    return Response(gen_frames(frame_rate, prev), mimetype='multipart/x-mixed-replace; boundary=frame')


@app.route('/')
def index():
    """Video streaming home page."""
    return render_template('index.html')


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')