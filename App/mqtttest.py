import time
from configparser import ConfigParser

import psutil
import os
import paho.mqtt.client as mqtt
import threading
import json
from uuid import getnode as get_mac
import platform
# from configparser import ConfigParser
import base64
import os.path

updateinterval = 15
maintopic = "SiqsessEdgeGateway-MCM"
devicelocation = "Chennai"
devicecoordinates = "8.25,9.35"
subscribedjson = 'null'
devicemac = get_mac()
macaddressstr = str(devicemac)
deviceid = "EGW6S-" + macaddressstr
topicname = deviceid
devicename = deviceid


def SettingsUpdate():
    global temperature, devicename, devicelocation, devicecoordinates, subscribedjson

    # if "temperature" in subscribedjson:
    #     temperature = subscribedjson["temperature"]
    #     # print(updateinterval)
    # if "DeviceName" in subscribedjson:
    #     devicename = subscribedjson["DeviceName"]
    #     # print(devicename)
    # if "DeviceLocation" in subscribedjson:
    #     devicelocation = subscribedjson["DeviceLocation"]
    #     # print(devicelocation)
    # if "DeviceCoOrdinates" in subscribedjson:
    #     devicecoordinates = subscribedjson["DeviceCoOrdinates"]
    #     # print(devicecoordinates)

    data = {
        "temperature": "11",
        "uvindex": "12",
        "rainfall": "13",
        "humidity": "14",
        "wind_speed": "15",
        "wind_direction": "11",
        "soil_moisture": "12",
        "soil_temperature": "14",
        "dew_point": "11",
        "wind_alert": "high",
        "timestamp": "date.time"
    }
    return data

def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Connected successfully")
    else:
        print("Connect returned result code: " + str(rc))


# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    global temperature, devicename, devicelocation, devicecoordinates, subscribedjson

    subscribedjsonstr = str(msg.payload.decode("utf-8"))
    print("Settings update received")
    print(subscribedjsonstr)
    subscribedjson = json.loads(subscribedjsonstr)

    SettingsUpdate()

# MQTT Connections
def mqttConnection():

    subscriptiontopic = "IOTC3WSX0001/Event"
    serveripaddress = "167.233.7.5"
    serverport = 1883

    # create the client
    client = mqtt.Client()

    # connection must be dynamic
    client.connect(serveripaddress, serverport)

    # connect to client
    client.on_connect = on_connect
    client.on_message = on_message
    client.subscribe(subscriptiontopic)
    print("Subscribed to the topic")
    time.sleep(3)




