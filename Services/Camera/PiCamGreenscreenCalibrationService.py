import io

import cv2
import numpy as np
from PyQt5.QtCore import QSize, Qt
from PyQt5.QtGui import QImage

from Services.CfgService import CfgService
from config.Config import CfgKey, cfgValue

try:
    from picamera import PiCamera
    from picamera.array import PiRGBArray
except ImportError:
    if cfgValue[CfgKey.IS_PI]:
        print("PiCamPhotoThread: PiCamera not found")

class PiCamGreenscreenCalibrationService():

    def __init__(self,img_dimensions : QSize):
        self.img_dimensions = img_dimensions

    def getImage(self):
        resolution = CfgService.get(CfgKey.PI_CAMERA_PHOTO_RESOLUTION)
        stream = io.BytesIO()
        with PiCamera() as camera:
            camera.resolution = resolution
            camera.capture(stream, format='jpeg')
        # Construct a numpy array from the stream
        data = np.fromstring(stream.getvalue(), dtype=np.uint8)
        frame = cv2.imdecode(data, 1)
        rgbImage = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        hsvImage = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        h, w, ch = rgbImage.shape
        bytesPerLine = ch * w
        origImageRGB = QImage(rgbImage.data, w, h, bytesPerLine, QImage.Format_RGB888)
        prewiewImage = origImageRGB.scaled(self.img_dimensions.width(), self.img_dimensions.height(), Qt.KeepAspectRatio)
        cv2.destroyAllWindows()
        return (hsvImage,prewiewImage)

