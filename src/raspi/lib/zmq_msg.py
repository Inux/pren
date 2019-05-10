import zmq
import src.raspi.lib.zmq_topics as zmq_topics
import src.raspi.pb.acceleration_pb2 as acceleration_pb2
import src.raspi.pb.acknowledge_pb2 as acknowledge_pb2
import src.raspi.pb.acoustic_command_pb2 as acoustic_command_pb2
import src.raspi.pb.crane_command_pb2 as crane_command_pb2
import src.raspi.pb.current_pb2 as current_pb2
import src.raspi.pb.cube_pb2 as cube_pb2
import src.raspi.pb.direction_pb2 as direction_pb2
import src.raspi.pb.distance_pb2 as distance_pb2
import src.raspi.pb.heartbeat_pb2 as heartbeat_pb2
import src.raspi.pb.move_command_pb2 as move_command_pb2
import src.raspi.pb.number_detection_pb2 as number_detection_pb2
import src.raspi.pb.speed_pb2 as speed_pb2
import src.raspi.pb.system_command_pb2 as system_command_pb2
import src.raspi.pb.system_status_pb2 as system_status_pb2

topic_proto_map = {
    zmq_topics.ACCELERATION_TOPIC: acceleration_pb2.Acceleration,
    zmq_topics.ACKNOWLEDGE_TOPIC: acknowledge_pb2.Acknowledge,
    zmq_topics.ACOUSTIC_TOPIC: acoustic_command_pb2.AcousticCommand,
    zmq_topics.CRANE_CMD_TOPIC: crane_command_pb2.CraneCommand,
    zmq_topics.CURRENT_TOPIC: current_pb2.Current,
    zmq_topics.CUBE_STATUS: cube_pb2.Cube,
    zmq_topics.DIRECTION_TOPIC: direction_pb2.Direction,
    zmq_topics.DISTANCE_TOPIC: distance_pb2.Distance,
    zmq_topics.HEARTBEAT_TOPIC: heartbeat_pb2.Heartbeat,
    zmq_topics.MOVE_CMD_TOPIC: move_command_pb2.MoveCommand,
    zmq_topics.NUMBER_DETECTOR_TOPIC: number_detection_pb2.NumberDetection,
    zmq_topics.SPEED_TOPIC: speed_pb2.Speed,
    zmq_topics.SYSTEM_CMD_TOPIC: system_command_pb2.SystemCommand,
    zmq_topics.SYSTEM_STATUS_TOPIC: system_status_pb2.SystemStatus,
}

def send_acceleration(socket, x, y, z):
    acc = acceleration_pb2.Acceleration()
    acc.x = x
    acc.y = y
    acc.z = z
    msg = acc.SerializeToString()
    socket.send(zmq_topics.ACCELERATION_TOPIC + b' ' + msg)

def send_ack(socket, action, component):
    ack = acknowledge_pb2.Acknowledge()
    ack.action = action
    ack.component = component
    msg = ack.SerializeToString()
    socket.send(zmq_topics.ACKNOWLEDGE_TOPIC + b' ' + msg)

def send_acoustic_cmd(socket, number):
    acoustic_cmd = acoustic_command_pb2.AcousticCommand()
    acoustic_cmd.number = number
    msg = acoustic_cmd.SerializeToString()
    socket.send(zmq_topics.ACOUSTIC_TOPIC + b' ' + msg)

def send_crane_cmd(socket, state):
    crane_cmd = crane_command_pb2.CraneCommand()
    crane_cmd.command = state
    msg = crane_cmd.SerializeToString()
    socket.send(zmq_topics.CRANE_CMD_TOPIC + b' ' + msg)

def send_current(socket, current):
    curr = current_pb2.Current()
    curr.current = current
    msg = curr.SerializeToString()
    socket.send(zmq_topics.CURRENT_TOPIC + b' ' + msg)

def send_cube_state(socket, state):
    cube = cube_pb2.Cube()
    cube.state = state
    msg = cube.SerializeToString()
    socket.send(zmq_topics.CUBE_STATUS + b' ' + msg)

def send_direction(socket, direction):
    d = direction_pb2.Direction()
    d.direction = direction
    msg = d.SerializeToString()
    socket.send(zmq_topics.DIRECTION_TOPIC + b' ' + msg)

def send_distance(socket, distance):
    dist = distance_pb2.Distance()
    dist.distance = distance
    msg = dist.SerializeToString()
    socket.send(zmq_topics.DISTANCE_TOPIC + b' ' + msg)

def send_move_cmd(socket, speed):
    move_cmd = move_command_pb2.MoveCommand()
    move_cmd.speed = speed
    msg = move_cmd.SerializeToString()
    socket.send(zmq_topics.MOVE_CMD_TOPIC + b' ' + msg)

def send_detected_number(socket, number):
    nd = number_detection_pb2.NumberDetection()
    nd.number = number
    msg = nd.SerializeToString()
    socket.send(zmq_topics.NUMBER_DETECTOR_TOPIC + b' ' + msg)

def send_speed(socket, speed):
    s = speed_pb2.Speed()
    s.speed = speed
    msg = s.SerializeToString()
    socket.send(zmq_topics.SPEED_TOPIC + b' ' + msg)

def send_system_cmd(socket, command, phases):
    c = system_command_pb2.SystemCommand()
    c.command = command
    for k, v in phases.items():
        c.phases[k] = v
    msg = c.SerializeToString()
    socket.send(zmq_topics.SYSTEM_CMD_TOPIC + b' ' + msg)

def send_system_status(socket, phase, message):
    s = system_status_pb2.SystemStatus()
    s.phase = phase
    s.message = message
    msg = s.SerializeToString()
    socket.send(zmq_topics.SYSTEM_STATUS_TOPIC + b' ' + msg)

def recv(socket, map_topic_callback):
    '''
    receive a middleware message
    '''
    if socket.poll(timeout=0.05, flags=zmq.POLLIN) & zmq.POLLIN == zmq.POLLIN:
        topic_and_data = socket.recv()
        recv_topic = topic_and_data.split(b' ', 1)[0]
        dataraw = topic_and_data.split(b' ', 1)[1]

        for topic, callback in map_topic_callback.items():
            if recv_topic == topic:
                #Try Parse the Message
                obj = topic_proto_map[topic]()
                obj.ParseFromString(dataraw)

                if obj is not None:
                    callback(obj)
