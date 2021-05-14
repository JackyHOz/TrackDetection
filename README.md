# TrackDetection
Prequisite and Remarks:  
A running model is required. Numbers of attributes needs to be replaced in the files before running, which are described as follows.  
The unfinished transform.py is also included, which is for transforming the image of the track that is taken at a random angle, into an angle of top view. 
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
cd ..  
cd cdk/  
cdk deploy --all  
**(may be)press 'y' to continue**  

Finally, use Load balancer's DNS to visit webpage  
You also can update resolution in the startlive.sh
