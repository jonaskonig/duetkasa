import asyncio
import datetime
import json
import time
import requests
from kasa import SmartPlug
from datetime import datetime
from datetime import timedelta
from DWClib import *
import timer as counter
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
    check(waittime,heatermaxtemp,plug)


def check(waittime,maxheatertemp,plug):
    asyncio.run(plug.update())
    if plug.is_on:
        data = rungcode()
        status = data["status"]
        heatertemp = data["htemp"]
        timer = counter.Timer(waittime)
        while status == "I" and heatertemp <= maxheatertemp:
            if timer.timer_up():
                asyncio.run(plug.turn_off())
                break
            else:
                data = rungcode()
                status = data["status"]
                heatertemp = data["htemp"]
            time.sleep(1)
    time.sleep(4)
    check(waittime,maxheatertemp,plug)



def rungcode():
    DSFsock = openDSF()
    r=Gcode(DSFsock,'M408')
    closeDSF(DSFsock)
    response = json.loads(r)
    response = response['result']
    response = json.loads(response)
    state = response['status']
    print(state)
    heatertemp = response['heaters'][1]
    return(dict(status = state, htemp = heatertemp))

initial()
