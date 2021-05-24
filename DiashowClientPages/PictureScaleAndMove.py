from PyQt5.QtCore import QSize, QPoint

from DiashowClientPages.PicturesConfig import PicturesConfig


class PictureScaleAndMove():

    def __init__(self,windowSize:QSize,pictureConfig:PicturesConfig):
        pictureSizeInPercent = pictureConfig.getInPercent(PicturesConfig.PICTURE_SIZE_PERCENT)
        if pictureSizeInPercent == None:
            self.size = windowSize
            self.move = QPoint(0,0)
        else:

            self.size = QSize(windowSize.width()*pictureSizeInPercent,windowSize.height()*pictureSizeInPercent)
            moveX = pictureConfig.getInPercent(PicturesConfig.PICTURE_MOVE_X_PERCENT)
            if moveX == None:
                moveX = 0
            moveY = pictureConfig.getInPercent(PicturesConfig.PICTURE_MOVE_Y_PERCENT)
            if moveY == None:
                moveY = 0
            pointX = int((-self.size.width()/2)+moveX*(1-pictureSizeInPercent)*windowSize.width())
            pointY = int((-self.size.height()/2)+moveY*(1-pictureSizeInPercent)*windowSize.height())
            self.move = QPoint(pointX,pointY)


    def getSize(self):
        return self.size
    def getMove(self):
        return self.move