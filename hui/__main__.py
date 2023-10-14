import sys, traceback
import os

from .home import Home, execute_method
from . import util, terminal as term


def execute(home, cmd):
	if len(cmd)==0: return

	if cmd[0] == 'py':
		code = " ".join(cmd[1:])
		exec('res={}'.format(code), globals(), locals())
		return locals()['res']

	if cmd[0] == 'sh':
		os.system(' '.join(cmd[1:]))
		return

	elif cmd[0] in ['quit', 'q']:
		exit()

	# util
	elif cmd[0] in util.executable.keys():
		return util.executable[cmd[0]](*cmd[1:])

	# device
	elif cmd[0] in home.devices.keys():
		if execute_method(home.devices[cmd[0]], cmd[1:]):
			print(home.devices[cmd[0]].status())

	# home
	elif cmd[0] == 'home':
		return execute_method(home, cmd[1:])

	elif cmd[0] in home.executable.keys() | home.properties:
		return execute_method(home, cmd)

	# fail
	else:
		return term.mod('failed to find device or command', [term.color('yellow')])


def main():

	if len(sys.argv)>1:
		home = Home()
		if re := execute(home, sys.argv[1:]):
			print(re)

	else:
		from .complete import Completer
		import readline

		print('running', util.running())

		home = Home()
		print(home.status())

		comp = Completer()

		readline.parse_and_bind('tab: complete')
		readline.set_completer(comp.complete)

		while True:
			try:
				home.update()

				cmd = input('>>> ').split()
				if re := execute(home, cmd):
					print(re)

			except KeyboardInterrupt:
				print()

			except EOFError:
				print()
				break

			except Exception as e:
				print("Exception in user code:")
				print("-"*40)
				traceback.print_exc(file=sys.stdout)
				print("-"*40)


if __name__ == '__main__':
	main()