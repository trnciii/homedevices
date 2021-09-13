import json
import os
import datetime
import sys

from .BotDevices import *
from .util import *


class Home:

    executable = [
        'debug_on',
        'debug_off',
        'down',
    ]

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
            s += d.name.ljust(w) + d.status()
            if d.debug:
                s += terminal_red(' DEBUG MODE')
            s += '\n'
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

            deviceList = request(url, headers, debug=self.debug)
            if deviceList:
                write(path_devices, json.dumps(deviceList, indent=4))
                return deviceList

    def debug_on(self):
        for d in self.devices.values():
            d.debug = True

    def debug_off(self):
        for d in self.devices.values():
            d.debug = False

# actions
    def execute(self, cmd):
        '''
        parse and execute a command in <Device name> <method> <args> style.
        return function's return if succeed or some message otherwise.
        '''
        if len(cmd)==0: return

        if cmd[0] == 'home':
            return self.execute_home(cmd)

        if cmd[0] in self.devices.keys():
            return self.execute_device(cmd)

        return 'device' + quate(cmd[0]) + ' not found'


    def execute_home(self, cmd):
        if not len(cmd)>1:
            return self.__str__()

        if cmd[1] in self.executable:
            return exec('self.'+cmd[1]+'('+','.join(cmd[2:])+')')
        else:
            return 'command ' + quate(cmd[1]) + ' not found in Home'


    def execute_device(self, cmd):
        device = self.devices[cmd[0]]

        if not len(cmd)>1:
            return device.status()


        if cmd[1] in device.executable:
            return exec('device.'+cmd[1]+'('+','.join(cmd[2:])+')')
        else:
            return 'command ' + quate(cmd[1]) + ' not found in ' + cmd[0]


    def down(self):
        for d in self.devices.values():
            d.off()
            print()
