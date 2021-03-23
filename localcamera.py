import cv2
import boto3
import base64

cam = cv2.VideoCapture(1,cv2.CAP_DSHOW)
cam.set(cv2.CAP_PROP_FRAME_WIDTH, 1920)
cam.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)
rekognition = boto3.client('rekognition')

def labelDetection(frame):
    ret, buf = cv2.imencode('.jpg', frame) 
    response = rekognition.detect_custom_labels(
        ProjectVersionArn='arn:aws:rekognition:us-east-1:046183741095:project/track_detect/version/track_detect.2021-01-11T19.39.43/1610365182453',
        Image={
            'Bytes': buf.tobytes(),
        },
        MinConfidence=95
    )
    return response

def show_webcam():
    while True:
        ret_val, frame = cam.read()
        try:
            resp = labelDetection(frame)
        
            imgHeight, imgWidth, channels = frame.shape
            # print(imgHeight,imgWidth)
            respones = resp['CustomLabels'][0]['Geometry']['BoundingBox']
            # print(respones)
            cv2.rectangle(frame, (int(respones['Left']*imgWidth),int(respones['Top']*imgHeight)),
            (int((respones['Left']+respones['Width'])*imgWidth),
            int((respones['Top']+respones['Height'])*imgHeight)), (0, 255, 0), 1)
            cv2.imshow('my webcam', frame)
        except:
            print('no label')
            cv2.imshow('my webcam', frame)
        if cv2.waitKey(1) == 27: 
            break  # esc to quit
    cv2.destroyAllWindows()

def main():
    show_webcam()

if __name__ == '__main__':
    main()

    