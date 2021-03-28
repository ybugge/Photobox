import math

from Services.CfgService import CfgService
from Services.GlobalPagesVariableService import GlobalPagesVariableService
from Services.ShottedPictureService import ShottedPictureService
from config.Config import CfgKey, textValue, TextKey
from PIL import Image
from tempfile import mktemp
from os import unlink

try:
    import cups
    import getpass
    printer_selection_enable = True
except ImportError:
    print("Cups ist nicht installiert! Druckfunktion wird deaktiviert!")

class PrinterService():
    def __init__(self):

        try:
            self.conn = cups.Connection()
            self.printers = self.conn.getPrinters()
            cups.setUser(getpass.getuser())
        except:
            print("Drucker konnte nicht intitialisiert werden.")
            self.printers = {}
            CfgService.set(CfgKey.PRINTER_IS_ACTIVE,False)

        self.jobs = {}

    def printingPosible(self):
        return len(self.printers) > 0

    def getPrinters(self):
        return self.printers.keys()

    def printLokal(self,globalVariable:GlobalPagesVariableService):
        name = globalVariable.getPictureSubName()
        if not self.isStatusInPrintLokal(globalVariable):
            printId = self._print(ShottedPictureService.getTempPicturePath())
            if printId != None:
                self.jobs.update({name:printId})

    def isStatusInPrintLokal(self, globalVariable:GlobalPagesVariableService):
        name = globalVariable.getPictureSubName()
        if name in self.jobs:
            return self.conn.getJobs().get(self.jobs[name], None) != None
        return False

    #https://stackoverflow.com/questions/39117196/raspberry-pi-photobooth-printing
    def _print(self,picturePath:str):
        printer = self._findPrinterByString(CfgService.get(CfgKey.PRINTER_SELECTED))
        if CfgService.get(CfgKey.PRINTER_IS_ACTIVE) and printer != None:
            pictureWithNewSizw = self.getPrintablePicture(picturePath)
            # Save data to a temporary file
            output = mktemp(prefix='jpg')
            pictureWithNewSizw.save(output, format='jpeg')
            # Send the picture to the printer | Options: https://www.cups.org/doc/options.html#OPTIONS
            #print_id = self.conn.printFile(printer, output, "Photo Booth", {'fit-to-page':'True'})
            print_id = self.conn.printFile(printer, output, "Photo Booth", {"fit-to-page":"True"})

            unlink(output)
            print("Bild wurde dem Drucker gesenden: ")
            return print_id
        else:
            print("Drucker nicht gefunden oder nicht aktiviert!")
            return None



    def getPrintablePicture(self,picturePath:str):
        originalPicture = Image.open(picturePath)
        originalPicture.load()
        originalPictureSize = originalPicture.size
        newPictureSize = self.getPaperResolution(originalPictureSize)
        top = 0
        bottom = newPictureSize[1]
        left = (originalPictureSize[0] - newPictureSize[0])/2
        right = left+newPictureSize[0]
        oldRGBPicture = Image.new("RGB", originalPictureSize, (255, 255, 255))
        oldRGBPicture.paste(originalPicture)
        newRGBPicture = oldRGBPicture.crop((left, top, right, bottom))
        return newRGBPicture

    def getPaperResolution(self,originalPictureSize):
        paperSize = CfgService.get(CfgKey.PRINTER_PAPER_SIZE)
        height = originalPictureSize[1]
        width = math.ceil((height*paperSize[0])/paperSize[1])
        return (width,height)



    def _findPrinterByString(self,printerAsString):
        for printerKey in self.getPrinters():
            if printerAsString == str(printerKey):
                return printerKey
        return None

    #https://github.com/sebmueller/Photobooth/blob/master/photobooth.py
    def getPrinterStatus(self):
        printer = self._findPrinterByString(CfgService.get(CfgKey.PRINTER_SELECTED))
        if CfgService.get(CfgKey.PRINTER_IS_ACTIVE) and printer != None:
            printerstate = self.conn.getPrinterAttributes(printer, requested_attributes=["printer-state-message"])
            if str(printerstate).find("error:") > 0:
                if str(printerstate).find("06") > 0:
                    return textValue[TextKey.PRINT_SERVICE_EMPTY_INK]
                if str(printerstate).find("03") > 0:
                    return textValue[TextKey.PRINT_SERVICE_EMPTY_PAPER]
                if str(printerstate).find("02") > 0:
                    return textValue[TextKey.PRINT_SERVICE_EMPTY_PAPER]
                else:
                    return textValue[TextKey.PRINT_SERVICE_ERROR]

            return textValue[TextKey.PRINT_SERVICE_PRINTER_READY]
        else:
            return textValue[TextKey.PRINT_SERVICE_PRINTER_NOT_EXIST]
