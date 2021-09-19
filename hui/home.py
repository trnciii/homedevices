import json
import os
import datetime
import sys

from .BotDevices import *
from .util import *


def execute_method(obj, cmd):
    if not len(cmd)>0:
        return obj.status()

    if cmd[0] in obj.executable:
        return exec('obj.'+cmd[0]+'(*cmd[1:])')
    elif cmd[0] in obj.properties:
        if len(cmd)>1:
            return exec('obj.'+cmd[0]+'=cmd[1]')
        else:
            return exec('print(obj.'+cmd[0]+')')
    else:
        return 'command ' + quate(cmd[0]) + ' not found in' + type(obj).__name__


class Home:

    executable = [
        'debug',
        'down',

        'saveConfig',
        'setAutho',
        'debug_default',
        'loadConfig'

        'fetchDeviceList_bot',
        'loadDevices_bot',
        'pullDevices_bot'
    ]

    properties = [
        'executable',
        'properties'
    ]

    def __init__(self):

        if not os.path.exists(path_data):
            os.mkdir(path_data)

        self._debug = False

        self.loadConfig()

        self.devices = {}
        self.loadDevices_bot()

        if self.config['debug_default']:
            self.debug(True)


    def __str__(self):
        w = 1 + max([len(i) for i in self.devices.keys()])

        s  = "---- devices ----\n"
        for d in self.devices.values():
            if d.debug:
                s += terminal_red('DEBUG ')
            s += d.name.ljust(w) + json.dumps(d.status())
            s += '\n'
        s += "---- ------- ----\n"
        return s


# config
    def saveConfig(self):
        write(path_config, json.dumps(self.config, indent=4))


    def loadConfig(self):
        self.config = {}
        if os.path.exists(path_config):
            self.config = json.load(open(path_config, 'r'))

        self.setAutho()
        if not 'debug_default' in self.config.keys():
            self.config['debug_default'] = False


    def debug_default(self, v=None):
        if v in ['on', True, 'True']:
            self.config['debug_default'] = True
            self.saveConfig()

        elif v in ['off', False, 'False']:
            self.config['debug_default'] = False
            self.saveConfig()

        else:
            self.debug_default


    def setAutho(self, string=None):
        if string:
            self.config['autho_bot'] = string
            self.saveConfig()

        elif not 'autho_bot' in self.config.keys():
            self.config['autho_bot'] = input('enter authentication: ')
            self.saveConfig()


# devices
    def loadDevices_bot(self):
        self.devices = {}

        try:
            print("using local device list")
            src = json.load(open(path_devices, "r"))
        except:
            print("fetchig device list from server")
            src = self.fetchDeviceList_bot()

        if not src:
            print('failed to load Switch Bot Devices')
            return

        autho = self.config['autho_bot']

        for s in src["deviceList"]:
            deviceType = s["deviceType"].replace(" ", "")
            device = eval(deviceType)(autho, s["deviceId"], s["deviceName"])
            self.devices[s["deviceName"]] = device

        for s in src["infraredRemoteList"]:
            deviceType = s["remoteType"].replace(" ", "")
            device = eval(deviceType)(autho, s["deviceId"], s["deviceName"])
            self.devices[s["deviceName"]] = device
            

    def fetchDeviceList_bot(self):
        url = 'https://api.switch-bot.com/v1.0/devices'
        headers = {'Authorization' : self.config['autho_bot']}

        deviceList = request(url, headers, debug=self._debug)
        if deviceList:
            write(path_devices, json.dumps(deviceList, indent=4))
            return deviceList

    def pullDevices_bot(self):
        self.fetchDeviceList_bot()
        self.loadDevices_bot()

# others
    def debug(self, v):
        if v in ['on', True]:
            print('entering debug mode')
            self._debug = True
            for d in self.devices.values():
                d.debug = True

        elif v in ['off', False]:
            print('leaving debug mode')
            self._debug = False
            for d in self.devices.values():
                d.debug = False


    def down(self):
        for d in self.devices.values():
            d.off()
            print()
