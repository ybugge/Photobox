import enum

class CfgKey(enum.Enum):

    #WIFI ##########################################################################################
    WIFI_SSID = 3000
    WIFI_PROTOCOL = 3001
    WIFI_PASSWORD = 3002
    WIFI_PICTURE_NAME = 3003
    WIFI_QR_CODE_FONT = 3004

    #DATABASE #######################################################################################
    DB_NAME = 2001

    #SERVER #########################################################################################
    SERVER_INDEX_PAGE = 1000
    SERVER_INDEX_PAGE_SHOW_ALL_PICTURES = 1004
    SERVER_DOWNLOAD_PICTURE_PAGE = 1001
    SERVER_DOWNLOAD_PICTURE = 1002
    SERVER_UPLOAD_PICTURE = 1005
    SERVER_DISPLAY_UPLOAD_PICTURE = 1011
    SERVER_UPLOAD_SUCCESS_PICTURE = 1006
    SERVER_RANDOM_URLIDS = 1003
    SERVER_IP=2004
    SERVER_PORT=2005
    SERVER_GETPICTUREURLIDS_NUMBER = 2006
    SERVER_GETPICTUREURLIDS_THRASHOLD = 2007
    SERVER_PRINT_PICTURE_PAGE = 1010
    SERVER_PRINT_INFORMATION_REST = 1012
    SERVER_PRINT_START_PRINT_REST = 1013
    SERVER_PRINT_REST_INFORMATION_INTERVALL = 1014

    #Printer #########################################################################################
    PRINTER_IS_ACTIVE = 6000
    PRINTER_IS_ACTIVE_WEB = 6005
    PRINTER_SELECTED = 6001
    PRINTER_PAPER_SIZE = 6002
    PRINTER_PAPER_FORMAT = 6003
    PRINTER_MAX_PRINTING_ORDER = 6004

    #GREENSCREEN #########################################################################################
    GREENSCREEN_IS_ACTIVE = 7000
    GREENSCREEN_MAX_COLOR_RANGE_HINT = 7001
    GREENSCREEN_MIN_HSV_GUI_COLOR = 7002
    GREENSCREEN_MAX_HSV_GUI_COLOR = 7003
    GREENSCREEN_AVERAGE_HSV_GUI_COLOR = 7004
    GREENSCREEN_MIN_HSV_CV2_COLOR = 7009
    GREENSCREEN_MAX_HSV_CV2_COLOR = 7010
    GREENSCREEN_AVERAGE_HSV_CV2_COLOR = 7011
    GREENSCREEN_FOLDER = 7012
    GREENSCREEN_TEMP_FOLDER = 7013
    GREENSCREEN_BACKGROUND_FOLDER = 7007
    GREENSCREEN_CUSTOM_BACKGROUND_FOLDER = 7008
    GREENSCREEN_CUSTOM_BACKGROUND_PREVIEW_FILENAME = 7015

    #DIASHOW CLIENT ##################################################################################
    DIASHOW_CLIENT_IS_ACTIVE = 5006
    DIASHOW_CLIENT_PICTURE_MAIN_FOLDER = 5000
    DIASHOW_CLIENT_PICTURE_CONFIG_FILE = 5001
    DIASHOW_CLIENT_PICTURE_SOURCE_FOLDER = 5002
    DIASHOW_CLIENT_PICTURE_FRAME_PICTURE = 5005
    DIASHOW_CLIENT_PICTURE_SHOW_NEW_PICTURE_INTERVAL = 5003
    DIASHOW_CLIENT_PICTURE_UPDATE_PICTURE_SOURCE_INTERVAL = 5004
    DIASHOW_CLIENT_PICTURE_UPDATE_PICTURE_SOURCE_INTERVAL_INITIAL = 5007

    #FOTOBOX #########################################################################################
    APPLICATION_CURSOR_HINT = 10
    IS_PI = 11
    USE_PI_CAMERA = 14
    USED_CAMERA_INDEX = 12
    PI_CAMERA_VIDEO_RESOLUTION = 15
    PI_CAMERA_VIDEO_FPS = 16
    PI_CAMERA_PHOTO_RESOLUTION = 17
    PI_CAMERA_STATIC_BRIGHTNESS = 18
    PI_CAMERA_STATIC_BRIGHTNESS_STATIC_VALUE = 21
    PI_CAMERA_STATIC_BRIGHTNESS_AWB_GAIN_RED = 19
    PI_CAMERA_STATIC_BRIGHTNESS_AWB_GAIN_BLUE = 20

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
    PAGE_SYSTEMPICTUREMANAGER_LOADINGGIFS_PICTURE_SOURCE = 203
    PAGE_SYSTEMPICTUREMANAGER_LOADINGGIFS_PICTURE_SOURCE_SUCCESS_DOWNLOAD = 204


    #PageTitlePicture.py
    PAGE_TITLEPICTURE_BUTTON_BACKGROUND_COLOR = 130
    PAGE_TITLEPICTURE_BUTTON_IMAGE_FOLDER=131
    PAGE_TITLEPICTURE_BACKGROUND_IMAGE=132

    #PageCameraPreview
    PAGE_CAMERAPREVIEW_COUNDOWN_IMAGE_FOLDER=140
    PAGE_CAMERAPREVIEW_COUNTER_PERIOD_LENGTH=141
    PAGE_CAMERAPREVIEW_COUNTER_START_VALUE=142

    #PageCapturePhoto
    PAGE_CAPTUREPHOTO_LAST_IMAGE_FOLDER=150
    PAGE_CAPTUREPHOTO_LOADING_GIF_FOLDER=154
    PAGE_CAPTUREPHOTO_TIMER_PERIOD_LENGTH=151
    PAGE_CAPTUREPHOTO_TIMER_START_VALUE=152
    PAGE_CAPTUREPHOTO_TIMER_CAPTUREPHOTO_VALUE=153

    #PagePictureEdit.py
    PAGE_PICTUREEDIT_FINISHED_BUTTON_ICON_DIR = 600
    PAGE_PICTUREEDIT_NEWPICTURE_BUTTON_ICON_DIR = 601
    PAGE_PICTUREEDIT_PRINT_BUTTON_ICON_DIR = 602
    PAGE_PICTUREEDIT_PRINT_BUTTON_DISABLED_ICON_DIR = 605
    PAGE_PICTUREEDIT_DOWNLOAD_BUTTON_ICON_DIR = 603
    PAGE_PICTUREEDIT_HELP_BUTTON_ICON_DIR = 607
    PAGE_PICTUREEDIT_SPACE_AUTO_FORWARD_WAIT_TIME = 604

    #PagePrint.py
    PAGE_PRINT_STATUS_UPDATE_PERIOD = 701

    #PageGreenscreenSelectBackround
    PAGE_GREENSCREEN_SELECT_BACKGROUND_ROTATE_LEFT_ICON = 801
    PAGE_GREENSCREEN_SELECT_BACKGROUND_ROTATE_RIGHT_ICON = 802

