#!/usr//bin/python

# Log MQTT sensor messages to a MongoDB database

import time
import json
import os
from datetime import datetime
import ConfigParser
import paho.mqtt.client as mqtt
import pymongo

dir = os.path.dirname(os.path.realpath(__file__))
config = ConfigParser.SafeConfigParser()
config.read(dir + '/application.cfg')

mqtt_broker = config.get('mqtt','broker')
database_url = config.get('database','url')
database_name = config.get('database','name')
database_log_rate = int(config.get('database','log_rate'))

db_connection = pymongo.MongoClient(database_url)
db = db_connection[database_name]
db.readings.ensure_index('datetime')

# Maps sensor location + type to timestamp, used to control logging rate
previous_times = {}

def on_message(client, userdata, msg):
    data = json.loads(msg.payload)
    dtime = datetime.strptime(data['datetime'], '%Y-%m-%d %H:%M:%S.%f')
    data['datetime'] = dtime

    # Limit logging rate for each sensor to once per database_log_rate seconds
    key = data['location'] + '#' + data['type']
    previous_time = previous_times.get(key)
    if previous_time == None or (dtime - previous_time).total_seconds() > database_log_rate:
        print 'Inserting'
        db.readings.insert(data)
        previous_times[key] = dtime

mqtt_client = mqtt.Client()
mqtt_client.on_message = on_message
mqtt_client.connect(mqtt_broker)
mqtt_client.subscribe('sensor/#')
mqtt_client.loop_forever()
