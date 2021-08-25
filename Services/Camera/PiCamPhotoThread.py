import datetime
import io

import cv2
import numpy as np
from PyQt5.QtCore import QThread

from Services.CfgService import CfgService
from Services.GlobalPagesVariableService import GlobalPagesVariableService
from Services.Greenscreen.GreenscreenReplaceBackgroundService import GreenscreenReplaceBackgroundService
from Services.ShottedPictureService import ShottedPictureService
from config.Config import cfgValue, CfgKey

try:
    from picamera import PiCamera
    from picamera.array import PiRGBArray
    from Services.Camera.PiCameraService import PiCameraService
except ImportError:
    if cfgValue[CfgKey.IS_PI]:
        print("PiCamPhotoThread: PiCamera not found")

class PiCamPhotoThread(QThread):

    def __init__(self,globalVariable:GlobalPagesVariableService,background = None):
        super().__init__()
        self.background = background

        self.globalVariable = globalVariable
        self.returnValue = True
        self.shoot = False

    def run(self):
        self.piCamWithCv2_test()
        #self.plainPiCam()
        self.returnValue = False

    # not used
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

    # not used
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

    #https://picamera.readthedocs.io/en/release-1.10/recipes1.html
    def piCamWithCv2_test(self):
        resolution = CfgService.get(CfgKey.PI_CAMERA_PHOTO_RESOLUTION)
        stream = io.BytesIO()
        with PiCamera() as camera:
            camera.resolution = resolution
            PiCameraService.setupCameraStaticBrightness(camera)
            camera.capture(stream, format='jpeg')
        # Construct a numpy array from the stream
        data = np.fromstring(stream.getvalue(), dtype=np.uint8)
        frame = cv2.imdecode(data, 1)
        if not self.background is None:
            frame = GreenscreenReplaceBackgroundService(self.globalVariable).replaceBackground(frame,self.background)

        cv2.imwrite(ShottedPictureService.getTempPicturePath(), frame)
        cv2.destroyAllWindows()

    def shootPicture(self):
        self.shoot = True