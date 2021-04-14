import datetime
import math
import time

import cv2
import numpy as np

from Services.CfgService import CfgService
from Services.GlobalPagesVariableService import GlobalPagesVariableService
from Services.Greenscreen.GreenscreenBackgroundService import GreenscreenBackgroundService
from config.Config import CfgKey


class GreenscreenReplaceBackgroundService():

    def __init__(self,globalVariable:GlobalPagesVariableService):
        self.globalVariable = globalVariable

    def replaceBackground(self,frame,background=None):
        if background is None:
            background = GreenscreenBackgroundService(self.globalVariable).getBackgroundAsHsv(GreenscreenBackgroundService.PICTURE_KEY,CfgService.get(CfgKey.PI_CAMERA_PHOTO_RESOLUTION))
        return self._replaceBackgroud(frame,background)

    #https://www.geeksforgeeks.org/replace-green-screen-using-opencv-python/
    def _replaceBackgroud(self,frame,backgroundHSV):
        # start = datetime.datetime.now()
        # start_time = time.time()
        # print("Greenscreen Start: "+str(start))
        resolution = [backgroundHSV.shape[1],backgroundHSV.shape[0]]
        resizeFrameHSV = cv2.cvtColor(frame,cv2.COLOR_BGR2HSV)
        resizeFrameHSV = cv2.resize(resizeFrameHSV, (resolution[0], resolution[1]))

        (hsvMinRange,hsvMaxRange) = self._getHsvRange()
        # preperation = datetime.datetime.now()
        # preperation_time = time.time()
        # print("Vorbereitung:"+str(preperation)+" "+str(preperation_time-start_time))

        # print("min")
        # print(hsvMinRange)
        # print((37,65,43))
        # print("max")
        # print(hsvMaxRange)
        # print((97,205,178))
        # print("Farbe Mitte HSV")
        # print(resizeFrameHSV[math.floor(resolution[1]/2),math.floor(resolution[0]/2)])

        mask = cv2.inRange(resizeFrameHSV, hsvMinRange, hsvMaxRange)
        res = cv2.bitwise_and(resizeFrameHSV,resizeFrameHSV,mask=mask)
        resultHsvFrame = resizeFrameHSV - res
        resultHsvFrame = np.where(resultHsvFrame == 0, backgroundHSV, resultHsvFrame)
        resultFrame = cv2.cvtColor(resultHsvFrame,cv2.COLOR_HSV2BGR)

        # end = datetime.datetime.now()
        # end_time = time.time()
        # print("Finished:"+str(end)+" "+str(end_time-start_time))
        return resultFrame

    def _getCurrentFrameRGB(self,resolution,frame):
        if resolution[1] != len(frame) or resolution[0] != len(frame[0]):
            resizeFrameRGB = cv2.resize(frame, (resolution[0], resolution[1]))
        else:
            resizeFrameRGB = frame
        return resizeFrameRGB

    def _getHsvRange(self):
        maxHsv = CfgService.getIntList(CfgKey.GREENSCREEN_MAX_HSV_CV2_COLOR)
        minHsv = CfgService.getIntList(CfgKey.GREENSCREEN_MIN_HSV_CV2_COLOR)

        return [(minHsv[0],minHsv[1],minHsv[2]),
                (maxHsv[0],maxHsv[1],maxHsv[2])]