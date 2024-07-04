from flask_socketio import SocketIO
import threading
import time

socketio = SocketIO()

# Global variables for queues and lock
buttons_queue = None
settings_queue = None
values_queue = None
lock = None

def set_queues(b_queue, s_queue, v_queue, lk):
    global buttons_queue, settings_queue, values_queue, lock
    buttons_queue = b_queue
    settings_queue = s_queue
    values_queue = v_queue
    lock = lk

def send_message_websocket(values_queue, lock):
    while True:
        lock.acquire()
        while len(values_queue) > 0:
            try:
                val = values_queue.pop(0)
                spl = val.split('#', 1)
                if len(spl) < 2:
                    continue
                val_topic = spl[0]
                value = spl[1] 
                print(f"Sending to websocket: {val}", flush=True)
                socketio.emit(val_topic, value)
                time.sleep(0.2)
            except ValueError as err:
                print(f'Errore nel formato: {val} -- {err}', flush=True)
            
        lock.release()
        time.sleep(2)

@socketio.on('buttons')
def websocket_buttons_message(message):
    print(f"Arrivato: {message}", flush=True)
    try:
        spl = message.split('#')
        if len(spl) < 2:
            return
        topic = spl[0]
        value = spl[1]
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
        if topic_mqtt != None: 
            buttons_queue.append((topic_mqtt, value))
    except ValueError:
        print(f'Errore nel formato: {message}', flush=True)
    
@socketio.on('settings')
def websocket_settings_message(message):
    print(f"Arrivato: {message}", flush=True)
    try:
        spl = message.split('#')
        if len(spl) < 2:
            return
        topic = spl[0]
        value = spl[1]
        settings_queue.append((topic, value))
        print(f"Arrivato mess da : {topic} con contenuto {value}", flush=True)
    except ValueError:
        print(f'Errore nel formato: {message}', flush=True)

@socketio.on('connect')
def websocket_connect():
    print("Connesso", flush=True)
