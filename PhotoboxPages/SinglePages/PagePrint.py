from PyQt5.QtCore import QSize, QTimer
from PyQt5.QtWidgets import QVBoxLayout, QHBoxLayout, QPushButton, QTextEdit

from PhotoboxPages.AllPages import AllPages
from PhotoboxPages.Page import Page
from Services.CfgService import CfgService
from Services.GlobalPagesVariableService import GlobalPagesVariableService
from Services.PageDbService import PageDbSevice
from Services.PrinterService import PrinterService
from Services.ShottedPictureService import ShottedPictureService
from config.Config import textValue, TextKey, CfgKey


class PagePrint(Page):
    def __init__(self, pages : AllPages, windowSize:QSize, globalVariable:GlobalPagesVariableService, printerService:PrinterService):
        super().__init__(pages,windowSize)
        self.globalVariable = globalVariable
        self.printerService = printerService
        mainLayout = QVBoxLayout()
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
        self.changeUiIfInPrint()

    def executeInAutoForwardTimerEvent(self):
        pictureTargetPath = ShottedPictureService.saveUsedPicture(self.globalVariable.getPictureSubName())
        PageDbSevice.updatePicture(self.globalVariable,pictureTargetPath,True)
        self.globalVariable.unlockPictureName()

    def print(self):
        self.printerService.printLokal(self.globalVariable)
        self.printerStatusUpdateTimer.start(CfgService.get(CfgKey.PAGE_PRINT_STATUS_UPDATE_PERIOD))

    def changeUiIfInPrint(self):
        isInPrint = self.printerService.isStatusInPrintLokal(self.globalVariable)
        if isInPrint:
            self.printButton.setDisabled(True)
            self.printButton.setText(textValue[TextKey.PAGE_PRINT_PRINTBUTTON_DISABLED])
            self.textArea.setText(textValue[TextKey.PAGE_PRINT_HINT_IN_PRINT])
        else:
            self.printButton.setDisabled(False)
            self.printButton.setText(textValue[TextKey.PAGE_PRINT_PRINTBUTTON])
            self.textArea.setText(textValue[TextKey.PAGE_PRINT_HINT_PRINT])
            self.printerStatusUpdateTimer.stop()