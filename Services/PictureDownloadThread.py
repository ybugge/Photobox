import math
from PyQt5.QtCore import QThread, pyqtSignal
from pip._vendor import requests
import re

from Services.FileFolderService import FileFolderService


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
            if( self.downloadSuccessFile != None and FileFolderService.containsLineInFile(url,self.downloadSuccessFile)):
                continue
            request = self.getRequest(url)
            if request == None:
                self.setProgress(index,numberUrls)
                continue

            self.savePicture(request, self.getContentFileType(request),index,self.targetFolder)
            self.setProgress(index,numberUrls)
            if self.downloadSuccessFile != None:
                FileFolderService.writeLineInFile(True,self.downloadSuccessFile,url)

        self.setProgress(numberUrls,numberUrls)

    def getContentFileType(self,request):
        d = request.headers['content-disposition']
        fileName = re.findall("filename=(.+)", d)[0]
        return FileFolderService.getFileType(fileName)

    def getRequest(self,url:str):
        try:
            request = requests.get(url)
            if request.status_code != 200:
                return None
            else:
                return request
        except requests.ConnectionError:
            return None

    def savePicture(self,request,fileType,index, folderPath):
        filePath = folderPath+"/"+str(index)+fileType
        with open(filePath, 'wb') as handler:
            handler.write(request.content)

    def setProgress(self,index:int, maxEntries:int):
        self._signal.emit(math.floor((index/maxEntries)*100))
