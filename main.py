import json
from homedevices import Home

def main():
    home = Home()

    # home.devices["AC"].powerState = "on"
    # home.devices["AC"].temperture = 27
    # home.devices["AC"].set()
    # home.devices["AC"].off()

    # home.devices["Fan"].power()
    home.devices["Fan"].on()

    # l = home.devices["Light"]
    # l.state = 0
    # l.mode("on")
    # print(l.brightness(2))

main()