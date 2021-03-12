from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QPushButton

from Pages import AllPages
from Pages.Page import Page


class PageTest2(Page):
    def __init__(self, pages : AllPages):
        super().__init__(pages)
        vbox = QtWidgets.QVBoxLayout()
        self.setLayout(vbox)

        vbox.addWidget(QtWidgets.QLabel("This is widget two"))

        self.nextButton = QPushButton(self)
        self.nextButton.setText("next2")
        self.nextButton.clicked.connect(self.nextPageEvent)
        vbox.addWidget(self.nextButton)