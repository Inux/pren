# -*- coding: utf-8 -*-
"""numberDetectionController
-Talks directly to Raspberry
-Sends heartbeat message
-Receives commands and does acknowledge
"""
import time
from datetime import timedelta
import sys

from src.raspi.lib import base_app
from src.raspi.lib import zmq_socket
from src.raspi.lib import periodic_job
from src.raspi.lib import heartbeat as hb
from src.raspi.numberdetector.numberDetectionPython import numberReco


socket = zmq_socket.get_numberdetector_sender()

def send_hb():
    hb.send_heartbeat(socket, hb.COMPONENT_NUMBERDETECTION, hb.STATUS_RUNNING)

class Movement(base_app.App):
    def __init__(self, *args, **kwargs):
        super().__init__("NumberDetection", self.detection_loop, *args, **kwargs)

        self.job = periodic_job.PeriodicJob(interval=timedelta(milliseconds=50), execute=send_hb)
        self.job.start()


        self.data = {}
        self.data['speed'] = None

    def detection_loop(self, *args, **kwargs):
        

if __name__ == '__main__':
    Movement().run()
