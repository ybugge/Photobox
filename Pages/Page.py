from PyQt5 import QtWidgets
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QLabel

from Pages import AllPages
from config.Config import cfgValue, CfgKey, textValue, TextKey


class Page(QtWidgets.QWidget):

    def __init__(self, allPages: AllPages):
        super().__init__()
        self.allPages = allPages
        self.stackedWidgets=allPages.getStackedWidgets()

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
                self.allPages.getCurrentPage().executeAfter()

                index = self.allPages.getPages().index(page)
                self.allPages.setCurrentIndex(index)
                page.executeBefore()
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
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet(self.__getTitleStyle())
        return title

    def __getTitleStyle(self):
        return  ("background-color:"+cfgValue[CfgKey.TITLE_BACKGROUND_COLOR]+";"
            "color:"+cfgValue[CfgKey.TITLE_COLOR]+";"
            "font-size: "+cfgValue[CfgKey.TITLE_SIZE]+";"
            "font-family: "+cfgValue[CfgKey.TITLE_FONT]+", serif;")