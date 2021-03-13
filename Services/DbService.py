import sqlite3

from Services.CfgService import CfgService
from Services.FileFolderService import FileFolderService
from config.Config import CfgKey


class DbService():

    def __init__(self, dbPath:str):
        self.dbConnection = None
        if dbPath and not dbPath.isspace():
            dbPathWithName = FileFolderService.getAbsoltPath(dbPath+"/"+CfgService.get(CfgKey.DB_NAME))
        else:
            dbPathWithName = FileFolderService.getAbsoltPath(CfgService.get(CfgKey.DB_NAME))

        FileFolderService.creatFolderByFileIfNotExist(dbPathWithName)

        TABLE_NAME = "PICTURE"
        TABLE_COLUMN_ID = "ID"
        TABLE_COLUMN_NAME = "NAME"
        TABLE_COLUMN_PATH = "PATH"
        self.CREATE_TABLE = '''CREATE TABLE IF NOT EXISTS {} \
         ({} INTEGER PRIMARY KEY AUTOINCREMENT, \
         {} TEXT NOT NULL,   \
         {} TEXT NOT NULL);'''.format(TABLE_NAME,TABLE_COLUMN_ID,TABLE_COLUMN_NAME,TABLE_COLUMN_PATH)
        self.INSERT_VALUE = '''INSERT INTO {} ({},{}) VALUES'''.format(TABLE_NAME,TABLE_COLUMN_NAME,TABLE_COLUMN_PATH)
        self.GET_ALL = '''SELECT {}, {} from {}'''.format(TABLE_COLUMN_NAME,TABLE_COLUMN_PATH,TABLE_NAME)
        self.DELETE_ALL_FROM_NAME = '''DELETE FROM {} WHERE {} ='''.format(TABLE_NAME,TABLE_COLUMN_NAME)
        self.GET_ALL_PATHS_FROM_PICTURE = '''SELECT {} FROM {} WHERE {} ='''.format(TABLE_COLUMN_PATH,TABLE_NAME,TABLE_COLUMN_NAME)

        self.dbConnection = sqlite3.connect(dbPathWithName)
        self._createTableIfNotExist()

    def _createTableIfNotExist(self):
        self.dbConnection.execute(self.CREATE_TABLE)

    def setPicture(self,pictureName:str, picturePATH:str):
        value = "('{}','{}')".format(pictureName,picturePATH)
        self.dbConnection.execute(self.INSERT_VALUE+value);
        self.dbConnection.commit()

    def deletePicture(self,pictureName:str):
        self.dbConnection.execute(self.DELETE_ALL_FROM_NAME+"'"+pictureName+"';");
        self.dbConnection.commit()

    def getAllPaths(self,pictureName):
        cursor = self.dbConnection.execute(self.GET_ALL_PATHS_FROM_PICTURE+"'"+pictureName+"';")
        result = []
        for row in cursor:
            result.append(row[0])
        return list(set(result))

    def printAll(self):
        cursor = self.dbConnection.execute(self.GET_ALL)
        for row in cursor:
            print("NAME = "+str(row[0])+ " PATH = "+ str(row[1]))

    def close(self):
        self.dbConnection.close()

