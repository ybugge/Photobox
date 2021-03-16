import qrcode
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QPushButton, QVBoxLayout, QLabel, QHBoxLayout, QFileDialog, QGridLayout, QLineEdit

from Pages.AllPages import AllPages
from Pages.Page import Page
from Services.CfgService import CfgService
from config.Config import textValue, TextKey, CfgKey


class PageConfig(Page):
    def __init__(self, pages : AllPages):
        super().__init__(pages)
        vbox = QVBoxLayout()
        self.setLayout(vbox)

        #Titel
        vbox.addWidget(self.getTitleAsQLabel(TextKey.PAGE_CONFIG_TITLE))

        #Configs ############################################################
            #mainSaveDir
        titleFont = QFont()
        titleFont.setUnderline(True)
        mainSaveDirTitle = QLabel(textValue[TextKey.PAGE_CONFIG_MAIN_SAVE_DIR_TITLE])
        mainSaveDirTitle.setFont(titleFont)
        vbox.addWidget(mainSaveDirTitle)

        mainSaveDirLayout= QGridLayout()
        vbox.addLayout(mainSaveDirLayout)

        self.mainSaveDirLabel = QLineEdit()
        self.mainSaveDirLabel.setText(CfgService.get(CfgKey.MAIN_SAVE_DIR))
        self.mainSaveDirLabel.setReadOnly(True)
        mainSaveDirLayout.addWidget(self.mainSaveDirLabel,0,0)

        dirButton = QPushButton("...")
        dirButton.clicked.connect(self.open_file_dialog)
        mainSaveDirLayout.addWidget(dirButton,0,3)

            #ProjectName
        projectNameTitle = QLabel(textValue[TextKey.PAGE_CONFIG_PROJECT_NAME_TITLE])
        projectNameTitle.setFont(titleFont)
        vbox.addWidget(projectNameTitle)

        self.projectNameValue = QLineEdit()
        self.projectNameValue.setText(CfgService.get(CfgKey.PROJECTNAME))
        vbox.addWidget(self.projectNameValue)

            #Camera calibration
        cameraCalibration = QPushButton(textValue[TextKey.PAGE_CONFIG_CAMERA_CALIBRATION_BUTTON])
        cameraCalibration.clicked.connect(self.cameraCalibrationEvent)
        vbox.addWidget(cameraCalibration)

            #Server
        serverTitle = QLabel(textValue[TextKey.PAGE_CONFIG_SERVER_IPANDPORT_TITLE])
        serverTitle.setFont(titleFont)
        vbox.addWidget(serverTitle)

        serverLayout = QHBoxLayout()
        vbox.addLayout(serverLayout)
        self.serverIpValue = QLineEdit()
        self.serverIpValue.setText(CfgService.get(CfgKey.SERVER_IP))
        serverLayout.addWidget(self.serverIpValue)

        self.serverPortValue = QLineEdit()
        self.serverPortValue.setText(CfgService.get(CfgKey.SERVER_PORT))
        serverLayout.addWidget(self.serverPortValue)

            #WIFI
        wifiTitle = QLabel(textValue[TextKey.PAGE_CONFIG_WIFI_TITLE])
        wifiTitle.setFont(titleFont)
        vbox.addWidget(wifiTitle)

        serverLayout = QHBoxLayout()
        vbox.addLayout(serverLayout)
        self.wifiSSIDValue = QLineEdit()
        self.wifiSSIDValue.setText(CfgService.get(CfgKey.WIFI_SSID))
        serverLayout.addWidget(self.wifiSSIDValue)

        self.wifiPasswordValue = QLineEdit()
        self.wifiPasswordValue.setText(CfgService.get(CfgKey.WIFI_PASSWORD))
        serverLayout.addWidget(self.wifiPasswordValue)

        self.wifiProtocolValue = QLineEdit()
        self.wifiProtocolValue.setText(CfgService.get(CfgKey.WIFI_PROTOCOL))
        serverLayout.addWidget(self.wifiProtocolValue)

        wifiPicture = QPushButton(textValue[TextKey.PAGE_CONFIG_WIFI_PICTURE_BUTTON])
        wifiPicture.clicked.connect(self.saveWifiPicture)
        vbox.addWidget(wifiPicture)

        vbox.addStretch()
        #Navigation
        navigationLayout = QHBoxLayout()
        vbox.addLayout(navigationLayout)

        backButton = QPushButton(textValue[TextKey.PAGE_CONFIG_BACKBUTTON])
        backButton.clicked.connect(self.backPageEvent)
        navigationLayout.addWidget(backButton)

        nextButton = QPushButton(textValue[TextKey.PAGE_CONFIG_NEXTBUTTON])
        nextButton.clicked.connect(self.nextPageEvent)
        navigationLayout.addWidget(nextButton)

    def executeAfter(self):
        CfgService.set(CfgKey.MAIN_SAVE_DIR, self.mainSaveDirLabel.text())
        CfgService.set(CfgKey.PROJECTNAME, self.projectNameValue.text())
        CfgService.set(CfgKey.SERVER_IP, self.serverIpValue.text())
        CfgService.set(CfgKey.SERVER_PORT,self.serverPortValue.text())
        CfgService.set(CfgKey.WIFI_SSID,self.wifiSSIDValue.text())
        CfgService.set(CfgKey.WIFI_PROTOCOL,self.wifiProtocolValue.text())
        CfgService.set(CfgKey.WIFI_PASSWORD,self.wifiPasswordValue.text())

    def open_file_dialog(self):
        CfgService.set(CfgKey.MAIN_SAVE_DIR, str(QFileDialog.getExistingDirectory()))
        self.mainSaveDirLabel.setText(CfgService.get(CfgKey.MAIN_SAVE_DIR))

    def setCameraCalibrationEventPage(self,page):
        self.cameraCalibrationPage = page

    def cameraCalibrationEvent(self):
        self.setPageEvent(self.cameraCalibrationPage)

    def saveWifiPicture(self):
        qrCodeValue = 'WIFI:S:{};T:{};P:{};;'.format(self.wifiSSIDValue.text(),self.wifiProtocolValue.text(),self.wifiPasswordValue.text())
        img = qrcode.make(qrCodeValue)
        img.save(self.mainSaveDirLabel.text()+"/"+CfgService.get(CfgKey.WIFI_PICTURE_NAME))