import os
import shutil

from config.Config import CfgKey, cfgValue


class FileFolderService():

    @staticmethod
    def getTempPicturePath():
        folder = os.path.join(FileFolderService.getSaveFolder(),cfgValue[CfgKey.RAW_PICTURE_SUB_DIR])
        FileFolderService.createFolderIfNotExist(folder)
        return os.path.join(folder,"temp.png")

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
        if os.path.exists(fileDir):
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
        if os.path.exists(fileDir) and not append:
            with open(fileDir, "a") as file:
                file.write(line)
            file.close()
        else:
            with open(fileDir,'wb') as file:
                file.write(line)
            file.close()

    @staticmethod
    def hasFolderContent(path:str):
        if os.path.exists(path):
            if(os.path.isdir(path)):
                return len(os.listdir(path) ) != 0
        return False