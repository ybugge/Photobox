from PyQt5 import QtWidgets
from PyQt5 import QtCore
from PyQt5.QtCore import QSize

from Pages.AllPages import AllPages
from Pages.SinglePages.PageCameraCalibrationView import PageCameraCalibrationView
from Pages.SinglePages.PageCapturePhoto import PageCapturePhoto
from Pages.SinglePages.PageCloseConfirm import PageCloseConfirm
from Pages.SinglePages.PageConfig import PageConfig
from Pages.SinglePages.PageCameraPreview import PageCameraPreview
from Pages.SinglePages.PageDownloadPicture import PageDownloadPicture
from Pages.SinglePages.PageHints import PageHints
from Pages.SinglePages.PagePictureEdit import PagePictureEdit
from Pages.SinglePages.PageStartServer import PageStartServer
from Pages.SinglePages.PageSystemPictureManager import PageSystemPictureManager
from Pages.SinglePages.PageTitlePicture import PageTitlePicture
from Services.GlobalPagesVariableService import GlobalPagesVariableService
from Services.WebServerExecThread import WebServerExecThread
from config.Config import cfgValue, CfgKey


#Ist das Hauptfenster
class MainWindow(QtWidgets.QMainWindow):
    def __init__(self, windowsize:QSize):
        super().__init__()
        self.windowsize = windowsize
        self.globalVariable = GlobalPagesVariableService()
        self.server=WebServerExecThread()

        #Background-color on Pi not work: https://stackoverflow.com/questions/57637541/pyqt5-on-raspbian-background-color-of-qwidgets-is-not-displayed
        #https://raspberrypi.stackexchange.com/questions/93900/opengl-desktop-driver
        # " QPushButton { background-color: "+cfgValue[CfgKey.MAIN_WINDOW_BUTTON_BACKGROUND_COLOR]+";}" \
        mainStyle = "QWidget {background-color: "+cfgValue[CfgKey.MAIN_WINDOW_BACKGROUND_COLOR]+";" \
                            "color: "+cfgValue[CfgKey.TEXT_COLOR]+";" \
                            "font-family:"+cfgValue[CfgKey.MAIN_WINDOW_TEXT_FONT]+";}" \
                    " QPushButton {background-image: url('"+cfgValue[CfgKey.PAGE_TITLEPICTURE_BACKGROUND_IMAGE]+"');}"\
                    " QPushButton:disabled { color: "+cfgValue[CfgKey.BUTTON_DISABLED_TEXT_COLOR]+";}" \
                    " QProgressBar {text-align: center;}" \
                    " QProgressBar::chunk {" \
                            "background-color:"+cfgValue[CfgKey.PROGRESSBAR_CHUNK_BACKGROUND_COLOR]+";}" \
                    " QLineEdit {" \
                            "border: 1px solid "+cfgValue[CfgKey.MAIN_WINDOW_LABEL_EDIT_BORDER_COLOR]+";" \
                            "background-color: "+cfgValue[CfgKey.MAIN_WINDOW_LABEL_EDIT_BACKGROUND_COLOR]+";}"

        self.setStyleSheet(mainStyle)

        #Initialisieren
        self.pages = AllPages()
        #Verschiedene inhalten -> Stacked Widget
        self.setCentralWidget(self.pages.getStackedWidgets())


        #ClosePage
        pageCloseConfirm = PageCloseConfirm(self.pages,self.windowsize, self, self.server)
        pageCloseConfirm.setNextPage(PageConfig)
        self.pages.addPage(pageCloseConfirm)

        #Seite 1 Hinweise
        pageHints = PageHints(self.pages, self.windowsize)
        pageHints.setBackPage(PageSystemPictureManager)
        pageHints.setNextPage(PageConfig)
        self.pages.addPage(pageHints)

        #Seite 1-1 Picture Manager
        pagePictureManager = PageSystemPictureManager(self.pages, self.windowsize)
        pagePictureManager.setNextPage(PageHints)
        self.pages.addPage(pagePictureManager)

        #Seite 2 Configuration
        pageConfig = PageConfig(self.pages, self.windowsize)
        pageConfig.setBackPage(PageHints)
        pageConfig.setNextPage(PageStartServer)
        pageConfig.setCameraCalibrationEventPage(PageCameraCalibrationView)
        self.pages.addPage(pageConfig)

        #Seite 2-2 Camera configuration view
        pageCameraConfig = PageCameraCalibrationView(self.pages, self.windowsize)
        pageCameraConfig.setBackPage(PageConfig)
        self.pages.addPage(pageCameraConfig)

        # Intermediate page:  Start Server
        pageStartServer = PageStartServer(self.pages,self.windowsize,  self.server)
        pageStartServer.setNextPage(PageTitlePicture)
        self.pages.addPage(pageStartServer)

        #Seite 3 Title
        pageTitlePicture = PageTitlePicture(self.pages, self.windowsize)
        pageTitlePicture.setNextPage(PageCameraPreview)
        self.pages.addPage(pageTitlePicture)

        #Seite 4 Camera Preview
        pageCameraPreview = PageCameraPreview(self.pages,self.windowsize)
        pageCameraPreview.setNextPage(PageCapturePhoto)
        self.pages.addPage(pageCameraPreview)

        #Seite 5 Capture Photo
        pageCapturePhoto = PageCapturePhoto(self.pages, self.windowsize)
        pageCapturePhoto.setNextPage(PagePictureEdit)
        self.pages.addPage(pageCapturePhoto)

        #Seite 6 Picture Edit
        pagePictureEdit = PagePictureEdit(self.pages, self.windowsize, self.globalVariable)
        pagePictureEdit.activateAutoForward(PageTitlePicture,CfgKey.PAGE_PICTUREEDIT_SPACE_AUTO_FORWARD_WAIT_TIME)
        pagePictureEdit.setPrinterPage(PagePictureEdit) #Anpassen
        pagePictureEdit.setDownloadPage(PageDownloadPicture)
        pagePictureEdit.setNewPicturePage(PageCameraPreview)
        pagePictureEdit.setFinishedPage(PageTitlePicture)
        self.pages.addPage(pagePictureEdit)

        #Seite 6.1 Download Picture
        pageDownloadPicture = PageDownloadPicture(self.pages, self.windowsize,self.globalVariable)
        pageDownloadPicture.activateAutoForward(PageTitlePicture,CfgKey.PAGE_PICTUREEDIT_SPACE_AUTO_FORWARD_WAIT_TIME)
        pageDownloadPicture.setBackPage(PagePictureEdit)
        self.pages.addPage(pageDownloadPicture)

        #Set first visible Page
        self.pages.showPage(PageHints)

        #Fullscreen
        self.showFullScreen()

    def exitNotAllowedInThisPages(self):
        return [PageCameraPreview, PageCapturePhoto, PageSystemPictureManager]

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

    def __del__(self):
        if self.server != None:
            self.server.stop()