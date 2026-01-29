# Import Raspberry Pi GPIO library to control GPIO pins
import RPi.GPIO as GPIO
import movement_control
# Import time library for delays
import time

#=========================================
#Distance Value retrieval
#=========================================
while True:
    try:
        distance_prompt = input("Input the desired distance you wish to travel (Insert a negative value to go backwards): ")
        distance = int (distance_prompt)
        break
    except ValueError:
        print("Invalid Value, please try again")
        time.sleep(2)
#==========================================
#Main Program
#==========================================

if distance<0:
    movement_control.goback(-distance)
else:
    movement_control.gostraight(distance)

# Stop the robot, effectively ending the program
movement_control.stop(2)

