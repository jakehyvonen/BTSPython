from gpiozero import LED
from time import sleep

#using Sunfounder 5V relays (need to convert 3.3V logic signal to 5V for this to work
led1 = LED(19)
led2 = LED(13) 
led3 = LED(6) 
led4 = LED(5) 
led5 = LED(27) #led5+6 = device rest plate
led6 = LED(22)
#on and off are backward for no apparent reason.
while True:
    #turn on switch 1
    led1.off()
    led2.on()
    led3.on()
    led4.on()
    led5.on()
    led6.on()
    sleep(4)
    #turn on switch 2
    led1.on()
    led2.off()
    led3.on()
    led4.on()
    led5.on()
    led6.on()
    sleep(4)
    #turn on switch 3
    led1.on()
    led2.on()
    led3.off()
    led4.on()
    led5.on()
    led6.on()
    sleep(4)
    #turn on switch 4
    led1.on()
    led2.on()
    led3.on()
    led4.off()
    led5.on()
    led6.on()
    sleep(4)
    #turn on switch 5+6
    led1.on()
    led2.on()
    led3.on()
    led4.on()
    led5.off()
    led6.off()
    sleep(4)