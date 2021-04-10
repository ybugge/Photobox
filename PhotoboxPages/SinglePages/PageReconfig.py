from PyQt5.QtCore import QSize
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QVBoxLayout, QHBoxLayout, QPushButton, QLabel

from PhotoboxPages.AllPages import AllPages
from PhotoboxPages.Page import Page
from Services.CfgService import CfgService
from Services.PrinterService import PrinterService
from config.Config import TextKey, textValue, CfgKey


class PageReconfig(Page):
    def __init__(self, pages : AllPages, windowSize:QSize, printerService:PrinterService):
        super().__init__(pages,windowSize)
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

    def updateGreenscreenActive(self):
        isGreenscreenActivate = CfgService.get(CfgKey.GREENSCREEN_IS_ACTIVE)
        self.greenscreenDisabledButton.setChecked(isGreenscreenActivate)
        if isGreenscreenActivate:
            self.greenscreenDisabledButton.setText(textValue[TextKey.PAGE_CONFIG_AKTIVATE])
        else:
            self.greenscreenDisabledButton.setText(textValue[TextKey.PAGE_CONFIG_INAKTIVATE])

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