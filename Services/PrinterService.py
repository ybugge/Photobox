from Services.CfgService import CfgService
from Services.GlobalPagesVariableService import GlobalPagesVariableService
from Services.ShottedPictureService import ShottedPictureService
from config.Config import CfgKey
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
            #size = [1280,720]
            size = [1066,720]
            im = Image.new('RGB', (size[0], size[1]))
            im.paste(Image.open(picturePath).resize((size[0], size[1])), ( 0, 0, size[0], size[1]))
            # Save data to a temporary file
            output = mktemp(prefix='jpg')
            im.save(output, format='jpeg')
            # Send the picture to the printer
            #print_id = self.conn.printFile(printer, output, "Photo Booth", {'fit-to-page':'True'})
            print_id = self.conn.printFile(printer, output, "Photo Booth", {})
            # Wait until the job finishes
            unlink(output)
            print("Bild wurde dem Drucker gesenden: ")
            return print_id
        else:
            print("Drucker nicht gefunden oder nicht aktiviert!")
            return None

    def _findPrinterByString(self,printerAsString):
        for printerKey in self.getPrinters():
            if printerAsString == str(printerKey):
                return printerKey
        return None