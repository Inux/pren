#!/usr/bin/env python
import src.raspi.lib.log as log
from src.raspi.lib import zmq_socket
from src.raspi.lib import zmq_topics
from src.raspi.lib import zmq_msg
from src.raspi.lib import zmq_heartbeat_listener
from src.raspi.lib import zmq_ack

logger = log.getLogger("SoulTrain.controlflow.mw_adapter_ctrlflow")

# Sockets
reader_linedetector = zmq_socket.get_linedetector_reader()
reader_movement = zmq_socket.get_movement_reader()
reader_webapp = zmq_socket.get_webapp_reader()
sender_ctrlflow = zmq_socket.get_controlflow_sender()
reader_number_detector = zmq_socket.get_numberdetector_reader()
hb_listener = zmq_heartbeat_listener.HeartBeatListener()

mw_data_ctrlflow = {} # data will be updated by HeartBeatListener
mw_data_ctrlflow['sys_cmd'] = ''
mw_data_ctrlflow['phases'] = dict()

def clear_states():
    global mw_data_ctrlflow

    #Clear only data! (some mw_data_ctrlflow should not be deleted!)
    mw_data_ctrlflow['speed'] = 0
    mw_data_ctrlflow['distance'] = 0
    mw_data_ctrlflow['x_acceleration'] = 0
    mw_data_ctrlflow['y_acceleration'] = 0
    mw_data_ctrlflow['z_acceleration'] = 0
    mw_data_ctrlflow['direction'] = "undefined"
    mw_data_ctrlflow['number'] = None
    mw_data_ctrlflow['cube'] = 0
    mw_data_ctrlflow['crane'] = 0
    mw_data_ctrlflow[zmq_ack.ACK_RECV_MOVE_CMD] = False
    mw_data_ctrlflow[zmq_ack.ACK_RECV_CRANE_CMD] = False

def set_data(key, val, log=True):
    global mw_data_ctrlflow
    mw_data_ctrlflow[key] = val
    if log:
        log_set_data(key, val)

def log_set_data(key, val):
    logger.debug("received -> key: " + str(key) + ", value: " + str(val))

def _set_sys_cmd(command, phases):
    global mw_data_ctrlflow
    logger.info("received sys cmd -> command: " + str(command) + ", phases: " + str(dict(phases)))
    mw_data_ctrlflow['sys_cmd'] = str(command)
    mw_data_ctrlflow['phases'] = dict(phases)

# Data Fields
def get_data():
    global mw_data_ctrlflow

    heartbeats = hb_listener.get_data()
    mw_data_ctrlflow.update(heartbeats) # append heartbeats data to data object

    #Handle LineDetector in Messages
    zmq_msg.recv(
        reader_linedetector,
        {
            zmq_topics.DIRECTION_TOPIC: lambda obj: set_data('direction', obj.direction)
        }
    )

    zmq_msg.recv(
        reader_movement,
        {
            zmq_topics.SPEED_TOPIC: lambda obj: set_data('speed', obj.speed),
            zmq_topics.ACCELERATION_TOPIC: lambda obj: [
                set_data('x_acceleration', obj.x),
                set_data('y_acceleration', obj.y),
                set_data('z_acceleration', obj.z),
            ],
            zmq_topics.DISTANCE_TOPIC: lambda obj: set_data('distance', obj.distance),
            zmq_topics.ACKNOWLEDGE_TOPIC: lambda obj: set_data(obj.action, True),
            zmq_topics.CURRENT_TOPIC: lambda obj: set_data('current', obj.current),
            zmq_topics.CUBE_STATUS: lambda obj: set_data('cube', obj.state),
            zmq_topics.CRANE_STATE: lambda obj: set_data('crane', obj.command)
        }
    )

    zmq_msg.recv(
        reader_webapp,
        {
            zmq_topics.SYSTEM_CMD_TOPIC: lambda obj: _set_sys_cmd(obj.command, dict(obj.phases))
        }
    )

    zmq_msg.recv(
        reader_number_detector,
        {
            zmq_topics.NUMBER_DETECTOR_TOPIC: lambda obj: set_data('number', obj.number)
        }
    )

    return mw_data_ctrlflow

def send_move_cmd(speed):
    zmq_msg.send_move_cmd(sender_ctrlflow, speed)
    logger.info("Sending move command. Speed: '%s'", speed)

def send_acoustic_cmd(number):
    zmq_msg.send_acoustic_cmd(sender_ctrlflow, number)
    logger.info("Sending acoustic command. Number: '%s'", number)

def send_crane_cmd(state):
    zmq_msg.send_crane_cmd(sender_ctrlflow, state)
    logger.info("Sending crane command. Command: '%s'", state)

def send_sys_status(phase, message):
    zmq_msg.send_system_status(sender_ctrlflow, str(phase), str(message))
    logger.debug("Sending sys status. Phase: '%s', Message :'%s'", phase, message)
