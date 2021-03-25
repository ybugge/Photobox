from PyQt5.QtCore import QSize, QPoint

from DiashowClientPages.PicturesConfig import PicturesConfig


class PictureScaleAndMove():

    def __init__(self,windowSize:QSize,configPath:str):
        pictureConfig = PicturesConfig(configPath)
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
            self.move = QPoint(moveX*(1-pictureSizeInPercent)*windowSize.width(),moveY*(1-pictureSizeInPercent)*windowSize.height())


    def getSize(self):
        return self.size
    def getMove(self):
        return self.move