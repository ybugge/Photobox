import base64
import os
import random

from PyQt5 import QtWidgets
from PyQt5 import QtCore
from PyQt5.QtCore import QSize, QTimer, Qt, QPoint
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QLabel, QWidget, QVBoxLayout
from pip._vendor import requests


#Ist das Hauptfenster
from DiashowClientPages.PicturesConfig import PicturesConfig
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
        self.setStyleSheet("background-color:black;")

        pictureWidget = QWidget()
        self.setCentralWidget(pictureWidget)

        self.backgroundPicture = QLabel(pictureWidget)
        self.backgroundPicture.setContentsMargins(0, 0, 0, 0)
        self.backgroundPicture.setAlignment(Qt.AlignCenter)
        self.backgroundPicture.setStyleSheet("background-color:transparent;")

        self.frontPicture = QLabel(pictureWidget)
        self.frontPicture.setContentsMargins(0, 0, 0, 0)
        self.frontPicture.setStyleSheet("background-color:transparent;")

        self.updatePictureSources()
        if len(self.usedPictureUrls) > 0:
            self.showNewPicture()

        self.showNewPictureTimer.timeout.connect(self.showNewPicture)
        self.showNewPictureTimer.start(cfgValue[CfgKey.DIASHOW_CLIENT_PICTURE_SHOW_NEW_PICTURE_INTERVAL])

        self.updatePictureSourcesTimer.timeout.connect(self.updatePictureSources)
        self.updatePictureSourcesTimer.start(cfgValue[CfgKey.DIASHOW_CLIENT_PICTURE_UPDATE_PICTURE_SOURCE_INTERVAL])


    def showNewPicture(self):
        randomPictureAndFolderPath = self.getRandomPicture()
        framePath = os.path.join(randomPictureAndFolderPath[1],cfgValue[CfgKey.DIASHOW_CLIENT_PICTURE_FRAME_PICTURE])

        if FileFolderService.existFile(framePath):
            self.showNewPictureWithFrame(randomPictureAndFolderPath,framePath)
        else:
            self.showNewPictureWithoutFrame(randomPictureAndFolderPath)

    def showNewPictureWithoutFrame(self,randomPictureAndFolderPath):
        picturePixelMap = QPixmap(randomPictureAndFolderPath[0])
        self.frontPicture.move(0,0)
        self.backgroundPicture.move(0,0)
        self.frontPicture.setPixmap(picturePixelMap.scaled(self.windowSize.width(),self.windowSize.height()))#, Qt.KeepAspectRatio))
        self.backgroundPicture.setPixmap(picturePixelMap.scaled(self.windowSize.width()-1,self.windowSize.height()-1))#, Qt.KeepAspectRatio))

    def showNewPictureWithFrame(self,randomPictureAndFolderPath,framePath):
        config = PicturesConfig(randomPictureAndFolderPath[1])
        if config.get(PicturesConfig.FRAME_FRONT) == "True":
            frontPicturePixelMap = QPixmap(framePath)
            backPicturePixelMap = QPixmap(randomPictureAndFolderPath[0])
            frontMove = QPoint(0,0)
            frontSize = QSize(self.windowSize.width()-1,self.windowSize.height()-1)
            backMove = QPoint(0,0)
            backSize = QSize(self.windowSize.width()-1,self.windowSize.height()-1)

        else:
            frontPicturePixelMap = QPixmap(randomPictureAndFolderPath[0])
            backPicturePixelMap = QPixmap(framePath)
            backMove = QPoint(0,0)
            backSize = QSize(self.windowSize.width()-1,self.windowSize.height()-1)
            frontMove = QPoint(self.windowSize.width() * 0.1, self.windowSize.height() * 0.1)
            frontSize = QSize(self.windowSize.width()-1 * 0.9,self.windowSize.height()-1 * 0.9)

        self.frontPicture.move(frontMove)
        self.backgroundPicture.move(backMove)
        self.frontPicture.setPixmap(frontPicturePixelMap.scaled(frontSize)) #, Qt.KeepAspectRatio))
        self.backgroundPicture.setPixmap(backPicturePixelMap.scaled(backSize)) #, Qt.KeepAspectRatio))

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
        picturesPath = os.path.join(subFolderDir,cfgValue[CfgKey.DIASHOW_CLIENT_PICTURE_SOURCE_FOLDER])
        pictureConfig = PicturesConfig(subFolderDir)

        if pictureConfig.get(PicturesConfig.DEFAULT) == "True":
            self.updatePicturesNotFound(picturesPath,subFolderDir)
        elif pictureConfig.get(PicturesConfig.FROM_SERVER) == "True":
            self.updatePicturesFromServer(picturesPath,subFolderDir)
        elif FileFolderService.existFolder(picturesPath):
            self.updatePictureSourceDefault(picturesPath,subFolderDir)

    def updatePicturesFromServer(self,picturesPath:str,subFolderDir:str):
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
            self.updatePictureSourceDefault(picturesPath,subFolderDir)

    def getRequest(self,url:str):
        try:
            request = requests.get(url)
            if request.status_code != 200:
                return None
            else:
                return request
        except requests.ConnectionError:
            return None

    def updatePicturesNotFound(self,picturesPath:str,subFolderDir:str):
        picturePaths = FileFolderService.getFolderContentPictures(picturesPath)
        picturePathsWithFrame = []
        for picturePath in picturePaths:
            picturePathsWithFrame.append([picturePath,subFolderDir])
        self.defaultPicturesUrls.extend(picturePathsWithFrame)


    def updatePictureSourceDefault(self,picturesPath:str,subFolderDir:str):
        picturePaths = FileFolderService.getFolderContentPictures(picturesPath)
        picturePathsWithFrame = []
        for picturePath in picturePaths:
            picturePathsWithFrame.append([picturePath,subFolderDir])
        self.usedPictureUrls.extend(picturePathsWithFrame)


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
