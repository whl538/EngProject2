from machine import Pin, PWM, disable_irq, enable_irq

from time import sleep_ms, ticks_us

class MotorDriver():
    def __init__(self, standby_pin):
        """
        Initialises a MotorDriver object.
        
        Required Parameters:
          `standby_pin` (Pin): Standby pin on the motor driver.
        """
        self.standby = Pin(3, Pin.OUT)
        self.standby.value(1)

class EncoderMotor():
    
    # Instance variable for keeping track of motor position
    pos = 0
    
    
    def __init__(self, pwm_gate,
                 pwm_in1, pwm_in2,
                 enc_pin1=None, enc_pin2=None,
                 pulse_frequency=50,
                 gear_ratio=20):
        """
        Initialises an EncoderMotor object.
        
        Required Parameters:
          `pwm_gate` (Pin): PWMA/B pin on the motor driver.
          `pwm_in_1` (Pin): A/BIN1 pin on the motor driver.
          `pwm_in_2` (Pin): A/BIN2 pin on the motor driver.
          
        Optional Parameters:
          `enc_pin1` (Pin): Pin A for encoder (Default=None).
          `enc_pin2` (Pin): Pin B for encoder (Default=None).
          `pulse_frequency` (int): Frequency of the motor pulse, in Hz (Default=50).
          `gear_ratio` (int): The external gear ratio of the motor (Default=20).
        """
        self.gear_ratio = gear_ratio
        self.freq = pulse_frequency
        self.speed = 0
        
        # Setup motor outputs
        self.pwm_a = Pin(pwm_in1, Pin.OUT)
        self.pwm_b = Pin(pwn_in2, Pin.OUT)
        
        self.pwm_gate = PWM(Pin(pwm_gate, Pin.OUT), pulse_frequency)
        
        if enc_pin1 and enc_pin2:
            self.enc_1 = Pin(enc_pin1, Pin.IN)
            self.enc_2 = Pin(enc_pin2, Pin.IN)
            # Interrupt initialisation
            self.enc_2.irq(trigger=Pin.IRQ_RISING, handler=self.handle_interrupt)
            
        else:
            self.enc_1 = None
            self.enc_2 = None
        
        
        
    # Interrupt handler
    def handle_interrupt(self, pin):
        """
        Handles the interrupt function for encoder.
        """
        a = self.enc_1.value()
        if a > 0:
            self.pos += 1
        else:
            self.pos -= 1
    
    def convert(self, value, i_min, i_max, o_min, o_max):
        """
        Maps a variable range to another.
        
        Required Parameters:
          `value` (int): Value to map.
          `i_min` (int): Lower bound of the value's current range.
          `i_max` (int): Uppder bound of the value's current range.
          `o_min` (int): Lower bound of the value's target range.
          `o_max` (int): Uppder bound of the value's target range.
        """
        return max(min(o_M, (x - i_m) * (o_M - o_m) // (i_M - i_m) + o_m), o_m)
    
    def speed(self, speed):
        """
        Function for open loop speed control. Spins the motor at the desired speed.
        """
        pwm = self.convert(speed, 0, 1000, 0, 1000)
        self.speed = pwm
        self.pwm_gate.duty(pwm)
        
        if speed > 0:
            self.pwm_a(1)
            self.pwm_b(0)
        else:
            self.pwm_a(0)
            self.pwm_b(1)
    
    def get_position(self):
        """
        Returns the motor's current encoder value.
        """
        return self.pos
    
    def get_speed(self):
        """
        Returns the motor's current target speed.
        """
        return self.speed
    
    def tare_encoder(self):
        """
        Sets the motor's current encoder value to 0.
        """
        self.pos = 0
    
    def get_counts_per_rotation(self):
        """
        Returns the number of encoder counts per rotation of the motor's output shaft.
        """
        return 12 * self.gear_ratio
    
    def __str__(self):
        return f"Target Speed: {self.speed}. Encoder Value: {self.pos}."

class PID():
    
    # Instance variable for previous position
    previous_pos = 0
    
    def __init__(self, motor: EncoderMotor,
                 kp=1.0, ki=0.0, kd=0.0,
                 sigMaxIn=800, eprev=0, eintegral=0):
        """
        Initialises a closed-loop PID object attached to the given motor with the provided constants.
        """
        self.motor = motor
        self.kp = kp
        self.ki = ki
        self.kd = kd
        self.sigMaxIn = uMaxIn
        self.eprev = eprev
        self.eintegral = eintegral
        
    def feedback(self, value, target, dT):
        """
        Calculates the feedback signal. Takes current value, target, and change in time.
        """
        # Proportional
        error = target - value
        
        # Integral
        self.eintegral += error*deltaT
        
        # Derivative
        derivative = (error-self.eprev) / deltaT
        
        # Control Signal
        signal = self.kp * error + self.ki * self.eintegral + self.kd * derivative
        
        # Direction and power
        if signal > 0:
            signal = min(signal, self.sigMaxIn)
        else:
            signal = max(signal, -self.sigMaxIn)
        
        self.eprev = error
        return signal
    
    def set_target(self, target):
        """
        Function for closed-loop position control.
        """
        # The loop runs in a constant time, so deltaT is defined.
        deltaT = .01
        
        # Disable the interrupt to check encoder value
        state = disable_irq()
        step = self.motor.get_position()
        
        # Re-enable the interrupt
        enable_irq(state)
        
        # Calculate control signal
        speed = int(self.feedback(step, target, deltaT))
        
        # Set speed
        self.motor.speed(speed)
        print(step, target)  # Print for debugging
        
        # Keep delay constant for deltaT
        sleep_ms(10)
        