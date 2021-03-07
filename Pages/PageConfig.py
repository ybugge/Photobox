from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QPushButton, QVBoxLayout, QLabel

from Pages.AllPages import AllPages
from Pages.Page import Page
from config.Config import textValue, TextKey


class PageConfig(Page):
    def __init__(self, pages : AllPages):
        super().__init__(pages)
        vbox = QVBoxLayout()
        self.setLayout(vbox)

        #Titel
        vbox.addWidget(self.getTitleAsQLabel(TextKey.PAGE_CONFIG_TITLE))
        vbox.addStretch()

        #Hinweise
        vbox.addWidget(QLabel(textValue[TextKey.PAGE_CONFIG_HINT_TITLE]))

        escapeHintLabel = QLabel(textValue[TextKey.PAGE_CONFIG_ESCAPE_HINT])
        escapeHintLabel.setAlignment(Qt.AlignCenter)
        vbox.addWidget(escapeHintLabel)
        vbox.addStretch()

        #Nextbutton
        nextButton = QPushButton(textValue[TextKey.PAGE_CONFIG_NEXTBUTTON])
        nextButton.clicked.connect(self.nextPageEvent)
        vbox.addWidget(nextButton)