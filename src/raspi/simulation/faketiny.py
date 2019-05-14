'''
Implements the protocol between raspi and the tiny
'''
import time
import datetime
import threading

import serial

from src.raspi.movement.messages import Message

RESEND_TIME=0.05

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
            Message.SPEED.value : self.__send_is_speed,
            Message.CRANE.value : self.__send_crane,
            Message.PHASE.value : self.__set_phase
        }

    def connect(self):
        '''
        connects to the serial port
        '''
        if self.conn is None:
            self.conn = serial.Serial(self.device, baudrate=self.baud, timeout=3)

    def disconnect(self):
        '''
        disconnects to the serial port
        '''
        if self.conn is not None:
            self.conn.close()

    def send_ack(self, message):
        '''
        write the ack to tiny
        '''
        self.__write_cmd(Message.ACK, message)

    def __write_cmd(self, message, value):
        if self.conn is not None:
            msg = str(message.value)+","+str(value)+"\n"
            print(str(datetime.datetime.now()) +" -> send msg: " + str(message.value) + "," + str(value))

            self.conn.write(msg.rstrip(' \t\r\0').encode())

    def rcv_handler(self):
        '''
        handles the received lines
        '''
        if self.conn is not None:
            while self.conn.in_waiting:
                line = self.conn.readline()

                #Expect to have byte array
                try:
                    line = line.decode('utf-8')
                except AttributeError:
                    pass

                line = line.strip(' \t\n\r ')
                if line is not None and line != "":
                    self.__parse_line(line)

    def __parse_line(self, line):
        rcv_msg=""
        rcv_key=""
        try:
            key_value = line.split(',')
            if len(key_value) >= 2:
                rcv_msg = key_value[0].strip(' \t\n\r ')
                rcv_val = key_value[1].strip(' \t\n\r ')

                if rcv_msg in self.recv_map.keys():
                    self.recv_map[rcv_msg](rcv_val) #call specific recv handler

        except KeyError as e:
            pass

    def __send_is_speed(self, val):
        print(str(datetime.datetime.now()) +" -> handle is_speed -> val: " + str(val))
        self.send_ack(Message.IS_SPEED.value)
        self.__write_cmd(Message.IS_SPEED, val)

    def __send_crane(self, val):
        print(str(datetime.datetime.now()) +" -> handle crane -> val: " + str(val))
        self.send_ack(Message.CRANE.value)
        crane_thread = threading.Thread(target=self.send_delayed, args=(Message.IS_CRANE, 1,))
        crane_thread.start()

    def __set_phase(self, val):
        print(str(datetime.datetime.now()) +" -> handle phase -> val: " + str(val))
        if 1 == int(val): # find_cube phase
            cube_thread = threading.Thread(target=self.send_delayed, args=(Message.CUBE, 1,))
            cube_thread.start()
        if 0 == int(val): # startup phase
            self.__write_cmd(Message.CUBE, 0)

        self.send_ack(Message.PHASE.value)

    def send_delayed(self, msg, val):
        time.sleep(5)
        self.__write_cmd(msg, val)

if __name__ == '__main__':
    proto = Protocol('/dev/ttys012', 115200)
    proto.connect()
    while True:
        proto.rcv_handler()
        time.sleep(0.2)

