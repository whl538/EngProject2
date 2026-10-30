import time
import math
import sys

import board
import busio
import digitalio

# --- Adafruit Device Library Imports ---
import adafruit_icm20x
import adafruit_vl53l4cd

sys.path.append("./devices")

# --- Devices ---
from IMU import IMU
from TOF import TOF

TOF_SCL_PIN = board.GP5
TOF_SDA_PIN = board.GP4
BUTTON_PIN = board.GP14

if __name__ == "__main__":
    tof = TOF(scl_pin=TOF_SCL_PIN, sda_pin=TOF_SDA_PIN)

    button = digitalio.DigitalInOut(BUTTON_PIN)
    button.switch_to_input(pull=digitalio.Pull.DOWN)

    while True:
        try:
            if tof.data_ready():
                tof.get_reading()
            if button.value:
                print("Button pressed! Exiting loop...")
                break

        except Exception as e:
            print(f"{e}\nExiting loop...")
            break

        time.sleep(0.1)
