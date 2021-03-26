from Services.FileFolderService import FileFolderService
from config.Config import CfgKey, cfgValue


class PropertiesService():

    def __init__(self):
        self.propertiesPath = cfgValue[CfgKey.PROPERTIES_PATH]
        self.KEY_VALUE_SEPPARATOR = "="

    def set(self, key:CfgKey, value):
        keyValuePairs = {}
        if FileFolderService.existFile(self.propertiesPath):
            fileLines = FileFolderService.readFile(self.propertiesPath)
            keyValuePairs = self._getPropertiesAsDict(fileLines)
        self._saveProperty(keyValuePairs, key, value)

    def find(self, key:CfgKey):
        if FileFolderService.existFile(self.propertiesPath):
            fileLines = FileFolderService.readFile(self.propertiesPath)
            keyValuePairs = self._getPropertiesAsDict(fileLines)
            if key._name_ in keyValuePairs:
                return keyValuePairs[key._name_]
        return None

    def _getPropertiesAsDict(self,fileLines:list):
        keyValuePairs = {}
        for line in fileLines:
            lineSplitted = str(line).split(self.KEY_VALUE_SEPPARATOR,1)
            if(len(lineSplitted)>1):
                key = lineSplitted[0].strip()
                value = lineSplitted[1].strip()
                if(len(key) > 0 and len(value) > 0):
                    keyValuePairs[key] = value
        return keyValuePairs

    def _saveProperty(self, existKeyValuePairs:dict, key:CfgKey, value):
        existKeyValuePairs[key._name_] = str(value)
        propertiesLines = []
        for key in existKeyValuePairs:
            propertiesLines.append(str(key)+self.KEY_VALUE_SEPPARATOR+str(existKeyValuePairs[key]))
        FileFolderService.writeLinesInFile(False,self.propertiesPath,propertiesLines)


