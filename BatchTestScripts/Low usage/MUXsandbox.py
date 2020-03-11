from gpiozero import LED
from time import sleep

#low level IC control pins
led1 = LED(13) #A0 pin
led2 = LED(6) #A1 pin
led3 = LED(5) #A2 pin
led4 = LED(27) #led4+5 = device rest plate
led5 = LED(22)



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

SwitchMUXtoD()