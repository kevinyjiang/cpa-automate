import logging

#Add stdout and file logging
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
	modelToPDFConverter = ModelToPDFConverter()

	invoiceNumber = input("Invoice #:")
	while not invoiceNumber.isdigit():
		invoiceNumber = input("Please enter an integer:")

	invoiceName = input("Invoice name:")
	invoiceDate = datetime.now().strftime("%m/%d/%Y")

	clientName = input("Client name:")
	clientEmail = input("Client email:")
	while not validate_email(clientEmail):
		clientEmail = input("Please enter a valid email:")

	clientPhone = input("Client phone:")
	photographerName = input("Photographer name:")
	eventQuantity = input("Event quantity:")
	portraitQuantity = input("Portrait quantity:")
	photoboothQuantity = input("Photobooth quantity:") 

	model = InvoiceModel()
	model.invoiceNumber = invoiceNumber
	model.invoiceName = invoiceName
	model.invoiceDate = invoiceDate
	model.clientName = clientName
	model.clientEmail = clientEmail
	model.clientPhone = clientPhone
	model.photographerName = photographerName

	if int(eventQuantity):
		model.items.append(InvoiceItemModel('Event Photography', eventQuantity))

	if int(portraitQuantity): 
		model.items.append(InvoiceItemModel('Portraiture', portraitQuantity))

	if int(photoboothQuantity): 
		model.items.append(InvoiceItemModel('Photobooth', photoboothQuantity))

	modelToPDFConverter.createInvoice(model)









