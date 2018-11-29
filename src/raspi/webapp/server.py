# -*- coding: utf-8 -*-
"""Server for the Raspi Webapp
"""
import sys
sys.path.append('..')
import os
import signal
import time

from sanic import Sanic
from sanic.response import json
from sanic.response import file

from acoustic import sound
import middlewareadapter as mwadapter

app = Sanic()
app.name = "PrenTeam28WebApp"

MIDDLEWARE_SCAN_INTERVAL = 0.100 # 100ms

middlewareData = None

# SIGINT handler (when pressing Ctrl+C)

def signal_int_handler(sig, frame):
    print("Ctrl+C Pressed. Exit...")
    sys.exit(0)

# Start middleware adapter
mwadapter.create()

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
    if middlewareData != None:
        direction = middlewareData.direction
    return json({'direction': str(direction)})


@app.route('/sound/<sound_nr>')
async def play_sound(request, sound_nr):
    print('playing sound: ' + sound_nr)
    sound.Sound.play_sound_by_number(sound_nr)
    return json({'received': True})

@app.route('/simulation/set', methods=["POST",])
async def simulationSet(request):
    print('simulating')
    print(request.json)

    return json({'received': True})

@app.route('/simulation/get')
async def simulationGet(request):
    print('getting sim data')

    mov_dict = {}
    mov_dict['acc'] = 20
    mov_dict['speed'] = 20
    mov_dict['distance'] = 20
    return json(mov_dict)

# Middleware handling

async def periodic_middleware_task(app):
    global middlewareData
    ''' periodic task for retrieving middleware messages '''
    print(app.name + '. Reading Middleware Messages...')
    middlewareData = mwadapter.get_data()
    print('Direction: ' + str(middlewareData.direction))
    time.sleep(MIDDLEWARE_SCAN_INTERVAL)
    app.add_task(periodic_middleware_task(app))

if __name__ == '__main__':
    signal.signal(signal.SIGINT, signal_int_handler)
    app.add_task(periodic_middleware_task(app))
    app.run(host='0.0.0.0', port=2828)
