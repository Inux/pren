'''
Implements the protocol between raspi and the tiny
'''
import time

import serial

from src.raspi.movement.messages import Message

class Protocol():
    '''
    The protocol itself
    '''
    def __init__(self, device, baud):
        self.device = device
        self.baud = baud
        self.conn = None
        self.ack_map = {}

        #Maps the received message to the function which either
        #sets the internal value or does a handling with the received value directly
        self.recv_map = {
            Message.IS_SPEED : self.__set_recv_speed,
            Message.CUBE : self.__set_recv_cube,
            Message.CURRENT : self.__set_recv_current,
            Message.LOG : self.__set_recv_log
        }

    def connect(self):
        '''
        connects to the serial port
        '''
        if self.conn is None:
            self.conn = serial.Serial(self.device, baudrate=self.baud, timeout=3.0)

    def disconnect(self):
        '''
        disconnects to the serial port
        '''
        if self.conn is not None:
            self.conn.close()

    def send_speed(self, speed):
        '''
        write speed to tiny (mm/s)
        '''
        self.__write_cmd(Message.SPEED, speed)

    def send_crane(self, state):
        '''
        write crane cmd to tiny
        '''
        if state in range(0, 1):
            self.__write_cmd(Message.CRANE, state)

    def send_phase(self, phase):
        '''
        write the phase to tiny
        '''
        if phase in range(0, 7):
            self.__write_cmd(Message.PHASE, phase)

    def send_ack(self, message):
        '''
        write the ack to tiny
        '''
        self.__write_cmd(Message.ACK, message)

    def __write_cmd(self, message, value):
        if self.conn is not None:
            self.conn.write(str(message.value)+","+str(value)+"\n")
            self.ack_map[message.value] = time.time()

    def receive_handler(self):
        '''
        handles the received lines
        '''
        if self.conn is not None:
            line = self.conn.readline(timeout=1)
            if line != "" and line is not None:
                self.__parse_line(line)

    def __parse_line(self, line):
        try:
            l = line.split(',')
            msg = l[0]
            val = l[1]
        except Exception as e:


    def __set_recv_speed(self, val):
        pass

    def __set_recv_cube(self, val):
        pass

    def __set_recv_current(self, val):
        pass

    def __set_recv_log(self, val):
        pass

    def __set_recv_ack(self, val):
        pass
