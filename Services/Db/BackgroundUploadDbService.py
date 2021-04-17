import os
import sqlite3
import uuid

from Services.CfgService import CfgService
from Services.FileFolderService import FileFolderService
from config.Config import CfgKey


class BackgroundUploadDbService():

    def __init__(self):
        self.dbConnection = None

        dbPathWithName = FileFolderService.getAbsoltPath(self._getDBPath())

        FileFolderService.creatFolderByFileIfNotExist(dbPathWithName)

        self.TABLE_NAME = "BACKGROUND"
        self.TABLE_COLUMN_ID = "UUID"
        self.TABLE_COLUMN_CLEAN = "CLEAN_BEFORE"
        self.TABLE_COLUMN_TARGETPATH = "TARGET_PATH"

        self.dbConnection = sqlite3.connect(dbPathWithName)
        self._createTableIfNotExist()

    def _createTableIfNotExist(self):
        CREATE_TABLE = '''CREATE TABLE IF NOT EXISTS {} ({} TEXT PRIMARY KEY, {} INTEGER NOT NULL, {} TEXT NOT NULL);''' \
            .format(self.TABLE_NAME,self.TABLE_COLUMN_ID,self.TABLE_COLUMN_CLEAN,self.TABLE_COLUMN_TARGETPATH)
        self.dbConnection.execute(CREATE_TABLE)

    def setUploadAuthorization(self,cleanBefore:bool, targetPath:str):
        self.cleanTable()
        backgroundUUID  = str(uuid.uuid1())
        cleanBeforeAsInt = 0
        if cleanBefore:
            cleanBeforeAsInt = 1
        INSERT_VALUE = '''INSERT INTO {} ({},{},{}) VALUES ('{}',{},'{}');''' \
            .format(self.TABLE_NAME,self.TABLE_COLUMN_ID,self.TABLE_COLUMN_CLEAN,self.TABLE_COLUMN_TARGETPATH,backgroundUUID,cleanBeforeAsInt,targetPath)
        self.dbConnection.execute(INSERT_VALUE)
        self.dbConnection.commit()
        return backgroundUUID

    def getUploadAuthorization(self,uuid:str):
        SELECT = '''SELECT {},{} from {} WHERE {} = '{}';''' \
            .format(self.TABLE_COLUMN_CLEAN, self.TABLE_COLUMN_TARGETPATH, self.TABLE_NAME,self.TABLE_COLUMN_ID,uuid)
        cursor = self.dbConnection.execute(SELECT)
        result = []
        for row in cursor:
            cleanBefore = False
            if(int(row[0]) == 1):
                cleanBefore = True
            result.append({"cleanBefore":cleanBefore,"targetPath":str(row[1])})

        if len(result) > 0:
            return result[0]
        else:
            return None

    def cleanTable(self):
        DELETE_ALL = '''DELETE FROM {};''' \
            .format(self.TABLE_NAME,)
        self.dbConnection.execute(DELETE_ALL);
        self.dbConnection.commit()

    def printAllDEBUG(self):
        GET_ALL = '''SELECT {},  {}, {}, {} from {}'''.format(self.TABLE_COLUMN_ID,self.TABLE_COLUMN_CLEAN,self.TABLE_COLUMN_TARGETPATH,self.TABLE_NAME)
        cursor = self.dbConnection.execute(GET_ALL)
        for row in cursor:
            print("UUID= "+str(row[0])+" |CLEAN_BEFORE = "+str(row[1])+ " |TARGET_PATH = "+ str(row[2]))

    def close(self):
        self.dbConnection.close()

    def _getDBPath(self):
        return os.path.join(CfgService.get(CfgKey.MAIN_SAVE_DIR), CfgService.get(CfgKey.PROJECTNAME),CfgService.get(CfgKey.DB_NAME))