#!/usr/bin/env python
from src.raspi.lib import zmq_socket
from src.raspi.lib import zmq_msg

# Sockets
sender_linedetector = zmq_socket.get_linedetector_sender()

def send_direction(direction):
    zmq_msg.send_direction(sender_linedetector, direction)
