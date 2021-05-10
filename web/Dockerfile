FROM python:3.8-slim-buster
WORKDIR /app
COPY requirements.txt requirements.txt
EXPOSE 5000
COPY . .
RUN python3 -m venv venv
RUN chmod 777 boot.sh
RUN chmod 777 app.py
ENTRYPOINT ["./boot.sh"]