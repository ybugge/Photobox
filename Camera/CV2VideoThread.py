import cv2
from PyQt5.QtCore import QThread, pyqtSignal, Qt, QSize
from PyQt5.QtGui import QImage

from config.Config import CfgKey, cfgValue


class CV2VideoThread(QThread):
    changePixmap = pyqtSignal(QImage)

    def __init__(self,img_dimensions : QSize):
        super().__init__()
        self.run = True
        self.img_dimensions = img_dimensions

    def run(self):
        cap = cv2.VideoCapture(cfgValue[CfgKey.USED_CAMERA_INDEX])
        cap.set(cv2.CAP_PROP_FRAME_WIDTH, self.img_dimensions.width())
        cap.set(cv2.CAP_PROP_FRAME_HEIGHT, self.img_dimensions.height())
        while self.run:
            ret, frame = cap.read()
            if ret:
                rgbImage = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
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