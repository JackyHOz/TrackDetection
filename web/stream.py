import boto3
import cv2
import logging
import ffmpeg_streaming
from ffmpeg_streaming import Formats
import os
import fnmatch

STREAM_NAME = "testing"
kvs = boto3.client("kinesisvideo", region_name='ap-southeast-1')

# Get the endpoint from GetDataEndpoint
endpoint = kvs.get_data_endpoint(
    APIName="GET_HLS_STREAMING_SESSION_URL",
    StreamName=STREAM_NAME
)['DataEndpoint']

# make folder to save hls's files
os.mkdir('./outimages')
# print(endpoint)

rekognition = boto3.client('rekognition')

# call the model to label images
def labelDetection(frame):
    ret, buf = cv2.imencode('.jpg', frame) 
    response = rekognition.detect_custom_labels(
        # find project arn in console
        ProjectVersionArn='arn:aws:rekognition:ap-southeast-1:046183741095:project/DeepRacer_Detection/version/DeepRacer_Detection.2021-04-01T23.46.23/1617291982531',
        Image={
            'Bytes': buf.tobytes(),
        },
        MinConfidence=95
    )
    return response

# Get the HLS Stream URL from the endpoint
kvam = boto3.client("kinesis-video-archived-media", endpoint_url=endpoint)
url = kvam.get_hls_streaming_session_url(
    StreamName=STREAM_NAME,
    PlaybackMode="LIVE"
)['HLSStreamingSessionURL']

s3_client = boto3.client('s3')
# use cv2 capture frames from kvs
vcap = cv2.VideoCapture(url)
vcap.set(cv2.CAP_PROP_BUFFERSIZE, 1)

while(True):
    # Capture frame-by-frame
    ret, frame = vcap.read()

    # if frame is not None:
    #     # Display the resulting frame
    #     # cv2.imshow('frame',frame)

    #     # Press q to close the video windows before it ends if you want
    #     if cv2.waitKey(22) & 0xFF == ord('q'):
    #         break
    # else:
    #     print("Frame is None")
    #     break

    try:
        resp = labelDetection(frame)
        
        imgHeight, imgWidth, channels = frame.shape
        # print(imgHeight,imgWidth)
        respones = resp['CustomLabels'][0]['Geometry']['BoundingBox']
        # print(respones)
        # draw the bounding box through cv2
        cv2.rectangle(frame, (int(respones['Left']*imgWidth),int(respones['Top']*imgHeight)),
            (int((respones['Left']+respones['Width'])*imgWidth),
            int((respones['Top']+respones['Height'])*imgHeight)), (0, 255, 0), 1)
        #cv2.imshow('my webcam', frame)

        # retval, buffer = cv2.imencode('.jpg', frame)
        # jpg_as_text = base64.b64encode(buffer)

        # s3_client.put_object(Key = 'outimages/img.jpg', Body = buffer.tobytes(), Bucket = '')
        


        # if cv2.waitKey(22) & 0xFF == ord('q'):
        #     break
    except:
        # if model is not working or cannot find object in frame
        print('no label')
        #cv2.imshow('my webcam', frame)
        # retval, buffer = cv2.imencode('.jpg', frame)
        # jpg_as_text = base64.b64encode(buffer)
        # s3_client.put_object(Key = 'outimages/img.jpg', Body = buffer.tobytes(), Bucket = '')
    
    # output video using XVID 
    fourcc = cv2.VideoWriter_fourcc(*'XVID')

    # Use VideoWriter to create video，output video called output.avi
    # FPS is 20.0，resolution is 640x360
    out = cv2.VideoWriter('output.avi', fourcc, 1.0, (1280, 720))
    out.write(frame)
out.release()
    #create hls file from output video
video = ffmpeg_streaming.input('output.avi')
hls = video.hls(Formats.h264())
hls.auto_generate_representations()

    # dash = video.dash(Formats.h264())
    # dash.auto_generate_representations()
    # dash.output('dash.mpd')

    # try:
    # hls.output('hls.m3u8')
    
hls.output('./outimages/hls.m3u8')
    # print('test')
    # s3_client = boto3.client('s3')
    # upload hls to s3
for dirPath, dirNames, fileNames in os.walk('./outimages'):
    # print(fileNames)
    for picture in fnmatch.filter(fileNames, '*'):
        s3_client.upload_file('outimages/' + picture, 'realtimeoutputlabeled',
                        'outimages/' + str(picture))

    # except:
        #upload hls to s3 


# When everything done, release the capture
vcap.release()
cv2.destroyAllWindows()
# print("Video stop")