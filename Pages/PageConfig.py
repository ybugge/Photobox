from PyQt5.QtCore import Qt
from PyQt5.QtMultimedia import QCameraInfo
from PyQt5.QtWidgets import QPushButton, QVBoxLayout, QLabel, QHBoxLayout, QFileDialog

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


        #Configs
        dirButton = QPushButton("...")
        dirButton.clicked.connect(self.open_file_dialog)
        vbox.addWidget(dirButton)



        vbox.addStretch()
        #Navigation
        navigationLayout = QHBoxLayout()
        vbox.addLayout(navigationLayout)

        backButton = QPushButton(textValue[TextKey.PAGE_CONFIG_BACKBUTTON])
        backButton.clicked.connect(self.backPageEvent)
        navigationLayout.addWidget(backButton)

        nextButton = QPushButton(textValue[TextKey.PAGE_CONFIG_NEXTBUTTON])
        nextButton.clicked.connect(self.nextPageEvent)
        navigationLayout.addWidget(nextButton)

    def open_file_dialog(self):
        directory = str(QFileDialog.getExistingDirectory())
        print(directory)
        #self.lineEdit.setText('{}'.format(directory))