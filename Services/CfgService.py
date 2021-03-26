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
            return cfgValue[key]

    @staticmethod
    def set(key:CfgKey,value):
        if cfgValue[key] != value:
            cfgValue[key] = value
            propertiesService = PropertiesService()
            propertiesService.set(key, value)

    @staticmethod
    def _convertString(value:str, key:CfgKey):
        try:
            if cfgValue[key].__class__ == bool:
                if value == "True":
                    return True
                else:
                    return False
            else:
                return cfgValue[key].__class__(value)
        except Exception as e:
            print(key._name_+" konnte nicht in '"+cfgValue[key].__class__+"' umgewandelt werden!")
            return value


