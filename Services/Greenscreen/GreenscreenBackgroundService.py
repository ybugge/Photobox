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

    PICTURE_KEY = "picture"
    VIDEO_KEY = "video"
    PICTURE_PREVIEW_PATH_KEY = "previewPath"
    PICTURE_PATH_KEY = "picturePath"
    IS_CUSTOM = "isCustom"
    ROTATE_ANGLE = "rotate_angle"

    def __init__(self,globalVariable:GlobalPagesVariableService):
        self.globalVariable = globalVariable

    def getBackgroundAsHsv(self,backroundKey:str,resolution):
        index = self.getIndex()
        background =  self.globalVariable.getDefaultBackground()[index][backroundKey].resize((resolution[0],resolution[1]))
        return cv2.cvtColor(np.array(background),cv2.COLOR_RGB2HSV)

    def getBlackBackgroundAsHsv(self,resolution):
        blackImage =  np.zeros((resolution[1], resolution[0], 3), dtype = "uint8")
        return cv2.cvtColor(blackImage,cv2.COLOR_BGR2HSV)

    def loadDefaultBackgrounds(self):
        # Bilder aus Ordner laden
        folderPath = self._getBackgroundPathCreateFolderIfNotExtist()
        picturePaths = FileFolderService.getFolderContentPictures(folderPath)
        FileFolderService.removeIfExist(self._getTempPath())
        FileFolderService.createFolderIfNotExist(self._getTempPath())
        backgrounds = []
        for picturePath in picturePaths:
            backgrounds.append(self._loadBackgroundImages(picturePath,False))
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
            return self._getBackgrounds()[index][self.PICTURE_PREVIEW_PATH_KEY]

    def _cutPicture(self,picturePath,targetResolution,rotateAngle:int):
        picture = Image.open(picturePath).rotate(rotateAngle, expand=True)
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


    def _getBackgroundPathCreateFolderIfNotExtist(self):
        folder = GreenscreenBackgroundService.getDefaultBackgroundPath()
        FileFolderService.createFolderIfNotExist(folder)
        return folder

    def _getBackgrounds(self):
        return self.globalVariable.getDefaultBackground()

    def rotateBackground(self,backgroundId:int,deltaRotateAngle:int):
        background = self._getBackgrounds()[backgroundId]
        backgroundPath = background[GreenscreenBackgroundService.PICTURE_PATH_KEY]
        backgroundIsCustom = background[GreenscreenBackgroundService.IS_CUSTOM]
        rotateAngle = background[GreenscreenBackgroundService.ROTATE_ANGLE]
        newRotateAngle = (rotateAngle+deltaRotateAngle)%360
        self._getBackgrounds()[backgroundId] = self._loadBackgroundImages(backgroundPath,backgroundIsCustom,newRotateAngle)

    def _loadBackgroundImages(self,picturePath,isCustom:bool,rotateAngle:int=0):
        videoBackground = self._cutPicture(picturePath,CfgService.get(CfgKey.PI_CAMERA_VIDEO_RESOLUTION),rotateAngle)
        pictureBackground = self._cutPicture(picturePath,CfgService.get(CfgKey.PI_CAMERA_PHOTO_RESOLUTION),rotateAngle)
        previewPath = self._savePreview(pictureBackground,picturePath,isCustom)
        return {GreenscreenBackgroundService.PICTURE_PATH_KEY:picturePath,
                GreenscreenBackgroundService.PICTURE_PREVIEW_PATH_KEY:previewPath,
                GreenscreenBackgroundService.VIDEO_KEY:videoBackground,
                GreenscreenBackgroundService.PICTURE_KEY:pictureBackground,
                GreenscreenBackgroundService.IS_CUSTOM:isCustom,
                GreenscreenBackgroundService.ROTATE_ANGLE:rotateAngle}

    def _savePreview(self,image,sourcePath:str,isCustom:bool):
        fileName = FileFolderService.getFileName(sourcePath)
        if isCustom:
            fileName = CfgService.get(CfgKey.GREENSCREEN_CUSTOM_BACKGROUND_PREVIEW_FILENAME)+fileName
            filePath = os.path.join(GreenscreenBackgroundService.getCustomBackgroundPath(), fileName)
        else:
            filePath = os.path.join(self._getTempPath(), fileName)
        windowSize = self.globalVariable.getWindowSize()
        preview = image.resize((windowSize.width(),windowSize.height()))
        preview.save(filePath)
        return filePath

    @staticmethod
    def getDefaultBackgroundPath():
        return os.path.join(CfgService.get(CfgKey.MAIN_SAVE_DIR), CfgService.get(CfgKey.PROJECTNAME), CfgService.get(CfgKey.GREENSCREEN_FOLDER),CfgService.get(CfgKey.GREENSCREEN_BACKGROUND_FOLDER))

    def _getTempPath(self):
        return os.path.join(CfgService.get(CfgKey.MAIN_SAVE_DIR), CfgService.get(CfgKey.PROJECTNAME), CfgService.get(CfgKey.GREENSCREEN_FOLDER),CfgService.get(CfgKey.GREENSCREEN_TEMP_FOLDER))

    @staticmethod
    def getCustomBackgroundPath():
        return os.path.join(CfgService.get(CfgKey.MAIN_SAVE_DIR), CfgService.get(CfgKey.PROJECTNAME), CfgService.get(CfgKey.GREENSCREEN_FOLDER),CfgService.get(CfgKey.GREENSCREEN_CUSTOM_BACKGROUND_FOLDER))

    def appendCustomBackground(self,customBackgroundFolder:str,uuid:str):
        filePath = GreenscreenBackgroundService.getCustomFilePathWithName(customBackgroundFolder,uuid)
        if filePath is None:
            return
        self.globalVariable.getDefaultBackground().insert(0,self._loadBackgroundImages(filePath,True))

    def cleanCustomBackground(self):
        for index, value in enumerate(self.globalVariable.getDefaultBackground()):
            if value[GreenscreenBackgroundService.IS_CUSTOM]:
                self.globalVariable.getDefaultBackground().remove(value)

        FileFolderService.removeIfExist(GreenscreenBackgroundService.getCustomBackgroundPath())


    @staticmethod
    def getCustomFilePathWithName(customBackgroundFolder:str,uuid:str, fileName:str = None):
        FileFolderService.createFolderIfNotExist(customBackgroundFolder)
        newFileName = uuid

        existingFileNames = []
        for fileUrl in FileFolderService.getFolderContentFiles(customBackgroundFolder):
            existingFileName = FileFolderService.getFileName(fileUrl)
            if existingFileName.startswith( newFileName ):
                existingFileNames.append(fileUrl)

        if fileName is None:
            if len(existingFileNames)> 0:
                newFileNameWithIndex = newFileName+"_"+str(len(existingFileNames))
                for existingFileUrl in existingFileNames:
                    existingFileName = FileFolderService.getFileName(existingFileUrl)
                    if existingFileName.startswith(newFileNameWithIndex):
                        return existingFileUrl


            return None
        else:
            type = FileFolderService.getFileType(fileName)
            return os.path.join(customBackgroundFolder,newFileName+"_"+str(len(existingFileNames)+1)+type)