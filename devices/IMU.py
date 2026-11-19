import sys
import time
import math

sys.path.append('../lib')

from machine import I2C
from icm20948 import ICM20948

class IMU():
    def __init__(self, scl_pin=None, sda_pin=None,
                 deadzone=2.0):
        """
        Initialises the IMU with the given scl and sda pins.
        
        Optional parameter for deadzone (defaults to 2.0 deg).
        """
        # Initialise the IMU
        self.i2c = I2C(0, scl=scl_pin, sda=sda_pin)
        self.icm = ICM20948(self.i2c)
        
        self.deadzone = deadzone
        
        # --- Measured Parameters ---
        self.previous_heading = 0.0
        
    def calibrate(self):
        """
        Calibrates the Gyroscope, Accelerometer, and Magnetometer.
        """
        self.icm.gyro_cal()
        self.icm.acc_cal()
        self.icm.mag_cal()
    
    def read_raw_sensor_data(self):
        """
        Reads and returns the raw sensor data from the Accelerometer and Magnetometer.
        
        Returns ax, ay, az, mx, my, mz.
        """
        ax, ay, az = self.icm.acc
        mx, my, mz = self.icm.mag
        
        my = -my
        mz = -mz
        
        return ax, ay, az, mx, my, mz
    
    def calculate_tilt_compensated_heading(self):
        """
        Reads the sensor and calculates a raw tilt-compensated heading (0 to 360).
        """
        ax, ay, az, mx, my, mz = self.read_raw_sensor_data()
        
        # Calculate Roll and Pitch from Accelerometer
        roll = math.atan2(ay, az)
        pitch = math.atan2(-ax, math.sqrt(ay * ay + az * az))
        
        # Tilt-compensate Magnetometer readings
        mx_comp = mx * math.cos(pitch) + mz * math.sin(pitch)
        my_comp = (mx * math.sin(roll) * math.sin(pitch) +
                   my * math.cos(roll) -
                   mz * math.sim(roll) * math.cos(pitch))
        
        # Calculate heading in degrees
        raw_heading = math.degrees(math.atan2(my_comp, mx_comp))
        
        if raw_heading < 0:
            raw_heading += 360.0
            
        return raw_heading
    
    def initialise_and_tare(self):
        """
        Stabilises the sensor reading at startup and saves the current angle as 0°.
        """
        print("Initialising sensor... Keep it completely still.")
        
        # Find a stable baseline
        total_samples = 20
        for _ in range(total_samples):
            heading = self.calculate_tilt_compensated_heading()
        
        self.heading_offset = heading
        print(f"Sensor Tared! Baseline offset stored: {self.heading_offset:.2f}°\n")
        
    def get_tared_heading(self):
        """
        Returns a tared and adjusted heading with all offsets applied.
        """
        raw_heading = self.calculate_tilt_compensated_heading()
        
        relative_heading = raw_heading - self.heading_offset
        
        relative_heading %= 360.0
        
        # Apply deadzone
        diff = abs(relative_heading - self.previous_heading)
        if diff > 180:
            diff = 360 - diff
        
        if diff >= self.deadzone:
            self.previous_heading = relative_heading
            print(f"Stable Tared Heading: {relative_heading}°")
        
        return self.previous_heading  # Return previous_heading, since it will be updated if appropriate.