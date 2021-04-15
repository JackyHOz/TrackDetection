FROM python:3.8-buster
COPY requirements.txt requirements.txt
RUN apt-get update ##[edited]
RUN apt-get install ffmpeg libsm6 libxext6 libx264-dev -y
RUN python3 -m venv venv
COPY stream.py stream.py
COPY boot.sh boot.sh
RUN chmod 777 boot.sh
RUN chmod 777 stream.py
WORKDIR /
ENTRYPOINT ["./boot.sh"]