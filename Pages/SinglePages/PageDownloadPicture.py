import io

import qrcode
from PyQt5.QtCore import QSize, Qt
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QVBoxLayout, QHBoxLayout, QPushButton, QLabel

from Pages.AllPages import AllPages
from Pages.Page import Page
from Services.CfgService import CfgService
from Services.GlobalPagesVariableService import GlobalPagesVariableService
from Services.PageDbService import PageDbSevice
from Services.ShottedPictureService import ShottedPictureService
from config.Config import TextKey, textValue, CfgKey


class PageDownloadPicture(Page):
    def __init__(self, pages : AllPages, windowsize:QSize, globalVariable:GlobalPagesVariableService):
        super().__init__(pages)
        self.windowsize = windowsize
        self.globalVariable = globalVariable

        mainLayout = QVBoxLayout()
        self.setLayout(mainLayout)

        #Titel
        mainLayout.addWidget(self.getTitleAsQLabel(TextKey.PAGE_DOWNLOADPICTURE_TITLE))
        mainLayout.addStretch()

        #Picture
        self.qrCodePicture = QLabel()
        self.qrCodePicture.setAlignment(Qt.AlignCenter)
        self.qrCodePicture.setText("")
        mainLayout.addWidget(self.qrCodePicture)

        #Navigation
        mainLayout.addStretch()
        navigationLayout=QHBoxLayout()
        mainLayout.addLayout(navigationLayout)

        backButton = QPushButton(textValue[TextKey.PAGE_DOWNLOADPICTURE_BACKBUTTON])
        backButton.clicked.connect(self.backPageEvent)
        navigationLayout.addWidget(backButton)

    def executeBefore(self):
        self.updateQrCodePicture()

    def executeInAutoForwardTimerEvent(self):
        pictureTargetPath = ShottedPictureService.saveUsedPicture(self.globalVariable.getPictureSubName())
        PageDbSevice.updatePicture(self.globalVariable,pictureTargetPath)

    def updateQrCodePicture(self):
        #QRCode
        data = "http://"+CfgService.get(CfgKey.SERVER_IP)+":"+CfgService.get(CfgKey.SERVER_PORT)+CfgService.get(CfgKey.SERVER_DOWNLOAD_PICTURE_PAGE)+"/"+self.globalVariable.getPictureSubName()
        buf = io.BytesIO()
        img = qrcode.make(data)
        img.save(buf, "PNG")

        qt_pixmap = QPixmap()
        qt_pixmap.loadFromData(buf.getvalue(), "PNG")

        qt_scaled_pixmap = qt_pixmap.scaled(self.qrStyle(),Qt.KeepAspectRatio)
        self.qrCodePicture.setPixmap(qt_scaled_pixmap)

    def qrStyle(self):
        devider = 2.5
        widthHeight = self.windowsize.width()/devider
        return QSize(widthHeight,widthHeight)