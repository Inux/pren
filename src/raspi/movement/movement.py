# -*- coding: utf-8 -*-
"""Movement Controller
-Talks directly to Raspberry
-Sends heartbeat message
-Receives commands and does acknowledge
"""
import time
from datetime import timedelta
import sys
import os

import src.raspi.config.config as config
from src.raspi.lib import base_app
from src.raspi.lib import zmq_socket
from src.raspi.lib import zmq_ack
from src.raspi.lib import periodic_job
from src.raspi.lib import heartbeat as hb
import src.raspi.lib.log as log
from src.raspi.movement import protocol
from src.raspi.movement.accelerometer import AccelerationReader
from src.raspi.movement.fakeaccelerometer import FakeAccelerationmeter
from src.raspi.movement import mw_adapter_movement

logger = log.getLogger("SoulTrain.movement.movement")

socket = zmq_socket.get_movement_sender()

def send_hb():
    hb.send_heartbeat(socket, hb.COMPONENT_MOVEMENT, hb.STATUS_RUNNING)

class Movement(base_app.App):
    def __init__(self, *args, **kwargs):
        super().__init__("Movement", self.movement_loop, *args, **kwargs)

        #We use fake acceleration and fake serial device when we don't run on raspi
        self.is_raspi = os.uname()[4].startswith("arm")

        if self.is_raspi: #check for raspi or not
            self.acc_reader = AccelerationReader(onNewAcceleration=self.acceleration_callback)
        else:
            self.acc_reader = FakeAccelerationmeter(onNewAcceleration=self.acceleration_callback)
        self.acc_reader.start()

        self.job = periodic_job.PeriodicJob(interval=timedelta(milliseconds=50), execute=send_hb)
        self.job.start()

        if self.is_raspi:
            self.tiny = protocol.Protocol(config.MASTER_UART_INTERFACE_TINY, config.MASTER_UART_BAUD, onNewSpeed=self.on_new_speed, onNewCurrent=self.on_new_current,
            onNewCubeState=self.on_new_cube_state,
            resend=config.RESEND_TINY_MESSAGES)
        else:
            self.tiny = protocol.Protocol(config.MASTER_UART_INTERFACE_PC, config.MASTER_UART_BAUD, onNewSpeed=self.on_new_speed, onNewCurrent=self.on_new_current,
            onNewCubeState=self.on_new_cube_state,
            resend=config.RESEND_TINY_MESSAGES)
        self.tiny.connect()

        self.data = {}
        self.data['speed'] = 0 #mm/s
        self.data['speed_tiny'] = 0 #mm/s
        self.data['distance'] = 0.0 #mm
        self.data['crane'] = 0 #mm
        self.data['phase'] = 'startup' #one of the phases of system_status.proto

        self.run() #run movement loop

    def movement_loop(self, *args, **kwargs):
        self.tiny.rcv_handler()
        self.tiny.ack_handler()

        data_tmp = mw_adapter_movement.get_data()

        # only send data if the change
        if self.data['speed'] != int(data_tmp['speed']):
            self.data['speed'] = int(data_tmp['speed'])
            self.tiny.send_speed(self.data['speed'])
            mw_adapter_movement.send_ack(zmq_ack.ACK_RECV_MOVE_CMD, hb.COMPONENT_MOVEMENT)

        if self.data['crane'] != int(data_tmp['crane']):
            self.data['crane'] = int(data_tmp['crane'])
            self.tiny.send_crane(self.data['crane'])
            mw_adapter_movement.send_ack(zmq_ack.ACK_RECV_CRANE_CMD, hb.COMPONENT_MOVEMENT)

        if self.data['phase'] not in data_tmp['phase']:
            self.data['phase'] = data_tmp['phase']

        self.tiny.send_phase(self.data['phase'])

    def on_new_speed(self, speed):
        self.data['speed_tiny'] = speed
        mw_adapter_movement.send_speed(speed)

    def on_new_current(self, current):
        mw_adapter_movement.send_current(current)

    def on_new_cube_state(self, state):
        mw_adapter_movement.send_cube_state(state)

    def acceleration_callback(self, time_delta_s, acc_x, acc_y, acc_z):
        # multiplying current speed_tiny with time offset to get distance for current section
        section_distance = float(self.data['speed_tiny']) * float(time_delta_s)
        logger.info("time_delta_us: " + str(time_delta_s))
        # adding distance of measured section to overall distance
        self.data['distance'] = self.data['distance'] + section_distance
        mw_adapter_movement.send_distance(self.data['distance'])

        logger.info("new distance: " + str(self.data['distance']) + ", speed: " + str(self.data['speed']))

        mw_adapter_movement.send_acceleration(acc_x, acc_y, acc_z)

if __name__ == '__main__':
    Movement().run()
