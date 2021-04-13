from PyQt5.QtCore import QSize, pyqtSlot, Qt
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtWidgets import QVBoxLayout, QHBoxLayout, QPushButton, QWidget, QLabel

from PhotoboxPages.AllPages import AllPages
from PhotoboxPages.Page import Page
from Services.Camera.CameraService import CameraService
from Services.GlobalPagesVariableService import GlobalPagesVariableService


class PageCameraCalibrationView(Page):
    def __init__(self, pages : AllPages, windowsize:QSize,globalVariable : GlobalPagesVariableService):
        super().__init__(pages,windowsize)

        self.windowsize = globalVariable.getWindowSize()
        self.globalVariable = globalVariable
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

        #Navigation
        backButton = QPushButton(widget)
        backButton.setStyleSheet("background-color: transparent; border: 0px;")
        backButton.setFixedSize(self.windowsize)
        backButton.clicked.connect(self.backPageEvent)


    def executeBefore(self):
        print("Start Video")
        self.videoThread = CameraService.initialAndStartVideo(self.windowsize,self.globalVariable,self.setVideoStreamToLabel)

    def executeAfter(self):
        print("Stop Video")
        self.videoThread.stop()

    @pyqtSlot(QImage)
    def setVideoStreamToLabel(self, image):
        self.videoLabel.setPixmap(QPixmap.fromImage(image))