from PyQt5.QtCore import QPoint, QSize
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QLabel

from DiashowClientPages.Picture import Picture
from DiashowClientPages.PictureScaleAndMove import PictureScaleAndMove
from DiashowClientPages.Pictures import Pictures
from DiashowClientPages.PicturesConfig import PicturesConfig


class ShowRandomPicture():

    def __init__(self,windowSize:QSize,pictures:Pictures,frontPicture:QLabel,backgroundPicture:QLabel):
        self.windowSize = windowSize
        self.pictures = pictures
        self.frontPicture = frontPicture
        self.backgroundPicture = backgroundPicture

    def show(self):
        picture = self.pictures.getRandomPicture()
        if picture == None:
            return

        if picture.existFrame():
            self._showPictureWithFrame(picture)
        else:
            self._showPictureWithoutFrame(picture)

    def _showPictureWithoutFrame(self,picture:Picture):
        picturePixelMap = QPixmap(picture.getPath())
        self.frontPicture.move(0,0)
        self.backgroundPicture.move(0,0)
        self.frontPicture.setPixmap(picturePixelMap.scaled(self.windowSize.width(),self.windowSize.height()))#, Qt.KeepAspectRatio))
        self.backgroundPicture.setPixmap(picturePixelMap.scaled(self.windowSize.width()-1,self.windowSize.height()-1))#, Qt.KeepAspectRatio))

    def _showPictureWithFrame(self,picture:Picture):
        config = picture.getConfig()
        pictureScaleAndMove = PictureScaleAndMove(self.windowSize,config)
        if config.get(PicturesConfig.FRAME_FRONT) == "True":
            frontPicturePixelMap = QPixmap(picture.getFramePath())
            backPicturePixelMap = QPixmap(picture.getPath())
            frontMove = QPoint(0,0)
            frontSize = QSize(self.windowSize.width()-1,self.windowSize.height()-1)
            backMove = pictureScaleAndMove.getMove()
            backSize = pictureScaleAndMove.getSize()

        else:
            frontPicturePixelMap = QPixmap(picture.getPath())
            backPicturePixelMap = QPixmap(picture.getFramePath())
            backMove = QPoint(0,0)
            backSize = QSize(self.windowSize.width()-1,self.windowSize.height()-1)
            frontMove = pictureScaleAndMove.getMove()
            frontSize = pictureScaleAndMove.getSize()

        self.frontPicture.setPixmap(frontPicturePixelMap.scaled(frontSize)) #, Qt.KeepAspectRatio))
        self.backgroundPicture.setPixmap(backPicturePixelMap.scaled(backSize)) #, Qt.KeepAspectRatio))
        self.frontPicture.move(frontMove)
        self.backgroundPicture.move(backMove)
        print(backMove)