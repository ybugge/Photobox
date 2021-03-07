import os
import random

from PyQt5.QtCore import Qt, QSize, QTimer
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QVBoxLayout, QLabel, QWidget

from Pages.AllPages import AllPages
from Pages.Page import Page
from config.Config import cfgValue, CfgKey


class PageCapturePhoto(Page):
    def __init__(self, pages : AllPages, windowsize:QSize):
        super().__init__(pages)
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

        #Timer starten
        self.countdown = -1
        self.timer = QTimer()
        self.timer.timeout.connect(self.timerUpdate)

    def executeBefore(self):
        randomPicture = self.getRandomPicture()
        randomPicture.scaledToHeight(self.windowsize.height())
        self.counterLabel.setPixmap(randomPicture.scaledToHeight(self.windowsize.height()))
        self.countdown = cfgValue[CfgKey.PAGE_CAPTUREPHOTO_TIMER_START_VALUE]
        self.timer.start(cfgValue[CfgKey.PAGE_CAPTUREPHOTO_TIMER_PERIOD_LENGTH])

    def executeAfter(self):
        self.timer.stop()

    def timerUpdate(self):
        if self.countdown == 1:
            self.capturePhoto()
        elif self.countdown <= 0:
            self.nextPageEvent()

        self.countdown -=1

    def capturePhoto(self):
        print("FOTO GESCHOSSEN !")

    def getRandomPicture(self):
        directories = os.listdir(cfgValue[CfgKey.PAGE_CAPTUREPHOTO_LAST_IMAGE_FOLDER])
        numberPictures = len(directories)
        pictureIndex = random.randint(0,numberPictures-1)
        return QPixmap(cfgValue[CfgKey.PAGE_CAPTUREPHOTO_LAST_IMAGE_FOLDER] + "/" + directories[pictureIndex])

