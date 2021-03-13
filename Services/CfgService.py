from Services.PropertiesService import PropertiesService
from config.Config import CfgKey, cfgValue, TextKey, textValue


class CfgService():

    @staticmethod
    def get(key:CfgKey):
        propertiesService = PropertiesService()
        propertiesValue = propertiesService.find(key)
        if propertiesValue == None:
            return cfgValue[key]
        else:
            cfgValue[key] = CfgService._convertString(propertiesValue, key)
            return propertiesValue

    @staticmethod
    def set(key:CfgKey,value):
        cfgValue[key] = value

    @staticmethod
    def _convertString(value:str, key:CfgKey):
        try:
            return cfgValue[key].__class__(value)
        except Exception as e:
            print(key._name_+" konnte nicht in '"+cfgValue[key].__class__+"' umgewandelt werden!")
            return value


