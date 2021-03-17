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
        resolution = (4056,3040)#CfgService.get(CfgKey.PI_CAMERA_PHOTO_RESOLUTION)
        camera = PiCamera()
        camera.resolution = resolution
        rawCapture = PiRGBArray(camera, size=resolution)
        time.sleep(2)
        camera.capture(rawCapture, format="bgr")
        image = rawCapture.array
        cv2.imwrite(ShottedPictureService.getTempPicturePath(), image)

        camera.close()
        cv2.destroyAllWindows()
        self.returnValue = False

    def stop(self):
        pass