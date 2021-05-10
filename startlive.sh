export GST_PLUGIN_PATH=`pwd`/
export LD_LIBRARY_PATH=`pwd`/open-source/local/lib
export AWS_DEFAULT_REGION=<your region>
gst-launch-1.0 v4l2src do-timestamp=TRUE device=/dev/video0 ! videoconvert ! video/x-raw,format=I420,width=640,height=480,framerate=30/1 ! omxh264enc control-rate=1 target-bitrate=5120000 periodicity-idr=45 inline-header=FALSE ! h264parse ! video/x-h264,stream-format=avc,alignment=au,width=640,height=480,framerate=30/1,profile=baseline ! kvssink stream-name="<your stream name>" access-key="<your access-key>" secret-key="your secret-key" aws-region="Your default region"
