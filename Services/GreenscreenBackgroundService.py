import datetime
import math
import os

import cv2
import numpy as np
from PIL import Image
from PIL.ImageQt import ImageQt
from PyQt5.QtCore import QSize
from PyQt5.QtGui import QPixmap

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
        start = datetime.datetime.now()
        print("Greenscreen Start: "+str(start))
        background = self._getUsedBackground(backroundKey,resolution)
        resultFrame = np.zeros((background.height,background.width,3), np.uint8)
        resizeFrameRGB = self._getCurrentFrameRGB(background,frame)
        resizeFrameHSV = cv2.cvtColor(resizeFrameRGB,cv2.COLOR_BGR2HSV)
        hsvMinMaxRange = self._getHsvRange()
        preperation = datetime.datetime.now()
        print("Vorbereitung:"+str(preperation)+" "+str(preperation-start))

        for x  in range((background.width)):
            for y in range((background.height)):
                pixelColorHSV = resizeFrameHSV[y,x]
                if self._isColorInRange(hsvMinMaxRange,pixelColorHSV):
                    color = background.getpixel((x,y))
                    resultFrame[y,x] = np.array((color[2],color[1],color[0]))
                else:
                    resultFrame[y,x] = resizeFrameRGB[y,x]
        end = datetime.datetime.now()
        print("Finished:"+str(end)+" "+str(preperation-end))
        return resultFrame


    def _getUsedBackground(self,backroundKey:str,resolution):
        index = self.getIndex()
        return self.globalVariable.getDefaultBackground()[index][backroundKey].resize((resolution[0],resolution[1]))

    def _getCurrentFrameRGB(self,background,frame):
        if background.height != len(frame) or background.width != len(frame[0]):
            resizeFrameRGB = cv2.resize(frame, (background.width, background.height))
        else:
            resizeFrameRGB = frame
        return resizeFrameRGB

    def _isColorInRange(self,hsvRange,color):
        for id in range(1):
            if hsvRange[0][id] > color[id] and color[id] > hsvRange[1][id]:
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
        return [minHsv,maxHsv]


    def _getBackgrounds(self):
        return self.globalVariable.getDefaultBackground()

    def _loadBackgroundImages(self,picturePath):
        videoBackground = self._cutPicture(picturePath,CfgService.get(CfgKey.PI_CAMERA_VIDEO_RESOLUTION))
        pictureBackground = self._cutPicture(picturePath,CfgService.get(CfgKey.PI_CAMERA_PHOTO_RESOLUTION))
        return {self.PICTURE_PATH_KEY:picturePath,self.VIDEO_KEY:videoBackground,self.PICTURE_KEY:pictureBackground}