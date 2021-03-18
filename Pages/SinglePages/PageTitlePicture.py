import os
import random

from PyQt5.QtCore import QSize
from PyQt5.QtGui import QImage, QBrush, QPalette
from PyQt5.QtWidgets import QPushButton, QVBoxLayout, QSizePolicy

from Pages.AllPages import AllPages
from Pages.Page import Page
from Services.CfgService import CfgService
from config.Config import CfgKey


class PageTitlePicture(Page):
    def __init__(self, pages : AllPages,windowSize:QSize):
        super().__init__(pages,windowSize)
        vbox = QVBoxLayout()
        self.setLayout(vbox)
        if CfgService.get(CfgKey.PAGE_TITLEPICTURE_BACKGROUND_IMAGE) != None:
            self.setStyleSheet("background-image: url('"+CfgService.get(CfgKey.PAGE_TITLEPICTURE_BACKGROUND_IMAGE)+"');")


        #Startbutton
        self.startButton = QPushButton()
        self.startButton.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.startButton.clicked.connect(self.nextPageEvent)
        vbox.addWidget(self.startButton)

    def executeBefore(self):
        self.setStartButtonStyle()

    def setStartButtonStyle(self):
        styling = "border-image : url(" + self.__getBackgroundPicturePath() + ");"
        if CfgService.get(CfgKey.PAGE_TITLEPICTURE_BACKGROUND_IMAGE) != None:
            styling += " background-color: transparent;"
        else:
            styling += "background-color: "+CfgService.get(CfgKey.PAGE_TITLEPICTURE_BUTTON_BACKGROUND_COLOR)+";"
        self.startButton.setStyleSheet(styling)

    def __getBackgroundPicturePath(self):
        directories = os.listdir(CfgService.get(CfgKey.PAGE_TITLEPICTURE_BUTTON_IMAGE_FOLDER))
        numberPictures = len(directories)
        pictureIndex = random.randint(0,numberPictures-1)
        return CfgService.get(CfgKey.PAGE_TITLEPICTURE_BUTTON_IMAGE_FOLDER) + "/" + directories[pictureIndex]