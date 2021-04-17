from Services.Db.BackgroundUploadDbService import BackgroundUploadDbService
from Services.Db.PictureDbService import PictureDbService
from Services.GlobalPagesVariableService import GlobalPagesVariableService
from Services.ShottedPictureService import ShottedPictureService


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

    @staticmethod
    def setBackgroundUploadAuthorization(cleanBefore:bool, targetPath:str):
        db = BackgroundUploadDbService()
        uuid = db.setUploadAuthorization(cleanBefore,targetPath)
        db.close()
        return uuid

    @staticmethod
    def clearBackgroundUploadAuthorization():
        db = BackgroundUploadDbService()
        db.cleanTable()
        db.close()