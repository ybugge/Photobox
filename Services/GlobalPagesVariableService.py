from datetime import datetime


class GlobalPagesVariableService():

    def __init__(self):
        self.lockPictureSubName = False
        self.pictureSubName = None


    def updatePictureName(self):
        if not self.lockPictureSubName:
            self.pictureSubName = datetime.now().strftime("%Y_%m_%d_%H_%M_%S_%f")
            self.lockPictureSubName = True

    def unlockPictureName(self):
        self.lockPictureSubName=False

    def getPictureSubName(self):
        return self.pictureSubName