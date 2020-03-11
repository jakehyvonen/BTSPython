#!/usr/bin/env python

import time
import serial

ser = serial.Serial(
    
    port="/dev/ttyACM0",
    baudrate=250000,
    parity=serial.PARITY_NONE,
    stopbits=serial.STOPBITS_ONE,
    bytesize=serial.EIGHTBITS,
    dsrdtr=False,
    rtscts=False,
    timeout=1
    )
ser.get_settings()
ser.readline()
while True:
    command='G1 Z13 F333\n'
    ser.write(command.encode())
    time.sleep(1)
    s = ser.readline()
    print(s.decode())
    