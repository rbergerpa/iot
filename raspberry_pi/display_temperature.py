#!/usr/bin/python

# Display temperature readings from an MQTT topic to an Adafruit 7 segment display

import os
import sys
import time
import json
from datetime import datetime
import ConfigParser
import paho.mqtt.client as mqtt
from Adafruit_LED_Backpack import SevenSegment

# TODO move these to config file
max_age = 600
brightness=4  # 15 = max
display_address = 0x71

msg_time = datetime.now()

dir = os.path.dirname(os.path.realpath(__file__))
config = ConfigParser.SafeConfigParser()
config.read(dir + '/application.cfg')
mqtt_broker = config.get('mqtt','broker')
mqtt_topic = config.get('display_temperature', 'topic')


def on_message(client, userdata, msg):
    global msg_time
    msg_time = datetime.now()
    data = json.loads(msg.payload)
    temperature = data['value']

    display.clear()
    display.print_number_str('%d ' % round(temperature))
    display.set_digit_raw(3, 0x63) # degree symbol
    display.write_display()

display = SevenSegment.SevenSegment(address = display_address)
display.begin()
display.set_brightness(brightness)
display.clear()
display.write_display()

mqtt_client = mqtt.Client()
mqtt_client.on_message = on_message
mqtt_client.connect(mqtt_broker)
mqtt_client.subscribe(mqtt_topic)

while True:
    mqtt_client.loop()

    # Clear display and exit if we haven't gotten a message for a while
    if (datetime.now() - msg_time).total_seconds() > max_age:
        display.clear()
        display.write_display()
        sys.exit(0)
