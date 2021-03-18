import math
from PyQt5.QtCore import QThread, pyqtSignal
from pip._vendor import requests

from Services.CfgService import CfgService
from Services.FileFolderService import FileFolderService
from config.Config import CfgKey


class PictureDownloadThread(QThread):
    _signal = pyqtSignal(int)
    def __init__(self, urls:list, targetFolder:str, downloadSuccessFile:str):
        super(PictureDownloadThread, self).__init__()
        self.urls = urls
        self.targetFolder = targetFolder
        self.downloadSuccessFile = downloadSuccessFile

    def run(self):
        numberUrls = len(self.urls)
        FileFolderService.createFolderIfNotExist(self.targetFolder)
        for index, url in enumerate(self.urls):
            if(FileFolderService.containsLineInFile(url,self.downloadSuccessFile)):
                continue
            request = self.getRequest(url)
            if request == None:
                self.setProgress(index,numberUrls)
                continue

            self.savePicture(request,url,index,self.targetFolder)
            self.setProgress(index,numberUrls)
            FileFolderService.writeLineInFile(True,self.downloadSuccessFile,url)

        self.setProgress(numberUrls,numberUrls)

    def getRequest(self,url:str):
        try:
            request = requests.get(url)
            if request.status_code != 200:
                return None
            else:
                return request
        except requests.ConnectionError:
            return None

    def savePicture(self,request,url,index, folderPath):
        fileType = FileFolderService.getFileType(url)
        filePath = folderPath+"/"+str(index)+fileType
        with open(filePath, 'wb') as handler:
            handler.write(request.content)

    def setProgress(self,index:int, maxEntries:int):
        self._signal.emit(math.floor((index/maxEntries)*100))
