from PyQt5.QtCore import QSize, QTimer
from PyQt5.QtWidgets import QVBoxLayout, QHBoxLayout, QPushButton, QTextEdit

from PhotoboxPages.AllPages import AllPages
from PhotoboxPages.Page import Page
from Services.CfgService import CfgService
from Services.GlobalPagesVariableService import GlobalPagesVariableService
from Services.PrinterService import PrinterService
from config.Config import textValue, TextKey, CfgKey


class PagePrint(Page):
    def __init__(self, pages : AllPages, windowSize:QSize, globalVariable:GlobalPagesVariableService, printerService:PrinterService):
        super().__init__(pages,windowSize)
        self.globalVariable = globalVariable
        self.printerService = printerService
        mainLayout = QVBoxLayout()
        mainLayout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(mainLayout)

        #Titel
        self.title = self.getTitleAsQLabel(TextKey.PAGE_PRINT_TITLE)
        mainLayout.addWidget(self.title)

        #Hinweise
        self.textArea = QTextEdit()
        mainLayout.addWidget(self.textArea)
        self.textArea.setReadOnly(True)

        #Navigation
        mainLayout.addStretch()
        navigationLayout=QHBoxLayout()
        mainLayout.addLayout(navigationLayout)

        backButton = QPushButton(textValue[TextKey.PAGE_PRINT_BACKBUTTON])
        backButton.clicked.connect(self.backPageEvent)
        self.setNavigationbuttonStyle(backButton)
        navigationLayout.addWidget(backButton)

        self.printButton = QPushButton(textValue[TextKey.PAGE_PRINT_PRINTBUTTON])
        self.printButton.clicked.connect(self.print)
        self.setNavigationbuttonStyle(self.printButton)
        navigationLayout.addWidget(self.printButton)

        #Timer
        self.printerStatusUpdateTimer = QTimer()
        self.printerStatusUpdateTimer.timeout.connect(self.changeUiIfInPrint)

    def executeBefore(self):
        self.globalVariable.setPictureUsed(True)
        self.printerStatusUpdateTimer.start(CfgService.get(CfgKey.PAGE_PRINT_STATUS_UPDATE_PERIOD))
        self.changeUiIfInPrint()

    def executeAfter(self):
        self.printerStatusUpdateTimer.stop()

    def print(self):
        self.printButton.setDisabled(True)
        self.printerService.printLokal(self.globalVariable)

    def changeUiIfInPrint(self):
        isInPrint = self.printerService.isStatusInPrintLokal(self.globalVariable)
        if self.printerService.hasTooManyPrintingOrderLokal(self.globalVariable) and (not isInPrint):
            self.printButton.setDisabled(True)
            self.printButton.setText(textValue[TextKey.PAGE_PRINT_PRINTBUTTON])
            self.textArea.setText(textValue[TextKey.PAGE_PRINT_HINT_TOO_MANY_ORDER])
        elif isInPrint:
            self.printButton.setDisabled(True)
            self.printButton.setText(textValue[TextKey.PAGE_PRINT_PRINTBUTTON_DISABLED])
            self.textArea.setText(textValue[TextKey.PAGE_PRINT_HINT_IN_PRINT])
            self.textArea.append(self.getPrinterStatus())
        else:
            self.printButton.setDisabled(False)
            self.printButton.setText(textValue[TextKey.PAGE_PRINT_PRINTBUTTON])
            self.textArea.setText(textValue[TextKey.PAGE_PRINT_HINT_PRINT])
            self.textArea.append(self.getPrinterStatus())

    def getPrinterStatus(self):
        return textValue[TextKey.PAGE_PRINT_HINT_STATUS_LABEL]+self.printerService.getPrinterStatus()