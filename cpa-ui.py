import logging

# Set up logging
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

import config

import os
import smtplib
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart

import traceback
from datetime import datetime

import gspread
from oauth2client.service_account import ServiceAccountCredentials
from validate_email import validate_email

from ModelToPDFConverter import ModelToPDFConverter
from InvoiceModel import InvoiceModel

from tkinter import *

class DocumentUI:
	def __init__(self):
		self.root = Tk()
		self.root.title("CPA is lit")

		# Object to handel PDF creation
		self.modelToPDFConverter = ModelToPDFConverter()

		# Defines form fields
		self.fields = ["Invoice Number", "Invoice Name", "Invoice Date", "Job Date", 
		"Job Location", "Client Name", "Client Email", "Client Phone", 
		"Photographer Name", "Event Hours", "Portrait Hours", "Photobooth Hours"]

		# Build text form
		self.entries = self.create_form(self.fields)

		# Checkboxes to specify which documents to generate, default all checked
		self.checkboxes = Frame(self.root)

		self.invoice = IntVar(value=1)
		self.release = IntVar(value=1)
		self.whatToExpect = IntVar(value=1)
		self.invoiceButton = Checkbutton(self.checkboxes, text="Invoice", 
			variable=self.invoice, onvalue=1, offvalue=0)
		self.releaseButton = Checkbutton(self.checkboxes, text="Release", 
			variable=self.release, onvalue=1, offvalue=0)
		self.whatToExpectButton = Checkbutton(self.checkboxes, text="What to Expect", 
			variable=self.whatToExpect, onvalue=1, offvalue=0)
		self.invoiceButton.pack(side=LEFT, padx=5, pady=3)
		self.releaseButton.pack(side=LEFT, padx=5, pady=3)
		self.whatToExpectButton.pack(side=LEFT, padx=5, pady=3)
		self.checkboxes.pack()
		
		# Regular buttons: Go, Autofill, Quit
		self.regularButtons = Frame(self.root)

		self.goButton = Button(self.regularButtons, text="Go", command=self.generate_docs)
		self.autoFillButton = Button(self.regularButtons, text="AutoFill", command=self.autofill_gdrive)
		self.quitButton = Button(self.regularButtons, text="Quit", command=self.destructor)
		self.goButton.pack(side=LEFT, padx=8, pady=8)
		self.autoFillButton.pack(side=LEFT, padx=8, pady=8)
		self.quitButton.pack(side=LEFT, padx=8, pady=8)
		self.regularButtons.pack()

		self.root.mainloop()

	def destructor(self):
		logging.info("Shutting down...")
		self.root.destroy()

	def create_form(self, fields):
		entries = []
		for field in self.fields:
			row = Frame(self.root)
			label = Label(row, width=15, text=field, anchor="w")
			entry = Entry(row)
			if field == "Invoice Date":
				entry.insert(0, datetime.now().strftime("%-m/%-d/%Y"))
			row.pack(side=TOP, fill=X, padx=5, pady=5)
			label.pack(side=LEFT)
			entry.pack(side=RIGHT, expand=YES, fill=X)
			entries.append((field, entry))

		return entries

	def generate_docs(self):
		logger.info("Go button pressed...")

		# Get invoice item quantities from text fields
		eventQuantity = self.entries[9][1].get()
		portraitQuantity = self.entries[10][1].get()
		photoboothQuantity = self.entries[11][1].get()

		# Ensure at least one invoice item quantity is greater than 0
		if (eventQuantity == "0" or eventQuantity == "") \
			and (portraitQuantity == "0" or portraitQuantity == "") \
			and (photoboothQuantity == "0" or photoboothQuantity == ""):
			self.popup("All invoice items are 0.", "Error")

		model = InvoiceModel()

		# Set invoice model attributes from text fields
		for entry in self.entries:
			setattr(model, self.toCamelCase(entry[0]), entry[1].get())

		# Add invoice items to model
		if eventQuantity != "0" and eventQuantity != "":
			model.addItem("Event Photography", int(eventQuantity))

		if portraitQuantity != "0" and portraitQuantity != "": 
			model.addItem("Portraiture", int(portraitQuantity))

		if photoboothQuantity != "0" and photoboothQuantity != "": 
			model.addItem("Photobooth", int(photoboothQuantity))

		# Generate documents according to checkboxes
		try:
			if self.invoice.get():
				self.modelToPDFConverter.createInvoice(model)	
			if self.release.get():
				self.modelToPDFConverter.createRelease(model)
			if self.whatToExpect.get():
				self.modelToPDFConverter.createWhatToExpect(model)
		except:
			errorMsg = traceback.format_exc()
			logger.error("[PDF Conversion Error] %s", errorMsg)

	# Autofills form using values from google drive spreadsheet
	def autofill_gdrive(self):
		if not self.entries[0][1].get().isdigit():
			self.popup("Please enter a valid invoice number before using AutoFill.", "Error")
			return
		try:
			# Google Drive authorization
			scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
			credentials = ServiceAccountCredentials.from_json_keyfile_name(config.CREDENTIALS_PATH, scope)
			gc = gspread.authorize(credentials)

			worksheet = gc.open_by_url(config.SPREADSHEET_URL).sheet1
			invoiceNumber = int(self.entries[0][1].get())
			invoiceNumbers = worksheet.col_values(1)
			invoiceRow = 0

			# Search for row in spreadsheet corresponding to given invoice
			for i in range(len(invoiceNumbers)):
				if i != 0 and int(invoiceNumbers[i]) == invoiceNumber:
					invoiceRow = int(i) + 1

			if invoiceRow == 0:
				# Invoice number not found in gdrive
				self.popup("Invoice number not found on jobs log.", "Error")

			self.set_text(self.entries[1][1], worksheet.cell(invoiceRow,8).value)
			self.set_text(self.entries[3][1], worksheet.cell(invoiceRow,7).value)
			self.set_text(self.entries[4][1], worksheet.cell(invoiceRow,10).value)
			self.set_text(self.entries[5][1], worksheet.cell(invoiceRow,11).value)
			self.set_text(self.entries[6][1], worksheet.cell(invoiceRow,12).value)
			self.set_text(self.entries[7][1], worksheet.cell(invoiceRow,13).value)
			self.set_text(self.entries[8][1], worksheet.cell(invoiceRow,14).value)
		except:
			fatalMessage = traceback.format_exc()
			logger.error("[Google Drive AutoFill Error] %s", fatalMessage)

	# Auxillary method for autofill, sets text in a text field
	def set_text(self, entry, text):
	    entry.delete(0,END)
	    entry.insert(0,text)
	    return

	def toCamelCase(self, string): 
		result = "".join(x for x in string.title() if not x.isspace()) 
		return result[0].lower() + result[1:]

	def popup(self, text, title):
	    popup = Tk()
	    popup.wm_title(title)
	    message = Label(popup, text=text)
	    message.pack(side="top", fill="x", padx=10, pady=5)
	    okButton = Button(popup, text="Ok senpai", command = popup.destroy)
	    okButton.pack(pady=5)
	    popup.mainloop()

if __name__ == "__main__":
	logger.info("Starting program")
	try:
		main = DocumentUI()
	except:
		fatalMessage = traceback.format_exc()
		logger.error("[Unknown Error] %s", fatalMessage)
		logger.info("Ending Script Unsuccessfully")

