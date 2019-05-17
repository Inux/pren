import random
from datetime import timedelta

import src.raspi.lib.log as log
from src.raspi.lib import periodic_job

logger = log.getLogger('SoulTrain.movement.fakeacceleration')

POLL_TIME = timedelta(milliseconds=5000)

class FakeAccelerationmeter:
    def __init__(self, onNewAcceleration):
        self.call_back = onNewAcceleration

        self.job = periodic_job.PeriodicJob(POLL_TIME, execute=self.read_acceleration)

    def start(self):
        self.job.start()

    def stop(self):
        self.job.stop()

    def read_acceleration(self):
        #x_axis, y_axis, z_axis = gyro.read()
        x_axis, y_axis, z_axis = self.mock_gyro()
        logger.debug("Acceleration x: %d, y: %d, z: %d", x_axis, y_axis, z_axis)
        self.call_back(POLL_TIME.total_seconds(), x_axis, y_axis, z_axis)

    def mock_gyro(self):
        fak = random.random()
        return int(fak * 1000), int(fak * 2000), int(fak * 3000)

