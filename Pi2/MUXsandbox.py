from time import sleep
from picamera import PiCamera


camera = PiCamera()
camera.resolution = (1024,768)
camera.start_preview()
sleep(2)
camera.capture('/home/pi/Pictures/foo.jpg')
camera.stop_preview()
                                                                                                                                                                                                                                                                                              