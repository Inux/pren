import zmq
import zmq.auth

import src.raspi.lib.zmq_topics as zmq_topics

#Define Ports for all Components
PORT_ACOUSTIC = 28281
PORT_CONTROLFLOW = 28282
PORT_LINEDETECTOR = 28283
PORT_MOVEMENT = 28284
PORT_NUMBERDETECTOR = 28285
PORT_WEBAPP = 28286

def __get_reader(port):
    context = zmq.Context()
    socket = context.socket(zmq.SUB)
    socket.connect("tcp://127.0.0.1:{}".format(port))

    return socket

def __get_sender(port):
    context = zmq.Context()
    socket = context.socket(zmq.PUB)
    socket.bind("tcp://*:{}".format(port))

    return socket

# Reader

__ar = None
def get_acoustic_reader():
    global __ar
    if __ar is None:
        __ar =  __get_reader(PORT_ACOUSTIC)
        __ar.setsockopt(zmq.SUBSCRIBE, zmq_topics.HEARTBEAT_TOPIC)
        __ar.setsockopt(zmq.SUBSCRIBE, zmq_topics.ACKNOWLEDGE_TOPIC)
    return __ar

__cr = None
def get_controlflow_reader():
    global __cr
    if __cr is None:
        __cr = __get_reader(PORT_CONTROLFLOW)
        __cr.setsockopt(zmq.SUBSCRIBE, zmq_topics.SYSTEM_STATUS_TOPIC)
        __cr.setsockopt(zmq.SUBSCRIBE, zmq_topics.HEARTBEAT_TOPIC)
        __cr.setsockopt(zmq.SUBSCRIBE, zmq_topics.ACKNOWLEDGE_TOPIC)
    return __cr

__lr = None
def get_linedetector_reader():
    global __lr
    if __lr is None:
        __lr = __get_reader(PORT_LINEDETECTOR)
        __lr.setsockopt(zmq.SUBSCRIBE, zmq_topics.DIRECTION_TOPIC)
        __lr.setsockopt(zmq.SUBSCRIBE, zmq_topics.HEARTBEAT_TOPIC)
        __lr.setsockopt(zmq.SUBSCRIBE, zmq_topics.ACKNOWLEDGE_TOPIC)
    return __lr

__mr = None
def get_movement_reader():
    global __mr
    if __mr is None:
        __mr = __get_reader(PORT_MOVEMENT)
        __mr.setsockopt(zmq.SUBSCRIBE, zmq_topics.SPEED_TOPIC)
        __mr.setsockopt(zmq.SUBSCRIBE, zmq_topics.CURRENT_TOPIC)
        __mr.setsockopt(zmq.SUBSCRIBE, zmq_topics.HEARTBEAT_TOPIC)
        __mr.setsockopt(zmq.SUBSCRIBE, zmq_topics.ACKNOWLEDGE_TOPIC)
    return __mr

__nr = None
def get_numberdetector_reader():
    global __nr
    if __nr is None:
        __nr = __get_reader(PORT_NUMBERDETECTOR)
        __nr.setsockopt(zmq.SUBSCRIBE, zmq_topics.NUMBER_DETECTION_TOPIC)
        __nr.setsockopt(zmq.SUBSCRIBE, zmq_topics.HEARTBEAT_TOPIC)
    return __nr

__wr = None
def get_webapp_reader():
    global __wr
    if __wr is None:
        __wr = __get_reader(PORT_WEBAPP)
        __wr.setsockopt(zmq.SUBSCRIBE, zmq_topics.MOVE_CMD_TOPIC)
        __wr.setsockopt(zmq.SUBSCRIBE, zmq_topics.ACOUSTIC_TOPIC)
        __wr.setsockopt(zmq.SUBSCRIBE, zmq_topics.SYSTEM_CMD_TOPIC)
    return __wr

# Sender

__acs = None
def get_acoustic_sender():
    global __acs
    if __acs is None:
        __acs = __get_sender(PORT_ACOUSTIC)
    return __acs

__cs = None
def get_controlflow_sender():
    global __cs
    if __cs is None:
        __cs = __get_sender(PORT_CONTROLFLOW)
    return __cs

__ls = None
def get_linedetector_sender():
    global __ls
    if __ls is None:
        __ls = __get_sender(PORT_LINEDETECTOR)
    return __ls

__ms = None
def get_movement_sender():
    global __ms
    if __ms is None:
        __ms = __get_sender(PORT_MOVEMENT)
    return __ms

__ns = None
def get_numberdetector_sender():
    global __ns
    if __ns is None:
        __ns = __get_sender(PORT_NUMBERDETECTOR)
    return __ns

__ws = None
def get_webapp_sender():
    global __ws
    if __ws is None:
        __ws = __get_sender(PORT_WEBAPP)
    return __ws
