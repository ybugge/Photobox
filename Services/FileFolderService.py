import ntpath
import os
import random
import shutil

from config.Config import CfgKey, cfgValue


class FileFolderService():

    @staticmethod
    def containsLineInFile(line:str,filePath:str):
        for fileLine in FileFolderService.readFile(filePath):
            if fileLine in line:
                return True
        return False

    @staticmethod
    def saveUsedPicture(fileName):
        folderName = os.path.join(FileFolderService.getSaveFolder(),cfgValue[CfgKey.USED_PICTURE_SUB_DIR])
        FileFolderService.savePicture(folderName, fileName)

    @staticmethod
    def saveUnusedPicture(fileName):
        folderName = os.path.join(FileFolderService.getSaveFolder(),cfgValue[CfgKey.UNUSED_PICTURE_SUB_DIR])
        FileFolderService.savePicture(folderName, fileName)

    @staticmethod
    def savePicture(targetFolder, fileName):
        sourceFile = FileFolderService.getTempPicturePath()
        if not os.path.exists(sourceFile):
            print("Quellfoto wurde nicht gefunden!")
            return
        FileFolderService.createFolderIfNotExist(targetFolder)
        targetPath = os.path.join(targetFolder,fileName+cfgValue[CfgKey.PICTURE_FORMAT])
        unicTargetPath = FileFolderService.getUnicFileName(targetPath)
        shutil.move(sourceFile,unicTargetPath)

    @staticmethod
    def getUnicFileName(filePath:str):
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
    def existFile(filePath:str):
        return os.path.exists(filePath) and os.path.isfile(filePath)

    @staticmethod
    def getShottedPictureNumber():
        unUsedPath = os.path.join(FileFolderService.getSaveFolder(),cfgValue[CfgKey.UNUSED_PICTURE_SUB_DIR])
        usedPath = os.path.join(FileFolderService.getSaveFolder(),cfgValue[CfgKey.USED_PICTURE_SUB_DIR])
        numberContent = FileFolderService.getFolderContentNumber(unUsedPath) + FileFolderService.getFolderContentNumber(usedPath)
        return numberContent

    @staticmethod
    def getTempPicturePath():
        folder = os.path.join(FileFolderService.getSaveFolder(),cfgValue[CfgKey.RAW_PICTURE_SUB_DIR])
        FileFolderService.createFolderIfNotExist(folder)
        return os.path.join(folder,"temp"+cfgValue[CfgKey.PICTURE_FORMAT])

    @staticmethod
    def getSaveFolder():
        return os.path.join(cfgValue[CfgKey.MAIN_SAVE_DIR], cfgValue[CfgKey.PROJECTNAME])

    @staticmethod
    def removeIfExist(fileOrFolderDir:str):
        if os.path.exists(fileOrFolderDir):
            if os.path.isdir(fileOrFolderDir):
                shutil.rmtree(fileOrFolderDir)
            elif os.path.isfile(fileOrFolderDir):
                os.remove(fileOrFolderDir)
            print(fileOrFolderDir +" wurde gelöscht!")

    @staticmethod
    def readFile(fileDir:str):
        if os.path.exists(fileDir) and os.path.isfile(fileDir):
            result = []
            file = open(fileDir, 'r')
            for line in file.readlines():
                result.append(line.replace("\n",""))
            return result
        else:
            return []

    @staticmethod
    def getFileType(file:str):
        _, file_extension = os.path.splitext(file)
        return file_extension

    @staticmethod
    def createFolderIfNotExist(folder:str):
        if not os.path.exists(folder):
            os.makedirs(folder)

    @staticmethod
    def writeLineInFile(append:bool,fileDir:str,line:str):
        if os.path.exists(fileDir) and append:
            with open(fileDir, "a") as file:
                file.write(line+"\n")
            file.close()
        else:
            with open(fileDir,'w') as file:
                file.write(line+"\n")
            file.close()

    @staticmethod
    def hasFolderContent(path:str):
        return FileFolderService.getFolderContentNumber(path) != 0

    @staticmethod
    def getFolderContentNumber(path:str):
        return len(FileFolderService.getFolderContent(path) )

    @staticmethod
    def getFolderContent(path:str):
        if os.path.exists(path):
            if(os.path.isdir(path)):
                return os.listdir(path)
        return []