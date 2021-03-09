from PyQt5 import QtWidgets
from PyQt5 import QtCore
from PyQt5.QtCore import QSize

from Pages.AllPages import AllPages
from Pages.PageCapturePhoto import PageCapturePhoto
from Pages.PageCloseConfirm import PageCloseConfirm
from Pages.PageConfig import PageConfig
from Pages.PageCameraPreview import PageCameraPreview
from Pages.PageHints import PageHints
from Pages.PageTitlePicture import PageTitlePicture
from Pages.PageTest import PageTest
from Pages.PageTest2 import PageTest2
from Services.FileNameService import FileNameService
from config.Config import cfgValue, CfgKey, textValue, TextKey

#Ist das Hauptfenster
class MainWindow(QtWidgets.QMainWindow):
    def __init__(self, windowsize:QSize):
        super().__init__()
        self.windowsize = windowsize
        self.fileNameService = FileNameService()

        #Sytling
        self.setStyleSheet("QWidget {background-color: "+cfgValue[CfgKey.MAIN_WINDOW_BACKGROUND_COLOR]+";"
                                "color: "+cfgValue[CfgKey.TEXT_COLOR]+";"
                                "font-size: "+cfgValue[CfgKey.MAIN_WINDOW_TEXT_SIZE]+";"
                                "font-family:"+cfgValue[CfgKey.MAIN_WINDOW_TEXT_FONT]+"}"
                           "QPushButton {"
                                "background-color: "+cfgValue[CfgKey.MAIN_WINDOW_BUTTON_BACKGROUND_COLOR]+";"
                                "height: "+cfgValue[CfgKey.MAIN_WINDOW_BUTTON_HEIGHT]+";}")

        #Initialisieren
        self.pages = AllPages()
        #Verschiedene inhalten -> Stacked Widget
        self.setCentralWidget(self.pages.getStackedWidgets())


        #ClosePage
        pageCloseConfirm = PageCloseConfirm(self.pages, self)
        pageCloseConfirm.setNextPage(PageConfig)
        self.pages.addPage(pageCloseConfirm)

        #Seite 1 Hinweise
        pageHints = PageHints(self.pages)
        pageHints.setNextPage(PageConfig)
        self.pages.addPage(pageHints)

        #Seite 2 Configuration
        pageConfig = PageConfig(self.pages)
        pageConfig.setBackPage(PageHints)
        pageConfig.setNextPage(PageTitlePicture)
        self.pages.addPage(pageConfig)

        #Seite 3 Title
        pageTitlePicture = PageTitlePicture(self.pages)
        pageTitlePicture.setNextPage(PageCameraPreview)
        self.pages.addPage(pageTitlePicture)

        #Seite 4 Camera Preview
        pageCameraPreview = PageCameraPreview(self.pages,self.windowsize)
        pageCameraPreview.setNextPage(PageCapturePhoto)
        self.pages.addPage(pageCameraPreview)

        #Seite 5 Capture Photo
        pageCapturePhoto = PageCapturePhoto(self.pages, self.windowsize, self.fileNameService)
        pageCapturePhoto.setNextPage(PageTest)
        self.pages.addPage(pageCapturePhoto)

        #TestSeite 1
        pageTest = PageTest(self.pages,self.fileNameService)
        pageTest.setNextPage(PageTest2)
        self.pages.addPage(pageTest)

        #TestseiteSeite2
        pageTest2 = PageTest2(self.pages)
        pageTest2.setNextPage(PageTest)
        self.pages.addPage(pageTest2)

        #Set first visible Page
        self.pages.showPage(PageHints)

        #Fullscreen
        self.showFullScreen()

    def exitNotAllowedInThisPages(self):
        return [PageCameraPreview, PageCapturePhoto]

    #Alle Keyevents
    def keyPressEvent(self, event):
        # close the window
        if event.key() == QtCore.Qt.Key_Escape:
            currentPage = self.pages.getCurrentPage()
            if currentPage.__class__ in self.exitNotAllowedInThisPages():
                print("Auf dieser Seite kann das Programm nicht geschlossen werden!")
                return
            pageCloseConfirmInstance = self.pages.getPageInstance(PageCloseConfirm)
            pageCloseConfirmInstance.setNextPage(currentPage.__class__)
            self.pages.showPage(PageCloseConfirm)
        event.accept()

    #Schliest die Anwendung
    def close(self):
        self.deleteLater()