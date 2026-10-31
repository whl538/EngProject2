import math

from IMU import IMU
from TOF import TOF
from EncoderMotor import EncoderMotor

class Drive():
    def __init__(self, wheel_radius,
                 left_motor: EncoderMotor, right_motor: EncoderMotor,
                 imu: IMU | None = None,
                 tof_left: TOF | None = None, tof_centre: TOF | None = None, tof_right: TOF | None = None):
        """
        Initialises a Drive object.

        Required Parameters:
          `wheel_radius` (float): The radius of the wheels in mm.
          `left_motor` (EncoderMotor): The EncoderMotor located on the drive's left side.
          `right_motor` (EncoderMotor): The EncoderMotor located on the drive's right side.

        Optional Parameters:
          `imu` (IMU): The IMU object (Default=None).
          `tof_left` (TOF): The Time-Of-Flight sensor on the left of the drive (Default=None).
          `tof_centre` (TOF): The Time-Of-Flight sensor on the center of the drive (Default=None).
          `tof_right` (TOF): The Time-Of-Flight sensor on the right of the drive (Default=None).
        """
        self.wheel_radius = wheel_radius  # Radius of the drive's wheels in mm.

        # Initialise motors
        self.left_motor = left_motor
        self.right_motor = right_motor

        self.reference_motor = left_motor  # Motor encoder to reference for PID Control

        # Initialise sensors
        self.imu = imu
        self.tof_left = tof_left
        self.tof_centre = tof_centre
        self.tof_right = tof_right

        # Stored PID values (default to 0 until set up manually)
        self.kp_straight = 0.0
        self.ki_straight = 0.0
        self.kd_straight = 0.0

        self.kp_turn = 0.0
        self.ki_turn = 0.0
        self.kd_turn = 0.0

    def init_pid_straight(self, kp, ki, kd):
        """
        Initialises the PID constants for straight (forwards and backwards) movement
        """
        self.kp_straight = kp
        self.ki_straight = ki
        self.kd_straight = kd

    def init_pid_turn(self, kp, ki, kd):
        """
        Initialises the PID constants for turning
        """
        self.kp_turn = kp
        self.ki_turn = ki
        self.kd_turn = kd

    # --- Utility Functions ---
    def counts_to_mm(self, counts):
        """
        Converts Encoder counts to mm
        """
        total_rotations = counts / self.reference_motor.get_counts_per_rotation()
        mm_per_rotation = self.wheel_radius * 2 * math.pi

        return total_rotations * mm_per_rotation

    def mm_to_counts(self, mm):
        """
        Converts mm to Encoder counts
        """
        mm_per_rotation = self.wheel_radius * 2 * math.pi
        total_rotations = mm / mm_per_rotation

        return total_rotations * self.reference_motor.get_counts_per_rotation()

    # -- Sensor Data ---
    def reset_encoders(self):
        """
        Resets both encoders back to 0.
        """
        self.left_motor.tare_encoder()
        self.right_motor.tare_encoder()

    # --- Basic Drive Functions (No Sensors) ---
    def drive(self, l_speed, r_speed):
        """
        Drives the robot. Can be used for regular driving or non on-the-spot turns.
        Parameters:
          `l_speed` (int): The percentage speed of the left motor (-100 to 100 inclusive)
          `r_speed` (int): The percentage speed of the right motor (-100 to 100 inclusive)
        """
        self.left_motor.spin(l_speed)
        self.right_motor.spin(r_speed)

    def forward(self, speed):
        """
        Drives forward at the given percentage speed.
        """
        self.drive(speed, speed)

    def backward(self, speed):
        """
        Drives backward at the given percentage speed. Takes a POSITIVE argument.
        """
        self.drive(-speed, -speed)

    def spot_turn_left(self, speed):
        """
        Turns left on-the-spot (one motor forward and the other backward at the same speed) at the given percentage speed.
        Takes a POSITIVE argument.
        """
        self.drive(-speed, speed)

    def spot_turn_right(self, speed):
        """
        Turns right on-the-spot (one motor forward and the other backward at the same speed) at the given percentage speed.
        Takes a POSITIVE argument.
        """
        self.drive(speed, -speed)

    def stop(self):
        """
        Stops both drive motors.
        """
        self.left_motor.stop()
        self.right_motor.stop()

    # --- Advanced Drive Functions (PID) ---
    def pid_drive_forward(self, target, break_threshold):
        """
        Drives forward to a target using PID control. Takes the target in mm.
        Also takes a break threshold (in encoder counts) to prevent infinite loops due to calibration errors.
        """
        target = self.mm_to_counts(target)
        integral = 0
        prev_error = target
        encoder_value = self.reference_motor.get_encoder_value()

        while (encoder_value < target - break_threshold) or (encoder_value > target + break_threshold) or (self.reference_motor.get_speed() != 0.0):
            error = target - encoder_value
            derivative = error - prev_error
            prev_error = error
            if abs(error > self.reference_motor.get_counts_per_rotation() / 12) or error == 0:
                integral = 0
            else:
                integral += error

            self.forward(error * self.kp_straight + integral * self.ki_straight + derivative * self.kd_straight)
            encoder_value = self.reference_motor.get_encoder_value()

    def pid_drive_backward(self, target, break_threshold):
        """
        Drives backward to a target using PID control. Takes the target in mm.
        Also takes a break threshold (in encoder counts) to prevent infinite loops due to calibration errors.
        """
        target = self.mm_to_counts(target)
        integral = 0
        prev_error = target
        encoder_value = self.reference_motor.get_encoder_value()

        target *= -1

        while (encoder_value < target + break_threshold) or (encoder_value > target - break_threshold) or (self.reference_motor.get_speed() != 0.0):
            error = abs(target - encoder_value)
            derivative = error - prev_error
            prev_error = error
            if abs(error > self.reference_motor.get_counts_per_rotation() / 12) or error == 0:
                integral = 0
            else:
                integral += error

            self.backward(error * self.kp_straight + integral * self.ki_straight + derivative * self.kd_straight)
            encoder_value = self.reference_motor.get_encoder_value()

    def pid_turn_left(self, target, break_threshold):
        """
        Turns left to a target angle using PID control. Takes the target in deg.
        Also takes a break threshold (in encoder counts) to prevent infinite loops due to calibration errors.
        """
        integral = 0
        prev_error = target
        imu_value = self.imu.get_tared_heading()

        target = 360 - target  # Account for wraparound in imu measurement

        while (imu_value > target + break_threshold) or (imu_value < target - break_threshold) or (self.reference_motor.get_speed() != 0.0):
            error = target - imu_value
            derivative = error - prev_error
            prev_error = error
            if abs(error < 7) or error == 0:
                integral = 0
            else:
                integral += error

            self.spot_turn_left(error * self.kp_turn + integral * self.ki_turn + derivative * self.kd_turn)
            imu_value = self.imu.get_tared_heading()

    def pid_turn_right(self, target, break_threshold):
        """
        Turns right to a target angle using PID control. Takes the target in deg.
        Also takes a break threshold (in encoder counts) to prevent infinite loops due to calibration errors.
        """
        integral = 0
        prev_error = target
        imu_value = self.imu.get_tared_heading()

        while (imu_value > target + break_threshold) or (imu_value < target - break_threshold) or (self.reference_motor.get_speed() != 0.0):
            error = target - imu_value
            derivative = error - prev_error
            prev_error = error
            if abs(error < 7) or error == 0:
                integral = 0
            else:
                integral += error

            self.spot_turn_right(error * self.kp_turn + integral * self.ki_turn + derivative * self.kd_turn)
            imu_value = self.imu.get_tared_heading()

    def __str__(self):
        """
        String representation of the Drive object.
        """
        motor_info =  f"Left Motor: {str(self.left_motor)}\nRight Motor: {str(self.right_motor)}\n"

        if self.imu:
            imu_info = f"Current Heading: {self.imu.get_tared_heading()}\n"
        else:
            imu_info = "No IMU in-use.\n"

        tof_info = "Time-Of-Flight Readings:\n"

        if self.tof_left:
            tof_info_l = f"\tLeft: {self.tof_left.get_reading()}\n"
        else:
            tof_info_l = "\tNo Left TOF\n"

        if self.tof_centre:
            tof_info_c = f"\tCentre: {self.tof_centre.get_reading()}\n"
        else:
            tof_info_c = "\tNo Centre TOF\n"

        if self.tof_right:
            tof_info_r = f"\tRight: {self.tof_right.get_reading()}\n"
        else:
            tof_info_r = "\tNo Right TOF\n"

        return motor_info + imu_info + tof_info + tof_info_l + tof_info_c + tof_info_r
