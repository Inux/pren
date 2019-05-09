#!/usr/bin/env python

import src.raspi.lib.log as log
from src.raspi.lib import zmq_socket
from src.raspi.lib import zmq_topics
from src.raspi.lib import zmq_msg
from src.raspi.lib import zmq_heartbeat_listener
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
data[zmq_ack.ACK_RECV_ACOUSTIC_CMD] = False
data[zmq_ack.ACK_RECV_MOVE_CMD] = False
data[zmq_ack.ACK_RECV_CRANE_CMD] = False

def _set_data(key, val):
    logger.info("received -> key: " + str(key) + ", value: " + str(val))
    data[key] = val

# Data Fields
def get_data():
    heartbeats = hb_listener.get_data()
    data.update(heartbeats) # append heartbeats data to data object

    #Handle LineDetector in Messages
    zmq_msg.recv(
        reader_linedetector,
        {
            zmq_topics.DIRECTION_TOPIC: lambda obj: _set_data('direction', obj.direction)
        }
    )

    zmq_msg.recv(
        reader_movement,
        {
            zmq_topics.SPEED_TOPIC: lambda obj: _set_data('speed', obj.speed),
            zmq_topics.ACCELERATION_TOPIC: lambda obj: [
                _set_data('x_acceleration', obj.x),
                _set_data('y_acceleration', obj.y),
                _set_data('z_acceleration', obj.z),
            ],
            zmq_topics.DISTANCE_TOPIC: lambda obj: _set_data('distance', obj.distance),
            zmq_topics.ACKNOWLEDGE_TOPIC: lambda obj: _set_data(obj.action, True),
            zmq_topics.CURRENT_TOPIC: lambda obj: _set_data('current', obj.current),
            zmq_topics.CUBE_STATUS: lambda obj: _set_data('cube', obj.state)
        }
    )

    return data

def send_move_cmd(speed):
    logger.info("Sending move command. Speed: '%s'", speed)
    zmq_msg.send_move_cmd(sender_webapp, speed)

def send_acoustic_cmd(number):
    logger.info("Sending acoustic command. Number: '%s'", number)
    zmq_msg.send_acoustic_cmd(sender_webapp, number)

def send_crane_cmd(state):
    logger.info("Sending crane command. Command: '%s'", state)
    zmq_msg.send_crane_cmd(sender_webapp, state)

def send_sys_cmd(command, phases):
    logger.info("Sending system command. Command: '%s', Phases: '%s'", command, str(phases))
    zmq_msg.send_system_cmd(sender_webapp, command, phases)
