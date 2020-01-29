# Documentation For Impactful Paper Project
# 1. Download the papers from asq.org
This step was done using the browser autmoation tool Selenium. To protect the web site from crawlers, it was decided to not include the code for this step.

# 2. Convert the pdf files obtained to text files
Based on example code listed on [stackoverflow](https://stackoverflow.com/questions/39854841/pdfminer-python-3-5), a python definition was created to convert pdf files to text files. This function is class pdfReader.py. The code for this definition is show below. This code will take in a pdf file and convert it to a text file.

```python
from pdfminer.pdfparser import PDFParser
from pdfminer.pdfdocument import PDFDocument
from pdfminer.pdfpage import PDFPage
from pdfminer.pdfpage import PDFTextExtractionNotAllowed
from pdfminer.pdfinterp import PDFResourceManager
from pdfminer.pdfinterp import PDFPageInterpreter
from pdfminer.pdfdevice import PDFDevice
import io
try:
    from StringIO import StringIO ## for Python 2
except ImportError:
    from io import StringIO ## for Python 3
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfpage import PDFPage

def pdfReader(fname, outputFile, pages=None):

    if not pages:
        pagenums = set()
    else:
        pagenums = set(pages)

    output = StringIO()
    manager = PDFResourceManager()
    converter = TextConverter(manager, output, laparams=LAParams())
    interpreter = PDFPageInterpreter(manager, converter)

    infile = open(fname, 'rb')
    for page in PDFPage.get_pages(infile, pagenums):
        interpreter.process_page(page)
    infile.close()
    converter.close()
    text = output.getvalue()
    output.close

    try:
        with open(outputFile+'.txt', 'w',encoding="utf-8") as f:
            f.write(text)
    except:
        print('Could not convert '+outputFile+'.txt'+ ' to text'
```

The script all_pdf_to_text.py was used to convert all of the papers to text from pdf using pdfReader.py. This code will take all of the pdf files in the directory that this file is stored in and convert them to text. The code for this file is shown below. 

```python
import os
from pdfReader import pdfReader
from tqdm import tqdm_gui
from tqdm import tqdm
import io

#Specify the directory for the papers
#papers_directory = 'C:/Users/Me/Desktop/pdf'
papers_directory = 'C:/Users/backal/Desktop/pdf'

# Specify the output directory for the text versions of the papers
#output_directory = 'C:/Users/Me/Desktop/text'
output_directory = 'C:/Users/backal/Desktop/text'

# Find all of the files in the input directory
files = os.listdir(papers_directory)

# Find all of the files in the output directory
output_files = os.listdir(output_directory)

# Initialize a list for pdf files
pdf_files = []
output_pdf_files = []

# Find only the pdfs in the directory
for file in files:
    if file.endswith('.pdf'):
        pdf_files.append(file)

# Find only the text files in the directory
for file in output_files:
    if file.endswith('.txt'):
        output_pdf_files.append(file)

# Convert the pdf files into text files and save to the output folder
for index in tqdm(range(len(pdf_files))):
        if (os.path.splitext(pdf_files[index])[0]+'.txt') not in output_pdf_files:
                output = output_directory+'/'+ os.path.splitext(pdf_files[index])[0]
                input_file = papers_directory + '/' + pdf_files[index]
                pdfReader(input_file, output)
        else:
                print('The file ' + pdf_files[index] + ' was already converted to a .txt file')
```