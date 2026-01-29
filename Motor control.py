# Import Raspberry Pi GPIO library to control GPIO pins
import RPi.GPIO as GPIO

# Import time library for delays
import time

# Disable GPIO warnings (useful when re-running the script)
GPIO.setwarnings(False)

# Use BCM pin numbering (GPIO numbers, not physical pin numbers)
GPIO.setmode(GPIO.BCM)

# Define GPIO pins connected to the motor driver
ENA = 14   # Enable pin for Motor A (PWM speed control)
ENB = 4    # Enable pin for Motor B (PWM speed control)
IN1 = 15   # Motor A direction pin 1
IN2 = 18   # Motor A direction pin 2
IN3 = 2    # Motor B direction pin 1
IN4 = 3    # Motor B direction pin 2

# Set default duty cycle (motor speed percentage)
Duty_cycle = 100

# Variables used for timing-based movement calibration
Duty_cycle_angle = 0   # Used for turning (degrees per second)
Duty_cycle_speed = 0   # Used for straight motion (distance per second)

# PWM frequency in Hz
PWM_frequency = 1000

# Set all motor-related GPIO pins as outputs
GPIO.setup(ENA, GPIO.OUT)
GPIO.setup(IN1, GPIO.OUT)
GPIO.setup(IN2, GPIO.OUT)
GPIO.setup(IN3, GPIO.OUT)
GPIO.setup(IN4, GPIO.OUT)
GPIO.setup(ENB, GPIO.OUT)

# Match-case structure to calibrate speed and turning based on duty cycle
match Duty_cycle:
    case 100:
        Duty_cycle_angle = 207  # Turning calibration for 100% speed
        Duty_cycle_speed = 59   # Forward speed calibration for 100%
    
    case 75:
        Duty_cycle_angle = 131  # Turning calibration for 75% speed
        Duty_cycle_speed = 44   # Forward speed calibration for 75%
        
    case 50:
        Duty_cycle_angle = 68   # Turning calibration for 50% speed
        Duty_cycle_speed = 31   # Forward speed calibration for 50%

# Function to move the robot straight forward
# distance: distance to move (units based on calibration)
def gostraight(distance):
    GPIO.output(IN1, True)   # Motor A forward
    GPIO.output(IN2, False)
    GPIO.output(IN3, True)   # Motor B forward
    GPIO.output(IN4, False)
    time.sleep(distance / Duty_cycle_speed)  # Time-based movement

# Function to move the robot backward
def goback(distance):
    GPIO.output(IN1, False)  # Motor A backward
    GPIO.output(IN2, True)
    GPIO.output(IN3, False)  # Motor B backward
    GPIO.output(IN4, True)
    time.sleep(distance / Duty_cycle_speed)

# Function to turn the robot left
# angle: angle to turn (degrees, based on calibration)
def turnleft(angle):
    GPIO.output(IN1, True)   # Left motor forward
    GPIO.output(IN2, False)
    GPIO.output(IN3, False)  # Right motor backward
    GPIO.output(IN4, True)
    time.sleep(angle / Duty_cycle_angle)

# Function to turn the robot right
def turnright(angle):
    GPIO.output(IN1, False)  # Left motor backward
    GPIO.output(IN2, True)
    GPIO.output(IN3, True)   # Right motor forward
    GPIO.output(IN4, False)
    time.sleep(angle / Duty_cycle_angle)

# Function to stop the robot for a specified time
def stop(seconds):
    GPIO.output(IN1, False)  # Stop Motor A
    GPIO.output(IN2, False)
    GPIO.output(IN3, False)  # Stop Motor B
    GPIO.output(IN4, False)
    time.sleep(seconds)

# Create PWM object for Motor A enable pin
pwm1 = GPIO.PWM(ENA, PWM_frequency)
pwm1.start(Duty_cycle)  # Start PWM with specified duty cycle

# Create PWM object for Motor B enable pin
pwm2 = GPIO.PWM(ENB, PWM_frequency)
pwm2.start(Duty_cycle)

# Move the robot straight for a distance of 1 (calibrated unit)
gostraight(1)

# Stop the robot for 2 seconds
stop(2)
