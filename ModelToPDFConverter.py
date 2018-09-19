import pdfkit
import logging

class ModelToPDFConverter(object):

    def __init__(self):
        self.logger = logging.getLogger('main')
        self.css = 'templates/bootstrap.min.css'

    def createInvoice(self, model):
        self.logger.info('Creating invoice PDF...')

        options = {
            'page-size': 'Letter',
            'margin-top': '0.25in',
            'margin-right': '0.25in',
            'margin-bottom': '0.25in',
            'margin-left': '0.25in',
            'encoding': "UTF-8",
            'dpi': 1100
        }

        invoiceItems = ""

        for item in model.items:
            invoiceItems += str(item)

        with open('templates/invoice_template.txt', 'r') as f:
            output = f.read().format(str(model.invoiceName), 
                                    str(model.clientName), 
                                    str(model.clientPhone), 
                                    str(model.clientEmail), 
                                    str(model.invoiceNumber), 
                                    str(model.invoiceDate), 
                                    str(model.photographerName), 
                                    str(invoiceItems)
                                    )
            filename = '{}_{}_Invoice.pdf'.format(model.invoiceNumber, model.invoiceName.replace(' ',''))
            pdfkit.from_string(output, filename, options=options, css=self.css)

        self.logger.info('Created {}'.format(filename))

    def createRelease(self, model):
        self.logger.info('Creating release PDF...')

        options = {
            'page-size': 'Letter',
            'margin-top': '0.25in',
            'margin-right': '0.25in',
            'margin-bottom': '0.25in',
            'margin-left': '0.25in',
            'encoding': "UTF-8",
            'dpi': 1400
        }

        with open('templates/release_template.txt', 'r') as f:
            output = f.read().format(model.invoiceName, model.jobDate)
            filename = '{}_{}_Release.pdf'.format(model.invoiceNumber, model.invoiceName.replace(' ',''))
            pdfkit.from_string(output, filename, options=options, css=self.css)

        self.logger.info('Created {}'.format(filename))
"""
    def createWhatToExpect(self, model):
        self.logger.info('Creating What To Expect PDF...')

        options = {
            'page-size': 'Letter',
            'margin-top': '0.25in',
            'margin-right': '0.25in',
            'margin-bottom': '0.25in',
            'margin-left': '0.25in',
            'encoding': "UTF-8",
            'dpi': 1250
        }

        unitPrice = 0

        if model.jobType == 'Event':
            unitPrice = 100
        else:
            unitPrice = 160

        quantity = float(model.clientPaymentAmount.replace('$',''))/unitPrice

        with open('templates/what_to_expect_template.txt', 'r') as f:
            output = f.read().format(model.eventDate, unitPrice, quantity, otherFees, model.clientPaymentAmount)
            filename = '{}_{}_WhatToExpect.pdf'.format(model.jobNumber, model.eventName.replace(' ',''))
            pdfkit.from_string(release, filename, options=options, css=self.css)

        self.logger.info('Created {}'.format(filename))
"""
