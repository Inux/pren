#!/usr/bin/env python
import src.raspi.lib.log as log
from src.raspi.lib import zmq_socket
from src.raspi.lib import zmq_topics
from src.raspi.lib import zmq_msg

logger = log.getLogger("SoulTrain.movement.mw_adapter_movement")

# Sockets
sender_movement = zmq_socket.get_movement_sender()
reader_webapp = zmq_socket.get_webapp_reader()
reader_controlflow = zmq_socket.get_controlflow_reader()

data = {}
data['speed'] = 0
data['crane'] = 0

def send_speed(speed):
    zmq_msg.send_speed(sender_movement, speed)

def send_current(current):
    zmq_msg.send_current(sender_movement, current)

def send_acceleration(x, y, z):
    zmq_msg.send_acceleration(sender_movement, x, y, z)

def send_distance(distance):
    zmq_msg.send_distance(sender_movement, distance)

def send_cube_state(state):
    zmq_msg.send_cube_state(sender_movement, state)

def send_ack(action, component):
    zmq_msg.send_ack(sender_movement, action, component)

def _set_data(key, val):
    logger.info("received -> key: " + str(key) + ", value: " + str(val))
    data[key] = val

# Data Fields
def get_data():
#webapp
    zmq_msg.recv(
        reader_webapp,
        {
            zmq_topics.MOVE_CMD_TOPIC: lambda obj: _set_data('speed', obj.speed),
            zmq_topics.CRANE_CMD_TOPIC: lambda obj: _set_data('crane', obj.command)
        }
    )

#controlflow
    zmq_msg.recv(
        reader_controlflow,
        {
            zmq_topics.MOVE_CMD_TOPIC: lambda obj: _set_data('speed', obj.speed),
            zmq_topics.CRANE_CMD_TOPIC: lambda obj: _set_data('crane', obj.command)
        }
    )

    return data
