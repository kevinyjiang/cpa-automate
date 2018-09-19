class InvoiceModel(object):

    def __init__(self):
        self.invoiceNumber = 0
        self.invoiceName = ""
        self.invoiceDate = ""
        self.clientName = ""
        self.clientEmail = ""
        self.clientPhone = ""
        self.photographerName = ""
        self.items = []


    def __str__(self):
        return """Job Number: {},
                Invoice Name: {},
                Invoice Date: {},
                Client Contact: {}, {}, {},
                Photographer: {},
                Items: {},""".format(str(self.invoiceNumber),
                            str(self.invoiceName),
                            str(self.invoiceDate),
                            str(self.clientName),
                            str(self.clientEmail),
                            str(self.clientPhone),
                            str(self.photographerName),
                            str(self.items)
                            )