import os
import random
import datetime

from PyQt5.QtCore import Qt, QSize, QTimer
from PyQt5.QtGui import QPixmap, QMovie
from PyQt5.QtWidgets import QVBoxLayout, QLabel

from Pages.AllPages import AllPages
from Pages.Page import Page
from Services.Camera.CameraService import CameraService
from Services.CfgService import CfgService
from config.Config import CfgKey


class PageCapturePhoto(Page):
    def __init__(self, pages : AllPages, windowsize:QSize):
        super().__init__(pages,windowsize)
        self.windowsize = windowsize
        mainLayout = QVBoxLayout()
        mainLayout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(mainLayout)

        #Photo
        self.counterLabel = QLabel()
        self.counterLabel.setAlignment(Qt.AlignCenter)
        self.counterLabel.setStyleSheet("background-color: transparent")
        self.counterLabel.setFixedSize(windowsize)
        mainLayout.addWidget(self.counterLabel)

        #gif
        self.gif = None

        #Timer starten
        self.isLoading = False
        self.countdown = -1
        self.timer = QTimer()
        self.timer.timeout.connect(self.timerUpdate)

    def executeBefore(self):
        randomPicture = self.getRandomPicture()
        randomPicture.scaledToHeight(self.windowsize.height())
        self.capturePhotoThread= CameraService.initialPhoto(self.windowsize)
        self.capturePhotoThread.start()
        self.counterLabel.setPixmap(randomPicture.scaledToHeight(self.windowsize.height()))
        self.countdown = CfgService.get(CfgKey.PAGE_CAPTUREPHOTO_TIMER_START_VALUE)
        self.timer.start(CfgService.get(CfgKey.PAGE_CAPTUREPHOTO_TIMER_PERIOD_LENGTH))
        self.isLoading = False

    def tryToExecuteAfterEvent(self):
        pass

    def executeAfter(self):
        self.timer.stop()
        print("Foto Finished: "+str(datetime.datetime.now()))

    def timerUpdate(self):
        if self.countdown == CfgService.get(CfgKey.PAGE_CAPTUREPHOTO_TIMER_CAPTUREPHOTO_VALUE):
            self.capturePhoto()
        elif self.countdown <= 0:
            if not self.capturePhotoThread.isFinished():
                self.countdown = 1
                if not self.isLoading:
                    self.isLoading = True
                    self.startGif()

            else:
                self.stopGif()
                self.nextPageEvent()

        self.countdown -=1

    def capturePhoto(self):
        print("FOTO GESCHOSSEN !")
        print("Foto Start: "+str(datetime.datetime.now()))
        self.capturePhotoThread.shootPicture()

    def getRandomPicture(self):
        directories = os.listdir(CfgService.get(CfgKey.PAGE_CAPTUREPHOTO_LAST_IMAGE_FOLDER))
        numberPictures = len(directories)
        pictureIndex = random.randint(0,numberPictures-1)
        return QPixmap(CfgService.get(CfgKey.PAGE_CAPTUREPHOTO_LAST_IMAGE_FOLDER) + "/" + directories[pictureIndex])

    def startGif(self):
        self.counterLabel.setPixmap(QPixmap())
        self.gif = self.getRandomGif()
        self.counterLabel.setMovie(self.gif)
        self.gif.start()

    def stopGif(self):
        if self.gif != None:
            self.gif.stop()

    def getRandomGif(self):
        directories = os.listdir(CfgService.get(CfgKey.PAGE_CAPTUREPHOTO_LOADING_GIF_FOLDER))
        numberPictures = len(directories)
        pictureIndex = random.randint(0,numberPictures-1)
        gif =  QMovie(CfgService.get(CfgKey.PAGE_CAPTUREPHOTO_LOADING_GIF_FOLDER) + "/" + directories[pictureIndex])
        gifSize = gif.scaledSize()
        gifScaleFactor = self.windowSize.height()/gifSize.height()
        gif.setScaledSize(QSize(gifSize.width()*gifScaleFactor,gifSize.height()*gifScaleFactor))
        return gif
