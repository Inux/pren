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
from src.raspi.controlflow.phases.phase import Phase
from src.raspi.controlflow.phases import a_starting
from src.raspi.controlflow.phases import b_find_cube
from src.raspi.controlflow.phases import c_grab_cube
from src.raspi.controlflow.phases import d_round_one
from src.raspi.controlflow.phases import f_find_stop
from src.raspi.controlflow.phases import g_stopping
from src.raspi.controlflow.phases import h_finished

socket = zmq_socket.get_controlflow_sender()

PHASE_STARTUP = 'startup'
PHASE_FIND_CUBE = 'find_cube'
PHASE_GRAB_CUBE = 'grab_cube'
PHASE_ROUND_ONE = 'round_one'
PHASE_ROUND_TWO = 'round_two'
PHASE_FIND_STOP = 'find_stop'
PHASE_STOPPING = 'stopping'
PHASE_FINISHED = 'finished'

def send_hb():
    hb.send_heartbeat(socket, hb.COMPONENT_CONTROLFLOW, hb.STATUS_RUNNING)

class Controlflow(base_app.App):
    def __init__(self, *args, **kwargs):
        super().__init__("Controlflow", self.controlflow_loop, *args, **kwargs)

        self.job = periodic_job.PeriodicJob(
            interval=timedelta(milliseconds=50), execute=send_hb)
        self.job.start()

        self.startup = Phase(PHASE_STARTUP,
                             a_starting.method,
                             PHASE_FIND_CUBE)
        self.find_cube = Phase(PHASE_FIND_CUBE,
                               a_starting.method,
                               PHASE_GRAB_CUBE)
        self.grab_cube = Phase(PHASE_GRAB_CUBE,
                               a_starting.method,
                               PHASE_ROUND_ONE)
        self.round_one = Phase(PHASE_ROUND_ONE,
                               a_starting.method,
                               PHASE_ROUND_TWO)
        self.round_two = Phase(PHASE_ROUND_TWO,
                               a_starting.method,
                               PHASE_FIND_STOP)
        self.find_stop = Phase(PHASE_FIND_STOP,
                               a_starting.method,
                               PHASE_STOPPING)
        self.stopping = Phase(PHASE_STOPPING,
                              a_starting.method,
                              PHASE_FINISHED)
        self.finished = Phase(PHASE_FINISHED,
                              a_starting.method,
                              "")

        self.actual_phase = None

    def controlflow_loop(self, *args, **kwargs):
        mw_data = mw_adapter_ctrlflow.get_data()

        if 'start' in mw_data['sys_cmd']:
            mw_adapter_ctrlflow.set_data('sys_cmd', '', False)
            self.actual_phase = self.startup

        if 'stop' in mw_data['sys_cmd']:
            mw_adapter_ctrlflow.set_data('sys_cmd', '', False)
            self.actual_phase = None

        if self.actual_phase is not None:
            self.actual_phase = self.actual_phase.run(mw_data)
            if self.actual_phase is not None:
                phase = self.actual_phase.get_name()
                msg = self.actual_phase.get_msg()

                mw_adapter_ctrlflow.send_sys_status(phase, msg)

            else:
                mw_adapter_ctrlflow.send_sys_status(PHASE_FINISHED,
                                                "no further phases to run...")
                self.actual_phase = None
        else:
            mw_adapter_ctrlflow.send_sys_status(PHASE_FINISHED,
                                                "waiting for command...")

if __name__ == '__main__':
    Controlflow().run()
