# Stage 1: Build stage!

FROM python:3.9-slim as builder

WORKDIR /weather_app

COPY . .

RUN pip install --no-cache-dir --upgrade -r requirements.txt && rm -f requirements.txt

RUN pip install gunicorn


EXPOSE 5000

CMD gunicorn --bind 0.0.0.0:5000 weather_deploy:app 


