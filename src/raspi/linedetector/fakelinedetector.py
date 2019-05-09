# -*- coding: utf-8 -*-
"""Fake Line Detector
"""
import time
from datetime import timedelta

import zmq
import zmq.auth

from src.raspi.lib import base_app
from src.raspi.lib import periodic_job
from src.raspi.lib import zmq_socket
from src.raspi.lib import zmq_topics
import src.raspi.lib.heartbeat as hb
from src.raspi.pb import direction_pb2

import src.raspi.linedetector.mw_adapter_linedetector as mwadapter

OFFSET = 0
DIRECTIONS = ['straight', 'left', 'right']

def get_dir():
    global OFFSET
    global DIRECTIONS

    d = DIRECTIONS[OFFSET]
    OFFSET = OFFSET + 1
    if OFFSET >= len(DIRECTIONS):
        OFFSET = 0

    return d

socket = zmq_socket.get_linedetector_sender()

def send_hb():
    hb.send_heartbeat(socket, hb.COMPONENT_LINEDETECTOR, hb.get_status())

class LineDetector(base_app.App):
    def __init__(self, *args, **kwargs):
        super().__init__("LineDetection", self.linedetection_loop, *args, **kwargs)

        self.job = periodic_job.PeriodicJob(interval=timedelta(milliseconds=50), execute=send_hb)
        self.job.start()

        self.run()

    def linedetection_loop(self, *args, **kwargs):
        mwadapter.send_direction(get_dir())
        time.sleep(3)

if __name__ == '__main__':
    LineDetector()