cfgValue = {}

#WIFI ##########################################################################################
cfgValue[CfgKey.WIFI_SSID] = "Phoenix-Photobox"
cfgValue[CfgKey.WIFI_PROTOCOL] = "WPA/WPA2"
cfgValue[CfgKey.WIFI_PASSWORD] = "09059528003481556247"
cfgValue[CfgKey.WIFI_PICTURE_NAME] = "wifi.png"
cfgValue[CfgKey.WIFI_QR_CODE_FONT] = "FreeSansBold.ttf"

#DB #############################################################################
cfgValue[CfgKey.DB_NAME] = "fotobox.db"

#SERVER #########################################################################
cfgValue[CfgKey.SERVER_INDEX_PAGE] = "/"
cfgValue[CfgKey.SERVER_INDEX_PAGE_SHOW_ALL_PICTURES] = False
cfgValue[CfgKey.SERVER_DOWNLOAD_PICTURE_PAGE] = "/downloadpage"
cfgValue[CfgKey.SERVER_DOWNLOAD_PICTURE] = "/downloadimage"
cfgValue[CfgKey.SERVER_RANDOM_URLIDS] = "/pictureuris"
cfgValue[CfgKey.SERVER_PRINT_PICTURE_PAGE] = "/print"
cfgValue[CfgKey.SERVER_PRINT_INFORMATION_REST] = "/printinformation"
cfgValue[CfgKey.SERVER_PRINT_REST_INFORMATION_INTERVALL] = 5000
cfgValue[CfgKey.SERVER_PRINT_START_PRINT_REST] = "/startprinting"
cfgValue[CfgKey.SERVER_UPLOAD_PICTURE] = "/upload"
cfgValue[CfgKey.SERVER_DISPLAY_UPLOAD_PICTURE] = "/display"
cfgValue[CfgKey.SERVER_UPLOAD_SUCCESS_PICTURE] = "/success"
cfgValue[CfgKey.SERVER_IP] = "photobox"
cfgValue[CfgKey.SERVER_PORT] = "5000"
cfgValue[CfgKey.SERVER_GETPICTUREURLIDS_NUMBER] = 10
cfgValue[CfgKey.SERVER_GETPICTUREURLIDS_THRASHOLD] = 3

#Printer #########################################################################################
cfgValue[CfgKey.PRINTER_IS_ACTIVE] = True
cfgValue[CfgKey.PRINTER_IS_ACTIVE_WEB]=False
cfgValue[CfgKey.PRINTER_SELECTED] = None
cfgValue[CfgKey.PRINTER_PAPER_SIZE] = (148,100)
cfgValue[CfgKey.PRINTER_PAPER_FORMAT] = "Postcard.Fullbleed"
cfgValue[CfgKey.PRINTER_MAX_PRINTING_ORDER] = 5

#GREENSCREEN #########################################################################################
cfgValue[CfgKey.GREENSCREEN_IS_ACTIVE] = False
cfgValue[CfgKey.GREENSCREEN_MAX_COLOR_RANGE_HINT] = 20
cfgValue[CfgKey.GREENSCREEN_MIN_HSV_GUI_COLOR] = "120;204;20"
cfgValue[CfgKey.GREENSCREEN_MAX_HSV_GUI_COLOR] = "136;255;52"
cfgValue[CfgKey.GREENSCREEN_AVERAGE_HSV_GUI_COLOR] = "129;241;32"
cfgValue[CfgKey.GREENSCREEN_MIN_HSV_CV2_COLOR] = "50;150;40"
cfgValue[CfgKey.GREENSCREEN_MAX_HSV_CV2_COLOR] = "80;255;150"
cfgValue[CfgKey.GREENSCREEN_AVERAGE_HSV_CV2_COLOR] = "64;240;23"
cfgValue[CfgKey.GREENSCREEN_FOLDER] = "greenscreen"
cfgValue[CfgKey.GREENSCREEN_BACKGROUND_FOLDER] = "backgrounds"
cfgValue[CfgKey.GREENSCREEN_TEMP_FOLDER] = "temp"
cfgValue[CfgKey.GREENSCREEN_CUSTOM_BACKGROUND_FOLDER] = "custom"
cfgValue[CfgKey.GREENSCREEN_CUSTOM_BACKGROUND_PREVIEW_FILENAME] = "preview"

#DIASHOW CLIENT #################################################################
cfgValue[CfgKey.DIASHOW_CLIENT_IS_ACTIVE] = True
cfgValue[CfgKey.DIASHOW_CLIENT_PICTURE_MAIN_FOLDER] = "Diashow/"
cfgValue[CfgKey.DIASHOW_CLIENT_PICTURE_CONFIG_FILE] = "config.txt"
cfgValue[CfgKey.DIASHOW_CLIENT_PICTURE_SOURCE_FOLDER] = "pictures/"
cfgValue[CfgKey.DIASHOW_CLIENT_PICTURE_FRAME_PICTURE] = "frame.png"
cfgValue[CfgKey.DIASHOW_CLIENT_PICTURE_SHOW_NEW_PICTURE_INTERVAL] =  int(10000)
cfgValue[CfgKey.DIASHOW_CLIENT_PICTURE_UPDATE_PICTURE_SOURCE_INTERVAL] = int(10*60000)
cfgValue[CfgKey.DIASHOW_CLIENT_PICTURE_UPDATE_PICTURE_SOURCE_INTERVAL_INITIAL] = 10000

# FOTOBOX #######################################################################

