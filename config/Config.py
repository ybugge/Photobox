import enum
from PyQt5 import QtCore

class CfgKey(enum.Enum):

    #WIFI ##########################################################################################
    WIFI_SSID = 3000
    WIFI_PROTOCOL = 3001
    WIFI_PASSWORD = 3002
    WIFI_PICTURE_NAME = 3003

    #DATABASE #######################################################################################
    DB_NAME = 2001

    #SERVER #########################################################################################
    SERVER_INDEX_PAGE = 1000
    SERVER_DOWNLOAD_PICTURE_PAGE = 1001
    SERVER_DOWNLOAD_PICTURE = 1002
    SERVER_RANDOM_URLIDS = 1003
    SERVER_DB_PATH = 2003
    SERVER_IP=2004
    SERVER_PORT=2005
    SERVER_GETPICTUREURLIDS_NUMBER = 2006

    #FOTOBOX #########################################################################################
    APPLICATION_DB_PATH = 13
    APPLICATION_CURSOR_HINT = 10
    IS_PI = 11
    USE_PI_CAMERA = 14
    USED_CAMERA_INDEX = 12
    PI_CAMERA_VIDEO_RESOLUTION = 15
    PI_CAMERA_VIDEO_FPS = 16
    PI_CAMERA_PHOTO_RESOLUTION = 17

    MAIN_WINDOW_BACKGROUND_COLOR = 50
    MAIN_WINDOW_BUTTON_BACKGROUND_COLOR = 51
    MAIN_WINDOW_BUTTON_HEIGHT = 54
    MAIN_WINDOW_TEXT_SIZE=52
    MAIN_WINDOW_TEXT_FONT=53
    MAIN_WINDOW_LABEL_EDIT_BORDER_COLOR=55
    MAIN_WINDOW_LABEL_EDIT_BACKGROUND_COLOR=56

    TITLE_SIZE = 100
    TITLE_FONT = 101
    TITLE_BACKGROUND_COLOR=102
    TITLE_COLOR=103
    TEXT_COLOR=110
    BUTTON_DISABLED_TEXT_COLOR=111
    PROGRESSBAR_CHUNK_BACKGROUND_COLOR=112

    MAIN_SAVE_DIR = 1
    PROJECTNAME = 2
    RAW_PICTURE_SUB_DIR=3
    USED_PICTURE_SUB_DIR = 4
    UNUSED_PICTURE_SUB_DIR = 5
    PICTURE_FORMAT=6
    PROPERTIES_PATH = 7

    #PageSystemPictureManager.py
    PAGE_SYSTEMPICTUREMANAGER_FUNNY_PICTURE_SOURCE = 200
    PAGE_SYSTEMPICTUREMANAGER_FUNNY_PICTURE_SOURCE_SUCCESS_DOWNLOAD = 201

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
    PAGE_CAPTUREPHOTO_TIMER_CAPTUREPHOTO_VALUE=153

    #PagePictureEdit.py
    PAGE_PICTUREEDIT_FINISHED_BUTTON_ICON_DIR = 600
    PAGE_PICTUREEDIT_NEWPICTURE_BUTTON_ICON_DIR = 601
    PAGE_PICTUREEDIT_PRINT_BUTTON_ICON_DIR = 602
    PAGE_PICTUREEDIT_DOWNLOAD_BUTTON_ICON_DIR = 603
    PAGE_PICTUREEDIT_SPACE_AUTO_FORWARD_WAIT_TIME = 604


cfgValue = {}

#WIFI ##########################################################################################
cfgValue[CfgKey.WIFI_SSID] = "Phoenix-Photobox"
cfgValue[CfgKey.WIFI_PROTOCOL] = "WPA/WPA2"
cfgValue[CfgKey.WIFI_PASSWORD] = "09059528003481556247"
cfgValue[CfgKey.WIFI_PICTURE_NAME] = "wifi.png"

#DB #############################################################################
cfgValue[CfgKey.DB_NAME] = "fotobox.db"
cfgValue[CfgKey.SERVER_DB_PATH] = "Server/db"
cfgValue[CfgKey.APPLICATION_DB_PATH] = "Server/db"

