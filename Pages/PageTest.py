from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QPushButton

from Pages import AllPages
from Pages.Page import Page


class PageTest(Page):
    def __init__(self, pages : AllPages):
        super().__init__(pages)
        color_1 = 'red'
        self.setStyleSheet('QWidget {background-color: %s}' % color_1)

        vbox = QtWidgets.QVBoxLayout()
        self.setLayout(vbox)


        self.fileNameLabel = QtWidgets.QLabel("FileName")
        vbox.addWidget(self.fileNameLabel)
        label2 = QtWidgets.QLabel()
        label2.setText(str(self.frameGeometry()))
        vbox.addWidget(label2)

        self.nextButton = QPushButton(self)
        self.nextButton.setText("next1")
        self.nextButton.clicked.connect(self.nextPageEvent)
        vbox.addWidget(self.nextButton)

    def executeBefore(self):
        pass