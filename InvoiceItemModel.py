class InvoiceItemModel(object):

    def __init__(self, itemtype, quantity):
        self.itemtype = itemtype
        self.quantity = int(quantity)
        self.unitprice = 0

        if itemtype == 'Portrait Photography':
            self.unitprice = 120
        else:
            self.unitprice = 100


    def __str__(self):
        return """<tr>
                    <td><strong>{} (1hr)</strong></td>
                    <td>{}</td>
                    <td>{}</td>
                    <td>{}</td>
                </tr>""".format(str(self.itemtype), 
                                str(self.quantity), 
                                str(self.unitprice),
                                str(self.unitprice * self.quantity))