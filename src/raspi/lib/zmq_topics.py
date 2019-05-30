'''
zmq topics used for soultrain
'''

ACCELERATION_TOPIC = b'acceleration'
ACKNOWLEDGE_TOPIC = b'acknowledge'
ACOUSTIC_TOPIC = b'acoustic'
CRANE_CMD_TOPIC = b'cranecommand'
#use message for both cmd and state
#for movement it is a command, for others it's the state sent from movement
CRANE_STATE = CRANE_CMD_TOPIC
CURRENT_TOPIC = b'current'
DIRECTION_TOPIC = b'direction'
DISTANCE_TOPIC = b'distance'
HEARTBEAT_TOPIC = b'heartbeat'
MOVE_CMD_TOPIC = b'movecommand'
NUMBER_DETECTOR_TOPIC = b'numberdetector'
SPEED_TOPIC = b'speed'
SYSTEM_CMD_TOPIC = b'systemcommand'
SYSTEM_STATUS_TOPIC = b'systemstatus'
CUBE_STATUS = b'cubestatus'
ROUND = b'round'
