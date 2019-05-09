# -*- coding: utf-8 -*-
"""Fake Number Detection
"""
import time
from datetime import timedelta
from random import randint

import zmq
import zmq.auth

from src.raspi.lib import base_app
from src.raspi.lib import periodic_job
from src.raspi.lib import zmq_socket
from src.raspi.lib import zmq_topics
import src.raspi.lib.heartbeat as hb
from src.raspi.pb import direction_pb2

import src.raspi.numberdetector.numberDetectionPython.mw_adapter_numberdetection as mwadapter

OFFSET = 0

def get_number():
    return randint(1,9)


socket = zmq_socket.get_numberdetector_sender()

def send_hb():
    hb.send_heartbeat(socket, hb.COMPONENT_NUMBERDETECTOR, hb.get_status())

class NumberDetector(base_app.App):
    def __init__(self, *args, **kwargs):
        super().__init__("numberdetector", self.numberdetectorloop, *args, **kwargs)
        self.job = periodic_job.PeriodicJob(interval=timedelta(milliseconds=50), execute=send_hb)
        self.job.start()

    def numberdetectorloop(self, *args, **kwargs):
        mwadapter.send_number(get_number())
        time.sleep(3)

if __name__ == '__main__':
    NumberDetector().run()