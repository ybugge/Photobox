from PyQt5 import QtWidgets
from PyQt5 import QtCore
from PyQt5.QtCore import QSize

from PhotoboxPages.AllPages import AllPages
from PhotoboxPages.SinglePages.PageCameraCalibrationView import PageCameraCalibrationView
from PhotoboxPages.SinglePages.PageCapturePhoto import PageCapturePhoto
from PhotoboxPages.SinglePages.PageCloseConfirm import PageCloseConfirm
from PhotoboxPages.SinglePages.PageConfig import PageConfig
from PhotoboxPages.SinglePages.PageConnectWithWifi import PageConnectWithWifi
from PhotoboxPages.SinglePages.PageCountdown import PageCameraPreview
from PhotoboxPages.SinglePages.PageDownloadPicture import PageDownloadPicture
from PhotoboxPages.SinglePages.PageGreenscreenColorPicker import PageGreenscreenColorPicker
from PhotoboxPages.SinglePages.PageGreenscreenConnectWithWifiCustomBackground import \
    PageGreenscreenConnectWithWifiCustomBackground
from PhotoboxPages.SinglePages.PageGreenscreenConnectWithWifiDefaultBackground import \
    PageGreenscreenConnectWithWifiDefaultBackground
from PhotoboxPages.SinglePages.PageGreenscreenSelectBackround import PageGreenscreenSelectBackround
from PhotoboxPages.SinglePages.PageGreenscreenToleranceConfig import PageGreenscreenToleranceConfig
from PhotoboxPages.SinglePages.PageGreenscreenUploadCustomBackground import PageGreenscreenUploadCustomBackground
from PhotoboxPages.SinglePages.PageGreenscreenUploadDefaultBackground import PageGreenscreenUploadDefaultBackground
from PhotoboxPages.SinglePages.PageHelp import PageHelp
from PhotoboxPages.SinglePages.PageHints import PageHints
from PhotoboxPages.SinglePages.PageMovePictureFromTemp_RedirectOne import PageMovePictureFromTemp_RedirectOne
from PhotoboxPages.SinglePages.PageMovePictureFromTemp_RedirectTwo import PageMovePictureFromTemp_RedirectTwo
from PhotoboxPages.SinglePages.PagePictureEdit import PagePictureEdit
from PhotoboxPages.SinglePages.PagePrint import PagePrint
from PhotoboxPages.SinglePages.PageReconfig import PageReconfig
from PhotoboxPages.SinglePages.PageStartServer import PageStartServer
from PhotoboxPages.SinglePages.PageSystemPictureManager import PageSystemPictureManager
from PhotoboxPages.SinglePages.PageTitlePicture import PageTitlePicture
from Services.GlobalPagesVariableService import GlobalPagesVariableService
from Services.PrinterService import PrinterService
from Services.WebServerExecThread import WebServerExecThread
from config.Config import cfgValue, CfgKey