cfgValue[CfgKey.IS_PI] = False                      #Changeable -> True when RasPi
cfgValue[CfgKey.USE_PI_CAMERA] = None               #Changeable -> True or False
cfgValue[CfgKey.APPLICATION_CURSOR_HINT] = False    #Changeable -> True when RasPi
cfgValue[CfgKey.USED_CAMERA_INDEX] = 0
#https://picamera.readthedocs.io/en/release-1.10/fov.html
#(1296,730) / (640,480) / (1920,1080), (1280, 720)
cfgValue[CfgKey.PI_CAMERA_VIDEO_RESOLUTION] = (1280,720)
cfgValue[CfgKey.PI_CAMERA_VIDEO_FPS] = 25
# cfgValue[CfgKey.PI_CAMERA_PHOTO_RESOLUTION] = (1920,1080)
cfgValue[CfgKey.PI_CAMERA_PHOTO_RESOLUTION] = (3840,2160)
cfgValue[CfgKey.PI_CAMERA_STATIC_BRIGHTNESS] = False
cfgValue[CfgKey.PI_CAMERA_STATIC_BRIGHTNESS_STATIC_VALUE] = 50
cfgValue[CfgKey.PI_CAMERA_STATIC_BRIGHTNESS_AWB_GAIN_RED] = 2.5
cfgValue[CfgKey.PI_CAMERA_STATIC_BRIGHTNESS_AWB_GAIN_BLUE] = 2.5
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
cfgValue[CfgKey.PAGE_SYSTEMPICTUREMANAGER_FUNNY_PICTURE_SOURCE] = "Resources/PageCapturePhoto/funnyPicturesUrl.txt"
cfgValue[CfgKey.PAGE_SYSTEMPICTUREMANAGER_FUNNY_PICTURE_SOURCE_SUCCESS_DOWNLOAD] = "Resources/PageCapturePhoto/funnyPicturesUrlDownloaded.txt"
cfgValue[CfgKey.PAGE_SYSTEMPICTUREMANAGER_LOADINGGIFS_PICTURE_SOURCE] = "Resources/PageCapturePhoto/LoadingGifUrl.txt"
cfgValue[CfgKey.PAGE_SYSTEMPICTUREMANAGER_LOADINGGIFS_PICTURE_SOURCE_SUCCESS_DOWNLOAD] = "Resources/PageCapturePhoto/LoadingGifUrlDownload.txt"

#PageTitlePicture.py
cfgValue[CfgKey.PAGE_TITLEPICTURE_BUTTON_BACKGROUND_COLOR] = 'yellow'
        #Quellen: mouth smile
cfgValue[CfgKey.PAGE_TITLEPICTURE_BUTTON_IMAGE_FOLDER] = 'Resources/PageTitlePicture/Smiley'
cfgValue[CfgKey.PAGE_TITLEPICTURE_BACKGROUND_IMAGE] = 'Resources/PageTitlePicture/background.png'

#PageCountdown.py
cfgValue[CfgKey.PAGE_CAMERAPREVIEW_COUNDOWN_IMAGE_FOLDER] = 'Resources/PageCameraPreview/CountDown'
cfgValue[CfgKey.PAGE_CAMERAPREVIEW_COUNTER_PERIOD_LENGTH] = 1000
cfgValue[CfgKey.PAGE_CAMERAPREVIEW_COUNTER_START_VALUE] = 6

#PageCaoturePhoto.py
cfgValue[CfgKey.PAGE_CAPTUREPHOTO_LAST_IMAGE_FOLDER] = 'Resources/PageCapturePhoto/FunnyPictures'
cfgValue[CfgKey.PAGE_CAPTUREPHOTO_LOADING_GIF_FOLDER] = 'Resources/PageCapturePhoto/LoadingGif'
cfgValue[CfgKey.PAGE_CAPTUREPHOTO_TIMER_PERIOD_LENGTH] = 250
cfgValue[CfgKey.PAGE_CAPTUREPHOTO_TIMER_START_VALUE] = 4
cfgValue[CfgKey.PAGE_CAPTUREPHOTO_TIMER_CAPTUREPHOTO_VALUE] = 4

#PagePictureEdit.py
cfgValue[CfgKey.PAGE_PICTUREEDIT_FINISHED_BUTTON_ICON_DIR] = "Resources/PagePictureEdit/Icon/finish_icon.png"
cfgValue[CfgKey.PAGE_PICTUREEDIT_NEWPICTURE_BUTTON_ICON_DIR] = "Resources/PagePictureEdit/Icon/newPhoto_icon.png"
cfgValue[CfgKey.PAGE_PICTUREEDIT_PRINT_BUTTON_ICON_DIR] = "Resources/PagePictureEdit/Icon/print_icon.png"
cfgValue[CfgKey.PAGE_PICTUREEDIT_PRINT_BUTTON_DISABLED_ICON_DIR] = "Resources/PagePictureEdit/Icon/print_icon_disable.png"
cfgValue[CfgKey.PAGE_PICTUREEDIT_DOWNLOAD_BUTTON_ICON_DIR] = "Resources/PagePictureEdit/Icon/download_icon.png"
cfgValue[CfgKey.PAGE_PICTUREEDIT_HELP_BUTTON_ICON_DIR] = "Resources/PagePictureEdit/Icon/help_icon.png"
# 300000 = 5 minutes
cfgValue[CfgKey.PAGE_PICTUREEDIT_SPACE_AUTO_FORWARD_WAIT_TIME] = 5*60000

#PagePrint.py
cfgValue[CfgKey.PAGE_PRINT_STATUS_UPDATE_PERIOD] = 1000

#PageGreenscreenSelectBackround
cfgValue[CfgKey.PAGE_GREENSCREEN_SELECT_BACKGROUND_ROTATE_LEFT_ICON] = "Resources/PageGreenscreenSelectBackground/Icon/pictureLeft.png"
cfgValue[CfgKey.PAGE_GREENSCREEN_SELECT_BACKGROUND_ROTATE_RIGHT_ICON] = "Resources/PageGreenscreenSelectBackground/Icon/pictureRight.png"

