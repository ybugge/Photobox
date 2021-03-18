import time

import cv2
from PyQt5.QtCore import QThread, QSize

from Services.CfgService import CfgService
from Services.ShottedPictureService import ShottedPictureService
from config.Config import CfgKey


class CV2CapturePhotoThread(QThread):

    def __init__(self,img_dimensions : QSize):
        super().__init__()
        self.img_dimensions = img_dimensions
        self.returnValue = True
        self.shoot = False

    def run(self):
        cap = cv2.VideoCapture(CfgService.get(CfgKey.USED_CAMERA_INDEX))
        cap.set(cv2.CAP_PROP_FRAME_WIDTH, self.img_dimensions.width())
        cap.set(cv2.CAP_PROP_FRAME_HEIGHT, self.img_dimensions.height())

        while not self.shoot:
            pass
        while self.returnValue:
            ret, frame = cap.read()
            if ret:
                cv2.imwrite(ShottedPictureService.getTempPicturePath(), frame)
                self.returnValue = False

        cap.release()
        cv2.destroyAllWindows()
        time.sleep(5)

    def shootPicture(self):
        self.shoot = True
