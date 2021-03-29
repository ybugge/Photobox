import random

from Services.CfgService import CfgService
from Services.PictureDbService import PictureDbService
from config.Config import CfgKey


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
    def printAll():
        db = PictureDbService()
        db.printAllDEBUG()
        db.close()