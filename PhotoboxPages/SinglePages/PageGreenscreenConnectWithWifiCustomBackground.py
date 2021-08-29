from PyQt5.QtCore import QSize

from PhotoboxPages import AllPages
from PhotoboxPages.SinglePages.abstract.PageGreenscreenConnectWithWifiAbstract import \
    PageGreenscreenConnectWithWifiAbstract
from Services import GlobalPagesVariableService


class PageGreenscreenConnectWithWifiCustomBackground(PageGreenscreenConnectWithWifiAbstract):
    def __init__(self, pages : AllPages, windowsize:QSize, globalVariable:GlobalPagesVariableService):
        super().__init__(pages,windowsize,globalVariable)
        self.windowsize = windowsize
        self.globalVariable = globalVariable