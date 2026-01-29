import time

#====================================================
#Main code
#====================================================
while True:
    try:
        mode_prompt = input("Select angle mode (1) or distance mode (2): ") #Prompts the user to decide whether they wna to run angle or distance mode
        mode = int (mode_prompt)
        if mode != 1 and mode != 2:
            print("Invalid number, please choose either 1 or 2") #Resets to the top of the kloop in the event of an invalid number
            time.sleep(2)
        else:
            break
    except ValueError:
        print("Invalid Value, please try again") #Resets to the top of the loop in case of ValueError
        time.sleep(2)
        

if mode == 1: #Runs either angle_control or distance_control depending on user selection
    import angle_control
else:
    import distance_control
        
    