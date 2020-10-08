'''
Created on 06.10.2020

@author: ybugge
'''
print("Hallo")

from picamera import PiCamera
from time import sleep

camera = PiCamera()

camera.start_preview()
sleep(10)
camera.stop_preview()