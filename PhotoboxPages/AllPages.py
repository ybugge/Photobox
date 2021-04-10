from PyQt5 import QtWidgets

from PhotoboxPages import Page


class AllPages():

    def __init__(self):
        self.stackedWidgets = QtWidgets.QStackedWidget()
        self.stackedWidgets.setContentsMargins(0, 0, 0, 0)
        self.pages = []

    def addPage(self, page : Page):
        self.pages.append(page)
        self.stackedWidgets.addWidget(page)

    def getStackedWidgets(self):
        return self.stackedWidgets

    def getCurrentPage(self):
        index = self.stackedWidgets.currentIndex()
        return self.pages[index]

    def showPage(self,type):
        foundedPage = self.getPageInstance(type)
        if foundedPage != None:
            foundedPage.executeBefore()
            index = self.getPages().index(foundedPage)
            self.setCurrentIndex(index)

    def getPageInstance(self,type):
        for page in self.getPages():
            if isinstance(page, type):
                return page
        print("Index wurde nicht gefunden!")
        return None

    def getPages(self):
        return self.pages

    def setCurrentIndex(self,index):
        self.stackedWidgets.setCurrentIndex(index)