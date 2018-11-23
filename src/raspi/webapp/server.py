# -*- coding: utf-8 -*-
"""Server for the Raspi Webapp
"""
import asyncio
import os
import sys
import signal
from sanic import Sanic
from sanic.response import json
from sanic.response import file

app = Sanic()
app.name = "PrenTeam28WebApp"

MIDDLEWARE_SCAN_INTERVAL = 0.100 # 100ms

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
    ''' api returns the API JSON available under /api '''
    return json({'direction': 'right'})

# Middleware handling

async def periodic_middleware_task(app):
    ''' periodic task for retrieving middleware messages '''
    print(app.name + '. Reading Middleware Messages...')
    asyncio.sleep(MIDDLEWARE_SCAN_INTERVAL)
    app.add_task(periodic_middleware_task(app))

if __name__ == '__main__':
    signal.signal(signal.SIGINT, signal_int_handler)
    app.add_task(periodic_middleware_task(app))
    app.run(host='0.0.0.0', port=2828)
