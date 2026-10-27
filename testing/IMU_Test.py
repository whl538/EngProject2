import time
import math
import sys

import board
import busio
import digitalio
import adafruit_icm20x

sys.path.append("./devices")

# --- Devices ---
from IMU import IMU

IMU_SCL_PIN = board.GP5
IMU_SDA_PIN = board.GP4
BUTTON_PIN = board.GP14

if __name__ == "__main__":
    imu = IMU(scl_pin=IMU_SCL_PIN, sda_pin=IMU_SDA_PIN)

    button = digitalio.DigitalInOut(BUTTON_PIN)
    button.switch_to_input(pull=digitalio.Pull.DOWN)

    imu.calibrate(button)

    imu.initialise_and_tare()
    while True:
        try:
            imu.get_tared_heading()
            if button.value:
                print("Button pressed! Exiting loop...")
                break

        except Exception as e:
            print(f"{e}\nExiting loop...")
            break

        time.sleep(0.1)
