import cv2
from PyQt5.QtCore import QSize, Qt
from PyQt5.QtGui import QImage

from Services.CfgService import CfgService
from config.Config import CfgKey


class CV2GreenscreenCalibrationService():

    def __init__(self,img_dimensions : QSize):
        self.img_dimensions = img_dimensions

    def getImage(self):
        cap = cv2.VideoCapture(CfgService.get(CfgKey.USED_CAMERA_INDEX))
        cap.set(cv2.CAP_PROP_FRAME_WIDTH, self.img_dimensions.width())
        cap.set(cv2.CAP_PROP_FRAME_HEIGHT, self.img_dimensions.height())
        finished = True
        origImageRGB = None
        prewiewImage = None

        while finished:
            ret, frame = cap.read()
            if ret:
                rgbImage = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                hsvImage = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
                h, w, ch = rgbImage.shape
                bytesPerLine = ch * w
                origImageRGB = QImage(rgbImage.data, w, h, bytesPerLine, QImage.Format_RGB888)
                prewiewImage = origImageRGB.scaled(self.img_dimensions.width(), self.img_dimensions.height(), Qt.KeepAspectRatio)
                finished = False
        cap.release()
        cv2.destroyAllWindows()
        return (hsvImage,prewiewImage)
