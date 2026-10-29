import digitalio

class MotorDriver():
    def __init__(self, standby_pin):
        """
        Initialises a MotorDriver object. 

        Required Parameters:
          `standby_pin` (pin): Standby pin on the motor driver.
        """
        # Enable the driver's standby pin
        self.standby = digitalio.DigitalInOut(standby_pin)
        self.standby.direction = digitalio.Direction.OUTPUT
        self.standby.value = True  # Take driver out of standby mode