# TrackDetection

## For draw the trail
git clone https://github.com/JackyHOz/TrackDetection.git
cd TrackDetection/
**update bucket name, prefix and model arn**
python DrawTrail.py

## For real time streaming
git clone https://github.com/JackyHOz/TrackDetection.git
cd TrackDetection/
./deploy.sh
**update your access key ,secret key , region and stream name in startlive.sh**
./startlive.sh


cd web/
**update stream name, region and model arn in app.py**
cd cdk/
cdk deploy --all
**(may be)press 'y' to continue**

Finally, use Load balancer's DNS to visit webpage