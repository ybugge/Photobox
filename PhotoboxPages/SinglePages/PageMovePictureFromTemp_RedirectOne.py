from PyQt5.QtCore import QSize

from PhotoboxPages.AllPages import AllPages
from PhotoboxPages.SinglePages.abstract.PageMovePictureFromTemp import PageMovePictureFromTemp
from Services.GlobalPagesVariableService import GlobalPagesVariableService
from Services.Greenscreen.GreenscreenBackgroundService import GreenscreenBackgroundService


class PageMovePictureFromTemp_RedirectOne(PageMovePictureFromTemp):
    def __init__(self, pages : AllPages,windowSize:QSize,globalVariable:GlobalPagesVariableService):
        super().__init__(pages,windowSize,globalVariable)

    def executeAfter(self):
        GreenscreenBackgroundService(self.globalVariable).cleanCustomBackground()