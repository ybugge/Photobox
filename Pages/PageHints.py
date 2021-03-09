import os
from pathlib import Path

from PyQt5.QtCore import Qt
from PyQt5.QtMultimedia import QCameraInfo
from PyQt5.QtWidgets import QPushButton, QVBoxLayout, QLabel, QScrollArea, QWidget, QTextEdit

from Pages.AllPages import AllPages
from Pages.Page import Page
from config.Config import textValue, TextKey, cfgValue, CfgKey


class PageHints(Page):
    def __init__(self, pages : AllPages):
        super().__init__(pages)
        vbox = QVBoxLayout()
        self.setLayout(vbox)
        self.camerasInfos = QCameraInfo.availableCameras()

        #Titel
        vbox.addWidget(self.getTitleAsQLabel(TextKey.PAGE_HINTS_TITLE))

        #Hinweise
        textArea = QTextEdit()
        vbox.addWidget(textArea)
        textArea.setReadOnly(True)
        textArea.append(textValue[TextKey.PAGE_HINTS_ESCAPE_HINT])
        textArea.append("")
        if not self.getExistCameras():
            textArea.append(textValue[TextKey.PAGE_HINTS_NO_CAMERA_WARN])
            textArea.append("")
        elif not self.getExistSelectedCamera():
            textArea.append(textValue[TextKey.PAGE_HINTS_NO_SELECTED_CAMERA_WARN])
            textArea.append("")
        else:
            cameraInfoText = textValue[TextKey.PAGE_HINTS_SELECTED_CAMERA_HINT] % (str(self.getCameraIndex()),self.getCameraName(), self.getCameraDescription())
            textArea.append(cameraInfoText)
            textArea.append("")

        if not self.hasFolderContent(cfgValue[CfgKey.PAGE_TITLEPICTURE_BUTTON_IMAGE_FOLDER]):
            warn = textValue[TextKey.PAGE_HINTS_NO_PICTURES_FOUND_WARN] % (cfgValue[CfgKey.PAGE_TITLEPICTURE_BUTTON_IMAGE_FOLDER])
            textArea.append(warn)
            textArea.append("")

        if not self.hasFolderContent(cfgValue[CfgKey.PAGE_CAPTUREPHOTO_LAST_IMAGE_FOLDER]):
            warn = textValue[TextKey.PAGE_HINTS_NO_PICTURES_FOUND_WARN] % (cfgValue[CfgKey.PAGE_CAPTUREPHOTO_LAST_IMAGE_FOLDER])
            textArea.append(warn)
            textArea.append("")

        #Nextbutton
        if(self.getExistCameras()
                and self.getExistCameras()
                and self.hasPageTitlePicturePictures()
                and self.hasPageCapturePhotoLastPicture()):
            nextButton = QPushButton(textValue[TextKey.PAGE_HINTS_NEXTBUTTON])
            nextButton.clicked.connect(self.nextPageEvent)
            vbox.addWidget(nextButton)


    #https://www.geeksforgeeks.org/creating-a-camera-application-using-pyqt5/
    def getExistCameras(self):
        return len(self.camerasInfos) > 0

    def getExistSelectedCamera(self):
        return len(self.camerasInfos) > cfgValue[CfgKey.USED_CAMERA_INDEX]

    def getCameraIndex(self):
        return cfgValue[CfgKey.USED_CAMERA_INDEX]

    def getCameraName(self):
        return self.camerasInfos[self.getCameraIndex()].deviceName()

    def getCameraDescription(self):
        return self.camerasInfos[self.getCameraIndex()].description()

    def hasPageTitlePicturePictures(self):
        return self.hasFolderContent(cfgValue[CfgKey.PAGE_TITLEPICTURE_BUTTON_IMAGE_FOLDER])

    def hasPageCapturePhotoLastPicture(self):
        return self.hasFolderContent(cfgValue[CfgKey.PAGE_CAPTUREPHOTO_LAST_IMAGE_FOLDER])

    def hasFolderContent(self,path:str):
        existFolder = os.path.isdir(path)
        if(not existFolder):
             return False
        return  os.listdir(path) != []
