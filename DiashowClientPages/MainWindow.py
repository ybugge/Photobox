from PyQt5 import QtWidgets
from PyQt5 import QtCore
from PyQt5.QtCore import QSize, QTimer, Qt
from PyQt5.QtWidgets import QLabel, QWidget


#Ist das Hauptfenster
from DiashowClientPages.PictureLoader import PictureLoader
from DiashowClientPages.Pictures import Pictures
from DiashowClientPages.ShowRandomPicture import ShowRandomPicture
from config.Config import cfgValue, CfgKey


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self, windowSize:QSize):
        super().__init__()
        self.setContentsMargins(0,0,0,0)
        #Fullscreen
        self.showFullScreen()
        self.windowSize = windowSize
        self.pictures = Pictures()
        self.showNewPictureTimer = QTimer()
        self.updatePictureSourcesTimer = QTimer()
        self.setStyleSheet("background-color:black;")

        pictureWidget = QWidget()
        self.setCentralWidget(pictureWidget)

        self.backgroundPicture = QLabel(pictureWidget)
        self.backgroundPicture.setContentsMargins(0, 0, 0, 0)
        self.backgroundPicture.setAlignment(Qt.AlignCenter)
        self.backgroundPicture.setStyleSheet("background-color:transparent;")

        self.frontPicture = QLabel(pictureWidget)
        self.frontPicture.setContentsMargins(0, 0, 0, 0)
        self.frontPicture.setAlignment(Qt.AlignCenter)
        self.frontPicture.setStyleSheet("background-color:transparent;")

        self.loadPictureSources()
        if self.pictures.existPictures():
            self.showRandomPicture()

        self.showNewPictureTimer.timeout.connect(self.showRandomPicture)
        self.showNewPictureTimer.start(cfgValue[CfgKey.DIASHOW_CLIENT_PICTURE_SHOW_NEW_PICTURE_INTERVAL])

        self.updatePictureSourcesTimer.timeout.connect(self.updatePictureSources)
        self.updatePictureSourcesTimer.start(cfgValue[CfgKey.DIASHOW_CLIENT_PICTURE_UPDATE_PICTURE_SOURCE_INTERVAL_INITIAL])

    def showRandomPicture(self):
        showRandomPicture = ShowRandomPicture(self.windowSize,self.pictures,self.frontPicture,self.backgroundPicture)
        showRandomPicture.show()

    def loadPictureSources(self):
        loader = PictureLoader(True)
        loader.update()
        self.pictures = loader.getPictures()

    def updatePictureSources(self):
        self.showNewPictureTimer.stop()
        self.updatePictureSourcesTimer.stop()
        loader = PictureLoader(False)
        loader.update()
        self.pictures = loader.getPictures()
        self.showNewPictureTimer.start(cfgValue[CfgKey.DIASHOW_CLIENT_PICTURE_SHOW_NEW_PICTURE_INTERVAL])
        self.updatePictureSourcesTimer.start(cfgValue[CfgKey.DIASHOW_CLIENT_PICTURE_UPDATE_PICTURE_SOURCE_INTERVAL])


    def exit(self):
        print("Keine Bilder gefunden. Bitte legen Sie folgende Ordner an: '"+cfgValue[CfgKey.DIASHOW_CLIENT_PICTURE_MAIN_FOLDER]+"' > 'default' > 'pictures'. In 'pictures' muss ein Bild hinterlegt werden!")
        self.showNewPictureTimer.stop()
        self.close()

    def signal_accept(self, msg):
        pass

    #Alle Keyevents
    def keyPressEvent(self, event):
        # close the window
        if event.key() == QtCore.Qt.Key_Escape:
            self.close()
        event.accept()

    #Schliest die Anwendung
    def close(self):
        self.deleteLater()
