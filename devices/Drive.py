import math
from time import sleep_ms

from IMU import IMU
from TOF import TOF
from EncoderMotor import EncoderMotor, PID

SLEEP_BETWEEN_ACTIONS = 1000  # How long to sleep between actions, in ms. Start high when testing.

class Drive():
    def __init__(self, wheel_diameter,
                 left_motor: EncoderMotor, right_motor: EncoderMotor,
                 imu: IMU | None = None,
                 tof_left: TOF | None = None, tof_centre: TOF | None = None, tof_right: TOF | None = None):
        """
        Initialises a Drive object.

        Required Parameters:
          `wheel_diameter` (float): The diameter of the wheels in mm.
          `left_motor` (EncoderMotor): The EncoderMotor located on the drive's left side.
          `right_motor` (EncoderMotor): The EncoderMotor located on the drive's right side.
        
        Optional Parameters:
          `imu` (IMU): The IMU object (Default=None).
          `tof_left` (TOF): The Time-Of-Flight sensor on the left of the drive (Default=None).
          `tof_centre` (TOF): The Time-Of-Flight sensor on the center of the drive (Default=None).
          `tof_right` (TOF): The Time-Of-Flight sensor on the right of the drive (Default=None).
        """
        self.wheel_diameter = wheel_diameter
        
        # Initialise motors
        self.left_motor = left_motor
        self.right_motor = right_motor
        
        # Initialise sensors
        self.imu = imu
        self.tof_left = tof_left
        self.tof_centre = tof_centre
        self.tof_right = tof_right
        
        # Stored PID values (default to 0 until set up manually)
        (self.kp, self.ki, self.kd) = (1.0, 0.0, 0.0)
        
        self.pid_left = None
        self.pid_right = None
        
        
    def init_pid(self, kp, ki, kd):
        """
        Initialises PID control with the given constants.
        """
        (self.kp, self.ki, self.kd) = (kp, ki, kd)
        self.pid_left = PID(self.left_motor, kp, ki, kd)
        self.pid_right = PID(self.right_motor, kp, ki, kd)
    
    def disable_pid(self):
        """
        Disables PID control.
        """
        self.pid_left = None
        self.pid_right = None
        
    # --- Utilities ---
    def ticks_to_mm(self, ticks):
        """
        Converts encoder ticks to mm.
        """
        total_rotations = counts / self.left_motor.get_counts_per_rotation()
        mm_per_rotation = self.wheel_diameter * math.pi
        
        return total_rotations * mm_per_rotation
    
    def mm_to_ticks(self, mm):
        """
        Converts mm to encoder ticks.
        """
        mm_per_rotation = self.wheel_diameter * math.pi
        total_rotations = mm / mm_per_rotation
        
        return total_rotations * self.left_motor.get_counts_per_rotation()
    
    # --- Sensor Data ---
    def reset_encoders(self):
        """
        Tares both motor encoders.
        """
        self.left_motor.tare_encoder()
        self.right_motor.tare_encoder()
    
    # --- Movement (Open-Loop) ---
    def drive(self, l_speed, r_speed):
        """
        Drives the robot using open-loop speed control.
        """
        self.left_motor.speed(l_speed)
        self.right_motor.speed(r_speed)
    
    def straight(self, speed):
        """
        Drives the robot in a straight line using open-loop speed control.
        """
        self.drive(speed, speed)
    
    def turn(self, speed):
        """
        Turns the robot on-the-spot using open-loop speed control (a positive speed is a right turn).
        """
        self.drive(speed, -speed)
    
    def stop(self):
        """
        Stops the robot.
        """
        self.drive(0, 0)
        
    # --- Movement (Closed-Loop) ---
    def pid_drive_straight(self, target):
        """
        Drives in a straight line to a target point. Takes the target in mm.
        """
        while (self.left_motor.get_speed() != 0) or (self.right_motor.get_speed() != 0):
            self.pid_left.set_target(target)
            self.pid_right.set_target(target)
            
        sleep_ms(SLEEP_BETWEEN_ACTIONS)
        
    def pid_turn_left(self, target, break_threshold):
        """
        Turns left to a target angle using PID control. Takes the target in deg.
        Also takes a break threshold (in encoder counts) to prevent infinite loops due to calibration errors.
        """
        integral = 0
        prev_error = target
        imu_value = self.imu.get_tared_heading()
        
        target = 360 - target  # Accounting for wraparound in IMU measurement
        
        while (imu_value > target + break_threshold) or (imu_value < target - break_threshold) or (self.left_motor.get_speed() != 0) or (self.right_motor.get_speed() != 0):
            error = target - imu_value
            derivative = error - prev_error
            prev_error = error
            if abs(error) > 7 or error == 0:
                integral = 0
            else:
                integral += error
            
            speed = error * self.kp + integral * self.ki + derivative * self.kd
            self.turn(-speed)
            
        sleep_ms(SLEEP_BETWEEN_ACTIONS)
        
    def pid_turn_right(self, target, break_threshold):
        """
        Turns right to a target angle using PID control. Takes the target in deg.
        Also takes a break threshold (in encoder counts) to prevent infinite loops due to calibration errors.
        """
        integral = 0
        prev_error = target
        imu_value = self.imu.get_tared_heading()
        while (imu_value > target + break_threshold) or (imu_value < target - break_threshold) or (self.left_motor.get_speed() != 0) or (self.right_motor.get_speed() != 0):
            error = target - imu_value
            derivative = error - prev_error
            prev_error = error
            if abs(error) > 7 or error == 0:
                integral = 0
            else:
                integral += error
            
            speed = error * self.kp + integral * self.ki + derivative * self.kd
            self.turn(speed)
            
        sleep_ms(SLEEP_BETWEEN_ACTIONS)
    
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

        