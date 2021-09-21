import json
import random
from datetime import datetime
import threading
import time
from pytz import timezone
import App.globalsettings as appsetting
from paho.mqtt import client as mqtt
from App.MongoDB_Main import Document as Doc
import App.index as mqttSetting


def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Connected successfully")
    else:
        print("Connect returned result code: " + str(rc))


# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    subscribe = str(msg.payload.decode("utf-8"))
    subscribedData = json.loads(subscribe)
    print(subscribedData)
    eventData(subscribedData)


def eventData(data):
    col = "DeviceStatus"
    log_col = "IOT_WS_log"
    DeviceID = "Arima_01"
    ID = {"DeviceID": DeviceID}

    formatTime = "%Y-%m-%d %H:%M:%S %Z%z"
    # Current time in UTC
    now_utc = datetime.now(timezone('UTC'))
    # Convert to Asia/Kolkata time zone
    now_asia = str(now_utc.astimezone(timezone('Asia/Kolkata')))

    data.update(ID)
    json.dumps(data, indent=4)
    deviceData = data["data"]["modbus"][0]
    windSpeed = int(deviceData["WIND_SPD"])
    if windSpeed > 10:
        windAlert: str = "High"
    elif windSpeed < 1:
        windAlert: str = "Low"
    else:
        windAlert: str = "Normal"
    data_to_DB = {
        "DeviceID": DeviceID,
        "temperature": int(deviceData["IN_TEMP"]) / 100,
        "uvindex": deviceData["SOLR_RADI"],
        "rainfall": deviceData["DAY_RAIN"],
        "humidity": deviceData["IN_HUMI"],
        "wind_speed": deviceData["WIND_SPD"],
        "wind_direction": deviceData["WIND_DIRT"],
        "soil_moisture": random.randint(32, 35),
        "soil_temperature": random.randint(32, 35),
        "dew_point": random.randint(32, 35),
        "wind_alert": windAlert,
        "timestamp": now_asia,
    }
    update = Doc().Write_Document(data=data_to_DB, col=col, DeviceID=DeviceID)
    if update == 0:
        Doc().DB_Write(data=data_to_DB, col=col)
    Doc().DB_Write(data=data_to_DB, col=log_col)
    return data


def mqttService(client: mqtt, subscriptiontopic, serveripaddress, serverport):
    # MQTT Connections
    # create the client

    if appsetting.startMqttService:
        # connection must be dynamic
        client.connect(serveripaddress, serverport)
        # connect to client
        client.on_connect = on_connect
        client.on_message = on_message

        client.subscribe(subscriptiontopic)
        print("Subscribed to the topic")
        time.sleep(3)
        client.loop_forever()


def start_thread():
    setting = mqttSetting.read_setting()
    subscriptiontopic: str = setting["subscriptiontopic"]
    serveripaddress: str = setting["serveripaddress"]
    serverport: int = setting["serverport"]
    client = mqtt.Client()

    if appsetting.startMqttService:

        thread = threading.Thread(
            target=mqttService,
            args=(client, subscriptiontopic, serveripaddress, serverport))

        # Starting the Thread
        thread.start()
    else:
        client.disconnect()
        print("Client Disconnected")
