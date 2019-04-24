#!/usr/bin/env python
import os
import select
import zmq

import src.raspi.lib.log as log
from src.raspi.lib import zmq_socket
from src.raspi.lib import zmq_topics
from src.raspi.pb import number_detection_pb2

# Sockets
sender_numberdetector = zmq_socket.get_linedetector_sender()

def send_number(number):
    msg_number = number_detection_pb2.NumberDetection()
    msg_number.number = number
    msg = msg_number.SerializeToString()
    sender_numberdetector.send(zmq_topics.NUMBER_DETECTOR_TOPIC + b' ' + msg)