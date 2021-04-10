from datetime import datetime


class GlobalPagesVariableService():

    def __init__(self):
        self.isInUserMode = False
        self.lockPictureSubName = False
        self.pictureSubName = None
        self.used = False
        self.defaultBackgrounds = []
        self.backgroundIndex = 0


    def updatePictureName(self):
        if not self.lockPictureSubName:
            self.pictureSubName = datetime.now().strftime("%Y_%m_%d_%H_%M_%S_%f")
            self.used=False
            self.lockPictureSubName = True

    def setBackgroundIndex(self,index:int):
        self.backgroundIndex = index

    def getBackgroundIndex(self):
        return self.backgroundIndex

    def setUserMode(self,isInUserMode:bool):
        self.isInUserMode = isInUserMode

    def getUserMode(self):
        return self.isInUserMode

    def unlockPictureName(self):
        self.lockPictureSubName=False

    def getPictureSubName(self):
        return self.pictureSubName

    def setPictureUsed(self,used:bool):
        self.used = used

    def isPictureUsed(self):
        return self.used

    def setDefaultBackground(self,defaultBackgrounds:list):
        self.defaultBackgrounds = defaultBackgrounds

    def getDefaultBackground(self):
        return self.defaultBackgrounds