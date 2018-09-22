import pdfkit
import logging
import re
import subprocess
import os

class ModelToPDFConverter(object):

    def __init__(self):
        self.logger = logging.getLogger('main')
        self.css = 'document_templates/bootstrap.min.css'

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

        with open('document_templates/invoice_template.txt', 'r') as f:
            output = f.read().format(str(model.invoiceNumber), 
                                    str(model.clientName), 
                                    str(model.clientPhone), 
                                    str(model.clientEmail), 
                                    str(model.invoiceName), 
                                    str(model.invoiceDate), 
                                    str(model.photographerName), 
                                    str(model.totalAmount),
                                    str(invoiceItems),
                                    str(model.totalAmount)
                                    )
            filename = '{}_{}_Invoice.pdf'.format(model.invoiceNumber, re.sub('[^ a-zA-Z0-9]', '', model.invoiceName))
            pdfkit.from_string(output, filename, options=options, css=self.css)
            
            if not os.path.isdir('output'):
                subprocess.call(['mkdir', './output'])
            subprocess.call(['mv', filename, './output/{}'.format(filename)])

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

        with open('document_templates/release_template.txt', 'r') as f:
            output = f.read().format(model.invoiceName, model.jobDate)
            filename = '{}_{}_Release.pdf'.format(model.invoiceNumber, re.sub('[^ a-zA-Z0-9]', '', model.invoiceName))
            pdfkit.from_string(output, filename, options=options, css=self.css)

            if not os.path.isdir('output'):
                subprocess.call(['mkdir', './output'])
            subprocess.call(['mv', filename, './output/{}'.format(filename)])

        self.logger.info('Created {}'.format(filename))


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

        with open('document_templates/what_to_expect_template.txt', 'r') as f:
            output = f.read().format(str(model.jobDate),
                                    str(model.jobLocation), 
                                    str(model.clientName),
                                    str(model.photographerName),
                                    str(model.totalAmount))
            filename = '{}_{}_WhatToExpect.pdf'.format(model.invoiceNumber, re.sub('[^ a-zA-Z0-9]', '', model.invoiceName))
            pdfkit.from_string(output, filename, options=options, css=self.css)

            if not os.path.isdir('output'):
                subprocess.call(['mkdir', './output'])
            subprocess.call(['mv', filename, './output/{}'.format(filename)])

        self.logger.info('Created {}'.format(filename))


