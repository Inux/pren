'''
Implements the protocol between raspi and the tiny
'''
import time

import serial
from src.raspi.movement.fakeserialdevice import FakeSerial

from src.raspi.movement.messages import Message
import src.raspi.lib.log as logger

class Protocol():
    '''
    The protocol itself
    '''
    def __init__(self, device, baud,
                 onNewSpeed=None, onNewCurrent=None, real_device=True):
        self.log = logger.getLogger('SoulTrain.movement.protocol')
        self.logTiny = logger.getLogger('SoulTrain.movement.tiny')

        self.real_device = real_device

        self.device = device
        self.baud = baud
        self.conn = None
        self.ack_map = {}

        #Maps the received message to the function which either
        #sets the internal value or does a handling with the received value directly
        self.recv_map = {
            Message.IS_SPEED.value : self.__set_recv_speed,
            Message.CUBE.value : self.__set_recv_cube,
            Message.CURRENT.value : self.__set_recv_current,
            Message.LOG.value : self.__set_recv_log,
            Message.ACK.value : self.__set_recv_ack
        }

        #Internal values received from tiny
        self.is_speed = None
        self.cube = None
        self.current = None

        #CallBacks
        self.onNewSpeed = onNewSpeed
        self.onNewCurrent = onNewCurrent

    def connect(self):
        '''
        connects to the serial port
        '''
        if self.conn is None:
            if self.real_device:
                self.conn = serial.Serial(self.device, baudrate=self.baud, timeout=3.0)
            else:
                self.conn = FakeSerial()

    def disconnect(self):
        '''
        disconnects to the serial port
        '''
        if self.conn is not None:
            self.conn.close()

    def get_speed(self):
        return self.is_speed

    def get_cube(self):
        return self.cube

    def get_current(self):
        return self.current

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

    def print_ack_map(self):
        for key, value in self.ack_map.items():
            self.log.info("Awaiting HeartBeat for '%s' since '%s'", key, str(time.ctime(value)))

    def __write_cmd(self, message, value):
        if self.conn is not None:
            msg = str(message.value)+","+str(value)+"\n"

            if self.real_device:
                self.log.info("Sending over uart. Msg: " + msg)
                self.conn.write(msg.rstrip(' \t\r\0').encode())
            else:
                self.log.info("Sending over fake console. Msg: " + msg)
                self.conn.write(msg)

            self.ack_map[message.value] = time.time()

    def rcv_handler(self):
        '''
        handles the received lines
        '''
        if self.conn is not None:
            while self.conn.in_waiting:
                line = self.conn.readline()
                if line != "" and line is not None:
                    self.__parse_line(line)

    def __parse_line(self, line):
        try:
            line = line.decode('utf-8')
            key_value = line.split(',')
            if len(key_value) >= 2:
                msg = key_value[0].replace("\n", "").replace("\t", "").replace(" ", "")
                val = key_value[1].replace("\n", "").replace("\t", "").replace(" ", "")

                self.log.info("Parsed line with Msg: '%s', Value: '%s'", msg, val)
                if msg in self.recv_map.keys():
                    self.log.info("Execution method of Msg: '%s'", msg)
                    self.recv_map[msg](val) #call specific recv handler

        except Exception as e:
            self.log.error("Could not parse line: '%s'. Exception: %s", line, e)

    def __set_recv_speed(self, val):
        if self.is_speed != int(val):
            self.is_speed = int(val)
            if self.onNewSpeed is not None:
                self.onNewSpeed(int(val))

        self.send_ack(Message.IS_SPEED.value)

    def __set_recv_cube(self, val):
        self.cube = int(val)
        self.send_ack(Message.CUBE.value)

    def __set_recv_current(self, val):
        if self.current != int(val):
            self.current = int(val)
            if self.onNewCurrent is not None:
                self.onNewCurrent(int(val))

        self.send_ack(Message.CURRENT.value)

    def __set_recv_log(self, val):
        self.logTiny.info(val) #log tiny log messages
        self.send_ack(Message.LOG.value)

    def __set_recv_ack(self, val):
        if val in self.ack_map.keys():
            del self.ack_map[val]
