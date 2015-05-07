#!/usr/bin/python

import ssl
from websocket import websocket
import sys
from pprint import pprint
import json
from threading import Timer


###### begin Bridge ############


sys.path.insert(0, '/usr/lib/python2.7/bridge/')
from bridgeclient import BridgeClient as bridgeclient


bridgeCli = bridgeclient()

### initial switch state is off
bridgeCli.put('switch1','0')

# Impulses of  Powermeters
previousPowermeterImpulseOne = 0
previousPowermeterImpulseTwo = 0

### timer for looping Bridge output

def loopImpulseOneBridge():
         global previousPowermeterImpulseOne
         currentPowermeterImpulse = float(bridgeCli.get('PowerMeterImpulseOne'))
         print(currentPowermeterImpulse)
         kWmin = currentPowermeterImpulse - previousPowermeterImpulseOne
         if previousPowermeterImpulseOne != 0:
                ws.send('{"variable":"1","value":'+str(kWmin)+'}')
         previousPowermeterImpulseOne = currentPowermeterImpulse
         Timer(60.0, loopImpulseOneBridge).start()  # have to read every 60 minutes

def loopImpulseTwoBridge():
         global previousPowermeterImpulseTwo
         currentPowermeterImpulse = float(bridgeCli.get('PowerMeterImpulseTwo'))
         print(currentPowermeterImpulse)
         kWmin = currentPowermeterImpulse - previousPowermeterImpulseTwo
         if previousPowermeterImpulseTwo != 0:
                ws.send('{"variable":"2","value":'+str(kWmin)+'}')
         previousPowermeterImpulseTwo = currentPowermeterImpulse
         Timer(60.0, loopImpulseTwoBridge).start()  # have to read every 60 minutes

##### end Bridge ##################

#### begin ws debugTrace ################
print sys.argv

for i in range(len(sys.argv)):
    if i == 0:
        print "Funktion name: %s" % sys.argv[0]
    else:
        print "%d. Argument: %s" % (i,sys.argv[i])

##### end ws debugTrace #################

##### begin Websocket #############

def on_message(ws, message):
        global savedTemperature
        jsonData = json.loads(message)
        print "unit = %s" % jsonData["unit"]
        print (type(jsonData["task"]))
        print "task = %s" % jsonData["task"]

###  REMROB control
        if int(jsonData["unit"]) == 20 and int(jsonData ["task"]) == 30:
          print("switchOn")
          bridgeCli.put('switch1','1')
          ws.send('{"unit":20,"state":30}')
        elif int(jsonData ["unit"]) == 20 and int(jsonData ["task"]) == 50:
          print("switchOff")
          bridgeCli.put('switch1','0')
          ws.send('{"unit":20,"state":50}')
        else:
          print "error"

def on_error(ws, error):
        print (error)
#       pprint(vars(ws.sock.sock))

def on_close(ws):
        print ("... closed ...")

def on_open(ws):
        Timer(1.0, loopImpulseOneBridge).start()
        Timer(2.0, loopImpulseTwoBridge).start()
        print ("opend")
#       pprint(vars(ws))
        ### show initial state of switch as Off
        ws.send('{"unit":20,"state":50}')

if __name__ == "__main__":
#websocket.enableTrace(True)
    if len(sys.argv) < 2:
#       host = "wss://echo.websocket.org/"
        print("passed")
        host = 'wss://rws.remrob.com/?model=741&id=1&key=741' # default
    else:
        host = sys.argv[1]

ws = websocket.WebSocketApp(host,
                               on_message = on_message,
                                on_error = on_error,
                                on_close = on_close)

#ws = websocket.WebSocketApp("wss://echo.websocket.org")

ws.on_open = on_open
#    ws.on_message = on_message
#    ws.on_error = on_error
#    ws.on_close = on_close
ws.run_forever()
##### end websocket #############

