from PyQt5.QtCore import QThread, pyqtSignal, QSize, Qt
from PyQt5.QtGui import QImage
import time
import cv2

from config.Config import cfgValue, CfgKey

try:
    from picamera import PiCamera
    from picamera.array import PiRGBArray
except ImportError:
    print("PiCamVideoThread: PiCamera not found")

class PiCamVideoThread(QThread):
    changePixmap = pyqtSignal(QImage)

    def __init__(self,img_dimensions : QSize):
        super().__init__()
        self.run = True
        self.img_dimensions = img_dimensions

    def run(self):
        camera = PiCamera()
        camera.resolution = (640, 480)
        camera.framerate = 32
        rawCapture = PiRGBArray(camera, size=(640, 480))
        time.sleep(0.1)

        for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
            if(self.run() == False):
                break
            rgbImage = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            h, w, ch = rgbImage.shape
            bytesPerLine = ch * w
            convertToQtFormat = QImage(rgbImage.data, w, h, bytesPerLine, QImage.Format_RGB888)
            p = convertToQtFormat.scaled(self.img_dimensions.width(), self.img_dimensions.height(), Qt.KeepAspectRatio)
            self.changePixmap.emit(p)
            rawCapture.truncate(0)


    def stop(self):
        self.run = False


