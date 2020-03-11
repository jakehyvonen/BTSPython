import socket
from time import sleep

#TCP_IP = '169.254.130.182'
#TCP_IP = '127.0.0.1'
TCP_PORT = 5005
BUFFER_SIZE = 1024
serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host = ''
serversocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
serversocket.bind((host,TCP_PORT))
serversocket.listen(1)

while True:
    conn, address = serversocket.accept()
    print ("Connection address:", address)
    data = conn.recv(BUFFER_SIZE)
    print ('received data:', data.decode())
    conn.close
    #sleep(1)

##TCP_IP = '169.254.130.182'
##TCP_PORT = 5005
##BUFFER_SIZE = 1024
##MESSAGE = "Hello, windummy"
##
##while True:
##    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
##    s.connect((TCP_IP, TCP_PORT))
##    s.send(str.encode(MESSAGE))
##    data = s.recv(BUFFER_SIZE)
##    #s.close()
##    sleep(10)
##    print(data.decode())
##    s.close()
