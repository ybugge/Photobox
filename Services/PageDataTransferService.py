from config.Config import cfgValue, CfgKey


class PageDataTransferService():

    def __init__(self):
        self.currentFileName = ""

    def setFileName(self,fileName:str):
        self.currentFileName = fileName

    def getFilePath(self):
        return cfgValue[CfgKey.MAIN_SAVE_DIR] + "/" + self.currentFileName