###########################################################
class TextKey(enum.Enum):

    #Webserver
    WEB_PRINT_STATUS_IN_PRINTING = 3000
    WEB_PRINT_STATUS_NO_MORE_COPY = 3001
    WEB_PRINT_STATUS_READY = 3007
    WEB_UPLOAD_BACKGROUND_ERROR_NO_PICTURE_SELECTED = 3002
    WEB_UPLOAD_BACKGROUND_ERROR_WRONG_TYPE = 3003
    WEB_UPLOAD_BACKGROUND_SUCCESS = 3004
    WEB_UPLOAD_BACKGROUND_SUCCESS_HINT_CUSTOMBACKGROUND = 3005
    WEB_UPLOAD_BACKGROUND_SUCCESS_HINT_DEFAULTBACKGROUND = 3006

    #PageSystemPictureManager.py
    PAGE_SYSTEMPICTUREMANAGER_TITLE = 60
    PAGE_SYSTEMPICTUREMANAGER_NEXTBUTTON = 61
    PAGE_SYSTEMPICTUREMANAGER_FUNNY_TITEL = 66
    PAGE_SYSTEMPICTUREMANAGER_SOURCELABEL = 64
    PAGE_SYSTEMPICTUREMANAGER_TARGETLABEL = 65
    PAGE_SYSTEMPICTUREMANAGER_DELETEBUTTON = 62
    PAGE_SYSTEMPICTUREMANAGER_UPDATEBUTTON = 63
    PAGE_SYSTEMPICTUREMANAGER_SUCCESSFULL = 67
    PAGE_SYSTEMPICTUREMANAGER_LOADINGGIFS_TITEL = 68

    #PageHints.py
    PAGE_HINTS_TITLE=40
    PAGE_HINTS_ESCAPE_HINT=41
    PAGE_HINTS_RECONFIG_HINT=53
    PAGE_HINTS_NO_CAMERA_WARN=42
    PAGE_HINTS_NO_SELECTED_CAMERA_WARN=44
    PAGE_HINTS_SELECTED_CAMERA_HINT=45
    PAGE_HINTS_SELECTED_PICAMERA_HINT=51
    PAGE_HINTS_NO_PICTURES_FOUND_WARN=46
    PAGE_HINTS_NEXTBUTTON = 43
    PAGE_HINTS_PICTURE_MANAGER_BUTTON = 50
    PAGE_HINTS_PRINTER_STATUS_LABEL=52

    #PageConfig.py
    PAGE_CONFIG_TITLE=1020
    PAGE_CONFIG_NEXTBUTTON=1021
    PAGE_CONFIG_BACKBUTTON=1022
    PAGE_CONFIG_MAIN_SAVE_DIR_TITLE=1023
    PAGE_CONFIG_PROJECT_NAME_TITLE=1024
    PAGE_CONFIG_CAMERA_TITLE=1050
    PAGE_CONFIG_CAMERA_CALIBRATION_BUTTON=1025
    PAGE_CONFIG_CAMERA_STATIC_BRIGHTNESS_TITLE=1051
    PAGE_CONFIG_CAMERA_STATIC_BRIGHTNESS_VALUE_TITLE=1056
    PAGE_CONFIG_CAMERA_STATIC_BRIGHTNESS_VALUE_STATIC=1052
    PAGE_CONFIG_CAMERA_STATIC_BRIGHTNESS_VALUE_DYNAMIC=1053
    PAGE_CONFIG_CAMERA_BRIGHTNESS_GAIN_RED=1054
    PAGE_CONFIG_CAMERA_BRIGHTNESS_GAIN_BLUE=1055
    PAGE_CONFIG_SERVER_IPANDPORT_TITLE=1026
    PAGE_CONFIG_WIFI_TITLE=1027
    PAGE_CONFIG_WIFI_PICTURE_BUTTON=1028
    PAGE_CONFIG_SERVER_TITLE=1060
    PAGE_CONFIG_SERVER_SHOW_ALL_PICTURES_ON_INDEX = 1061
    PAGE_CONFIG_PRINTER_TITLE=1029
    PAGE_CONFIG_SERVICE_STATUS=1030
    PAGE_CONFIG_AKTIVATE=1031
    PAGE_CONFIG_INAKTIVATE=1032
    PAGE_CONFIG_SERVICE_PRINTER_WEB=1033
    PAGE_CONFIG_PRINTER_SELECT_LABEL=1035
    PAGE_CONFIG_PRINTER_POWER_ON_HINT=1036
    PAGE_CONFIG_PRINTER_PAPER_FORMAT_LABEL=1037
    PAGE_CONFIG_GREENSCREEN_TITLE=1040
    PAGE_CONFIG_GREENSCREEN_COLOR_PICER_BUTTON=1041
    PAGE_CONFIG_GREENSCREEN_AVERAGE_COLOR_LABEL=1042

    #PageGeenscreenColorPicker.py
    PAGE_GREENSCREEN_COLOR_PICKER_TITLE=4000
    PAGE_GREENSCREEN_COLOR_PICKER_CAPTURE_PHOTO_BUTTON = 4001
    PAGE_GREENSCREEN_COLOR_PICKER_HINT_OK=4002
    PAGE_GREENSCREEN_COLOR_PICKER_HINT_FAILED=4003
    PAGE_GREENSCREEN_COLOR_PICKER_SAVE_BUTTON = 4004
    PAGE_GREENSCREEN_COLOR_PICKER_TOLERANCE_BUTTON = 4005
    PAGE_GREENSCREEN_COLOR_PICKER_SAVE_SUCCESS_BUTTON = 4006

    #PageGreenscreenToleranceConfig.py
    PAGE_GREENSCREEN_TOLERANCE_CONFIG_TITLE=4500
    PAGE_GREENSCREEN_TOLERANCE_CONFIG_SAVE_AND_BACK_BUTTON = 4504
    PAGE_GREENSCREEN_TOLERANCE_CONFIG_BACK_BUTTON = 4501

    #PageGreenscreenSelectBackround.py
    PAGE_GREENSCREEN_SELECT_BACKGROUND_TITLE = 6000
    PAGE_GREENSCREEN_SELECT_BACKGROUND_OWN_BACKGROUND_BUTTON = 6001
    PAGE_GREENSCREEN_SELECT_BACKGROUND_BACK_BUTTON = 6002

    #PageGreenscreenUploadBackground.py
    PAGE_GREENSCREEN_UPLOAD_BACKGROUND_TITLE = 8000
    PAGE_GREENSCREEN_UPLOAD_BACKGROUND_BACK_BUTTON = 8001
    PAGE_GREENSCREEN_UPLOAD_BACKGROUND_WIFI_TITLE = 8002

    #PageGreenscreenConnectWithWifi
    PAGE_GREENSCREEN_CONNECT_WIFI_TITLE = 8010
    PAGE_GREENSCREEN_CONNECT_WIFI_REQUIREMENT = 8011
    PAGE_GREENSCREEN_CONNECT_WIFI_STEP1 = 8012
    PAGE_GREENSCREEN_CONNECT_WIFI_STEP2 = 8013
    PAGE_GREENSCREEN_CONNECT_WIFI_STEP3 = 8014
    PAGE_GREENSCREEN_CONNECT_WIFI_STEP4 = 8015
    PAGE_GREENSCREEN_CONNECT_WIFI_STEP5 = 8016
    PAGE_GREENSCREEN_CONNECT_WIFI_STEP6 = 8018
    PAGE_GREENSCREEN_CONNECT_WIFI_BACK_BUTTON = 8017

    #PageReconfig.py
    PAGE_RECONFIG_TITLE=2020
    PAGE_RECONFIG_BACKBUTTON=2021
    PAGE_RECONFIG_LOAD_GREENSCREEN_BACKGROUND=2022
    PAGE_RECONFIG_WAS_LOADED_GREENSCREEN_BACKGROUND = 2023
    PAGE_RECONFIG_UPLOAD_DEFAULT_GREENSCREEN_BACKGROUNDS=2024

    #PageCloseConfirm.py
    PAGE_CLOSECONFIRM_TITLE = 30
    PAGE_CLOSECONFIRM_TEXT = 31
    PAGE_CLOSECONFIRM_YES = 32
    PAGE_CLOSECONFIRM_NO = 33

    #PageDownloadPicture.py
    PAGE_DOWNLOADPICTURE_TITLE = 100
    PAGE_DOWNLOADPICTURE_BACKBUTTON = 101

    #PageConnectWithWifi
    PAGE_DOWNLOADPICTURE_WIFI_TITLE = 102
    PAGE_CONNECT_WITH_WIFI_REQUIREMENT = 125
    PAGE_CONNECT_WITH_WIFI_STEP1 = 126
    PAGE_CONNECT_WITH_WIFI_STEP2 = 127
    PAGE_CONNECT_WITH_WIFI_STEP3 = 128
    PAGE_CONNECT_WITH_WIFI_STEP4 = 129
    PAGE_CONNECT_WITH_WIFI_STEP5 = 130

    #PagePrint.py
    PAGE_PRINT_TITLE = 150
    PAGE_PRINT_BACKBUTTON=151
    PAGE_PRINT_PRINTBUTTON=152
    PAGE_PRINT_PRINTBUTTON_DISABLED=153
    PAGE_PRINT_HINT_PRINT=154
    PAGE_PRINT_HINT_IN_PRINT=155
    PAGE_PRINT_HINT_STATUS_LABEL=156
    PAGE_PRINT_HINT_TOO_MANY_ORDER=157

    #PrintService
    PRINT_SERVICE_EMPTY_INK=200
    PRINT_SERVICE_EMPTY_PAPER=201
    PRINT_SERVICE_MISSING_PAPER_CONTAINER=206
    PRINT_SERVICE_PRINTER_READY=203
    PRINT_SERVICE_PRINTER_NOT_EXIST=204
    PRINT_SERVICE_ERROR=205
    PRINT_SERVICE_ERROR_INSTRUCTION=207

    #PageConfig.py
    PAGE_HELP_TITLE = 10001
    PAGE_HELP_GENERAL_DESCRIPTION = 10004
    PAGE_HELP_PRINT_DESCRIPTION = 10002
    PAGE_HELP_DOWNLOAD_DESCRIPTION = 10005
    PAGE_HELP_NEW_PICTURE_DESCRIPTION = 10006
    PAGE_HELP_FINISHED_DESCRIPTION = 10007
    PAGE_HELP_BACKBUTTON=10003

    #QR-CODE
    QR_CODE_WIFI_NAME = 3201
    QR_CODE_WIFI_PASSWORD = 3202

