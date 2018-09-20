import logging

logger = logging.getLogger("main")
logger.setLevel(logging.DEBUG)

formatString = "%(asctime)s %(levelname)-8.8s [%(module)s] [%(funcName)s:%(lineno)4s] %(message)s"
formatter = logging.Formatter(formatString)

ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
ch.setFormatter(formatter)
logger.addHandler(ch)

fh = logging.FileHandler("log.txt")
fh.setFormatter(formatter)
logger.addHandler(fh)

import traceback
from datetime import datetime
from validate_email import validate_email

from ModelToPDFConverter import ModelToPDFConverter
from InvoiceModel import InvoiceModel

jobTypes = ["Event Photography", "Portraiture", "Photobooth"]

if __name__ == "__main__":
	logger.info("Starting script")
	try:
		modelToPDFConverter = ModelToPDFConverter()

		invoiceNumber = input("Invoice #: ")
		while not invoiceNumber.isdigit():
			invoiceNumber = input("Please enter an integer: ")

		invoiceName = input("Invoice name: ")
		invoiceDate = datetime.now().strftime("%m/%d/%Y")
		jobDate = input("Job Date: ")
		jobLocation = input("Job Location: ")

		clientName = input("Client name: ")
		clientEmail = input("Client email: ")
		while not validate_email(clientEmail):
			clientEmail = input("Please enter a valid email: ")

		clientPhone = input("Client phone: ")
		photographerName = input("Photographer name: ")
		eventQuantity = input("Event quantity: ")
		while not eventQuantity.isdigit():
			eventQuantity = input("Please enter an integer: ")

		portraitQuantity = input("Portrait quantity: ")
		while not portraitQuantity.isdigit():
			portraitQuantity = input("Please enter an integer: ")

		photoboothQuantity = input("Photobooth quantity: ")
		while not photoboothQuantity.isdigit():
			photoboothQuantity = input("Please enter an integer: ")

		model = InvoiceModel()
		model.invoiceNumber = invoiceNumber
		model.invoiceName = invoiceName
		model.invoiceDate = invoiceDate
		model.jobDate = jobDate
		model.jobLocation = jobLocation
		model.clientName = clientName
		model.clientEmail = clientEmail
		model.clientPhone = clientPhone
		model.photographerName = photographerName

		if eventQuantity != '0' and eventQuantity != '': 
			model.addItem("Event Photography", int(eventQuantity))

		if portraitQuantity != '0' and portraitQuantity != '': 
			model.addItem("Portraiture", int(portraitQuantity))

		if photoboothQuantity != '0' and photoboothQuantity != '': 
			model.addItem("Photobooth", int(photoboothQuantity))

		try:
			modelToPDFConverter.createInvoice(model)
		
			modelToPDFConverter.createRelease(model)

			modelToPDFConverter.createWhatToExpect(model)
		except:
			errorMsg = traceback.format_exc()
			logger.error("[PDF Conversion Error] %s", errorMsg)

	except:
		fatalMessage = traceback.format_exc()
		logger.error("[Unknown Error] %s", fatalMessage)
		logger.info("Ending Script Unsuccessfully")









