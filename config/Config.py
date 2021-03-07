import enum
from PyQt5 import QtCore

class CfgKey(enum.Enum):

    APPLICATION_CURSOR_HINT = 10
    IS_PI = 11

    MAIN_WINDOW_BACKGROUND_COLOR = 50
    MAIN_WINDOW_BUTTON_BACKGROUND_COLOR = 51
    MAIN_WINDOW_BUTTON_HEIGHT = 54
    MAIN_WINDOW_TEXT_SIZE=52
    MAIN_WINDOW_TEXT_FONT=53

    TITLE_SIZE = 100
    TITLE_FONT = 101
    TITLE_BACKGROUND_COLOR=102
    TITLE_COLOR=103
    TEXT_COLOR=110

    DIR_PICTURE = 1

    #PageTitlePicture.py
    PAGE_TITLEPICTURE_BUTTON_BACKGROUND_COLOR = 130
    PAGE_TITLEPICTURE_BUTTON_IMAGE_FOLDER=131

    #PageCameraPreview
    PAGE_CAMERAPREVIEW_COUNDOWN_IMAGE_FOLDER=140
    PAGE_CAMERAPREVIEW_COUNTER_PERIOD_LENGTH=141
    PAGE_CAMERAPREVIEW_COUNTER_START_VALUE=142

    #PageCapturePhoto
    PAGE_CAPTUREPHOTO_LAST_IMAGE_FOLDER=150
    PAGE_CAPTUREPHOTO_TIMER_PERIOD_LENGTH=151
    PAGE_CAPTUREPHOTO_TIMER_START_VALUE=152

cfgValue = {}

cfgValue[CfgKey.IS_PI] = False                      #Changeable -> True when RasPi
cfgValue[CfgKey.APPLICATION_CURSOR_HINT] = False    #Changeable -> True when RasPi

cfgValue[CfgKey.DIR_PICTURE] = "picture"

#Styling
cfgValue[CfgKey.MAIN_WINDOW_BACKGROUND_COLOR] = "black"
cfgValue[CfgKey.MAIN_WINDOW_BUTTON_BACKGROUND_COLOR] = "rgb(30,30,30)"
cfgValue[CfgKey.MAIN_WINDOW_BUTTON_HEIGHT] = "80px"
cfgValue[CfgKey.MAIN_WINDOW_TEXT_SIZE] = "35px"
cfgValue[CfgKey.MAIN_WINDOW_TEXT_FONT] = 'Arial Black'
cfgValue[CfgKey.TITLE_SIZE] = "80px"
cfgValue[CfgKey.TITLE_FONT] = 'Arial Black'
cfgValue[CfgKey.TITLE_BACKGROUND_COLOR] = 'grey'
cfgValue[CfgKey.TITLE_COLOR] = 'white'
cfgValue[CfgKey.TEXT_COLOR] = 'white'

#PageTitlePicture.py
cfgValue[CfgKey.PAGE_TITLEPICTURE_BUTTON_BACKGROUND_COLOR] = 'yellow'
        #Quellen: mouth smile
cfgValue[CfgKey.PAGE_TITLEPICTURE_BUTTON_IMAGE_FOLDER] = 'Pages/Resources/PageTitlePicture'

#PageCameraPreview.py
cfgValue[CfgKey.PAGE_CAMERAPREVIEW_COUNDOWN_IMAGE_FOLDER] = 'Pages/Resources/PageCameraPreview/CountDown'
cfgValue[CfgKey.PAGE_CAMERAPREVIEW_COUNTER_PERIOD_LENGTH] = 1000
cfgValue[CfgKey.PAGE_CAMERAPREVIEW_COUNTER_START_VALUE] = 6

#PageCaoturePhoto.py
cfgValue[CfgKey.PAGE_CAPTUREPHOTO_LAST_IMAGE_FOLDER] = 'Pages/Resources/PageCapturePhoto/LastImage'
cfgValue[CfgKey.PAGE_CAPTUREPHOTO_TIMER_PERIOD_LENGTH] = 500
cfgValue[CfgKey.PAGE_CAPTUREPHOTO_TIMER_START_VALUE] = 2


###########################################################
class TextKey(enum.Enum):
    #PageConfig.py
    PAGE_CONFIG_TITLE=20
    PAGE_CONFIG_NEXTBUTTON=21
    PAGE_CONFIG_HINT_TITLE=23
    PAGE_CONFIG_ESCAPE_HINT=22

    #PageCloseConfirm.py
    PAGE_CLOSECONFIRM_TITLE = 30
    PAGE_CLOSECONFIRM_TEXT = 31
    PAGE_CLOSECONFIRM_YES = 32
    PAGE_CLOSECONFIRM_NO = 33

textValue={}

#PageConfig
textValue[TextKey.PAGE_CONFIG_TITLE] = "Konfigurationen"
textValue[TextKey.PAGE_CONFIG_NEXTBUTTON] = "Fotobox starten"
textValue[TextKey.PAGE_CONFIG_HINT_TITLE] = "Hinweise:"
textValue[TextKey.PAGE_CONFIG_ESCAPE_HINT] = "- Um das Programm verlassen zu können, muss ESC gedrückt werden."

#PageCloseConfirm
textValue[TextKey.PAGE_CLOSECONFIRM_TITLE] = "Anwendung schließen?"
textValue[TextKey.PAGE_CLOSECONFIRM_TEXT] = "Soll die Anwendung geschlossen werden?"
textValue[TextKey.PAGE_CLOSECONFIRM_YES] = "Ja"
textValue[TextKey.PAGE_CLOSECONFIRM_NO] = "Nein"