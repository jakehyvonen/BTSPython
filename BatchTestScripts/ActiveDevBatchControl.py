from gpiozero import LED
from time import sleep
import socket
import serial
import io
import struct
import time
import picamera

#low level IC control pins
#using Sunfounder 5V relays
led1 = LED(19)
led2 = LED(13) 
led3 = LED(6) 
led4 = LED(5) 
led5 = LED(27) #led5+6 = device rest plate
led6 = LED(22)

InProgressIndicatorLed = LED(17)

###setup communication with C# software

TCP_PORT = 7007
BUFFER_SIZE = 1024
serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host = ''
serversocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
serversocket.bind((host,TCP_PORT))
serversocket.listen(1)

camera = picamera.PiCamera()
camera.resolution = (1920,1080)

#setup communication with Arduino Mega CNC controllers
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
SystemHasBeenInitialized = False

def WaitForOk():
    ser.reset_input_buffer()
    SerialBufferIsClear = False
    while(SerialBufferIsClear != True):
        MarlinMessage = ser.readline().decode()
        print(MarlinMessage)
        if("ok" in MarlinMessage):
            SerialBufferIsClear = True
            print("got the ok")

def SendCommandToCNC(com):
    print('sending command: ' + com)
    command = str(com)+"\n"
    ser.write(command.encode())
    WaitForOk()
    ser.write('M84\n'.encode())#dumb workaround to trigger busy:processing response from Marlin
    WaitForOk()

#on and off are backward (on=digital LOW) because relays are active LOW
def SwitchMUXtoA():
    led1.off()
    led2.on()
    led3.on()
    led4.on()
    
def SwitchMUXtoB():
    led1.on()
    led2.off()
    led3.on()
    led4.on()
    
def SwitchMUXtoC():
    led1.on()
    led2.on()
    led3.off()
    led4.on()
    
def SwitchMUXtoD():
    led1.on()
    led2.on()
    led3.on()
    led4.off()

def RestPlateON():
    led5.off()
    led6.off()
    
def RestPlateOFF():
    led5.on()
    led6.on()

def AllOFF():
    led1.on()
    led2.on()
    led3.on()
    led4.on()
    led5.on()
    led6.on()

def SwitchToPixelA():
    SwitchMUXtoA()
    SendCommandToCNC('G1 X6.2 Z4.3')
    #ser.write('G1 X6.2 Z4.3\n'.encode())
    
def SwitchToPixelB():
    SwitchMUXtoB()
    SendCommandToCNC('G1 X0.9 Z6.3')
    #ser.write('G1 X0.9 Z6.3\n'.encode())
    
def SwitchToPixelC():
    SwitchMUXtoC()
    SendCommandToCNC('G1 X2.8 Z11.8')
    #ser.write('G1 X2.8 Z11.8\n'.encode())
    
def SwitchToPixelD():
    SwitchMUXtoD()
    SendCommandToCNC('G1 X8.3 Z9.6')
    #ser.write('G1 X8.3 Z9.6\n'.encode())
    
def SystemInitialize():
    global SystemHasBeenInitialized
    RestPlateON()
    InProgressIndicatorLed.on()
    SendCommandToCNC('M302 P1')#Allow cold extrusion to use E motor
    SendCommandToCNC('G92 Y0')#assume Y is starting at the correct position and set to 0
    SendCommandToCNC('G28 X0 Z0')
    SendCommandToCNC('G1 Y43 F777')
    SendCommandToCNC('G1 Y40')
    SendCommandToCNC('G1 E22 F333')
    RestPlateOFF()
    print("Finished Initialization")
    SystemHasBeenInitialized = True

def SwapDevice():
    global SystemHasBeenInitialized
    if(not SystemHasBeenInitialized):
        SendCNCActiveStateSettings()
    RestPlateOFF()
    SendCommandToCNC('G1 E0 F333')
    SendCommandToCNC('G1 Y74 F777')
    SendCommandToCNC('G1 Y0')
    RestPlateON()
    SendCommandToCNC('G1 Y43')
    SendCommandToCNC('G1 Y40')
    SendCommandToCNC('G1 E22 F333')
    RestPlateOFF()
    print("Finished swapping devices")
    
def ReturnToStartPositions():
    global SystemHasBeenInitialized
    RestPlateOFF()
    InProgressIndicatorLed.off()
    if(not SystemHasBeenInitialized):
        SendCNCActiveStateSettings()
    SendCommandToCNC('G1 E0 F333')
    SendCommandToCNC('G1 Y74 F777')
    SendCommandToCNC('G1 Y0')
    SystemHasBeenInitialized = False
    
