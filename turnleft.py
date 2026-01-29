# Function to turn the robot left
# angle: angle to turn (degrees, based on calibration)
def turnleft(angle):
    GPIO.output(IN1, True)   # Left motor forward
    GPIO.output(IN2, False)
    GPIO.output(IN3, False)  # Right motor backward
    GPIO.output(IN4, True)
    time.sleep(angle / Duty_cycle_angle)