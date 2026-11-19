import sys

sys.path.append('../lib')

from machine import I2C
from vl53l4cd import VL53L4CD

class TOF():
    def __init__(self, scl_pin=None, sda_pin=None,
                 timing=50, inter=0):
        """
        Initialises the TOF with the given scl and sda pins.

        Optional parameters for timing budget (must be between 10ms and 200ms -
        lower is faster but more noisy) (defaults to 50ms), and inter-measurement period,
        which must be greater than or equal to the timing budget (defaults to 0, which indicates
        continuous mode).

        Raises a ValueError if these parameters are given but are not within range.
        """
        self.i2c = I2C(0, scl=scl_pin, sda=sda_pin)
        self.tof = VL53L4CD(i2c)
        
        if (timing < 10) or (timing > 200):
            raise ValueError(f"Timing is set to {timing}. Please ensure it is between 10ms and 200ms!")
        else:
            self.tof.timing_budget = timing
        
        if inter < timing and inter != 0:
            raise ValueError("Inter must either be 0 or greater than/equal to timing!")
        else:
            self.tof.inter_measurement = inter
        
        self.tof.start_ranging()
    
    def get_reading(self):
        """
        Gets TOF sensor reading in mm
        """
        distance = self.tof.get_distance()
        distance *= 10
        
        return distance
    