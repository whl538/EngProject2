import time
import sys

import board
import digitalio

sys.path.append("./devices")

# --- Devices ---
from IMU import IMU

IMU_SCL_PIN = board.GP5
IMU_SDA_PIN = board.GP4
BUTTON_PIN = board.GP14

CALIBRATE = False

OFFSET_X = 13.725
OFFSET_Y = -0.15000536
OFFSET_Z = 0.0000
SCALE_X = 1.0234
SCALE_Y = 0.9776

if __name__ == "__main__":
    imu = IMU(scl_pin=IMU_SCL_PIN, sda_pin=IMU_SDA_PIN,
    offset_x=OFFSET_X, offset_y=OFFSET_Y, offset_z=OFFSET_Z,
    scale_x=SCALE_X, scale_y=SCALE_Y)

    button = digitalio.DigitalInOut(BUTTON_PIN)
    button.switch_to_input(pull=digitalio.Pull.DOWN)

    if CALIBRATE:
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

        time.sleep(0.01)
