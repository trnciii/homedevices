import json
import urllib.request
from .device import *


def request(url, headers, data=None):
    req = urllib.request.Request(url, json.dumps(data).encode() if data else None, headers)
    try:
        with urllib.request.urlopen(req) as response:
            body = json.loads(response.read())
            return body
    except urllib.error.URLError as e:
        print(e)


class Home:

    def __init__(self):
        self.File_autho = "./data/autho"
        self.File_devices = "./data/devices.json"

        self.devices = {}

        try:
            with open(self.File_autho, "r") as f:
                self.autho = f.readline().replace("\n", "")
        except:
            print("failed to read token")

        try:
            with open(self.File_devices, "r") as f:
                print("using local device list")
                devices_raw = json.load(f)
        except:
            print("fetching device list")
            res = self.fetchDevices()

            if res["message"] == "success":
                devices_raw = res["body"]
                with open(self.File_devices, 'w') as f:
                    json.dump(devices_raw, f, indent=4)
                    print('saved device list as', self.File_devices)
                    print()
            else:
                print("failed to get device list")
                devices_raw = None

        if devices_raw:
            self.createDevices(devices_raw)


    def createDevices(self, src):
        for s in src["deviceList"]:
            deviceType = s["deviceType"].replace(" ", "")
            device = eval(deviceType)(self, s["deviceId"], s["deviceName"])
            self.devices[s["deviceName"]] = device

        for s in src["infraredRemoteList"]:
            deviceType = s["remoteType"].replace(" ", "")
            device = eval(deviceType)(self, s["deviceId"], s["deviceName"])
            self.devices[s["deviceName"]] = (device)


    def listDevices(self):
        for d in self.devices.values():
            print("-", d)
        print()


    def fetchDevices(self):
        url = 'https://api.switch-bot.com/v1.0/devices'
        headers = {'Authorization' : self.autho}
        return request(url, headers)


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