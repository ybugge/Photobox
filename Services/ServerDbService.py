from Services.CfgService import CfgService
from Services.DbService import DbService
from config.Config import CfgKey


class ServerDbSevice():

    @staticmethod
    def printAll():
        db = DbService(CfgService.get(CfgKey.SERVER_DB_PATH))
        db.printAll()
        db.close()
