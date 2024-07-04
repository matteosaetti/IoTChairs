import os
from flask import Flask, render_template
from flask_socketio import SocketIO
import threading

from mqtt_handler import run_mqtt_client
from websocket_handler import socketio, set_queues, send_message_websocket

template_dir = os.path.abspath("app/templates")
static_dir = os.path.abspath("app/static")

app = Flask(__name__, template_folder=template_dir, static_url_path='', static_folder=static_dir)
socketio.init_app(app)

lock = threading.Lock()
values_queue = []
buttons_queue = []
settings_queue = []

# Pass the queues to the WebSocket server
set_queues(buttons_queue, settings_queue, values_queue, lock)

@app.route('/')
def home():
    t_websocket = threading.Thread(target=send_message_websocket, args=(values_queue, lock))
    t_websocket.start()
    return render_template("index.html")

if __name__ == '__main__':
    t = threading.Thread(target=run_mqtt_client, args=(values_queue, buttons_queue, settings_queue, lock))
    t.start()

    socketio.run(app, host="0.0.0.0", allow_unsafe_werkzeug=True)
