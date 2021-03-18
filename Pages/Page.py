from PyQt5 import QtWidgets
from PyQt5.QtCore import Qt, QTimer, QSize
from PyQt5.QtWidgets import QLabel, QPushButton

from Pages import AllPages
from Services.CfgService import CfgService
from config.Config import CfgKey, textValue, TextKey


class Page(QtWidgets.QWidget):

    def __init__(self, allPages: AllPages, windowSize:QSize):
        super().__init__()
        self.allPages = allPages
        self.stackedWidgets=allPages.getStackedWidgets()
        self.windowSize = windowSize
        self.windowComponentHeightDevider = 9
        self.autoForwardActive = False
        self.autoForwardTimer = QTimer()
        self.autoForwardTimer.timeout.connect(self.autoFowardEvent)

    # AUTO FORWARD start
    def activateAutoForward(self,page, waitTime:CfgKey):
        self.autoForwardPageType = page
        self.autoForwardWaitTime = waitTime
        self.autoForwardActive = True

    def isAutoForwardActive(self):
        return self.autoForwardActive

    def startAutoForwardTimer(self):
        self.autoForwardTimer.start(CfgService.get(self.autoForwardWaitTime))

    def stopAutoForwardTimer(self):
        self.autoForwardTimer.stop()

    def resetAutoForwardTimer(self):
        self.stopAutoForwardTimer()
        self.startAutoForwardTimer()

    def autoFowardEvent(self):
        self.executeInAutoForwardTimerEvent()
        self.setPageEvent(self.autoForwardPageType)

    def executeInAutoForwardTimerEvent(self):
        pass

    # AUTO FORWARD stop

    def setBackPage(self,backPage):
        self.backPage = backPage

    def nextPageEvent(self):
        self.setPageEvent(self.nextPage)

    def setNextPage(self,nextPage):
        self.nextPage = nextPage

    def backPageEvent(self):
        self.setPageEvent(self.backPage)

    def setPageEvent(self, type):
        isFound = False
        for page in self.allPages.getPages():
            if isinstance(page, type):

                if self.isAutoForwardActive():
                    self.stopAutoForwardTimer()
                self.allPages.getCurrentPage().executeAfter()

                index = self.allPages.getPages().index(page)
                self.allPages.setCurrentIndex(index)
                page.executeBefore()
                if page.isAutoForwardActive():
                    page.startAutoForwardTimer()
                isFound = True
        if(not isFound):
            print("Index wurde nicht gefunden!")

    def executeBefore(self):
        pass

    def executeAfter(self):
        pass

    def getTitleAsQLabel(self,text:TextKey):
        title = QLabel()
        title.setText(textValue[text])
        title.setFixedHeight(self.__getTitleAndNavigationButtonHeight())
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet(self.__getTitleStyle())
        return title

    def __getTitleStyle(self):
        return  ("background-color:" + CfgService.get(CfgKey.TITLE_BACKGROUND_COLOR) + ";"\
            "color:" + CfgService.get(CfgKey.TITLE_COLOR) +";"\
            "font-size: " + str(self.__getTitelAndNavigationButtonTextSize()) +"px ;"\
            "font-family: " + CfgService.get(CfgKey.TITLE_FONT) +", serif;")

    def setNavigationbuttonStyle(self, button:QPushButton):
        button.setFixedHeight(self.__getTitleAndNavigationButtonHeight())
        button.setStyleSheet("background-color: "+CfgService.get(CfgKey.MAIN_WINDOW_BUTTON_BACKGROUND_COLOR)+";"\
                            "font-size: " + str(self.__getTitelAndNavigationButtonTextSize()) +"px ;" \
                            "font-family: " + CfgService.get(CfgKey.MAIN_WINDOW_TEXT_FONT) +", serif;")

    def setContentButtonStyle(self,button:QPushButton):
        button.setFixedHeight(int(self.__getTitleAndNavigationButtonHeight()*(1/3)))

    def __getTitelAndNavigationButtonTextSize(self):
        return int(self.__getTitleAndNavigationButtonHeight()*(2/4))

    def __getContentHeightWithNavigationButton(self):
        return (self.__getTitleAndNavigationButtonHeight())*(self.windowComponentHeightDevider-1)

    def __getContentHeightWithNavigationButtonAndTitle(self):
        return (self.__getTitleAndNavigationButtonHeight())*(self.windowComponentHeightDevider-2)

    def __getTitleAndNavigationButtonHeight(self):
        return self.windowSize.height()/self.windowComponentHeightDevider