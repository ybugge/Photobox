import os

from PyQt5.QtCore import QTimer
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QVBoxLayout, QHBoxLayout, QPushButton, QLineEdit, QLabel, QProgressBar

from Pages.AllPages import AllPages
from Pages.Page import Page
from Services.FileFolderService import FileFolderService
from Services.PictureDownloadThread import PictureDownloadThread
from config.Config import TextKey, textValue, CfgKey, cfgValue


class PageSystemPictureManager(Page):
    def __init__(self, pages : AllPages):
        super().__init__(pages)
        vbox = QVBoxLayout()
        self.setLayout(vbox)

        #Titel
        vbox.addWidget(self.getTitleAsQLabel(TextKey.PAGE_SYSTEMPICTUREMANAGER_TITLE))

        #Funny pictures
        funnyTitle = QLabel(textValue[TextKey.PAGE_SYSTEMPICTUREMANAGER_FUNNY_TITEL])
        funnyTitleFont = QFont()
        funnyTitleFont.setUnderline(True)
        funnyTitle.setFont(funnyTitleFont)
        vbox.addWidget(funnyTitle)

        vbox.addWidget(QLabel(textValue[TextKey.PAGE_SYSTEMPICTUREMANAGER_FUNNY_SOURCELABEL]))
        funnySource = QLineEdit()
        funnySource.setEnabled(False)
        funnySource.setText(cfgValue[CfgKey.PAGE_SYSTEMPICTUREMANAGER_FUNNY_PICTURE_SOURCE])
        vbox.addWidget(funnySource)

        vbox.addWidget(QLabel(textValue[TextKey.PAGE_SYSTEMPICTUREMANAGER_FUNNY_TARGETLABEL]))
        funnyTarget = QLineEdit()
        funnyTarget.setEnabled(False)
        funnyTarget.setText(cfgValue[CfgKey.PAGE_CAPTUREPHOTO_LAST_IMAGE_FOLDER])
        vbox.addWidget(funnyTarget)

        funnyPictureNavigation = QHBoxLayout()
        vbox.addLayout(funnyPictureNavigation)

        self.funnyDeleteButton = QPushButton(textValue[TextKey.PAGE_SYSTEMPICTUREMANAGER_FUNNY_DELETEBUTTON])
        self.funnyDeleteButton.clicked.connect(self.deleteFunnyPictureFolder)
        funnyPictureNavigation.addWidget(self.funnyDeleteButton)

        self.funnyUpdateButton = QPushButton(textValue[TextKey.PAGE_SYSTEMPICTUREMANAGER_FUNNY_UPDATEBUTTON])
        self.funnyUpdateButton.clicked.connect(self.updateFunnyPictures)
        funnyPictureNavigation.addWidget(self.funnyUpdateButton)


        vbox.addStretch()
        #progressbar
        self.progressbar = QProgressBar()
        self.progressbar.setValue(0)
        vbox.addWidget(self.progressbar)
        #Navigationbuttons
        navigationBox = QHBoxLayout()
        vbox.addLayout(navigationBox)

        self.pictureManagerButton = QPushButton(textValue[TextKey.PAGE_SYSTEMPICTUREMANAGER_NEXTBUTTON])
        self.pictureManagerButton.clicked.connect(self.nextPageEvent)
        navigationBox.addWidget(self.pictureManagerButton)

        #timer
        self.timer = QTimer()
        self.timer.timeout.connect(self.timerUpdate)


    def timerUpdate(self):
        self.funnyDeleteButton.setText(textValue[TextKey.PAGE_SYSTEMPICTUREMANAGER_FUNNY_DELETEBUTTON])
        self.funnyUpdateButton.setText(textValue[TextKey.PAGE_SYSTEMPICTUREMANAGER_FUNNY_UPDATEBUTTON])

    def deleteFunnyPictureFolder(self):
        self.disableAllButtons()
        FileFolderService.removeIfExist(cfgValue[CfgKey.PAGE_CAPTUREPHOTO_LAST_IMAGE_FOLDER])
        FileFolderService.removeIfExist(cfgValue[CfgKey.PAGE_SYSTEMPICTUREMANAGER_FUNNY_PICTURE_SOURCE_SUCCESS_DOWNLOAD])
        self.enableAllButtons()
        self.funnyDeleteButton.setText(textValue[TextKey.PAGE_SYSTEMPICTUREMANAGER_SUCCESSFULL])

    def updateFunnyPictures(self):
        self.disableAllButtons()
        urls = FileFolderService.readFile(cfgValue[CfgKey.PAGE_SYSTEMPICTUREMANAGER_FUNNY_PICTURE_SOURCE])
        if(len(urls) > 0):
            self.thread = PictureDownloadThread(urls)
            self.thread._signal.connect(self.signal_accept)
            self.thread.start()
        else:
            self.enableAllButtons()
            self.funnyUpdateButton.setText(textValue[TextKey.PAGE_SYSTEMPICTUREMANAGER_SUCCESSFULL])

    def disableAllButtons(self):
        self.startTime()
        self.pictureManagerButton.setDisabled(True)
        self.funnyUpdateButton.setDisabled(True)
        self.funnyDeleteButton.setDisabled(True)

    def enableAllButtons(self):
        self.startTime()
        self.pictureManagerButton.setDisabled(False)
        self.funnyUpdateButton.setDisabled(False)
        self.funnyDeleteButton.setDisabled(False)

    def signal_accept(self, msg):
        self.progressbar.setValue(int(msg))
        if self.progressbar.value() >= 99:
            self.progressbar.setValue(0)
            self.enableAllButtons()
            self.funnyUpdateButton.setText(textValue[TextKey.PAGE_SYSTEMPICTUREMANAGER_SUCCESSFULL])

    def stopTimer(self):
        self.timer.stop()

    def startTime(self):
        self.timer.start(1000)