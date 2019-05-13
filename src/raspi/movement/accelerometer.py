from datetime import timedelta

from src.raspi.movement.gyroADXL345 import ADXL345
import src.raspi.lib.log as log
from src.raspi.lib import periodic_job
import src.raspi.movement.mw_adapter_movement as mwadapter

logger = log.getLogger('SoulTrain.movement.accelerometer')

POLL_TIME = timedelta(milliseconds=50)

class AccelerationReader:
    def __init__(self, onNewAcceleration):
        self.gyro = ADXL345()
        self.call_back = onNewAcceleration

        self.job = periodic_job.PeriodicJob(POLL_TIME, execute=self.read_acceleration)

    def start(self):
        self.job.start()

    def stop(self):
        self.job.stop()

    def read_acceleration(self):
        """
        :param gyro:
        :return:
        """
        x_axis, y_axis, z_axis = self.gyro.read()
        self.call_back(POLL_TIME.total_seconds(), x_axis, y_axis, z_axis)
