import datetime
import math
import os

import cv2
import numpy as np
from PIL import Image
from PyQt5.QtCore import QSize

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

    def _replaceBackgroud(self,frame,backroundKey:str,resolution):
        background = self._getUsedBackground(backroundKey,resolution)
        backgroundHSV = cv2.cvtColor(np.array(background),cv2.COLOR_BGR2HSV)
        resizeFrameRGB = self._getCurrentFrameRGB(resolution,frame)
        resizeFrameHSV = cv2.cvtColor(resizeFrameRGB,cv2.COLOR_RGB2HSV)
        hsvMinMaxRange = self._getHsvRange()

        for x  in range(resolution[0]):
             for y in range(resolution[1]):
                 pixelColorHSV = resizeFrameHSV[y,x]
                 if self._isColorInRange(hsvMinMaxRange,pixelColorHSV):
                     backgroundHSV[y,x] = pixelColorHSV

        resultFrame = cv2.cvtColor(backgroundHSV,cv2.COLOR_HSV2RGB)
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

    def _isColorInRange(self,hsvRange,color):
        if hsvRange[0] > self._convertHsvToInt(color) > hsvRange[1]:
            return False
        return True


    def _getHsvRange(self):
        maxHsv = CfgService.getIntList(CfgKey.GREENSCREEN_MAX_HSV_COLOR_WITHOUT_TOLERANCE)
        minHsv = CfgService.getIntList(CfgKey.GREENSCREEN_MIN_HSV_COLOR_WITHOUT_TOLERANCE)
        addToMax = CfgService.getIntList(CfgKey.GREENSCREEN_COLOR_TOLERANCE_POS)
        addToMin = CfgService.getIntList(CfgKey.GREENSCREEN_COLOR_TOLERANCE_NEG)
        for id, amount in enumerate(addToMax):
            maxHsv[id] += amount

        for id, amount in enumerate(addToMin):
            minHsv[id] += amount
        return [self._convertHsvToInt(minHsv),self._convertHsvToInt(maxHsv)]

    def _convertHsvToInt(self,hsv):
        return hsv[0]*1000000+hsv[1]*1000+hsv[2]

    def _getBackgrounds(self):
        return self.globalVariable.getDefaultBackground()

    def _loadBackgroundImages(self,picturePath):
        videoBackground = self._cutPicture(picturePath,CfgService.get(CfgKey.PI_CAMERA_VIDEO_RESOLUTION))
        pictureBackground = self._cutPicture(picturePath,CfgService.get(CfgKey.PI_CAMERA_PHOTO_RESOLUTION))
        return {self.PICTURE_PATH_KEY:picturePath,self.VIDEO_KEY:videoBackground,self.PICTURE_KEY:pictureBackground}