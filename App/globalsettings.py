from paho.mqtt import client as mqtt

def init():
    global startMqttService
    startMqttService = False
