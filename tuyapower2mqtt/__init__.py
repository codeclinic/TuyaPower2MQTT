#!/usr/bin/python
# TuyaPower2MQTT
# Python module to pull power & state data from Tuya WiFi smart devices with reporting via MQTT
#
# Author: Phill Healey

name = "tuyapower2mqtt"

import datetime
import time
import os
import sys
from time import sleep

#import pycrypto
#import Crypto
#import paes
import pytuya
import paho.mqtt.client as mqtt
import json



#DEVICEID=sys.argv[1] if len(sys.argv) >= 2 else '01234567891234567890'
#DEVICEIP=sys.argv[2] if len(sys.argv) >= 3 else '012.345.678.910'
#DEVICEKEY=sys.argv[3] if len(sys.argv) >= 4 else '0123456789abcdef'
#DEVICEVERS=sys.argv[4] if len(sys.argv) >= 5 else '3.1'

# Check for environmental variables and always use those if available (required for Docker)
#PLUGID=os.getenv('PLUGID', DEVICEID)
#PLUGIP=os.getenv('PLUGIP', DEVICEIP)
#PLUGKEY=os.getenv('PLUGKEY', DEVICEKEY)
#PLUGVERS=os.getenv('PLUGVERS', DEVICEVERS)
# how my times to try to probe plug before giving up
RETRY=5

# Setup MQTT server with your credentials
# EDIT THIS
#MQTTSERVER="127.0.0.1"
#MQTTUSER="homeassistant"
#MQTTPASSWORD="homeassistant"
#MQTTTOPIC="devices/tuya/plug/"
#MQTTPORT=1883
# STOP EDITING

def getValuesFromDataPack(data, wi, ai, vi, swi=1):
    returnedInfo = {}
    returnedInfo["switch"] = data['dps'][str(swi)] # Switch State - True = On
    try:
        returnedInfo["power"] = (float(data['dps'][str(wi)])/10.0) # Power - W
        returnedInfo["current"] = float(data['dps'][str(ai)]) # Current - mA
        returnedInfo["voltage"] = (float(data['dps'][str(vi)])/10.0) # Voltage - V
    except IndexError:
        returnedInfo["result"] = "Only switch information was able to be parsed from the plug"

    return returnedInfo

def deviceInfo( deviceid, ip, key, vers ):
    returnedInfo = {}
    watchdog = 0
    now = datetime.datetime.utcnow()
    iso_time = now.strftime("%Y-%m-%dT%H:%M:%SZ") 
    returnedInfo["datetime"] = iso_time
    returnedInfo["deviceid"] = deviceid

    while True:
        try:
            d = pytuya.OutletDevice(deviceid, ip, key)
            if vers == '3.3':
                d.set_version(3.3)

            data = d.status()
            if(d):
                dpsKeys = data['dps'].keys()
                if vers == '3.3' and ('19' in dpsKeys):
                    returnedInfo.update(getValuesFromDataPack(data, 19, 18, 20))
                else:
                    if '5' in dpsKeys:
                        returnedInfo.update(getValuesFromDataPack(data, 5, 4, 6))
            else:
                returnedInfo["result"] = "Incomplete response from plug: %s [%s]." % (deviceid, ip)
            break
        except KeyboardInterrupt:
            pass
        except:
            watchdog+=1
            if(watchdog>RETRY):
                returnedInfo["result"] = "Incomplete response from plug%s [%s]." % (deviceid, ip)
                break
            sleep(2)

    return json.dumps(returnedInfo)


#def pub_mqtt( w, mA, V, sw ):
def pub_mqtt(mqttcreds, deviceid, ret):
# Publish to MQTT service
    mqttc = mqtt.Client(mqttcreds[2])
    mqttc.username_pw_set(mqttcreds[2], mqttcreds[3])
    mqttc.connect(mqttcreds[0], mqttcreds[1])
    mqttc.publish(mqttcreds[4]+deviceid, ret, retain=mqttcreds[5])
    mqttc.loop(2)
    mqttc.loop_stop() #stop the loop


# Start the process
#responsejson = deviceInfo(PLUGID,PLUGIP,PLUGKEY,PLUGVERS)

#if __name__ == "__main__":
#    deviceInfo(PLUGID,PLUGIP,PLUGKEY,PLUGVERS)