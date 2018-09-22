import config

class InvoiceItemModel(object):

    def __init__(self, itemType, quantity):
        self.itemType = itemType
        self.quantity = int(quantity)
        self.unitPrice = 0

        if itemType == 'Portraiture':
            self.unitPrice = config.PORTRAIT_RATE
        else:
            self.unitPrice = config.EVENT_RATE


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