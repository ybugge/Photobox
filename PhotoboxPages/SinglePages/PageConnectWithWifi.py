import io

import qrcode
from PIL import Image, ImageFont, ImageDraw
from PyQt5.QtCore import QSize, Qt
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QVBoxLayout, QHBoxLayout, QPushButton, QLabel

from PhotoboxPages.AllPages import AllPages
from PhotoboxPages.Page import Page
from Services.CfgService import CfgService
from Services.GlobalPagesVariableService import GlobalPagesVariableService
from config.Config import TextKey, textValue, CfgKey

class PageConnectWithWifi(Page):
    def __init__(self, pages : AllPages, windowsize:QSize, globalVariable:GlobalPagesVariableService):
        super().__init__(pages,windowsize)
        self.windowsize = windowsize
        self.globalVariable = globalVariable
        self.switch = False

        mainLayout = QVBoxLayout()
        mainLayout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(mainLayout)

        #Titel
        self.title = self.getTitleAsQLabel(TextKey.PAGE_DOWNLOADPICTURE_WIFI_TITLE)
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

        backButton = QPushButton(textValue[TextKey.PAGE_DOWNLOADPICTURE_BACKBUTTON])
        backButton.clicked.connect(self.backPageEvent)
        self.setNavigationbuttonStyle(backButton)
        navigationLayout.addWidget(backButton)

    def executeBefore(self):
        self.updateQrCodePicture()
        self.globalVariable.setPictureUsed(True)

    def updateQrCodePicture(self):
        #QRCode

        data = 'WIFI:S:{};T:{};P:{};;'.format(CfgService.get(CfgKey.WIFI_SSID),CfgService.get(CfgKey.WIFI_PROTOCOL),CfgService.get(CfgKey.WIFI_PASSWORD))

        buf = io.BytesIO()
        qr_code = qrcode.make(data)
        img = Image.new("RGB", (qr_code.pixel_size,qr_code.pixel_size), "white")
        img.paste(qr_code,(0,0))
        img = img.resize((qr_code.pixel_size*2,qr_code.pixel_size*2))


        fontSize = 40
        myFont = ImageFont.truetype(CfgService.get(CfgKey.WIFI_QR_CODE_FONT), fontSize)
        title = ImageDraw.Draw(img)
        title.text((20, 20), textValue[TextKey.QR_CODE_WIFI_NAME]+CfgService.get(CfgKey.WIFI_SSID),font=myFont, fill=(0, 0, 0))

        password = ImageDraw.Draw(img)
        witheSpaceNumber = 4
        unformatedPasswordAsString = CfgService.get(CfgKey.WIFI_PASSWORD)
        formatedPasswordAsString = " ".join(unformatedPasswordAsString[i:i+witheSpaceNumber] for i,c in enumerate(unformatedPasswordAsString) if i % witheSpaceNumber == 0)
        password.text((20, qr_code.pixel_size*2-20-fontSize), textValue[TextKey.QR_CODE_WIFI_PASSWORD]+formatedPasswordAsString,font=myFont, fill=(0, 0, 0))
        img.save(buf, "PNG")

        qt_pixmap = QPixmap()
        qt_pixmap.loadFromData(buf.getvalue(), "PNG")

        qt_scaled_pixmap = qt_pixmap.scaled(self.qrStyle(),Qt.KeepAspectRatio)
        self.qrCodePicture.setPixmap(qt_scaled_pixmap)

    def qrStyle(self):
        devider = 2.5
        widthHeight = self.windowsize.width()/devider
        return QSize(widthHeight,widthHeight)