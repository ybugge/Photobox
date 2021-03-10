from PyQt5.QtCore import QSize, pyqtSlot, Qt
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtWidgets import QVBoxLayout, QHBoxLayout, QPushButton, QSizePolicy, QWidget, QLabel

from Pages.AllPages import AllPages
from Pages.Page import Page
from Services.CV2VideoThread import CV2VideoThread


class PageCameraCalibrationView(Page):
    def __init__(self, pages : AllPages, windowsize:QSize):
        super().__init__(pages)

        self.windowsize = windowsize
        mainLayout = QVBoxLayout()
        mainLayout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(mainLayout)

        widget = QWidget()
        mainLayout.addWidget(widget)

        #Video
        self.videoLabel = QLabel(widget)
        self.videoLabel.setAlignment(Qt.AlignCenter)
        self.videoThread = self.initialVideoThread(self.windowsize)

        videoLayout = QHBoxLayout(widget)
        videoLayout.setContentsMargins(0, 0, 0, 0)
        videoLayout.addWidget(self.videoLabel)

        #Navigation
        backButton = QPushButton(widget)
        backButton.setStyleSheet("background-color: transparent; border: 0px;")
        backButton.setFixedSize(self.windowsize)
        backButton.clicked.connect(self.backPageEvent)

    def initialVideoThread(self,windowSize):
        t_videoThread = CV2VideoThread(windowSize)
        t_videoThread.changePixmap.connect(self.setVideoStreamToLabel)
        return t_videoThread

    def executeBefore(self):
        print("Start Video")
        self.videoThread = self.initialVideoThread(self.windowsize)
        self.videoThread.start()

    def executeAfter(self):
        print("Stop Video")
        self.videoThread.stop()

    @pyqtSlot(QImage)
    def setVideoStreamToLabel(self, image):
        self.videoLabel.setPixmap(QPixmap.fromImage(image))