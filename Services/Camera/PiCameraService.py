from time import sleep

from config.Config import cfgValue, CfgKey

try:
    from picamera import PiCamera
except ImportError:
    if cfgValue[CfgKey.IS_PI]:
        print("CameraService: PiCamera not found")


class PiCameraService():

    @staticmethod
    def setupCameraStaticBrightness(camera:PiCamera):
        if cfgValue[CfgKey.PI_CAMERA_STATIC_BRIGHTNESS]:
            #https://picamera.readthedocs.io/en/release-1.13/recipes1.html
            #https://picamera.readthedocs.io/en/release-1.10/api_camera.html
            #https://github.com/waveform80/picamera/issues/581
            camera.shutter_speed = camera.exposure_speed
            camera.exposure_mode = 'off'
            camera.awb_mode = 'off'
            camera.awb_gains = cfgValue[CfgKey.PI_CAMERA_STATIC_BRIGHTNESS_AWB_GAINS]
            sleep(0.1)