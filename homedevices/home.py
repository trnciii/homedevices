import json
import os
import datetime

from .BotDevices import *
from .util import *


class Home:

    def __init__(self):

        if not os.path.exists(path_data):
            os.mkdir(path_data)

        self.autho = ""
        self.setAutho()

        self.devices = {}
        self.loadDevices_bot()

        self.removeAutho = removeAutho
        self.removeDeviceList = removeDeviceList

        print(self)


    def __str__(self):
        w = 2 + max([len(i) for i in self.devices.keys()])

        s  = "---- devices ----\n"
        for d in self.devices.values():
            s += d.name.ljust(w) + d.status() + "\n"
        s += "---- ------- ----\n"
        return s


# autho
    def setAutho(self, string=None):
        if string:
            self.autho = string
            write(path_autho, self.autho)
            return

        try:
            with open(path_autho, "r") as f:
                self.autho = f.readline().replace("\n", "")
        except:
            self.autho = input("enter authentication: ")
            write(path_autho, self.autho)


# devices
    def loadDevices_bot(self):
        src = self.fetchDeviceList_bot()

        if not src: return

        for s in src["deviceList"]:
            deviceType = s["deviceType"].replace(" ", "")
            device = eval(deviceType)(self.autho, s["deviceId"], s["deviceName"])
            self.devices[s["deviceName"]] = device

        for s in src["infraredRemoteList"]:
            deviceType = s["remoteType"].replace(" ", "")
            device = eval(deviceType)(self.autho, s["deviceId"], s["deviceName"])
            self.devices[s["deviceName"]] = device
            

    def fetchDeviceList_bot(self):
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
    def down(self):
        for d in self.devices.values():
            d.off()

    def on(self, d):
        self.devices[d].on()

    def off(self, d):
        self.devices[d].off()
