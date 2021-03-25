import os

from Services.FileFolderService import FileFolderService
from config.Config import cfgValue, CfgKey


class PicturesConfig():

    DEFAULT = "default"
    FROM_SERVER = "from_server"
    FRAME_FRONT = "frame_front"
    PICTURE_SIZE_PERCENT = "picture_size_percent_xy"
    PICTURE_MOVE_X_PERCENT = "picture_move_percent_x"
    PICTURE_MOVE_Y_PERCENT = "picture_move_percent_y"

    def __init__(self, folderPath):
        configFilePath = os.path.join(folderPath,cfgValue[CfgKey.DIASHOW_CLIENT_PICTURE_CONFIG_FILE])
        self.config = {}
        if FileFolderService.existFile(configFilePath):
            fileLines = FileFolderService.readFile(configFilePath)
            self.config = {}
            for fileLine in fileLines:
                fileLineParts = fileLine.split("=",1)
                self.config[fileLineParts[0].replace('=', '').strip()] = fileLineParts[1].strip()

    def get(self,keyWord:str):
        if keyWord in self.config:
            return self.config[keyWord]
        return None

    def getAsInt(self,keyWord:str):
        valueAsString = self.get(keyWord)
        if valueAsString == None:
            return None
        try:
            return int(valueAsString)
        except ValueError:
            print ("Config ist kein Int!")
        return None


    def getInPercent(self,keyWord:str):
        valueAsInt = self.getAsInt(keyWord)
        if valueAsInt == None:
            return None
        elif valueAsInt > 100 and valueAsInt < 0:
            return None
        return float(valueAsInt) / 100


        return None

