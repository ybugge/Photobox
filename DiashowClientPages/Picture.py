from DiashowClientPages.PicturesConfig import PicturesConfig


class Picture():

    def __init__(self,path:str,config:PicturesConfig):
        self.path = path
        self.config = config
        self.framePath = None

    def getPath(self) -> str:
        return self.path

    def setFramePath(self,framePath:str):
        self.framePath = framePath

    def existFrame(self):
        return self.framePath != None

    def getFramePath(self) -> str:
        return self.framePath

    def getConfig(self) -> PicturesConfig:
        return self.config

