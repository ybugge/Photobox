import math

import cv2
from PyQt5.QtCore import QThread, pyqtSignal, Qt, QSize
from PyQt5.QtGui import QImage

from Services.CfgService import CfgService
from Services.GlobalPagesVariableService import GlobalPagesVariableService
from Services.Greenscreen.GreenscreenReplaceBackgroundService import GreenscreenReplaceBackgroundService
from config.Config import CfgKey


class CV2VideoThread(QThread):
    changePixmap = pyqtSignal(QImage)
    pixelHsv = pyqtSignal(list)

    def __init__(self,img_dimensions:QSize,globalVariable : GlobalPagesVariableService, background = None):
        super().__init__()
        self.background = background
        self.run = True
        self.img_dimensions = img_dimensions
        self.globalVariable = globalVariable

    def run(self):
        cap = cv2.VideoCapture(CfgService.get(CfgKey.USED_CAMERA_INDEX))
        cap.set(cv2.CAP_PROP_FRAME_WIDTH, self.img_dimensions.width())
        cap.set(cv2.CAP_PROP_FRAME_HEIGHT, self.img_dimensions.height())
        while self.run:
            ret, frame = cap.read()
            if ret:
                self.updatePixel(frame)
                if not self.background is None:
                    frame = GreenscreenReplaceBackgroundService(self.globalVariable).replaceBackground(frame,self.background)
                rgbImage = cv2.flip(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB),1)
                h, w, ch = rgbImage.shape
                bytesPerLine = ch * w
                convertToQtFormat = QImage(rgbImage.data, w, h, bytesPerLine, QImage.Format_RGB888)
                p = convertToQtFormat.scaled(self.img_dimensions.width(), self.img_dimensions.height(), Qt.KeepAspectRatio)
                self.changePixmap.emit(p)
        self.changePixmap.emit(QImage())
        cap.release()
        cv2.destroyAllWindows()

    def stop(self):
        self.run = False

    def updatePixel(self,frame):
        hsvFrame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        h,w,_ = hsvFrame.shape
        hsv = hsvFrame[math.floor(h/2),math.floor(w/2)]
        self.pixelHsv.emit([hsv[0],hsv[1],hsv[2]])
