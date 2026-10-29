from IMU import IMU
from TOF import TOF
from EncoderMotor import EncoderMotor

class Drive():
    def __init__(self, left_motor: EncoderMotor, right_motor: EncoderMotor,
                 imu: IMU | None = None,
                 tof_left: TOF | None = None, tof_centre: TOF | None = None, tof_right: TOF | None = None):
        """
        Initialises a Drive object.

        Required Parameters:
          `left_motor` (EncoderMotor): The EncoderMotor located on the drive's left side.
          `right_motor` (EncoderMotor): The EncoderMotor located on the drive's right side.
        
        Optional Parameters:
          `imu` (IMU): The IMU object (Default=None)
          `tof_left` (TOF): The Time-Of-Flight sensor on the left of the drive
          `tof_centre` (TOF): The Time-Of-Flight sensor on the center of the drive
          `tof_right` (TOF): The Time-Of-Flight sensor on the right of the drive
        """
        # Initialise motors
        self.left_motor = left_motor
        self.right_motor = right_motor

        self.reference_motor = left_motor  # Motor encoder to reference for PID Control

        # Initialise sensors
        self.imu = imu
        self.tof_left = tof_left
        self.tof_centre = tof_centre
        self.tof_right = tof_right

        # Stored PID values (default to preassigned values until set up manually)
        self.kp_straight = 0.1
        self.ki_straight = 0.05
        self.kd_straight = 0.1

        self.kp_turn = 0.1
        self.ki_turn = 0.05
        self.kd_turn = 0.1

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

    # -- Sensor Data ---
    def reset_encoders(self):
        """
        Resets both encoders back to 0.
        """
        self.left_motor.tare_encoder()
        self.right_motor.tare_encoder()

    # --- Basic Drive Functions (No Sensors) ---
    def forward(self, speed):
        """
        Drives forward at the given percentage speed.
        """
        self.left_motor.spin(speed)
        self.right_motor.spin(speed)

    def backward(self, speed):
        """
        Drives backward at the given percentage speed. Takes a POSITIVE argument.
        """
        self.left_motor.spin(-speed)
        self.right_motor.spin(-speed)

    def turn_left(self, speed):
        pass

    def turn_right(self, speed):
        pass

    def stop(self):
        """
        Stops both drive motors.
        """
        self.left_motor.stop()
        self.right_motor.stop()

    def __str__(self):
        """
        String representation of the Drive object.
        """
        motor_info =  f"Left Motor: {str(self.left_motor)}\nRight Motor: {str(self.right_motor)}\n"
        if self.imu:
            imu_info = f"Current Heading: {self.imu.get_tared_heading()}\n"
        else:
            imu_info = "No IMU in-use.\n"
        return motor_info + imu_info