#SERVER #########################################################################
cfgValue[CfgKey.SERVER_INDEX_PAGE] = "/"
cfgValue[CfgKey.SERVER_DOWNLOAD_PICTURE_PAGE] = "/downloadpage"
cfgValue[CfgKey.SERVER_DOWNLOAD_PICTURE] = "/downloadimage"
cfgValue[CfgKey.SERVER_RANDOM_URLIDS] = "/pictureuris"
cfgValue[CfgKey.SERVER_IP] = "photobox.fritz.box"
cfgValue[CfgKey.SERVER_PORT] = "5000"
cfgValue[CfgKey.SERVER_GETPICTUREURLIDS_NUMBER] = 20

# FOTOBOX #######################################################################

cfgValue[CfgKey.IS_PI] = False                      #Changeable -> True when RasPi
cfgValue[CfgKey.USE_PI_CAMERA] = None               #Changeable -> True or False
cfgValue[CfgKey.APPLICATION_CURSOR_HINT] = False    #Changeable -> True when RasPi
cfgValue[CfgKey.USED_CAMERA_INDEX] = 0
#https://picamera.readthedocs.io/en/release-1.10/fov.html
#(1296,730) / (640,480) / (1920,1080)
cfgValue[CfgKey.PI_CAMERA_VIDEO_RESOLUTION] = (1296,730)
cfgValue[CfgKey.PI_CAMERA_VIDEO_FPS] = 25
cfgValue[CfgKey.PI_CAMERA_PHOTO_RESOLUTION] = (2592,1944)
cfgValue[CfgKey.PROPERTIES_PATH] = "Resources/config.properties"

cfgValue[CfgKey.MAIN_SAVE_DIR] = "FotoboxData/"
cfgValue[CfgKey.PROJECTNAME] = "Party"
cfgValue[CfgKey.RAW_PICTURE_SUB_DIR] = "raw"
cfgValue[CfgKey.USED_PICTURE_SUB_DIR] = "used"
cfgValue[CfgKey.UNUSED_PICTURE_SUB_DIR] = "unused"
cfgValue[CfgKey.PICTURE_FORMAT] = ".png"

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
cfgValue[CfgKey.BUTTON_DISABLED_TEXT_COLOR] = 'rgb(80,80,80)'
cfgValue[CfgKey.PROGRESSBAR_CHUNK_BACKGROUND_COLOR] = 'grey'
cfgValue[CfgKey.MAIN_WINDOW_LABEL_EDIT_BORDER_COLOR] = 'rgb(80,80,80)'
cfgValue[CfgKey.MAIN_WINDOW_LABEL_EDIT_BACKGROUND_COLOR] = 'rgb(30,30,30)'

#PageSystemPictureManager.py
cfgValue[CfgKey.PAGE_SYSTEMPICTUREMANAGER_FUNNY_PICTURE_SOURCE] = "Resources/funnyPicturesUrl.txt"
cfgValue[CfgKey.PAGE_SYSTEMPICTUREMANAGER_FUNNY_PICTURE_SOURCE_SUCCESS_DOWNLOAD] = "Resources/funnyPicturesUrlDownloaded.txt"

#PageTitlePicture.py
cfgValue[CfgKey.PAGE_TITLEPICTURE_BUTTON_BACKGROUND_COLOR] = 'yellow'
        #Quellen: mouth smile
cfgValue[CfgKey.PAGE_TITLEPICTURE_BUTTON_IMAGE_FOLDER] = 'Resources/PageTitlePicture'

#PageCameraPreview.py
cfgValue[CfgKey.PAGE_CAMERAPREVIEW_COUNDOWN_IMAGE_FOLDER] = 'Resources/PageCameraPreview/CountDown'
cfgValue[CfgKey.PAGE_CAMERAPREVIEW_COUNTER_PERIOD_LENGTH] = 1000
cfgValue[CfgKey.PAGE_CAMERAPREVIEW_COUNTER_START_VALUE] = 6

#PageCaoturePhoto.py
cfgValue[CfgKey.PAGE_CAPTUREPHOTO_LAST_IMAGE_FOLDER] = 'Resources/PageCapturePhoto/FunnyPictures'
cfgValue[CfgKey.PAGE_CAPTUREPHOTO_TIMER_PERIOD_LENGTH] = 250
cfgValue[CfgKey.PAGE_CAPTUREPHOTO_TIMER_START_VALUE] = 4
cfgValue[CfgKey.PAGE_CAPTUREPHOTO_TIMER_CAPTUREPHOTO_VALUE] = 4

