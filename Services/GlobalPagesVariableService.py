from datetime import datetime


class GlobalPagesVariableService():

    def __init__(self):
        self.pictureSubName = None


    def updatePictureName(self):
        self.pictureSubName = datetime.now().strftime("%Y_%m_%d_%H_%M_%S_%f")

    def getPictureSubName(self):
        return self.pictureSubName