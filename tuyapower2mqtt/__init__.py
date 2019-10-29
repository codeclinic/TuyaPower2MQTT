#!/usr/bin/python
# TuyaPower2MQTT
# Python module to pull power & state data from Tuya WiFi smart devices with reporting via MQTT
#
# Author: Phill Healey

name = "tuyapower2mqtt"

import pycrypto
import pycryptodome
import paes
import pytuya
import paho.mqtt.client as mqtt

import datetime
import time
import os
import sys
from time import sleep

DEVICEID=sys.argv[1] if len(sys.argv) >= 2 else '01234567891234567890'
DEVICEIP=sys.argv[2] if len(sys.argv) >= 3 else '012.345.678.910'
DEVICEKEY=sys.argv[3] if len(sys.argv) >= 4 else '0123456789abcdef'
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
MQTTTOPIC="sensor/tuya/DEVICEID/" #trailing slash is receommended
MQTTPORT="1883"
# STOP EDITING

def deviceInfo( deviceid, ip, key, vers ):
    watchdog = 0
    now = datetime.datetime.utcnow()
    iso_time = now.strftime("%Y-%m-%dT%H:%M:%SZ") 
    while True:
        try:
            d = pytuya.OutletDevice(deviceid, ip, key)
            if vers == '3.3':
                d.set_version(3.3)

            data = d.status()
            if(d):
                sw =data['dps']['1']

                if vers == '3.3':
                    if '19' in data['dps'].keys():
                        w = (float(data['dps']['19'])/10.0)
                        mA = float(data['dps']['18'])
                        V = (float(data['dps']['20'])/10.0)
                        ret = "{ \"datetime\": \"%s\", \"switch\": \"%s\", \"power\": \"%s\", \"current\": \"%s\", \"voltage\": \"%s\" }" % (iso_time, sw, w, mA, V)

                        pub_mqtt( w, mA, V )

                        return(ret)
                    else:
                        ret = "{ \"switch\": \"%s\" }" % sw
                        return(ret)
                else:
                    if '5' in data['dps'].keys():
                        w = (float(data['dps']['5'])/10.0)
                        mA = float(data['dps']['4'])
                        V = (float(data['dps']['6'])/10.0)
                        ret = "{ \"datetime\": \"%s\", \"switch\": \"%s\", \"power\": \"%s\", \"current\": \"%s\", \"voltage\": \"%s\" }" % (iso_time, sw, w, mA, V)

                        pub_mqtt( w, mA, V )

                        return(ret)
                    else:
                        ret = "{ \"switch\": \"%s\" }" % sw
                        return(ret)
            else:
                ret = "{\"result\": \"Incomplete response from plug %s [%s].\"}" % (deviceid,ip)
                return(ret)
            break
        except KeyboardInterrupt:
            pass
        except:
            watchdog+=1
            if(watchdog>RETRY):
                ret = "{\"result\": \"ERROR: No response from plug %s [%s].\"}" % (deviceid,ip)
                return(ret)
            sleep(2)


def pub_mqtt( w, mA, V ):
# Publish to MQTT service
    mqttc = mqtt.Client(MQTTUSER)
    mqttc.username_pw_set(MQTTUSER, MQTTPASSWORD)
    mqttc.connect(MQTTSERVER, MQTTPORT)
    mqttc.publish(MQTTTOPIC+"watt", w, retain=False)
    mqttc.publish(MQTTTOPIC+"current", mA, retain=False)
    mqttc.publish(MQTTTOPIC+"voltage", V, retain=False)
    mqttc.loop(2)


# Start the process
responsejson = deviceInfo(PLUGID,PLUGIP,PLUGKEY,PLUGVERS)