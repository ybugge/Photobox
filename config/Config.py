import enum
from PyQt5 import QtCore

class CfgKey(enum.Enum):

    APPLICATION_CURSOR_HINT = 10
    IS_PI = 11
    USED_CAMERA_INDEX = 12

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
cfgValue[CfgKey.USED_CAMERA_INDEX] = 0

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
cfgValue[CfgKey.PAGE_CAPTUREPHOTO_LAST_IMAGE_FOLDER] = 'Pages/Resources/PageCapturePhoto/LastPicture'
cfgValue[CfgKey.PAGE_CAPTUREPHOTO_TIMER_PERIOD_LENGTH] = 500
cfgValue[CfgKey.PAGE_CAPTUREPHOTO_TIMER_START_VALUE] = 2


###########################################################
class TextKey(enum.Enum):

    #PageHints.py
    PAGE_HINTS_TITLE=40
    PAGE_HINTS_ESCAPE_HINT=41
    PAGE_HINTS_NO_CAMERA_WARN=42
    PAGE_HINTS_NO_SELECTED_CAMERA_WARN=44
    PAGE_HINTS_SELECTED_CAMERA_HINT=45
    PAGE_HINTS_NO_PICTURES_FOUND_WARN=46
    PAGE_HINTS_NEXTBUTTON = 43

    #PageConfig.py
    PAGE_CONFIG_TITLE=20
    PAGE_CONFIG_NEXTBUTTON=21
    PAGE_CONFIG_BACKBUTTON=22

    #PageCloseConfirm.py
    PAGE_CLOSECONFIRM_TITLE = 30
    PAGE_CLOSECONFIRM_TEXT = 31
    PAGE_CLOSECONFIRM_YES = 32
    PAGE_CLOSECONFIRM_NO = 33

textValue={}

#PageHints
textValue[TextKey.PAGE_HINTS_TITLE] = "Hinweise:"
textValue[TextKey.PAGE_HINTS_ESCAPE_HINT] = "- Um das Programm verlassen zu können, muss ESC gedrückt werden."
textValue[TextKey.PAGE_HINTS_NO_CAMERA_WARN] = "- Fehler: Es wurde keine Kamera gefunden! Bitte schließen sie eine Kamera an und starten Sie die Anwendung neu!"
textValue[TextKey.PAGE_HINTS_NO_SELECTED_CAMERA_WARN] = "- Fehler: Die ausgewählte Kamera ist nicht verfügbar. Schließen Sie bitte die Kammera an oder korrigieren Sie den Index in Config.py->"+CfgKey.USED_CAMERA_INDEX.name+". Bitte schließen Sie die Software!"
textValue[TextKey.PAGE_HINTS_SELECTED_CAMERA_HINT] = "- Die Kamera kann über den Index 0-n in Config.py->"+CfgKey.USED_CAMERA_INDEX.name+" ausgewählt werden. Folgende Kamera wird verwendet: Index=%s | Name=%s | Beschreibung=%s."
textValue[TextKey.PAGE_HINTS_NO_PICTURES_FOUND_WARN]= "- Fehler: Bitte erstellen sie folgenden Ordner und hinterlegen Sie mindestens ein Bild: '%s' ! Bitte schließen Sie die Software!"
textValue[TextKey.PAGE_HINTS_NEXTBUTTON] = "Weiter"

#PageConfig
textValue[TextKey.PAGE_CONFIG_TITLE] = "Konfigurationen"
textValue[TextKey.PAGE_CONFIG_NEXTBUTTON] = "Fotobox starten"
textValue[TextKey.PAGE_CONFIG_BACKBUTTON] = "Zurück"

#PageCloseConfirm
textValue[TextKey.PAGE_CLOSECONFIRM_TITLE] = "Anwendung schließen?"
textValue[TextKey.PAGE_CLOSECONFIRM_TEXT] = "Soll die Anwendung geschlossen werden?"
textValue[TextKey.PAGE_CLOSECONFIRM_YES] = "Ja"
textValue[TextKey.PAGE_CLOSECONFIRM_NO] = "Nein"