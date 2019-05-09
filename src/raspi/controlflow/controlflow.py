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
from src.raspi.controlflow import mw_adapter_ctrlflow

socket = zmq_socket.get_controlflow_sender()

PHASE_STARTUP = 'startup'
MSG_STARTUP_WAITING = 'waiting for all components...'

PHASE_FIND_CUBE = 'find_cube'
PHASE_GRAB_CUBE = 'grab_cube'
PHASE_ROUND_ONE = 'round_one'
PHASE_ROUND_TWO = 'round_two'
PHASE_FIND_STOP = 'find_stop'
PHASE_STOPPING = 'stopping'
PHASE_FINISHED = 'finished'

current_phase = PHASE_STARTUP
current_msg = MSG_STARTUP_WAITING

def send_hb():
    hb.send_heartbeat(socket, hb.COMPONENT_CONTROLFLOW, hb.STATUS_RUNNING)

class Controlflow(base_app.App):
    def __init__(self, *args, **kwargs):
        super().__init__("Controlflow", self.controlflow_loop, *args, **kwargs)

        self.job = periodic_job.PeriodicJob(interval=timedelta(milliseconds=50), execute=send_hb)
        self.job.start()

    def controlflow_loop(self, *args, **kwargs):
        mw_adapter_ctrlflow.send_sys_status(current_phase, current_msg)

if __name__ == '__main__':
    Controlflow().run()
