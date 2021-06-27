
from PyQt5.QtCore import QSize, Qt
from PyQt5.QtWidgets import QVBoxLayout, QWidget, QScrollArea, QHBoxLayout, QLabel

from PhotoboxPages import AllPages
from PhotoboxPages.Page import Page
from Services.CfgService import CfgService
from config.Config import TextKey, CfgKey


class PageHelp(Page):
    def __init__(self, pages : AllPages,windowSize:QSize):
        super().__init__(pages,windowSize)

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

        #printer description
        printerLayout = QHBoxLayout()
        mainContentLayout.addLayout(printerLayout)

        printerPicture = QLabel()
        printerPicture.setStyleSheet("qproperty-icon: url(" + CfgService.get(CfgKey.PAGE_PICTUREEDIT_PRINT_BUTTON_ICON_DIR) + ");")
        printerLayout.addWidget(printerPicture)