textValue={}

#Webserver
textValue[TextKey.WEB_PRINT_STATUS_IN_PRINTING] = "Druckauftrag gestartet"
textValue[TextKey.WEB_PRINT_STATUS_READY] = "Du kannst maximal %s Kopien drucken."
textValue[TextKey.WEB_PRINT_STATUS_NO_MORE_COPY] = "Leider kannst du keine weiteren Kopien drucken."
textValue[TextKey.WEB_UPLOAD_BACKGROUND_ERROR_NO_PICTURE_SELECTED] = "Es wurde kein Bild ausgewählt!"
textValue[TextKey.WEB_UPLOAD_BACKGROUND_ERROR_WRONG_TYPE] = "Nur folgende Dateien sind erlaubt -> png, jpg, jpeg"
textValue[TextKey.WEB_UPLOAD_BACKGROUND_SUCCESS] = "Der Hintergrund wurde erfolgreich geladen."
textValue[TextKey.WEB_UPLOAD_BACKGROUND_SUCCESS_HINT_CUSTOMBACKGROUND] = "Bitte drücken sie auf der Fotobox auf 'Übernehmen'"
textValue[TextKey.WEB_UPLOAD_BACKGROUND_SUCCESS_HINT_DEFAULTBACKGROUND] = "Sie können weitere Bilder hochladen. Einfach ein weiteres Bild auswählen und über 'An die Fotobox senden' hochladen."

#PageSystemPictureManager.py
textValue[TextKey.PAGE_SYSTEMPICTUREMANAGER_TITLE] = "Systembilder Bearbeiten"
textValue[TextKey.PAGE_SYSTEMPICTUREMANAGER_NEXTBUTTON] = "Zurück zu den Hinweisen"
textValue[TextKey.PAGE_SYSTEMPICTUREMANAGER_FUNNY_TITEL] = "Lustige Bilder"
textValue[TextKey.PAGE_SYSTEMPICTUREMANAGER_LOADINGGIFS_TITEL] = "Lustige Ladegifs"
textValue[TextKey.PAGE_SYSTEMPICTUREMANAGER_SOURCELABEL] = "Quell-URLs:"
textValue[TextKey.PAGE_SYSTEMPICTUREMANAGER_TARGETLABEL] = "Ziel-Ordner:"
textValue[TextKey.PAGE_SYSTEMPICTUREMANAGER_DELETEBUTTON] = "Bilder löschen"
textValue[TextKey.PAGE_SYSTEMPICTUREMANAGER_UPDATEBUTTON] = "Bilder herunterladen"
textValue[TextKey.PAGE_SYSTEMPICTUREMANAGER_SUCCESSFULL] = "OK"

