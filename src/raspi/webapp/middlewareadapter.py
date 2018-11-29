#!/usr/bin/env python

import logging
import sys
sys.path.append('..')
import os
import select

import zmq

from pb import direction_pb2


PUBLISHER_IP = 'localhost'
PORT = 8282

#Topics
DIRECTION_TOPIC = b'direction'

socket = None

#Data Fields
dataDirection = ''

class Data(object):
    pass

def create():
    global socket
    socket = _make_socket()

def destroy():
    global socket
    socket.close()

def get_data():
    global socket
    global dataDirection

    dataobj = Data()

    if socket.poll(timeout=1, flags=zmq.POLLIN) & zmq.POLLIN == zmq.POLLIN:
        topic_and_data = socket.recv()
        print(topic_and_data)
        dataraw = topic_and_data.split(b' ', 1)[1]

        direction = direction_pb2.Direction()
        direction.ParseFromString(dataraw)

        dataDirection = direction

    #set Data object
    dataobj.direction = dataDirection

    return dataobj

#private methods

def _make_socket():
    context = zmq.Context()

    socket = context.socket(zmq.SUB)

    _connect_and_subscribe_socket(socket)

    return socket

def _connect_and_subscribe_socket(socket):
    socket.connect("tcp://{ip}:{port}".format(ip=PUBLISHER_IP, port=PORT))

    socket.setsockopt(zmq.SUBSCRIBE, DIRECTION_TOPIC)
