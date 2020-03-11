from gpiozero import LED
from time import sleep
import socket
import serial
import io
import struct
import time
import picamera

#low level IC control pins
led1 = LED(13) #A0 pin
led2 = LED(6) #A1 pin
led3 = LED(5) #A2 pin
led4 = LED(27) #led4+5 = device rest plate
led5 = LED(22)

InProgressIndicatorLed = LED(17)

###setup communication with C# software

TCP_PORT = 5005
BUFFER_SIZE = 1024
serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host = ''
serversocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
serversocket.bind((host,TCP_PORT))
serversocket.listen(1)

camera = picamera.PiCamera()
camera.resolution = (1920,1080)

#setup communication with Arduino Mega CNC controller
ser = serial.Serial(
    
    port="/dev/ttyACM0",
    baudrate=250000,
    parity=serial.PARITY_NONE,
    stopbits=serial.STOPBITS_ONE,
    bytesize=serial.EIGHTBITS,
    dsrdtr=True,
    rtscts=True,
    timeout=1
    )
ser.get_settings()
ser.readlines()
SerialBufferIsClear = True

def WaitForOk():
    SerialBufferIsClear = False
    while(SerialBufferIsClear != True):
        MarlinMessage = ser.readline().decode()
        print(MarlinMessage)
        if("ok" in MarlinMessage):
            SerialBufferIsClear = True
            print("got the ok")

def SwitchMUXtoA():
    led1.off()
    led2.off()
    led3.off()
    
def SwitchMUXtoB():
    led1.on()
    led2.off()
    led3.off()
    
def SwitchMUXtoC():
    led1.off()
    led2.on()
    led3.off()
    
def SwitchMUXtoD():
    led1.on()
    led2.on()
    led3.off()

def RestPlateON():
    led4.off()
    led5.off()
    
def RestPlateOFF():
    led4.on()
    led5.on()

def SwitchToPixelA():
    RestPlateOFF() #script is being dumb, dumb workaround
    SwitchMUXtoA()
    ser.write('G1 X6.2 Z4.3\n'.encode())
    
def SwitchToPixelB():
    SwitchMUXtoB()
    ser.write('G1 X0.9 Z6.3\n'.encode())
    
def SwitchToPixelC():
    SwitchMUXtoC()
    ser.write('G1 X2.8 Z11.8\n'.encode())
    
def SwitchToPixelD():
    SwitchMUXtoD()
    ser.write('G1 X8.3 Z9.6\n'.encode())



def SwapDevice():
    RestPlateOFF()
    ser.write('G1 E0\n'.encode())
    WaitForOk()
    ser.write('M84\n'.encode())
    WaitForOk()
    sleep(15)
    ser.write('G1 Y54\n'.encode())
    WaitForOk()
    sleep(7)
    #RestPlateOFF()
    ser.write('G1 Y0\n'.encode())
    WaitForOk()
    RestPlateON()
    ser.write('G1 Y43 F777\n'.encode())
    WaitForOk()
    ser.write('G1 E175\n'.encode())
    WaitForOk()
    ser.write('M84\n'.encode())
    sleep(20)
    #RestPlateOFF()
    print("Finished swapping devices")
    
def SystemInitialize():
    RestPlateON()
    InProgressIndicatorLed.on()
    ser.write('M302 P1\n'.encode())
    WaitForOk()
    ser.write('G28 X0 Z0\n'.encode())
    WaitForOk()
    #ser.write('G28 Z0\n'.encode())
    ser.write('G1 Y43 F777\n'.encode())
    WaitForOk()
    #ser.write('G1 Y0\n'.encode())
    ser.write('G1 E175\n'.encode())
    WaitForOk()
    ser.write('M84\n'.encode())
    WaitForOk()
    #sleep(10) #buffer to prevent mistiming
    #RestPlateOFF()
    print("Finished Initialization")
    
def ReturnToStartPositions():
    RestPlateOFF()
    InProgressIndicatorLed.off()
    ser.write('G1 E0\n'.encode())
    WaitForOk()
    ser.write('M84\n'.encode())
    WaitForOk()
    sleep(20)
    ser.write('G1 Y54\n'.encode())
    WaitForOk()
    #RestPlateOFF()
    ser.write('G1 Y0\n'.encode())
    WaitForOk()
    
def TakePicture():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    #client_socket.connect(('169.254.132.130',5005))
    client_socket.connect(('192.168.1.42',5005))

    connection = client_socket.makefile('wb')
    try:
        
        #camera.start_preview()
        #time.sleep(2)
        start = time.time()
        stream = io.BytesIO()
        camera.capture(stream, 'jpeg')
        camera.stop_preview()
        connection.write(struct.pack('<L',stream.tell()))
        connection.flush()
        stream.seek(0)
        connection.write(stream.read())
    finally:
        #connection.close()
        #client_socket.close()
        print('finished')


def GetRawInput():
    var = input("Please enter a command:")
    print("entered: "+str(var))
    if(var=="A"):
        SwitchMUXtoA()
    if(var=="PixelA"):
        SwitchToPixelA()
    if(var=="B"):
        SwitchMUXtoB()
    if(var=="PixelB"):
        SwitchToPixelB()
    if(var=="C"):
        SwitchMUXtoC()
    if(var=="PixelC"):
        SwitchToPixelC()
    if(var=="D"):
        SwitchMUXtoD()
    if(var=="PixelD"):
        SwitchToPixelD()
    if(var=="ActON"):
        RestPlateON()
    if(var=="ActOFF"):
        RestPlateOFF()
    if(var=="Return"):
        ReturnToStartPositions()
    if(var=="Initialize"):
        SystemInitialize()
    if(var=="Swap"):
        SwapDevice()
    else:
        command = str(var)+"\n"
        ser.write(command.encode())
        WaitForOk()
 


RestPlateOFF()
#SystemInitialize()
while True:
    conn, address = serversocket.accept()
    print ("Connection address:", address)
    data = conn.recv(BUFFER_SIZE)
    print ('received data:', data.decode())
    conn.close
    command = data.decode()
    if(command=="Initialize"):
        SystemInitialize()
    if(command=="PixelA"):
        SwitchToPixelA()
    if(command=="PixelB"):
        SwitchToPixelB()
    if(command=="PixelC"):
        SwitchToPixelC()
    if(command=="PixelD"):
        SwitchToPixelD()
    if(command=="Swap"):
        SwapDevice()
    if(command=="Return"):
        ReturnToStartPositions()
    if(command=="Picture"):
        TakePicture()
    

##
##    print("pixel A")
##    SwitchToPixelA()
##    sleep(10)
##    print("pixel B")
##    SwitchToPixelB()
##    sleep(10)
##    print("pixel C")
##    SwitchToPixelC()
##    sleep(10)
##    print("pixel D")
##    SwitchToPixelD()
##    sleep(10)
##    SwapDevice()

    
##    GetRawInput()
    