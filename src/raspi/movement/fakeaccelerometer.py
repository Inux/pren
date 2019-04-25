import random
from datetime import timedelta

import src.raspi.lib.log as log
from src.raspi.lib import periodic_job
import src.raspi.movement.mw_adapter_movement as mwadapter

logger = log.getLogger('SoulTrain.movement.accelerometer')

class AccelerationReader:
    def __init__(self):
        self.job = periodic_job.PeriodicJob(interval=timedelta(milliseconds=50), execute=self.read_acceleration)
        self.job.start()

    def start(self):
        self.job.start()

    def stop(self):
        self.job.stop()

    def read_acceleration(self):
        #x_axis, y_axis, z_axis = gyro.read()
        x_axis, y_axis, z_axis = self.mock_gyro()
        self.send_acceleration(x_axis, y_axis, z_axis)

    def send_acceleration(self, x_axis, y_axis, z_axis):
        """
        :param x_axis:
        :param y_axis:
        :param z_axis:
        :return:
        """

        print("Acceleration in X-Axis : %d" % x_axis)
        print("Acceleration in Y-Axis : %d" % y_axis)
        print("Acceleration in Z-Axis : %d" % z_axis)
        mwadapter.send_acceleration(x_axis, y_axis, z_axis)

    def mock_gyro(self):
        fak = random.random()
        return int(fak * 1000), int(fak * 2000), int(fak * 3000)

if __name__ == '__main__':
    AccelerationReader()