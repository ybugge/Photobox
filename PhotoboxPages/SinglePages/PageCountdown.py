import os

from PyQt5.QtCore import pyqtSlot, Qt, QSize, QTimer
from PyQt5.QtGui import QPixmap, QImage
from PyQt5.QtWidgets import QVBoxLayout, QLabel, QHBoxLayout, QWidget

from PhotoboxPages.AllPages import AllPages
from PhotoboxPages.Page import Page
from Services.Camera.CameraService import CameraService
from Services.CfgService import CfgService
from config.Config import CfgKey


class PageCameraPreview(Page):
    def __init__(self, pages : AllPages, windowsize:QSize):
        super().__init__(pages,windowsize)

        self.windowsize = windowsize
        mainLayout = QVBoxLayout()
        mainLayout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(mainLayout)

        widget = QWidget()
        mainLayout.addWidget(widget)

        #Video
        self.videoLabel = QLabel(widget)
        self.videoLabel.setAlignment(Qt.AlignCenter)
        self.videoThread = None

        videoLayout = QHBoxLayout(widget)
        videoLayout.setContentsMargins(0, 0, 0, 0)
        videoLayout.addWidget(self.videoLabel)

        #Countdown
        self.counterLabel = QLabel(widget)
        self.counterLabel.setAlignment(Qt.AlignCenter)
        self.counterLabel.setStyleSheet("background-color: transparent")
        self.counterLabel.setFixedSize(self.windowsize)

        #Timer starten
        self.countdown = -1
        self.timer = QTimer()
        self.timer.timeout.connect(self.timerUpdate)

    def timerUpdate(self):
        if self.countdown <= 1:
            self.nextPageEvent()
        pixmap = self.getCounterImage(self.countdown)
        if pixmap == None:
            self.counterLabel.setPixmap(QPixmap())
        else:
            self.counterLabel.setPixmap(pixmap.scaledToHeight(self.windowsize.height()/2))
        self.countdown -=1

    def getCounterImage(self,number:int):
        directories = os.listdir(CfgService.get(CfgKey.PAGE_CAMERAPREVIEW_COUNDOWN_IMAGE_FOLDER))
        for file in directories:
            if file.endswith(str(number)+".png"):
                return QPixmap(CfgService.get(CfgKey.PAGE_CAMERAPREVIEW_COUNDOWN_IMAGE_FOLDER)+"/"+file)
        return None

    def executeBefore(self):
        print("Start Video")
        self.videoLabel.setPixmap(QPixmap())
        self.videoThread = CameraService.initialAndStartVideo(self.windowsize,self.setVideoStreamToLabel)
        self.countdown = CfgService.get(CfgKey.PAGE_CAMERAPREVIEW_COUNTER_START_VALUE)
        self.timer.start(CfgService.get(CfgKey.PAGE_CAMERAPREVIEW_COUNTER_PERIOD_LENGTH))

    def executeAfter(self):
        print("Stop Video")
        self.videoThread.stop()
        self.timer.stop()

    @pyqtSlot(QImage)
    def setVideoStreamToLabel(self, image):
        self.videoLabel.setPixmap(QPixmap.fromImage(image))
