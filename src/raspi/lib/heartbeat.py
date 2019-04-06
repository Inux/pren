import sys

import src.raspi.lib.log as log
import src.raspi.lib.zmq_topics as zmq_topics
from src.raspi.pb import heartbeat_pb2

STATUS_STARTING = "starting"
STATUS_RUNNING = "running"
STATUS_ERROR = "error"
STATUS_FINISHED = "finished"

COMPONENT_LINEDETECTION = "linedetection"
COMPONENT_NUMBERDETECTION = "numberdetection"
COMPONENT_MOVEMENT = "movement"
COMPONENT_ACOUSTIC = "acoustic"
COMPONENT_CONTROLFLOW = "controlflow"
COMPONENT_WEBAPP = "webapp"

logger = log.getLogger('SoulTrain.lib.heartbeat')

def send_heartbeat(socket, component, status):
    msg = get_heartbeat_msg(component, status)
    logger.debug("Sending HeartBeat for '%s' with status '%s'", component, status)
    socket.send(zmq_topics.HEARTBEAT_TOPIC + b' ' + msg)

def get_heartbeat_msg(component, status):
    heartbeat = heartbeat_pb2.Heartbeat()
    heartbeat.component = component
    heartbeat.status = status
    return heartbeat.SerializeToString()
