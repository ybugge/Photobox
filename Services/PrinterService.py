import math

from Services.CfgService import CfgService
from Services.GlobalPagesVariableService import GlobalPagesVariableService
from Services.PrinterDbService import PrinterDbService
from Services.PrintingLimitationDbService import PrintingLimitationDbService
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


    def printingPosible(self):
        return len(self.printers) > 0

    def getPrinters(self):
        return self.printers.keys()

    def printLokal(self,globalVariable:GlobalPagesVariableService):
        self.printWeb(globalVariable.getPictureSubName(),ShottedPictureService.getTempPicturePath())

    def isStatusInPrintLokal(self, globalVariable:GlobalPagesVariableService):
        return self.isStatusInPrintWeb(globalVariable.getPictureSubName())

    def printWeb(self,pictureName:str,picturePath:str):

        if self.hasTooManyPrintingOrderWeb(pictureName):
            print("Das maximale orderlimit des Bildes wurde erreicht! Bild wird nicht ausgedruckt. Picture")
            return

        if not self.isStatusInPrintWeb(pictureName):
            printId = self._print(picturePath)
            if printId != None:
                self.updateOrderNumber(pictureName)
                printerService = PrinterDbService()
                printerService.addRungingJob(pictureName,printId)
                printerService.close()


    def isStatusInPrintWeb(self, pictureName:str):
        printerService = PrinterDbService()
        jobId = printerService.getFirstJob(pictureName)
        if jobId != None and self.conn.getJobs().get(jobId, None) != None:
            status = True
        else:
            status = False
            if jobId != None:
                printerService.setJobFinished(pictureName)
        printerService.close()
        self._cleanDB()
        return status

    def _cleanDB(self):
        printerService = PrinterDbService()
        for job in printerService.getAllJobs():
            if self.conn.getJobs().get(job[0], None) == None:
                printerService.setJobFinished(job[1])
        printerService.close()

    #https://stackoverflow.com/questions/39117196/raspberry-pi-photobooth-printing
    def _print(self,picturePath:str):
        printer = self._findPrinterByString(CfgService.get(CfgKey.PRINTER_SELECTED))
        if CfgService.get(CfgKey.PRINTER_IS_ACTIVE) and printer != None:
            pictureWithNewSizw = self.getPrintablePicture(picturePath)
            # Save data to a temporary file
            output = mktemp(prefix='jpg')
            pictureWithNewSizw.save(output, format='jpeg')
            # Send the picture to the printer | Options: https://www.cups.org/doc/options.html#OPTIONS / https://stuff.mit.edu/afs/athena/astaff/project/opssrc/cups/cups-1.4.4/doc/help/options.html
            paperFormat = CfgService.get(CfgKey.PRINTER_PAPER_FORMAT)
            print_id = self.conn.printFile(printer, output, "", {"landscape":"True","media":paperFormat})

            unlink(output)
            print("Bild wurde dem Drucker gesendet!")
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

    def hasTooManyPrintingOrderLokal(self,globalVariable:GlobalPagesVariableService):
        return self.hasTooManyPrintingOrderWeb(globalVariable.getPictureSubName())

    def hasTooManyPrintingOrderWeb(self, pictureName:str):
        printingLimitationDbService = PrintingLimitationDbService()
        tooManyPrintingOrder = not printingLimitationDbService.allowToPrint(pictureName)
        printingLimitationDbService.close()
        return tooManyPrintingOrder

    def updateOrderNumber(self,pictureName):
        printingLimitationDbService = PrintingLimitationDbService()
        printingLimitationDbService.setNewPrintOrder(pictureName)
        printingLimitationDbService.close()

