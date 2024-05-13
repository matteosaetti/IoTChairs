import os
import json

def valida_config(mqtt_address, mqtt_port):
    return \
        mqtt_address != "" and \
        mqtt_port    != ""

config_filename = os.path.abspath("mqtt_config.json")
file = open(config_filename)
config = json.load(file)

mqtt_address = config['mqtt']['address']
mqtt_port    = config['mqtt']['port']

if(not valida_config(mqtt_address, mqtt_port)):
    raise ConfigException("MQTT config error")