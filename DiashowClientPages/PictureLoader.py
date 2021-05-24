import base64
import os

from pip._vendor import requests

from DiashowClientPages.Picture import Picture
from DiashowClientPages.Pictures import Pictures
from DiashowClientPages.PicturesConfig import PicturesConfig
from Services.FileFolderService import FileFolderService
from Services.PictureDownloadThread import PictureDownloadThread
from config.Config import cfgValue, CfgKey


class PictureLoader():

    def __init__(self,withoutServer:bool):
        self.pictures = Pictures()
        self.withoutServer = withoutServer

    def getPictures(self):
        return self.pictures

    def update(self):
        subFolderDirs = FileFolderService.getFolderContentFolders(cfgValue[CfgKey.DIASHOW_CLIENT_PICTURE_MAIN_FOLDER])

        for subFolderDir in subFolderDirs:
            self._updatePictureSource(subFolderDir)

    def _updatePictureSource(self,subFolderDir:str):
        picturesPath = os.path.join(subFolderDir,cfgValue[CfgKey.DIASHOW_CLIENT_PICTURE_SOURCE_FOLDER])
        framePath = os.path.join(subFolderDir,cfgValue[CfgKey.DIASHOW_CLIENT_PICTURE_FRAME_PICTURE])
        if not FileFolderService.existFile(framePath):
            framePath = None
        pictureConfig = PicturesConfig(subFolderDir)

        if pictureConfig.get(PicturesConfig.DEFAULT) == "True":
            self.pictures.addDefault(self._getPicturesByPath(picturesPath,pictureConfig,framePath))
        elif pictureConfig.get(PicturesConfig.FROM_SERVER) == "True":
            if self.withoutServer:
                FileFolderService.removeIfExist(picturesPath)
            else:
                self._loadPicturesFromServer(picturesPath)
                self.pictures.add(self._getPicturesByPath(picturesPath,pictureConfig,framePath))
        elif FileFolderService.existFolder(picturesPath):
            self.pictures.add(self._getPicturesByPath(picturesPath,pictureConfig,framePath))

    def _getPicturesByPath(self,picturesPath:str,pictureConfig:PicturesConfig,framePath:str):
        pictures = []
        for picturePath in FileFolderService.getFolderContentPictures(picturesPath):
            picture = Picture(picturePath,pictureConfig)
            if framePath != None:
                picture.setFramePath(framePath)
            pictures.append(picture)
        return pictures


    def _loadPicturesFromServer(self,picturesPath:str):
        serverUrl = "http://"+str(cfgValue[CfgKey.SERVER_IP])+":"+str(cfgValue[CfgKey.SERVER_PORT])+str(cfgValue[CfgKey.SERVER_RANDOM_URLIDS])
        pictureRequest = self._getRequest(serverUrl)

        if pictureRequest == None:
            return
        pictureUrlsAsString = base64.b64decode(pictureRequest.content).decode('utf-8')
        pictureUrls = list(filter(None,pictureUrlsAsString.split(";")))

        if len(pictureUrls) > 0:
            FileFolderService.removeIfExist(picturesPath)
            pictureDownloadThread = PictureDownloadThread(pictureUrls,picturesPath,None)
            pictureDownloadThread.start()
            while not pictureDownloadThread.isFinished():
                pass

    def _getRequest(self,url:str):
        try:
            request = requests.get(url)
            if request.status_code != 200:
                return None
            else:
                return request
        except requests.ConnectionError:
            return None
