import datetime
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
        self.shoot = False

    def run(self):
        self.piCamWithCv2_test()
        #self.plainPiCam()
        self.returnValue = False

    def plainPiCam(self):
        resolution = CfgService.get(CfgKey.PI_CAMERA_PHOTO_RESOLUTION)
        camera = PiCamera()
        camera.resolution = resolution
        camera.framerate = 30
        while not self.shoot:
            pass
        print("Befor capture: "+str(datetime.datetime.now()))
        camera.capture(ShottedPictureService.getTempPicturePath(),'png')
        print("After capture: "+str(datetime.datetime.now()))
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

    def piCamWithCv2_test(self):
        resolution = CfgService.get(CfgKey.PI_CAMERA_PHOTO_RESOLUTION)
        camera = PiCamera()
        camera.resolution = resolution
        #camera.framerate = 15
        rawCapture = PiRGBArray(camera)
        time.sleep(2)
        camera.capture(rawCapture, format="bgr")
        image = rawCapture.array[:, :, ::-1]
        cv2.imwrite(ShottedPictureService.getTempPicturePath(), image)
        cv2.destroyAllWindows()
        camera.close()

    def shootPicture(self):
        self.shoot = True