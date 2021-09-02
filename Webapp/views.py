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


class ReadDeviceSettings(APIView):

    def get(self, request):
        # jsonData = eventData("")
        # print(jsonData)
        # jsonResponse = json.dumps(jsonData, indent=4)
        appsetting.runWebSocket = True
        col = "DeviceStatus"
        DeviceID = "Arima_01"
        data = str(Doc().Read_Document(col, DeviceID))
        jsonResponse = json.dumps(data, indent=4)
        return HttpResponse(jsonResponse, "application/json")


class startMQTT(APIView):

    def post(self, request):
        appsetting.startMqttService = True
        start_thread()
        return HttpResponse("Success", "application/json")


class StopMQTT(APIView):

    def post(self, request):
        appsetting.startMqttService = False
        start_thread()
        return HttpResponse('success', "application/json")