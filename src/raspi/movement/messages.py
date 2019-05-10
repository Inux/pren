'''
Defines the messages which are sent between raspi and tiny
'''
from enum import Enum

class Message(Enum):
    '''
    Message enum defines all possible messages
    '''
    SPEED = "speed"
    CRANE = "crane"
    IS_CRANE = 'is_crane'
    PHASE = "phase"
    IS_SPEED = "is_speed"
    CUBE = "cube"
    CURRENT = "current"
    LOG = "log"
    ACK = "ack"
