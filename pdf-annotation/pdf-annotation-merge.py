from borb.pdf import Document
from borb.pdf import Page
from borb.pdf import PDF

# Read the documents
doc_1 = None
with open(input("input file: "), "rb") as in_file_handle:
    doc_1 = PDF.loads(in_file_handle)

# Extract annotations from doc_1:
for i in range(0,30):
	annots = doc_1.get_page(i).get_annotations()
	print(">>> ", annots)
	# annots2 = doc_1.get_page(i)["Annots"]
	# print("second method:", annots2)

exit(0)

from borb.pdf import Document
from borb.pdf import Page
from borb.pdf import SingleColumnLayout
from borb.pdf import Paragraph
from borb.pdf import PDF

# Read the 1st and 2nd documents:
doc_1 = None
with open(input("input PDF file 1: "), "rb") as in_file_handle:
	doc_1 = PDF.loads(in_file_handle)

doc_2 = None
with open(input("input PDF file 2: "), "rb") as in_file_handle:
	doc_2 = PDF.loads(in_file_handle)

# Add all annotations from 1 to 2:
annots = doc_1.get_page(0).get_annotations()
doc_2.get_page(0)["Annots"] = list()
for a in annots:
	doc_2.get_page(0)["Annots"].append(a)

# Write PDF 2:
with open(input("output PDF file: "), "wb") as out_file_handle:
	PDF.dumps(out_file_handle, doc_2)

exit(0)

# create an empty Document
pdf = Document()

# add an empty Page
page = Page()
pdf.add_page(page)

# use a PageLayout (SingleColumnLayout in this case)
layout = SingleColumnLayout(page)

# add a Paragraph object
layout.add(Paragraph("Hello World!"))
	
# store the PDF
with open("output.pdf", "wb") as pdf_file_handle:
	PDF.dumps(pdf_file_handle, pdf)
