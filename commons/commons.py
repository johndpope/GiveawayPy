import os, datetime, time
import inspect

def get_time():
    return datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S')

def myprint(*args):
    parent = ""
    try:
        stack = inspect.stack()
        parent = stack[1][3].strip()
    except:
        pass

    res_str = ""
    for arg in args:
        res_str = res_str + str(arg) + ' '
    print(get_time(), parent, res_str)
