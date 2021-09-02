import socket
import uuid
import paho.mqtt.client as mqtt
import asyncio

topic = "IOTC3WSX0001/Event"


class AsyncMqttExample:

    def on_connect(self, client, userdata, flags, rc):
        print("Subscribing")

        client.subscribe(topic)


    def on_message(self, client, userdata, msg):
        print("test")
        data = msg.payload.decode("utf-8")
        print(data)

    def on_disconnect(self, client, userdata, rc):
        self.client.disconnect()

    def __init__(self):
        self.client = mqtt.Client()
        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message
        self.client.on_disconnect = self.on_disconnect
        self.client.connect('167.233.7.5', 1883, 60)
        self.client.loop_forever()