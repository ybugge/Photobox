from PyQt5.QtCore import QSize
from PyQt5.QtGui import QIntValidator
from PyQt5.QtWidgets import QVBoxLayout, QPushButton, QHBoxLayout, QLabel, QLineEdit

from PhotoboxPages.AllPages import AllPages
from PhotoboxPages.Page import Page
from Services.CfgService import CfgService
from config.Config import TextKey, textValue, CfgKey


class PageGreenscreenToleranceConfig(Page):
    def __init__(self, pages : AllPages, windowsize:QSize):
        super().__init__(pages,windowsize)

        mainLayout = QVBoxLayout()
        mainLayout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(mainLayout)

        #Titel
        mainLayout.addWidget(self.getTitleAsQLabel(TextKey.PAGE_GREENSCREEN_TOLERANCE_CONFIG_TITLE))

        #Positiv tolerance:
        posLabel = QLabel()
        posLabel.setText(textValue[TextKey.PAGE_GREENSCREEN_TOLERANCE_CONFIG_POS_LABEL])
        mainLayout.addWidget(posLabel)

        posToleranceLayout = QHBoxLayout()
        mainLayout.addLayout(posToleranceLayout)

        self.posHTextField = QLineEdit()
        self.posHTextField.setValidator(QIntValidator())
        posToleranceLayout.addWidget(self.posHTextField)

        self.posSTextField = QLineEdit()
        self.posSTextField.setValidator(QIntValidator())
        posToleranceLayout.addWidget(self.posSTextField)

        self.posVTextField = QLineEdit()
        self.posVTextField.setValidator(QIntValidator())
        posToleranceLayout.addWidget(self.posVTextField)

        #Negativ tolerance:
        negLabel = QLabel()
        negLabel.setText(textValue[TextKey.PAGE_GREENSCREEN_TOLERANCE_CONFIG_NEG_LABEL])
        mainLayout.addWidget(negLabel)

        negToleranceLayout = QHBoxLayout()
        mainLayout.addLayout(negToleranceLayout)

        self.negHTextField = QLineEdit()
        self.negHTextField.setValidator(QIntValidator())
        negToleranceLayout.addWidget(self.negHTextField)

        self.negSTextField = QLineEdit()
        self.negSTextField.setValidator(QIntValidator())
        negToleranceLayout.addWidget(self.negSTextField)

        self.negVTextField = QLineEdit()
        self.negVTextField.setValidator(QIntValidator())
        negToleranceLayout.addWidget(self.negVTextField)

        #Navigation   ##################################################################################################
        mainLayout.addStretch()
        navigationLayout = QHBoxLayout()
        mainLayout.addLayout(navigationLayout)

        backButton = QPushButton(textValue[TextKey.PAGE_GREENSCREEN_TOLERANCE_CONFIG_BACK_BUTTON])
        backButton.clicked.connect(self.backPageEvent)
        self.setNavigationbuttonStyle(backButton)
        navigationLayout.addWidget(backButton)

    def executeBefore(self):
        posToleranceValues = CfgService.getIntList(CfgKey.GREENSCREEN_COLOR_TOLERANCE_POS)
        self.posHTextField.setText(str(posToleranceValues[0]))
        self.posSTextField.setText(str(posToleranceValues[1]))
        self.posVTextField.setText(str(posToleranceValues[2]))
        negToleranceValues = CfgService.getIntList(CfgKey.GREENSCREEN_COLOR_TOLERANCE_NEG)
        self.negHTextField.setText(str(negToleranceValues[0]))
        self.negSTextField.setText(str(negToleranceValues[1]))
        self.negVTextField.setText(str(negToleranceValues[2]))

    def executeAfter(self):
        posToleranceValues = [int(self.posHTextField.text()),int(self.posSTextField.text()),int(self.posVTextField.text())]
        negToleranceValues = [int(self.negHTextField.text()),int(self.negSTextField.text()),int(self.negVTextField.text())]
        CfgService.setIntList(CfgKey.GREENSCREEN_COLOR_TOLERANCE_POS,posToleranceValues)
        CfgService.setIntList(CfgKey.GREENSCREEN_COLOR_TOLERANCE_NEG,negToleranceValues)
