#!/usr//bin/python
import time
import json
from datetime import datetime
import paho.mqtt.client as mqtt
from ds18b20 import DS18B20

# TODO move this to a config fie
device_locations = { '28-000003cb57a4': 'ny/outdoor',  '28-0000044b383b': 'ny/den' }
mqtt_host = '127.0.0.1'

delay = 30.0

device_ids = device_locations.keys()
sensors = {}
for id in device_ids:
    sensors[id] = DS18B20(id)

mqtt_client = mqtt.Client()
mqtt_client.connect(mqtt_host)
mqtt_client.loop_start()

while True:
    for id in device_ids:
        location = device_locations[id]
        topic =  "sensor/temperature/" + location
        temperature = sensors[id].read_fahrenheit()
        msg = json.dumps({ 'location' : location, 'datetime':  str(datetime.now()), 'type': 'temperature', 'value': temperature })
        mqtt_client.publish(topic, msg)

    time.sleep(delay)


