import io

import qrcode
from PyQt5.QtCore import QSize, Qt
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QVBoxLayout, QHBoxLayout, QPushButton, QLabel

from PhotoboxPages.AllPages import AllPages
from PhotoboxPages.Page import Page
from Services.CfgService import CfgService
from Services.Db.PageDbService import PageDbSevice
from Services.GlobalPagesVariableService import GlobalPagesVariableService
from Services.Greenscreen.GreenscreenBackgroundService import GreenscreenBackgroundService
from config.Config import TextKey, textValue, CfgKey


class PageGreenscreenUploadBackground(Page):
    def __init__(self, pages : AllPages, windowsize:QSize, globalVariable:GlobalPagesVariableService):
        super().__init__(pages,windowsize)
        self.windowsize = windowsize
        self.globalVariable = globalVariable
        self.switch = False

        mainLayout = QVBoxLayout()
        mainLayout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(mainLayout)

        #Titel
        self.title = self.getTitleAsQLabel(TextKey.PAGE_GREENSCREEN_UPLOAD_BACKGROUND_TITLE)
        mainLayout.addWidget(self.title)
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

        backButton = QPushButton(textValue[TextKey.PAGE_GREENSCREEN_UPLOAD_BACKGROUND_BACK_BUTTON])
        backButton.clicked.connect(self.backPageEvent)
        self.setNavigationbuttonStyle(backButton)
        navigationLayout.addWidget(backButton)

        self.switchButton = QPushButton(textValue[TextKey.PAGE_DOWNLOADPICTURE_WIFI_TITLE])
        self.switchButton.clicked.connect(self._switchEvent)
        self.setNavigationbuttonStyle(self.switchButton)
        navigationLayout.addWidget(self.switchButton)

    def executeBefore(self):
        self.uuid = PageDbSevice.setBackgroundUploadAuthorization(True, GreenscreenBackgroundService.getCustomBackgroundPath())
        self._updateQrCodePicture()

    def executeAfter(self):
        greenscreenBackgroundService = GreenscreenBackgroundService(self.globalVariable);
        greenscreenBackgroundService.appendCustomBackground(GreenscreenBackgroundService.getCustomBackgroundPath(),self.uuid)
        PageDbSevice.clearBackgroundUploadAuthorization()


    def _switchEvent(self):
        self.switch = not self.switch
        if self.switch:
            self.switchButton.setText(textValue[TextKey.PAGE_GREENSCREEN_UPLOAD_BACKGROUND_TITLE])
            self.title.setText(textValue[TextKey.PAGE_GREENSCREEN_UPLOAD_BACKGROUND_WIFI_TITLE])
            self._updateQrCodePicture()
        else:
            self.switchButton.setText(textValue[TextKey.PAGE_GREENSCREEN_UPLOAD_BACKGROUND_WIFI_TITLE])
            self.title.setText(textValue[TextKey.PAGE_GREENSCREEN_UPLOAD_BACKGROUND_TITLE])
            self._updateQrCodePicture()

    def _updateQrCodePicture(self):
        #QRCode
        if self.switch:
            data = 'WIFI:S:{};T:{};P:{};;'.format(CfgService.get(CfgKey.WIFI_SSID),CfgService.get(CfgKey.WIFI_PROTOCOL),CfgService.get(CfgKey.WIFI_PASSWORD))
        else:
            data = "http://"+CfgService.get(CfgKey.SERVER_IP)+":"+CfgService.get(CfgKey.SERVER_PORT)+CfgService.get(CfgKey.SERVER_UPLOAD_PICTURE)+"/"+self.uuid

        buf = io.BytesIO()
        img = qrcode.make(data)
        img.save(buf, "PNG")

        qt_pixmap = QPixmap()
        qt_pixmap.loadFromData(buf.getvalue(), "PNG")

        qt_scaled_pixmap = qt_pixmap.scaled(self._qrStyle(),Qt.KeepAspectRatio)
        self.qrCodePicture.setPixmap(qt_scaled_pixmap)

    def _qrStyle(self):
        devider = 2.5
        widthHeight = self.windowsize.width()/devider
        return QSize(widthHeight,widthHeight)