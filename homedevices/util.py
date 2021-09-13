import os
import shutil
import time
import threading
import urllib.request
import json


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
        f(*args)

    th = threading.Thread(target=ex)
    th.start()

def ls(l):
    if isinstance(l, dict):
        l = l.values()

    for i in l:
        print(i)


def request(url, headers, data=None, debug=False):

    if debug:
        print(terminal_red('debugging request'))
        print('-'*40)
        print('url :', url)
        print('headers :', headers)
        print('data :', data)
        print('-'*40)
        return False

    req = urllib.request.Request(url, json.dumps(data).encode() if data else None, headers)
    try:
        with urllib.request.urlopen(req) as response:
            body = json.loads(response.read())
            if body["message"] == "success":
                return body["body"] if body["body"] else True
            else:
                print("ERROR")
                print("request data:", data)
                print("response message:", body["message"])
                print("response body", body["body"])

    except urllib.error.URLError as e:
        print("URLError", e)


def write(file, string):
    try:
        open(file, "w").write(string)
        print("saved", file)
    except:
        print("failed to save", file)


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

    # when v is int
    if isinstance(v, int) and 0<=v and v<len(ls):
        return v

    # when v is 'n'
    if v in [str(i) for i in range(len(ls))]:
        return int(v)

    v = input("choose option " + toOptions(ls) + " >>")
    return setOption(int(v) if v.isdigit() else v, ls)


def terminal_red(s):
    return "\033[1;31m" + s + "\033[0m"

def terminal_green(s):
    return "\033[1;32m" + s + "\033[0m"

def terminal_yellow(s):
    return "\033[1;33m" + s + "\033[0m"

def terminal_blue(s):
    return "\033[1;34m" + s + "\033[0m"

def terminal_bold(s):
    return "\033[1;1m" + s + "\033[0m"

def quate(s):
    return '\'' + s + '\''

def angle(s):
    return '<' + s + '>'