import os
import shutil


class FileFolderService():

    @staticmethod
    def containsLineInFile(line:str,filePath:str):
        for fileLine in FileFolderService.readFile(filePath):
            if fileLine in line:
                return True
        return False

    @staticmethod
    def moveFile(sourceFile:str, targetFile:str):
        if not os.path.exists(sourceFile) or not os.path.isfile(sourceFile):
            print("Quellfoto wurde nicht gefunden!")
            return
        FileFolderService.creatFolderByFileIfNotExist(targetFile)
        shutil.move(sourceFile,targetFile)

    @staticmethod
    def existFile(filePath:str):
        return os.path.exists(filePath) and os.path.isfile(filePath)

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
    def readImage(fileDir:str):
        resultAsByte = None
        if os.path.exists(fileDir) and os.path.isfile(fileDir):
            file = open(fileDir, 'rb')
            resultAsByte = file.read()
            file.close()
        return resultAsByte


    @staticmethod
    def getFileType(file:str):
        _, file_extension = os.path.splitext(file)
        return file_extension

    @staticmethod
    def creatFolderByFileIfNotExist(file:str):
        FileFolderService.createFolderIfNotExist(os.path.dirname(file))

    @staticmethod
    def createFolderIfNotExist(folder:str):
        os.makedirs(folder,exist_ok=True)

    @staticmethod
    def getAbsoltPath(file:str):
        return os.path.abspath(file)

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
    def writeLinesInFile(append:bool,fileDir:str,lines:list):
        if os.path.exists(fileDir) and append:
            with open(fileDir, "a") as file:
                file.writelines(lines)
            file.close()
        else:
            with open(fileDir,'w') as file:
                file.writelines(lines)
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