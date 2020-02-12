import os
from pdfReader import pdfReader
from tqdm import tqdm_gui
from tqdm import tqdm
import io

#Specify the directory for the papers
papers_directory = 'C:/Users/Me/Desktop/pdf'
#papers_directory = 'C:/Users/backal/Desktop/pdf'

# Specify the output directory for the text versions of the papers
output_directory = 'C:/Users/Me/Desktop/text'
#output_directory = 'C:/Users/backal/Desktop/text'

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


