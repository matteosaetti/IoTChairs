import os
from flask import Flask, jsonify, request, render_template
from flask_socketio import SocketIO
import json
import threading
import time
from paho.mqtt import client as mqtt_client
#per la network
# docker network create --driver=bridge --subnet=172.42.0.0/24 --gateway=172.42.0.1 docker_net


broker = '192.168.1.176'
port = 1883
topic ="topico"
light_topic = "light_status"
temp_topic = "light_status"
client_id = f'python-mqtt-xxx'



template_dir = os.path.abspath("app/templates")
static_dir   = os.path.abspath("app/static")

app = Flask(__name__, template_folder=template_dir,static_url_path='', static_folder=static_dir)
socketio = SocketIO(app)

lock = threading.Lock()
values_queue = []

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
    msg_count = 1
    while True:
        time.sleep(1)
        msg = f"messages: {msg_count}"
        result = client.publish(topic, msg)


def subscribe(client: mqtt_client):
    def on_message(client, userdata, msg):
        mess = msg.payload.decode()#.split(':')[1].split('"')[1]
        print(f"Received `{mess}` from `{msg.topic}` topic", flush=True)
        lock.acquire()
        global values_queue
        values_queue.append(mess)
        lock.release()
        print(values_queue, flush=True)

    client.subscribe(topic)
    client.on_message = on_message


def run():
    client = connect_mqtt()
    #client.loop_start()
    #publish(client)
    subscribe(client)
    client.loop_forever()


#WebSocket Functions
@socketio.on('message')
def websocket_message(message):
    print(f"Arrivatototo: {message}", flush=True)


def send_message_websocket():
    while True:
        lock.acquire()
        global values_queue
        while len(values_queue) > 0:
            val = values_queue.pop(0)
            trim_val = val.split('#', 1)
            val_topic, value = trim_val
            print(f"Sending to websocket: {val}", flush=True)
            socketio.emit(val_topic, value)
            time.sleep(0.5)
        lock.release()
        time.sleep(2)


@socketio.on('connect')
def websocket_connect():
    print("Connectato", flush=True)

@app.route('/')
def home():
    t = threading.Thread(target=run)
    t.start()

    t_websocket = threading.Thread(target=send_message_websocket)
    t_websocket.start()

    return render_template("index.html")

if __name__ == '__main__':
    #app.run(host="0.0.0.0", port=5000, threaded=True)
    socketio.run(app, host="0.0.0.0", allow_unsafe_werkzeug=True)