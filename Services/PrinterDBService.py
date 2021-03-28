import os
import sqlite3

from Services.CfgService import CfgService
from Services.FileFolderService import FileFolderService
from config.Config import CfgKey


class PrinterDBService():

    def __init__(self):
        self.dbConnection = None

        dbPathWithName = FileFolderService.getAbsoltPath(self._getDBPath())
        FileFolderService.creatFolderByFileIfNotExist(dbPathWithName)

        self.TABLE_NAME = "PRINT"
        self.TABLE_COLUMN_ID = "ID"
        self.TABLE_COLUMN_PICTURE_NAME = "PICTURE_NAME"
        self.TABLE_COLUMN_JOBID = "JOB_ID"

        self.dbConnection = sqlite3.connect(dbPathWithName)
        self._createTableIfNotExist()

    def _createTableIfNotExist(self):
        CREATE_TABLE = '''CREATE TABLE IF NOT EXISTS {} ({} INTEGER PRIMARY KEY AUTOINCREMENT, {} TEXT NOT NULL, {} INTEGER NOT NULL);''' \
            .format(self.TABLE_NAME,self.TABLE_COLUMN_ID,self.TABLE_COLUMN_PICTURE_NAME,self.TABLE_COLUMN_JOBID)
        self.dbConnection.execute(CREATE_TABLE)

    def addRungingJob(self,pictureName:str, jobId:int):
        INSERT_VALUE = '''INSERT INTO {} ({},{}) VALUES ('{}',{});''' \
            .format(self.TABLE_NAME,self.TABLE_COLUMN_PICTURE_NAME,self.TABLE_COLUMN_JOBID,pictureName,jobId)
        self.dbConnection.execute(INSERT_VALUE);
        self.dbConnection.commit()

    def isInPrint(self,pictureName:str):
        SELECT = '''SELECT {} from {} WHERE {} = '{}';''' \
            .format(self.TABLE_COLUMN_ID, self.TABLE_NAME,self.TABLE_COLUMN_PICTURE_NAME,pictureName)
        cursor = self.dbConnection.execute(SELECT)
        result = []
        for row in cursor:
           result.append(str(row[1]))
        return len(result) > 0

    def getFirstJob(self,pictureName:str):
        SELECT = '''SELECT {} from {} WHERE {} = '{}';''' \
            .format(self.TABLE_COLUMN_JOBID, self.TABLE_NAME,self.TABLE_COLUMN_PICTURE_NAME,pictureName)
        cursor = self.dbConnection.execute(SELECT)
        result = []
        for row in cursor:
            result.append(int(row[0]))
        if len(result) <=0:
            return None
        else:
            return result[0]

    def getAllJobs(self):
        SELECT = '''SELECT {}, {} from {};''' \
            .format(self.TABLE_COLUMN_JOBID,self.TABLE_COLUMN_PICTURE_NAME, self.TABLE_NAME)
        cursor = self.dbConnection.execute(SELECT)
        result = []
        for row in cursor:
            result.append([int(row[0]),str(row[1])])
        return result

    def setJobFinished(self,pictureName:str):
        DELETE_ALL_BY_NAME = '''DELETE FROM {} WHERE {} = '{}';''' \
            .format(self.TABLE_NAME,self.TABLE_COLUMN_PICTURE_NAME,pictureName)
        self.dbConnection.execute(DELETE_ALL_BY_NAME);
        self.dbConnection.commit()

    def printAllDEBUG(self):
        GET_ALL = '''SELECT {},  {}, {} from {}'''.format(self.TABLE_COLUMN_ID,self.TABLE_COLUMN_PICTURE_NAME,self.TABLE_COLUMN_JOBID,self.TABLE_NAME)
        cursor = self.dbConnection.execute(GET_ALL)
        for row in cursor:
            print("ID= "+str(row[0])+" |PICTURE_NAME = "+str(row[1])+ " |JOB_ID = "+ str(row[2]))

    def close(self):
        self.dbConnection.close()

    def _getDBPath(self):
        return os.path.join(CfgService.get(CfgKey.MAIN_SAVE_DIR), CfgService.get(CfgKey.PROJECTNAME),CfgService.get(CfgKey.DB_NAME))
