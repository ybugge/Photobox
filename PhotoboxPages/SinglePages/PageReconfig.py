from PyQt5.QtCore import QSize
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QVBoxLayout, QHBoxLayout, QPushButton, QLabel

from PhotoboxPages.AllPages import AllPages
from PhotoboxPages.Page import Page
from Services.CfgService import CfgService
from Services.GlobalPagesVariableService import GlobalPagesVariableService
from Services.Greenscreen.GreenscreenBackgroundService import GreenscreenBackgroundService
from Services.PrinterService import PrinterService
from config.Config import TextKey, textValue, CfgKey


class PageReconfig(Page):
    def __init__(self, pages : AllPages, windowSize:QSize, printerService:PrinterService,globalPagesVariableService:GlobalPagesVariableService):
        super().__init__(pages,windowSize)
        self.greenscreenBackgroundService = GreenscreenBackgroundService(globalPagesVariableService)
        self.printerService = printerService
        mainLayout = QVBoxLayout()
        mainLayout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(mainLayout)

        #Titel
        mainLayout.addWidget(self.getTitleAsQLabel(TextKey.PAGE_RECONFIG_TITLE))

        titleFont = QFont()
        titleFont.setUnderline(True)

        # Printer -------------------------------------------------------------------------------  From PageConfig!
        printerTitle = QLabel(textValue[TextKey.PAGE_CONFIG_PRINTER_TITLE])
        printerTitle.setFont(titleFont)
        mainLayout.addWidget(printerTitle)

        # Printer enabled?
        printerDisabledLayout = QHBoxLayout()
        mainLayout.addLayout(printerDisabledLayout)

        self.printerDisabledLabel = QLabel()
        self.printerDisabledLabel.setText(textValue[TextKey.PAGE_CONFIG_SERVICE_STATUS])
        printerDisabledLayout.addWidget(self.printerDisabledLabel)

        self.printerDisabledButton = QPushButton()
        self.printerDisabledButton.setCheckable(True)
        isPrinterActivate = CfgService.get(CfgKey.PRINTER_IS_ACTIVE)
        self.printerDisabledButton.setChecked(isPrinterActivate)
        if CfgService.get(CfgKey.PRINTER_IS_ACTIVE):
            self.printerDisabledButton.setText(textValue[TextKey.PAGE_CONFIG_AKTIVATE])
        else:
            self.printerDisabledButton.setText(textValue[TextKey.PAGE_CONFIG_INAKTIVATE])
        self.printerDisabledButton.clicked.connect(self.activatePrinter)
        printerDisabledLayout.addWidget(self.printerDisabledButton)

        #Aktiviert Printer Web
        printerDisabledWebLayout = QHBoxLayout()
        mainLayout.addLayout(printerDisabledWebLayout)

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

        # Greenscreen -------------------------------------------------------------------------------
        greenscreenTitle = QLabel(textValue[TextKey.PAGE_CONFIG_GREENSCREEN_TITLE])
        greenscreenTitle.setFont(titleFont)
        mainLayout.addWidget(greenscreenTitle)

        # Greenscreen enabled?
        greenscreenDisabledLayout = QHBoxLayout()
        mainLayout.addLayout(greenscreenDisabledLayout)

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
        mainLayout.addWidget(greenscreenColorPickerButton)

        #Load Background
        self.greenscreenLoadBackgroundButton = QPushButton()
        self.greenscreenLoadBackgroundButton.setText(textValue[TextKey.PAGE_RECONFIG_LOAD_GREENSCREEN_BACKGROUND])
        self.greenscreenLoadBackgroundButton.clicked.connect(self.loadGreenscreenBackground)
        mainLayout.addWidget(self.greenscreenLoadBackgroundButton)

        #Upload Backgrounds
        self.uploadDefaultBackgroundsButton = QPushButton()
        self.uploadDefaultBackgroundsButton.setText(textValue[TextKey.PAGE_RECONFIG_UPLOAD_DEFAULT_GREENSCREEN_BACKGROUNDS])
        self.uploadDefaultBackgroundsButton.clicked.connect(self._uploadDefaultBackgroundEvent)
        mainLayout.addWidget(self.uploadDefaultBackgroundsButton)

        # Camera Calibration -------------------------------------------------------------------------------
        self.cameraCalibrationButton = QPushButton()
        self.cameraCalibrationButton.setText(textValue[TextKey.PAGE_CONFIG_CAMERA_CALIBRATION_BUTTON])
        self.cameraCalibrationButton.clicked.connect(self.cameraCalibrationEvent)
        mainLayout.addWidget(self.cameraCalibrationButton)

        # Server  ------------------------------------------------------------------------------- cfgValue[CfgKey.SERVER_INDEX_PAGE_SHOW_ALL_PICTURES] = True
        serverTitle = QLabel(textValue[TextKey.PAGE_CONFIG_SERVER_TITLE])
        serverTitle.setFont(titleFont)
        mainLayout.addWidget(serverTitle)

        # show all Picture in Index -> enabled?
        showAllPicturesOnIndexLayout = QHBoxLayout()
        mainLayout.addLayout(showAllPicturesOnIndexLayout)

        self.showAllPicturesOnIndexLabel = QLabel()
        self.showAllPicturesOnIndexLabel.setText(textValue[TextKey.PAGE_CONFIG_SERVER_SHOW_ALL_PICTURES_ON_INDEX])
        showAllPicturesOnIndexLayout.addWidget(self.showAllPicturesOnIndexLabel)

        self.showAllPicturesOnIndexButton = QPushButton()
        self.showAllPicturesOnIndexButton.setCheckable(True)
        self.showAllPicturesOnIndexButton.setChecked(True)
        self.showAllPicturesOnIndexButton.setText(textValue[TextKey.PAGE_CONFIG_AKTIVATE])
        self.showAllPicturesOnIndexButton.clicked.connect(self.activateShowAllPicturesOnIndex)
        showAllPicturesOnIndexLayout.addWidget(self.showAllPicturesOnIndexButton)


        #Navigation   ##################################################################################################
        mainLayout.addStretch()
        navigationLayout = QHBoxLayout()
        mainLayout.addLayout(navigationLayout)

        backButton = QPushButton(textValue[TextKey.PAGE_RECONFIG_BACKBUTTON])
        backButton.clicked.connect(self.backPageEvent)
        self.setNavigationbuttonStyle(backButton)
        navigationLayout.addWidget(backButton)

    def executeBefore(self):
        self.updateUiPrintingPossible()
        self.updateGreenscreenActive()
        self.greenscreenLoadBackgroundButton.setText(textValue[TextKey.PAGE_RECONFIG_LOAD_GREENSCREEN_BACKGROUND])
        self.greenscreenLoadBackgroundButton.setDisabled(False)
        self.updateShowAllPicturesOnIndex()

    def updateGreenscreenActive(self):
        isGreenscreenActivate = CfgService.get(CfgKey.GREENSCREEN_IS_ACTIVE)
        self.greenscreenDisabledButton.setChecked(isGreenscreenActivate)
        if isGreenscreenActivate:
            self.greenscreenDisabledButton.setText(textValue[TextKey.PAGE_CONFIG_AKTIVATE])
        else:
            self.greenscreenDisabledButton.setText(textValue[TextKey.PAGE_CONFIG_INAKTIVATE])

    def loadGreenscreenBackground(self):
        self.greenscreenLoadBackgroundButton.setText(textValue[TextKey.PAGE_RECONFIG_WAS_LOADED_GREENSCREEN_BACKGROUND])
        self.greenscreenLoadBackgroundButton.setDisabled(True)
        self.greenscreenBackgroundService.loadDefaultBackgrounds()

    def updateUiPrintingPossible(self):
        if not self.printerService.printingPosible():
            CfgService.set(CfgKey.PRINTER_IS_ACTIVE,False)
            self.printerDisabledButton.setText(textValue[TextKey.PAGE_CONFIG_INAKTIVATE])
            self.printerDisabledButton.setChecked(CfgService.get(CfgKey.PRINTER_IS_ACTIVE))
            self.printerDisabledButton.setDisabled(True)

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

    def activateGreenscreen(self):
        if self.greenscreenDisabledButton.isChecked():
            CfgService.set(CfgKey.GREENSCREEN_IS_ACTIVE,True)
            self.greenscreenDisabledButton.setText(textValue[TextKey.PAGE_CONFIG_AKTIVATE])
            self.greenscreenDisabledButton.setChecked(CfgService.get(CfgKey.GREENSCREEN_IS_ACTIVE))
        else:
            CfgService.set(CfgKey.GREENSCREEN_IS_ACTIVE,False)
            self.greenscreenDisabledButton.setText(textValue[TextKey.PAGE_CONFIG_INAKTIVATE])
            self.greenscreenDisabledButton.setChecked(CfgService.get(CfgKey.GREENSCREEN_IS_ACTIVE))

    def setGreenscreenColorPickerEventPage(self,page):
        self.greenscreenColorPickerPage = page

    def greenscreenColorPickerEvent(self):
        self.setPageEvent(self.greenscreenColorPickerPage)

    def setUploadDefaultBackgroundEventPage(self,page):
        self.uploadDefaultBackground = page

    def _uploadDefaultBackgroundEvent(self):
        self.setPageEvent(self.uploadDefaultBackground)

    def setCameraCalibrationEventPage(self,page):
        self.cameraCalibrationPage = page

    def cameraCalibrationEvent(self):
        self.setPageEvent(self.cameraCalibrationPage)

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