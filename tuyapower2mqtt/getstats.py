#!/usr/bin/python
# TuyaPower2MQTT
# Python module to pull power & state data from Tuya WiFi smart devices with reporting via MQTT
#
# Author: Phill Healey

#import logging
#logging.basicConfig(filename='tuyapower2mqtt.log', filemode='w', level=logging.DEBUG)

import os
import sys

import tuyapower2mqtt

DEVICEID=sys.argv[1] if len(sys.argv) >= 2 else '-99'
DEVICEIP=sys.argv[2] if len(sys.argv) >= 3 else '-99'
DEVICEKEY=sys.argv[3] if len(sys.argv) >= 4 else '-99'
DEVICEVERS=sys.argv[4] if len(sys.argv) >= 5 else '3.1'

# Check for environmental variables and always use those if available (required for Docker)
PLUGID=os.getenv('PLUGID', DEVICEID)
PLUGIP=os.getenv('PLUGIP', DEVICEIP)
PLUGKEY=os.getenv('PLUGKEY', DEVICEKEY)
PLUGVERS=os.getenv('PLUGVERS', DEVICEVERS)
# how my times to try to probe plug before giving up
RETRY=5

# Setup MQTT server with your credentials
# EDIT THIS
MQTTSERVER="127.0.0.1"
MQTTUSER="homeassistant"
MQTTPASSWORD="homeassistant"
MQTTTOPIC="devices/tuya/plug/"
MQTTPORT=1883
# STOP EDITING

#tuyapower2mqtt.deviceInfo(PLUGID,PLUGIP,PLUGKEY,PLUGVERS)

responsejson = tuyapower2mqtt.deviceInfo(PLUGID,PLUGIP,PLUGKEY,PLUGVERS)
tuyapower2mqtt.pub_mqtt(PLUGID, responsejson)