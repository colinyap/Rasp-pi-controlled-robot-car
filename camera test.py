import RPi.GPIO as GPIO
from picamera2 import Picamera2, Preview
import time

GPIO.setwarnings(False)
# Create a Picamera2 object
picam2 = Picamera2()

# Create a configuration suitable for still images
config = picam2.create_preview_configuration()
picam2.configure(config)

# Start the camera and preview (preview will appear in a separate window)
picam2.start_preview(Preview.QT)
picam2.start()



picam2.capture_file("test_photo.jpg")


try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    pass
finally:
    picam2.stop()