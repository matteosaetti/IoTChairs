import os
from flask import Flask, jsonify, request, render_template
from flask_socketio import SocketIO
import threading
import time
import mqtt
#per la network
# docker network create --driver=bridge --subnet=172.42.0.0/24 --gateway=172.42.0.1 docker_net

template_dir = os.path.abspath("app/templates")
static_dir   = os.path.abspath("app/static")

app = Flask(__name__, template_folder=template_dir,static_url_path='', static_folder=static_dir)
socketio = SocketIO(app)

lock = threading.Lock()

def get_lock():
    return lock

#websocket functions
@socketio.on('message')
def websocket_message(message):
    print(f"Arrivatototo: {message}", flush=True)


def send_message_websocket():
    while True:
        lock.acquire()
        values_queue = mqtt.get_queue_values()
        while len(values_queue) > 0:
            val = values_queue.pop(0)
            # trim_val = val.split('#', 1)
            # topic, value = trim_val
            # print("topic, value ", topic, value, flush=True)
            print(f"Sending to websocket: {val}", flush=True)
            socketio.emit("message", val)
            time.sleep(0.5)
        lock.release()
        time.sleep(2)


@socketio.on('connect')
def websocket_connect():
    print("Connectato", flush=True)

@app.route('/')
def home():
    t = threading.Thread(target=mqtt.run)
    t.start()

    t_websocket = threading.Thread(target=send_message_websocket)
    t_websocket.start()

    return render_template("index.html")

if __name__ == '__main__':
    #app.run(host="0.0.0.0", port=5000, threaded=True)
    socketio.run(app, host="0.0.0.0", allow_unsafe_werkzeug=True)
