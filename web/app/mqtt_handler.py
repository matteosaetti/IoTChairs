import threading
import time
from paho.mqtt import client as mqtt_client

#broker = '192.168.18.24'
broker = '192.168.1.114'
port = 1883
#topic = "topico"

light_topic = "sensor/light"
temp_topic = "sensor/temp"
pressure_topic ="sensor/pressure"

client_id = f'python-mqtt-xxx'

lock = threading.Lock()
values_queue = []
buttons_queue = []
settings_queue = []

def connect_mqtt():
    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            print("Connected to MQTT Broker!", flush=True)
        else:
            print("Failed to connect, return code %d\n", rc, flush=True)
    
    client = mqtt_client.Client(client_id)
    client.on_connect = on_connect
    client.connect(broker, port)
    return client

def publish(client):
    while True:
        time.sleep(1)
        lock.acquire()
        global buttons_queue, settings_queue

        while len(buttons_queue) > 0:
            val = buttons_queue.pop(0)
            topic, value = val
            print(f"send `{value}` from `{topic}` topic", flush=True)
            client.publish(topic, value)
            time.sleep(0.5)

        while len(settings_queue) > 0:
            val = settings_queue.pop(0)
            topic, value = val
            print(f"send `{value}` from `{topic}` topic", flush=True)
            client.publish(topic, value)
            time.sleep(0.5)
        
        lock.release()
        time.sleep(2)

def subscribe(client):
    def on_message(client, userdata, msg):
        mess = msg.payload.decode()
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
    threading.Thread(target=publish, args=(client,)).start()
    client.loop_forever()
