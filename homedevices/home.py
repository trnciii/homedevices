import json
import urllib.request
import os
from .device import *


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

def write(path, string):
    path = os.path.abspath(path)
    try:
        open(path, "w").write(string)
        print("saved", path)
    except:
        print("failed to save", path)


class Home:

    def __init__(self):

        os.chdir(os.path.dirname(os.path.abspath(__file__)))
        if not os.path.exists("./data/"):
            os.mkdir("./data/")

        self.File_autho = "./data/autho"
        self.File_devices = "./data/devices.json"

        self.autho = ""
        self.setAutho()

        self.devices = {}
        self.loadDevices()


    # autho token
    def setAutho(self, string=None):
        if string:
            self.autho = string
            write(self.File_autho, self.autho)
            return

        try:
            with open(self.File_autho, "r") as f:
                self.autho = f.readline().replace("\n", "")
        except:
            self.autho = input("enter an authorization token: ")
            write(self.File_autho, self.autho)


    def removeAutho(self):
        os.remove(self.File_autho)
        print("removed", os.path.abspath(self.File_autho))


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
            with open(self.File_devices, "r") as f:
                print("using local device list")
                return json.load(f)
        except:
            print("fetchig device list")

            url = 'https://api.switch-bot.com/v1.0/devices'
            headers = {'Authorization' : self.autho}

            deviceList = request(url, headers)            
            if deviceList:
                write(self.File_devices, json.dumps(deviceList, indent=4))
                return deviceList


    def removeDeviceList(self):
        os.remove(self.File_devices)
        print("removed", os.path.abspath(self.File_devices))


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