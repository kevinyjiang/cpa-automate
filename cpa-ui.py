from InvoiceModel import InvoiceModel
from ModelToPDFConverter import ModelToPDFConverter

from tkinter import *
fields = 'Invoice Number', 'Invoice Name', 'Invoice Date', 'Job Date', 'Job Location', 'Client Name', 'Client Email', 'Client Phone', 'Photographer Name', 'Event Quantity', 'Portrait Quantity', 'Photobooth Quantity'

def create_form(root, fields):
	entries = []
	for field in fields:
		row = Frame(root)
		label = Label(row, width=15, text=field, anchor='w')
		entry = Entry(row)
		row.pack(side=TOP, fill=X, padx=5, pady=5)
		label.pack(side=LEFT)
		entry.pack(side=RIGHT, expand=YES, fill=X)
		entries.append((field, entry))
	return entries

def toCamelCase(string): 
	result = ''.join(x for x in string.title() if not x.isspace()) 
	return result[0].lower() + result[1:]

def generate_docs(entries, invoice, release, whatToExpect):
	modelToPDFConverter = ModelToPDFConverter()
	model = InvoiceModel()

	for entry in entries:
		setattr(model, toCamelCase(entry[0]), entry[1].get())

	eventQuantity = entries[9][1].get()
	portraitQuantity = entries[10][1].get()
	photoboothQuantity = entries[11][1].get()

	if eventQuantity != '0' and eventQuantity != '':
		model.addItem("Event Photography", int(eventQuantity))

	if portraitQuantity != '0' and portraitQuantity != '': 
		model.addItem("Portraiture", int(portraitQuantity))

	if photoboothQuantity != '0' and photoboothQuantity != '': 
		model.addItem("Photobooth", int(photoboothQuantity))

	if invoice:
		modelToPDFConverter.createInvoice(model)	
	if release:
		modelToPDFConverter.createRelease(model)
	if whatToExpect:
		modelToPDFConverter.createWhatToExpect(model)


if __name__ == "__main__":
	root = Tk()
	root.title("Kyeongjoo SUcks")

	entries = create_form(root, fields)

	invoice = IntVar(value=1)
	release = IntVar(value=1)
	whatToExpect = IntVar(value=1)

	invoiceButton = Checkbutton(root, text = "Invoice", variable = invoice, 
					onvalue = 1, offvalue = 0)
	releaseButton = Checkbutton(root, text = "Release", variable = release,
					onvalue = 1, offvalue = 0)
	whatToExpectButton = Checkbutton(root, text = "What to Expect", variable = whatToExpect,
					onvalue = 1, offvalue = 0)
	invoiceButton.pack(side=LEFT, padx=5, pady=5)
	releaseButton.pack(side=LEFT, padx=5, pady=5)
	whatToExpectButton.pack(side=LEFT, padx=5, pady=5)

	goButton = Button(root, text='Go', command=lambda: generate_docs(entries, 
		invoice.get(), release.get(), whatToExpect.get()))
	goButton.pack(side=LEFT, padx=5, pady=5)
	quitButton = Button(root, text='Quit', command=root.quit)
	quitButton.pack(side=RIGHT, padx=5, pady=5)

	root.mainloop()