#PagePictureEdit.py
cfgValue[CfgKey.PAGE_PICTUREEDIT_FINISHED_BUTTON_ICON_DIR] = "Resources/PagePictureEdit/Icon/finish_icon.png"
cfgValue[CfgKey.PAGE_PICTUREEDIT_NEWPICTURE_BUTTON_ICON_DIR] = "Resources/PagePictureEdit/Icon/newPhoto_icon.png"
cfgValue[CfgKey.PAGE_PICTUREEDIT_PRINT_BUTTON_ICON_DIR] = "Resources/PagePictureEdit/Icon/print_icon.png"
cfgValue[CfgKey.PAGE_PICTUREEDIT_DOWNLOAD_BUTTON_ICON_DIR] = "Resources/PagePictureEdit/Icon/download_icon.png"
# 300000 = 5 minutes
cfgValue[CfgKey.PAGE_PICTUREEDIT_SPACE_AUTO_FORWARD_WAIT_TIME] = 300000

###########################################################
class TextKey(enum.Enum):

    #PageSystemPictureManager.py
    PAGE_SYSTEMPICTUREMANAGER_TITLE = 60
    PAGE_SYSTEMPICTUREMANAGER_NEXTBUTTON = 61
    PAGE_SYSTEMPICTUREMANAGER_FUNNY_TITEL = 66
    PAGE_SYSTEMPICTUREMANAGER_FUNNY_SOURCELABEL = 64
    PAGE_SYSTEMPICTUREMANAGER_FUNNY_TARGETLABEL = 65
    PAGE_SYSTEMPICTUREMANAGER_FUNNY_DELETEBUTTON = 62
    PAGE_SYSTEMPICTUREMANAGER_FUNNY_UPDATEBUTTON = 63
    PAGE_SYSTEMPICTUREMANAGER_SUCCESSFULL = 67

    #PageHints.py
    PAGE_HINTS_TITLE=40
    PAGE_HINTS_ESCAPE_HINT=41
    PAGE_HINTS_NO_CAMERA_WARN=42
    PAGE_HINTS_NO_SELECTED_CAMERA_WARN=44
    PAGE_HINTS_SELECTED_CAMERA_HINT=45
    PAGE_HINTS_SELECTED_PICAMERA_HINT=51
    PAGE_HINTS_NO_PICTURES_FOUND_WARN=46
    PAGE_HINTS_NEXTBUTTON = 43
    PAGE_HINTS_PICTURE_MANAGER_BUTTON = 50

    #PageConfig.py
    PAGE_CONFIG_TITLE=20
    PAGE_CONFIG_NEXTBUTTON=21
    PAGE_CONFIG_BACKBUTTON=22
    PAGE_CONFIG_MAIN_SAVE_DIR_TITLE=23
    PAGE_CONFIG_PROJECT_NAME_TITLE=24
    PAGE_CONFIG_CAMERA_CALIBRATION_BUTTON=25
    PAGE_CONFIG_SERVER_IPANDPORT_TITLE=26
    PAGE_CONFIG_WIFI_TITLE=27
    PAGE_CONFIG_WIFI_PICTURE_BUTTON=28

    #PageCloseConfirm.py
    PAGE_CLOSECONFIRM_TITLE = 30
    PAGE_CLOSECONFIRM_TEXT = 31
    PAGE_CLOSECONFIRM_YES = 32
    PAGE_CLOSECONFIRM_NO = 33

    #PageDownloadPicture.py
    PAGE_DOWNLOADPICTURE_TITLE = 100
    PAGE_DOWNLOADPICTURE_BACKBUTTON = 101
    PAGE_DOWNLOADPICTURE_WIFI_TITLE = 102

textValue={}

#PageSystemPictureManager.py
textValue[TextKey.PAGE_SYSTEMPICTUREMANAGER_TITLE] = "Systembilder Bearbeiten"
textValue[TextKey.PAGE_SYSTEMPICTUREMANAGER_NEXTBUTTON] = "Zurück zu den Hinweisen"
textValue[TextKey.PAGE_SYSTEMPICTUREMANAGER_FUNNY_TITEL] = "Lustige Bilder"
textValue[TextKey.PAGE_SYSTEMPICTUREMANAGER_FUNNY_SOURCELABEL] = "Quell-URLs:"
textValue[TextKey.PAGE_SYSTEMPICTUREMANAGER_FUNNY_TARGETLABEL] = "Ziel-Ordner:"
textValue[TextKey.PAGE_SYSTEMPICTUREMANAGER_FUNNY_DELETEBUTTON] = "Bilder löschen"
textValue[TextKey.PAGE_SYSTEMPICTUREMANAGER_FUNNY_UPDATEBUTTON] = "Bilder herunterladen"
textValue[TextKey.PAGE_SYSTEMPICTUREMANAGER_SUCCESSFULL] = "OK"

