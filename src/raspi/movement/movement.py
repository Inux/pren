# -*- coding: utf-8 -*-
"""Movement Controller
-Talks directly to Raspberry
-Sends heartbeat message
-Receives commands and does acknowledge
"""
import time
from datetime import timedelta
import sys

import src.raspi.config.config as config
from src.raspi.lib import base_app
from src.raspi.lib import zmq_socket
from src.raspi.lib import periodic_job
from src.raspi.lib import heartbeat as hb
from src.raspi.movement import protocol
from src.raspi.movement import mw_adapter_movement

socket = zmq_socket.get_movement_sender()

def send_hb():
    hb.send_heartbeat(socket, hb.COMPONENT_MOVEMENT, hb.STATUS_RUNNING)

class Movement(base_app.App):
    def __init__(self, *args, **kwargs):
        super().__init__("Movement", self.movement_loop, *args, **kwargs)

        self.job = periodic_job.PeriodicJob(interval=timedelta(milliseconds=50), execute=send_hb)
        self.job.start()

        self.tiny = protocol.Protocol(config.MASTER_UART_INTERFACE_TINY, config.MASTER_UART_BAUD, onNewSpeed=self.onNewSpeed, onNewCurrent=self.onNewCurrent)
        self.tiny.connect()

        self.data = {}
        self.data['speed'] = None

    def movement_loop(self, *args, **kwargs):
        self.tiny.rcv_handler()

        data_tmp = mw_adapter_movement.get_data()

        # only send data if the change
        if self.data['speed'] != int(data_tmp['speed']):
            self.data['speed'] = int(data_tmp['speed'])
            self.tiny.send_speed(self.data['speed'])

    def onNewSpeed(self, speed):
        mw_adapter_movement.send_speed(speed)

    def onNewCurrent(self, current):
        mw_adapter_movement.send_current(current)

if __name__ == '__main__':
    Movement().run()
