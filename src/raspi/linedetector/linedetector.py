# -*- coding: utf-8 -*-
"""Linedetector
-Checks direction of trails
-Sends direction over middleware (straight, left, right)
"""
import time
from datetime import timedelta

from src.raspi.lib import base_app
from src.raspi.lib import zmq_socket
from src.raspi.lib import periodic_job
from src.raspi.lib import heartbeat as hb

socket = zmq_socket.make_socket()

def send_hb():
    hb.send_heartbeat(socket, hb.COMPONENT_LINEDETECTOR, hb.STATUS_RUNNING)

class Linedetection(base_app.App):
    def __init__(self, *args, **kwargs):
        super().__init__("Linedetection", self.linedetection_loop, *args, **kwargs)

        self.job = periodic_job.PeriodicJob(interval=timedelta(milliseconds=50), execute=send_hb)
        self.job.start()

    def linedetection_loop(self, *args, **kwargs):
        time.sleep(5)

if __name__ == '__main__':
    Linedetection().run()
