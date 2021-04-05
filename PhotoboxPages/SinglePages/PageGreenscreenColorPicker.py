from PyQt5.QtCore import QSize, Qt
from PyQt5.QtGui import QPixmap, QImage, QColor
from PyQt5.QtWidgets import QVBoxLayout, QHBoxLayout, QLineEdit, QPushButton, QLabel

from PhotoboxPages.AllPages import AllPages
from PhotoboxPages.Page import Page
from Services.Camera.CameraService import CameraService
from config.Config import textValue, TextKey


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
        colorLayout.addWidget(self.averageColorLabel)

        self.minColorLabel = QLineEdit()
        colorLayout.addWidget(self.minColorLabel)

        self.maxColorLabel = QLineEdit()
        colorLayout.addWidget(self.maxColorLabel)

        self.averageFromMinMaxColorLabel = QLineEdit()
        colorLayout.addWidget(self.averageFromMinMaxColorLabel)


        #Picture
        self.picture = QLabel()
        self.picture.setAlignment(Qt.AlignCenter)
        mainLayout.addWidget(self.picture)


        #Navigation   ##################################################################################################
        navigationLayout = QHBoxLayout()
        mainLayout.addLayout(navigationLayout)

        backButton = QPushButton(textValue[TextKey.PAGE_CONFIG_BACKBUTTON])
        backButton.clicked.connect(self.backPageEvent)
        self.setNavigationbuttonStyle(backButton)
        navigationLayout.addWidget(backButton)

        capturePhotoButton = QPushButton(textValue[TextKey.PAGE_GREENSCREEN_COLOR_PICKER_CAPTURE_PHOTO_BUTTON])
        capturePhotoButton.clicked.connect(self._capturePhoto)
        self.setNavigationbuttonStyle(capturePhotoButton)
        navigationLayout.addWidget(capturePhotoButton)

    def executeBefore(self):
        self._capturePhoto()

    def _capturePhoto(self):
        rawAndPreviewPicture = self.camera.getImage()
        self._updatePreviewPicture(rawAndPreviewPicture[1])
        self._scannImage(rawAndPreviewPicture[1])

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

        averageQColor = QColor.fromHsv(round(averageColor[0]),round(averageColor[1]),round(averageColor[2]),255)
        minQColor = QColor.fromHsv(round(minColor[0]),round(minColor[1]),round(minColor[2]),255)
        maxQColor = QColor.fromHsv(round(maxColor[0]),round(maxColor[1]),round(maxColor[2]),255)
        minMaxQColor = QColor.fromHsv(round((minColor[0]+maxColor[0])/2),round((minColor[1]+maxColor[1])/2),round((minColor[2]+maxColor[2])/2),255)


        self._updateMonitoringLabel(self.averageColorLabel,averageQColor,"Ø:")
        self._updateMonitoringLabel(self.minColorLabel,minQColor,"Min:")
        self._updateMonitoringLabel(self.maxColorLabel,maxQColor,"Max:")
        self._updateMonitoringLabel(self.averageFromMinMaxColorLabel,minMaxQColor,"X̅:")

    def _updateMonitoringLabel(self,label:QLabel, color:QColor, additionalText:str):
        label.setStyleSheet("background-color:rgb("+str(color.getRgb()[0])+","+str(color.getRgb()[1])+","+str(color.getRgb()[2])+")")
        label.setText(additionalText+" "+str(color.getHsv()))

    def _updateMinColor(self,minColor,rgbColor,index):
        if(minColor[index] > rgbColor[index]):
            minColor[index] = rgbColor[index]

    def _updateMaxColor(self,maxColor,rgbColor,index):
        if(maxColor[index] < rgbColor[index]):
            maxColor[index] = rgbColor[index]