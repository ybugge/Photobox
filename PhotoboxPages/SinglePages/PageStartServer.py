from PyQt5.QtCore import QSize

from PhotoboxPages.AllPages import AllPages
from PhotoboxPages.Page import Page
from Services.GlobalPagesVariableService import GlobalPagesVariableService
from Services.Greenscreen.GreenscreenBackgroundService import GreenscreenBackgroundService
from Services.WebServerExecThread import WebServerExecThread


class PageStartServer(Page):
    def __init__(self, pages : AllPages,windowSize:QSize, server:WebServerExecThread, globalPagesVariable:GlobalPagesVariableService):
        super().__init__(pages,windowSize)
        self.server = server
        self.globalPagesVariable = globalPagesVariable

    def executeBefore(self):
        self.nextPageEvent()

    def executeAfter(self):
        self.globalPagesVariable.setUserMode(True)
        self.server.start()