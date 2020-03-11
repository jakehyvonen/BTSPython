import picamera
import time

camera = picamera.PiCamera()

try:
    camera.resolution = (1920,1080)
    camera.start_preview()
    time.sleep(33)
    
finally:
    camera.stop_preview()