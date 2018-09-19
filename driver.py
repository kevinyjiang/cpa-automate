import logging

logger = logging.getLogger('main')
logger.setLevel(logging.DEBUG)

formatString = '%(asctime)s %(levelname)-8.8s [%(module)s] [%(funcName)s:%(lineno)4s] %(message)s'
formatter = logging.Formatter(formatString)

ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
ch.setFormatter(formatter)
logger.addHandler(ch)

fh = logging.FileHandler('log.txt')
fh.setFormatter(formatter)
logger.addHandler(fh)

import traceback
from datetime import datetime
from validate_email import validate_email

from ModelToPDFConverter import ModelToPDFConverter
from InvoiceModel import InvoiceModel
from InvoiceItemModel import InvoiceItemModel

if __name__ == '__main__':
	logger.info("Starting script")
	try:
		modelToPDFConverter = ModelToPDFConverter()

		invoiceNumber = input("Invoice #: ")
		while not invoiceNumber.isdigit():
			invoiceNumber = input("Please enter an integer: ")

		invoiceName = input("Invoice name: ")
		invoiceDate = datetime.now().strftime("%m/%d/%Y")
		jobDate = input("Job Date: ")

		clientName = input("Client name: ")
		clientEmail = input("Client email: ")
		while not validate_email(clientEmail):
			clientEmail = input("Please enter a valid email: ")

		clientPhone = input("Client phone: ")
		photographerName = input("Photographer name: ")
		eventQuantity = input("Event quantity: ")
		portraitQuantity = input("Portrait quantity: ")
		photoboothQuantity = input("Photobooth quantity: ") 

		model = InvoiceModel()
		model.invoiceNumber = invoiceNumber
		model.invoiceName = invoiceName
		model.invoiceDate = invoiceDate
		model.jobDate = jobDate
		model.clientName = clientName
		model.clientEmail = clientEmail
		model.clientPhone = clientPhone
		model.photographerName = photographerName

		if eventQuantity:
			model.items.append(InvoiceItemModel('Event Photography', eventQuantity))

		if portraitQuantity: 
			model.items.append(InvoiceItemModel('Portraiture', portraitQuantity))

		if photoboothQuantity: 
			model.items.append(InvoiceItemModel('Photobooth', photoboothQuantity))


		try:
			modelToPDFConverter.createInvoice(model)
			
			modelToPDFConverter.createRelease(model)
		except:
			errorMsg = traceback.format_exc()
			failureDao.addFailure(model, errorMsg)
			logger.error("[PDF Conversion Error] %s", errorMsg)

	except:
		fatalMessage = traceback.format_exc()
		logger.error("[Unknown Error] %s", fatalMessage)
		failureDao.sendFatalError(fatalMessage)
		logger.info("Ending Script Unsuccessfully")









