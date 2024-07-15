from flask_socketio import SocketIO
import threading
import time

socketio = SocketIO()

# Global variables for queues and lock
buttons_queue = None
settings_queue = None
values_queue = None
lock = None

#function for setting queue and lock
def set_queues(b_queue, s_queue, v_queue, lk):
    global buttons_queue, settings_queue, values_queue, lock
    buttons_queue = b_queue
    settings_queue = s_queue
    values_queue = v_queue
    lock = lk

#function for sending message to websocket(py --> js)
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
                print(f'Format error: {val} -- {err}', flush=True)
            
        lock.release()
        time.sleep(2)

#function that received message when buttons is clicked and appends on buttons_queue the message "buttons/topic#value"
@socketio.on('buttons')
def websocket_buttons_message(message):
    print(f"Message: {message}", flush=True)
    try:
        spl = message.split('#')
        if len(spl) < 2:
            return
        topic = spl[0]
        value = spl[1]
        topic_mqtt = None
        if topic == "light":
            topic_mqtt = "buttons/light"
        elif topic == "temp":
            topic_mqtt = "buttons/temp"
        elif topic == "all":
            buttons_queue.append(("buttons/temp", value))    
            buttons_queue.append(("buttons/light", value))    
            return
        elif topic == "mode":
            topic_mqtt = "mode"
        if topic_mqtt != None: 
            buttons_queue.append((topic_mqtt, value))
    except ValueError:
        print(f'Format error: {message}', flush=True)
   
#function that received message when settings are changed and appends on settings_queue the message "settings/topic#value"
@socketio.on('settings')
def websocket_settings_message(message):
    print(f"Message: {message}", flush=True)
    try:
        spl = message.split('#')
        if len(spl) < 2:
            return
        topic = spl[0]
        value = spl[1]
        settings_queue.append((topic, value))
        print(f"Arrived message from : {topic} with content: {value}", flush=True)
    except ValueError:
        print(f'Format error: {message}', flush=True)

#Function that confirm the connection
@socketio.on('connect')
def websocket_connect():
    print("Connect", flush=True)
