from PyQt5.QtCore import QSize, pyqtSlot, Qt
from PyQt5.QtGui import QIntValidator, QImage, QPixmap
from PyQt5.QtWidgets import QVBoxLayout, QPushButton, QHBoxLayout, QLabel, QLineEdit, QWidget

from PhotoboxPages.AllPages import AllPages
from PhotoboxPages.Page import Page
from Services.Camera.CameraService import CameraService
from Services.CfgService import CfgService
from Services.GlobalPagesVariableService import GlobalPagesVariableService
from Services.Greenscreen.GreenscreenBackgroundService import GreenscreenBackgroundService
from config.Config import TextKey, textValue, CfgKey


class PageGreenscreenToleranceConfig(Page):
    def __init__(self, pages : AllPages, windowsize:QSize,globalVariable:GlobalPagesVariableService):
        super().__init__(pages,windowsize)

        self.globalVariable = globalVariable
        mainLayout = QVBoxLayout()
        mainLayout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(mainLayout)
        self.minMaxStore = None

        #Titel
        mainLayout.addWidget(self.getTitleAsQLabel(TextKey.PAGE_GREENSCREEN_TOLERANCE_CONFIG_TITLE))

        #Positiv tolerance:
        posToleranceLayout = QHBoxLayout()
        mainLayout.addLayout(posToleranceLayout)

        self.posHTextField = QLineEdit()
        self.posHTextField.setValidator(QIntValidator())
        self.posHTextField.textChanged.connect(self._posTextFieldEvent)
        posToleranceLayout.addWidget(self.posHTextField)

        self.posSTextField = QLineEdit()
        self.posSTextField.setValidator(QIntValidator())
        self.posSTextField.textChanged.connect(self._posTextFieldEvent)
        posToleranceLayout.addWidget(self.posSTextField)

        self.posVTextField = QLineEdit()
        self.posVTextField.setValidator(QIntValidator())
        self.posVTextField.textChanged.connect(self._posTextFieldEvent)
        posToleranceLayout.addWidget(self.posVTextField)

        #current tolerance:
        curToleranceLayout = QHBoxLayout()
        mainLayout.addLayout(curToleranceLayout)

        self.curHTextField = QLineEdit()
        self.curHTextField.setValidator(QIntValidator())
        self.curHTextField.setReadOnly(True)
        curToleranceLayout.addWidget(self.curHTextField)

        self.curSTextField = QLineEdit()
        self.curSTextField.setValidator(QIntValidator())
        self.curSTextField.setReadOnly(True)
        curToleranceLayout.addWidget(self.curSTextField)

        self.curVTextField = QLineEdit()
        self.curVTextField.setValidator(QIntValidator())
        self.curVTextField.setReadOnly(True)
        curToleranceLayout.addWidget(self.curVTextField)

        #Negativ tolerance:
        negToleranceLayout = QHBoxLayout()
        mainLayout.addLayout(negToleranceLayout)

        self.negHTextField = QLineEdit()
        self.negHTextField.setValidator(QIntValidator())
        self.negHTextField.textChanged.connect(self._negTextFieldEvent)
        negToleranceLayout.addWidget(self.negHTextField)

        self.negSTextField = QLineEdit()
        self.negSTextField.setValidator(QIntValidator())
        self.negSTextField.textChanged.connect(self._negTextFieldEvent)
        negToleranceLayout.addWidget(self.negSTextField)

        self.negVTextField = QLineEdit()
        self.negVTextField.setValidator(QIntValidator())
        self.negVTextField.textChanged.connect(self._negTextFieldEvent)
        negToleranceLayout.addWidget(self.negVTextField)

        mainLayout.addStretch()
        #Video
        widget = QWidget()
        mainLayout.addWidget(widget)

        self.videoLabel = QLabel(widget)
        self.videoLabel.setAlignment(Qt.AlignCenter)
        self.videoThread = None

        videoLayout = QHBoxLayout(widget)
        videoLayout.setContentsMargins(0, 0, 0, 0)
        videoLayout.addWidget(self.videoLabel)


        #Navigation   ##################################################################################################
        mainLayout.addStretch()
        navigationLayout = QHBoxLayout()
        mainLayout.addLayout(navigationLayout)

        backButton = QPushButton(textValue[TextKey.PAGE_GREENSCREEN_TOLERANCE_CONFIG_BACK_BUTTON])
        backButton.clicked.connect(self._onlyBackEvent)
        self.setNavigationbuttonStyle(backButton)
        navigationLayout.addWidget(backButton)

        saveAndbackButton = QPushButton(textValue[TextKey.PAGE_GREENSCREEN_TOLERANCE_CONFIG_SAVE_AND_BACK_BUTTON])
        saveAndbackButton.clicked.connect(self._saveAndBackEvent)
        self.setNavigationbuttonStyle(saveAndbackButton)
        navigationLayout.addWidget(saveAndbackButton)

    def executeBefore(self):
        posToleranceValues = CfgService.getIntList(CfgKey.GREENSCREEN_MAX_HSV_CV2_COLOR)
        self.posHTextField.setText(str(posToleranceValues[0]))
        self.posSTextField.setText(str(posToleranceValues[1]))
        self.posVTextField.setText(str(posToleranceValues[2]))
        negToleranceValues = CfgService.getIntList(CfgKey.GREENSCREEN_MIN_HSV_CV2_COLOR)
        self.negHTextField.setText(str(negToleranceValues[0]))
        self.negSTextField.setText(str(negToleranceValues[1]))
        self.negVTextField.setText(str(negToleranceValues[2]))

        self.minMaxStore = [negToleranceValues,posToleranceValues]
        background = GreenscreenBackgroundService(self.globalVariable).getBlackBackgroundAsHsv(CfgService.get(CfgKey.PI_CAMERA_VIDEO_RESOLUTION))
        self.videoThread = CameraService.initialAndStartVideo(QSize(self.windowSize.width()/2,self.windowSize.height()/2),self.globalVariable,self.setVideoStreamToLabel,background,self.setHsvPixelToLabel)

    def executeAfter(self):
        self.videoThread.stop()

    def _saveAndBackEvent(self):
        posToleranceValues = [int(self.posHTextField.text()),int(self.posSTextField.text()),int(self.posVTextField.text())]
        negToleranceValues = [int(self.negHTextField.text()),int(self.negSTextField.text()),int(self.negVTextField.text())]
        CfgService.setIntList(CfgKey.GREENSCREEN_MAX_HSV_CV2_COLOR,posToleranceValues)
        CfgService.setIntList(CfgKey.GREENSCREEN_MIN_HSV_CV2_COLOR,negToleranceValues)
        self.backPageEvent()

    def _onlyBackEvent(self):
        CfgService.setIntList(CfgKey.GREENSCREEN_MAX_HSV_CV2_COLOR,self.minMaxStore[1])
        CfgService.setIntList(CfgKey.GREENSCREEN_MIN_HSV_CV2_COLOR,self.minMaxStore[0])
        self.backPageEvent()

    @pyqtSlot(QImage)
    def setVideoStreamToLabel(self, image):
        self.videoLabel.setPixmap(QPixmap.fromImage(image))

    @pyqtSlot(list)
    def setHsvPixelToLabel(self, hsv):
        self.curHTextField.setText(str(hsv[0]))
        self.curSTextField.setText(str(hsv[1]))
        self.curVTextField.setText(str(hsv[2]))

    def _posTextFieldEvent(self):
        hAsString = self.posHTextField.text()
        sAsString = self.posSTextField.text()
        vAsString = self.posVTextField.text()
        if len(hAsString) > 0 and len(sAsString) > 0 and len(vAsString) > 0:
            h = max(min(int(hAsString),179),0)
            s = max(min(int(sAsString),255),0)
            v = max(min(int(vAsString),255),0)
            CfgService.setIntList(CfgKey.GREENSCREEN_MAX_HSV_CV2_COLOR,[h,s,v])

    def _negTextFieldEvent(self):
        hAsString = self.negHTextField.text()
        sAsString = self.negSTextField.text()
        vAsString = self.negVTextField.text()
        if len(hAsString) > 0 and len(sAsString) > 0 and len(vAsString) > 0:
            h = max(min(int(hAsString),179),0)
            s = max(min(int(sAsString),255),0)
            v = max(min(int(vAsString),255),0)
            CfgService.setIntList(CfgKey.GREENSCREEN_MIN_HSV_CV2_COLOR,[h,s,v])