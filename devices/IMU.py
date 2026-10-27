import time
import math

import board
import busio
import adafruit_icm20x

# --- CONFIGURATION ---
FILTER_WINDOW = 20  # Number of readings for measurements to smooth out noise (higher = smoother, more lag)

class IMU():
    def __init__(self, scl_pin=None, sda_pin=None,
                 offset_x=0.00, offset_y=0.00, offset_z=0.00,
                 scale_x=1.0000, scale_y=1.0000,
                 deadzone=2.0):
        """
        Initialises the IMU with the given scl and sda pins.

        Optional parameters for manually calibrated Hard Iron Offsets and Soft Iron Scaling.
        These default to 0.00 for offsets, and 1.0000 for scalings.

        Optional parameters for deadzone (defaults to 2.0)
        """
        # Initialise the IMU
        self.i2c = busio.I2C(scl=scl_pin, sda=sda_pin)
        self.icm = adafruit_icm20x.ICM20948(self.i2c)

        # --- Mesaured Parameters ---
        self.heading_buffer = []
        self.heading_offset = 0.0  # Taring offset
        self.previous_heading = 0.0

        # --- Hard Iron Offsets ---
        self.offset_x = offset_x
        self.offset_y = offset_y
        self.offset_z = offset_z

        # --- Soft Iron Scaling ---
        self.scale_x = scale_x
        self.scale_y = scale_y

        self.deadzone = deadzone

    def read_raw_sensor_data(self):
        """
        Reads and returns the raw sensor data from the Accelerometer and the Magnetometer.
        Returns ax, ay, az, mx, my, mz
        """
        ax, ay, az = self.icm.acceleration
        mx, my, mz = self.icm.magnetic

        my = -my
        mz = -mz

        mx -= self.offset_x
        my -= self.offset_y
        mz -= self.offset_z

        mx *= self.scale_x
        my *= self.scale_y

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
                   mz * math.sin(roll) * math.cos(pitch))

        # Calculate heading in degrees
        raw_heading = math.degrees(math.atan2(my_comp, mx_comp))

        if raw_heading < 0:
            raw_heading += 360.0

        return raw_heading

    def get_smoothed_heading(self, new_raw_heading):
        """
        Applies a rolling vector average to eliminate noise and handle 359°/0° wrapping.
        """
        # Convert incoming angle to radians
        rad = math.radians(new_raw_heading)
        self.heading_buffer.append(rad)

        if len(self.heading_buffer) > FILTER_WINDOW:
            self.heading_buffer.pop(0)

        # Sum up the vector components of all saved samples
        sum_sin = sum(math.sin(r) for r in self.heading_buffer)
        sum_cos = sum(math.cos(r) for r in self.heading_buffer)

        # Convert the averaged vector components back into degrees
        smoothed_angle = math.degrees(math.atan2(sum_sin, sum_cos))

        if smoothed_angle < 0:
            smoothed_angle += 360.0

        return smoothed_angle

    def initialise_and_tare(self):
        """
        Stabilises the sensor reading at startup and saves the current angle as 0°.
        """
        print("Initialising sensor... Keep it completely still.")

        # Gather initial samples to populate the buffer and find a stable baseline
        total_samples = 20
        for _ in range(total_samples):
            raw = self.calculate_tilt_compensated_heading()
            stable_raw = self.get_smoothed_heading(raw)
            time.sleep(0.1)

        self.heading_offset = stable_raw
        print(f"Sensor Tared! Baseline offset stored: {self.heading_offset:.2f}°\n")

    def calibrate(self, stop_button):
        """
        Calibrate the Hard Iron Offsets and Soft Iron Scaling.
        Parameter for a button object used to stop the calibration
        """
        # Initialise variables ready for calibration
        x_max = -999999
        x_min = 999999
        y_max = -999999
        y_min = 999999

        print("Beginning calibration. Slowly turn robot in 360 degree circle then press button...")

        while True:
            if stop_button.value:
                print(f"X_MAX = {x_max:.2f}\nX_MIN = {x_min:.2f}\nY_MAX = {y_max:.2f}\nY_MIN = {y_min:.2f}\n")
                print("")
                offset_x = (x_max + x_min) / 2
                offset_y = (y_max + y_min) / 2
                dX = x_max - x_min
                dY = y_max - y_min
                print(f"dX = {dX:.4f}\ndY = {dY:.4f}")
                print("")
                avg = (dX + dY) / 2
                print(f"AVG = {avg:.4f}")
                print("")
                print("--- Constant Values ---")
                print(f"OFFSET_X: {offset_x}\nOFFSET_Y: {offset_y}")
                print(f"SCALE_X: {avg/dX:.4f}\nSCALE_Y: {avg/dY:.4f}")
                print("------------")

                self.offset_x = offset_x
                self.offset_y = offset_y
                self.scale_x = avg/dX
                self.scale_y = avg/dY
                break

            try:
                ax, ay, az, mx, my, mz = self.read_raw_sensor_data()
                x_max = max(x_max, mx)
                x_min = min(x_min, mx)
                y_max = max(y_max, my)
                y_min = min(y_min, my)
                time.sleep(0.05)
            except Exception as e:
                print(e)

    def get_tared_heading(self):
        """
        Returns a Tared and Adjusted heading with all offsets applied.
        """
        # Get raw heading
        raw_heading = self.calculate_tilt_compensated_heading()

        # Smooth out readings
        smooth_raw = self.get_smoothed_heading(raw_heading)

        tared_heading = smooth_raw - self.heading_offset
        tared_heading %= 360.0

        # Apply deadzone
        diff = abs(tared_heading - self.previous_heading)
        if diff > 180:
            diff = 360 - diff

        if diff >= self.deadzone:
            self.previous_heading = tared_heading
            print(f"Stable Tared Heading: {tared_heading}°")

        return self.previous_heading  # Return previous_heading, since it will be updated if appropriate.


if __name__ == "__main__":
    # Test variables
    test_offset_x = 0.00
    test_offset_y = 0.00
    test_offset_z = 0.00

    test_scale_x = 1.0000
    test_scale_y = 1.0000

    imu = IMU(scl_pin=board.GP5, sda_pin=board.GP4,
              offset_x=test_offset_x, offset_y=test_offset_y, offset_z=test_offset_z,
              scale_x=test_scale_x, scale_y=test_scale_y)
    previous_heading = 0.0

    IMU.initialise_and_tare()

    try:
        while True:
            IMU.get_tared_heading()
    except KeyboardInterrupt:
        print("\nExiting heading loop.")
