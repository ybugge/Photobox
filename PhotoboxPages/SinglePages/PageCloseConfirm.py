from PyQt5.QtCore import Qt, QSize
from PyQt5.QtWidgets import QVBoxLayout, QLabel, QHBoxLayout, QPushButton

from PhotoboxPages import MainWindow
from PhotoboxPages.AllPages import AllPages
from PhotoboxPages.Page import Page
from Services.WebServerExecThread import WebServerExecThread
from config.Config import textValue, TextKey


class PageCloseConfirm(Page):
    def __init__(self, pages : AllPages, windowSize:QSize, mainWindow: MainWindow, server:WebServerExecThread):
        super().__init__(pages,windowSize)
        self.server = server

        self.mainWindow = mainWindow

        vbox = QVBoxLayout()
        vbox.setContentsMargins(0, 0, 0, 0)
        vbox.addWidget(self.getTitleAsQLabel(TextKey.PAGE_CLOSECONFIRM_TITLE))
        vbox.addStretch()

        mainText = QLabel(textValue[TextKey.PAGE_CLOSECONFIRM_TEXT])
        mainText.setAlignment(Qt.AlignCenter)
        vbox.addWidget(mainText)
        vbox.addStretch()

        bottomButtonHBox = QHBoxLayout()
        yesButton = QPushButton(textValue[TextKey.PAGE_CLOSECONFIRM_YES])
        yesButton.clicked.connect(self.closeApplication)
        self.setNavigationbuttonStyle(yesButton)
        bottomButtonHBox.addWidget(yesButton)

        noButton = QPushButton(textValue[TextKey.PAGE_CLOSECONFIRM_NO])
        noButton.clicked.connect(self.nextPageEvent)
        self.setNavigationbuttonStyle(noButton)
        bottomButtonHBox.addWidget(noButton)
        vbox.addLayout(bottomButtonHBox)
        self.setLayout(vbox)

    def closeApplication(self):
        self.server.stop()
        print("Close Application")
        self.mainWindow.close()

