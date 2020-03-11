from gpiozero import LED
from time import sleep
import socket
import serial

#low level IC control pins
#using Sunfounder 5V relays
led1 = LED(19)
led2 = LED(13) 
led3 = LED(6) 
led4 = LED(5) 
led5 = LED(27) #led5+6 = device rest plate
led6 = LED(22)

###setup communication with C# software

TCP_PORT = 5005
BUFFER_SIZE = 1024
serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host = ''
serversocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
serversocket.bind((host,TCP_PORT))
serversocket.listen(1)

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

def SwitchToPixelA():
    SwitchMUXtoA()
    ser.write('G1 X5.6 Z3.6\n'.encode())
    
def SwitchToPixelB():
    SwitchMUXtoB()
    ser.write('G1 X0.3 Z5.6\n'.encode())
    
def SwitchToPixelC():
    SwitchMUXtoC()
    ser.write('G1 X2.3 Z11\n'.encode())
    
def SwitchToPixelD():
    SwitchMUXtoD()
    ser.write('G1 X7.7 Z8.9\n'.encode())



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

def GetRawInput():
    var = input("Please enter a command:")
    print("entered: "+str(var))
    if(var=="A"):
        SwitchMUXtoA()
        return True
    if(var=="PixelA"):
        SwitchToPixelA()
        return True
    if(var=="B"):
        SwitchMUXtoB()
        return True
    if(var=="PixelB"):
        SwitchToPixelB()
        return True
    if(var=="C"):
        SwitchMUXtoC()
        return True
    if(var=="PixelC"):
        SwitchToPixelC()
        return True
    if(var=="D"):
        SwitchMUXtoD()
        return True
    if(var=="PixelD"):
        SwitchToPixelD()
        return True
    if(var=="ActON"):
        RestPlateON()
        return True
    if(var=="ActOFF"):
        RestPlateOFF()
        return True
    if(var=="Return"):
        ReturnToStartPositions()
    if(var=="Initialize"):
        SystemInitialize()
    if(var=="Swap"):
        SwapDevice()
        return True
        
    else:
        command = str(var)+"\n"
        ser.write(command.encode())
        WaitForOk()
    
#RestPlateON()
#SystemInitialize()
while True:
    GetRawInput()
##    conn, address = serversocket.accept()
##    print ("Connection address:", address)
##    data = conn.recv(BUFFER_SIZE)
##    print ('received data:', data.decode())
##    conn.close
##    command = data.decode()
##    if(command=="Initialize"):
##        SystemInitialize()
##    if(command=="PixelA"):
##        SwitchToPixelA()
##    if(command=="PixelB"):
##        SwitchToPixelB()
##    if(command=="PixelC"):
##        SwitchToPixelC()
##    if(command=="PixelD"):
##        SwitchToPixelD()
##    if(command=="Swap"):
##        SwapDevice()
##    if(command=="Return"):
##        ReturnToStartPositions()

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

    
    