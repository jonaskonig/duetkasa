import asyncio
import datetime
import json
import time
import requests
from kasa import SmartPlug
from datetime import datetime
from datetime import timedelta
import DuetWebAPI as DWA
import timer as counter
waittime = 1
heatermaxtemp = None
def initial():
    with open('conf.json') as json_file:
        data = json.load(json_file)
        plug = SmartPlug(data["kasa_ip"])
        waittime = int(data["timebeforshutdown"])
        heatermaxtemp = int(data["maxheatertemp"])
        printer = DWA.DuetWebAPI("http://"+data["duet_ip"])
        check(waittime,heatermaxtemp,plug,printer)


def check(waittime,maxheatertemp,plug,printer):
    timer = counter.Timer(waittime)
    asyncio.run(plug.update())
    emeterdata = asyncio.run(plug.get_emeter_realtime())
    write_data(emeterdata)
    if plug.is_on and emeterdata["power"] < 20:
        print(emeterdata["power"])
        if printer.getStatus() == "idle":
                print(printer.getStatus())
                while printer.getTemperatures()[1]["lastReading"] <= maxheatertemp and printer.getStatus() == "idle":
                    asyncio.run(plug.update())
                    emeterdata = asyncio.run(plug.get_emeter_realtime())
                    write_data(emeterdata)
                    if timer.timer_up():
                        asyncio.run(plug.turn_off())
                        break
                    else:
                        print("Not there jet")
                        time.sleep(1)
    print("Sleeping!")
    #time.sleep(1)
    check(waittime,maxheatertemp,plug,printer)

def write_data(emeterdata):
    emeterdata["time"] = str(datetime.now())
    with open("data.json") as datain:
        try:
            data = json.load(datain)
            data["reading"].append(emeterdata)
        except:
            print("vermutlich leer!")
            data = {}
            data["reading"] = []
            data["reading"].append(emeterdata)
    with open("data.json", "w") as dataout:
        json.dump(data,dataout)



initial()
