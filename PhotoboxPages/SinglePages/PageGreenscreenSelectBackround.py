from PyQt5.QtCore import QSize
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QVBoxLayout, QHBoxLayout, QPushButton

from PhotoboxPages.AllPages import AllPages
from PhotoboxPages.Page import Page
from Services.CfgService import CfgService
from Services.GlobalPagesVariableService import GlobalPagesVariableService
from Services.GreenscreenBackgroundService import GreenscreenBackgroundService
from config.Config import CfgKey, TextKey, textValue


class PageGreenscreenSelectBackround(Page):
    def __init__(self, pages : AllPages, windowsize:QSize,globalPagesVariableService:GlobalPagesVariableService):
        super().__init__(pages,windowsize)
        self.greenscreenBackgroundService = GreenscreenBackgroundService(globalPagesVariableService)
        mainLayout = QVBoxLayout()
        mainLayout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(mainLayout)
        self.currentBackgroundImageIndex = 0

        #Titel
        mainLayout.addWidget(self.getTitleAsQLabel(TextKey.PAGE_GREENSCREEN_SELECT_BACKGROUND_TITLE))
        mainLayout.addStretch()

        #Background Images
        backgroundLayout = QHBoxLayout()
        mainLayout.addLayout(backgroundLayout)

        self.leftBackgroundButton = QPushButton("<")
        self.leftBackgroundButton.clicked.connect(self._backgroundBackEvent)
        self.setPictureNavigationbuttonStyle(self.leftBackgroundButton)
        backgroundLayout.addWidget(self.leftBackgroundButton)

        self.backgroundButton = QPushButton()
        self.backgroundButton.setContentsMargins(0,0,0,0)
        self.backgroundButton.setAutoFillBackground(True)
        self.backgroundButton.setFlat(True)
        self.backgroundButton.clicked.connect(self._setOwnBackgroundPageEvent)
        backgroundLayout.addWidget(self.backgroundButton)

        self.rightBackgroundButton = QPushButton(">")
        self.rightBackgroundButton.clicked.connect(self._backgroundNextEvent)
        self.setPictureNavigationbuttonStyle(self.rightBackgroundButton)
        backgroundLayout.addWidget(self.rightBackgroundButton)

        #Navigation   ##################################################################################################
        mainLayout.addStretch()
        navigationLayout = QHBoxLayout()
        mainLayout.addLayout(navigationLayout)

        backButton = QPushButton(textValue[TextKey.PAGE_GREENSCREEN_SELECT_BACKGROUND_BACK_BUTTON])
        backButton.clicked.connect(self.backPageEvent)
        self.setNavigationbuttonStyle(backButton)
        navigationLayout.addWidget(backButton)

        ownBackgroundButton = QPushButton(textValue[TextKey.PAGE_GREENSCREEN_SELECT_BACKGROUND_OWN_BACKGROUND_BUTTON])
        #ownBackgroundButton.clicked.connect(self._setOwnBackgroundPageEvent)
        #ownBackgroundButton.clicked.connect(self._updateBackgroundImages)
        self.setNavigationbuttonStyle(ownBackgroundButton)
        #navigationLayout.addWidget(ownBackgroundButton)


    def executeBefore(self):
        if not CfgService.get(CfgKey.GREENSCREEN_IS_ACTIVE):
            self.nextPageEvent()
        else:
            self.greenscreenBackgroundService.loadDefaultBackgrounds()
            self.currentBackgroundImageIndex = 0
            self._navigationBackgroundButtonStatus()
            self._setBrackgroundPreview()

    def _backgroundBackEvent(self):
        self.currentBackgroundImageIndex -= 1
        if self.currentBackgroundImageIndex < 0:
            self.currentBackgroundImageIndex = 0
        self._navigationBackgroundButtonStatus()
        self._setBrackgroundPreview()

    def _backgroundNextEvent(self):
        self.currentBackgroundImageIndex += 1
        if self.greenscreenBackgroundService.getBackgroundSize() <= self.currentBackgroundImageIndex:
            self.currentBackgroundImageIndex = self.greenscreenBackgroundService.getBackgroundSize() - 1
        self._navigationBackgroundButtonStatus()
        self._setBrackgroundPreview()

    def _updateBackgroundImages(self):
        self.greenscreenBackgroundService.loadDefaultBackgrounds()
        self.currentBackgroundImageIndex = 0
        self._navigationBackgroundButtonStatus()
        self._setBrackgroundPreview()

    def _navigationBackgroundButtonStatus(self):
        if self.greenscreenBackgroundService.getBackgroundSize() <= 0:
            self.leftBackgroundButton.setDisabled(True)
            self.backgroundButton.setDisabled(True)
            self.rightBackgroundButton.setDisabled(True)
        else:
            self.leftBackgroundButton.setDisabled(False)
            self.backgroundButton.setDisabled(False)
            self.rightBackgroundButton.setDisabled(False)

            if 0 == self.currentBackgroundImageIndex:
                self.leftBackgroundButton.setDisabled(True)
            if self.greenscreenBackgroundService.getBackgroundSize() <= (self.currentBackgroundImageIndex+1):
                self.rightBackgroundButton.setDisabled(True)

    def _setBrackgroundPreview(self):
        size = self._getPictureButtonsSize()
        image = self.greenscreenBackgroundService.getPreviewImageAsQPixmap(self.currentBackgroundImageIndex,size)
        if image is None:
            self.backgroundButton.setText("Kein Bild vorhanden!")
            self.backgroundButton.setIcon(QIcon())
        else:
            self.backgroundButton.setText("")
            self.backgroundButton.setIcon(QIcon(image))
            #self.backgroundButton.setIconSize(size)

    def setOwnBackgroundPage(self,ownBackgroundPage:Page):
        self.ownBackgroundPage = ownBackgroundPage

    def _setOwnBackgroundPageEvent(self):
        self.greenscreenBackgroundService.setIndex(self.currentBackgroundImageIndex)
        self.setPageEvent(self.ownBackgroundPage)

    def setPictureNavigationbuttonStyle(self, button:QPushButton):
        button.setFixedHeight(self.getContentHeightWithNavigationButtonAndTitle())
        button.setStyleSheet("font-size: " + str(self.getTitelAndNavigationButtonTextSize()) + "px ;" \
                            "font-family: " + CfgService.get(CfgKey.MAIN_WINDOW_TEXT_FONT) +", serif;")

    def _getPictureButtonsSize(self):
        piCameraResolution = CfgService.get(CfgKey.PI_CAMERA_PHOTO_RESOLUTION)
        height = self.getContentHeightWithNavigationButtonAndTitle()
        cameraHeight = piCameraResolution[1]
        camerawidth = piCameraResolution[0]
        width = height * camerawidth / cameraHeight
        return QSize(width,height)