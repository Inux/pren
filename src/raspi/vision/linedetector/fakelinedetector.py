# -*- coding: utf-8 -*-
"""Fake Line Detector
"""
import random
import time

import zmq
import zmq.auth
from zmq.auth.thread import ThreadAuthenticator
import direction_pb2

PORT = 8282
DIRECTION_TOPIC = b'direction'

def _main():
    socket = make_socket()

    try:
        while True:
            send_messages(socket)
            time.sleep(5)

    except KeyboardInterrupt:
        raise

def make_socket():
    context = zmq.Context()
    socket = context.socket(zmq.PUB)
    socket.bind("tcp://*:{}".format(PORT))

    return socket

def send_messages(socket):
    direction = get_direction_update()
    socket.send(DIRECTION_TOPIC + b' ' + direction)

def get_direction_update():
    direction = direction_pb2.Direction()
    direction.direction = "leftOrRight"
    directionBytes = direction.SerializeToString()
    return directionBytes

if __name__ == '__main__':
    _main()
