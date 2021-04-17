import random

from Services.Db.BackgroundUploadDbService import BackgroundUploadDbService
from Services.Db.PictureDbService import PictureDbService


class ServerDbSevice():

    @staticmethod
    def getPictureNames():
        db = PictureDbService()
        result = db.getPictureNames()
        db.close()
        return result

    @staticmethod
    def getPictureUrlIds(name:str):
        db = PictureDbService()
        result = db.getPictureUrlIds(name)
        db.close()
        return result

    @staticmethod
    def getPicturePathAndName(urlId:str):
        db = PictureDbService()
        result = db.getPicturePath(urlId)
        db.close()
        return result

    @staticmethod
    def getRendomPictureUrlIds(number:int):
        db = PictureDbService()
        result = db.getUsedPictureUrlIdsUnsecure()
        db.close()
        if len(result) > number:
            return random.sample(result,number)
        else:
            return result

    @staticmethod
    def getNumberUsedPictures():
        db = PictureDbService()
        result = db.getNumberUsedPicture()
        db.close()
        return result

    @staticmethod
    def getBackgroundUploadAuthorization(uuid:str):
        db = BackgroundUploadDbService()
        result = db.getUploadAuthorization(uuid)
        db.close()
        return result

    @staticmethod
    def printAll():
        db = PictureDbService()
        db.printAllDEBUG()
        db.close()