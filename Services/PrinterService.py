import cups

class PrinterService():
    def __init__(self):
        self.conn = cups.Connection()
        self.printers = self.conn.getPrinters()


        '''classes = conn.getClasses()

        
        print(classes)

        print("######################################")

        for printer in printers:
            print (printer)
            for printerInformation in printers[printer]:
                print(printerInformation+ " = "+str(printers[printer][printerInformation]))
            print("\n")

        print("########################################")

        for name, queue in printers.items ():
            print(name)
            print(queue)
            print("###")'''

    def getPrinters(self):
        return self.printers.keys()


#printer = PrintService()