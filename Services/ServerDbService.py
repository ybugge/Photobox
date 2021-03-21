import random

from Services.CfgService import CfgService
from Services.DbService import DbService
from config.Config import CfgKey


class ServerDbSevice():

    @staticmethod
    def getPictureNames():
        db = DbService()
        result = db.getPictureNames()
        db.close()
        return result

    @staticmethod
    def getPictureUrlIds(name:str):
        db = DbService()
        result = db.getPictureUrlIds(name)
        db.close()
        return result

    @staticmethod
    def getPicturePathAndName(urlId:str):
        db = DbService()
        result = db.getPicturePath(urlId)
        db.close()
        return result

    @staticmethod
    def getRendomPictureUrlIds(number:int):
        db = DbService()
        result = db.getUsedPictureUrlIdsUnsecure()
        db.close()
        if len(result) > number:
            return random.sample(result,number)
        else:
            return result

    @staticmethod
    def getNumberUsedPictures():
        db = DbService()
        result = db.getNumberUsedPicture()
        db.close()
        return result

    @staticmethod
    def printAll():
        db = DbService()
        db.printAllDEBUG()
        db.close()