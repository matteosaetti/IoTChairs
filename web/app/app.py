import os
from flask import Flask, jsonify, render_template
import json
import threading
import time
import paho.mqtt.client as mqtt
# docker network create --driver=bridge --subnet=172.42.0.0/24 --gateway=172.42.0.1 docker_net
template_dir = os.path.abspath("app/templates")
static_dir   = os.path.abspath("app/static")
app = Flask(__name__, template_folder=template_dir,static_url_path='', static_folder=static_dir)

sensor_data = {
    'pressureValue1': 'No',
    'pressureValue2': 'No',
    'light': 0,
    'temperature': 0
}

def on_connect(client, userdata, flags, rc):
    print(f"Connesso al broker MQTT con codice {rc}")
    client.subscribe("/pressureValue1")
    client.subscribe("/pressureValue2")
    client.subscribe("/light")
    client.subscribe("/temperature")

def on_message(client, userdata, msg):
    global sensor_data
    try:
        value = msg.payload.decode()
        if msg.topic == "/pressureValue1":
            sensor_data['pressureValue1'] = value
        elif msg.topic == "/pressureValue2":
            sensor_data['pressureValue2'] = value
        elif msg.topic == "/light":
            sensor_data['light'] = int(value)
        elif msg.topic == "/temperature":
            sensor_data['temperature'] = int(value)
    except ValueError:
        print(f"Messaggio non è un valore valido: {msg.payload.decode()}")

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
client.connect("localhost", 1883, 60)

def mqtt_loop():
    client.loop_start()
    while True:
        time.sleep(1)

mqtt_thread = threading.Thread(target=mqtt_loop)
mqtt_thread.start()

@app.route('/')
def home():
    return render_template("index.html")

@app.route('/settings')
def settings():
    return render_template('settings.html')

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)
