import io

import qrcode
from PyQt5.QtCore import QSize, Qt
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QVBoxLayout, QHBoxLayout, QPushButton, QLabel

from Pages.AllPages import AllPages
from Pages.Page import Page
from Services.FileFolderService import FileFolderService
from Services.GlobalPagesVariableService import GlobalPagesVariableService
from config.Config import TextKey, textValue


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

        backButton = QPushButton()
        backButton = QPushButton(textValue[TextKey.PAGE_DOWNLOADPICTURE_BACKBUTTON])
        backButton.clicked.connect(self.backPageEvent)
        navigationLayout.addWidget(backButton)

    def executeBefore(self):
        self.updateQrCodePicture()

    def executeAfterStopAutoForwardTimer(self):
        FileFolderService.saveUsedPicture(self.globalVariable.getPictureSubName())

    def updateQrCodePicture(self):
        #QRCode
        data = "https://www.wikipedia.com"

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