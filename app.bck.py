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
topic ="topico"
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
    msg_count = 1
    while True:
        time.sleep(1)
        # msg = f"messages: {msg_count}"
        # result = client.publish(topic, msg)
        lock.acquire()
        global buttons_queue
        global settings_queue
        
        while len(buttons_queue) > 0:
            val = buttons_queue.pop(0)
            trim_val = val.split('=', 1)
            topic, value = trim_val
            print(f"send `{value}` from `{topic}` topic", flush=True)
            mqtt_client.publish(topic, value)
            time.sleep(0.5)

        while len(settings_queue) > 0:
            val = settings_queue.pop(0)
            trim_val = val.split('=', 1)
            topic, value = trim_val
            print(f"send `{value}` from `{topic}` topic", flush=True)
            mqtt_client.publish(topic, value)
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

    client.subscribe(topic)
    client.on_message = on_message


def run():
    client = connect_mqtt()
    subscribe(client)
    client.loop_forever()


#WebSocket Functions
@socketio.on('buttons')
def websocket_message(message):
    print(f"Arrivatototoaaaaaaaaaaaa: {message}", flush=True)
    try:
        topic, value = message.split('=')
        global buttons_queue
        print(f"{topic}, {value}", flush=True)
        buttons_queue.append((topic, value))
    except ValueError:
        print(f'Errore nel formato: {message}', flush=True)
    

@socketio.on('settings')
def websocket_message(message):
    print(f"Arrivatototo: {message}", flush=True)
    try:
        topic, value = message.split('=')
        global settings_queue
        settings_queue.append((topic, value))
    except ValueError:
        print(f'Errore nel formato: {message}')
    

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
   
    t_websocket = threading.Thread(target=send_message_websocket)
    t_websocket.start()

    return render_template("index.html")


if __name__ == '__main__':
    t = threading.Thread(target=run)
    t.start()

    socketio.run(app, host="0.0.0.0", allow_unsafe_werkzeug=True)
    
    
    #-----------------------------------
    #import os
#from flask import Flask, render_template
#from flask_socketio import SocketIO
#import threading
#from mqtt_handler import run as run_mqtt
#from websocket_handler import websocket_message_buttons, websocket_message_settings, send_message_websocket, websocket_connect
#
#template_dir = os.path.abspath("app/templates")
#static_dir   = os.path.abspath("app/static")
#
#app = Flask(__name__, template_folder=template_dir, static_url_path='', static_folder=static_dir)
#socketio = SocketIO(app)
#
#@app.route('/')
#def home():
#    t_websocket = threading.Thread(target=send_message_websocket)
#    t_websocket.start()
#    return render_template("index.html")
#
#if __name__ == '__main__':
#    t = threading.Thread(target=run_mqtt)
#    t.start()
#    socketio.run(app, host="0.0.0.0", allow_unsafe_werkzeug=True)
#
