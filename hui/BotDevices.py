from functools import partial
from .util import request, setOption
from .util import terminal_red

class BotDevice:

	_cmd_on = {"commandType":"command", "command":"turnOn", "parameter":"default"}
	_cmd_off = {"commandType":"command", "command":"turnOff", "parameter":"default"}

	properties = [
		'debug',
		'properties',
		'executable'
	]

	executable = [
		'on',
		'off',
		'status'
	]

	def __init__(self, autho, deviceId, name, deviceType, isRemote):
		self.id = deviceId
		self.name = name
		self.type = deviceType
		self.isRemote = isRemote
		self.autho = autho
		self.debug = False


	def fetchStatus(self):
		url = 'https://api.switch-bot.com/v1.0/devices/'+self.id+'/status'
		headers = {'Authorization' : self.autho}
		return request(url, headers, debug=self.debug)


	def post(self, data):
		url = 'https://api.switch-bot.com/v1.0/devices/'+self.id+'/commands'
		headers = {
			'Content-Type': 'application/json; charset: utf8',
			'Authorization' : self.autho,
		}
		return request(url, headers, data, debug=self.debug)


	def status(self):
		return {}

	def on(self):
		if not self.post(BotDevice._cmd_on):
			print("failed")

	def off(self):
		if not self.post(BotDevice._cmd_off):
			print("failed")


class AirConditioner(BotDevice):

	_modeNames = ["auto", "cool", "dry", "fan", "heat"]
	_fanSpeedNames = ["auto", "low", "medium", "high"]

	executable = BotDevice.executable + [
		'set',
		'cool',
		'heat',
	]

	properties = BotDevice.properties + [
		'mode',
		'fan',
		'temperature'
	]

	def __init__(self, autho, deviceId, name):
		deviceType = "Air Conditioner"
		isRemote = True
		super().__init__(autho, deviceId, name, deviceType, isRemote)

		self.temperature = 25
		self.mode = "cool"
		self.fan = "auto"


	def status(self):
		return {
			'temperature': self.temperature,
			'mode': self.mode,
			'fan': self.fan
		}


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

		if self.post(cmd):
			print(self.status())


	def cool(self, t):
		self.temperature = t
		self.mode = "cool"
		return self.set()

	def heat(self, t):
		self.temperature = t
		self.mode = 'heat'
		return self.set()


class Plug(BotDevice):

	executable = BotDevice.executable + [
		'toggle',
	]

	def __init__(self, autho, deviceId, name):
		deviceType = "Plug"
		isRemote = False
		super().__init__(autho, deviceId, name, deviceType, isRemote)


	def status(self):
		return {'power':self.power}


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
		else:
			return 'none'



class DIYLight(BotDevice):
	# for my room's only

	_cmd_up = {"commandType":"command", "command":"brightnessUp", "parameter":"default"}
	_cmd_down = {"commandType":"command", "command":"brightnessDown", "parameter":"default"}

	executable = BotDevice.executable + [
		'mode',
		'brightness',
	]

	properties = BotDevice.properties

	def __init__(self, autho, deviceId, name):
		deviceType = "DIY Light"
		isRemote = True
		super().__init__(autho, deviceId, name, deviceType, isRemote)


	def status(self):
		return {}


	def mode(self, next=1):
		n = int(next)%3

		if n == 1:
			self.post(DIYLight._cmd_on)
		elif n == 2:
			self.post(DIYLight._cmd_off)


	def brightness(self, n):

		if n[0] == '+':
			print('brighten', self.name, 'by', n[1:])
			cmd = [DIYLight._cmd_up]*int(n)
		elif n[0] == '-':
			print('dim', self.name, 'by', n[1:])
			cmd = [DIYLight._cmd_down]*-int(n)
		else:
			print('set', self.name, 'brightness to', n)
			cmd = [DIYLight._cmd_down]*10 + [DIYLight._cmd_up]*int(n)

		res = []
		for c in cmd:
			res.append(self.post(c))

		if res.count(True) == len(res):
			print("success")
		else:
			print("failed.", res)



class HubMini(BotDevice):

	executable = []

	def __init__(self, autho, deviceId, name):
		deviceType = "Hub Mini"
		isRemote = False
		super().__init__(autho, deviceId, name, deviceType, isRemote)


	def off(self):pass
	def on(self):pass