#Ist das Hauptfenster

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self, windowsize:QSize):
        super().__init__()
        self.windowsize = windowsize
        self.globalVariable = GlobalPagesVariableService(self.windowsize)
        self.server=WebServerExecThread()
        self.printerService = PrinterService()

        #Background-color on Pi not work: https://stackoverflow.com/questions/57637541/pyqt5-on-raspbian-background-color-of-qwidgets-is-not-displayed
        #https://raspberrypi.stackexchange.com/questions/93900/opengl-desktop-driver
        # " QPushButton { background-color: "+cfgValue[CfgKey.MAIN_WINDOW_BUTTON_BACKGROUND_COLOR]+";}"
        #" QPushButton {background-image: url('"+cfgValue[CfgKey.PAGE_TITLEPICTURE_BACKGROUND_IMAGE]+"');}"
        #" QPushButton:disabled { color: "+cfgValue[CfgKey.BUTTON_DISABLED_TEXT_COLOR]+";}"
        mainStyle = "QWidget {background-color: "+cfgValue[CfgKey.MAIN_WINDOW_BACKGROUND_COLOR]+";" \
                            "color: "+cfgValue[CfgKey.TEXT_COLOR]+";" \
                            "font-family:"+cfgValue[CfgKey.MAIN_WINDOW_TEXT_FONT]+";}" \
                    " QPushButton { background-color:white; color: black;}"\
                    " QPushButton:disabled { color: grey;}"\
                    " QProgressBar {text-align: center;}" \
                    " QProgressBar::chunk {" \
                            "background-color:"+cfgValue[CfgKey.PROGRESSBAR_CHUNK_BACKGROUND_COLOR]+";}" \
                    " QLineEdit {" \
                            "border: 1px solid "+cfgValue[CfgKey.MAIN_WINDOW_LABEL_EDIT_BORDER_COLOR]+";" \
                            "background-color: "+cfgValue[CfgKey.MAIN_WINDOW_LABEL_EDIT_BACKGROUND_COLOR]+";}"\
                    " QLineEdit:disabled { color:grey;}"\
                    " QLabel:disabled {color:grey;}"

        self.setStyleSheet(mainStyle)

        #Initialisieren
        self.pages = AllPages()
        #Verschiedene inhalten -> Stacked Widget
        self.setCentralWidget(self.pages.getStackedWidgets())

        #ClosePage
        pageCloseConfirm = PageCloseConfirm(self.pages,self.windowsize, self, self.server)
        pageCloseConfirm.setNextPage(PageConfig)
        self.pages.addPage(pageCloseConfirm)

        #Reconfigure
        pageReconfig = PageReconfig(self.pages,self.windowsize, self.printerService,self.globalVariable)
        pageReconfig.setBackPage(PageTitlePicture)
        pageReconfig.setGreenscreenColorPickerEventPage(PageGreenscreenColorPicker)
        pageReconfig.setUploadDefaultBackgroundEventPage(PageGreenscreenUploadDefaultBackground)
        pageReconfig.setCameraCalibrationEventPage(PageCameraCalibrationView)
        self.pages.addPage(pageReconfig)

        #Reconfig: Greenscreen Upload Default Background
        pageGreenscreenUploadDefaultBackground = PageGreenscreenUploadDefaultBackground(self.pages, self.windowsize, self.globalVariable)
        pageGreenscreenUploadDefaultBackground.setBackPage(PageReconfig)
        pageGreenscreenUploadDefaultBackground.setNextPage(PageGreenscreenConnectWithWifiDefaultBackground)
        pageGreenscreenUploadDefaultBackground.disabledAfter(PageGreenscreenConnectWithWifiDefaultBackground)
        self.pages.addPage(pageGreenscreenUploadDefaultBackground)

        #Reconfig.1: Greenscreen Connect wifi
        pageGreenscreenConnectWithWifiDefaultBackground = PageGreenscreenConnectWithWifiDefaultBackground(self.pages, self.windowsize, self.globalVariable)
        pageGreenscreenConnectWithWifiDefaultBackground.setBackPage(PageGreenscreenUploadDefaultBackground)
        pageGreenscreenConnectWithWifiDefaultBackground.disabledBefore(PageGreenscreenUploadDefaultBackground)
        self.pages.addPage(pageGreenscreenConnectWithWifiDefaultBackground)

        #Seite 1 Hinweise
        pageHints = PageHints(self.pages, self.windowsize, self.printerService)
        pageHints.setBackPage(PageSystemPictureManager)
        pageHints.setNextPage(PageConfig)
        self.pages.addPage(pageHints)

        #Seite 1-1 Picture Manager
        pagePictureManager = PageSystemPictureManager(self.pages, self.windowsize)
        pagePictureManager.setNextPage(PageHints)
        self.pages.addPage(pagePictureManager)

        #Seite 2 Configuration
        pageConfig = PageConfig(self.pages, self.windowsize, self.printerService)
        pageConfig.setBackPage(PageHints)
        pageConfig.setNextPage(PageStartServer)
        pageConfig.setCameraCalibrationEventPage(PageCameraCalibrationView)
        pageConfig.setGreenscreenColorPickerEventPage(PageGreenscreenColorPicker)
        self.pages.addPage(pageConfig)

        #Seite 2-2 Camera configuration view
        pageCameraConfig = PageCameraCalibrationView(self.pages, self.windowsize,self.globalVariable)
        pageCameraConfig.setBackPage(PageConfig)
        pageCameraConfig.setBackPageIsInUserMode(PageReconfig)
        self.pages.addPage(pageCameraConfig)

        #Seite 2-3 Greenscreen Read Collor
        pageGreenscreenColorPicker = PageGreenscreenColorPicker(self.pages, self.windowsize, self.globalVariable)
        pageGreenscreenColorPicker.setBackPage(PageConfig)
        pageGreenscreenColorPicker.setBackPageIsInUserMode(PageReconfig)
        pageGreenscreenColorPicker.setTolerancePage(PageGreenscreenToleranceConfig)
        self.pages.addPage(pageGreenscreenColorPicker)

        #Seite 2-4 PageGreenscreenToleranceConfig
        pageGreenscreenToleranceConfig = PageGreenscreenToleranceConfig(self.pages, self.windowsize,self.globalVariable)
        pageGreenscreenToleranceConfig.setBackPage(PageGreenscreenColorPicker)
        self.pages.addPage(pageGreenscreenToleranceConfig)

        # Intermediate page:  Start Server
        pageStartServer = PageStartServer(self.pages,self.windowsize, self.server, self.globalVariable)
        pageStartServer.setNextPage(PageTitlePicture)
        self.pages.addPage(pageStartServer)

        #Seite 3 Title
        pageTitlePicture = PageTitlePicture(self.pages, self.windowsize)
        pageTitlePicture.setNextPage(PageGreenscreenSelectBackround)
        self.pages.addPage(pageTitlePicture)

        #Seite Opt 3.1 Greenscreen Background
        pageGreenscreenSelectBackround = PageGreenscreenSelectBackround(self.pages, self.windowsize,self.globalVariable)
        pageGreenscreenSelectBackround.setNextPage(PageCameraPreview)
        pageGreenscreenSelectBackround.setBackPage(PageTitlePicture)
        pageGreenscreenSelectBackround.setOwnBackgroundPage(PageGreenscreenUploadCustomBackground)
        self.pages.addPage(pageGreenscreenSelectBackround)

        #Seite Opt 3.2 Greenscreen Upload Background
        pageGreenscreenUploadCustomBackground = PageGreenscreenUploadCustomBackground(self.pages, self.windowsize, self.globalVariable)
        pageGreenscreenUploadCustomBackground.setBackPage(PageGreenscreenSelectBackround)
        pageGreenscreenUploadCustomBackground.setNextPage(PageGreenscreenConnectWithWifiCustomBackground)
        pageGreenscreenUploadCustomBackground.disabledAfter(PageGreenscreenConnectWithWifiCustomBackground)
        self.pages.addPage(pageGreenscreenUploadCustomBackground)

        #Seite Opt 3.3 Greenscreen Wifi Connect
        pageGreenscreenConnectWithWifiCustomBackground = PageGreenscreenConnectWithWifiCustomBackground(self.pages, self.windowsize, self.globalVariable)
        pageGreenscreenConnectWithWifiCustomBackground.setBackPage(PageGreenscreenUploadCustomBackground)
        pageGreenscreenConnectWithWifiCustomBackground.disabledBefore(PageGreenscreenUploadCustomBackground)
        self.pages.addPage(pageGreenscreenConnectWithWifiCustomBackground)

        #Seite 4 Camera Preview
        pageCameraPreview = PageCameraPreview(self.pages,self.windowsize, self.globalVariable)
        pageCameraPreview.setNextPage(PageCapturePhoto)
        self.pages.addPage(pageCameraPreview)

        #Seite 5 Capture Photo
        pageCapturePhoto = PageCapturePhoto(self.pages, self.windowsize,self.globalVariable)
        pageCapturePhoto.setNextPage(PagePictureEdit)
        self.pages.addPage(pageCapturePhoto)

        #Seite 6 Picture Edit
        pagePictureEdit = PagePictureEdit(self.pages, self.windowsize)
        pagePictureEdit.activateAutoForward(PageMovePictureFromTemp_RedirectOne, CfgKey.PAGE_PICTUREEDIT_SPACE_AUTO_FORWARD_WAIT_TIME)
        pagePictureEdit.setPrinterPage(PagePrint)
        pagePictureEdit.setDownloadPage(PageDownloadPicture)
        pagePictureEdit.setHelpPage(PageHelp)
        pagePictureEdit.setNewPicturePage(PageMovePictureFromTemp_RedirectTwo)
        pagePictureEdit.setFinishedPage(PageMovePictureFromTemp_RedirectOne)
        self.pages.addPage(pagePictureEdit)

        #Seite 6.1 Download Picture
        pageDownloadPicture = PageDownloadPicture(self.pages, self.windowsize,self.globalVariable)
        pageDownloadPicture.activateAutoForward(PageMovePictureFromTemp_RedirectOne, CfgKey.PAGE_PICTUREEDIT_SPACE_AUTO_FORWARD_WAIT_TIME)
        pageDownloadPicture.setBackPage(PagePictureEdit)
        pageDownloadPicture.setNextPage(PageConnectWithWifi)
        pageDownloadPicture.disabledAfter(PageConnectWithWifi)
        self.pages.addPage(pageDownloadPicture)

        #Seite 6.1.2 Connect with Wifi
        pageConnectWithWifi = PageConnectWithWifi(self.pages, self.windowsize,self.globalVariable)
        pageConnectWithWifi.activateAutoForward(PageMovePictureFromTemp_RedirectOne, CfgKey.PAGE_PICTUREEDIT_SPACE_AUTO_FORWARD_WAIT_TIME)
        pageConnectWithWifi.setBackPage(PageDownloadPicture)
        pageConnectWithWifi.disabledBefore(PageDownloadPicture)
        self.pages.addPage(pageConnectWithWifi)

        #Seite 6.2 Print
        pagePrint = PagePrint(self.pages, self.windowsize,self.globalVariable, self.printerService)
        pagePrint.activateAutoForward(PageMovePictureFromTemp_RedirectOne, CfgKey.PAGE_PICTUREEDIT_SPACE_AUTO_FORWARD_WAIT_TIME)
        pagePrint.setBackPage(PagePictureEdit)
        self.pages.addPage(pagePrint)

        #Seite 6.3
        pageHelp = PageHelp(self.pages, self.windowsize)
        pageHelp.setBackPage(PagePictureEdit)
        self.pages.addPage(pageHelp)

        #Intermediate Page: Move Picture from raw to used or unused folder
        pageMovePictureFromTemp_RedirectOne = PageMovePictureFromTemp_RedirectOne(self.pages, self.windowsize, self.globalVariable)
        pageMovePictureFromTemp_RedirectOne.setNextPage(PageTitlePicture)
        self.pages.addPage(pageMovePictureFromTemp_RedirectOne)

        pageMovePictureFromTemp_RedirectTwo =  PageMovePictureFromTemp_RedirectTwo(self.pages, self.windowsize, self.globalVariable)
        pageMovePictureFromTemp_RedirectTwo.setNextPage(PageCameraPreview)
        self.pages.addPage(pageMovePictureFromTemp_RedirectTwo)

        #Set first visible Page
        self.pages.showPage(PageHints)

        #Fullscreen
        self.showFullScreen()

    def exitNotAllowedInThisPages(self):
        return [PageCameraPreview, PageCapturePhoto, PageSystemPictureManager,PageCloseConfirm,PageGreenscreenToleranceConfig,PageGreenscreenColorPicker,PageCameraCalibrationView]

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
        elif event.key() == QtCore.Qt.Key_1:
            currentPage = self.pages.getCurrentPage()
            if currentPage.__class__ == PageTitlePicture:
                self.pages.showPage(PageReconfig)

        event.accept()

    #Schliest die Anwendung
    def close(self):
        self.deleteLater()

    def __del__(self):
        if self.server != None:
            self.server.stop()