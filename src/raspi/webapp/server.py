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

from src.raspi.acoustic import sound
from src.raspi.lib import heartbeat
import src.raspi.webapp.mw_adapter_server as mwadapter

app = Sanic()
app.name = "PrenTeam28WebApp"

app.static('/static', os.path.join(os.path.dirname(__file__), 'static'))

MIDDLEWARE_SCAN_INTERVAL = 0.010 # 50ms

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
        position = middlewareData['position']
        x_acceleration = middlewareData['x_acceleration']
        y_acceleration = middlewareData['y_acceleration']
        z_acceleration = middlewareData['z_acceleration']
        direction = middlewareData['direction']
        linedetector = middlewareData['linedetector']
        numberdetector = middlewareData['numberdetector']
        movement = middlewareData['movement']
        acoustic = middlewareData['acoustic']
        controlflow = middlewareData['controlflow']

    return json({
        'state': str(state),
        'stateMessage': str(state_message),
        'speed': str(speed),
        'position': str(position),
        'xAcceleration': str(x_acceleration),
        'yAcceleration': str(y_acceleration),
        'zAcceleration': str(z_acceleration),
        'direction': str(direction),
        'heartBeatLineDetector': str(linedetector),
        'heartBeatNumberDetector': str(numberdetector),
        'heartBeatMovement': str(movement),
        'heartBeatAcoustic': str(acoustic),
        'heartBeatControlFlow': str(controlflow)
    })

@app.route('/sound/<sound_nr>')
async def play_sound(request, sound_nr):
    sound.play_sound_by_number(sound_nr)
    return json({'received': True})

@app.route('/speed/<speed>')
async def send_speed(request, speed):
    mwadapter.send_move_cmd(int(speed))
    return json({'received': True})

# Middleware handling

async def periodic_middleware_task(app):
    global middlewareData
    ''' periodic task for retrieving middleware messages '''
    middlewareData = mwadapter.get_data()
    time.sleep(MIDDLEWARE_SCAN_INTERVAL)
    app.add_task(periodic_middleware_task(app))

if __name__ == '__main__':
    signal.signal(signal.SIGINT, signal_int_handler)
    app.add_task(periodic_middleware_task(app))
    app.run(host='0.0.0.0', port=2828)
