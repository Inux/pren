#!/usr/bin/env python

import logging
import os
import select
import zmq

import src.raspi.lib.log as log
from src.raspi.lib import zmq_socket
from src.raspi.lib import zmq_topics
from src.raspi.pb import direction_pb2
from src.raspi.pb import move_command_pb2
from src.raspi.pb import heartbeat_pb2
from src.raspi.pb import speed_pb2
from src.raspi.pb import current_pb2
from src.raspi.lib import zmq_heartbeat_listener

logger = log.getLogger("SoulTrain.webapp.mw_adapter_server")

# Sockets
reader_linedetector = zmq_socket.get_linedetector_reader()
reader_movement = zmq_socket.get_movement_reader()
sender_webapp = zmq_socket.get_webapp_sender()
hb_listener = zmq_heartbeat_listener.HeartBeatListener()

data = {} # data will be updated by HeartBeatListener
data['direction'] = "undefined"
data['state'] = "undefined"
data['state_message'] = "undefined"
data['speed'] = 0
data['position'] = 0
data['x_acceleration'] = 0
data['y_acceleration'] = 0
data['z_acceleration'] = 0
data['direction'] = 'undefined'

# Data Fields
def get_data():
    global data

    heartbeats = hb_listener.get_data()
    data.update(heartbeats) # append heartbeats data to data object

    #Handle LineDetector in Messages
    if reader_linedetector.poll(timeout=1, flags=zmq.POLLIN) & zmq.POLLIN == zmq.POLLIN:
        topic_and_data = reader_linedetector.recv()
        topic = topic_and_data.split(b' ', 1)[0]
        dataraw = topic_and_data.split(b' ', 1)[1]

        if topic == zmq_topics.DIRECTION_TOPIC:
            #Try Parse Direction
            dir_obj = direction_pb2.Direction()
            dir_obj.ParseFromString(dataraw)

            if dir_obj is not None:
                logger.debug("received direction: '%s'", dir_obj.direction)
                data['direction'] = dir_obj.direction
                return data

    #Handle Movement in Messages
    if reader_movement.poll(timeout=1, flags=zmq.POLLIN) & zmq.POLLIN == zmq.POLLIN:
        topic_and_data = reader_movement.recv()
        topic = topic_and_data.split(b' ', 1)[0]
        dataraw = topic_and_data.split(b' ', 1)[1]

        if topic == zmq_topics.SPEED_TOPIC:
            #Try Parse Speed
            speed = speed_pb2.Speed()
            speed.ParseFromString(dataraw)

            if speed is not None:
                logger.debug("received speed '%s'", speed.speed)
                data['speed'] = speed.speed
                return data

        if topic == zmq_topics.CURRENT_TOPIC:
            #Try Parse Current
            current = current_pb2.Current()
            current.ParseFromString(dataraw)

            if current is not None:
                logger.debug("received current '%s'", current.current)
                data['current'] = current.current
                return data

    return data

def send_move_cmd(speed):
    move_cmd = move_command_pb2.MoveCommand()
    move_cmd.speed = speed
    msg = move_cmd.SerializeToString()
    logger.info("Sending move command. Speed: '%s'", move_cmd.speed)
    sender_webapp.send(zmq_topics.MOVE_CMD_TOPIC + b' ' + msg)
