from Services.CfgService import CfgService
from Services.PictureDbService import PictureDbService
from Services.GlobalPagesVariableService import GlobalPagesVariableService
from Services.ShottedPictureService import ShottedPictureService
from config.Config import CfgKey


class PageDbSevice():

    @staticmethod
    def setInitialPicture(pageName:GlobalPagesVariableService):
        db = PictureDbService()
        db.setPicture(pageName.getPictureSubName(),ShottedPictureService.getTempPicturePath(),False)
        db.close()

    @staticmethod
    def updatePicture(pageName:GlobalPagesVariableService, path:str,isUsed:bool):
        db = PictureDbService()
        db.deletePictureByName(pageName.getPictureSubName())
        db.setPicture(pageName.getPictureSubName(),path, isUsed)
        db.close()


    @staticmethod
    def printAll():
        db = PictureDbService()
        db.printAllDEBUG()
        db.close()