#PageHints
textValue[TextKey.PAGE_HINTS_NEXTBUTTON] = "Weiter"
textValue[TextKey.PAGE_HINTS_PICTURE_MANAGER_BUTTON] = "Systembilder bearbeiten"
textValue[TextKey.PAGE_HINTS_TITLE] = "Hinweise:"
textValue[TextKey.PAGE_HINTS_ESCAPE_HINT] = "- Um das Programm verlassen zu können, muss ESC gedrückt werden."
textValue[TextKey.PAGE_HINTS_NO_CAMERA_WARN] = "- Fehler: Es wurde keine Kamera gefunden! Bitte schließen sie eine Kamera an und starten Sie die Anwendung neu!"
textValue[TextKey.PAGE_HINTS_NO_SELECTED_CAMERA_WARN] = "- Fehler: Die ausgewählte Kamera ist nicht verfügbar. Schließen Sie bitte die Kammera an oder korrigieren Sie den Index in Config.py->"+CfgKey.USED_CAMERA_INDEX.name+". Bitte schließen Sie die Software!"
textValue[TextKey.PAGE_HINTS_SELECTED_CAMERA_HINT] = "- Die Kamera kann über den Index 0-n in Config.py->"+CfgKey.USED_CAMERA_INDEX.name+" ausgewählt werden. Folgende Kamera wird verwendet: Index=%s | Name=%s | Beschreibung=%s."
textValue[TextKey.PAGE_HINTS_SELECTED_PICAMERA_HINT] = "- Verwendet wird die Kamera: Pi-Camera"
textValue[TextKey.PAGE_HINTS_NO_PICTURES_FOUND_WARN]= "- Fehler: Bitte erstellen sie folgenden Ordner und hinterlegen Sie mindestens ein Bild: '%s' ! Bitte schließen Sie die Software oder laden sie die Bilder über den Button '"+textValue[TextKey.PAGE_HINTS_PICTURE_MANAGER_BUTTON]+"' herunter!"

#PageConfig
textValue[TextKey.PAGE_CONFIG_TITLE] = "Konfigurationen"
textValue[TextKey.PAGE_CONFIG_NEXTBUTTON] = "Fotobox starten"
textValue[TextKey.PAGE_CONFIG_BACKBUTTON] = "Zurück"
textValue[TextKey.PAGE_CONFIG_MAIN_SAVE_DIR_TITLE] = "Speicherort:"
textValue[TextKey.PAGE_CONFIG_PROJECT_NAME_TITLE] = "Projektname:"
textValue[TextKey.PAGE_CONFIG_CAMERA_CALIBRATION_BUTTON] = "Kamera kalibrieren"
textValue[TextKey.PAGE_CONFIG_SERVER_IPANDPORT_TITLE] = "Server IP und Port"
textValue[TextKey.PAGE_CONFIG_WIFI_TITLE] = "WIFI"
textValue[TextKey.PAGE_CONFIG_WIFI_PICTURE_BUTTON] = "QR-Code speichern"

#PageCloseConfirm
textValue[TextKey.PAGE_CLOSECONFIRM_TITLE] = "Anwendung schließen?"
textValue[TextKey.PAGE_CLOSECONFIRM_TEXT] = "Soll die Anwendung geschlossen werden?"
textValue[TextKey.PAGE_CLOSECONFIRM_YES] = "Ja"
textValue[TextKey.PAGE_CLOSECONFIRM_NO] = "Nein"

#PageDownloadPicture.py
textValue[TextKey.PAGE_DOWNLOADPICTURE_TITLE] = "Bild transferieren"
textValue[TextKey.PAGE_DOWNLOADPICTURE_WIFI_TITLE] = "Mit der Fotobox verbinden"
textValue[TextKey.PAGE_DOWNLOADPICTURE_BACKBUTTON] = "Zurück"