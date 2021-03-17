from PyQt5.QtCore import QSize
from PyQt5.QtMultimedia import QCameraInfo

from Services.Camera.CV2CapturePhotoThread import CV2CapturePhotoThread
from Services.Camera.CV2VideoThread import CV2VideoThread
from Services.Camera.PiCamPhotoThread import PiCamPhotoThread
from Services.Camera.PiCamVideoThread import PiCamVideoThread
from Services.CfgService import CfgService
from config.Config import cfgValue, CfgKey

try:
    from picamera import PiCamera
except ImportError:
    if cfgValue[CfgKey.IS_PI]:
        print("CameraService: PiCamera not found")

class CameraService():

    @staticmethod
    def existPiCamera():
        if cfgValue[CfgKey.USE_PI_CAMERA] == None:
            if cfgValue[CfgKey.IS_PI]:
                try:
                    camera = PiCamera()
                    camera.close()
                    cfgValue[CfgKey.USE_PI_CAMERA] = True
                except Exception as e:
                    print(e)
                    cfgValue[CfgKey.USE_PI_CAMERA] =  False
            else:
                cfgValue[CfgKey.USE_PI_CAMERA] =  False
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
            return PiCamPhotoThread(windowSize)
        else:
            return CV2CapturePhotoThread(windowSize)
