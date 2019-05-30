# -*- coding: utf-8 -*-
"""numberDetectionController
-Talks directly to Raspberry
-Sends heartbeat message
-Receives commands and does acknowledge
"""

from datetime import timedelta

from src.raspi.lib import base_app
from src.raspi.config import config as cfg
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

        self.job = periodic_job.PeriodicJob(interval=timedelta(milliseconds=cfg.HB_INTERVAL), execute=send_hb)
        self.job.start()

    def detection_loop(self, *args, **kwargs):
        pass


if __name__ == '__main__':
    Movement().run()
