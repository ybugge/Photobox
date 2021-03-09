import cv2
from PyQt5.QtCore import QThread, QSize

from config.Config import CfgKey, cfgValue


class CV2CapturePhoto(QThread):

    def __init__(self,img_dimensions : QSize, fileName:str):
        super().__init__()
        self.img_dimensions = img_dimensions
        self.fileName = fileName
        self.returnValue = True

    def run(self):
        cap = cv2.VideoCapture(cfgValue[CfgKey.USED_CAMERA_INDEX])
        cap.set(cv2.CAP_PROP_FRAME_WIDTH, self.img_dimensions.width())
        cap.set(cv2.CAP_PROP_FRAME_HEIGHT, self.img_dimensions.height())

        while self.returnValue:
            ret, frame = cap.read()
            if ret:
                cv2.imwrite(self.fileName, frame)
                print("Bild gespeichert: "+self.fileName)
                self.returnValue = False

        cap.release()
        cv2.destroyAllWindows()

    def stop(self):
        self.returnValue=False