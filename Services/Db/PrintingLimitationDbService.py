import os
import sqlite3

from Services.CfgService import CfgService
from Services.FileFolderService import FileFolderService
from config.Config import CfgKey


class PrintingLimitationDbService():
    def __init__(self):
        self.dbConnection = None

        dbPathWithName = FileFolderService.getAbsoltPath(self._getDBPath())
        FileFolderService.creatFolderByFileIfNotExist(dbPathWithName)

        self.TABLE_NAME = "PRINTING_LIMITATION"
        self.TABLE_COLUMN_PICTURE_NAME = "PICTURE_NAME"
        self.TABLE_COLUMN_ORDER_NUMBER = "ORDER_NUMBER"

        self.dbConnection = sqlite3.connect(dbPathWithName)
        self._createTableIfNotExist()

    def _createTableIfNotExist(self):
        CREATE_TABLE = '''CREATE TABLE IF NOT EXISTS {} ({} TEXT PRIMARY KEY, {} INTEGER NOT NULL);''' \
            .format(self.TABLE_NAME,self.TABLE_COLUMN_PICTURE_NAME,self.TABLE_COLUMN_ORDER_NUMBER)
        self.dbConnection.execute(CREATE_TABLE)

    def allowToPrint(self,pictureName:str):
        currentOrderNumber = self._getOrderNumber(pictureName)
        return self._allowToPrint(currentOrderNumber)

    def _allowToPrint(self,currentOrderNumber:int):
        maxPrintingOrderNumber = CfgService.get(CfgKey.PRINTER_MAX_PRINTING_ORDER)
        return currentOrderNumber < maxPrintingOrderNumber

    def setNewPrintOrder(self,pictureName:str):
        currentOrderNumber = self._getOrderNumber(pictureName)
        if self._allowToPrint(currentOrderNumber):
            if currentOrderNumber <= 0:
                self._addPrintOrder(pictureName)
            else:
                self._updatePrintOrder(pictureName)

    def _addPrintOrder(self,pictureName:str):
        INSERT_VALUE = '''INSERT INTO {} ({},{}) VALUES ('{}',{});''' \
                .format(self.TABLE_NAME,self.TABLE_COLUMN_PICTURE_NAME,self.TABLE_COLUMN_ORDER_NUMBER,pictureName,1)
        self.dbConnection.execute(INSERT_VALUE);
        self.dbConnection.commit()

    def _updatePrintOrder(self,pictureName:str):
        UPDATE_VALUE = '''UPDATE {} SET {} = {} + 1 WHERE {} = '{}';''' \
            .format(self.TABLE_NAME,self.TABLE_COLUMN_ORDER_NUMBER, self.TABLE_COLUMN_ORDER_NUMBER,self.TABLE_COLUMN_PICTURE_NAME,pictureName)
        self.dbConnection.execute(UPDATE_VALUE);
        self.dbConnection.commit()

    def _getOrderNumber(self,pictureName:str):
        SELECT = '''SELECT {} from {} WHERE {} = '{}';''' \
            .format(self.TABLE_COLUMN_ORDER_NUMBER, self.TABLE_NAME,self.TABLE_COLUMN_PICTURE_NAME,pictureName)
        cursor = self.dbConnection.execute(SELECT)
        result = []
        for row in cursor:
            result.append(int(row[0]))
        if len(result) > 0:
            return result[0]
        else:
            return 0

    def printAllDEBUG(self):
        GET_ALL = '''SELECT {},  {} from {}'''.format(self.TABLE_COLUMN_PICTURE_NAME,self.TABLE_COLUMN_ORDER_NUMBER,self.TABLE_NAME)
        cursor = self.dbConnection.execute(GET_ALL)
        for row in cursor:
            print("PICTURE_NAME = "+str(row[0])+ " |ORDER_NUMBER = "+ str(row[1]))

    def close(self):
        self.dbConnection.close()

    def _getDBPath(self):
        return os.path.join(CfgService.get(CfgKey.MAIN_SAVE_DIR), CfgService.get(CfgKey.PROJECTNAME),CfgService.get(CfgKey.DB_NAME))