'''
Implements the protocol between raspi and the tiny
'''
import time

import serial
from src.raspi.movement.fakeserialdevice import FakeSerial

from src.raspi.movement.messages import Message
import src.raspi.lib.log as logger

RESEND_TIME=0.05

class Protocol():
    '''
    The protocol itself
    '''
    def __init__(self, device, baud,
                 onNewSpeed=None, onNewCurrent=None, onNewCubeState=None, resend=True, real_device=True):
        self.log = logger.getLogger('SoulTrain.movement.protocol')
        self.logTiny = logger.getLogger('SoulTrain.movement.tiny')

        self.resend = resend
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

        #Internal values sent to tiny
        self.last_sent_crane_state = None
        self.last_sent_phase = None
        self.last_sent_speed = None

        #CallBacks
        self.onNewSpeed = onNewSpeed
        self.onNewCurrent = onNewCurrent
        self.onNewCubeState = onNewCubeState

        #Stores the methods to execute again when a message has to be resend
        self.resend_map = {
            Message.SPEED.value: lambda: self.send_speed(self.last_sent_speed),
            Message.CRANE.value: lambda: self.send_crane(self.last_sent_crane_state),
            Message.PHASE.value: lambda: self.send_phase(self.last_sent_phase)
        }


    def connect(self):
        '''
        connects to the serial port
        '''
        if self.conn is None:
            if self.real_device:
                self.conn = serial.Serial(self.device, baudrate=self.baud, timeout=3.0)
                self.log.info("connect to device: " + self.device + ", baudrate: " + str(self.baud))
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
        self.last_sent_speed = speed
        self.__write_cmd(Message.SPEED, speed)

    def send_crane(self, state):
        '''
        write crane cmd to tiny
        '''
        if state in range(0, 2):
            self.last_sent_crane_state = state
            self.__write_cmd(Message.CRANE, state)

    def send_phase(self, phase):
        '''
        write the phase to tiny
        '''
        if phase in range(0, 7):
            self.last_sent_phase = phase
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

                #Expect to have byte array
                try:
                    line = line.decode('utf-8')
                except AttributeError:
                    pass

                line = line.strip(' \t\n\r ')
                if line is not None and line != "":
                    self.__parse_line(line)

    def ack_handler(self):
        '''
        resend if not received ack
        '''
        if self.resend:
            for key in self.ack_map.keys():
                if self.ack_map[key]+RESEND_TIME < time.time():
                    if key in self.resend_map.keys():
                        self.resend_map[key]()

    def __parse_line(self, line):
        rcv_msg=""
        rcv_key=""
        try:
            self.log.info("parsing line: '" + line + "'")

            key_value = line.split(',')
            if len(key_value) >= 2:
                rcv_msg = key_value[0].strip(' \t\n\r ')
                rcv_val = key_value[1].strip(' \t\n\r ')

                self.log.info("parsed line with msg: '%s', val: '%s'", str(rcv_msg), str(rcv_val))
                if rcv_msg in self.recv_map.keys():
                    self.log.info("execute method of msg: '%s'", str(rcv_msg))
                    self.recv_map[rcv_msg](rcv_val) #call specific recv handler

        except KeyError as e:
            self.log.error("Could not parse line: '%s', msg: '%s', val: '%s', exception: %s", line, str(rcv_msg), str(rcv_val), e)

    def __set_recv_speed(self, val):
        if self.is_speed != int(val):
            self.is_speed = int(val)
            if self.onNewSpeed is not None:
                self.onNewSpeed(self.is_speed)

        self.send_ack(Message.IS_SPEED.value)

    def __set_recv_cube(self, val):
        if int(val) in range(0, 2):
            if self.cube != int(val):
                self.cube = int(val)
                if self.onNewCubeState is not None:
                    self.onNewCubeState(int(val))

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
