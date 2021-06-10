import json
from homedevices import Home
from homedevices.device import *

def main():
    home = Home()
    home.listDevices()

    # home.devices["AC"].powerState = "off"
    # home.devices["AC"].set()

    # home.devices["Fan"].power()
    # home.devices["Fan"].power(False)


    # print(home.devices["Light"])

    # l = home.devices["Light"]
    
    # l.cState = 1
    # l.nState = 1

    # l.cBrightness = 2
    # l.nBrightness = 0
    # l.setAbsoluteBrightness = False

    # l.set()

    # print(l)
    # print(home.devices["Light"])

main()