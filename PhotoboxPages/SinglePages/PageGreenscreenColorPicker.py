import time

from PyQt5.QtCore import QSize, Qt
from PyQt5.QtGui import QPixmap, QImage, QColor
from PyQt5.QtWidgets import QVBoxLayout, QHBoxLayout, QLineEdit, QPushButton, QLabel

from PhotoboxPages.AllPages import AllPages
from PhotoboxPages.Page import Page
from Services.Camera.CameraService import CameraService
from Services.CfgService import CfgService
from config.Config import textValue, TextKey, CfgKey


class PageGreenscreenColorPicker(Page):
    def __init__(self, pages : AllPages, windowsize:QSize):
        super().__init__(pages,windowsize)

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

        self.averageFromMinMaxColorLabel = QLineEdit()
        self.averageFromMinMaxColorLabel.setReadOnly(True)
        colorLayout.addWidget(self.averageFromMinMaxColorLabel)

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

        capturePhotoButton = QPushButton(textValue[TextKey.PAGE_GREENSCREEN_COLOR_PICKER_CAPTURE_PHOTO_BUTTON])
        capturePhotoButton.clicked.connect(self._capturePhotoEvent)
        self.setNavigationbuttonStyle(capturePhotoButton)
        navigationTopLayout.addWidget(capturePhotoButton)

        #Bottom ------------------------------------------------
        navigationBottomLayout = QHBoxLayout()
        mainLayout.addLayout(navigationBottomLayout)

        backButton = QPushButton(textValue[TextKey.PAGE_CONFIG_BACKBUTTON])
        backButton.clicked.connect(self.backPageEvent)
        self.setNavigationbuttonStyle(backButton)
        navigationBottomLayout.addWidget(backButton)

        self.saveButton = QPushButton(textValue[TextKey.PAGE_GREENSCREEN_COLOR_PICKER_SAVE_BUTTON])
        self.saveButton.clicked.connect(self._saveEvent)
        self.setNavigationbuttonStyle(self.saveButton)
        navigationBottomLayout.addWidget(self.saveButton)



    def executeBefore(self):
        self._capturePhoto()

    def _capturePhotoEvent(self):
        time.sleep(2)
        self._capturePhoto()

    def _capturePhoto(self):
        rawAndPreviewPicture = self.camera.getImage()
        self._updatePreviewPicture(rawAndPreviewPicture[1])
        self._scannImage(rawAndPreviewPicture[1])
        self.saveButton.setText(textValue[TextKey.PAGE_GREENSCREEN_COLOR_PICKER_SAVE_BUTTON])
        self.saveButton.setDisabled(False)

    def _updatePreviewPicture(self,preview:QImage):
        self.picture.setPixmap(QPixmap.fromImage(preview))

    def _scannImage(self,image:QImage):
        imageSize = image.size()

        averageColor = [0,0,0]
        minColor = [255,255,255]
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
        minMaxQColor = QColor.fromHsv(round((minColor[0]+maxColor[0])/2),round((minColor[1]+maxColor[1])/2),round((minColor[2]+maxColor[2])/2),255)

        self._updateMonitoringLabel(self.averageColorLabel,self.averageQColor,"Ø:")
        self._updateMonitoringLabel(self.minColorLabel,self.minQColor,"Min:")
        self._updateMonitoringLabel(self.maxColorLabel,self.maxQColor,"Max:")
        self._updateMonitoringLabel(self.averageFromMinMaxColorLabel,minMaxQColor,"X̅:")
        self._setHint(maxColor[0] - minColor[0] > CfgService.get(CfgKey.GREENSCREEN_MAX_COLOR_RANGE_HINT))


    def _updateMonitoringLabel(self,label:QLabel, color:QColor, additionalText:str):
        label.setStyleSheet("background-color:rgb("+str(color.getRgb()[0])+","+str(color.getRgb()[1])+","+str(color.getRgb()[2])+")")
        label.setText(additionalText+" ("+str(color.getHsv()[0])+","+str(color.getHsv()[1])+","+str(color.getHsv()[2])+")")

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
        CfgService.setColor(CfgKey.GREENSCREEN_MIN_HSV_COLOR_WITHOUT_TOLERANCE,self.minQColor)
        CfgService.setColor(CfgKey.GREENSCREEN_MAX_HSV_COLOR_WITHOUT_TOLERANCE,self.maxQColor)
        CfgService.setColor(CfgKey.GREENSCREEN_AVERAGE_HSV_COLOR_WITHOUT_TOLERANCE,self.averageQColor)
        self.saveButton.setText(textValue[TextKey.PAGE_GREENSCREEN_COLOR_PICKER_SAVE_SUCCESS_BUTTON])
        self.saveButton.setDisabled(True)

    def setTolerancePage(self,tolerancePage):
        self.tolerancePage = tolerancePage

    def _toleranceButtonEvent(self):
        self.setPageEvent(self.tolerancePage)