import random
from datetime import timedelta

import src.raspi.lib.log as log
import zmq_socket
from src.raspi.lib import periodic_job
from src.raspi.lib import heartbeat as hb
import passiv_buzzer
import src.raspi.acoustic.mw_adapter_acoustic as mw_adapter

logger = log.getLogger('SoulTrain.acoustic.sound')

socket = zmq_socket.get_acoustic_sender()

def send_hb():
    hb.send_heartbeat(socket, hb.COMPONENT_MOVEMENT, hb.STATUS_RUNNING)

def buzz(number):
    for x in range(0, number):
        passiv_buzzer.beep(number)

class Buzzer:
    def __init__(self):
        super().__init__("Acoustic", self.acoustic_loop, *args, **kwargs)

        self.job = periodic_job.PeriodicJob(interval=timedelta(milliseconds=50), execute=send_hb)
        self.job.start()

    def acoustic_loop(self, *args, **kwargs):

        data_tmp = mw_adapter.get_data()

        # only send data if the change
        if self.data['number'] != int(data_tmp['number']):
            self.data['number'] = int(data_tmp['number'])
            self.buzz()

    def buzz(self, number):
        for x in range(0, number):
            passiv_buzzer.beep(number)

if __name__ == '__main__':
    buzz(4)
    Buzzer()