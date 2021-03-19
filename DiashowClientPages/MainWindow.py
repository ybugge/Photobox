from PyQt5 import QtWidgets
from PyQt5 import QtCore
from PyQt5.QtCore import QSize

from DiashowClientPages.SinglePage.PageDiashow import PageDiashow
from PhotoboxPages.AllPages import AllPages


#Ist das Hauptfenster
class MainWindow(QtWidgets.QMainWindow):
    def __init__(self, windowsize:QSize):
        super().__init__()
        self.windowsize = windowsize

        self.setStyleSheet('background-color: black;')

        #Initialisieren
        self.pages = AllPages()
        #Verschiedene inhalten -> Stacked Widget
        self.setCentralWidget(self.pages.getStackedWidgets())

        #Page 1 Diashow
        pageDiashow = PageDiashow(self.pages,self.windowsize,self)
        self.pages.addPage(pageDiashow)


        #Set first visible Page
        self.pages.showPage(PageDiashow)

        #Fullscreen
        self.showFullScreen()

    #Alle Keyevents
    def keyPressEvent(self, event):
        # close the window
        if event.key() == QtCore.Qt.Key_Escape:
            self.close()
        event.accept()

    #Schliest die Anwendung
    def close(self):
        self.deleteLater()