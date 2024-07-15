import time
from paho.mqtt import client as mqtt_client
import threading

#Mqtt broker
broker = '172.20.10.5'
port = 1883

#topic
light_topic = "sensor/light"
temp_topic = "sensor/temp"
pressure_topic = "sensor/pressure"

client_id = f'python-mqtt-xxx'

#Mqtt connection function
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

#Mqtt public function
def publish(client, buttons_queue, settings_queue, lock):
    while True:
        time.sleep(1)
        lock.acquire()
        while len(buttons_queue) > 0:
            spl = buttons_queue.pop(0)
            topic = spl[0]
            value = spl[1]
            print(f"send `{value}` to `{topic}`", flush=True)
            client.publish(topic, value)
            time.sleep(0.2)
            
        while len(settings_queue) > 0:
            spl = settings_queue.pop(0)
            topic = spl[0]
            value = spl[1]
            print(f"send `{value}` to `{topic}`", flush=True)
            client.publish(topic, value)
            time.sleep(0.2)
                
        lock.release()
        time.sleep(2)
        
#Mqtt subscribe funtion
def subscribe(client, values_queue, lock):
    def on_message(client, userdata, msg):
        mess = msg.payload.decode()
        print(f"Received `{mess}` from `{msg.topic}` topic", flush=True)
        lock.acquire()
        values_queue.append(mess)
        lock.release()
        print(values_queue, flush=True)

    client.subscribe(light_topic)
    client.subscribe(temp_topic)
    client.subscribe(pressure_topic)
    client.on_message = on_message


def run_mqtt_client(values_queue, buttons_queue, settings_queue, lock):
    client = connect_mqtt()
    subscribe(client, values_queue, lock)
    threading.Thread(target=publish, args=(client, buttons_queue, settings_queue, lock)).start()
    client.loop_forever()
