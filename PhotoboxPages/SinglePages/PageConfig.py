import qrcode
from PIL import ImageDraw, Image, ImageFont
from PyQt5.QtCore import QSize, Qt
from PyQt5.QtGui import QFont, QColor, QDoubleValidator, QIntValidator
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

        # Camera  -------------------------------------------------------------------------------
        cameraTitle = QLabel(textValue[TextKey.PAGE_CONFIG_CAMERA_TITLE])
        cameraTitle.setFont(titleFont)
        mainContentLabel.addWidget(cameraTitle)

            #Camera calibration
        cameraCalibration = QPushButton(textValue[TextKey.PAGE_CONFIG_CAMERA_CALIBRATION_BUTTON])
        cameraCalibration.clicked.connect(self.cameraCalibrationEvent)
        self.setContentButtonStyle(cameraCalibration)
        mainContentLabel.addWidget(cameraCalibration)

            #Camera Brightness
        cameraAutoBrightnessLayout = QHBoxLayout()
        mainContentLabel.addLayout(cameraAutoBrightnessLayout)

        self.cameraAutoBrightnessLabel = QLabel()
        self.cameraAutoBrightnessLabel.setText(textValue[TextKey.PAGE_CONFIG_CAMERA_STATIC_BRIGHTNESS_TITLE])
        cameraAutoBrightnessLayout.addWidget(self.cameraAutoBrightnessLabel)

        self.cameraAutoBrightnessButton = QPushButton()
        self.cameraAutoBrightnessButton.setCheckable(True)
        self.cameraAutoBrightnessButton.clicked.connect(self.activateCameraAutoBrightness)
        cameraAutoBrightnessLayout.addWidget(self.cameraAutoBrightnessButton)

            #Camera Brightness Gains
                #Brightness -> TODO: Fehler -> Die Helligkeit ändert sich dynamisch und bleibt nicht statisch | Deswegen raus genommen
        brightnessValueValidator = QIntValidator(0,100)
        cameraAutoBrightnessStaticValueLayout = QHBoxLayout()
        #mainContentLabel.addLayout(cameraAutoBrightnessStaticValueLayout)

        self.cameraBrightnessStaticValueLabel = QLabel()
        self.cameraBrightnessStaticValueLabel.setText(textValue[TextKey.PAGE_CONFIG_CAMERA_STATIC_BRIGHTNESS_VALUE_TITLE])
        cameraAutoBrightnessStaticValueLayout.addWidget(self.cameraBrightnessStaticValueLabel)

        self.cameraBrightnessStaticValue = QLineEdit()
        self.cameraBrightnessStaticValue.setValidator(brightnessValueValidator)
        self.cameraBrightnessStaticValue.setText(str(CfgService.get(CfgKey.PI_CAMERA_STATIC_BRIGHTNESS_STATIC_VALUE)))
        cameraAutoBrightnessStaticValueLayout.addWidget(self.cameraBrightnessStaticValue)

        gainValidator = QDoubleValidator(0,8,1)
                #Red
        cameraAutoBrightnessGainRedLayout = QHBoxLayout()
        mainContentLabel.addLayout(cameraAutoBrightnessGainRedLayout)

        self.cameraBrightnessGainRedLabel = QLabel()
        self.cameraBrightnessGainRedLabel.setText(textValue[TextKey.PAGE_CONFIG_CAMERA_BRIGHTNESS_GAIN_RED])
        cameraAutoBrightnessGainRedLayout.addWidget(self.cameraBrightnessGainRedLabel)

        self.cameraBrightnessGainRed = QLineEdit()
        self.cameraBrightnessGainRed.setValidator(gainValidator)
        self.cameraBrightnessGainRed.setText(str(CfgService.get(CfgKey.PI_CAMERA_STATIC_BRIGHTNESS_AWB_GAIN_RED)))
        cameraAutoBrightnessGainRedLayout.addWidget(self.cameraBrightnessGainRed)

            #Blue
        cameraAutoBrightnessGainBlueLayout = QHBoxLayout()
        mainContentLabel.addLayout(cameraAutoBrightnessGainBlueLayout)

        self.cameraBrightnessGainBlueLabel = QLabel()
        self.cameraBrightnessGainBlueLabel.setText(textValue[TextKey.PAGE_CONFIG_CAMERA_BRIGHTNESS_GAIN_BLUE])
        cameraAutoBrightnessGainBlueLayout.addWidget(self.cameraBrightnessGainBlueLabel)

        self.cameraBrightnessGainBlue = QLineEdit()
        self.cameraBrightnessGainBlue.setValidator(gainValidator)
        self.cameraBrightnessGainBlue.setText(str(CfgService.get(CfgKey.PI_CAMERA_STATIC_BRIGHTNESS_AWB_GAIN_BLUE)))
        cameraAutoBrightnessGainBlueLayout.addWidget(self.cameraBrightnessGainBlue)

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

        # Server  ------------------------------------------------------------------------------- cfgValue[CfgKey.SERVER_INDEX_PAGE_SHOW_ALL_PICTURES] = True
        serverTitle = QLabel(textValue[TextKey.PAGE_CONFIG_SERVER_TITLE])
        serverTitle.setFont(titleFont)
        mainContentLabel.addWidget(serverTitle)

            # show all Picture in Index -> enabled?
        showAllPicturesOnIndexLayout = QHBoxLayout()
        mainContentLabel.addLayout(showAllPicturesOnIndexLayout)

        self.showAllPicturesOnIndexLabel = QLabel()
        self.showAllPicturesOnIndexLabel.setText(textValue[TextKey.PAGE_CONFIG_SERVER_SHOW_ALL_PICTURES_ON_INDEX])
        showAllPicturesOnIndexLayout.addWidget(self.showAllPicturesOnIndexLabel)

        self.showAllPicturesOnIndexButton = QPushButton()
        self.showAllPicturesOnIndexButton.setCheckable(True)
        self.showAllPicturesOnIndexButton.setChecked(True)
        self.showAllPicturesOnIndexButton.setText(textValue[TextKey.PAGE_CONFIG_AKTIVATE])
        self.showAllPicturesOnIndexButton.clicked.connect(self.activateShowAllPicturesOnIndex)
        showAllPicturesOnIndexLayout.addWidget(self.showAllPicturesOnIndexButton)

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
        self.updateCameraAutoBrightnessActive()
        self.updateShowAllPicturesOnIndex()

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
        self.persistentGain()

    def open_file_dialog(self):
        CfgService.set(CfgKey.MAIN_SAVE_DIR, str(QFileDialog.getExistingDirectory()))
        self.mainSaveDirLabel.setText(CfgService.get(CfgKey.MAIN_SAVE_DIR))

    def setCameraCalibrationEventPage(self,page):
        self.cameraCalibrationPage = page

    def cameraCalibrationEvent(self):
        self.setPageEvent(self.cameraCalibrationPage)

    def saveWifiPicture(self):
        qrCodeValue = 'WIFI:S:{};T:{};P:{};;'.format(self.wifiSSIDValue.text(),self.wifiProtocolValue.text(),self.wifiPasswordValue.text())
        qr_code = qrcode.make(qrCodeValue)
        img = Image.new("RGB", (qr_code.pixel_size,qr_code.pixel_size), "white")
        img.paste(qr_code,(0,0))

        fontSize = 20
        myFont = ImageFont.truetype(CfgService.get(CfgKey.WIFI_QR_CODE_FONT), fontSize)

        title = ImageDraw.Draw(img)
        title.text((10, 10), textValue[TextKey.QR_CODE_WIFI_NAME]+self.wifiSSIDValue.text(),font=myFont, fill=(0, 0, 0))

        password = ImageDraw.Draw(img)
        password.text((10, qr_code.pixel_size-10-fontSize), textValue[TextKey.QR_CODE_WIFI_PASSWORD]+self.wifiPasswordValue.text(),font=myFont, fill=(0, 0, 0))
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

    #Camera
    def updateCameraAutoBrightnessActive(self):
        isAutoBrightnessActivate = CfgService.get(CfgKey.PI_CAMERA_STATIC_BRIGHTNESS)
        self.cameraAutoBrightnessButton.setChecked(isAutoBrightnessActivate)
        if isAutoBrightnessActivate:
            self.cameraAutoBrightnessButton.setText(textValue[TextKey.PAGE_CONFIG_CAMERA_STATIC_BRIGHTNESS_VALUE_STATIC])
        else:
            self.cameraAutoBrightnessButton.setText(textValue[TextKey.PAGE_CONFIG_CAMERA_STATIC_BRIGHTNESS_VALUE_DYNAMIC])
        self.disableIfBrightnessDynamic();

    def activateCameraAutoBrightness(self):
        if self.cameraAutoBrightnessButton.isChecked():
            CfgService.set(CfgKey.PI_CAMERA_STATIC_BRIGHTNESS,True)
            self.cameraAutoBrightnessButton.setText(textValue[TextKey.PAGE_CONFIG_CAMERA_STATIC_BRIGHTNESS_VALUE_STATIC])
            self.cameraAutoBrightnessButton.setChecked(CfgService.get(CfgKey.PI_CAMERA_STATIC_BRIGHTNESS))
        else:
            CfgService.set(CfgKey.PI_CAMERA_STATIC_BRIGHTNESS,False)
            self.cameraAutoBrightnessButton.setText(textValue[TextKey.PAGE_CONFIG_CAMERA_STATIC_BRIGHTNESS_VALUE_DYNAMIC])
            self.cameraAutoBrightnessButton.setChecked(CfgService.get(CfgKey.PI_CAMERA_STATIC_BRIGHTNESS))
        self.disableIfBrightnessDynamic();

    def disableIfBrightnessDynamic(self):
        isDisabled = not CfgService.get(CfgKey.PI_CAMERA_STATIC_BRIGHTNESS)
        self.cameraBrightnessGainRed.setDisabled(isDisabled)
        self.cameraBrightnessGainBlue.setDisabled(isDisabled)
        self.cameraBrightnessGainBlueLabel.setDisabled(isDisabled)
        self.cameraBrightnessGainRedLabel.setDisabled(isDisabled)
        self.cameraBrightnessStaticValue.setDisabled(isDisabled)
        self.cameraBrightnessStaticValueLabel.setDisabled(isDisabled)

    def persistentGain(self):
        gainRedInt = float(self.cameraBrightnessGainRed.text())
        if(gainRedInt >= 0.0 and gainRedInt <= 8.0):
            CfgService.set(CfgKey.PI_CAMERA_STATIC_BRIGHTNESS_AWB_GAIN_RED, gainRedInt)

        gainBlueInt = float(self.cameraBrightnessGainBlue.text())
        if(gainBlueInt >= 0.0 and gainBlueInt <= 8.0):
            CfgService.set(CfgKey.PI_CAMERA_STATIC_BRIGHTNESS_AWB_GAIN_BLUE, gainBlueInt)

        brightnessInt = int(self.cameraBrightnessStaticValue.text())
        if(brightnessInt >= 0 and brightnessInt <= 100):
            CfgService.set(CfgKey.PI_CAMERA_STATIC_BRIGHTNESS_STATIC_VALUE, brightnessInt)

    # Server
    def updateShowAllPicturesOnIndex(self):
        isActivate = CfgService.get(CfgKey.SERVER_INDEX_PAGE_SHOW_ALL_PICTURES)
        self.showAllPicturesOnIndexButton.setChecked(isActivate)
        if isActivate:
            self.showAllPicturesOnIndexButton.setText(textValue[TextKey.PAGE_CONFIG_AKTIVATE])
        else:
            self.showAllPicturesOnIndexButton.setText(textValue[TextKey.PAGE_CONFIG_INAKTIVATE])

    def activateShowAllPicturesOnIndex(self):
        if self.showAllPicturesOnIndexButton.isChecked():
            CfgService.set(CfgKey.SERVER_INDEX_PAGE_SHOW_ALL_PICTURES,True)
            self.showAllPicturesOnIndexButton.setText(textValue[TextKey.PAGE_CONFIG_AKTIVATE])
            self.showAllPicturesOnIndexButton.setChecked(CfgService.get(CfgKey.SERVER_INDEX_PAGE_SHOW_ALL_PICTURES))
        else:
            CfgService.set(CfgKey.SERVER_INDEX_PAGE_SHOW_ALL_PICTURES,False)
            self.showAllPicturesOnIndexButton.setText(textValue[TextKey.PAGE_CONFIG_INAKTIVATE])
            self.showAllPicturesOnIndexButton.setChecked(CfgService.get(CfgKey.SERVER_INDEX_PAGE_SHOW_ALL_PICTURES))
