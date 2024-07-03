import threading
import time
from flask_socketio import SocketIO, emit

#TODO: problema con i topic => mancano :) 

lock = threading.Lock()
values_queue = []

buttons_queue = []
settings_queue = []

def websocket_message_buttons(message):
    print(f"Arrivatototoaaaaaaaaaaaa: {message}", flush=True)
    try:
        topic, value = message.split('=')
        global buttons_queue
        print(f"{topic}, {value}", flush=True)
        buttons_queue.append((topic, value))
    except ValueError:
        print(f'Errore nel formato: {message}', flush=True)

def websocket_message_settings(message):
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
            val_topic, value = val.split('#', 1)
            print(f"Sending to websocket: {val}", flush=True)
            emit(val_topic, value)
            time.sleep(0.5)
        lock.release()
        time.sleep(2)

def websocket_connect():
    print("Connectato", flush=True)
