from src.raspi.numberdetector.numberDetectionPython.StateMachine import SlaveStateMachine
import time
from datetime import timedelta
from random import randint
from src.raspi.numberdetector.numberDetectionPython.detection import Detection
from src.raspi.numberdetector.numberDetectionPython.camera import Camera


import zmq
import zmq.auth
from src.raspi.config import config as cfg
from src.raspi.lib import periodic_job
from src.raspi.lib import zmq_socket
from src.raspi.lib import zmq_topics
import src.raspi.lib.heartbeat as hb
from src.raspi.pb import direction_pb2


class Ablauf():

    def __init__(self):
        job = periodic_job.PeriodicJob(interval=timedelta(milliseconds=cfg.HB_INTERVAL), execute=send_hb)
        job.start()
        self.number = 0
        self.name = "Ablauf"
        self.cam = Camera()
        self.detection = Detection(self.cam.imageQueueStartSignal, self.cam.imageQueueNumberDetector)
        self.stateMachine = SlaveStateMachine(self.detection, self.camera)
        self.detection.register(self)

        self.stateMachine.run('startbefehl')

    def update(self, message):
        if message.__eq__("r"+1):
            self.stateMachine.run('startsignalErkannt')
        elif message.__eq__("r"+2):
            if self.number > 0:
                self.stateMachine.run('runde1StartSignalErkanntMitNummer')
            else:
                self.stateMachine.run('runde1StartSignalErkanntOhneNummer')
        elif message.__eq__("r"+3):
            if self.stateMachine.current_state.__eq__('runde2Langsam'):
                self.stateMachine.run('stopSignalErkanntOhneNummer')
            else:
                self.stateMachine.run('stopSignalErkanntMitNummer')


if __name__ == '__main__':
    ablauf = Ablauf()
