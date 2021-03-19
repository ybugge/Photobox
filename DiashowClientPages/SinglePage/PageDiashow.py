import os
import random

from PyQt5.QtCore import QSize, Qt, QTimer
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QVBoxLayout, QLabel

from DiashowClientPages import MainWindow
from PhotoboxPages.AllPages import AllPages
from PhotoboxPages.Page import Page
from Services.FileFolderService import FileFolderService
from config.Config import CfgKey, cfgValue


class PageDiashow(Page):
    def __init__(self, pages : AllPages,windowSize:QSize,mainWindow:MainWindow):
        super().__init__(pages,windowSize)
        self.mainWindow = mainWindow
        self.usedPictureUrls = []

        mainLayout = QVBoxLayout()
        self.setLayout(mainLayout)


        self.picture = QLabel(self)
        self.picture.setAlignment(Qt.AlignCenter)
        mainLayout.addWidget(self.picture)

        self.updatePictureSources()
        if len(self.usedPictureUrls) > 0:
            self.showNewPicture()

        self.showNewPictureTimer = QTimer()
        self.showNewPictureTimer.timeout.connect(self.showNewPicture)
        self.showNewPictureTimer.start(cfgValue[CfgKey.DIASHOW_CLIENT_PICTURE_SHOW_NEW_PICTURE_INTERVAL])

        self.updatePictureSourcesTimer = QTimer()
        self.updatePictureSourcesTimer.timeout.connect(self.updatePictureSources)
        self.updatePictureSourcesTimer.start(cfgValue[CfgKey.DIASHOW_CLIENT_PICTURE_UPDATE_PICTURE_SOURCE_INTERVAL])



    def showNewPicture(self):
        picturePixelMap = QPixmap(self.getRandomPicture())
        self.picture.setPixmap(picturePixelMap.scaled(self.windowSize,Qt.KeepAspectRatio))

    def getRandomPicture(self):
        pictureUrls = self.usedPictureUrls
        print(pictureUrls)
        numberPictures = len(pictureUrls)
        pictureUrlIndex = random.randint(0,numberPictures-1)
        return pictureUrls[pictureUrlIndex]

    def updatePictureSources(self):
        self.usedPictureUrls = []
        subFolderDirs = FileFolderService.getFolderContentFolders(cfgValue[CfgKey.DIASHOW_CLIENT_PICTURE_MAIN_FOLDER])
        if len(subFolderDirs) <= 0:
            self.exit()
            return
        numberPictures = 0
        for subFolderDir in subFolderDirs:
            numberPictures += self.updatePictureSource(subFolderDir)

        if numberPictures <= 0:
            self.exit()


    def updatePictureSource(self,subFolderDir:str):
        configFilePath = os.path.join(subFolderDir,cfgValue[CfgKey.DIASHOW_CLIENT_PICTURE_CONFIG_FILE])
        picturesPath = os.path.join(subFolderDir,cfgValue[CfgKey.DIASHOW_CLIENT_PICTURE_SOURCE_FOLDER])
        if FileFolderService.existFile(configFilePath):
            return 0
        elif FileFolderService.existFolder(picturesPath):
            return self.updatePictureSourceDefault(picturesPath)
        else:
            return 0

    def updatePictureSourceDefault(self,picturesPath:str):
        picturePaths = FileFolderService.getFolderContentPictures(picturesPath)
        self.usedPictureUrls.extend(picturePaths)
        return len(picturePaths)


    def exit(self):
        print("Keine Bilder gefunden. Bitte legen Sie folgende Ordner an: '"+cfgValue[CfgKey.DIASHOW_CLIENT_PICTURE_MAIN_FOLDER]+"' > 'default' > 'pictures'. In 'pictures' muss ein Bild hinterlegt werden!")
        self.showNewPictureTimer.stop()
        self.mainWindow.close()