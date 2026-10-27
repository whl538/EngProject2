from machine import Pin, PWM #tells pico to load hardware,pin turns them on/off, pwm controls motor speed
import time #built in libary for like sleep in arduino

#Motor Driver setup
stby = Pin(3, Pin.OUT) #stby connected to gp3/pin 5
stby.value(1) #sends HIGH signal to wake up motor chip

#Motor A-White wires for outs in encoder
ain1 = Pin(1, Pin.OUT) 	#
ain2 = Pin(0, Pin.OUT) 	#
pwm_a = PWM(Pin(2))		#
pwm_a.freq(1000)		#

#Motor B-Green wires from encoder
bin1 = Pin(5, Pin.OUT) 	#
bin2 = Pin(4, Pin.OUT) 	#
pwm_b = PWM(Pin(6))		#
pwm_b.freq(1000)		#

#Encoder setup- 54 ticks was 1 revolution, at 10000 speed so
                # distance travelled = circumference of wheel / 54

#Motor A-left side
encoder_A_a = Pin(15, Pin.IN, Pin.PULL_UP) #how fast wheel spinning (channel A)- gp15
encoder_A_b = Pin(14, Pin.IN, Pin.PULL_UP) #what direction wheel spinning (Channel B)-gp14
encoder_A_count = 0 #

def encoder_A_isr(pin): #interupt function to check encoder for motor A
    global encoder_A_count #allows function to modify variable
    if encoder_A_b.value()==1: #checks channel b of encoder
        encoder_A_count += 1 # if high(spinning forward) add 1 to count
    else:
        encoder_A_count -= 1 #if low(spinning backward) minus 1 to count

encoder_A_a.irq(trigger=Pin.IRQ_RISING, handler=encoder_A_isr) #interrupt request- run function when gp15 goes low to high

#Motor B- right side

encoder_B_a = Pin(13, Pin.IN, Pin.PULL_UP) #how fast wheel spinning (channel A)- gp13
encoder_B_b = Pin(12, Pin.IN, Pin.PULL_UP) #what direction wheel spinning (Channel B)-gp12
encoder_B_count = 0 #

def encoder_B_isr(pin): #interupt function to check encoder for motor B
    global encoder_B_count #allows function to modify variable
    if encoder_B_b.value()==1: #checks channel b of encoder
        encoder_B_count += 1 # if high(spinning forward) add 1 to count
    else:
        encoder_B_count -= 1 #if low(spinning backward) minus 1 to count

encoder_B_a.irq(trigger=Pin.IRQ_RISING, handler=encoder_B_isr) #interrupt request- run function when gp13 goes low to high

#moving robot

def drive_forward(speed): #creates function/command that accepts speed
    #Motor A
    ain1.value(1) #motor goes forward
    ain2.value(0)
    pwm_a.duty_u16(speed) #duty cycle of pwm, u means unsigned- only posotive, 16 for a 16 bit interger as pico has 16-bit timer
    
    #Motor B
    bin1.value(1) #motor goes forward
    bin2.value(0)
    pwm_b.duty_u16(speed) #
    
def turn_left(speed):
     #Motor A
    ain1.value(0) #motor backward
    ain2.value(1)
    pwm_a.duty_u16(speed) #
    
    #Motor B
    bin1.value(1) #motor forward
    bin2.value(0)
    pwm_b.duty_u16(speed) #
    
def turn_right(speed):
     #Motor A
    ain1.value(1) #motor forward
    ain2.value(0)
    pwm_a.duty_u16(speed) #
    
    #Motor B
    bin1.value(0) #motor backward
    bin2.value(1)
    pwm_b.duty_u16(speed) #

def drive_backward(speed):
     #Motor A
    ain1.value(0) #motor backward
    ain2.value(1)
    pwm_a.duty_u16(speed) #
    
    #Motor B
    bin1.value(0) #motor backward
    bin2.value(1)
    pwm_b.duty_u16(speed)

    
def stop_motors(): #stops both motors
    #Motor A
    ain1.value(0) 
    ain2.value(0)
    pwm_a.duty_u16(0) 
    
    #Motor B
    bin1.value(0)
    bin2.value(0)
    pwm_b.duty_u16(0)
    

#main program loop
    
print("Robot test starting...")

try:#testing code
    while True:
        print("Driving forward...")
        drive_forward(40000) # Speed value from 0 to 65535
        
        # Print encoder counts for 3 seconds
        start_time = time.ticks_ms()
        while time.ticks_diff(time.ticks_ms(), start_time) < 3000:#1000 miliseconds is 1 second
            print(f"Encoder A: {encoder_A_count} | Encoder B: {encoder_B_count}")# fills curly brackets with counter number
            time.sleep(0.5)
            
        print("Turning left...")
        turn_left(40000)

         # Print encoder counts for 3 seconds
        start_time = time.ticks_ms()
        while time.ticks_diff(time.ticks_ms(), start_time) < 3000:#1000 miliseconds is 1 second
            print(f"Encoder A: {encoder_A_count} | Encoder B: {encoder_B_count}")# fills curly brackets with counter number
            time.sleep(0.5)

        print("Turning right...")
        turn_right(40000)

         # Print encoder counts for 3 seconds
        start_time = time.ticks_ms()
        while time.ticks_diff(time.ticks_ms(), start_time) < 3000:#1000 miliseconds is 1 second
            print(f"Encoder A: {encoder_A_count} | Encoder B: {encoder_B_count}")# fills curly brackets with counter number
            time.sleep(0.5)
            
        print("Going Backwards...")
        drive_backward(40000)
        
         # Print encoder counts for 3 seconds
        start_time = time.ticks_ms()
        while time.ticks_diff(time.ticks_ms(), start_time) < 3000:#1000 miliseconds is 1 second
            print(f"Encoder A: {encoder_A_count} | Encoder B: {encoder_B_count}")# fills curly brackets with counter number
            time.sleep(0.5)
   
        print("Stopping...")
        stop_motors()
        time.sleep(2)
        
        # Reset counts for the next run if desired
        encoder_A_count = 0
        encoder_B_count = 0
        
        print("Waiting before next loop...")
        time.sleep(2)

except KeyboardInterrupt:
    # Safely stop motors if you click the Stop button in Thonny
    stop_motors()
    print("Program stopped safely.")
