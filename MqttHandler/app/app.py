
import paho.mqtt.client as mqtt
import time

import mqtt_config_reader as mcr


client = None
reconnect = True


def startListening():
    print("start listening", flush=True)

def connect():
    return client.connect(mcr.mqtt_address, int(mcr.mqtt_port), 60)

def on_connect():
    print("MQTT Connected.", flush=True)

def onDisconnect():
    print("Disconnected", flush=True)
    # if(reconnect): connect()

# def onPublish():
#     print("Published MQTT", flush=True)

def setup():
    # client.on_connect = on_connect
    # client.on_disconnect = onDisconnect
    if connect() != 0: print("Can't connect", flush=True)
    client.loop_start()
    startListening()


def publishMQTT():
    pass

if __name__ == "__main__":
    print("Avvio MQTTHandler", flush=True)

    client = mqtt.Client()
    setup()
    startListening()
