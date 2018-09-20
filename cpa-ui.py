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

import traceback
from datetime import datetime
from validate_email import validate_email

from ModelToPDFConverter import ModelToPDFConverter
from InvoiceModel import InvoiceModel

from tkinter import *
fields = "Invoice Number", "Invoice Name", "Invoice Date", "Job Date", "Job Location", "Client Name", "Client Email", "Client Phone", "Photographer Name", "Event Hours", "Portrait Hours", "Photobooth Hours"

class DocumentUI:
	def __init__(self):
		self.root = Tk()
		self.root.title("Kyeongjoo SUcks")

		self.modelToPDFConverter = ModelToPDFConverter()

		self.entries = self.create_form(fields)

		self.invoice = IntVar(value=1)
		self.release = IntVar(value=1)
		self.whatToExpect = IntVar(value=1)

		self.invoiceButton = Checkbutton(self.root, text="Invoice", 
			variable=self.invoice, onvalue=1, offvalue=0)
		self.releaseButton = Checkbutton(self.root, text="Release", 
			variable=self.release, onvalue=1, offvalue=0)
		self.whatToExpectButton = Checkbutton(self.root, text="What to Expect", 
			variable=self.whatToExpect, onvalue=1, offvalue=0)
		self.invoiceButton.pack(side=LEFT, padx=5, pady=5)
		self.releaseButton.pack(side=LEFT, padx=5, pady=5)
		self.whatToExpectButton.pack(side=LEFT, padx=5, pady=5)

		self.goButton = Button(self.root, text="Go", command=self.generate_docs)
		self.goButton.pack(side=LEFT, padx=5, pady=5)
		self.quitButton = Button(self.root, text="Quit", command=self.destructor)
		self.quitButton.pack(side=RIGHT, padx=5, pady=5)

		self.root.mainloop()

	def destructor(self):
		logging.info("Shutting down...")
		self.root.destroy()

	def create_form(self, fields):
		entries = []
		for field in fields:
			row = Frame(self.root)
			label = Label(row, width=15, text=field, anchor="w")
			entry = Entry(row)
			if field == 'Invoice Date':
				entry.insert(0, datetime.now().strftime("%m/%d/%Y"))
			row.pack(side=TOP, fill=X, padx=5, pady=5)
			label.pack(side=LEFT)
			entry.pack(side=RIGHT, expand=YES, fill=X)
			entries.append((field, entry))

		return entries

	def generate_docs(self):
		logger.info("Go button pressed...")
		model = InvoiceModel()

		for entry in self.entries:
			setattr(model, self.toCamelCase(entry[0]), entry[1].get())

		eventQuantity = self.entries[9][1].get()
		portraitQuantity = self.entries[10][1].get()
		photoboothQuantity = self.entries[11][1].get()

		if eventQuantity != "0" and eventQuantity != "":
			model.addItem("Event Photography", int(eventQuantity))

		if portraitQuantity != "0" and portraitQuantity != "": 
			model.addItem("Portraiture", int(portraitQuantity))

		if photoboothQuantity != "0" and photoboothQuantity != "": 
			model.addItem("Photobooth", int(photoboothQuantity))

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

	def toCamelCase(self, string): 
		result = "".join(x for x in string.title() if not x.isspace()) 
		return result[0].lower() + result[1:]

if __name__ == "__main__":
	logger.info("Starting program")
	try:
		main = DocumentUI()
	except:
		fatalMessage = traceback.format_exc()
		logger.error("[Unknown Error] %s", fatalMessage)
		logger.info("Ending Script Unsuccessfully")

