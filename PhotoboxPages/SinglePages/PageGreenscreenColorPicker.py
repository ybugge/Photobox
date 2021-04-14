import time

import numpy as np
from PyQt5.QtCore import QSize, Qt
from PyQt5.QtGui import QPixmap, QImage, QColor
from PyQt5.QtWidgets import QVBoxLayout, QHBoxLayout, QLineEdit, QPushButton, QLabel

from PhotoboxPages.AllPages import AllPages
from PhotoboxPages.Page import Page
from Services.Camera.CameraService import CameraService
from Services.CfgService import CfgService
from Services.GlobalPagesVariableService import GlobalPagesVariableService
from Services.Greenscreen.GreenscreenColorRangeService import GreenscreenColorRangeService
from config.Config import textValue, TextKey, CfgKey


class PageGreenscreenColorPicker(Page):
    def __init__(self, pages : AllPages, windowsize:QSize, globalPagesVariable:GlobalPagesVariableService):
        super().__init__(pages,windowsize)
        self.globalPagesVariable = globalPagesVariable
        self.greenscreenColorRangeService = GreenscreenColorRangeService()
        self.camera = CameraService.initGreenscreenCalibrationCam(QSize(windowsize.width()/2,windowsize.height()/2))
        mainLayout = QVBoxLayout()
        mainLayout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(mainLayout)

        #Titel
        mainLayout.addWidget(self.getTitleAsQLabel(TextKey.PAGE_GREENSCREEN_COLOR_PICKER_TITLE))

        #Monitoring:
        colorLayout = QHBoxLayout()
        mainLayout.addLayout(colorLayout)

        self.averageColorLabel = QLineEdit()
        self.averageColorLabel.setReadOnly(True)
        colorLayout.addWidget(self.averageColorLabel)

        self.minColorLabel = QLineEdit()
        self.minColorLabel.setReadOnly(True)
        colorLayout.addWidget(self.minColorLabel)

        self.maxColorLabel = QLineEdit()
        self.maxColorLabel.setReadOnly(True)
        colorLayout.addWidget(self.maxColorLabel)

        #Hinweis:
        self.hintLabel = QLabel()
        mainLayout.addWidget(self.hintLabel)

        #Picture
        mainLayout.addStretch()
        self.picture = QLabel()
        self.picture.setAlignment(Qt.AlignCenter)
        mainLayout.addWidget(self.picture)


        #Buttons   ##################################################################################################
        mainLayout.addStretch()
        navigationTopLayout = QHBoxLayout()
        mainLayout.addLayout(navigationTopLayout)

        toleranceButton = QPushButton(textValue[TextKey.PAGE_GREENSCREEN_COLOR_PICKER_TOLERANCE_BUTTON])
        toleranceButton.clicked.connect(self._toleranceButtonEvent)
        self.setNavigationbuttonStyle(toleranceButton)
        navigationTopLayout.addWidget(toleranceButton)

        self.capturePhotoButton = QPushButton(textValue[TextKey.PAGE_GREENSCREEN_COLOR_PICKER_CAPTURE_PHOTO_BUTTON])
        self.capturePhotoButton.clicked.connect(self._capturePhotoEvent)
        self.setNavigationbuttonStyle(self.capturePhotoButton)
        navigationTopLayout.addWidget(self.capturePhotoButton)

        #Bottom ------------------------------------------------
        navigationBottomLayout = QHBoxLayout()
        mainLayout.addLayout(navigationBottomLayout)

        backButton = QPushButton(textValue[TextKey.PAGE_CONFIG_BACKBUTTON])
        backButton.clicked.connect(self._backPageSelectEvent)
        self.setNavigationbuttonStyle(backButton)
        navigationBottomLayout.addWidget(backButton)

        self.saveButton = QPushButton(textValue[TextKey.PAGE_GREENSCREEN_COLOR_PICKER_SAVE_BUTTON])
        self.saveButton.clicked.connect(self._saveEvent)
        self.setNavigationbuttonStyle(self.saveButton)
        navigationBottomLayout.addWidget(self.saveButton)

    def executeBefore(self):
        self._capturePhoto()

    def _capturePhotoEvent(self):
        self.capturePhotoButton.setDisabled(True)
        time.sleep(2)
        self._capturePhoto()
        self.capturePhotoButton.setDisabled(False)

    def _capturePhoto(self):
        frame, preview = self.camera.getImage()
        self._updatePreviewPicture(preview)
        self._scannImageForProperties(frame)
        self.saveButton.setText(textValue[TextKey.PAGE_GREENSCREEN_COLOR_PICKER_SAVE_BUTTON])
        self.saveButton.setDisabled(False)

    def _updatePreviewPicture(self,preview:QImage):
        self.picture.setPixmap(QPixmap.fromImage(preview))

    def _scannImageForProperties(self, image):
        self.greenscreenColorRangeService.scanImage(image)

        hueDiverence = self.greenscreenColorRangeService.getMaxHSV()[0] - self.greenscreenColorRangeService.getMinHSV()[0]
        self._setHint(hueDiverence > CfgService.get(CfgKey.GREENSCREEN_MAX_COLOR_RANGE_HINT))

        self._setColorLabelText(self.minColorLabel,self.greenscreenColorRangeService.getMinHSV(),"Min:")
        self._updateMonitoringLabel(self.minColorLabel,self.greenscreenColorRangeService.getMinQColor())

        self._setColorLabelText(self.maxColorLabel,self.greenscreenColorRangeService.getMaxHSV(), "Max:")
        self._updateMonitoringLabel(self.maxColorLabel,self.greenscreenColorRangeService.getMaxQColor())

        self._setColorLabelText(self.averageColorLabel,self.greenscreenColorRangeService.getAverageHSV(),"Ø:")
        self._updateMonitoringLabel(self.averageColorLabel,self.greenscreenColorRangeService.getAverageQColor())

    def _setHint(self,colorRangeToBig:bool):
        if colorRangeToBig:
            self.hintLabel.setText(textValue[TextKey.PAGE_GREENSCREEN_COLOR_PICKER_HINT_FAILED])
            self.hintLabel.setStyleSheet("color:red")
        else:
            self.hintLabel.setText(textValue[TextKey.PAGE_GREENSCREEN_COLOR_PICKER_HINT_OK])
            self.hintLabel.setStyleSheet("color:green")

    def _setColorLabelText(self,label:QLineEdit, color, additionalText:str):
        label.setText(additionalText+" "+str(color))

    def _updateMonitoringLabel(self,label:QLineEdit, color:QColor):
        label.setStyleSheet("background-color:rgb("+str(color.getRgb()[0])+","+str(color.getRgb()[1])+","+str(color.getRgb()[2])+")")

    def _saveEvent(self):
        CfgService.setColor(CfgKey.GREENSCREEN_MIN_HSV_GUI_COLOR, self.greenscreenColorRangeService.getMinQColor())
        CfgService.setColor(CfgKey.GREENSCREEN_MAX_HSV_GUI_COLOR, self.greenscreenColorRangeService.getMaxQColor())
        CfgService.setColor(CfgKey.GREENSCREEN_AVERAGE_HSV_GUI_COLOR, self.greenscreenColorRangeService.getAverageQColor())
        CfgService.setIntList(CfgKey.GREENSCREEN_MIN_HSV_CV2_COLOR, self.greenscreenColorRangeService.getMinHSV())
        CfgService.setIntList(CfgKey.GREENSCREEN_MAX_HSV_CV2_COLOR, self.greenscreenColorRangeService.getMaxHSV())
        CfgService.setIntList(CfgKey.GREENSCREEN_AVERAGE_HSV_CV2_COLOR, self.greenscreenColorRangeService.getAverageHSV())
        self.saveButton.setText(textValue[TextKey.PAGE_GREENSCREEN_COLOR_PICKER_SAVE_SUCCESS_BUTTON])
        self.saveButton.setDisabled(True)

    def setTolerancePage(self,tolerancePage):
        self.tolerancePage = tolerancePage

    def _toleranceButtonEvent(self):
        self.setPageEvent(self.tolerancePage)

    def setBackPageIsInUserMode(self,backPageIsInUserMode):
        self.backPageIsInUserMode = backPageIsInUserMode

    def _backPageSelectEvent(self):
        if self.globalPagesVariable.getUserMode():
            self._backPageIsInUserModeEvent()
        else:
            self.backPageEvent()

    def _backPageIsInUserModeEvent(self):
        self.setPageEvent(self.backPageIsInUserMode)