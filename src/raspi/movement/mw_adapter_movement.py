#!/usr/bin/env python
import os
import select
import zmq

import src.raspi.lib.log as log
from src.raspi.lib import zmq_socket
from src.raspi.lib import zmq_topics
from src.raspi.pb import speed_pb2
from src.raspi.pb import current_pb2
from src.raspi.pb import acceleration_pb2
from src.raspi.pb import heartbeat_pb2
from src.raspi.pb import move_command_pb2

logger = log.getLogger("SoulTrain.movement.mw_adapter_movement")

# Sockets
sender_movement = zmq_socket.get_movement_sender()
reader_webapp = zmq_socket.get_webapp_reader()

data = {}
data['speed'] = 0

def send_speed(speed):
    speed = speed_pb2.Speed()
    speed.speed = speed
    msg = speed.SerializeToString()
    sender_movement.send(zmq_topics.SPEED_TOPIC + b' ' + msg)

def send_current(current):
    current = current_pb2.Current()
    current.current = current
    msg = current.SerializeToString()
    sender_movement.send(zmq_topics.CURRENT_TOPIC + b' ' + msg)

def send_acceleration(x, y, z):
    acc = acceleration_pb2.Acceleration()
    acc.x = x
    acc.y = y
    acc.z = z
    msg = acc.SerializeToString()
    sender_movement.send(zmq_topics.ACCELERATION_TOPIC + b' ' + msg)

def send_distance(distance):
    distance = distance.Speed()
    distance.distance = distance
    msg = distance.SerializeToString()
    sender_movement.send(zmq_topics.DISTANCE_TOPIC + b' ' + msg)

# Data Fields
def get_data():
    global data

    if reader_webapp.poll(timeout=1, flags=zmq.POLLIN) & zmq.POLLIN == zmq.POLLIN:
        topic_and_data = reader_webapp.recv()
        topic_and_data = topic_and_data.split(b' ')
        topic = topic_and_data[0]
        dataraw = topic_and_data[1]

        #Try parse move command
        move_cmd = move_command_pb2.MoveCommand()
        move_cmd.ParseFromString(dataraw)

        if move_cmd is not None:
            logger.info("received move command. Speed: '%s'", move_cmd.speed)
            data['speed'] = move_cmd.speed
            return data

    return data

