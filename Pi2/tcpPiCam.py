import io
import socket
import struct
import time
import picamera

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect(('192.168.77.1',5005))

connection = client_socket.makefile('wb')
try:
    camera = picamera.PiCamera()
    camera.resolution = (1920,1080)
    camera.start_preview()
    time.sleep(2)
    start = time.time()
    stream = io.BytesIO()
    camera.capture(stream, 'jpeg')
    camera.stop_preview()
    connection.write(struct.pack('<L',stream.tell()))
    connection.flush()
    stream.seek(0)
    connection.write(stream.read())
finally:
    connection.close()
    client_socket.close()
    print('finished')