#PageHints
textValue[TextKey.PAGE_HINTS_NEXTBUTTON] = "Weiter"
textValue[TextKey.PAGE_HINTS_PICTURE_MANAGER_BUTTON] = "Systembilder bearbeiten"
textValue[TextKey.PAGE_HINTS_TITLE] = "Hinweise:"
textValue[TextKey.PAGE_HINTS_ESCAPE_HINT] = "- Um das Programm verlassen zu können, muss 'ESC' gedrückt werden."
textValue[TextKey.PAGE_HINTS_RECONFIG_HINT] = "- Um im Betrieb den Drucker zu deaktivieren, muss auf der Titelseite (die mit dem Mund) die Taste '1' gedrückt werden. Von dort aus gelangt man auf eine weitere Konfigurationsseite."
textValue[TextKey.PAGE_HINTS_NO_CAMERA_WARN] = "- Fehler: Es wurde keine Kamera gefunden! Bitte schließen sie eine Kamera an und starten Sie die Anwendung neu!"
textValue[TextKey.PAGE_HINTS_NO_SELECTED_CAMERA_WARN] = "- Fehler: Die ausgewählte Kamera ist nicht verfügbar. Schließen Sie bitte die Kammera an oder korrigieren Sie den Index in Config.py->"+CfgKey.USED_CAMERA_INDEX.name+". Bitte schließen Sie die Software!"
textValue[TextKey.PAGE_HINTS_SELECTED_CAMERA_HINT] = "- Die Kamera kann über den Index 0-n in Config.py->"+CfgKey.USED_CAMERA_INDEX.name+" ausgewählt werden. Folgende Kamera wird verwendet: Index=%s | Name=%s | Beschreibung=%s."
textValue[TextKey.PAGE_HINTS_SELECTED_PICAMERA_HINT] = "- Verwendet wird die Kamera: Pi-Camera"
textValue[TextKey.PAGE_HINTS_NO_PICTURES_FOUND_WARN] = "- Fehler: Bitte erstellen sie folgenden Ordner und hinterlegen Sie mindestens ein Bild: '%s' ! Bitte schließen Sie die Software oder laden sie die Bilder über den Button '"+textValue[TextKey.PAGE_HINTS_PICTURE_MANAGER_BUTTON]+"' herunter!"
textValue[TextKey.PAGE_HINTS_PRINTER_STATUS_LABEL] = "- Druckerstatus: "


#PageConfig
textValue[TextKey.PAGE_CONFIG_TITLE] = "Konfigurationen"
textValue[TextKey.PAGE_CONFIG_NEXTBUTTON] = "Fotobox starten"
textValue[TextKey.PAGE_CONFIG_BACKBUTTON] = "Zurück"
textValue[TextKey.PAGE_CONFIG_MAIN_SAVE_DIR_TITLE] = "Speicherort:"
textValue[TextKey.PAGE_CONFIG_PROJECT_NAME_TITLE] = "Projektname:"
textValue[TextKey.PAGE_CONFIG_CAMERA_TITLE] = "Kamera:"
textValue[TextKey.PAGE_CONFIG_CAMERA_CALIBRATION_BUTTON] = "Kamera kalibrieren"
textValue[TextKey.PAGE_CONFIG_CAMERA_STATIC_BRIGHTNESS_TITLE] = "Helligkeit:"
textValue[TextKey.PAGE_CONFIG_CAMERA_STATIC_BRIGHTNESS_VALUE_TITLE] = "Helligkeitswert:(0-100)"
textValue[TextKey.PAGE_CONFIG_CAMERA_STATIC_BRIGHTNESS_VALUE_STATIC] = "statisch"
textValue[TextKey.PAGE_CONFIG_CAMERA_STATIC_BRIGHTNESS_VALUE_DYNAMIC] = "dynamisch"
textValue[TextKey.PAGE_CONFIG_CAMERA_BRIGHTNESS_GAIN_RED] = "Gain Rot (0.0-8.0):"
textValue[TextKey.PAGE_CONFIG_CAMERA_BRIGHTNESS_GAIN_BLUE] = "Gain Blau (0.0-8.0):"
textValue[TextKey.PAGE_CONFIG_SERVER_IPANDPORT_TITLE] = "Server IP und Port"
textValue[TextKey.PAGE_CONFIG_WIFI_TITLE] = "WIFI"
textValue[TextKey.PAGE_CONFIG_WIFI_PICTURE_BUTTON] = "QR-Code speichern"
textValue[TextKey.PAGE_CONFIG_SERVER_TITLE] = "Web-Server"
textValue[TextKey.PAGE_CONFIG_SERVER_SHOW_ALL_PICTURES_ON_INDEX] = "Indexseite: Zeige alle Bilder:"
textValue[TextKey.PAGE_CONFIG_PRINTER_TITLE] = "Drucker"
textValue[TextKey.PAGE_CONFIG_SERVICE_STATUS] = "Aktiviert: "
textValue[TextKey.PAGE_CONFIG_AKTIVATE] = "Ja"
textValue[TextKey.PAGE_CONFIG_INAKTIVATE] = "Nein"
textValue[TextKey.PAGE_CONFIG_SERVICE_PRINTER_WEB] = "Aktiviert WEB: "
textValue[TextKey.PAGE_CONFIG_PRINTER_SELECT_LABEL] = "Verwendeter Drucker:"
textValue[TextKey.PAGE_CONFIG_PRINTER_POWER_ON_HINT] = "Hinweis: Bitte schalten sie den Drucker ein!"
textValue[TextKey.PAGE_CONFIG_PRINTER_PAPER_FORMAT_LABEL] = "Papierformat: "
textValue[TextKey.PAGE_CONFIG_GREENSCREEN_TITLE] = "Greenscreen: "
textValue[TextKey.PAGE_CONFIG_GREENSCREEN_COLOR_PICER_BUTTON] = "Setze Greenscreenfarbe"
textValue[TextKey.PAGE_CONFIG_GREENSCREEN_AVERAGE_COLOR_LABEL]= "Greenscreenfarbe: "

