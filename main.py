import json
from homedevices import Home
from homedevices.device import *

def main():
    home = Home()

    # home.devices["AC"].powerState = "on"
    # home.devices["AC"].temperture = 27
    # home.devices["AC"].set()
    # home.devices["AC"].off()

    # home.devices["Fan"].power()
    # home.devices["Fan"].power(False)

    l = home.devices["Light"]
    l.state = 1
    l.mode("night")
    print(l.brightness(2, True))

main()