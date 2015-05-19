#!/usr/bin/python

import logging
import ssl
from websocket import websocket
import sys
import json
from threading import Timer

# Author: Michael Macherey

###### logging #####
logger = logging.getLogger('powermeter')
logger.setLevel(logging.DEBUG) #ERROR
# create file handler which logs even debug messages
fh = logging.FileHandler('/root/powermeter.log')
fh.setLevel(logging.DEBUG) #DEBUG

# create formatter and add it to the handlers
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
fh.setFormatter(formatter)
# add the handlers to logger
logger.addHandler(fh)

###### begin Bridge ############
sys.path.insert(0, '/usr/lib/python2.7/bridge/')
from bridgeclient import BridgeClient as bridgeclient

bridgeCli = bridgeclient()

# Impulses of  Powermeters
#previousPowermeterImpulseOne = 0
#previousPowermeterImpulseTwo = 0

### timer for looping Bridge output
### timer for looping Bridge output

def loopImpulseOneBridge():
    global previousPowermeterImpulseOne,bridgeCli
    logger.info("ws.sock at ImpOne:  "+str(ws.sock))
    if ws.sock: #is None:
        if not bridgeCli:
            logger.error('ImpulseOne Bridge doesnot exist')
        try:
            currentPowermeterImpulse = float(bridgeCli.get('PowerMeterImpulseOne'))
            logger.info('PowerMeterImpulseOne = '+ str(currentPowermeterImpulse))
        except Exception as e:
            logger.error('Can not read Bridge ImpulseOne')
            logger.error(e)
        else:
            logger.info("CurrentPowermeterImpulse One = " + str(currentPowermeterImp$
            kWmin = currentPowermeterImpulse - previousPowermeterImpulseOne
            if previousPowermeterImpulseOne != 0:
                try:
                    ws.send('{"variable":"1","value":'+str(kWmin)+'}')
                except Exception as e:
                    logger.error('In loopImpulseOneBridge ws.send broken')

            previousPowermeterImpulseOne = currentPowermeterImpulse
    Timer(60.0, loopImpulseOneBridge).start()  # have to read every 60 minutes

def loopImpulseTwoBridge():
    global previousPowermeterImpulseTwo
    logger.info("ws.sock at ImpTwo:  "+str(ws.sock))
    if ws.sock: #is None
        if not bridgeCli:
            logger.error('ImpulseOne Bridge doesnot exist')
        try:
            currentPowermeterImpulse = float(bridgeCli.get('PowerMeterImpulseTwo'))
            logger.info('PowerMeterImpulseTwo = '+ str(currentPowermeterImpulse))
        except Exception as e:
            logger.error('Can not read Bridge ImpulseTwo')
            logger.error(e)
        else:
            logger.info("CurrentPowermeterImpulse Two = " + str(currentPowermeterImp$
            kWmin = currentPowermeterImpulse - previousPowermeterImpulseTwo
            if previousPowermeterImpulseTwo != 0:
                try:
                    ws.send('{"variable":"2","value":'+str(kWmin)+'}')
                except Exception as e:
                    logger.error('In loopImpulseTwoBridge() ws.send broken')
            previousPowermeterImpulseTwo = currentPowermeterImpulse
    Timer(60.0, loopImpulseTwoBridge).start()  # have to read every 60 minutes

##### begin Websocket #############
#def on_message(ws, message):
    #logger.info("on_message() message received"+ str(message))

def on_error(ws, error):
    # pprint(vars(ws.sock.sock))
    logger.exception("Exception in on_error() = " + str(error))

def on_close(ws):
    logger.info("... closed ...")
    Timer(20.0, startSocket).start()

def on_open(ws):
    # Impulses of Powermeters, important for resetting if reconnect, as otherwise off
    global previousPowermeterImpulseOne,previousPowermeterImpulseTwo
    previousPowermeterImpulseOne = 0
    previousPowermeterImpulseTwo = 0
    logger.info("... opend ...")
    ####### initial timers ##########
    Timer(5.0, loopImpulseOneBridge()).start()
    Timer(40.0, loopImpulseTwoBridge()).start()

ws = websocket.WebSocketApp('wss://objects.remrob.com/v1/?model=741&id=1&key=741',on$

def startSocket():
    global ws
    try:
        ws.run_forever()
    except Exception as e:
        logger.error('In startSocket() ws.run_forever broken')

startSocket()
