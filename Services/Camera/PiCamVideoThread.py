import math

from PyQt5.QtCore import QThread, pyqtSignal, QSize, Qt
from PyQt5.QtGui import QImage
import time
import cv2

from Services.CfgService import CfgService
from Services.GlobalPagesVariableService import GlobalPagesVariableService
from Services.Greenscreen.GreenscreenReplaceBackgroundService import GreenscreenReplaceBackgroundService
from config.Config import cfgValue, CfgKey

try:
    from picamera import PiCamera
    from picamera.array import PiRGBArray
    from Services.Camera.PiCameraService import PiCameraService
except ImportError:
    if cfgValue[CfgKey.IS_PI]:
        print("PiCamVideoThread: PiCamera not found")

class PiCamVideoThread(QThread):
    changePixmap = pyqtSignal(QImage)
    pixelHsv = pyqtSignal(list)

    def __init__(self,img_dimensions:QSize,globalVariable : GlobalPagesVariableService, background):
        super().__init__()
        self.run = True
        self.background = background
        self.img_dimensions = img_dimensions
        self.globalVariable = globalVariable

    def run(self):
        resolution = CfgService.get(CfgKey.PI_CAMERA_VIDEO_RESOLUTION)
        camera = PiCamera()
        camera.resolution =  resolution
        PiCameraService.setupCameraStaticBrightness(camera)
        camera.framerate = CfgService.get(CfgKey.PI_CAMERA_VIDEO_FPS)
        rawCapture = PiRGBArray(camera, size=resolution)
        time.sleep(0.1)

        for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
            if(self.run == False):
                break
            frameArray = frame.array
            self.updatePixel(frame.array)
            if not self.background is None:
                frameArray = GreenscreenReplaceBackgroundService(self.globalVariable).replaceBackground(frameArray,self.background)
            rgbImage = cv2.flip(cv2.cvtColor(frameArray, cv2.COLOR_BGR2RGB),1)
            h, w, ch = rgbImage.shape
            bytesPerLine = ch * w
            convertToQtFormat = QImage(rgbImage.data, w, h, bytesPerLine, QImage.Format_RGB888)
            p = convertToQtFormat.scaled(self.img_dimensions.width(), self.img_dimensions.height(), Qt.KeepAspectRatio)
            self.changePixmap.emit(p)
            rawCapture.truncate(0)
        camera.close()
        cv2.destroyAllWindows()

    def stop(self):
        self.run = False

    def updatePixel(self,frame):
        hsvFrame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        h,w,_ = hsvFrame.shape
        hsv = hsvFrame[math.floor(h/2),math.floor(w/2)]
        self.pixelHsv.emit([hsv[0],hsv[1],hsv[2]])