#GreenscreenColorPicker.py
textValue[TextKey.PAGE_GREENSCREEN_COLOR_PICKER_TITLE]= "Farben des Greenscreens kalibrieren (HSV)"
textValue[TextKey.PAGE_GREENSCREEN_COLOR_PICKER_CAPTURE_PHOTO_BUTTON] = "Neues Foto"
textValue[TextKey.PAGE_GREENSCREEN_COLOR_PICKER_HINT_OK]= "Der Hintergrund ist OK."
textValue[TextKey.PAGE_GREENSCREEN_COLOR_PICKER_HINT_FAILED]= "Der Hintergrund ist nicht einheitlich genug!"
textValue[TextKey.PAGE_GREENSCREEN_COLOR_PICKER_SAVE_BUTTON] = "Übernehmen"
textValue[TextKey.PAGE_GREENSCREEN_COLOR_PICKER_SAVE_SUCCESS_BUTTON] = "Wurde übernommen"
textValue[TextKey.PAGE_GREENSCREEN_COLOR_PICKER_TOLERANCE_BUTTON] = "Toleranzen anpassen"

#PageGreenscreenToleranceConfig.py
textValue[TextKey.PAGE_GREENSCREEN_TOLERANCE_CONFIG_TITLE] = "Greenscreen Toleranz Config (H | S | V)"
textValue[TextKey.PAGE_GREENSCREEN_TOLERANCE_CONFIG_SAVE_AND_BACK_BUTTON] = "Übernehmen"
textValue[TextKey.PAGE_GREENSCREEN_TOLERANCE_CONFIG_BACK_BUTTON] = "Zurück"

#PageGreenscreenSelectBackround.py
textValue[TextKey.PAGE_GREENSCREEN_SELECT_BACKGROUND_TITLE] = "Hintergrund auswählen"
textValue[TextKey.PAGE_GREENSCREEN_SELECT_BACKGROUND_OWN_BACKGROUND_BUTTON] = "Eigenen Hintergrund"
textValue[TextKey.PAGE_GREENSCREEN_SELECT_BACKGROUND_BACK_BUTTON] = "Zurück"

#PageGreenscreenUploadBackground.py
textValue[TextKey.PAGE_GREENSCREEN_UPLOAD_BACKGROUND_TITLE] = "Hintergund auf Fotobox transferieren"
textValue[TextKey.PAGE_GREENSCREEN_UPLOAD_BACKGROUND_BACK_BUTTON] = "Übernehmen"
textValue[TextKey.PAGE_GREENSCREEN_UPLOAD_BACKGROUND_WIFI_TITLE] = "Mit der Fotobox verbinden (W-LAN)"

#PageGreenscreenConnectWithWifi
textValue[TextKey.PAGE_GREENSCREEN_CONNECT_WIFI_TITLE] = "Was soll ich tun?"
textValue[TextKey.PAGE_GREENSCREEN_CONNECT_WIFI_REQUIREMENT] = "Voraussetzung:\n\tVoraussetzung ist ein Smartphone mit QR-Code-Scanner.\n\tModerne Smartphones haben ein Scanner in der Kamera-App."
textValue[TextKey.PAGE_GREENSCREEN_CONNECT_WIFI_STEP1] = "Schritt 1:\n\tMit dem W-LAN der Fotobox verbinden.\n\tDie Zugangsdaten finden sie im folgeden QR-Code:"
textValue[TextKey.PAGE_GREENSCREEN_CONNECT_WIFI_STEP2] = "Schritt 2:\n\tUm Fehler zu vermeiden, sollten die mobilen Daten auf dem Smartphone\n\tdeaktivert werden. Die mobilen Daten können wieder aktiviert werden,\n\twenn nicht mehr auf die Fotobox zugegriffen werden soll."
textValue[TextKey.PAGE_GREENSCREEN_CONNECT_WIFI_STEP3] = "Schritt 3:\n\tAuf 'Zurück' klicken."
textValue[TextKey.PAGE_GREENSCREEN_CONNECT_WIFI_STEP4] = "Schritt 4:\n\tDen QR-Code mit dem QR-Code-Scanner oder Kamera-App abfotografieren.\n\tEs sollte sich der Browser öffnen, in dem der Hintergrund hochgeladen werden kann."
textValue[TextKey.PAGE_GREENSCREEN_CONNECT_WIFI_STEP5] = "Schritt 5:\n\tAuf 'Datei auswählen' klicken, ein Bild auswählen und danach auf\n\t'An die Fotobox senden' klicken. Dieser Schritt kann beliebig oft wiederholt werden."
textValue[TextKey.PAGE_GREENSCREEN_CONNECT_WIFI_STEP6] = "Schritt 6:\n\tAuf der Fotobox auf 'Übernehmen' klicken."
textValue[TextKey.PAGE_GREENSCREEN_CONNECT_WIFI_BACK_BUTTON] = "Zurück"

#PageReconfig.py
textValue[TextKey.PAGE_RECONFIG_TITLE] = "Konfiguration"
textValue[TextKey.PAGE_RECONFIG_BACKBUTTON] = "Zurück"
textValue[TextKey.PAGE_RECONFIG_LOAD_GREENSCREEN_BACKGROUND] = "Greenscreenhintergründe laden"
textValue[TextKey.PAGE_RECONFIG_WAS_LOADED_GREENSCREEN_BACKGROUND] = "Greenscreenhintergründe sind geladen"
textValue[TextKey.PAGE_RECONFIG_UPLOAD_DEFAULT_GREENSCREEN_BACKGROUNDS] = "Hintergründe hochladen"

#PageCloseConfirm
textValue[TextKey.PAGE_CLOSECONFIRM_TITLE] = "Anwendung schließen?"
textValue[TextKey.PAGE_CLOSECONFIRM_TEXT] = "Soll die Anwendung geschlossen werden?"
textValue[TextKey.PAGE_CLOSECONFIRM_YES] = "Ja"
textValue[TextKey.PAGE_CLOSECONFIRM_NO] = "Nein"

#PageDownloadPicture.py
textValue[TextKey.PAGE_DOWNLOADPICTURE_TITLE] = "Bild auf Handy transferieren"
textValue[TextKey.PAGE_DOWNLOADPICTURE_BACKBUTTON] = "Zurück"

