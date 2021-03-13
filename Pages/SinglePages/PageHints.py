from PyQt5.QtMultimedia import QCameraInfo
from PyQt5.QtWidgets import QPushButton, QVBoxLayout, QTextEdit, QHBoxLayout

from Pages.AllPages import AllPages
from Pages.Page import Page
from Services.CfgService import CfgService
from Services.FileFolderService import FileFolderService
from config.Config import textValue, TextKey, CfgKey


class PageHints(Page):
    def __init__(self, pages : AllPages):
        super().__init__(pages)
        vbox = QVBoxLayout()
        self.setLayout(vbox)
        self.camerasInfos = QCameraInfo.availableCameras()

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
        navigationBox.addWidget(pictureManagerButton)

        self.nextButton = QPushButton(textValue[TextKey.PAGE_HINTS_NEXTBUTTON])
        self.nextButton.clicked.connect(self.nextPageEvent)
        navigationBox.addWidget(self.nextButton)
        self.disableNextButton()



    def executeBefore(self):
        self.setHints()
        self.disableNextButton()

    def disableNextButton(self):
        if(self.getExistCameras()
                and self.getExistCameras()
                and self.hasPageTitlePicturePictures()
                and self.hasPageCapturePhotoLastPicture()):
            self.nextButton.setDisabled(False)
        else:
            self.nextButton.setDisabled(True)

    def setHints(self):
        self.textArea.clear()
        self.textArea.append(textValue[TextKey.PAGE_HINTS_ESCAPE_HINT])
        self.textArea.append("")
        if not self.getExistCameras():
            self.textArea.append(textValue[TextKey.PAGE_HINTS_NO_CAMERA_WARN])
            self.textArea.append("")
        elif not self.getExistSelectedCamera():
            self.textArea.append(textValue[TextKey.PAGE_HINTS_NO_SELECTED_CAMERA_WARN])
            self.textArea.append("")
        else:
            cameraInfoText = textValue[TextKey.PAGE_HINTS_SELECTED_CAMERA_HINT] % (str(self.getCameraIndex()),self.getCameraName(), self.getCameraDescription())
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

    #https://www.geeksforgeeks.org/creating-a-camera-application-using-pyqt5/
    def getExistCameras(self):
        return len(self.camerasInfos) > 0

    def getExistSelectedCamera(self):
        return len(self.camerasInfos) > CfgService.get(CfgKey.USED_CAMERA_INDEX)

    def getCameraIndex(self):
        return CfgService.get(CfgKey.USED_CAMERA_INDEX)

    def getCameraName(self):
        return self.camerasInfos[self.getCameraIndex()].deviceName()

    def getCameraDescription(self):
        return self.camerasInfos[self.getCameraIndex()].description()

    def hasPageTitlePicturePictures(self):
        return FileFolderService.hasFolderContent(CfgService.get(CfgKey.PAGE_TITLEPICTURE_BUTTON_IMAGE_FOLDER))

    def hasPageCapturePhotoLastPicture(self):
        return FileFolderService.hasFolderContent(CfgService.get(CfgKey.PAGE_CAPTUREPHOTO_LAST_IMAGE_FOLDER))

