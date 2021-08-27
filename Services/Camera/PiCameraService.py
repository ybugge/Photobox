from time import sleep

from Services.CfgService import CfgService
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
            camera.brightness = CfgService.get(CfgKey.PI_CAMERA_STATIC_BRIGHTNESS_STATIC_VALUE)
            camera.iso = 100
            sleep(0.1)
            camera.shutter_speed = camera.exposure_speed
            camera.exposure_mode = 'off'
            camera.awb_mode = 'off'
            camera.awb_gains = (CfgService.get(CfgKey.PI_CAMERA_STATIC_BRIGHTNESS_AWB_GAIN_RED),CfgService.get(CfgKey.PI_CAMERA_STATIC_BRIGHTNESS_AWB_GAIN_BLUE))
            sleep(0.1)