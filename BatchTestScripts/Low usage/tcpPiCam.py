import io
import socket
import struct
import picamera
import time

client_socket = socket.socket(

try:
    camera = picamera.PiCamera()
    camera.resolution = (1920,1080)
    camera.start_preview()
    time.sleep(60)
    
finally:
    camera.stop_preview()