# Import Raspberry Pi GPIO library to control GPIO pins
import RPi.GPIO as GPIO
import movement_control
# Import time library for delays
import time

#=========================================
#Angle and value retrieval
#=========================================


while True:
    try:
        angle_prompt = input("Input the desired angle you wish to turn to: ") #Prompts user to insert their desired angle
        angle = int (angle_prompt) #converts the input vlaue to a usable int
        break #Breaks the loop in the case of no errors
    except ValueError:
        print("Invalid Value, please try again")
        time.sleep(2) #Send an error message before resetting to the beginning of the loop in case of ValueError

#==========================================
#Main Program
#==========================================


        
if angle < 0 : #Checks whether to turnn clockwise or counterclockwise
    movement_control.turnleft(-angle)
else:
    movement_control.turnright(angle)

# Stop the robot and effectively ends the program
movement_control.stop(2)
