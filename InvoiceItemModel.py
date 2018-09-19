class InvoiceItemModel(object):

    def __init__(self, itemType, quantity):
        self.itemType = itemType
        self.quantity = int(quantity)
        self.unitPrice = 0

        if itemType == 'Portraiture':
            self.unitPrice = 120
        else:
            self.unitPrice = 100


    def __str__(self):
        return """<tr>
                    <td><strong>{} (1hr)</strong></td>
                    <td>{}</td>
                    <td>${}</td>
                    <td>${}</td>
                </tr>""".format(str(self.itemType), 
                                str(self.quantity), 
                                str(self.unitPrice),
                                str(self.unitPrice * self.quantity))