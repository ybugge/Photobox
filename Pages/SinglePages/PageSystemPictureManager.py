import os

from PyQt5.QtCore import QTimer, QSize
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QVBoxLayout, QHBoxLayout, QPushButton, QLineEdit, QLabel, QProgressBar

from Pages.AllPages import AllPages
from Pages.Page import Page
from Services.CfgService import CfgService
from Services.FileFolderService import FileFolderService
from Services.PictureDownloadThread import PictureDownloadThread
from config.Config import TextKey, textValue, CfgKey


class PageSystemPictureManager(Page):
    def __init__(self, pages : AllPages,windowSize:QSize):
        super().__init__(pages,windowSize)
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

        vbox.addWidget(QLabel(textValue[TextKey.PAGE_SYSTEMPICTUREMANAGER_SOURCELABEL]))
        funnySource = QLineEdit()
        funnySource.setEnabled(False)
        funnySource.setText(CfgService.get(CfgKey.PAGE_SYSTEMPICTUREMANAGER_FUNNY_PICTURE_SOURCE))
        vbox.addWidget(funnySource)

        vbox.addWidget(QLabel(textValue[TextKey.PAGE_SYSTEMPICTUREMANAGER_TARGETLABEL]))
        funnyTarget = QLineEdit()
        funnyTarget.setEnabled(False)
        funnyTarget.setText(CfgService.get(CfgKey.PAGE_CAPTUREPHOTO_LAST_IMAGE_FOLDER))
        vbox.addWidget(funnyTarget)

        funnyPictureNavigation = QHBoxLayout()
        vbox.addLayout(funnyPictureNavigation)

        self.funnyDeleteButton = QPushButton(textValue[TextKey.PAGE_SYSTEMPICTUREMANAGER_DELETEBUTTON])
        self.funnyDeleteButton.clicked.connect(self.deleteFunnyPictureFolder)
        funnyPictureNavigation.addWidget(self.funnyDeleteButton)

        self.funnyUpdateButton = QPushButton(textValue[TextKey.PAGE_SYSTEMPICTUREMANAGER_UPDATEBUTTON])
        self.funnyUpdateButton.clicked.connect(self.updateFunnyPictures)
        funnyPictureNavigation.addWidget(self.funnyUpdateButton)

        #Loading Gifs
        loadingGifTitle = QLabel(textValue[TextKey.PAGE_SYSTEMPICTUREMANAGER_LOADINGGIFS_TITEL])
        loadingGifFont = QFont()
        loadingGifFont.setUnderline(True)
        loadingGifTitle.setFont(funnyTitleFont)
        vbox.addWidget(loadingGifTitle)

        vbox.addWidget(QLabel(textValue[TextKey.PAGE_SYSTEMPICTUREMANAGER_SOURCELABEL]))
        loadingGifSource = QLineEdit()
        loadingGifSource.setEnabled(False)
        loadingGifSource.setText(CfgService.get(CfgKey.PAGE_SYSTEMPICTUREMANAGER_LOADINGGIFS_PICTURE_SOURCE))
        vbox.addWidget(loadingGifSource)

        vbox.addWidget(QLabel(textValue[TextKey.PAGE_SYSTEMPICTUREMANAGER_TARGETLABEL]))
        loadingGifTarget = QLineEdit()
        loadingGifTarget.setEnabled(False)
        loadingGifTarget.setText(CfgService.get(CfgKey.PAGE_CAPTUREPHOTO_LOADING_GIF_FOLDER))
        vbox.addWidget(loadingGifTarget)

        loadingGifNavigation = QHBoxLayout()
        vbox.addLayout(loadingGifNavigation)

        self.loadingGifDeleteButton = QPushButton(textValue[TextKey.PAGE_SYSTEMPICTUREMANAGER_DELETEBUTTON])
        self.loadingGifDeleteButton.clicked.connect(self.deleteLoadingGifFolder)
        loadingGifNavigation.addWidget(self.loadingGifDeleteButton)

        self.loadingGifUpdateButton = QPushButton(textValue[TextKey.PAGE_SYSTEMPICTUREMANAGER_UPDATEBUTTON])
        self.loadingGifUpdateButton.clicked.connect(self.updateLoadingGifs)
        loadingGifNavigation.addWidget(self.loadingGifUpdateButton)


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
        self.setNavigationbuttonStyle(self.pictureManagerButton)
        navigationBox.addWidget(self.pictureManagerButton)

        #timer
        self.timer = QTimer()
        self.timer.timeout.connect(self.timerUpdate)


    def timerUpdate(self):
        self.funnyDeleteButton.setText(textValue[TextKey.PAGE_SYSTEMPICTUREMANAGER_DELETEBUTTON])
        self.funnyUpdateButton.setText(textValue[TextKey.PAGE_SYSTEMPICTUREMANAGER_UPDATEBUTTON])
        self.loadingGifDeleteButton.setText(textValue[TextKey.PAGE_SYSTEMPICTUREMANAGER_DELETEBUTTON])
        self.loadingGifUpdateButton.setText(textValue[TextKey.PAGE_SYSTEMPICTUREMANAGER_UPDATEBUTTON])

    def deleteFunnyPictureFolder(self):
        self.disableAllButtons()
        FileFolderService.removeIfExist(CfgService.get(CfgKey.PAGE_CAPTUREPHOTO_LAST_IMAGE_FOLDER))
        FileFolderService.removeIfExist(CfgService.get(CfgKey.PAGE_SYSTEMPICTUREMANAGER_FUNNY_PICTURE_SOURCE_SUCCESS_DOWNLOAD))
        self.enableAllButtons()
        self.funnyDeleteButton.setText(textValue[TextKey.PAGE_SYSTEMPICTUREMANAGER_SUCCESSFULL])


    def deleteLoadingGifFolder(self):
        self.disableAllButtons()
        FileFolderService.removeIfExist(CfgService.get(CfgKey.PAGE_CAPTUREPHOTO_LOADING_GIF_FOLDER))
        FileFolderService.removeIfExist(CfgService.get(CfgKey.PAGE_SYSTEMPICTUREMANAGER_LOADINGGIFS_PICTURE_SOURCE_SUCCESS_DOWNLOAD))
        self.enableAllButtons()
        self.loadingGifDeleteButton.setText(textValue[TextKey.PAGE_SYSTEMPICTUREMANAGER_SUCCESSFULL])

    def updateLoadingGifs(self):
        self.disableAllButtons()
        urls = FileFolderService.readFile(CfgService.get(CfgKey.PAGE_SYSTEMPICTUREMANAGER_LOADINGGIFS_PICTURE_SOURCE))
        if(len(urls) > 0):
            self.thread = PictureDownloadThread(urls,CfgService.get(CfgKey.PAGE_CAPTUREPHOTO_LOADING_GIF_FOLDER),CfgService.get(CfgKey.PAGE_SYSTEMPICTUREMANAGER_LOADINGGIFS_PICTURE_SOURCE_SUCCESS_DOWNLOAD))
            self.thread._signal.connect(self.signal_accept)
            self.thread.start()
        else:
            self.enableAllButtons()
            self.loadingGifUpdateButton.setText(textValue[TextKey.PAGE_SYSTEMPICTUREMANAGER_SUCCESSFULL])

    def updateFunnyPictures(self):
        self.disableAllButtons()
        urls = FileFolderService.readFile(CfgService.get(CfgKey.PAGE_SYSTEMPICTUREMANAGER_FUNNY_PICTURE_SOURCE))
        if(len(urls) > 0):
            self.thread = PictureDownloadThread(urls,CfgService.get(CfgKey.PAGE_CAPTUREPHOTO_LAST_IMAGE_FOLDER),CfgService.get(CfgKey.PAGE_SYSTEMPICTUREMANAGER_FUNNY_PICTURE_SOURCE_SUCCESS_DOWNLOAD))
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
        self.loadingGifDeleteButton.setDisabled(True)

    def enableAllButtons(self):
        self.startTime()
        self.pictureManagerButton.setDisabled(False)
        self.funnyUpdateButton.setDisabled(False)
        self.funnyDeleteButton.setDisabled(False)
        self.loadingGifDeleteButton.setDisabled(False)

    def signal_accept(self, msg):
        self.progressbar.setValue(int(msg))
        if self.progressbar.value() >= 99:
            self.progressbar.setValue(0)
            self.enableAllButtons()
            self.funnyUpdateButton.setText(textValue[TextKey.PAGE_SYSTEMPICTUREMANAGER_SUCCESSFULL])
            self.loadingGifUpdateButton.setText(textValue[TextKey.PAGE_SYSTEMPICTUREMANAGER_SUCCESSFULL])

    def stopTimer(self):
        self.timer.stop()

    def startTime(self):
        self.timer.start(1000)