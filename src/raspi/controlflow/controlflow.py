# -*- coding: utf-8 -*-
"""Linedetector
-Checks direction of trails
-Sends direction over middleware (straight, left, right)
"""
import time
from datetime import timedelta
import sys
sys.path.append('..')

from lib import base_app
from lib import zmq_socket
from lib import periodic_job
from lib import heartbeat as hb

socket = zmq_socket.make_socket()

def send_hb():
    hb.send_heartbeat(socket, hb.COMPONENT_CONTROLFLOW, hb.STATUS_RUNNING)

class Controlflow(base_app.App):
    def __init__(self, *args, **kwargs):
        super().__init__("Controlflow", self.controlflow_loop, *args, **kwargs)

        self.job = periodic_job.PeriodicJob(interval=timedelta(milliseconds=50), execute=send_hb)
        self.job.start()

    def controlflow_loop(self, *args, **kwargs):
        time.sleep(5)

if __name__ == '__main__':
    Controlflow().run()
