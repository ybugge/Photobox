from Services.CfgService import CfgService
from Services.DbService import DbService
from Services.GlobalPagesVariableService import GlobalPagesVariableService
from Services.ShottedPictureService import ShottedPictureService
from config.Config import CfgKey


class PageDbSevice():

    @staticmethod
    def setInitialPicture(pageName:GlobalPagesVariableService):
        db = DbService(CfgService.get(CfgKey.APPLICATION_DB_PATH))
        db.setPicture(pageName.getPictureSubName(),ShottedPictureService.getTempPicturePath(),False)
        db.close()

    @staticmethod
    def updatePicture(pageName:GlobalPagesVariableService, path:str,isUsed:bool):
        db = DbService(CfgService.get(CfgKey.APPLICATION_DB_PATH))
        db.deletePictureByName(pageName.getPictureSubName())
        db.setPicture(pageName.getPictureSubName(),path, isUsed)
        db.close()


    @staticmethod
    def printAll():
        db = DbService(CfgService.get(CfgKey.APPLICATION_DB_PATH))
        db.printAllDEBUG()
        db.close()