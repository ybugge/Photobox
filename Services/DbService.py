import os
import sqlite3

from Services.CfgService import CfgService
from Services.FileFolderService import FileFolderService
from config.Config import CfgKey


class DbService():

    def __init__(self):
        self.dbConnection = None

        dbPathWithName = FileFolderService.getAbsoltPath(self._getDBPath())

        FileFolderService.creatFolderByFileIfNotExist(dbPathWithName)

        self.TABLE_NAME = "PICTURE"
        self.TABLE_COLUMN_ID = "ID"
        self.TABLE_COLUMN_NAME = "NAME"
        self.TABLE_COLUMN_PATH = "PATH"
        self.TABLE_COLUMN_ISUSED = "USED"

        self.dbConnection = sqlite3.connect(dbPathWithName)
        self._createTableIfNotExist()

    def _createTableIfNotExist(self):
        CREATE_TABLE = '''CREATE TABLE IF NOT EXISTS {} ({} INTEGER PRIMARY KEY AUTOINCREMENT, {} TEXT NOT NULL, {} TEXT NOT NULL, {} INTEGER NOT NULL);''' \
            .format(self.TABLE_NAME,self.TABLE_COLUMN_ID,self.TABLE_COLUMN_NAME,self.TABLE_COLUMN_PATH, self.TABLE_COLUMN_ISUSED)
        self.dbConnection.execute(CREATE_TABLE)

    def setPicture(self,pictureName:str, picturePATH:str, isUsed:bool):
        isUsedAsInt = 0
        if isUsed:
            isUsedAsInt = 1

        INSERT_VALUE = '''INSERT INTO {} ({},{},{}) VALUES ('{}','{}',{});'''\
            .format(self.TABLE_NAME,self.TABLE_COLUMN_NAME,self.TABLE_COLUMN_PATH,self.TABLE_COLUMN_ISUSED,pictureName,picturePATH,isUsedAsInt)
        self.dbConnection.execute(INSERT_VALUE);
        self.dbConnection.commit()

    def _deletById(self,id:str):
        DELETE_ALL_BY_ID = '''DELETE FROM {} WHERE {} = '{}';'''.format(self.TABLE_NAME,self.TABLE_COLUMN_ID,id)
        self.dbConnection.execute(DELETE_ALL_BY_ID);
        self.dbConnection.commit()

    def deletePictureByName(self, name:str):
        DELETE_ALL_BY_NAME = '''DELETE FROM {} WHERE {} = '{}';'''\
            .format(self.TABLE_NAME,self.TABLE_COLUMN_NAME,name)
        self.dbConnection.execute(DELETE_ALL_BY_NAME);
        self.dbConnection.commit()

    def getPictureNames(self):
        SELECT = '''SELECT {}, {}, {} from {};''' \
            .format(self.TABLE_COLUMN_ID, self.TABLE_COLUMN_NAME, self.TABLE_COLUMN_PATH, self.TABLE_NAME)
        cursor = self.dbConnection.execute(SELECT)
        result = []
        for row in cursor:
            if self._checkImageExist(str(row[0]),str(row[2])):
                result.append(str(row[1]))
        return list(set(result))


    def getPictureUrlIds(self,name:str):
        SELECT = '''SELECT {}, {}, {} from {} WHERE {} = '{}'; '''\
            .format(self.TABLE_COLUMN_ID, self.TABLE_COLUMN_NAME, self.TABLE_COLUMN_PATH, self.TABLE_NAME, self.TABLE_COLUMN_NAME, name)

        cursor = self.dbConnection.execute(SELECT)
        result = []
        for row in cursor:
            if self._checkImageExist(str(row[0]),str(row[2])):
                result.append(str(row[1])+"_"+str(row[0]))
        return result

    def getPicturePath(self, urlId:str):
        if not urlId or len(urlId.rsplit("_",1)) != 2:
            return None
        urlIdSplitted = urlId.rsplit("_",1)
        id = urlIdSplitted[1]
        name = urlIdSplitted[0]

        SELECT = '''SELECT {}, {}, {} from {} WHERE ({} = '{}' AND {} = '{}'); '''\
            .format(self.TABLE_COLUMN_ID, self.TABLE_COLUMN_NAME, self.TABLE_COLUMN_PATH, self.TABLE_NAME, self.TABLE_COLUMN_ID, id, self.TABLE_COLUMN_NAME, name)

        cursor = self.dbConnection.execute(SELECT)
        result = []
        for row in cursor:
            if self._checkImageExist(str(row[0]),str(row[2])):
                result.append([row[1],row[2]])
        if not result:
            return None
        else:
            return result[0]

    def getUsedPictureUrlIdsUnsecure(self):
        SELECT = '''SELECT {}, {}, {} from {} WHERE {} = '{}'; ''' \
            .format(self.TABLE_COLUMN_ID, self.TABLE_COLUMN_NAME, self.TABLE_COLUMN_PATH, self.TABLE_NAME, self.TABLE_COLUMN_ISUSED, 1)

        cursor = self.dbConnection.execute(SELECT)
        result = []
        for row in cursor:
            result.append(str(row[1])+"_"+str(row[0]))
        return result

    def getNumberUsedPicture(self):
        SELECT = '''SELECT COUNT(DISTINCT {}) FROM {} WHERE {} = {}''' \
            .format(self.TABLE_COLUMN_NAME,self.TABLE_NAME, self.TABLE_COLUMN_ISUSED, 1)
        cursor = self.dbConnection.execute(SELECT)
        result = []
        for row in cursor:
            result.append(int(row[0]))

        if len(result) <= 0:
            return 0
        else:
            return result[0]

    def _checkImageExist(self,id:str,path:str):
        if(FileFolderService.existFile(path)):
            return True
        else:
            self._deletById(id)
            return False


    def printAllDEBUG(self):
        GET_ALL = '''SELECT {},  {}, {} from {}'''.format(self.TABLE_COLUMN_ID,self.TABLE_COLUMN_NAME,self.TABLE_COLUMN_PATH,self.TABLE_NAME)
        cursor = self.dbConnection.execute(GET_ALL)
        for row in cursor:
            print("ID= "+str(row[0])+" |NAME = "+str(row[1])+ " |PATH = "+ str(row[2]))

    def close(self):
        self.dbConnection.close()

    def _getDBPath(self):
        return os.path.join(CfgService.get(CfgKey.MAIN_SAVE_DIR), CfgService.get(CfgKey.PROJECTNAME),CfgService.get(CfgKey.DB_NAME))

