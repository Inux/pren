import src.raspi.lib.log as log
from src.raspi.config import config
import src.raspi.lib.zmq_topics as zmq_topics
import src.raspi.lib.zmq_msg as zmq_msg
import src.raspi.lib.zmq_socket as zmq_socket
from src.raspi.pb import heartbeat_pb2

# Dont change - has impact on conditional logic
STATUS_STARTING = "starting"
STATUS_RUNNING = "running"
STATUS_ERROR = "error"
STATUS_FINISHED = "finished"

# Dont change - has impact on conditional logic
COMPONENT_LINEDETECTOR = "linedetector"
COMPONENT_NUMBERDETECTOR = "numberdetector"
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

data = {}
data['phase'] = STATUS_ERROR

def _set_data(key, val):
    global data
    data[key] = val

