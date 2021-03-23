import os

from Services.FileFolderService import FileFolderService
from config.Config import cfgValue, CfgKey


class PicturesConfig():

    DEFAULT = "default"
    FROM_SERVER = "from_server"
    FRAME_FRONT = "frame_front"

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

