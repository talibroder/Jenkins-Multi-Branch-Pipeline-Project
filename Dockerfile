
FROM python:slim

WORKDIR /app

COPY . /app

RUN pip install --no-cache-dir -r requirements.txt

RUN pip install gunicorn

EXPOSE 5000
EXPOSE 8000

ENV NAME World

CMD ["gunicorn", "weather_deploy:app", "-b", "0.0.0.0:5000"]
