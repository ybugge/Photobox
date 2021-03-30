from PyQt5.QtCore import QSize

from PhotoboxPages.AllPages import AllPages
from PhotoboxPages.Page import Page
from Services.GlobalPagesVariableService import GlobalPagesVariableService
from Services.PageDbService import PageDbSevice
from Services.ShottedPictureService import ShottedPictureService


class PageMovePictureFromTemp(Page):
    def __init__(self, pages : AllPages,windowSize:QSize,globalVariable:GlobalPagesVariableService):
        super().__init__(pages,windowSize)
        self.globalVariable = globalVariable

    def executeBefore(self):
        pictureIsUsed = self.globalVariable.isPictureUsed()
        if pictureIsUsed:
            pictureTargetPath = ShottedPictureService.saveUsedPicture(self.globalVariable.getPictureSubName())
        else:
            pictureTargetPath = ShottedPictureService.saveUnusedPicture(self.globalVariable.getPictureSubName())
        PageDbSevice.updatePicture(self.globalVariable,pictureTargetPath,pictureIsUsed)
        self.globalVariable.unlockPictureName()
        self.nextPageEvent()