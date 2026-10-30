import time
import board
import busio
import adafruit_tca9548a
import adafruit_vl53l4cd

# Initialize the primary I2C bus on GP4 and GP5
i2c = busio.I2C(board.GP5, board.GP4)

# Bind the TCA9548A multiplexer to the I2C bus
tca = adafruit_tca9548a.TCA9548A(i2c)

# Instantiate three distinct instances of the sensor on different multiplexer channels
sensor1 = adafruit_vl53l4cd.VL53L4CD(tca[0])
sensor2 = adafruit_vl53l4cd.VL53L4CD(tca[1])
sensor3 = adafruit_vl53l4cd.VL53L4CD(tca[2])

# Configure and initiate ranging on each sensor
sensors = [sensor1, sensor2, sensor3]
for idx, sensor in enumerate(sensors):
    sensor.timing_budget = 50  # Set timing budget in milliseconds (min 10ms)
    sensor.inter_measurement = 0
    sensor.start_ranging()
    print(f"Sensor {idx+1} initialized.")

while True:
    for idx, sensor in enumerate(sensors):
        # Check if the target channel has finished taking a reading
        if sensor.data_ready:
            print(f"Sensor {idx+1} Distance: {sensor.distance:.1f} cm")
            sensor.clear_interrupt()
            
    time.sleep(0.1)

