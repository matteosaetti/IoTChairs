from paho.mqtt import client as mqtt_client
import time
from app import get_lock

broker = '192.168.18.24'
port = 1883
topic ="topico"
light_topic = "sensor/light"
temp_topic = "sensor/temp"
pressure_topic ="sensor/pressure"
client_id = f'python-mqtt-xxx'

values_queue = []
lock = get_lock()

def get_queue_values():
    return values_queue

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
        result = client.publish(light_topic, msg)
        result = client.publish(temp_topic, msg)
        result = client.publish(pressure_topic, msg)

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
    client.subscribe(light_topic)
    client.subscribe(temp_topic)
    client.subscribe(pressure_topic)
    client.on_message = on_message
    
def run():
    client = connect_mqtt()
    #client.loop_start()
    #publish(client)
    subscribe(client)
    client.loop_forever()
