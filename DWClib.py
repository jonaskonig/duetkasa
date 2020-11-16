import socket

import json



def openDSF():
    s = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
    s.connect('/var/run/dsf/dcs.sock')
    s.setblocking(True)
    j=json.dumps({"mode":"command"}).encode()
    s.send(j)
    r=s.recv(128).decode()
    if (-1 == r.find('{"version":')):
          print("Failed to enter command mode - version not received")
          print(r)
          exit(8)
    if (-1 == r.find('{"success":true}')):   #could be in same buffer as version
        r=s.recv(128).decode()
        if (-1 == r.find('{"success":true}')):
              print("Failed to enter command mode - success not received")
              print(r)
              exit(8)
    return(s)



def closeDSF(s):
    s.close()



def Gcode(s,cmd=''):
    j=json.dumps({"code": cmd,"channel": 0,"command": "SimpleCode"}).encode()
    s.send(j)
    r=s.recv(2048).decode()
    return(r)



def getPos(s):
  result = json.loads(Gcode(s,'M408'))['result']
  pos = json.loads(result)['pos']
  print('getPos = '+str(pos))
  return pos
