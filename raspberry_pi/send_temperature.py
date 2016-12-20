#!/usr//bin/python

# Send temperature readings to a MQTT topic

import os
import time
import json
from datetime import datetime
import ConfigParser
import paho.mqtt.client as mqtt
from ds18b20 import DS18B20

delay = 30.0

dir = os.path.dirname(os.path.realpath(__file__))
config = ConfigParser.SafeConfigParser()
config.read(dir + '/application.cfg')
mqtt_broker = config.get('mqtt','broker')

sensor_locations = {}
sensors = {}
for id, location in config.items('sensors'):
    sensor_locations[id] = location
    sensors[id] = DS18B20(id)


mqtt_client = mqtt.Client()
mqtt_client.connect(mqtt_broker)
mqtt_client.loop_start()

while True:
    for id in sensor_locations.keys():
        location = sensor_locations[id]
        topic =  "sensor/temperature/" + location
        temperature = sensors[id].read_fahrenheit()
        msg = json.dumps({ 'location' : location, 'datetime':  str(datetime.now()), 'type': 'temperature', 'value': temperature })
        mqtt_client.publish(topic, msg)

    time.sleep(delay)
