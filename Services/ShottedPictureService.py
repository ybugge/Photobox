import os
import random
import ntpath

from Services.FileFolderService import FileFolderService
from config.Config import CfgKey, cfgValue


class ShottedPictureService():

    @staticmethod
    def saveUsedPicture(fileName):
        folderName = os.path.join(ShottedPictureService._getSaveFolder(),cfgValue[CfgKey.USED_PICTURE_SUB_DIR])
        ShottedPictureService._savePicture(folderName, fileName)

    @staticmethod
    def saveUnusedPicture(fileName):
        folderName = os.path.join(ShottedPictureService._getSaveFolder(),cfgValue[CfgKey.UNUSED_PICTURE_SUB_DIR])
        ShottedPictureService._savePicture(folderName, fileName)

    @staticmethod
    def getTempPicturePath():
        folder = os.path.join(ShottedPictureService._getSaveFolder(),cfgValue[CfgKey.RAW_PICTURE_SUB_DIR])
        FileFolderService.createFolderIfNotExist(folder)
        return os.path.join(folder,"temp"+cfgValue[CfgKey.PICTURE_FORMAT])

    @staticmethod
    def _savePicture(targetFolder, fileName):
        sourceFile = ShottedPictureService.getTempPicturePath()
        targetPath = os.path.join(targetFolder,fileName+cfgValue[CfgKey.PICTURE_FORMAT])
        unicTargetPath = ShottedPictureService._getUnicFileName(targetPath)
        FileFolderService.moveFile(sourceFile,unicTargetPath)


    @staticmethod
    def _getUnicFileName(filePath:str):
        nameWithExtension = os.path.basename(filePath)
        name = os.path.splitext(nameWithExtension)[0]
        extension = os.path.splitext(nameWithExtension)[1]
        dir = ntpath.dirname(filePath)

        while True:
            randomNumber = random.randint(1000, 9999)
            newFilePath = os.path.join(dir, name+"_"+str(randomNumber)+extension)
            if not FileFolderService.existFile(newFilePath):
                return newFilePath

    @staticmethod
    def _getSaveFolder():
        return os.path.join(cfgValue[CfgKey.MAIN_SAVE_DIR], cfgValue[CfgKey.PROJECTNAME])