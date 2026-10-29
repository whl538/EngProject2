import time
import math

import board
import busio

import digitalio
import pwmio
import rotaryio
from adafruit_motor import motor

class EncoderMotor():
    def __init__(self, pwm_gate,
                 pwm_in1, pwm_in2,
                 enc_pin1=None, enc_pin2=None,
                 pulse_frequency=20000):
        """
        Initialises an EncoderMotor object. 

        Required Parameters:
          `pwm_gate` (pin): PWMA/B pin on the motor driver (acts as a master gate).
          `pwm_in1` (pin): A/BIN1 pin on the motor driver.
          `pwm_in2` (pin): A/BIN2 pin on the motor driver.

        Optional Parameters:
          `enc_pin1` (pin): Pin A for encoder (Default=None).
          `enc_pin2` (pin): Pin B for encoder (Default=None).
          `pulse_frequency` (int): Frequency of the motor pulse, in Hz (Default=20000).
        """

        # Setup motor outputs
        self.pwm_a = pwmio.PWMOut(pwm_in1, frequency=pulse_frequency)
        self.pwm_b = pwmio.PWMOut(pwm_in2, frequency=pulse_frequency)

        self.pwm_gate = digitalio.DigitalInOut(pwm_gate)
        self.pwm_gate.direction = digitalio.Direction.OUTPUT
        self.pwm_gate.value = True

        # Initialise motor object
        self.motor = motor.DCMotor(self.pwm_a, self.pwm_b)

        # Setup encoder (if used)
        if enc_pin1 and enc_pin2:
            self.encoder = rotaryio.IncrementalEncoder(enc_pin1, enc_pin2)
        else:
            self.encoder = None

    def spin(self, speed):
        """
        Spins the motor at the given percent speed. Handles conversion from percent to motor speed.

        Parameters:
          `speed` (int) - Integer between -100 and 100 (inclusive) representing a percent speed and direction (with a negative number representing backward movement)
        """
        if speed >= -100 and speed <= 100:
            self.motor.throttle = speed / 100.0
        elif speed < -100:
            self.motor.throttle = -1.0
        else:
            self.motor.throttle = 1.0

    def stop(self):
        """
        Stops the motor (coasts).
        """
        self.motor.throttle = 0

    def get_speed(self):
        """
        Returns the motor's speed as a percentage.
        """
        return self.motor.throttle * 100

    def tare_encoder(self):
        """
        Sets the motor encoder position to 0.
        """
        if self.encoder:
            self.encoder.position = 0
        else:
            print("This motor does not have a configured encoder.")

    def get_encoder_value(self):
        """
        Returns the motor encoder's position in ticks.
        """
        if self.encoder:
            return self.encoder.position
        else:
            return None

    def __str__(self):
        """
        String representation of an EncoderMotor object.
        Will show motor's current target speed (as a percentage) and current encoder value.
        """
        return f"Target Speed: {self.motor.throttle * 100}. Encoder Value: {self.get_encoder_value()}"
    