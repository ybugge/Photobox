import base64
import os
import random

from PyQt5 import QtWidgets
from PyQt5 import QtCore
from PyQt5.QtCore import QSize, QTimer, Qt
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QLabel
from pip._vendor import requests


#Ist das Hauptfenster
from Services.FileFolderService import FileFolderService
from Services.PictureDownloadThread import PictureDownloadThread
from config.Config import cfgValue, CfgKey


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self, windowSize:QSize):
        super().__init__()
        self.setContentsMargins(0,0,0,0)
        #Fullscreen
        self.showFullScreen()
        self.windowSize = windowSize
        self.usedPictureUrls = []
        self.defaultPicturesUrls = []
        self.showNewPictureTimer = QTimer()
        self.updatePictureSourcesTimer = QTimer()



        self.picture = QLabel(self)
        self.picture.setContentsMargins(0,0,0,0)
        self.picture.setAlignment(Qt.AlignCenter)
        self.setCentralWidget(self.picture)

        self.updatePictureSources()
        if len(self.usedPictureUrls) > 0:
            self.showNewPicture()


        self.showNewPictureTimer.timeout.connect(self.showNewPicture)
        self.showNewPictureTimer.start(cfgValue[CfgKey.DIASHOW_CLIENT_PICTURE_SHOW_NEW_PICTURE_INTERVAL])

        self.updatePictureSourcesTimer.timeout.connect(self.updatePictureSources)
        self.updatePictureSourcesTimer.start(cfgValue[CfgKey.DIASHOW_CLIENT_PICTURE_UPDATE_PICTURE_SOURCE_INTERVAL])



    def showNewPicture(self):
        picturePixelMap = QPixmap(self.getRandomPicture())
        self.picture.setPixmap(picturePixelMap.scaled(self.windowSize,Qt.KeepAspectRatioByExpanding))

    def getRandomPicture(self):
        pictureUrls = self.usedPictureUrls
        numberPictures = len(pictureUrls)
        pictureUrlIndex = random.randint(0,numberPictures-1)
        return pictureUrls[pictureUrlIndex]

    def updatePictureSources(self):
        self.showNewPictureTimer.stop()
        self.usedPictureUrls = []
        self.defaultPicturesUrls = []
        subFolderDirs = FileFolderService.getFolderContentFolders(cfgValue[CfgKey.DIASHOW_CLIENT_PICTURE_MAIN_FOLDER])
        if len(subFolderDirs) <= 0:
            self.exit()
            return

        for subFolderDir in subFolderDirs:
            self.updatePictureSource(subFolderDir)

        if len(self.usedPictureUrls) <= 0:
            self.usedPictureUrls.extend(self.defaultPicturesUrls)
        if len(self.usedPictureUrls) <= 0:
            self.exit()
        self.showNewPictureTimer.start(cfgValue[CfgKey.DIASHOW_CLIENT_PICTURE_SHOW_NEW_PICTURE_INTERVAL])


    def updatePictureSource(self,subFolderDir:str):
        configFilePath = os.path.join(subFolderDir,cfgValue[CfgKey.DIASHOW_CLIENT_PICTURE_CONFIG_FILE])
        picturesPath = os.path.join(subFolderDir,cfgValue[CfgKey.DIASHOW_CLIENT_PICTURE_SOURCE_FOLDER])
        if FileFolderService.existFile(configFilePath):
            return self.updatePictureSourceWithConfig(picturesPath,configFilePath)
        elif FileFolderService.existFolder(picturesPath) and not FileFolderService.existFile(configFilePath):
            return self.updatePictureSourceDefault(picturesPath)

    def updatePictureSourceWithConfig(self,picturesPath:str, configFilePath:str):
        fileLines = FileFolderService.readFile(configFilePath)
        config = {}
        for fileLine in fileLines:
            fileLineParts = fileLine.split("=",1)
            config[fileLineParts[0].replace('=', '').strip()] = fileLineParts[1].strip()

        if "default" in config and config["default"] == "True":
            self.updatePicturesNotFound(picturesPath)
        elif "from_server" in config and config["from_server"] == "True":
            self.updatePicturesFromServer(picturesPath)

    def updatePicturesFromServer(self,picturesPath:str):
        serverUrl = "http://"+str(cfgValue[CfgKey.SERVER_IP])+":"+str(cfgValue[CfgKey.SERVER_PORT])+str(cfgValue[CfgKey.SERVER_RANDOM_URLIDS])
        pictureRequest = self.getRequest(serverUrl)

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
            self.updatePictureSourceDefault(picturesPath)



    def getRequest(self,url:str):
        try:
            request = requests.get(url)
            if request.status_code != 200:
                return None
            else:
                return request
        except requests.ConnectionError:
            return None



    def updatePicturesNotFound(self,picturesPath:str):
        picturePaths = FileFolderService.getFolderContentPictures(picturesPath)
        self.defaultPicturesUrls.extend(picturePaths)


    def updatePictureSourceDefault(self,picturesPath:str):
        picturePaths = FileFolderService.getFolderContentPictures(picturesPath)
        self.usedPictureUrls.extend(picturePaths)


    def exit(self):
        print("Keine Bilder gefunden. Bitte legen Sie folgende Ordner an: '"+cfgValue[CfgKey.DIASHOW_CLIENT_PICTURE_MAIN_FOLDER]+"' > 'default' > 'pictures'. In 'pictures' muss ein Bild hinterlegt werden!")
        self.showNewPictureTimer.stop()
        self.close()

    def signal_accept(self, msg):
        pass

    #Alle Keyevents
    def keyPressEvent(self, event):
        # close the window
        if event.key() == QtCore.Qt.Key_Escape:
            self.close()
        event.accept()

    #Schliest die Anwendung
    def close(self):
        self.deleteLater()