import pdfkit
import logging
import re
import subprocess
import os

import config

class ModelToPDFConverter(object):

    def __init__(self):
        self.logger = logging.getLogger("main")
        self.css = "document_templates/bootstrap.min.css"
        self.options = {
            "page-size": "Letter",
            "margin-top": "0.25in",
            "margin-right": "0.25in",
            "margin-bottom": "0.25in",
            "margin-left": "0.25in",
            "encoding": "UTF-8",
            "dpi": 1100
        }

    def createInvoice(self, model):
        self.logger.info("Creating invoice PDF...")

        invoiceItems = ""

        for item in model.items:
            invoiceItems += str(item)

        with open("document_templates/invoice_template.txt", "r") as f:
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

            self.options["dpi"] = 1100
            self.write_pdf(output, model, 'Invoice')
            
    def createRelease(self, model):
        self.logger.info("Creating release PDF...")

        with open("document_templates/release_template.txt", "r") as f:
            output = f.read().format(model.invoiceName, model.jobDate)

            self.options["dpi"] = 1400
            self.write_pdf(output, model, 'Release')

    def createWhatToExpect(self, model):
        self.logger.info("Creating What To Expect PDF...")

        with open("document_templates/what_to_expect_template.txt", "r") as f:
            output = f.read().format(str(model.jobDate),
                                    str(model.jobLocation), 
                                    str(model.clientName),
                                    str(model.photographerName),
                                    str(model.totalAmount))

            self.options["dpi"] = 1250
            self.write_pdf(output, model, 'WhatToExpect')

    def write_pdf(self, output, model, document_type):
        filename = "{}_{}_{}.pdf".format(model.invoiceNumber, re.sub("[^ a-zA-Z0-9]", "", model.invoiceName), document_type)
        pdfkit.from_string(output, filename, options=self.options, css=self.css)

        if not os.path.isdir(config.OUTPUT_DESTINATION):
            subprocess.call(["mkdir", config.OUTPUT_DESTINATION])
        subprocess.call(["mv", filename, "{}/{}".format(config.OUTPUT_DESTINATION, filename)])
        
        self.logger.info("Created {}".format(filename))


