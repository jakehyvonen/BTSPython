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