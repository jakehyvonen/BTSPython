import socket
from time import sleep

TCP_IP = '192.168.77.1'
TCP_PORT = 5005
BUFFER_SIZE = 1024
MESSAGE = 'Hello, World!'

while(True):
    MESSAGE_asbytes = str.encode(MESSAGE)
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((TCP_IP, TCP_PORT))
    s.send(MESSAGE_asbytes)
    data = s.recv(BUFFER_SIZE)
    s.close()

    print(data)
    sleep(1)
    
