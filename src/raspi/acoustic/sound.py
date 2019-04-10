import pyttsx3

import zmq
import zmq.auth

#import direction_pb2
#from pb import direction_pb2

PORT = 8282
DIRECTION_TOPIC = b'sound'

OFFSET = 0
DIRECTIONS = ['straight', 'left', 'right']

def main():
    make_socket()


def make_socket():
    context = zmq.Context()
    socket = context.socket(zmq.PUB)
    socket.bind("tcp://*:{}".format(PORT))

    return socket

def play_sound_by_number(number):
    engine = pyttsx3.init()
    engine.say('Number ' + str(number))
    print('start playing')
    engine.runAndWait()
    print('stopped playing')

def buzz_by_number(number):
    print('buzzing ' + str(number) + ' times')
    for i in range(number):
        print('bzzzz')

