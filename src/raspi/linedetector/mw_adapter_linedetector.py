#!/usr/bin/env python
import os
import select
import zmq

import src.raspi.lib.log as log
from src.raspi.lib import zmq_socket
from src.raspi.lib import zmq_topics
from src.raspi.pb import direction_pb2

# Sockets
sender_linedetector = zmq_socket.get_linedetector_sender()

def send_direction(direction):
    msg_direction = direction_pb2.Direction()
    msg_direction.direction = direction
    msg = msg_direction.SerializeToString()
    sender_linedetector.send(zmq_topics.DIRECTION_TOPIC + b' ' + msg)
