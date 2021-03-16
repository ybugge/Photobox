from PyQt5.QtCore import QSize
from PyQt5.QtMultimedia import QCameraInfo

from Services.Camera.CV2CapturePhotoThread import CV2CapturePhotoThread
from Services.Camera.CV2VideoThread import CV2VideoThread
from Services.Camera.PiCamVideoThread import PiCamVideoThread
from Services.CfgService import CfgService
from config.Config import cfgValue, CfgKey

try:
    print("Import Pi Camaer")
    from picamera import PiCamera
    print("Import Pi Camaer Success")
except ImportError:
    print("CameraService: PiCamera not found")

class CameraService():

    @staticmethod
    def existPiCamera():
        if cfgValue[CfgKey.USE_PI_CAMERA] == None:
            if cfgValue[CfgKey.IS_PI]:
                try:
                    print("Start")
                    camera = PiCamera()
                    print("Erfolgreich 1")
                    camera.close()
                    print("Erfolgreich 2")
                    cfgValue[CfgKey.USE_PI_CAMERA] = True
                except Exception as e:
                    print(e)
                    print("FEHLER")
                    cfgValue[CfgKey.USE_PI_CAMERA] =  False
            cfgValue[CfgKey.USE_PI_CAMERA] =  False
        print("WERT:" + str(cfgValue[CfgKey.USE_PI_CAMERA]))
        return cfgValue[CfgKey.USE_PI_CAMERA]

    #https://www.geeksforgeeks.org/creating-a-camera-application-using-pyqt5/
    @staticmethod
    def existCameras():
        camerasInfos = QCameraInfo.availableCameras()
        return len(camerasInfos) > 0

    @staticmethod
    def existSelectedCamera():
        camerasInfos = QCameraInfo.availableCameras()
        return len(camerasInfos) > CfgService.get(CfgKey.USED_CAMERA_INDEX)

    @staticmethod
    def getCameraIndex():
        return CfgService.get(CfgKey.USED_CAMERA_INDEX)

    @staticmethod
    def getCameraName():
        camerasInfos = QCameraInfo.availableCameras()
        cameraIndex = CameraService.getCameraIndex()
        return camerasInfos[cameraIndex].deviceName()

    @staticmethod
    def getCameraDescription():
        camerasInfos = QCameraInfo.availableCameras()
        cameraIndex = CameraService.getCameraIndex()
        return camerasInfos[cameraIndex].description()

    @staticmethod
    def initialAndStartVideo(windowSize:QSize, setVideoStreamToLabel):
        if CameraService.existPiCamera():
            t_videoThread = PiCamVideoThread(windowSize)
            t_videoThread.changePixmap.connect(setVideoStreamToLabel)
            t_videoThread.start()
            return t_videoThread
        else:
            t_videoThread = CV2VideoThread(windowSize)
            t_videoThread.changePixmap.connect(setVideoStreamToLabel)
            t_videoThread.start()
            return t_videoThread

    @staticmethod
    def initialPhoto(windowSize:QSize):
        if CameraService.existPiCamera():
            pass
        else:
            return CV2CapturePhotoThread(windowSize)
