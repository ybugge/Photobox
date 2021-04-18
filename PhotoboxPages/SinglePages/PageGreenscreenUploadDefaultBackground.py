from PyQt5.QtCore import QSize

from PhotoboxPages.AllPages import AllPages
from PhotoboxPages.SinglePages.abstract.PageGreenscreenUploadBackgroundAbstract import \
    PageGreenscreenUploadBackgroundAbstract
from Services.GlobalPagesVariableService import GlobalPagesVariableService


class PageGreenscreenUploadDefaultBackground(PageGreenscreenUploadBackgroundAbstract):
    def __init__(self, pages : AllPages, windowsize:QSize, globalVariable:GlobalPagesVariableService):
        super().__init__(pages,windowsize,globalVariable)
        self.windowsize = windowsize
        self.globalVariable = globalVariable

    def executeBefore(self):
        self.executeBeforeDefault()

    def executeAfter(self):
        self.executeAfterDefault()