def SendCNCActiveStateSettings():
    print('Setting active state')
    sleep(7)#wait for Marlin to do stuff
    SendCommandToCNC('M302 P1')#allow cold extrusion
    SendCommandToCNC('M211 S0')#override software stops
    SendCommandToCNC('G92 Y40 E22')#set Y and E coordinates in Marlin CNC firmware
    
def TakePicture():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    #client_socket.connect(('169.254.132.130',5005))
    client_socket.connect(('192.168.1.65',7007))

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
        RestPlateOFF() #script is being dumb, dumb workaround
        SwitchMUXtoA()
    elif(var=="PixelA"):
        SwitchToPixelA()
    elif(var=="B"):
        SwitchMUXtoB()
    elif(var=="PixelB"):
        SwitchToPixelB()
    elif(var=="C"):
        SwitchMUXtoC()
    elif(var=="PixelC"):
        SwitchToPixelC()
    elif(var=="D"):
        SwitchMUXtoD()
    elif(var=="PixelD"):
        SwitchToPixelD()
    elif(var=="ActON"):
        RestPlateON()
    elif(var=="ActOFF"):
        RestPlateOFF()
    elif(var=="AllOFF"):
        AllOFF()
    elif(var=="Return"):
        ReturnToStartPositions()
    elif(var=="Initialize"):
        SystemInitialize()
    elif(var=="Swap"):
        SwapDevice()        
    else:
        SendCommandToCNC(var)
##        command = str(var)+"\n"
##        ser.write(command.encode())
##        WaitForOk()
    

    
AllOFF()
#SystemInitialize()
while True:
    conn, address = serversocket.accept()
    print ("Connection address:", address)
    data = conn.recv(BUFFER_SIZE)
    print ('received data:', data.decode())
    conn.close()
    command = data.decode()
    if(command=="Initialize"):
        SystemInitialize()
    elif(command=="PixelA"):
        SwitchToPixelA()
    elif(command=="A"):
        SwitchMUXtoA()
    elif(command=="PixelB"):
        SwitchToPixelB()
    elif(command=="B"):
        SwitchMUXtoB()
    elif(command=="PixelC"):
        SwitchToPixelC()
    elif(command=="C"):
        SwitchMUXtoC()
    elif(command=="PixelD"):
        SwitchToPixelD()
    elif(command=="D"):
        SwitchMUXtoD()
    elif(command=="Swap"):
        SwapDevice()
    elif(command=="Return"):
        ReturnToStartPositions()
    elif(command=="Picture"):
        TakePicture()
    else:
        SendCommandToCNC(command)

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

    
 ##   GetRawInput()
    
    
    
    
    
    
    
    
##def SystemInitialize():
##    RestPlateON()
##    InProgressIndicatorLed.on()
##    ser.write('M302 P1\n'.encode())
##    WaitForOk()
##    ser.write('G28 X0 Z0\n'.encode())
##    WaitForOk()
##    #ser.write('G28 Z0\n'.encode())
##    ser.write('G1 Y44 F777\n'.encode())
##    WaitForOk()
##    ser.write('G1 Y40 F777\n'.encode())
##    WaitForOk()
##    #ser.write('G1 Y0\n'.encode())
##    ser.write('G1 E175\n'.encode())
##    WaitForOk()
##    ser.write('M84\n'.encode())
##    WaitForOk()
##    #sleep(10) #buffer to prevent mistiming
##    #RestPlateOFF()
##    print("Finished Initialization")

##def SwapDevice():
##    RestPlateOFF()
##    ser.write('G1 E0\n'.encode())
##    WaitForOk()
##    ser.write('M84\n'.encode())
##    WaitForOk()
##    sleep(15)
##    ser.write('G1 Y74\n'.encode())
##    WaitForOk()
##    sleep(7)
##    #RestPlateOFF()
##    ser.write('G1 Y0\n'.encode())
##    WaitForOk()
##    RestPlateON()
##    ser.write('G1 Y44 F777\n'.encode())
##    WaitForOk()
##    ser.write('G1 Y40 F777\n'.encode())
##    WaitForOk()
##    ser.write('G1 E175\n'.encode())
##    WaitForOk()
##    ser.write('M84\n'.encode())
##    sleep(20)
##    #RestPlateOFF()
##    print("Finished swapping devices")
    
##def ReturnToStartPositions():
##    RestPlateOFF()
##    InProgressIndicatorLed.off()
##    ser.write('G1 E0\n'.encode())
##    WaitForOk()
##    ser.write('M84\n'.encode())
##    WaitForOk()
##    sleep(20)
##    ser.write('G1 Y74\n'.encode())
##    WaitForOk()
##    #RestPlateOFF()
##    ser.write('G1 Y0\n'.encode())
##    WaitForOk()
    