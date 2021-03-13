from Services.CfgService import CfgService
from Services.DbService import DbService
from Services.GlobalPagesVariableService import GlobalPagesVariableService
from Services.ShottedPictureService import ShottedPictureService
from config.Config import CfgKey


class PageDbSevice():

    @staticmethod
    def setInitialPicture(pageName:GlobalPagesVariableService):
        db = DbService(CfgService.get(CfgKey.APPLICATION_DB_PATH))
        db.setPicture(pageName.getPictureSubName(),ShottedPictureService.getTempPicturePath())
        db.close()

    @staticmethod
    def updatePicture(pageName:GlobalPagesVariableService, path:str):
        PageDbSevice._deletInitialPicture(pageName)
        PageDbSevice._setTargetPicture(pageName,path)

    @staticmethod
    def _deletInitialPicture(pageName:GlobalPagesVariableService):
        db = DbService(CfgService.get(CfgKey.APPLICATION_DB_PATH))
        db.deletePicture(pageName.getPictureSubName())
        db.close()

    @staticmethod
    def _setTargetPicture(pageName:GlobalPagesVariableService, path:str):
        db = DbService(CfgService.get(CfgKey.APPLICATION_DB_PATH))
        db.setPicture(pageName.getPictureSubName(),path)
        db.close()