#PageConnectWithWifi
textValue[TextKey.PAGE_DOWNLOADPICTURE_WIFI_TITLE] = "Was soll ich tun?"
textValue[TextKey.PAGE_CONNECT_WITH_WIFI_REQUIREMENT] = "Voraussetzung:\n\tVoraussetzung ist ein Smartphone mit QR-Code-Scanner.\n\tModerne Smartphones haben ein Scanner in der Kamera-App."
textValue[TextKey.PAGE_CONNECT_WITH_WIFI_STEP1] = "Schritt 1:\n\tMit dem W-LAN der Fotobox verbinden.\n\tDie Zugangsdaten finden sie im folgeden QR-Code:"
textValue[TextKey.PAGE_CONNECT_WITH_WIFI_STEP2] = "Schritt 2:\n\tUm Fehler zu vermeiden, sollten die mobilen Daten auf dem Smartphone\n\tdeaktivert werden. Die mobilen Daten können wieder aktiviert werden,\n\twenn nicht mehr auf die Fotobox zugegriffen werden soll."
textValue[TextKey.PAGE_CONNECT_WITH_WIFI_STEP3] = "Schritt 3:\n\tAuf 'Zurück' klicken."
textValue[TextKey.PAGE_CONNECT_WITH_WIFI_STEP4] = "Schritt 4:\n\tDen QR-Code mit dem QR-Code-Scanner oder Kamera-App abfotografieren.\n\tEs sollte sich der Browser öffnen, in dem dein Bild zu sehen ist."
textValue[TextKey.PAGE_CONNECT_WITH_WIFI_STEP5] = "Schritt 5:\n\tKlick einfach auf dein Bild, um es herunterzuladen."

#PagePrint.py
textValue[TextKey.PAGE_PRINT_TITLE] = "Bild Drucken"
textValue[TextKey.PAGE_PRINT_BACKBUTTON] = "Zurück"
textValue[TextKey.PAGE_PRINT_PRINTBUTTON] = "Drucken"
textValue[TextKey.PAGE_PRINT_PRINTBUTTON_DISABLED] = "Wird Gedruckt..."
textValue[TextKey.PAGE_PRINT_HINT_PRINT] = "- Über den Button 'Drucken' kann ein Bild ausgedruckt werden. Erst nach dem Drucken kann ein weiterer Druckprozess gestartet werden. Der Druck sollte innerhalb von 2 Minuten gestartet werden. Wenn der Druck nicht gestartet wurde dann holen Sie einen Verantwortlichen.\n- Sie können auch über den Dowloadbereich, im nachhinein die Bilder ausdrucken."
textValue[TextKey.PAGE_PRINT_HINT_IN_PRINT] = "- Der Druck wurde gestartet! Wenn der Drucker nach 2 Minuten nicht gestartet ist, dann wenden Sie sich bitte an den Verantwortlichen."
textValue[TextKey.PAGE_PRINT_HINT_STATUS_LABEL] = "- Druckerstatus: "
textValue[TextKey.PAGE_PRINT_HINT_TOO_MANY_ORDER] = "- Die maximale Anzahl an Ausdrucken wurde erreicht. Dieses Bild darf kein weiteres mal ausgedruckt werden!"

#PrintService
textValue[TextKey.PRINT_SERVICE_PRINTER_READY]= "Bereit"
textValue[TextKey.PRINT_SERVICE_ERROR]= "<span style='color:#ff0000;'>Unbekannter Fehler!</span>"
textValue[TextKey.PRINT_SERVICE_PRINTER_NOT_EXIST]= "<span style='color:#ff0000;'>Drucker konnte nicht gefunden werden!</span>"
textValue[TextKey.PRINT_SERVICE_EMPTY_INK]="<span style='color:#ff0000;'>Farbe ist alle!</span>"
textValue[TextKey.PRINT_SERVICE_EMPTY_PAPER]="<span style='color:#ff0000;'>Kein Papier mehr vorhanden!</span>"
textValue[TextKey.PRINT_SERVICE_MISSING_PAPER_CONTAINER]="<span style='color:#ff0000;'>Der Papierbehälter ist nicht eingesteckt!</span>"
textValue[TextKey.PRINT_SERVICE_ERROR_INSTRUCTION] = "Bitte holen Sie einen Verantwortlichen."

#PageConfig.py
textValue[TextKey.PAGE_HELP_TITLE] = "Hilfe"
textValue[TextKey.PAGE_HELP_GENERAL_DESCRIPTION] = "Hier wird kurz beschrieben, was du mit der Fotobox machen kannst.\nWenn du ein Foto machen willst, dann achte bitte darauf, dass das Licht eingeschaltet ist.\nDas Licht wird über die weißen Schalter, hinten rechts, eingeschaltet."
textValue[TextKey.PAGE_HELP_PRINT_DESCRIPTION] = "Über diesen Button kannst du dein Bild ausdrucken.\nMaximal können %s Kopien erstellt werden.\nBitte beachte, dass der Drucker beim drucken mehrmals das Papier einzieht.\nWarte geduldig, bis der Drucker fertig ist, bevor du das Foto entnimmst."
textValue[TextKey.PAGE_HELP_DOWNLOAD_DESCRIPTION] = "Über den Button kannst du dein Bild auf dein Handy laden.\nVoraussetzung ist, dass du mit dem WLAN der Fotobox verbunden bist.\nDie Zugangsdaten findest du ebenfalls hinter dieser Schalltfläche.\nDie Bilder können nur im W-LAN der Fotobox heruntergeladen werden\nund nicht nachträglich über das Internet. Softwareseitig benötigst du\nein QR-Code-Scanner. Bei modernen Smartphones ist ein solcher Scanner\nin der Kamera-App integriert."
textValue[TextKey.PAGE_HELP_NEW_PICTURE_DESCRIPTION] = "Wenn dir dein Bild nicht gefällt, kannst\ndu über diesen Button direkt ein neues Bild schießen."
textValue[TextKey.PAGE_HELP_FINISHED_DESCRIPTION] = "Wenn du fertig bist, dann kommst du über diese Schaltfläche auf die Startseite.\nSo kann kein Fremder dein Foto auf sein Smartphone laden oder ausdrucken."
textValue[TextKey.PAGE_HELP_BACKBUTTON] = "Zurück"

#QR-CODE
textValue[TextKey.QR_CODE_WIFI_NAME] = "Name: "
textValue[TextKey.QR_CODE_WIFI_PASSWORD] = "Passwort: "