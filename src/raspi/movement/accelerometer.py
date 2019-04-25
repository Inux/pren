from datetime import timedelta

from src.raspi.movement.gyroADXL345 import ADXL345
import src.raspi.lib.log as log
from src.raspi.lib import periodic_job
import src.raspi.movement.mw_adapter_movement as mwadapter

logger = log.getLogger('SoulTrain.movement.accelerometer')

class AccelerationReader:
    def __init__(self):
        self.gyro = ADXL345()

        self.job = periodic_job.PeriodicJob(interval=timedelta(milliseconds=50), execute=self.read_acceleration)

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

if __name__ == '__main__':
    AccelerationReader()