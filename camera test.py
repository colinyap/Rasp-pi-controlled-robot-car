import cv2
import picamera2
import numpy as np
from picamera2 import Picamera2
import time
 
# Initialize video capture
picam2 = Picamera2()
picam2.configure(picam2.create_preview_configuration(main={"format": "XRGB8888", "size": (640, 480)}))
picam2.start()

while True:
    frame = picam2.capture_array()
    
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY) #Convert to grayscale

    
    _, bw = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY) #Prints out a pure black and white image based on the min and max threshold

    cv2.imshow("BW", bw) #Creates a preview window for the mask 
    cv2.imshow("Frame", frame) #Creates a preview window for the normal camera feed for comparison
    if cv2.waitKey(1) & 0xff ==ord('q'): #Exits the loop when the letter q is pressed
        break
 
 
# Clean up
picam2.stop
cv2.destroyAllWindows()
