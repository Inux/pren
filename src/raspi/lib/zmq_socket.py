import zmq
import zmq.auth

PORT = 2828

def make_socket():
    context = zmq.Context()
    socket = context.socket(zmq.PUB)
    socket.bind("tcp://*:{}".format(PORT))

    return socket
