from functools import partial

def toOptions(ls):
    s = "[ "
    for i in range(len(ls)):
        s += str(i) + " " + str(ls[i])
        if i < len(ls)-1:
            s += " | "

    return s + " ]"

def setOption(v, ls):
    if v in ls:
        return ls.index(v)

    if isinstance(v, int) and 0<=v and v<len(ls):
        return v

    v = input("choose option " + toOptions(ls) + " >>")
    return setOption(int(v) if v.isdigit() else v, ls)


class Device:

    _cmd_on = {"commandType":"command", "command":"turnOn", "parameter":"default"}
    _cmd_off = {"commandType":"command", "command":"turnOff", "parameter":"default"}

    def __init__(self, home, deviceId, name, deviceType, isRemote):
        self.id = deviceId
        self.name = name
        self.type = deviceType
        self.isRemote = isRemote

        self.post = partial(home.postCommand, deviceId=self.id)
        self.fetchStatus = partial(home.fetchStatus, deviceId=self.id)


    def __str__(self):
        s = "[\'" + self.name + "\'], type: " + self.type
        if self.isRemote:
            s += "(remote)"

        s += ", status: " + self.status()

        return s

    def status(self):
        return "{}"

    def on(self):
        print("turn " + self.name + " on")
        if self.post(Device._cmd_on):
            print(self.status())
        else:
            print("failed")

    def off(self):
        print("turn", self.name, "off")
        if self.post(Device._cmd_off):
            print(self.status())
        else:
            print("failed")


class AirConditioner(Device):
    
    _modeNames = ["auto", "cool", "dry", "fan", "heat"]
    _fanSpeedNames = ["auto", "low", "medium", "high"]

    def __init__(self, home, deviceId, name):
        deviceType = "Air Conditioner"
        isRemote = True
        super().__init__(home, deviceId, name, deviceType, isRemote)

        self.temperature = 25
        self.mode = "cool"
        self.fan = "auto"


    def status(self):
        s = "{ "
        s = s + "temperature: " + str(self.temperature) + ", "
        s = s + "mode: " + self.mode + ", "
        s = s + "fan: " + self.fan + " }"
        return s


    @property
    def mode(self):
        return AirConditioner._modeNames[self._mode]
    
    @mode.setter
    def mode(self, v):
        self._mode = setOption(v, AirConditioner._modeNames)

    @property
    def fan(self):
        return AirConditioner._fanSpeedNames[self._fan]

    @fan.setter
    def fan(self, v):
        self._fan = setOption(v, AirConditioner._fanSpeedNames)


    def set(self):
        para = str(self.temperature)+","+str(self._mode+1)+","+str(self._fan+1)+",on"
        cmd = {
            "command":"setAll",
            "parameter": para,
            "commandType":"command"
        }

        print("set", self.name, self.status(), "(command:", para+")")
        if self.post(cmd):
            print("success")


    def cool(self, t):
        self.temperature = t
        self.mode = "cool"
        return self.set()



class Plug(Device):
    def __init__(self, home, deviceId, name):
        deviceType = "Plug"
        isRemote = False
        super().__init__(home, deviceId, name, deviceType, isRemote)


    def status(self):
        return "{ power: " + self.power + " }"


    def toggle(self):
        p = self.power
        if p == "on":
            return self.off()
        elif p == "off":
            return self.on()

    @property
    def power(self):
        st = self.fetchStatus()
        if st:
            return st["power"]



class DIYLight(Device):
    # for my room's only

    _stateNames = ["off", "on", "night"]
    
    _cmd_up = {"commandType":"command", "command":"brightnessUp", "parameter":"default"}
    _cmd_down = {"commandType":"command", "command":"brightnessDown", "parameter":"default"}

    def __init__(self, home, deviceId, name):
        deviceType = "DIY Light"
        isRemote = True
        super().__init__(home, deviceId, name, deviceType, isRemote)

        self.power = 1

        self.on = partial(self.mode, next="on")
        self.off = partial(self.mode, next="off")
        self.night = partial(self.mode, next="night")


    def status(self):
        return "{ power: " + self.power + " }"


    @property
    def power(self):
        return DIYLight._stateNames[self._power]

    @power.setter
    def power(self, v):
        self._power = setOption(v, DIYLight._stateNames)
    

    def mode(self, next):
        n = 0

        if isinstance(next, str) and next in DIYLight._stateNames:
            n = DIYLight._stateNames.index(next) - self._power
            n = n%3
        elif isinstance(next, int):
            n = next%3

        print("turn", self.name, "form", self.power, "to", DIYLight._stateNames[(self._power + n)%3])
 
        if n == 1 and self.post(DIYLight._cmd_on):
            self._power = (self._power + n)%3
        elif n == 2 and self.post(DIYLight._cmd_off):
            self._power = (self._power + n)%3


    def brightness(self, n, absolute=False):
        cmd = []

        if absolute:
            print("set", self.name, "brightness", n)
            cmd = [DIYLight._cmd_down]*10 + [DIYLight._cmd_up]*n
        elif n>0:
            print("brighten", self.name, "by", n)
            cmd = [DIYLight._cmd_up]*n
        elif n<0:
            print("dim", self.name, "by", n)
            cmd = [DIYLight._cmd_down]*(-n)

        res = []
        for c in cmd:
            res.append(self.post(c))

        if res.count(True) == len(res):
            print("success")
        else:
            print("failed.", res)



class HubMini(Device):
    def __init__(self, home, deviceId, name):
        deviceType = "Hub Mini"
        isRemote = False
        super().__init__(home, deviceId, name, deviceType, isRemote)


    def off(self):pass
    def on(self):pass