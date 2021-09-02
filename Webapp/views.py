import datetime
import json
import threading
import time
import App.globalsettings as appsetting
from django.shortcuts import render
from rest_framework.views import APIView
from django.http import HttpResponse
from App.MongoDB_Main import Document as Doc
from App.mqttListener import mqttService, start_thread
import asyncio

from App.mqtttest import AsyncMqttExample


class ReadDeviceSettings(APIView):

    def get(self, request):
        # jsonData = eventData("")
        # print(jsonData)
        # jsonResponse = json.dumps(jsonData, indent=4)
        appsetting.runWebSocket = True
        col = "DeviceStatus"
        DeviceID = "Arima_01"
        data = Doc().Read_Document(col, DeviceID)
        jsonResponse = json.dumps(data, indent=4)
        return HttpResponse(jsonResponse, "application/json")


class startMQTT(APIView):

    def get(self, request):
        appsetting.startMqttService = True

        print("Thread Starting")
        # AsyncMqttExample()
        Thread = threading.Thread(target=start_thread)
        Thread.start()
        print("Theread Finished")

        successjson = {"Success": "True"}
        jsonResponse = json.dumps(successjson, indent=4)
        return HttpResponse(jsonResponse, "application/json")


class StopMQTT(APIView):

    def post(self, request):
        appsetting.startMqttService = False
        start_thread()
        return HttpResponse('success', "application/json")