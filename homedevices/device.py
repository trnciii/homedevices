from functools import partial

class Device:
    def __init__(self, home, deviceId, name, deviceType, isRemote):
        self.id = deviceId
        self.name = name
        self.type = deviceType
        self.isRemote = isRemote

        self.post = partial(home.postCommand, deviceId=self.id)
        self.fetchStatus = partial(home.fetchStatus, deviceId=self.id)


    def __str__(self):
        s = str(self.id) + ", " + self.name + ", " + self.type
        if self.isRemote:
            s = s + "(remote)"

        return s



class AirConditioner(Device):
    def __init__(self, home, deviceId, name):
        deviceType = "Air Conditioner"
        isRemote = True
        super().__init__(home, deviceId, name, deviceType, isRemote)

        # 25,2,1,off
        # temperature, mode(cool), fan speed(auto), power
        self.temperature = 25
        self.mode = 2
        self.fan = 1
        self.powerState = "off"

    def __str__(self):
        s = super().__str__()

        modes = ["auto", "cool", "dry", "fan"]
        fan = ["auto", "low", "medium", "high"]

        s = s + " { "
        s = s + "power : " + self.powerState + ", "
        s = s + "temperature : " + str(self.temperature) + ", "
        s = s + "mode : " + modes[self.mode-1] + ", "
        s = s + "fan : " + fan[self.fan-1] + " }"

        return s


    def set(self):
        para = str(self.temperature)+","+str(self.mode)+","+str(self.fan)+","+self.powerState
        cmd = {
            "command":"setAll",
            "parameter": para,
            "commandType":"command"
        }

        return self.post(cmd)



class Plug(Device):
    def __init__(self, home, deviceId, name):
        deviceType = "Plug"
        isRemote = False
        super().__init__(home, deviceId, name, deviceType, isRemote)

        self.powerState = False
        self.sync()


    def __str__(self):
        s = super().__str__()
        return s + " { power: " + ("on" if self.powerState else "off") + " }"


    def power(self, mode=None):
        if mode is None:
            self.powerState = not self.powerState
        else:
            self.powerState = mode

        cmd = {
            "command":"turnOn" if self.powerState else "turnOff",
            "parameter":"default",
            "commandType":"command"
        }

        return self.post(cmd)


    def sync(self):
        st = self.fetchStatus()
        if st["message"] == "success":
            self.powerState = st["body"]["power"] == "on"
        return st


class DIYLight(Device):
    
    state = ["off", "on", "night"]
    
    cmd_on = {"commandType":"command", "command":"turnOn", "parameter":"default"}
    cmd_off = {"commandType":"command", "command":"turnOff", "parameter":"default"}
    cmd_up = {"commandType":"command", "command":"brightnessUp", "parameter":"default"}
    cmd_down = {"commandType":"command", "command":"brightnessDown", "parameter":"default"}

    def __init__(self, home, deviceId, name):
        deviceType = "DIY Light"
        isRemote = True
        super().__init__(home, deviceId, name, deviceType, isRemote)

        self.cState = 0
        self.nState = self.cState + 1

        self.setAbsoluteBrightness = False

    def __str__(self):
        s = super().__str__()
        s = s + " { state: " + DIYLight.state[self.cState] + ", "
        s = s + "absolute brightness flag: " + str(self.setAbsoluteBrightness)
        s = s + " }"
        return s


    def mode(self, state):
        n = 0

        if isinstance(state, str) and state in DIYLight.state:
            n = DIYLight.state.index(state) - self.cState

        if isinstance(state, int):
            n = state%3

        if n == 1:
            return self.run([DIYLight.cmd_on])
        if n == 2:
            return self.run([DIYLight.cmd_off])
        return []


    def brightness(self, n, absolute=False):
        cmd = []

        if absolute:
            cmd = [DIYLight.cmd_down]*10 + [DIYLight.cmd_up]*self.nBrightness
        elif n>0:
            cmd = [DIYLight.cmd_up]*n
        elif n<0:
            cmd = [DIYLight.cmd_down]*(-n)

        self.run(cmd)


    def run(self, commands):
        res = []
        for c in commands:
            res.append(self.post(c))
        return res



class HubMini(Device):
    def __init__(self, home, deviceId, name):
        deviceType = "Hub Mini"
        isRemote = False
        super().__init__(home, deviceId, name, deviceType, isRemote)

    def __str__(self):
        return self.type