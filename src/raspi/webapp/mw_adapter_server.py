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
from src.raspi.pb import acceleration_pb2
from src.raspi.pb import number_detection_pb2
from src.raspi.pb import acoustic_command_pb2
from src.raspi.pb import crane_command_pb2
from src.raspi.pb import distance_pb2
from src.raspi.pb import acknowledge_pb2
from src.raspi.lib import zmq_heartbeat_listener
from src.raspi.lib import heartbeat as hb
from src.raspi.lib import zmq_ack

logger = log.getLogger("SoulTrain.webapp.mw_adapter_server")

# Sockets
reader_linedetector = zmq_socket.get_linedetector_reader()
reader_movement = zmq_socket.get_movement_reader()
sender_webapp = zmq_socket.get_webapp_sender()
hb_listener = zmq_heartbeat_listener.HeartBeatListener()

data = {} # data will be updated by HeartBeatListener
data['state'] = "undefined"
data['state_message'] = "undefined"
data['speed'] = 0
data['distance'] = 0
data['x_acceleration'] = 0
data['y_acceleration'] = 0
data['z_acceleration'] = 0
data['direction'] = "undefined"
data['number'] = 0
data['cube'] = 0
data['crane'] = 0
data[zmq_ack.ACK_RECV_CRANE_CMD+","+hb.COMPONENT_MOVEMENT] = False

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

        if topic == zmq_topics.ACCELERATION_TOPIC:
            # Try Parse Acceleration
            acceleration = acceleration_pb2.Acceleration()
            acceleration.ParseFromString(dataraw)

            if acceleration is not None:
                logger.debug("received acceleration in x-axis '%s'", acceleration.x)
                logger.debug("received acceleration in y-axis '%s'", acceleration.y)
                logger.debug("received acceleration in z-axis '%s'", acceleration.z)
                data['x_acceleration'] = acceleration.x
                data['y_acceleration'] = acceleration.y
                data['z_acceleration'] = acceleration.z

        if topic == zmq_topics.CURRENT_TOPIC:
            #Try Parse Current
            current = current_pb2.Current()
            current.ParseFromString(dataraw)

            if current is not None:
                logger.debug("received current '%s'", current.current)
                data['current'] = current.current

        if topic == zmq_topics.DISTANCE_TOPIC:
            #Try Parse Distance
            distance = distance_pb2.Distance()
            distance.ParseFromString(dataraw)

            if distance is not None:
                logger.debug("received distance '%s'", distance.distance)
                data['distance'] = distance.distance

        if topic == zmq_topics.ACKNOWLEDGE_TOPIC:
            #Try Parse Acknowledge
            ack = acknowledge_pb2.Acknowledge()
            ack.ParseFromString(dataraw)

            if ack is not None:
                logger.debug("received ack -> action: '%s', component: '%s'", ack.action, ack.component)
                data[ack.action+","+ack.component] = True

    return data

def send_move_cmd(speed):
    move_cmd = move_command_pb2.MoveCommand()
    move_cmd.speed = speed
    msg = move_cmd.SerializeToString()
    logger.info("Sending move command. Speed: '%s'", move_cmd.speed)
    sender_webapp.send(zmq_topics.MOVE_CMD_TOPIC + b' ' + msg)

def send_acoustic_cmd(number):
    acoustic_cmd = acoustic_command_pb2.AcousticCommand()
    acoustic_cmd.number = number
    msg = acoustic_cmd.SerializeToString()
    logger.info("Sending acoustic command. Number: '%s'", acoustic_cmd.number)
    sender_webapp.send(zmq_topics.ACOUSTIC_TOPIC + b' ' + msg)

def send_crane_cmd(state):
    crane_cmd = crane_command_pb2.CraneCommand()
    crane_cmd.command = state
    msg = crane_cmd.SerializeToString()
    logger.info("Sending crane command. Number: '%s'", crane_cmd.command)
    sender_webapp.send(zmq_topics.CRANE_CMD_TOPIC + b' ' + msg)
