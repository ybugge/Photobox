
from PyQt5.QtCore import QSize, Qt
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QVBoxLayout, QWidget, QScrollArea, QHBoxLayout, QLabel, QPushButton

from PhotoboxPages import AllPages
from PhotoboxPages.Page import Page
from Services.CfgService import CfgService
from config.Config import TextKey, CfgKey, textValue


class PageHelp(Page):
    def __init__(self, pages : AllPages,windowSize:QSize):
        super().__init__(pages,windowSize)

        self.windowsize = windowSize
        self.heightDevider = 8

        mainLayout = QVBoxLayout()
        mainLayout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(mainLayout)

        #Titel
        mainLayout.addWidget(self.getTitleAsQLabel(TextKey.PAGE_HELP_TITLE))

        #Content #######################################################################################################
        #Scroll Layout
        scroll_area_content_widget = QWidget()
        self.scroll_area = QScrollArea(self)
        self.scroll_area.setGeometry(0, 0, windowSize.width(), windowSize.height())
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.scroll_area.setWidget(scroll_area_content_widget)

        mainContentLayout = QVBoxLayout()
        scroll_area_content_widget.setLayout(mainContentLayout)
        mainLayout.addWidget(self.scroll_area)

        #Allgemein
        generalDescription = QLabel(textValue[TextKey.PAGE_HELP_GENERAL_DESCRIPTION])
        mainContentLayout.addWidget(generalDescription)

        #printer description
        printerLayout = QHBoxLayout()
        mainContentLayout.addLayout(printerLayout)

        printerPicture = QLabel()
        printerIcon = QPixmap(CfgService.get(CfgKey.PAGE_PICTUREEDIT_PRINT_BUTTON_ICON_DIR))
        printerPicture.setPixmap(printerIcon.scaledToHeight(self.windowsize.height()/self.heightDevider))
        printerPicture.setStyleSheet("background-color : white;")
        printerPicture.setFixedSize(self.getIconSize())
        printerLayout.addWidget(printerPicture)

        printerDescription = QLabel(textValue[TextKey.PAGE_HELP_PRINT_DESCRIPTION] % CfgService.get(CfgKey.PRINTER_MAX_PRINTING_ORDER))
        printerLayout.addWidget(printerDescription)

        #download description
        downloadLayout = QHBoxLayout()
        mainContentLayout.addLayout(downloadLayout)

        downloadPicture = QLabel()
        downloadIcon = QPixmap(CfgService.get(CfgKey.PAGE_PICTUREEDIT_DOWNLOAD_BUTTON_ICON_DIR))
        downloadPicture.setPixmap(downloadIcon.scaledToHeight(self.windowsize.height()/self.heightDevider))
        downloadPicture.setStyleSheet("background-color : white;")
        downloadPicture.setFixedSize(self.getIconSize())
        downloadLayout.addWidget(downloadPicture)

        downloadDescription = QLabel(textValue[TextKey.PAGE_HELP_DOWNLOAD_DESCRIPTION])
        downloadLayout.addWidget(downloadDescription)

        #new picture description
        newPictureLayout = QHBoxLayout()
        mainContentLayout.addLayout(newPictureLayout)

        newPicturePicture = QLabel()
        newPictureIcon = QPixmap(CfgService.get(CfgKey.PAGE_PICTUREEDIT_NEWPICTURE_BUTTON_ICON_DIR))
        newPicturePicture.setPixmap(newPictureIcon.scaledToHeight(self.windowsize.height()/self.heightDevider))
        newPicturePicture.setStyleSheet("background-color : white;")
        newPicturePicture.setFixedSize(self.getIconSize())
        newPictureLayout.addWidget(newPicturePicture)

        newPictureDescription = QLabel(textValue[TextKey.PAGE_HELP_NEW_PICTURE_DESCRIPTION])
        newPictureLayout.addWidget(newPictureDescription)

        #finished description
        finishedLayout = QHBoxLayout()
        mainContentLayout.addLayout(finishedLayout)

        finishedPicture = QLabel()
        finishedIcon = QPixmap(CfgService.get(CfgKey.PAGE_PICTUREEDIT_FINISHED_BUTTON_ICON_DIR))
        finishedPicture.setPixmap(finishedIcon.scaledToHeight(self.windowsize.height()/self.heightDevider))
        finishedPicture.setStyleSheet("background-color : white;")
        finishedPicture.setFixedSize(self.getIconSize())
        finishedLayout.addWidget(finishedPicture)

        finishedDescription = QLabel(textValue[TextKey.PAGE_HELP_FINISHED_DESCRIPTION])
        finishedLayout.addWidget(finishedDescription)

        #Navigation Backbutton
        #mainLayout.addStretch()
        backButton = QPushButton(textValue[TextKey.PAGE_HELP_BACKBUTTON])
        backButton.clicked.connect(self.backPageEvent)
        self.setNavigationbuttonStyle(backButton)
        mainLayout.addWidget(backButton)

    def getIconSize(self):
        return QSize(self.windowsize.height()/self.heightDevider,self.windowsize.height()/self.heightDevider)