from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QVBoxLayout, QLabel, QHBoxLayout, QPushButton

import MainWindow
from Pages.AllPages import AllPages
from Pages.Page import Page
from config.Config import textValue, TextKey


class PageCloseConfirm(Page):
    def __init__(self, pages : AllPages, mainWindow: MainWindow):
        super().__init__(pages)

        self.mainWindow = mainWindow

        vbox = QVBoxLayout()
        vbox.addWidget(self.getTitleAsQLabel(TextKey.PAGE_CLOSECONFIRM_TITLE))
        vbox.addStretch()

        mainText = QLabel(textValue[TextKey.PAGE_CLOSECONFIRM_TEXT])
        mainText.setAlignment(Qt.AlignCenter)
        vbox.addWidget(mainText)
        vbox.addStretch()

        bottomButtonHBox = QHBoxLayout()
        yesButton = QPushButton(textValue[TextKey.PAGE_CLOSECONFIRM_YES])
        yesButton.clicked.connect(self.closeApplication)
        bottomButtonHBox.addWidget(yesButton)
        noButton = QPushButton(textValue[TextKey.PAGE_CLOSECONFIRM_NO])
        noButton.clicked.connect(self.nextPageEvent)
        bottomButtonHBox.addWidget(noButton)
        vbox.addLayout(bottomButtonHBox)
        self.setLayout(vbox)

    def closeApplication(self):
        print("Close Application")
        self.mainWindow.close()

