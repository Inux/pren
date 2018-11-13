# -*- coding: utf-8 -*-
"""Server for the Raspi Webapp
"""
import os
from sanic import Sanic
from sanic.response import json
from sanic.response import file

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

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=2828)
