import time

import board
import busio
import adafruit_vl53l4cd

class TOF():
    def __init__(self, scl_pin=None, sda_pin=None, timing=50, inter=60):
        """
        Initialises the TOF with the given scl and sda pins.

        Optional parameters for timing budget (must be between 10ms and 200ms -
        lower is faster but more noisy) (defaults to 50ms), and inter-measurement period,
        which must be greater than or equal to the timing budget (defaults to
        60ms).

        Raises a ValueError if these parameters are given but are not within range.
        """
        self.i2c = busio.I2C(scl=scl_pin, sda=sda_pin)
        self.tof = adafruit_vl53l4cd.VL53L4CD(self.i2c)

        if (timing < 10) or (timing > 200):
            raise ValueError(f"Timing is set to {timing}. Please ensure it is between 10ms and 200ms!")
        else:
            self.tof.timing_budget = 50

        if inter < timing:
            raise ValueError(f"Inter is set to {inter}, while timing is {timing}. Inter must be greater than or equal to timing")
        else:
            self.tof.inter_measurement = 60

    def data_ready(self):
        """
        Returns True if the sensor has a new distance reading ready.
        """
        return self.tof.data_ready

    def get_reading(self):
        """
        Gets sensor reading in mm.
        """
        distance = self.tof.distance
        self.tof.clear_interrupt()
        distance *= 10  # Convert to mm

        print(f"Distance: {distance}mm")
        return distance
