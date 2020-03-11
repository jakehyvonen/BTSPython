from gpiozero import LED
from time import sleep
import socket
import serial

#low level IC control pins
led1 = LED(13) #A0 pin
led2 = LED(6) #A1 pin
led3 = LED(5) #A2 pin
led4 = LED(27) #led4+5 = device rest plate
led5 = LED(22)

###setup communication with C# host software
##TCP_IP = '169.254.130.182'
##TCP_PORT = 5005
##BUFFER_SIZE = 1024
##MESSAGE = "Hello, windummy"
##
##s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
##s.connect((TCP_IP, TCP_PORT))
###s.send(str.encode(MESSAGE))

#setup communication with Arduino Mega CNC controller
ser = serial.Serial(
    
    port="/dev/ttyACM1",
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
    led4.on()
    led5.on()
    
def RestPlateOFF():
    led4.off()
    led5.off()
    
#gcode-pixel positions 05/21/18
#pixel A: X5.3 Z0.9
#pixel B: X0 Z2.9
#pixel C: X2.1 Z8.3
#pixel D: X7.4 Z6.3

def SwitchToPixelA():
    SwitchMUXtoA()
    ser.write('G1 X5.3 Z0.9\n'.encode())
    
def SwitchToPixelB():
    SwitchMUXtoB()
    ser.write('G1 X0 Z2.9\n'.encode())
    
def SwitchToPixelC():
    SwitchMUXtoC()
    ser.write('G1 X2.1 Z8.3\n'.encode())
    
def SwitchToPixelD():
    SwitchMUXtoD()
    ser.write('G1 X7.4 Z6.3\n'.encode())


def SwapDevice():
    ser.write('G1 E0\n'.encode())
    SerialBufferIsClear = False
    while(SerialBufferIsClear != True):
        MarlinMessage = ser.readline().decode()
        print(MarlinMessage)
        if("ok" in MarlinMessage):
            SerialBufferIsClear = True
            print("got the ok")
    ser.write('M84\n'.encode())
    SerialBufferIsClear = False
    while(SerialBufferIsClear != True):
        MarlinMessage = ser.readline().decode()
        print(MarlinMessage)
        if("ok" in MarlinMessage):
            SerialBufferIsClear = True
            print("got the ok")
    sleep(15)
    RestPlateOFF()
    sleep(3)
    RestPlateON()
    ser.write('G1 E0\n'.encode())
    SerialBufferIsClear = False
    while(SerialBufferIsClear != True):
        MarlinMessage = ser.readline().decode()
        print(MarlinMessage)
        if("ok" in MarlinMessage):
            SerialBufferIsClear = True
            print("got the ok")
    ser.write('G1 Y0\n'.encode())
    SerialBufferIsClear = False
    while(SerialBufferIsClear != True):
        MarlinMessage = ser.readline().decode()
        print(MarlinMessage)
        if("ok" in MarlinMessage):
            SerialBufferIsClear = True
            print("got the ok")
    ser.write('G1 Y32 F777\n'.encode())
    SerialBufferIsClear = False
    while(SerialBufferIsClear != True):
        MarlinMessage = ser.readline().decode()
        print(MarlinMessage)
        if("ok" in MarlinMessage):
            SerialBufferIsClear = True
            print("got the ok")
    ser.write('G1 E175\n'.encode())
    SerialBufferIsClear = False
    while(SerialBufferIsClear != True):
        MarlinMessage = ser.readline().decode()
        print(MarlinMessage)
        if("ok" in MarlinMessage):
            SerialBufferIsClear = True
            print("got the ok")
    ser.write('M84\n'.encode())
    sleep(20)
    RestPlateOFF()
    print("Finished swapping devices")
    
def SystemInitialize():
    RestPlateON()
    ser.write('M302 P1\n'.encode())
    SerialBufferIsClear = False
    while(SerialBufferIsClear != True):
        MarlinMessage = ser.readline().decode()
        print(MarlinMessage)
        if("ok" in MarlinMessage):
            SerialBufferIsClear = True
            print("got the ok")

    ser.write('G28 X0 Z0\n'.encode())
    SerialBufferIsClear = False
    while(SerialBufferIsClear != True):
        MarlinMessage = ser.readline().decode()
        print(MarlinMessage)
        if("ok" in MarlinMessage):
            SerialBufferIsClear = True
            print("got the ok")
    #ser.write('G28 Z0\n'.encode())
    ser.write('G1 Y33 F777\n'.encode())
    SerialBufferIsClear = False
    while(SerialBufferIsClear != True):
        MarlinMessage = ser.readline().decode()
        print(MarlinMessage)
        if("ok" in MarlinMessage):
            SerialBufferIsClear = True
            print("got the ok")
    #ser.write('G1 Y0\n'.encode())
    ser.write('G1 E175\n'.encode())
    SerialBufferIsClear = False
    while(SerialBufferIsClear != True):
        MarlinMessage = ser.readline().decode()
        print(MarlinMessage)
        if("ok" in MarlinMessage):
            SerialBufferIsClear = True
            print("got the ok")
    ser.write('M84\n'.encode())
    SerialBufferIsClear = False
    while(SerialBufferIsClear != True):
        MarlinMessage = ser.readline().decode()
        print(MarlinMessage)
        if("ok" in MarlinMessage):
            SerialBufferIsClear = True
            print("got the ok")
    sleep(10) #buffer to prevent mistiming
    #RestPlateOFF()
    print("Finished Initialization")

def GetRawInput():
    var = input("Please enter a command:")
    print("entered: "+str(var))
    if(var=="A"):
        SwitchMUXtoA()
        return True
    if(var=="B"):
        SwitchMUXtoB()
        return True
    if(var=="C"):
        SwitchMUXtoC()
        return True
    if(var=="D"):
        SwitchMUXtoD()
        return True
    if(var=="ActON"):
        RestPlateON()
        return True
    if(var=="ActOFF"):
        print("thing worked")
        RestPlateOFF()
        return True
        
    else:
        command = str(var)+"\n"
        ser.write(command.encode())
        return False
    
#RestPlateON()
SystemInitialize()
while True:
##    data = s.recv(BUFFER_SIZE)
##    print(data.decode())
##    s.send(str.encode(MESSAGE))
##    if data.decode() == "SwitchMUXtoA":
##        SwitchMUXtoA()
##    MarlinMessage = ser.readline().decode()
##    #print(SerialBufferIsClear)
##    #print(MarlinMessage)
##    if("ok" in MarlinMessage):
##        SerialBufferIsClear = True
##        print("got the ok")
    
    print("pixel A")
    SwitchToPixelA()
    sleep(10)
    print("pixel B")
    SwitchToPixelB()
    sleep(10)
    print("pixel C")
    SwitchToPixelC()
    sleep(10)
    print("pixel D")
    SwitchToPixelD()
    sleep(10)
    SwapDevice()

##    if(SerialBufferIsClear):
##        SerialBufferIsClear = GetRawInput()