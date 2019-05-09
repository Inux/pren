#!/usr/bin/env python
import os
import select
import zmq

import src.raspi.lib.log as log
from src.raspi.lib import zmq_socket
from src.raspi.lib import zmq_msg

# Sockets
sender_numberdetector = zmq_socket.get_linedetector_sender()

def send_number(number):
    zmq_msg.send_detected_number(sender_numberdetector, number)
