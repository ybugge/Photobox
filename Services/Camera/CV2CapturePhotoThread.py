import cv2
from PyQt5.QtCore import QThread, QSize

from Services.CfgService import CfgService
from Services.GlobalPagesVariableService import GlobalPagesVariableService
from Services.GreenscreenBackgroundService import GreenscreenBackgroundService
from Services.ShottedPictureService import ShottedPictureService
from config.Config import CfgKey


class CV2CapturePhotoThread(QThread):

    def __init__(self,globalVariable:GlobalPagesVariableService):
        super().__init__()
        self.globalVariable = globalVariable
        self.returnValue = True
        self.shoot = False

    def run(self):
        greenscreenService = GreenscreenBackgroundService(self.globalVariable)
        cap = cv2.VideoCapture(CfgService.get(CfgKey.USED_CAMERA_INDEX))
        cap.set(cv2.CAP_PROP_FRAME_WIDTH, CfgService.get(CfgKey.PI_CAMERA_PHOTO_RESOLUTION)[0])
        cap.set(cv2.CAP_PROP_FRAME_HEIGHT, CfgService.get(CfgKey.PI_CAMERA_PHOTO_RESOLUTION)[1])

        while not self.shoot:
            pass
        while self.returnValue:
            ret, frame = cap.read()
            if ret:
                if CfgService.get(CfgKey.GREENSCREEN_IS_ACTIVE):
                    newFrame = greenscreenService.replaceBackgroundPhoto(frame)
                    cv2.imwrite(ShottedPictureService.getTempPicturePath(), newFrame)
                else:
                    cv2.imwrite(ShottedPictureService.getTempPicturePath(), frame)
                self.returnValue = False

        cap.release()
        cv2.destroyAllWindows()

    def shootPicture(self):
        self.shoot = True
