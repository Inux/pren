# -*- coding: utf-8 -*-
"""Server for the Raspi Webapp
"""
import sys
import os
import signal
import json as j
import time
from sanic import Sanic
from sanic.response import json
from sanic.response import file

import src.raspi.webapp.mw_adapter_server as mw_adapter_server
from src.raspi.lib import zmq_ack
from src.raspi.config import config as cfg
from src.raspi.lib import heartbeat as hb
import src.raspi.lib.log as log

logger = log.getLogger("SoulTrain.webapp.server")

app = Sanic()
app.name = "PrenTeam28WebApp"

app.static('/static', os.path.join(os.path.dirname(__file__), 'static'))

middlewareData = None
hb_last_sent = 0.0
is_simulation_mode = True

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
        phase = middlewareData['phase']
        phase_message = middlewareData['phase_message']
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
        'phase': str(phase),
        'phaseMessage': str(phase_message),
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
    mw_adapter_server.send_acoustic_cmd(int(sound_nr))
    return json({'received': True})

@app.route('/speed/<speed>')
async def send_speed(request, speed):
    global middlewareData

    middlewareData['speed_ack'] = False
    mw_adapter_server.send_move_cmd(int(speed))
    return json({'received': True})

@app.route('/crane/<state>')
async def send_crane_cmd(request, state):
    global middlewareData

    middlewareData['crane_ack'] = False
    if int(state) == 1:
        mw_adapter_server.send_phase(cfg.PHASE_GRAB_CUBE)
        mw_adapter_server.send_crane_cmd(1)
    else:
        mw_adapter_server.reset_tiny()
        mw_adapter_server.send_crane_cmd(0)
    return json({'received': True})

class Payload(object):
    def __init__(self, json_string):
        self.__dict__ = j.loads(json_string)

@app.post('/controlflow')
async def send_controlflow_cmd(request):
    json_string = request.body.decode('utf-8')
    p = Payload(json_string)

    if 'start' in p.command:
        mw_adapter_server.reset_tiny()
        mw_adapter_server.clear_states() #clear states when starting controlflow

    mw_adapter_server.send_sys_cmd(p.command, dict(p.phases))
    return json({'received': True})

@app.route('/mode/<state>')
async def set_mode(request, state):
    global is_simulation_mode

    if int(state) == 1:
        logger.info("Switched to Simulation Mode!")
        mw_adapter_server.send_phase(cfg.PHASE_FIND_CUBE) #otherwise tiny will not send this state
        is_simulation_mode = True
    else:
        logger.info("Switched to ControlFlow Mode!")
        is_simulation_mode = False

    return json({'received': True})

@app.route('/resettiny')
async def reset_tiny(request):
    mw_adapter_server.reset_tiny()

    return json({'received': True})

# Middleware handling

async def periodic_middleware_task(app):
    global middlewareData
    global hb_last_sent

    ''' periodic task for handling middleware '''

    #send heartbeat
    if (hb_last_sent+(float(cfg.HB_INTERVAL)/1000)) < time.time():
        hb_last_sent = time.time()
        mw_adapter_server.send_hb()

    middlewareData = mw_adapter_server.get_data()

    #Change crane value if we receive acknowledge
    if zmq_ack.ACK_RECV_CRANE_CMD in middlewareData.keys():
        if middlewareData[zmq_ack.ACK_RECV_CRANE_CMD] is True:
            logger.info("received crane cmd ack from movement")
            middlewareData['crane_ack'] = True
            middlewareData[zmq_ack.ACK_RECV_CRANE_CMD] = False

    #Change speed ack value if we receive acknowledge
    if zmq_ack.ACK_RECV_MOVE_CMD in middlewareData.keys():
        if middlewareData[zmq_ack.ACK_RECV_MOVE_CMD] is True:
            logger.info("received move cmd ack from movement")
            middlewareData['speed_ack'] = True
            middlewareData[zmq_ack.ACK_RECV_MOVE_CMD] = False

    app.add_task(periodic_middleware_task(app))

if __name__ == '__main__':
    mw_adapter_server.clear_states() #set default values
    signal.signal(signal.SIGINT, signal_int_handler)
    app.add_task(periodic_middleware_task(app))
    app.run(host='0.0.0.0', port=2828, debug=False, access_log=False)
