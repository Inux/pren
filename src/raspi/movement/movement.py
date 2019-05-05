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

        self.tiny = protocol.Protocol(config.MASTER_UART_INTERFACE_TINY, config.MASTER_UART_BAUD, onNewSpeed=self.on_new_speed, onNewCurrent=self.on_new_current,
        real_device=self.is_raspi)
        self.tiny.connect()

        self.data = {}
        self.data['speed'] = 0 #mm/s
        self.data['distance'] = 0.0 #mm
        self.data['crane'] = 0 #mm

        self.run() #run movement loop

    def movement_loop(self, *args, **kwargs):
        self.tiny.rcv_handler()

        data_tmp = mw_adapter_movement.get_data()

        # only send data if the change
        if self.data['speed'] != int(data_tmp['speed']):
            self.data['speed'] = int(data_tmp['speed'])
            self.tiny.send_speed(self.data['speed'])

        if self.data['crane'] != int(data_tmp['crane']):
            self.data['crane'] = int(data_tmp['crane'])
            logger.info("sending crane command ack")
            mw_adapter_movement.send_ack(zmq_ack.ACK_RECV_CRANE_CMD, hb.COMPONENT_MOVEMENT)

    def on_new_speed(self, speed):
        mw_adapter_movement.send_speed(speed)

    def on_new_current(self, current):
        mw_adapter_movement.send_current(current)

    def acceleration_callback(self, time_delta_us, acc_x, acc_y, acc_z):
        # multiplying current speed with time offset to get distance for current section
        section_distance = float(self.data['speed']) * (float(time_delta_us) / 1000000.0)
        # adding distance of measured section to overall distance
        self.data['distance'] = self.data['distance'] + section_distance
        mw_adapter_movement.send_distance(self.data['distance'])

        mw_adapter_movement.send_acceleration(acc_x, acc_y, acc_z)

if __name__ == '__main__':
    Movement().run()
