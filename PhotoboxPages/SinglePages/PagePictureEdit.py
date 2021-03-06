
from PyQt5.QtCore import QSize, Qt
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QVBoxLayout, QPushButton, QHBoxLayout, QLabel

from PhotoboxPages.AllPages import AllPages
from PhotoboxPages.Page import Page
from Services.CfgService import CfgService
from Services.ShottedPictureService import ShottedPictureService
from config.Config import CfgKey


class PagePictureEdit(Page):
    def __init__(self, pages : AllPages, windowsize:QSize):
        super().__init__(pages,windowsize)
        self.windowsize = windowsize
        self.heightDevider = 8
        self.resetPictureIdUsed()


        mainLayout = QVBoxLayout()
        mainLayout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(mainLayout)

        #Picture
        self.picture = QLabel(self)
        self.picture.setAlignment(Qt.AlignCenter)
        mainLayout.addWidget(self.picture)

        #Navigation
        mainLayout.addStretch()
        navigationLayout=QHBoxLayout()
        mainLayout.addLayout(navigationLayout)

        self.printButton = QPushButton()
        self.printButton.clicked.connect(self.printPageEvent)
        self.printButton.setStyleSheet("qproperty-icon: url(" + CfgService.get(CfgKey.PAGE_PICTUREEDIT_PRINT_BUTTON_ICON_DIR) + ");")
        self.printButton.setIconSize(self.getButtonSize())
        self.printButton.setFixedSize(self.getButtonSize())
        navigationLayout.addWidget(self.printButton)

        downloadButton = QPushButton()
        downloadButton.clicked.connect(self.downloadPageEvent)
        downloadButton.setStyleSheet("qproperty-icon: url(" + CfgService.get(CfgKey.PAGE_PICTUREEDIT_DOWNLOAD_BUTTON_ICON_DIR) + ");")
        downloadButton.setIconSize(self.getButtonSize())
        downloadButton.setFixedSize(self.getButtonSize())
        navigationLayout.addWidget(downloadButton)

        navigationLayout.addStretch()

        helpButton = QPushButton()
        helpButton.clicked.connect(self.helpPageEvent)
        helpButton.setStyleSheet("qproperty-icon: url(" + CfgService.get(CfgKey.PAGE_PICTUREEDIT_HELP_BUTTON_ICON_DIR) + ");")
        helpButton.setIconSize(self.getButtonSize())
        helpButton.setFixedSize(self.getButtonSize())
        navigationLayout.addWidget(helpButton)

        navigationLayout.addStretch()

        nextPictureButton = QPushButton()
        nextPictureButton.clicked.connect(self.newPicturePageEvent)
        nextPictureButton.setStyleSheet("qproperty-icon: url(" + CfgService.get(CfgKey.PAGE_PICTUREEDIT_NEWPICTURE_BUTTON_ICON_DIR) + ");")
        nextPictureButton.setIconSize(self.getButtonSize())
        nextPictureButton.setFixedSize(self.getButtonSize())
        navigationLayout.addWidget(nextPictureButton)

        finishedButton = QPushButton()
        finishedButton.clicked.connect(self.finishedPageEvent)
        finishedButton.setStyleSheet("qproperty-icon: url(" + CfgService.get(CfgKey.PAGE_PICTUREEDIT_FINISHED_BUTTON_ICON_DIR) + ");")
        finishedButton.setIconSize(self.getButtonSize())
        finishedButton.setFixedSize(self.getButtonSize())
        navigationLayout.addWidget(finishedButton)

    def executeBefore(self):
        self.showPrinterButtonIfActivated()
        self.updatePicture()

    def showPrinterButtonIfActivated(self):
        printerIsActiv = CfgService.get(CfgKey.PRINTER_IS_ACTIVE)
        if not printerIsActiv:
            self.printButton.setDisabled(True)
            self.printButton.setStyleSheet("qproperty-icon: url(" + CfgService.get(CfgKey.PAGE_PICTUREEDIT_PRINT_BUTTON_DISABLED_ICON_DIR) + ");")

    def updatePicture(self):
        picturePixelMap = QPixmap(ShottedPictureService.getTempPicturePath())
        self.picture.setPixmap(picturePixelMap.scaled(self.getPictureSize(),Qt.KeepAspectRatio))

    def getButtonSize(self):
        return QSize(self.windowsize.height()/self.heightDevider,self.windowsize.height()/self.heightDevider)

    def getPictureSize(self):
        return QSize(self.windowsize.width(), (self.windowsize.height()/self.heightDevider)*(self.heightDevider-1))

    def setFinishedPage(self,page):
        self.finishedPage=page

    def finishedPageEvent(self):
        self.setPageEvent(self.finishedPage)

    def setNewPicturePage(self,page):
        self.newPicturePage = page

    def newPicturePageEvent(self):
        self.setPageEvent(self.newPicturePage)

    def setPrinterPage(self,page):
        self.picturePage = page

    def printPageEvent(self):
        self.setPictureIsUsed()
        self.setPageEvent(self.picturePage)

    def setDownloadPage(self,page):
        self.downloadPage = page

    def downloadPageEvent(self):
        self.setPictureIsUsed()
        self.setPageEvent(self.downloadPage)

    def setHelpPage(self,page):
        self.helpPage = page

    def helpPageEvent(self):
        self.setPageEvent(self.helpPage)

    def setPictureIsUsed(self):
        self.pictureIsUsed=True

    def resetPictureIdUsed(self):
        self.pictureIsUsed=False