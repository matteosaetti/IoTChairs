import os
from flask import Flask, jsonify, request, render_template
from flask_socketio import SocketIO
import json
import threading
import time
from paho.mqtt import client as mqtt_client
#per la network
# docker network create --driver=bridge --subnet=172.42.0.0/24 --gateway=172.42.0.1 docker_net


broker = '192.168.18.24'
port = 1883
light_topic = "sensor/light"
temp_topic = "sensor/temp"
pressure_topic ="sensor/pressure"
client_id = f'python-mqtt-xxx'



template_dir = os.path.abspath("app/templates")
static_dir   = os.path.abspath("app/static")

app = Flask(__name__, template_folder=template_dir,static_url_path='', static_folder=static_dir)
socketio = SocketIO(app)

lock = threading.Lock()
values_queue = []

buttons_queue = []
settings_queue = []


#MQTT Functions
def connect_mqtt():
    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            print("Connected to MQTT Broker!", flush=True)
        else:
            print("Failed to connect, return code %d\n", rc, flush=True)
    # Set Connecting Client ID
    client = mqtt_client.Client(client_id)
    client.on_connect = on_connect
    client.connect(broker, port)
    return client


def publish(client):
    while True:
        time.sleep(1)
        lock.acquire()
        while len(buttons_queue) > 0:
            topic, value = buttons_queue.pop(0)
            print(f"send `{value}` to `{topic}` topic", flush=True)
            client.publish(topic, value)
            time.sleep(0.5)
        while len(settings_queue) > 0:
            topic, value = settings_queue.pop(0)
            print(f"send `{value}` to `{topic}` topic", flush=True)
            client.publish(topic, value)
            time.sleep(0.5)
        lock.release()
        time.sleep(2)


def subscribe(client: mqtt_client):
    def on_message(client, userdata, msg):
        mess = msg.payload.decode()#.split(':')[1].split('"')[1]
        print(f"Received `{mess}` from `{msg.topic}` topic", flush=True)
        lock.acquire()
        global values_queue
        values_queue.append(mess)
        lock.release()
        print(values_queue, flush=True)

    client.subscribe(light_topic)
    client.subscribe(temp_topic)
    client.subscribe(pressure_topic)
    client.on_message = on_message


def run():
    client = connect_mqtt()
    subscribe(client)
    client.loop_forever()


#WebSocket Functions
@socketio.on('buttons')
def websocket_buttons_message(message):
    print(f"Arrivato: {message}", flush=True)
    try:
        spl = message.split('#')
        if len(spl) < 2:
            return
        topic, value = spl
        topic_mqtt = None
        if topic == "light":
            topic_mqtt = "sensor/light"
        elif topic == "temp":
            topic_mqtt = "sensor/temp"
        elif topic == "all":
            buttons_queue.append(("sensor/temp", value))    
            buttons_queue.append(("sensor/light", value))    
            return
        elif topic == "mode":
            topic_mqtt = "mode"
        if not topic_mqtt: 
            buttons_queue.append((topic_mqtt, value))
    except ValueError:
        print(f'Errore nel formatoto: {message}', flush=True)


@socketio.on('settings')
def websocket_settings_message(message):
    print(f"Arrivato: {message}", flush=True)
    try:
        spl = message.split('#')
        if len(spl) < 2:
            return
        topic, value = spl
        topic, value = message.split('#')
        settings_queue.append((topic, value))
        print(f"Arrivato mess da : {topic} con contenuto {value}", flush=True)
    except ValueError:
        print(f'Errore nel formato: {message}', flush=True)


def send_message_websocket():
    while True:
        lock.acquire()
        global values_queue
        while len(values_queue) > 0:
            val = values_queue.pop(0)
            try:
                trim_val = val.split('#')
                val_topic, value = trim_val
                print(f"Sending to websocket: {val}", flush=True)
                socketio.emit(val_topic, value)
                time.sleep(0.5)
            except ValueError:
                print(f'Errore nel formato: {val}', flush=True)

        lock.release()
        time.sleep(2)


@socketio.on('connect')
def websocket_connect():
    print("Connectato", flush=True)

@app.route('/')
def home():
   
    t_websocket = threading.Thread(target=send_message_websocket)
    t_websocket.start()

    return render_template("index.html")


if __name__ == '__main__':
    t = threading.Thread(target=run)
    t.start()

    socketio.run(app, host="0.0.0.0", allow_unsafe_werkzeug=True)