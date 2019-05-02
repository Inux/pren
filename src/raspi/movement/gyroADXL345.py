# Distributed with a free-will license.
# Use it any way you want, profit or free, provided it fits in the licenses of its associated works.
# ADXL345
# This code is designed to work with the ADXL345_I2CS I2C Mini Module available from ControlEverything.com.
# https://www.controleverything.com/content/Accelorometer?sku=ADXL345_I2CS#tabs-0-product_tabset-2

import smbus2
import time


class ADXL345:

    def __init__(self):
        # Get I2C bus
        self.bus = smbus2.SMBus(1)
        # ADXL345 address, 0x53(83)
        # Select bandwidth rate register, 0x2C(44)
        #		0x0A(10)	Normal mode, Output data rate = 100 Hz
        self.bus.write_byte_data(0x53, 0x2C, 0x0A)
        # ADXL345 address, 0x53(83)
        # Select power control register, 0x2D(45)
        #		0x08(08)	Auto Sleep disable
        self.bus.write_byte_data(0x53, 0x2D, 0x08)
        # ADXL345 address, 0x53(83)
        # Select data format register, 0x31(49)
        #		0x08(08)	Self test disabled, 4-wire interface
        #					Full resolution, Range = +/-2g
        self.bus.write_byte_data(0x53, 0x31, 0x08)
        time.sleep(0.5)

    def read(self):
        # ADXL345 address, 0x53(83)
        # Read data back from 0x32(50), 2 bytes
        # X-Axis LSB, X-Axis MSB
        data0 = self.bus.read_byte_data(0x53, 0x32)
        data1 = self.bus.read_byte_data(0x53, 0x33)

        # Convert the data to 10-bits
        xAccl = ((data1 & 0x03) * 256) + data0
        if xAccl > 511:
            xAccl -= 1024

        # ADXL345 address, 0x53(83)
        # Read data back from 0x34(52), 2 bytes
        # Y-Axis LSB, Y-Axis MSB
        data0 = self.bus.read_byte_data(0x53, 0x34)
        data1 = self.bus.read_byte_data(0x53, 0x35)

        # Convert the data to 10-bits
        yAccl = ((data1 & 0x03) * 256) + data0
        if yAccl > 511:
            yAccl -= 1024

        # ADXL345 address, 0x53(83)
        # Read data back from 0x36(54), 2 bytes
        # Z-Axis LSB, Z-Axis MSB
        data0 = self.bus.read_byte_data(0x53, 0x36)
        data1 = self.bus.read_byte_data(0x53, 0x37)

        # Convert the data to 10-bits
        zAccl = ((data1 & 0x03) * 256) + data0
        if zAccl > 511:
            zAccl -= 1024

        return xAccl, yAccl, zAccl
