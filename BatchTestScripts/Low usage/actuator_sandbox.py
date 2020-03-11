from gpiozero import LED
from time import sleep

led1 = LED(27) #led1+2 = device rest plate
led2 = LED(22)
#led3 = LED(6) #led3+4+5+6 = compressor plate
#led4 = LED(13)
#led5 = LED(19)
#led6 = LED(26)

while True:
    led2.on()
    led1.on()
    sleep(4)
    #led3.on()
    #led5.on()
    #sleep(0.05)
    #led4.on()
    #led6.on()
    #sleep(4)
    #led3.off()
    #led4.off()
    #led5.off()
    #led6.off()
    #sleep(1)
    
    led1.off()
    led2.off()
    sleep(1)
    