import time
import board
import busio
import adafruit_vl53l4cd

# Initialize the I2C bus using GP4 (SDA) and GP5 (SCL)
i2c = busio.I2C(board.GP5, board.GP4)

# Initialize the VL53L4CD sensor
sensor = adafruit_vl53l4cd.VL53L4CD(i2c)

# Optional: Configure the sensor settings
# Valid timing budgets: 10ms to 200ms (10ms is fast but noisy; 200ms is highly accurate)
sensor.timing_budget = 50 
# Valid inter-measurement periods: must be >= timing_budget
sensor.inter_measurement = 60 

print("VL53L4CD Initialized successfully!")
print("---------------------------------")

# Start continuous ranging measurements
sensor.start_ranging()

while True:
    # Check if a new distance reading is ready
    if sensor.data_ready:
        # Distance is returned in centimeters; clear the interrupt to request the next reading
        distance_cm = sensor.distance
        sensor.clear_interrupt()
        
        # Convert to millimeters for standard ToF precision
        distance_mm = distance_cm * 10
        
        print(f"Distance: {distance_mm:.1f} mm")
        
    time.sleep(0.05)
