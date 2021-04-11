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
from config.Config import textValue, TextKey, CfgKey


class PageGreenscreenColorPicker(Page):
    def __init__(self, pages : AllPages, windowsize:QSize, globalPagesVariable:GlobalPagesVariableService):
        super().__init__(pages,windowsize)
        self.globalPagesVariable = globalPagesVariable

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
        cv2HsvImage, preview = self.camera.getImage()
        self._updatePreviewPicture(preview)
        self._scannImageForProperties(cv2HsvImage)
        self._scannImageForPreview(preview)
        self.saveButton.setText(textValue[TextKey.PAGE_GREENSCREEN_COLOR_PICKER_SAVE_BUTTON])
        self.saveButton.setDisabled(False)

    def _updatePreviewPicture(self,preview:QImage):
        self.picture.setPixmap(QPixmap.fromImage(preview))

    def _scannImageForProperties(self, image):
        self.minCV2 = image.min(axis=(0, 1)).astype(int)
        self.maxCV2 = image.max(axis=(0, 1)).astype(int)
        self.averageCV2 = np.average(image,axis=(0, 1)).astype(int)

        self._setColorLabelText(self.minColorLabel,self.minCV2,"Min:")
        self._setColorLabelText(self.maxColorLabel,self.maxCV2,"Max:")
        self._setColorLabelText(self.averageColorLabel,self.averageCV2,"Ø:")

    def _setColorLabelText(self,label:QLabel, color, additionalText:str):
        label.setText(additionalText+" ("+str(color[0])+","+str(color[1])+","+str(color[2])+")")

    def _scannImageForPreview(self, image:QImage):
        imageSize = image.size()

        averageColor = [0,0,0]
        minColor = [360,255,255]
        maxColor = [0,0,0]
        for x in range(imageSize.width()):
            averageColumnColor = [0,0,0]
            for y in range(imageSize.height()):
                color = image.pixelColor(x,y)
                hsvColor = color.getHsv()
                averageColumnColor[0] += hsvColor[0]
                averageColumnColor[1] += hsvColor[1]
                averageColumnColor[2] += hsvColor[2]

                self._updateMinColor(minColor,hsvColor,0)
                self._updateMinColor(minColor,hsvColor,1)
                self._updateMinColor(minColor,hsvColor,2)
                self._updateMaxColor(maxColor,hsvColor,0)
                self._updateMaxColor(maxColor,hsvColor,1)
                self._updateMaxColor(maxColor,hsvColor,2)

            averageColumnColor[0] /= imageSize.height()
            averageColumnColor[1] /= imageSize.height()
            averageColumnColor[2] /= imageSize.height()
            averageColor[0] += averageColumnColor[0]
            averageColor[1] += averageColumnColor[1]
            averageColor[2] += averageColumnColor[2]
        averageColor[0] /= imageSize.width()
        averageColor[1] /= imageSize.width()
        averageColor[2] /= imageSize.width()

        self.averageQColor = QColor.fromHsv(round(averageColor[0]),round(averageColor[1]),round(averageColor[2]),255)
        self.minQColor = QColor.fromHsv(round(minColor[0]),round(minColor[1]),round(minColor[2]),255)
        self.maxQColor = QColor.fromHsv(round(maxColor[0]),round(maxColor[1]),round(maxColor[2]),255)

        self._updateMonitoringLabel(self.averageColorLabel,self.averageQColor)
        self._updateMonitoringLabel(self.minColorLabel,self.minQColor)
        self._updateMonitoringLabel(self.maxColorLabel,self.maxQColor)
        self._setHint(maxColor[0] - minColor[0] > CfgService.get(CfgKey.GREENSCREEN_MAX_COLOR_RANGE_HINT))


    def _updateMonitoringLabel(self,label:QLabel, color:QColor):
        label.setStyleSheet("background-color:rgb("+str(color.getRgb()[0])+","+str(color.getRgb()[1])+","+str(color.getRgb()[2])+")")

    def _updateMinColor(self,minColor,rgbColor,index):
        if(minColor[index] > rgbColor[index]):
            minColor[index] = rgbColor[index]

    def _updateMaxColor(self,maxColor,rgbColor,index):
        if(maxColor[index] < rgbColor[index]):
            maxColor[index] = rgbColor[index]

    def _setHint(self,colorRangeToBig:bool):
        if colorRangeToBig:
            self.hintLabel.setText(textValue[TextKey.PAGE_GREENSCREEN_COLOR_PICKER_HINT_FAILED])
            self.hintLabel.setStyleSheet("color:red")
        else:
            self.hintLabel.setText(textValue[TextKey.PAGE_GREENSCREEN_COLOR_PICKER_HINT_OK])
            self.hintLabel.setStyleSheet("color:green")

    def _saveEvent(self):
        CfgService.setColor(CfgKey.GREENSCREEN_MIN_HSV_GUI_COLOR, self.minQColor)
        CfgService.setColor(CfgKey.GREENSCREEN_MAX_HSV_GUI_COLOR, self.maxQColor)
        CfgService.setColor(CfgKey.GREENSCREEN_AVERAGE_HSV_GUI_COLOR, self.averageQColor)
        CfgService.setIntList(CfgKey.GREENSCREEN_MIN_HSV_CV2_COLOR, self.minCV2)
        CfgService.setIntList(CfgKey.GREENSCREEN_MAX_HSV_CV2_COLOR, self.maxCV2)
        CfgService.setIntList(CfgKey.GREENSCREEN_AVERAGE_HSV_CV2_COLOR, self.averageCV2)
        self.saveButton.setText(textValue[TextKey.PAGE_GREENSCREEN_COLOR_PICKER_SAVE_SUCCESS_BUTTON])
        self.saveButton.setDisabled(True)

    def setTolerancePage(self,tolerancePage):
        self.tolerancePage = tolerancePage

    def _toleranceButtonEvent(self):
        self.setPageEvent(self.tolerancePage)

    def _backPageSelectEvent(self):
        if self.globalPagesVariable.getUserMode():
            self._backPageIsInUserModeEvent()
        else:
            self.backPageEvent()

    def setBackPageIsInUserMode(self,backPageIsInUserMode):
        self.backPageIsInUserMode = backPageIsInUserMode

    def _backPageIsInUserModeEvent(self):
        self.setPageEvent(self.backPageIsInUserMode)