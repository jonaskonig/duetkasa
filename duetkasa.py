import asyncio
import datetime
import json
import time
import requests
from kasa import SmartPlug
from datetime import datetime
from datetime import timedelta
from duetwebapi import DuetWebAPI
timer = None;
waittime = 1
heatermaxtemp = None
plugip = None
duet_host = None
with open('conf.json') as json_file:
    data = json.load(json_file)
    duet_host = data["duet_ip"]
    plugip = data["kasa_ip"]
    waittime = int(data["timebeforshutdown"])
    heatermaxtemp = int(data["maxheatertemp"])
printer = DuetWebAPI("http://"+duet_host)
plug = SmartPlug(plugip)
while True:
    asyncio.run(plug.update())
    if plug.is_on:
        json_data = printer.send_code("M408")
        response = json_data['response']
        response = json.loads(response)
        status = response['status']
        heatertemp = response['heaters'][1]
        #print(heatertemp)
        if status == "I" and heatertemp <= heatermaxtemp:
            if timer == None:
                timer = datetime.now()+timedelta(minutes=waittime)
            else:
                if timer < datetime.now():
                    asyncio.run(plug.turn_off())
                    timer = None
        else:
            timer = None
    else:
        timer = None
    time.sleep(1)
