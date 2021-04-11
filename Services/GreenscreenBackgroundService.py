import datetime
import math
import os
import time

import cv2
import numpy as np
from PIL import Image
from PyQt5.QtCore import QSize
from PyQt5.QtGui import QColor

from Services.CfgService import CfgService
from Services.FileFolderService import FileFolderService
from Services.GlobalPagesVariableService import GlobalPagesVariableService
from config.Config import CfgKey

class GreenscreenBackgroundService():

    def __init__(self,globalVariable:GlobalPagesVariableService):
        self.globalVariable = globalVariable
        self.PICTURE_KEY = "picture"
        self.VIDEO_KEY = "video"
        self.PICTURE_PATH_KEY = "path"

    def loadDefaultBackgrounds(self):
        # Bilder aus Ordner laden
        folderPath = self._getDefultBackgroundPathCreateFolderIfNotExtist()
        picturePaths = FileFolderService.getFolderContentPictures(folderPath)
        backgrounds = []
        for picturePath in picturePaths:
            backgrounds.append(self._loadBackgroundImages(picturePath))
        self.globalVariable.setDefaultBackground(backgrounds)

    def setIndex(self,index:int):
        self.globalVariable.setBackgroundIndex(index)

    def getIndex(self):
        return self.globalVariable.getBackgroundIndex()

    def getBackgroundSize(self):
        return len(self._getBackgrounds())

    def getPreviewImageAsQPixmap(self,index,size:QSize):
        if index >= self.getBackgroundSize():
            return None
        else:
            return self._getBackgrounds()[index][self.PICTURE_PATH_KEY]

    def _cutPicture(self,picturePath,targetResolution):
        picture = Image.open(picturePath)
        picture.load()
        pictureSize = picture.size
        newPictureRationSize = self._getNewPictureRatio(pictureSize,targetResolution)

        top = math.floor((pictureSize[1]-newPictureRationSize[1]) / 2)
        bottom = top+newPictureRationSize[1]
        left = math.floor((pictureSize[0]-newPictureRationSize[0]) / 2)
        right = left+newPictureRationSize[0]
        oldRGBPicture = Image.new("RGB", pictureSize, (255, 255, 255))
        oldRGBPicture.paste(picture)
        return oldRGBPicture.crop((left, top, right, bottom))

    def _getNewPictureRatio(self,pictureSize,targetResolution): #(1280,720)
        newPictureSizeWidth = (targetResolution[0]*pictureSize[1])/targetResolution[1]
        if newPictureSizeWidth > pictureSize[0]:
            newPictureSizeHight = (targetResolution[1]*pictureSize[0])/targetResolution[0]
            return (pictureSize[0],math.floor(newPictureSizeHight))
        else:
            return (math.floor(newPictureSizeWidth),pictureSize[1])


    def _getDefultBackgroundPathCreateFolderIfNotExtist(self):
        folder = self._getDefaultBackgroundPath()
        FileFolderService.createFolderIfNotExist(folder)
        return folder

    def _getDefaultBackgroundPath(self):
        return os.path.join(CfgService.get(CfgKey.MAIN_SAVE_DIR), CfgService.get(CfgKey.PROJECTNAME), CfgService.get(CfgKey.GREENSCREEN_DEFAULT_BACKGROUND_FOLDER))

    def replaceBackgroundPhoto(self,frame):
        return self._replaceBackgroud(frame,self.PICTURE_KEY,CfgService.get(CfgKey.PI_CAMERA_PHOTO_RESOLUTION))

    #https://www.geeksforgeeks.org/replace-green-screen-using-opencv-python/
    def _replaceBackgroud(self,frame,backroundKey:str,resolution):
        start = datetime.datetime.now()
        start_time = time.time()
        print("Greenscreen Start: "+str(start))
        background = self._getUsedBackground(backroundKey,resolution)
        backgroundHSV = cv2.cvtColor(np.array(background),cv2.COLOR_BGR2HSV)
        resizeFrameRGB = self._getCurrentFrameRGB(resolution,frame)
        resizeFrameHSV = cv2.cvtColor(resizeFrameRGB,cv2.COLOR_RGB2HSV)
        (hsvMinRange,hsvMaxRange) = self._getHsvRange()
        preperation = datetime.datetime.now()
        preperation_time = time.time()
        print("Vorbereitung:"+str(preperation)+" "+str(preperation_time-start_time))

        # for x  in range(resolution[0]):
        #      for y in range(resolution[1]):
        #          pixelColorHSV = resizeFrameHSV[y,x]
        #          pixelColorHSVAsInt = pixelColorHSV[0]*1000000+pixelColorHSV[1]*1000+pixelColorHSV[2]
        #          if not (hsvMinRange > pixelColorHSVAsInt > hsvMaxRange):
        #              backgroundHSV[y,x] = pixelColorHSV
        #resultFrame = cv2.cvtColor(backgroundHSV,cv2.COLOR_HSV2RGB)
        print("min")
        print(hsvMinRange)
        print((37,65,43))
        print("max")
        print(hsvMaxRange)
        print((97,205,178))
        print("Farbe Mitte HSV")
        print(resizeFrameHSV[math.floor(resolution[1]/2),math.floor(resolution[0]/2)])
        mask = cv2.inRange(resizeFrameHSV, hsvMinRange, hsvMaxRange)
        res = cv2.bitwise_and(resizeFrameHSV,resizeFrameHSV,mask=mask)
        resultHsvFrame = resizeFrameHSV - res
        resultHsvFrame = np.where(resultHsvFrame == 0, backgroundHSV, resultHsvFrame)

        resultFrame = cv2.cvtColor(resultHsvFrame,cv2.COLOR_HSV2RGB)
        end = datetime.datetime.now()
        end_time = time.time()
        print("Finished:"+str(end)+" "+str(end_time-start_time))
        return resultFrame

    def _getUsedBackground(self,backroundKey:str,resolution):
        index = self.getIndex()
        return self.globalVariable.getDefaultBackground()[index][backroundKey].resize((resolution[0],resolution[1]))

    def _getCurrentFrameRGB(self,resolution,frame):
        if resolution[1] != len(frame) or resolution[0] != len(frame[0]):
            resizeFrameRGB = cv2.resize(frame, (resolution[0], resolution[1]))
        else:
            resizeFrameRGB = frame
        return resizeFrameRGB


    def _getHsvRange(self):
        maxHsv = CfgService.getIntList(CfgKey.GREENSCREEN_MAX_HSV_COLOR_WITHOUT_TOLERANCE)
        minHsv = CfgService.getIntList(CfgKey.GREENSCREEN_MIN_HSV_COLOR_WITHOUT_TOLERANCE)
        addToMax = CfgService.getIntList(CfgKey.GREENSCREEN_COLOR_TOLERANCE_POS)
        addToMin = CfgService.getIntList(CfgKey.GREENSCREEN_COLOR_TOLERANCE_NEG)
        for id, amount in enumerate(addToMax):
            maxHsv[id] += amount

        for id, amount in enumerate(addToMin):
            minHsv[id] += amount
        return [GreenscreenBackgroundService._addHsvAndConvertToCv2(minHsv,addToMin),
                GreenscreenBackgroundService._addHsvAndConvertToCv2(maxHsv,addToMax)]

    @staticmethod
    def _addHsvAndConvertToCv2(value,value2):
        h = (value[0] + value2[0])/2
        if h < 0:
            h = 0
        elif h > 179:
            h = 179
        s = (value[1] + value2[1])
        if s < 0:
            s = 0
        elif s > 255:
            s = 255
        v = (value[2] + value2[2])
        if s < 0:
            s = 0
        elif s > 255:
            s = 255
        qColorRGB = QColor.fromHsv(h,s,v,255).getRgb()

        blank_image = np.zeros((1,1,3), np.uint8)
        blank_image[0][0] = (qColorRGB[0],qColorRGB[1],qColorRGB[2])
        return cv2.cvtColor(blank_image,cv2.COLOR_RGB2HSV)[0][0]


    def _getBackgrounds(self):
        return self.globalVariable.getDefaultBackground()

    def _loadBackgroundImages(self,picturePath):
        videoBackground = self._cutPicture(picturePath,CfgService.get(CfgKey.PI_CAMERA_VIDEO_RESOLUTION))
        pictureBackground = self._cutPicture(picturePath,CfgService.get(CfgKey.PI_CAMERA_PHOTO_RESOLUTION))
        return {self.PICTURE_PATH_KEY:picturePath,self.VIDEO_KEY:videoBackground,self.PICTURE_KEY:pictureBackground}