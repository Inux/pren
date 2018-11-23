# -*- coding: utf-8 -*-
"""Server for the Raspi Webapp
"""
import sys
sys.path.append('../')

import os
from sanic import Sanic
from sanic.response import json
from sanic.response import file

from acoustic import sound

app = Sanic()

@app.route('/')
async def index(request):
    return await file(os.path.join(os.path.dirname(__file__), "index.html"))

@app.route('/favicon.ico')
async def favicon(request):
    return await file(os.path.join(os.path.dirname(__file__), "favicon.ico"))

@app.route('/api')
async def api(request):
    return json({'direction': 'right'})


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

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=2828)


async def notify_server_started_after_five_seconds():
    print('Server successfully started!')

app.add_task(notify_server_started_after_five_seconds())