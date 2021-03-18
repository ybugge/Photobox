import time

import cv2
from PyQt5.QtCore import QThread, QSize

from Services.CfgService import CfgService
from Services.ShottedPictureService import ShottedPictureService
from config.Config import cfgValue, CfgKey

try:
    from picamera import PiCamera
    from picamera.array import PiRGBArray
except ImportError:
    if cfgValue[CfgKey.IS_PI]:
        print("PiCamPhotoThread: PiCamera not found")

class PiCamPhotoThread(QThread):

    def __init__(self,img_dimensions : QSize):
        super().__init__()
        self.img_dimensions = img_dimensions
        self.returnValue = True

    def run(self):
        self.plainPiCam()
        self.returnValue = False

    def plainPiCam(self):
        resolution = CfgService.get(CfgKey.PI_CAMERA_PHOTO_RESOLUTION)
        camera = PiCamera()
        camera.resolution = resolution
        camera.framerate = 30
        camera.capture(ShottedPictureService.getTempPicturePath(),'png')
        camera.close()

    def piCamWithCv2(self):
        resolution = CfgService.get(CfgKey.PI_CAMERA_PHOTO_RESOLUTION)
        camera = PiCamera()
        camera.resolution = resolution
        camera.framerate = 30
        rawCapture = PiRGBArray(camera, size=camera.resolution)
        #time.sleep(0.1)
        camera.capture(rawCapture, format="rgb")
        image = rawCapture.array
        cv2.imwrite(ShottedPictureService.getTempPicturePath(), image)

        camera.close()
        cv2.destroyAllWindows()


    def stop(self):
        pass