from datetime import datetime


class GlobalPagesVariableService():

    def __init__(self):
        self.lockPictureSubName = False
        self.pictureSubName = None
        self.used = False


    def updatePictureName(self):
        if not self.lockPictureSubName:
            self.pictureSubName = datetime.now().strftime("%Y_%m_%d_%H_%M_%S_%f")
            self.used=False
            self.lockPictureSubName = True


    def unlockPictureName(self):
        self.lockPictureSubName=False

    def getPictureSubName(self):
        return self.pictureSubName

    def setPictureUsed(self,used:bool):
        self.used = used
    def isPictureUsed(self):
        return self.used