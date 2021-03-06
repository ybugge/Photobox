from PyQt5.QtCore import QSize
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtWidgets import QVBoxLayout, QHBoxLayout, QPushButton

from PhotoboxPages.AllPages import AllPages
from PhotoboxPages.Page import Page
from Services.CfgService import CfgService
from Services.GlobalPagesVariableService import GlobalPagesVariableService
from Services.Greenscreen.GreenscreenBackgroundService import GreenscreenBackgroundService
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
        self.title = self.getTitleAsQLabel(TextKey.PAGE_GREENSCREEN_SELECT_BACKGROUND_TITLE)
        mainLayout.addWidget(self.title)
        mainLayout.addStretch()

        #Background Images
        backgroundLayout = QHBoxLayout()
        mainLayout.addLayout(backgroundLayout)

        backgroundLeftNavigationLayout = QVBoxLayout()
        backgroundLayout.addLayout(backgroundLeftNavigationLayout)

        self.leftRotateBackgroundButton = QPushButton()
        leftRotateIcon = QPixmap(CfgService.get(CfgKey.PAGE_GREENSCREEN_SELECT_BACKGROUND_ROTATE_LEFT_ICON))
        leftRotateIcon = leftRotateIcon.scaledToHeight(self.getRotateIconHight())
        self.leftRotateBackgroundButton.setIcon(QIcon(leftRotateIcon))
        self.leftRotateBackgroundButton.setIconSize(leftRotateIcon.size())
        self.leftRotateBackgroundButton.clicked.connect(self._rotateLeft)
        self.setPictureRotateButtonStyle(self.leftRotateBackgroundButton)
        backgroundLeftNavigationLayout.addWidget(self.leftRotateBackgroundButton)

        self.leftBackgroundButton = QPushButton("<")
        self.leftBackgroundButton.clicked.connect(self._backgroundBackEvent)
        self.setPictureNavigationButtonStyle(self.leftBackgroundButton)
        backgroundLeftNavigationLayout.addWidget(self.leftBackgroundButton)

        self.backgroundButton = QPushButton()
        self.backgroundButton.setContentsMargins(0,0,0,0)
        self.backgroundButton.setAutoFillBackground(True)
        self.backgroundButton.setFlat(True)
        self.backgroundButton.clicked.connect(self._nextPageEvent)
        backgroundLayout.addWidget(self.backgroundButton)

        backgroundRightNavigationLayout = QVBoxLayout()
        backgroundLayout.addLayout(backgroundRightNavigationLayout)

        self.rightRotateBackgroundButton = QPushButton()
        rightRotateIcon = QPixmap(CfgService.get(CfgKey.PAGE_GREENSCREEN_SELECT_BACKGROUND_ROTATE_RIGHT_ICON))
        rightRotateIcon = rightRotateIcon.scaledToHeight(self.getRotateIconHight())
        self.rightRotateBackgroundButton.setIcon(QIcon(rightRotateIcon))
        self.rightRotateBackgroundButton.setIconSize(rightRotateIcon.size())
        self.rightRotateBackgroundButton.clicked.connect(self._rotateRight)
        self.setPictureRotateButtonStyle(self.rightRotateBackgroundButton)
        backgroundRightNavigationLayout.addWidget(self.rightRotateBackgroundButton)

        self.rightBackgroundButton = QPushButton(">")
        self.rightBackgroundButton.clicked.connect(self._backgroundNextEvent)
        self.setPictureNavigationButtonStyle(self.rightBackgroundButton)
        backgroundRightNavigationLayout.addWidget(self.rightBackgroundButton)

        #Navigation   ##################################################################################################
        mainLayout.addStretch()
        navigationLayout = QHBoxLayout()
        mainLayout.addLayout(navigationLayout)

        backButton = QPushButton(textValue[TextKey.PAGE_GREENSCREEN_SELECT_BACKGROUND_BACK_BUTTON])
        backButton.clicked.connect(self._backPageEvent)
        self.setNavigationbuttonStyle(backButton)
        navigationLayout.addWidget(backButton)

        ownBackgroundButton = QPushButton(textValue[TextKey.PAGE_GREENSCREEN_SELECT_BACKGROUND_OWN_BACKGROUND_BUTTON])
        ownBackgroundButton.clicked.connect(self._setOwnBackgroundPageEvent)
        self.setNavigationbuttonStyle(ownBackgroundButton)
        navigationLayout.addWidget(ownBackgroundButton)


    def executeBefore(self):
        if not CfgService.get(CfgKey.GREENSCREEN_IS_ACTIVE):
            self.nextPageEvent()
        else:
            self.currentBackgroundImageIndex = 0
            self._navigationBackgroundButtonStatus()
            self._setBrackgroundPreview()
            self._updateTitle()

    def _backPageEvent(self):
        self.greenscreenBackgroundService.cleanCustomBackground()
        self.backPageEvent()

    def _updateTitle(self):
        self.title.setText(textValue[TextKey.PAGE_GREENSCREEN_SELECT_BACKGROUND_TITLE]+" ("+str(self.currentBackgroundImageIndex+1)+"/"+str(self.greenscreenBackgroundService.getBackgroundSize())+")")

    def _backgroundBackEvent(self):
        self.currentBackgroundImageIndex -= 1
        if self.currentBackgroundImageIndex < 0:
            self.currentBackgroundImageIndex = 0
        self._navigationBackgroundButtonStatus()
        self._setBrackgroundPreview()
        self._updateTitle()

    def _backgroundNextEvent(self):
        self.currentBackgroundImageIndex += 1
        if self.greenscreenBackgroundService.getBackgroundSize() <= self.currentBackgroundImageIndex:
            self.currentBackgroundImageIndex = self.greenscreenBackgroundService.getBackgroundSize() - 1
        self._navigationBackgroundButtonStatus()
        self._setBrackgroundPreview()
        self._updateTitle()

    def _rotateLeft(self):
        self.greenscreenBackgroundService.rotateBackground(self.currentBackgroundImageIndex,90)
        self._setBrackgroundPreview()

    def _rotateRight(self):
        self.greenscreenBackgroundService.rotateBackground(self.currentBackgroundImageIndex,-90)
        self._setBrackgroundPreview()

    def _navigationBackgroundButtonStatus(self):
        if self.greenscreenBackgroundService.getBackgroundSize() <= 0:
            self.leftBackgroundButton.setDisabled(True)
            self.backgroundButton.setDisabled(True)
            self.rightBackgroundButton.setDisabled(True)
            self.rightRotateBackgroundButton.setDisabled(True)
            self.leftRotateBackgroundButton.setDisabled(True)
        else:
            self.leftBackgroundButton.setDisabled(False)
            self.backgroundButton.setDisabled(False)
            self.rightBackgroundButton.setDisabled(False)
            self.rightRotateBackgroundButton.setDisabled(False)
            self.leftRotateBackgroundButton.setDisabled(False)

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
            self.backgroundButton.setMinimumSize(size)
            icon = QIcon(image)
            self.backgroundButton.setIcon(icon)
            self.backgroundButton.setIconSize(size)

    def setOwnBackgroundPage(self,ownBackgroundPage:Page):
        self.ownBackgroundPage = ownBackgroundPage

    def _setOwnBackgroundPageEvent(self):
        self.setPageEvent(self.ownBackgroundPage)

    def _nextPageEvent(self):
        self.greenscreenBackgroundService.setIndex(self.currentBackgroundImageIndex)
        self.nextPageEvent()

    def setPictureNavigationButtonStyle(self, button:QPushButton):
        button.setFixedHeight((self.getContentHeightWithNavigationButtonAndTitle()/5)*4)
        button.setStyleSheet("font-size: " + str(self.getTitelAndNavigationButtonTextSize()) + "px ;" \
                            "font-family: " + CfgService.get(CfgKey.MAIN_WINDOW_TEXT_FONT) +", serif;")

    def setPictureRotateButtonStyle(self, button:QPushButton):
        button.setFixedHeight((self.getContentHeightWithNavigationButtonAndTitle()/5))
        button.setStyleSheet("font-size: " + str(self.getTitelAndNavigationButtonTextSize()) + "px ;" \
                            "font-family: " + CfgService.get(CfgKey.MAIN_WINDOW_TEXT_FONT) +", serif;")

    def getRotateIconHight(self):
        return (self.getContentHeightWithNavigationButtonAndTitle()/5)

    def _getPictureButtonsSize(self):
        piCameraResolution = CfgService.get(CfgKey.PI_CAMERA_PHOTO_RESOLUTION)
        height = self.getContentHeightWithNavigationButtonAndTitle()
        cameraHeight = piCameraResolution[1]
        camerawidth = piCameraResolution[0]
        width = height * camerawidth / cameraHeight
        return QSize(width,height)