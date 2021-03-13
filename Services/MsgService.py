from config.Config import TextKey, textValue


class MsgService():

    @staticmethod
    def get(key:TextKey):
        return textValue[key]

    @staticmethod
    def set(key:TextKey, text:str):
        textValue[key] = text