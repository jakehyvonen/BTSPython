import serial
from time import sleep

print('starting serial test')
ser = serial.Serial(
    port ="/dev/ttyACM0",
    baudrate=115200,
    parity=serial.PARITY_NONE,
    stopbits=serial.STOPBITS_ONE,
    bytesize=serial.EIGHTBITS,
    dsrdtr=True,
    rtscts=True,
    timeout=None
    )
ser.reset_input_buffer()
ser.reset_output_buffer()
ser.write('P'.encode())
ser.write('H'.encode())
ser.write('O'.encode())
ser.write('T'.encode())
ser.write('O'.encode())
ser.write('\n'.encode())
print('init response: ' + ser.read_until('MODE'.encode()).decode())
sleep(1)
ser.write('M'.encode())
ser.write('1'.encode())
ser.write('\n'.encode())
#sleep(13)
#print('M1 response: ' + ser.readline().decode())
print('M1 response: ' + ser.read_until('\r\n'.encode()).decode())
ser.flush()
ser.close()
print('finished')