from PyQt5.QtCore import QSize
from PyQt5.QtMultimedia import QCameraInfo
from PyQt5.QtWidgets import QPushButton, QVBoxLayout, QTextEdit, QHBoxLayout

from Pages.AllPages import AllPages
from Pages.Page import Page
from Services.Camera.CameraService import CameraService
from Services.CfgService import CfgService
from Services.FileFolderService import FileFolderService
from config.Config import textValue, TextKey, CfgKey, cfgValue


class PageHints(Page):
    def __init__(self, pages : AllPages,windowSize:QSize):
        super().__init__(pages,windowSize)
        vbox = QVBoxLayout()
        self.setLayout(vbox)

        #Titel
        vbox.addWidget(self.getTitleAsQLabel(TextKey.PAGE_HINTS_TITLE))

        #Hinweise
        self.textArea = QTextEdit()
        vbox.addWidget(self.textArea)
        self.textArea.setReadOnly(True)
        self.setHints()

        #Navigationbuttons
        navigationBox = QHBoxLayout()
        vbox.addLayout(navigationBox)

        pictureManagerButton = QPushButton(textValue[TextKey.PAGE_HINTS_PICTURE_MANAGER_BUTTON])
        pictureManagerButton.clicked.connect(self.backPageEvent)
        self.setNavigationbuttonStyle(pictureManagerButton)
        navigationBox.addWidget(pictureManagerButton)

        self.nextButton = QPushButton(textValue[TextKey.PAGE_HINTS_NEXTBUTTON])
        self.nextButton.clicked.connect(self.nextPageEvent)
        self.setNavigationbuttonStyle(self.nextButton)
        navigationBox.addWidget(self.nextButton)
        self.disableNextButton()



    def executeBefore(self):
        self.setHints()
        self.disableNextButton()

    def disableNextButton(self):
        if((CameraService.existPiCamera() or CameraService.existCameras())
                and self.hasPageTitlePicturePictures()
                and self.hasPageCapturePhotoLastPicture()):
            self.nextButton.setDisabled(False)
        else:
            self.nextButton.setDisabled(True)

    def setHints(self):
        self.textArea.clear()
        self.textArea.append(textValue[TextKey.PAGE_HINTS_ESCAPE_HINT])
        self.textArea.append("")

        if not CameraService.existCameras() and not CameraService.existPiCamera():
            self.textArea.append(textValue[TextKey.PAGE_HINTS_NO_CAMERA_WARN])
            self.textArea.append("")
        elif not CameraService.existSelectedCamera() and not CameraService.existPiCamera():
            self.textArea.append(textValue[TextKey.PAGE_HINTS_NO_SELECTED_CAMERA_WARN])
            self.textArea.append("")
            #Erfolgsfaelle###########################################################################
        elif CameraService.existPiCamera():
            cameraInfoText = textValue[TextKey.PAGE_HINTS_SELECTED_PICAMERA_HINT]
            self.textArea.append(cameraInfoText)
            self.textArea.append("")
        else:
            cameraInfoText = textValue[TextKey.PAGE_HINTS_SELECTED_CAMERA_HINT] % (str(CameraService.getCameraIndex()),CameraService.getCameraName(), CameraService.getCameraDescription())
            self.textArea.append(cameraInfoText)
            self.textArea.append("")

        if not FileFolderService.hasFolderContent(CfgService.get(CfgKey.PAGE_TITLEPICTURE_BUTTON_IMAGE_FOLDER)):
            warn = textValue[TextKey.PAGE_HINTS_NO_PICTURES_FOUND_WARN] % (CfgService.get(CfgKey.PAGE_TITLEPICTURE_BUTTON_IMAGE_FOLDER))
            self.textArea.append(warn)
            self.textArea.append("")

        if not FileFolderService.hasFolderContent(CfgService.get(CfgKey.PAGE_CAPTUREPHOTO_LAST_IMAGE_FOLDER)):
            warn = textValue[TextKey.PAGE_HINTS_NO_PICTURES_FOUND_WARN] % (CfgService.get(CfgKey.PAGE_CAPTUREPHOTO_LAST_IMAGE_FOLDER))
            self.textArea.append(warn)
            self.textArea.append("")



    def hasPageTitlePicturePictures(self):
        return FileFolderService.hasFolderContent(CfgService.get(CfgKey.PAGE_TITLEPICTURE_BUTTON_IMAGE_FOLDER))

    def hasPageCapturePhotoLastPicture(self):
        return FileFolderService.hasFolderContent(CfgService.get(CfgKey.PAGE_CAPTUREPHOTO_LAST_IMAGE_FOLDER))

