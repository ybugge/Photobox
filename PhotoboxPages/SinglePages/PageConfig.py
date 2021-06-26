import qrcode
from PyQt5.QtCore import QSize, Qt
from PyQt5.QtGui import QFont, QColor
from PyQt5.QtWidgets import QPushButton, QVBoxLayout, QLabel, QHBoxLayout, QFileDialog, QGridLayout, QLineEdit, QWidget, \
    QScrollArea, QComboBox

from PhotoboxPages.AllPages import AllPages
from PhotoboxPages.Page import Page
from Services.CfgService import CfgService
from Services.PrinterService import PrinterService
from config.Config import textValue, TextKey, CfgKey


class PageConfig(Page):
    def __init__(self, pages : AllPages, windowSize:QSize, printerService:PrinterService):
        super().__init__(pages,windowSize)
        mainLayout = QVBoxLayout()
        mainLayout.setContentsMargins(0, 0, 0, 0)
        self.printerService = printerService
        self.setLayout(mainLayout)

        #Titel
        mainLayout.addWidget(self.getTitleAsQLabel(TextKey.PAGE_CONFIG_TITLE))

        #Configs #######################################################################################################
        #Layout
        scroll_area_content_widget = QWidget()
        self.scroll_area = QScrollArea(self)
        self.scroll_area.setGeometry(0, 0, windowSize.width(), windowSize.height())
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.scroll_area.setWidget(scroll_area_content_widget)

        mainContentLabel = QVBoxLayout()
        scroll_area_content_widget.setLayout(mainContentLabel)
        mainLayout.addWidget(self.scroll_area)

            #mainSaveDir
        titleFont = QFont()
        titleFont.setUnderline(True)
        mainSaveDirTitle = QLabel(textValue[TextKey.PAGE_CONFIG_MAIN_SAVE_DIR_TITLE])
        mainSaveDirTitle.setFont(titleFont)
        mainContentLabel.addWidget(mainSaveDirTitle)

        mainSaveDirLayout= QGridLayout()
        mainContentLabel.addLayout(mainSaveDirLayout)

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
        mainContentLabel.addWidget(projectNameTitle)

        self.projectNameValue = QLineEdit()
        self.projectNameValue.setText(CfgService.get(CfgKey.PROJECTNAME))
        mainContentLabel.addWidget(self.projectNameValue)

            #Camera calibration
        cameraCalibration = QPushButton(textValue[TextKey.PAGE_CONFIG_CAMERA_CALIBRATION_BUTTON])
        cameraCalibration.clicked.connect(self.cameraCalibrationEvent)
        self.setContentButtonStyle(cameraCalibration)
        mainContentLabel.addWidget(cameraCalibration)

            #Server
        serverTitle = QLabel(textValue[TextKey.PAGE_CONFIG_SERVER_IPANDPORT_TITLE])
        serverTitle.setFont(titleFont)
        mainContentLabel.addWidget(serverTitle)

        serverLayout = QHBoxLayout()
        mainContentLabel.addLayout(serverLayout)
        self.serverIpValue = QLineEdit()
        self.serverIpValue.setText(CfgService.get(CfgKey.SERVER_IP))
        serverLayout.addWidget(self.serverIpValue)

        self.serverPortValue = QLineEdit()
        self.serverPortValue.setText(CfgService.get(CfgKey.SERVER_PORT))
        serverLayout.addWidget(self.serverPortValue)

            #WIFI
        wifiTitle = QLabel(textValue[TextKey.PAGE_CONFIG_WIFI_TITLE])
        wifiTitle.setFont(titleFont)
        mainContentLabel.addWidget(wifiTitle)

        serverLayout = QHBoxLayout()
        mainContentLabel.addLayout(serverLayout)
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
        self.setContentButtonStyle(wifiPicture)
        mainContentLabel.addWidget(wifiPicture)

        # Printer -------------------------------------------------------------------------------
        printerTitle = QLabel(textValue[TextKey.PAGE_CONFIG_PRINTER_TITLE])
        printerTitle.setFont(titleFont)
        mainContentLabel.addWidget(printerTitle)

        # Printer enabled?
        printerDisabledLayout = QHBoxLayout()
        mainContentLabel.addLayout(printerDisabledLayout)

        self.printerDisabledLabel = QLabel()
        self.printerDisabledLabel.setText(textValue[TextKey.PAGE_CONFIG_SERVICE_STATUS])
        printerDisabledLayout.addWidget(self.printerDisabledLabel)

        self.printerDisabledButton = QPushButton()
        self.printerDisabledButton.setCheckable(True)
        isPrinterActivate = CfgService.get(CfgKey.PRINTER_IS_ACTIVE)
        self.printerDisabledButton.setChecked(isPrinterActivate)
        if isPrinterActivate:
            self.printerDisabledButton.setText(textValue[TextKey.PAGE_CONFIG_AKTIVATE])
        else:
            self.printerDisabledButton.setText(textValue[TextKey.PAGE_CONFIG_INAKTIVATE])
        self.printerDisabledButton.clicked.connect(self.activatePrinter)
        printerDisabledLayout.addWidget(self.printerDisabledButton)

            #Aktiviert Printer Web
        printerDisabledWebLayout = QHBoxLayout()
        mainContentLabel.addLayout(printerDisabledWebLayout)

        printerDisabledWebLabel = QLabel()
        printerDisabledWebLabel.setText(textValue[TextKey.PAGE_CONFIG_SERVICE_PRINTER_WEB])
        printerDisabledWebLayout.addWidget(printerDisabledWebLabel)

        self.printerDisabledWebButton = QPushButton()
        self.printerDisabledWebButton.setCheckable(True)
        isPrinterActivateWeb = CfgService.get(CfgKey.PRINTER_IS_ACTIVE_WEB)
        self.printerDisabledWebButton.setChecked(isPrinterActivateWeb)
        if isPrinterActivateWeb:
            self.printerDisabledWebButton.setText(textValue[TextKey.PAGE_CONFIG_AKTIVATE])
        else:
            self.printerDisabledWebButton.setText(textValue[TextKey.PAGE_CONFIG_INAKTIVATE])
        self.printerDisabledWebButton.clicked.connect(self.activatePrinterWeb)
        printerDisabledWebLayout.addWidget(self.printerDisabledWebButton)

            # Selected Printer
        printerSelectedLayout = QHBoxLayout()
        mainContentLabel.addLayout(printerSelectedLayout)

        printerSelectLabel = QLabel()
        printerSelectLabel.setText(textValue[TextKey.PAGE_CONFIG_PRINTER_SELECT_LABEL])
        printerSelectedLayout.addWidget(printerSelectLabel)

        self.printerSelectedComboBox = QComboBox()
        for printer in printerService.getPrinters():
            self.printerSelectedComboBox.addItem(str(printer))
        self.printerSelectedComboBox.currentIndexChanged.connect(self.selectionchangePrinter)
        printerSelectedLayout.addWidget(self.printerSelectedComboBox)

            #Paper format
        printerPaperFormatLayout = QHBoxLayout()
        mainContentLabel.addLayout(printerPaperFormatLayout)

        printerPaperFormatLabel = QLabel()
        printerPaperFormatLabel.setText(textValue[TextKey.PAGE_CONFIG_PRINTER_PAPER_FORMAT_LABEL])
        printerPaperFormatLayout.addWidget(printerPaperFormatLabel)

        printerPaperFormatValue = QLineEdit()
        printerPaperFormatValue.setText(CfgService.get(CfgKey.PRINTER_PAPER_FORMAT))
        printerPaperFormatValue.setReadOnly(True)
        printerPaperFormatLayout.addWidget(printerPaperFormatValue)

            #Printer hint -> startup the printer!
        printerHintLabel = QLabel()
        printerHintLabel.setText(textValue[TextKey.PAGE_CONFIG_PRINTER_POWER_ON_HINT])
        mainContentLabel.addWidget(printerHintLabel)

        # Greenscreen -------------------------------------------------------------------------------
        greenscreenTitle = QLabel(textValue[TextKey.PAGE_CONFIG_GREENSCREEN_TITLE])
        greenscreenTitle.setFont(titleFont)
        mainContentLabel.addWidget(greenscreenTitle)

            # Greenscreen enabled?
        greenscreenDisabledLayout = QHBoxLayout()
        mainContentLabel.addLayout(greenscreenDisabledLayout)

        self.greenscreenDisabledLabel = QLabel()
        self.greenscreenDisabledLabel.setText(textValue[TextKey.PAGE_CONFIG_SERVICE_STATUS])
        greenscreenDisabledLayout.addWidget(self.greenscreenDisabledLabel)

        self.greenscreenDisabledButton = QPushButton()
        self.greenscreenDisabledButton.setCheckable(True)
        self.greenscreenDisabledButton.clicked.connect(self.activateGreenscreen)
        greenscreenDisabledLayout.addWidget(self.greenscreenDisabledButton)

            #Greenscreen ColorPicker
        greenscreenColorPickerButton = QPushButton()
        greenscreenColorPickerButton.setText(textValue[TextKey.PAGE_CONFIG_GREENSCREEN_COLOR_PICER_BUTTON])
        greenscreenColorPickerButton.clicked.connect(self.greenscreenColorPickerEvent)
        mainContentLabel.addWidget(greenscreenColorPickerButton)

        greenscreenAverageColorLayout = QHBoxLayout()
        mainContentLabel.addLayout(greenscreenAverageColorLayout)

        greenscreenAverageColorLabel = QLabel()
        greenscreenAverageColorLabel.setText(textValue[TextKey.PAGE_CONFIG_GREENSCREEN_AVERAGE_COLOR_LABEL])
        greenscreenAverageColorLayout.addWidget(greenscreenAverageColorLabel)

        self.averageColorLabel = QLineEdit()
        self.averageColorLabel.setReadOnly(True)
        greenscreenAverageColorLayout.addWidget(self.averageColorLabel)

        #Navigation   ##################################################################################################
        mainContentLabel.addStretch()
        navigationLayout = QHBoxLayout()
        mainLayout.addLayout(navigationLayout)

        backButton = QPushButton(textValue[TextKey.PAGE_CONFIG_BACKBUTTON])
        backButton.clicked.connect(self.backPageEvent)
        self.setNavigationbuttonStyle(backButton)
        navigationLayout.addWidget(backButton)

        nextButton = QPushButton(textValue[TextKey.PAGE_CONFIG_NEXTBUTTON])
        nextButton.clicked.connect(self.nextPageEvent)
        self.setNavigationbuttonStyle(nextButton)
        navigationLayout.addWidget(nextButton)

    def executeBefore(self):
        self.updateUiPrintingPossible()
        self.setPrinterFromProperties()
        self.updateGreenscreenColor()
        self.updateGreenscreenActive()

    def updateGreenscreenActive(self):
        isGreenscreenActivate = CfgService.get(CfgKey.GREENSCREEN_IS_ACTIVE)
        self.greenscreenDisabledButton.setChecked(isGreenscreenActivate)
        if isGreenscreenActivate:
            self.greenscreenDisabledButton.setText(textValue[TextKey.PAGE_CONFIG_AKTIVATE])
        else:
            self.greenscreenDisabledButton.setText(textValue[TextKey.PAGE_CONFIG_INAKTIVATE])

    def updateGreenscreenColor(self):
        averageGreenscreenQColor = CfgService.getColor(CfgKey.GREENSCREEN_AVERAGE_HSV_GUI_COLOR)
        averageGreenscreenCv2ColorText = CfgService.getIntList(CfgKey.GREENSCREEN_AVERAGE_HSV_CV2_COLOR)
        self.averageColorLabel.setText(str(averageGreenscreenCv2ColorText))
        self.averageColorLabel.setStyleSheet("background-color:rgb("+str(averageGreenscreenQColor.getRgb()[0])+","+str(averageGreenscreenQColor.getRgb()[1])+","+str(averageGreenscreenQColor.getRgb()[2])+")")


    def updateUiPrintingPossible(self):
        if not self.printerService.printingPosible():
            CfgService.set(CfgKey.PRINTER_IS_ACTIVE,False)
            self.printerDisabledButton.setText(textValue[TextKey.PAGE_CONFIG_INAKTIVATE])
            self.printerDisabledButton.setChecked(CfgService.get(CfgKey.PRINTER_IS_ACTIVE))
            self.printerDisabledButton.setDisabled(True)


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

    def activatePrinter(self):
        if self.printerDisabledButton.isChecked():
            CfgService.set(CfgKey.PRINTER_IS_ACTIVE,True)
            self.printerDisabledButton.setText(textValue[TextKey.PAGE_CONFIG_AKTIVATE])
            self.printerDisabledButton.setChecked(CfgService.get(CfgKey.PRINTER_IS_ACTIVE))
        else:
            CfgService.set(CfgKey.PRINTER_IS_ACTIVE,False)
            self.printerDisabledButton.setText(textValue[TextKey.PAGE_CONFIG_INAKTIVATE])
            self.printerDisabledButton.setChecked(CfgService.get(CfgKey.PRINTER_IS_ACTIVE))

    def activatePrinterWeb(self):
        if self.printerDisabledWebButton.isChecked():
            CfgService.set(CfgKey.PRINTER_IS_ACTIVE_WEB,True)
            self.printerDisabledWebButton.setText(textValue[TextKey.PAGE_CONFIG_AKTIVATE])
            self.printerDisabledWebButton.setChecked(CfgService.get(CfgKey.PRINTER_IS_ACTIVE_WEB))
        else:
            CfgService.set(CfgKey.PRINTER_IS_ACTIVE_WEB,False)
            self.printerDisabledWebButton.setText(textValue[TextKey.PAGE_CONFIG_INAKTIVATE])
            self.printerDisabledWebButton.setChecked(CfgService.get(CfgKey.PRINTER_IS_ACTIVE_WEB))

    def selectionchangePrinter(self,index):
        printers = self.printerService.getPrinters()
        if len(printers) > index:
            CfgService.set(CfgKey.PRINTER_SELECTED,str(list(printers)[index]))
        else:
            self.setDefaultPrinter(printers)

    def setPrinterFromProperties(self):
        selectedPrinterAsString = CfgService.get(CfgKey.PRINTER_SELECTED)
        printers = self.printerService.getPrinters()
        if selectedPrinterAsString == None and len(printers) > 0:
            self.setDefaultPrinter(printers)
        elif selectedPrinterAsString != None and len(printers) > 0:
            selectedPrinterAsKey = self.findPrinterIndexByString(printers, selectedPrinterAsString)
            if selectedPrinterAsKey == None:
                self.setDefaultPrinter(printers)
            else:
                self.printerSelectedComboBox.setCurrentIndex(selectedPrinterAsKey)


    def setDefaultPrinter(self,printers):
        firstPrinter = list(printers)[0]
        CfgService.set(CfgKey.PRINTER_SELECTED,str(firstPrinter))
        self.printerSelectedComboBox.setCurrentIndex(0)

    def findPrinterIndexByString(self, printers, keyAsString:str):
        counter = 0
        for printerKey in printers:
            if keyAsString == str(printerKey):
                return counter
            counter +=1
        return None

    #greenscreen
    def setGreenscreenColorPickerEventPage(self,page):
        self.greenscreenColorPickerPage = page

    def greenscreenColorPickerEvent(self):
        self.setPageEvent(self.greenscreenColorPickerPage)

    def activateGreenscreen(self):
        if self.greenscreenDisabledButton.isChecked():
            CfgService.set(CfgKey.GREENSCREEN_IS_ACTIVE,True)
            self.greenscreenDisabledButton.setText(textValue[TextKey.PAGE_CONFIG_AKTIVATE])
            self.greenscreenDisabledButton.setChecked(CfgService.get(CfgKey.GREENSCREEN_IS_ACTIVE))
        else:
            CfgService.set(CfgKey.GREENSCREEN_IS_ACTIVE,False)
            self.greenscreenDisabledButton.setText(textValue[TextKey.PAGE_CONFIG_INAKTIVATE])
            self.greenscreenDisabledButton.setChecked(CfgService.get(CfgKey.GREENSCREEN_IS_ACTIVE))