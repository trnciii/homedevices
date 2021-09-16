import sys, traceback

from .home import Home
from .util import *

def execute(home, cmd):
    if len(cmd)==0: return

    if cmd[0] == 'py':
        code = " ".join(cmd[1:])
        exec('res='+code, globals(), locals())
        return locals()['res']

    elif cmd[0] == 'clean':
        if input('delete all local data? [y/n]') == 'y':
            clean()

    elif cmd[0] in ['quit', 'q']:
        exit()

    elif cmd[0] in ['help', 'h']:
        s = "Command list:\n\
        <device name> <method> <args>   execute method\n\
        \n\
        clean                           remove all local data (use this before uninstall)\n\
        quit                            quit application\n\
        help                            show this message\n\
        "
        return s

    elif cmd[0] in home.devices.keys() or cmd[0] == 'home':
        return home.execute(cmd)

    else:
        return 'failed to find device or command. use <help> to show commands.'


def run():
    print('running interactive interface')

    home = Home()
    home.debug('on')
    print(home)

    while(True):
        try:
            cmd = input('>>> ').split()
            res = execute(home, cmd)
            if res:
                print(res)

        except Exception:
            print("Exception in user code:")
            print("-"*40)
            traceback.print_exc(file=sys.stdout)
            print("-"*40)

# main
if len(sys.argv)>1:
    execute(Home(), sys.argv[1:])
else:
    run()
