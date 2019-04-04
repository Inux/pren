#!/usr/bin/env python

import logging
import os
import select
import zmq

from src.raspi.lib import zmq_socket
from src.raspi.pb import direction_pb2
from src.raspi.pb import heartbeat_pb2

# Topics
DIRECTION_TOPIC = b'direction'
HEARTBEAT_TOPIC = b'heartbeat'

# Sockets
reader_linedetector = zmq_socket.get_linedetector_reader()

data = {}
data['direction'] = "undefined"
data['state'] = "undefined"
data['state_message'] = "undefined"
data['speed'] = 0
data['position'] = 0
data['x_acceleration'] = 0
data['y_acceleration'] = 0
data['z_acceleration'] = 0
data['direction'] = 'undefined'
data['heartbeat_linedetection'] = 'error'
data['heartbeat_numberdetection'] = 'error'
data['heartbeat_movement'] = 'error'
data['heartbeat_acoustic'] = 'error'
data['heartbeat_controlflow'] = 'error'

# Data Fields
def get_data():
    global data

    if reader_linedetector.poll(timeout=1, flags=zmq.POLLIN) & zmq.POLLIN == zmq.POLLIN:
        topic_and_data = reader_linedetector.recv()
        dataraw = topic_and_data.split(b' ', 1)[1]

        dir_obj = direction_pb2.Direction()
        dir_obj.ParseFromString(dataraw)

        data['direction'] = dir_obj.direction

        #heartbeat = heartbeat_pb2.Heartbeat()
        #heartbeat.component .ParseFromString(dataraw)

        #dataHeartbeat = heartbeat


    return data
