#!/usr/bin/env python

import src.raspi.lib.log as log
from src.raspi.lib import zmq_socket
from src.raspi.lib import zmq_topics
from src.raspi.lib import zmq_msg
from src.raspi.lib import zmq_heartbeat_listener
from src.raspi.lib import zmq_ack
from src.raspi.lib import heartbeat as hb

logger = log.getLogger("SoulTrain.webapp.mw_adapter_server")

# Sockets
reader_linedetector = zmq_socket.get_linedetector_reader()
reader_movement = zmq_socket.get_movement_reader()
reader_ctrlflow = zmq_socket.get_controlflow_reader()
reader_numberdetection = zmq_socket.get_numberdetector_reader()
sender_webapp = zmq_socket.get_webapp_sender()
hb_listener = zmq_heartbeat_listener.HeartBeatListener()

data = {} # data will be updated by HeartBeatListener

def clear_states():
    global data
    data['phase'] = "undefined"
    data['phase_message'] = "undefined"
    data['speed'] = 0
    data['distance'] = 0
    data['x_acceleration'] = 0
    data['y_acceleration'] = 0
    data['z_acceleration'] = 0
    data['direction'] = "undefined"
    data['number'] = "undefined"
    data['round'] = "undefined"
    data['cube'] = 0
    data['crane'] = 0
    data[zmq_ack.ACK_RECV_ACOUSTIC_CMD] = False
    data[zmq_ack.ACK_RECV_MOVE_CMD] = False
    data[zmq_ack.ACK_RECV_CRANE_CMD] = False

def _set_data(key, val):
    global data

    logger.debug("received -> key: " + str(key) + ", value: " + str(val))
    data[key] = val

# Data Fields
def get_data():
    global data

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
            zmq_topics.CUBE_STATUS: lambda obj: _set_data('cube', obj.state),
            zmq_topics.CRANE_STATE: lambda obj: _set_data('crane', obj.command)
        }
    )

    zmq_msg.recv(
        reader_ctrlflow,
        {
            zmq_topics.SYSTEM_STATUS_TOPIC: lambda obj: [
                _set_data('phase', obj.phase),
                _set_data('phase_message', obj.message)
            ]
        }
    )

    zmq_msg.recv(
        reader_numberdetection,
        {
            zmq_topics.ROUND: lambda obj: [
                _set_data('round', obj.round)
            ],
            zmq_topics.NUMBER_DETECTOR_TOPIC: lambda obj: [
                _set_data('number', obj.number)
            ]
        }
    )

    return data

def send_move_cmd(speed):
    zmq_msg.send_move_cmd(sender_webapp, speed)
    logger.info("Sending move command. Speed: '%s'", speed)

def send_acoustic_cmd(number):
    zmq_msg.send_acoustic_cmd(sender_webapp, number)
    logger.info("Sending acoustic command. Number: '%s'", number)

def send_crane_cmd(state):
    zmq_msg.send_crane_cmd(sender_webapp, state)
    logger.info("Sending crane command. Command: '%s'", state)

def send_sys_cmd(command, phases):
    zmq_msg.send_system_cmd(sender_webapp, command, phases)
    logger.info("Sending system command. Command: '%s', Phases: '%s'", command, str(phases))

def reset_tiny():
    zmq_msg.send_crane_cmd(sender_webapp, 42) #magic!

def send_phase(phase):
    zmq_msg.send_system_status(sender_webapp, phase, "simulating...")

def send_hb():
    hb.send_heartbeat(sender_webapp, hb.COMPONENT_WEBAPP, hb.STATUS_RUNNING)
