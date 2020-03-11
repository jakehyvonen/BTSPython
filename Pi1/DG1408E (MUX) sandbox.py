from gpiozero import LED
from time import sleep

led1 = LED(13) #A0 pin
led2 = LED(6) #A1 pin
led3 = LED(5) #A2 pin

while True:
    #turn on switch 1
    led1.off()
    led2.off()
    led3.off()
    sleep(4)
    #turn on switch 2
    led1.on()
    led2.off()
    led3.off()
    sleep(4)
    #turn on switch 3
    led1.off()
    led2.on()
    led3.off()
    sleep(4)
    #turn on switch 4
    led1.on()
    led2.on()
    led3.off()
    sleep(4)