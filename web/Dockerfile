FROM python:3.8-slim-buster
WORKDIR /app
COPY requirements.txt requirements.txt
EXPOSE 5000
COPY . .
# CMD [ "python3", "-m" , "flask", "run", "--host=0.0.0.0"]
# RUN apt-get update ##[edited]
# RUN apt-get install ffmpeg libsm6 libxext6 libx264-dev -y
RUN python3 -m venv venv
# RUN pip3 install -r requirements.txt
# COPY stream.py stream.py
# COPY app.py app.py
# COPY templates ./
# COPY boot.sh boot.sh
RUN chmod 777 boot.sh
RUN chmod 777 app.py

ENTRYPOINT ["./boot.sh"]