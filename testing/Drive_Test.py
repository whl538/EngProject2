import time
import sys

import board
import digitalio

sys.path.append("./devices")

# --- Devices ---
from MotorDriver import MotorDriver
from EncoderMotor import EncoderMotor
from Drive import Drive

# --- Driver Pins ---
DRIVER_SBY_PIN = board.GP3
DRIVER_PWM_PINA = board.GP2
DRIVER_PWM_PINB = board.GP6

# --- Motor Pins ---
MOTOR_A_PIN1 = board.GP1
MOTOR_A_PIN2 = board.GP0
MOTOR_B_PIN1 = board.GP5
MOTOR_B_PIN2 = board.GP4

# --- Encoder Pins ---
ENCODER_A_PIN1 = board.GP15
ENCODER_A_PIN2 = board.GP14
ENCODER_B_PIN1 = board.GP13
ENCODER_B_PIN2 = board.GP12

if __name__ == "__main__":
    # Initialise Motor Driver
    driver = MotorDriver(DRIVER_SBY_PIN)

    # Initialise Encoder Motors
    drive_motor_l = EncoderMotor(DRIVER_PWM_PINA,
                                 MOTOR_A_PIN1, MOTOR_A_PIN2,
                                 enc_pin1=ENCODER_A_PIN1, enc_pin2=ENCODER_A_PIN2)

    drive_motor_r = EncoderMotor(DRIVER_PWM_PINB,
                                 MOTOR_B_PIN1, MOTOR_B_PIN2,
                                 enc_pin1=ENCODER_B_PIN1, enc_pin2=ENCODER_B_PIN2)

    # Initialise Drive
    drive = Drive(37.5,
                  drive_motor_l, drive_motor_r)

    print("Taring Encoders...")
    try:
        drive.reset_encoders()
    except:
        print("Unable to tare encoders. Values may be inaccurate")

    while True:
        try:
            print(str(drive))
        except Exception as e:
            print(f"{e}\nExiting loop...")
            break

        time.sleep(0.1)
