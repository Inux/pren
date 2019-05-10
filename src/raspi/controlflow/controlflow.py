# -*- coding: utf-8 -*-
"""Linedetector
-Checks direction of trails
-Sends direction over middleware (straight, left, right)
"""
import time
from datetime import timedelta

from src.raspi.lib import base_app
from src.raspi.lib import zmq_socket
from src.raspi.lib import zmq_ack
from src.raspi.lib import periodic_job
from src.raspi.lib import heartbeat as hb
from src.raspi.config import config
from src.raspi.controlflow import mw_adapter_ctrlflow
from src.raspi.controlflow.phases.phase import Phase
from src.raspi.controlflow.phases import a_starting
from src.raspi.controlflow.phases import b_find_cube
from src.raspi.controlflow.phases import c_grab_cube
from src.raspi.controlflow.phases import d_round_one
from src.raspi.controlflow.phases import e_round_two
from src.raspi.controlflow.phases import f_find_stop
from src.raspi.controlflow.phases import g_stopping
from src.raspi.controlflow.phases import h_finished

socket = zmq_socket.get_controlflow_sender()

def send_hb():
    hb.send_heartbeat(socket, hb.COMPONENT_CONTROLFLOW, hb.STATUS_RUNNING)

class Controlflow(base_app.App):
    def __init__(self, *args, **kwargs):
        super().__init__("Controlflow", self.controlflow_loop, *args, **kwargs)

        self.job = periodic_job.PeriodicJob(
            interval=timedelta(milliseconds=50), execute=send_hb)
        self.job.start()

        self.startup = Phase(config.PHASE_STARTUP,
                             a_starting.method,
                             config.PHASE_FIND_CUBE)
        self.find_cube = Phase(config.PHASE_FIND_CUBE,
                               b_find_cube.method,
                               config.PHASE_GRAB_CUBE)
        self.grab_cube = Phase(config.PHASE_GRAB_CUBE,
                               c_grab_cube.method,
                               config.PHASE_ROUND_ONE)
        self.round_one = Phase(config.PHASE_ROUND_ONE,
                               d_round_one.method,
                               config.PHASE_ROUND_TWO)
        self.round_two = Phase(config.PHASE_ROUND_TWO,
                               e_round_two.method,
                               config.PHASE_FIND_STOP)
        self.find_stop = Phase(config.PHASE_FIND_STOP,
                               f_find_stop.method,
                               config.PHASE_STOPPING)
        self.stopping = Phase(config.PHASE_STOPPING,
                              g_stopping.method,
                              config.PHASE_FINISHED)
        self.finished = Phase(config.PHASE_FINISHED,
                              h_finished.method,
                              "")

        self.actual_phase = None
        self.oldphase = ''
        self.oldmsg = ''

    def controlflow_loop(self, *args, **kwargs):
        global mw_data

        mw_data = mw_adapter_ctrlflow.get_data()


        # Handle commands from webapp

        if 'start' in mw_data['sys_cmd']:
            mw_adapter_ctrlflow.set_data('sys_cmd', '', False)
            self.actual_phase = self.startup

        if 'stop' in mw_data['sys_cmd']:
            mw_adapter_ctrlflow.set_data('sys_cmd', '', False)
            self.actual_phase = self.finished


        # Run phases (Statemachine)

        if self.actual_phase is not None:
            phase = self.actual_phase.get_name()
            msg = self.actual_phase.get_msg()

            #send only a status if we really change the value
            if str(phase) not in str(self.oldphase) and str(msg) not in str(self.oldmsg):
                mw_adapter_ctrlflow.send_sys_status(str(phase), str(msg))

            #run phase
            self.actual_phase = self.actual_phase.run(mw_data)

            #send sys status again after running
            if self.actual_phase is not None:
                phase = self.actual_phase.get_name()
                msg = self.actual_phase.get_msg()

                #send only a status if we really change the value
                if str(phase) not in str(self.oldphase) and str(msg) not in str(self.oldmsg):
                    mw_adapter_ctrlflow.send_sys_status(str(phase), str(msg))

        else:
            mw_adapter_ctrlflow.send_sys_status(config.PHASE_FINISHED,
                                                "waiting for command...")

if __name__ == '__main__':
    Controlflow().run()
