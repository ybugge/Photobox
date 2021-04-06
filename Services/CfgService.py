from PyQt5.QtGui import QColor

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
    def setColor(key:CfgKey,color:QColor):
        valueAsString = str(color.getHsv()[0])+";"+str(color.getHsv()[1])+";"+str(color.getHsv()[2])
        if cfgValue[key] != valueAsString:
            cfgValue[key] = valueAsString
            propertiesService = PropertiesService()
            propertiesService.set(key, valueAsString)

    @staticmethod
    def getColor(key:CfgKey):
        propertiesService = PropertiesService()
        propertiesValue = propertiesService.find(key)

        if propertiesValue == None:
            colorCfgValue =  cfgValue[key]
        else:
            colorCfgValue = propertiesValue

        colorCfgValueHsvParts = colorCfgValue.split(";")
        if len(colorCfgValueHsvParts) != 3:
            print("Die Properties mit dem Key '"+key._name_+"' hat das falsche Format!")
            return QColor.fromHsv(0,0,0)
        else:
            return QColor.fromHsv(int(colorCfgValueHsvParts[0]),int(colorCfgValueHsvParts[1]),int(colorCfgValueHsvParts[2]))

    @staticmethod
    def _convertString(value:str, key:CfgKey):
        try:
            if cfgValue[key] == None:
                return value
            elif cfgValue[key].__class__ == bool:
                if value == "True":
                    return True
                else:
                    return False
            else:
                return cfgValue[key].__class__(value)
        except Exception as e:
            print(key._name_+" konnte nicht in '"+cfgValue[key].__class__+"' umgewandelt werden!")
            return value


