import io
import socket
import struct
import time
import picamera

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect(('192.168.77.1',5005))

try:
    camera = picamera.PiCamera()
    camera.resolution = (1024,768)
    camera.start_preview()
    time.sleep(2)
    
    camera.capture(client_socket, 'jpeg')
    camera.stop_preview()
    
finally:
    client_socket.close()