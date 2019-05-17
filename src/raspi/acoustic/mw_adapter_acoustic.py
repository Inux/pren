#!/usr/bin/env python
from src.raspi.lib import zmq_socket
from src.raspi.lib import zmq_topics
from src.raspi.lib import zmq_msg

# Sockets
reader_number = zmq_socket.get_numberdetector_reader()
reader_web = zmq_socket.get_webapp_reader()

data_acoustic = {}
data_acoustic['number'] = 0

def _set_data(key, val):
    global data_acoustic
    data_acoustic[key] = val

# Data Fields
def get_data():
    global data_acoustic

    zmq_msg.recv(
        reader_web,
        {
            zmq_topics.ACOUSTIC_TOPIC: lambda obj: _set_data('number', obj.number)
        }
    )

    zmq_msg.recv(
        reader_number,
        {
            zmq_topics.NUMBER_DETECTOR_TOPIC: lambda obj: _set_data('number', obj.number)
        }
    )

    return data_acoustic
