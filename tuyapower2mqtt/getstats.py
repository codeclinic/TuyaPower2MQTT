#!/usr/bin/python
# TuyaPower2MQTT
# Python module to pull power & state data from Tuya WiFi smart devices with reporting via MQTT
#
# Author: Phill Healey

#import pycrypto
#import Crypto
#import paes
#import pytuya
#import paho.mqtt.client as mqtt

#import datetime
#import time
import os
import sys
#from time import sleep

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

tuyapower2mqtt.deviceInfo(PLUGID,PLUGIP,PLUGKEY,PLUGVERS)

#responsejson = tuyapower2mqtt.deviceInfo(PLUGID,PLUGIP,PLUGKEY,PLUGVERS)
#print(responsejson)