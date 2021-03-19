from PyQt5.QtCore import QSize
from PyQt5.QtWidgets import QVBoxLayout, QHBoxLayout, QPushButton

from PhotoboxPages.AllPages import AllPages
from PhotoboxPages.Page import Page
from Services.GlobalPagesVariableService import GlobalPagesVariableService
from Services.PageDbService import PageDbSevice
from Services.ShottedPictureService import ShottedPictureService
from config.Config import textValue, TextKey


class PagePrint(Page):
    def __init__(self, pages : AllPages, windowSize:QSize, globalVariable:GlobalPagesVariableService):
        super().__init__(pages,windowSize)
        self.globalVariable = globalVariable

        mainLayout = QVBoxLayout()
        self.setLayout(mainLayout)

        #Titel
        self.title = self.getTitleAsQLabel(TextKey.PAGE_PRINT_TITLE)
        mainLayout.addWidget(self.title)
        mainLayout.addStretch()

        #Navigation
        mainLayout.addStretch()
        navigationLayout=QHBoxLayout()
        mainLayout.addLayout(navigationLayout)

        backButton = QPushButton(textValue[TextKey.PAGE_PRINT_BACKBUTTON])
        backButton.clicked.connect(self.backPageEvent)
        self.setNavigationbuttonStyle(backButton)
        navigationLayout.addWidget(backButton)

    def executeInAutoForwardTimerEvent(self):
        pictureTargetPath = ShottedPictureService.saveUsedPicture(self.globalVariable.getPictureSubName())
        PageDbSevice.updatePicture(self.globalVariable,pictureTargetPath,True)
        self.globalVariable.unlockPictureName()