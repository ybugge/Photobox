from Pages.AllPages import AllPages
from Pages.Page import Page
from Services.WebServerExecThread import WebServerExecThread


class PageStartServer(Page):
    def __init__(self, pages : AllPages, server:WebServerExecThread):
        super().__init__(pages)
        self.server = server

    def executeBefore(self):
        self.nextPageEvent()

    def executeAfter(self):
        self.server.start()