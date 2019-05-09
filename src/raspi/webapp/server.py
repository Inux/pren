# -*- coding: utf-8 -*-
"""Server for the Raspi Webapp
"""
import sys
import os
import signal
import time
from sanic import Sanic
from sanic.response import json
from sanic.response import file

import src.raspi.webapp.mw_adapter_server as mwadapter
from src.raspi.lib import zmq_ack
from src.raspi.lib import heartbeat as hb
import src.raspi.lib.log as log

logger = log.getLogger("SoulTrain.webapp.server")

app = Sanic()
app.name = "PrenTeam28WebApp"

app.static('/static', os.path.join(os.path.dirname(__file__), 'static'))

middlewareData = None

# SIGINT handler (when pressing Ctrl+C)

def signal_int_handler(sig, frame):
    print("Ctrl+C Pressed. Exit...")
    sys.exit(0)

# Routes

@app.route('/')
async def index(request):
    ''' index returns index.html available under / '''
    return await file(os.path.join(os.path.dirname(__file__), "index.html"))

@app.route('/favicon.ico')
async def favicon(request):
    ''' favicon returns favicon.ico available under /favicon.ico '''
    return await file(os.path.join(os.path.dirname(__file__), "favicon.ico"))

@app.route('/api')
async def api(request):
    global middlewareData
    ''' api returns the API JSON available under /api '''
    direction = 'undefined'
    if middlewareData is not None:
        state = middlewareData['state']
        state_message = middlewareData['state_message']
        speed = middlewareData['speed']
        distance = middlewareData['distance']
        x_acceleration = middlewareData['x_acceleration']
        y_acceleration = middlewareData['y_acceleration']
        z_acceleration = middlewareData['z_acceleration']
        direction = middlewareData['direction']
        number = middlewareData['number']
        cube = middlewareData['cube']
        crane = middlewareData['crane']
        linedetector = middlewareData['linedetector']
        numberdetector = middlewareData['numberdetector']
        movement = middlewareData['movement']
        acoustic = middlewareData['acoustic']
        controlflow = middlewareData['controlflow']

    return json({
        'state': str(state),
        'stateMessage': str(state_message),
        'speed': str(speed),
        'distance': str(distance),
        'xAcceleration': str(x_acceleration),
        'yAcceleration': str(y_acceleration),
        'zAcceleration': str(z_acceleration),
        'direction': str(direction),
        'number': str(number),
        'cube': str(cube),
        'crane': str(crane),
        'heartBeatLineDetector': str(linedetector),
        'heartBeatNumberDetector': str(numberdetector),
        'heartBeatMovement': str(movement),
        'heartBeatAcoustic': str(acoustic),
        'heartBeatControlFlow': str(controlflow)
    })

@app.route('/sound/<sound_nr>')
async def play_sound(request, sound_nr):
    mwadapter.send_acoustic_cmd(int(sound_nr))
    return json({'received': True})

@app.route('/speed/<speed>')
async def send_speed(request, speed):
    global middlewareData

    middlewareData['speed_ack'] = False
    mwadapter.send_move_cmd(int(speed))
    return json({'received': True})

@app.route('/crane/<state>')
async def send_crane_cmd(request, state):
    if int(state) == 1:
        mwadapter.send_crane_cmd(1)
    else:
        mwadapter.send_crane_cmd(0)
    return json({'received': True})

# Middleware handling

async def periodic_middleware_task(app):
    global middlewareData
    ''' periodic task for retrieving middleware messages '''
    middlewareData = mwadapter.get_data()

    #Change crane value if we receive acknowledge
    if zmq_ack.ACK_RECV_CRANE_CMD in middlewareData.keys():
        if middlewareData[zmq_ack.ACK_RECV_CRANE_CMD] is True:
            logger.info("received crane cmd ack from movement")
            if middlewareData['crane'] == 0:
                middlewareData['crane'] = 1
            else:
                middlewareData['crane'] = 0
            middlewareData[zmq_ack.ACK_RECV_CRANE_CMD] = False

    #Change speed ack value if we receive acknowledge
    if zmq_ack.ACK_RECV_MOVE_CMD in middlewareData.keys():
        if middlewareData[zmq_ack.ACK_RECV_MOVE_CMD] is True:
            logger.info("received move cmd ack from movement")
            middlewareData['speed_ack'] = True
            middlewareData[zmq_ack.ACK_RECV_MOVE_CMD] = False

    app.add_task(periodic_middleware_task(app))

if __name__ == '__main__':
    signal.signal(signal.SIGINT, signal_int_handler)
    app.add_task(periodic_middleware_task(app))
    app.run(host='0.0.0.0', port=2828, debug=False, access_log=False)
