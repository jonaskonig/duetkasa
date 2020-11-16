import asyncio
import datetime
import json
import time
import requests
from kasa import SmartPlug
from datetime import datetime
from datetime import timedelta
from DWClib import *
import timer
waittime = 1
heatermaxtemp = None
plugip = None


def initial():
    with open('conf.json') as json_file:
        data = json.load(json_file)
        plugip = data["kasa_ip"]
        waittime = int(data["timebeforshutdown"])
        heatermaxtemp = int(data["maxheatertemp"])
    plug = SmartPlug(plugip)
    DSFsock = openDSF()
    check(waittime,heatermaxtemp)


def check(waittime,maxheatertemp):
    asyncio.run(plug.update())
    if plug.is_on:
        data = rungcode()
        status = data["status"]
        heatertemp = data["htemp"]
        timer = timer.Timer(waittime)
        while status == "I" and heatertemp <= heatermaxtemp:
            if timer.timer_up():
                asyncio.run(turn_off())
                break
            else:
                data = rungcode()
                status = data["status"]
                heatertemp = data["htemp"]
            time.sleep(1)
    time.sleep(4)
    check(waittime,maxheatertemp)



def rungcode():
    r=Gcode(DSFsock,'M408')
    response = json.loads(response)
    response = json_data['response']
    response = json.loads(response)
    state = response['status']
    heatertemp = response['heaters'][1]
    return(dict(status = status, htemp = heatertemp))

initial()
