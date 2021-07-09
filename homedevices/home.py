import json
import urllib.request
import os

from .device import *
from .util import *


def request(url, headers, data=None):
    req = urllib.request.Request(url, json.dumps(data).encode() if data else None, headers)
    try:
        with urllib.request.urlopen(req) as response:
            body = json.loads(response.read())
            if body["message"] == "success":
                return body["body"] if body["body"] else True
            else:
                print(body["message"])

    except urllib.error.URLError as e:
        print(e)


def write(file, string):
    try:
        open(file, "w").write(string)
        print("saved", file)
    except:
        print("failed to save", file)



class Home:

    def __init__(self):

        if not os.path.exists(path_data):
            os.mkdir(path_data)

        self.autho = ""
        self.setAutho()

        self.devices = {}
        self.loadDevices()

        self.removeAutho = removeAutho
        self.removeDeviceList = removeDeviceList

        print(self)


    def __str__(self):
        s = "---- devices ----\n"
        for d in self.devices:
            s += d + "\n"
        s += "---- ------- ----\n"
        return s


    # autho token
    def setAutho(self, string=None):
        if string:
            self.autho = string
            write(path_autho, self.autho)
            return

        try:
            with open(path_autho, "r") as f:
                self.autho = f.readline().replace("\n", "")
        except:
            self.autho = input("enter an authorization token: ")
            write(path_autho, self.autho)


    # devices
    def loadDevices(self):
        src = self.fetchDeviceList()

        if not src: return

        for s in src["deviceList"]:
            deviceType = s["deviceType"].replace(" ", "")
            device = eval(deviceType)(self, s["deviceId"], s["deviceName"])
            self.devices[s["deviceName"]] = device

        for s in src["infraredRemoteList"]:
            deviceType = s["remoteType"].replace(" ", "")
            device = eval(deviceType)(self, s["deviceId"], s["deviceName"])
            self.devices[s["deviceName"]] = device
            

    def fetchDeviceList(self):
        try:
            with open(path_devices, "r") as f:
                print("using local device list")
                return json.load(f)
        except:
            print("fetchig device list")

            url = 'https://api.switch-bot.com/v1.0/devices'
            headers = {'Authorization' : self.autho}

            deviceList = request(url, headers)
            if deviceList:
                write(path_devices, json.dumps(deviceList, indent=4))
                return deviceList


    # actions
    def fetchStatus(self, deviceId):
        url = 'https://api.switch-bot.com/v1.0/devices/'+deviceId+'/status'
        headers = {'Authorization' : self.autho}
        return request(url, headers)


    def postCommand(self, data, deviceId):
        url = 'https://api.switch-bot.com/v1.0/devices/'+deviceId+'/commands'
        headers = {
            'Content-Type': 'application/json; charset: utf8',
            'Authorization' : self.autho,
        }
        return request(url, headers, data)
