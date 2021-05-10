sudo apt-get install -y libssl-dev libcurl4-openssl-dev liblog4cplus-dev libgstreamer1.0-dev libgstreamer-plugins-base1.0-dev gstreamer1.0-plugins-base-apps gstreamer1.0-plugins-bad gstreamer1.0-plugins-good gstreamer1.0-plugins-ugly gstreamer1.0-tools git
git clone https://github.com/awslabs/amazon-kinesis-video-streams-producer-sdk-cpp.git
sudo apt-get install -y openjdk-11-jdk
sudo apt-get install -y default-jdk
cd amazon-kinesis-video-streams-producer-sdk-cpp/
export JAVA_HOME=/usr/lib/jvm/java-11-openjdk-amd64
cmake -DBUILD_GSTREAMER_PLUGIN=ON -DBUILD_JNI=TRUE
make