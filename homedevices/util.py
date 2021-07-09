import os
import shutil
import time
import threading


path_lib = os.path.dirname(os.path.abspath(__file__))
path_data = path_lib+"/data"
path_autho = path_data+"/autho"
path_devices = path_data+"/devices.json"


def clean():
    if os.path.exists(path_data):
        shutil.rmtree(path_data)
        print("deleted", path_data)


def removeAutho():
    os.remove(path_autho)
    print("removed", path_autho)


def removeDeviceList():
    os.remove(path_devices)
    print("removed", path_devices)


def delay(t, f, *args):
    
    def ex():
        time.sleep(60*t)
        print(f(*args))

    th = threading.Thread(target=ex)
    th.start()
