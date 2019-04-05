# -*- coding: utf-8 -*-
"""Fake Line Detector
"""
import time

import zmq
import zmq.auth

from src.raspi.lib import zmq_socket
from src.raspi.pb import direction_pb2

PORT = 8282
DIRECTION_TOPIC = b'direction'

OFFSET = 0
DIRECTIONS = ['straight', 'left', 'right']

def _main():
    socket = zmq_socket.get_linedetector_sender()

    try:
        while True:
            send_messages(socket)
            time.sleep(5)

    except KeyboardInterrupt:
        raise

def send_messages(socket):
    direction = get_direction_update()
    socket.send(DIRECTION_TOPIC + b' ' + direction)

def get_direction_update():
    direction = direction_pb2.Direction()
    direction.direction = get_dir()
    directionBytes = direction.SerializeToString()
    return directionBytes

def get_dir():
    global OFFSET
    global DIRECTIONS

    d = DIRECTIONS[OFFSET]
    OFFSET = OFFSET + 1
    if OFFSET >= len(DIRECTIONS):
        OFFSET = 0

    return d

if __name__ == '__main__':
    _main()
