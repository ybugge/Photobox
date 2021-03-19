from PyQt5.QtCore import QSize

from PhotoboxPages.AllPages import AllPages
from PhotoboxPages.Page import Page
from Services.WebServerExecThread import WebServerExecThread


class PageStartServer(Page):
    def __init__(self, pages : AllPages,windowSize:QSize, server:WebServerExecThread):
        super().__init__(pages,windowSize)
        self.server = server

    def executeBefore(self):
        self.nextPageEvent()

    def executeAfter(self):
        self.server.start()