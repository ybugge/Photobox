import os
import random

from PyQt5.QtWidgets import QPushButton, QVBoxLayout, QSizePolicy

from Pages.AllPages import AllPages
from Pages.Page import Page
from config.Config import cfgValue, CfgKey


class PageTitlePicture(Page):
    def __init__(self, pages : AllPages):
        super().__init__(pages)
        vbox = QVBoxLayout()
        self.setLayout(vbox)

        #Startbutton
        self.startButton = QPushButton(self)
        self.startButton.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.startButton.clicked.connect(self.nextPageEvent)
        vbox.addWidget(self.startButton)

    def executeBefore(self):
        self.setStartButtonStyle()

    def setStartButtonStyle(self):
        self.startButton.setStyleSheet("border-image : url(" + self.__getBackgroundPicturePath() + ");"
                                        " background-color:" + cfgValue[CfgKey.PAGE_TITLEPICTURE_BUTTON_BACKGROUND_COLOR] + ";")
    def __getBackgroundPicturePath(self):
        directories = os.listdir(cfgValue[CfgKey.PAGE_TITLEPICTURE_BUTTON_IMAGE_FOLDER])
        numberPictures = len(directories)
        pictureIndex = random.randint(0,numberPictures-1)
        return cfgValue[CfgKey.PAGE_TITLEPICTURE_BUTTON_IMAGE_FOLDER] + "/" + directories[pictureIndex]