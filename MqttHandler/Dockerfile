FROM python:3.8-slim

WORKDIR /

WORKDIR /MqttHandler/app

COPY /MqttHandler/app/requirementsMqtt.txt .

# COPY /MqttHandler/mosquitto.conf /

RUN pip install -r requirementsMqtt.txt

COPY /MqttHandler/app .

CMD ["python", "app.py"]