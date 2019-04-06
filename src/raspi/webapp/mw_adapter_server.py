#!/usr/bin/env python

import logging
import os
import select
import zmq

import src.raspi.lib.log as log
from src.raspi.lib import zmq_socket
from src.raspi.pb import direction_pb2
from src.raspi.pb import heartbeat_pb2

logger = log.getLogger("SoulTrain.webapp.mw_adapter_server")

# Sockets
reader_linedetector = zmq_socket.get_linedetector_reader()
reader_movement = zmq_socket.get_movement_reader()

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
data['linedetection'] = 'error'
data['numberdetection'] = 'error'
data['movement'] = 'error'
data['acoustic'] = 'error'
data['controlflow'] = 'error'

# Data Fields
def get_data():
    global data

    #Handle LineDetector in Messages
    if reader_linedetector.poll(timeout=1, flags=zmq.POLLIN) & zmq.POLLIN == zmq.POLLIN:
        topic_and_data = reader_linedetector.recv()
        dataraw = topic_and_data.split(b' ', 1)[1]

        #Try Parse Direction
        dir_obj = direction_pb2.Direction()
        dir_obj.ParseFromString(dataraw)

        if dir_obj is not None:
            logger.debug("received direction: '%s'", dir_obj.direction)
            data['direction'] = dir_obj.direction
            return data

        #Try Parse HeartBeat
        heartbeat = heartbeat_pb2.Heartbeat()
        heartbeat.ParseFromString(dataraw)

        if heartbeat is not None:
            logger.debug("received heartbeat from '%s' with status '%s'", heartbeat.component, heartbeat.status)
            data[heartbeat.component] = heartbeat.status
            return data

    #Handle Movement in Messages
    if reader_movement.poll(timeout=1, flags=zmq.POLLIN) & zmq.POLLIN == zmq.POLLIN:
        topic_and_data = reader_movement.recv()
        dataraw = topic_and_data.split(b' ', 1)[1]

        #Try Parse HeartBeat
        heartbeat = heartbeat_pb2.Heartbeat()
        heartbeat.ParseFromString(dataraw)

        if heartbeat is not None:
            logger.debug("received heartbeat from '%s' with status '%s'", heartbeat.component, heartbeat.status)
            data[heartbeat.component] = heartbeat.status
            return data

    return data
