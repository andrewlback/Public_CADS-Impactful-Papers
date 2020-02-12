# Documentation For Impactful Paper Project

# Table of Contents
1. [Download the papers from asq.org](#Downloadthepapersfromasq.org)
2. [Convert the pdf files obtained to text files](#Convertthepdffiles)
3. [Combine the data from web of science](#Combinethedata)
4. [Match the text files to the titles of the files listed in Web of Science](#titlesAndFiles)

# 1. Download the papers from asq.org <a name="Downloadthepapersfromasq.org"></a>
This step was done using the browser autmoation tool Selenium. To protect the web site from crawlers, it was decided to not include the code for this step.

# 2. Convert the pdf files obtained to text files <a name="Convertthepdffiles"></a>
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
papers_directory = ''

# Specify the output directory for the text versions of the papers
#output_directory = 'C:/Users/Me/Desktop/text'
output_directory = ''

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

# 3. Combine the data from web of science <a name="Combinethedata"></a>
Next, the data from web of science was colleted. The data from web of science came from two places. One data set was obtained from creating a citation report from the Journal of Quality technology and the other was from exporting data from Web of Science. The citation report was given in three excel files that were combined with cleanWebOfScience.py which is shown below. 

```python 

import pandas as pd
import os
import re


self_path = os.path.dirname(os.path.realpath(__file__))

self_path = re.sub(r'\\','/',self_path)
os.chdir(self_path)

excel_files = []
files_to_join = []
for file in os.listdir():
    if file.endswith(".xls"):
        excel_files.append(file)

for excel_file in excel_files:
    excel_file = pd.read_excel(excel_file, index=False)
    files_to_join.append(excel_file)

merged_frames = pd.concat(files_to_join)
merged_frames = merged_frames.sort_values(by=['Publication Year'])
merged_frames = merged_frames.reset_index()
merged_frames.to_csv(self_path+'/combinedWebOfScience.csv')
```

Then the export data was downloaded from web of science. This data was also downloaded as three excel files and were combined using CleanWebOfScienceExport.py. The code used to combine these files is shown below. 

```python
import pandas as pd

data1 = pd.read_table('savedrecs.txt')
data2 = pd.read_table('savedrecs (1).txt') 
data3 = pd.read_table('savedrecs (2).txt')

combinedData = [data1, data2, data3]
combinedData = pd.concat(combinedData,ignore_index=True)

FieldTags = pd.read_csv('FieldTags.csv', header=None, index_col=0, squeeze=True).to_dict()

combinedData = combinedData.rename(columns=FieldTags)
combinedData = combinedData.dropna(axis=1,how='all')
combinedData = combinedData.drop(columns=['ZR','ZS'])
combinedData = combinedData.sort_values(by=['Title'])
combinedData = combinedData.reset_index(drop=True)
combinedData.to_csv('combinedDataExport.csv')
```

Then the data from the citation report and the export were combined using CombinedExportAndCitation.py. The code for this file is shown below. 

```python
import pandas as pd

data1 = pd.read_csv('combinedDataCitationReport.csv',index_col=0)
data2 = pd.read_csv('combinedDataExport.csv',index_col=0)

combinedData = [data1, data2]
combinedData = pd.concat(combinedData, axis=1, sort=False)
combinedData = combinedData.dropna(axis=1,how='all')
combinedData.to_csv('combinedCitationExport.csv')
```  
# 4. Match the text files to the titles of the files listed in Web of Science <a name="titlesAndFiles"></a>

When the papers were downloaded from the Journal of Quality Technology, their convention was to name the file as the title of the publication with an added .pdf. Once these were converted to text, the name would be changed to the title of the publication with .txt added. Unfortunately, the titles expressed throught the file name were not the same as the names listed in the Web of Science data. Usually they would be off by a letter or two or a number would be spelled versus expressed in characters. Because of this, a Python script called findPapersNotInWebOfScience.py was written to match the titles from the files to the titles given by the Web of Science data. This script works by using fuzzy logic, which compares the difference between the Web of Science titles and the file titles and computes a simularity percentage. The code then matches each Web of Science title with a file title according to the highest simularity score. The code is shown below. 

```python
import os
import io
import pandas as pd
from fuzzywuzzy import fuzz,process
from tqdm import tqdm

#Specify the directory for the papers
input_directory = ''
os.chdir('')

# Find all of the files in the input directory
files = os.listdir(input_directory)
files.sort()

# Load the names of the titles from pandas
df = pd.read_csv('combinedCitationExport.csv')
titles = df['Title']
titles
titles = titles.tolist()
titles.sort()


matching_files=[]
scores = []
no_matches = []
used_files = []

for index in tqdm(range(len(titles))):
    max_score = -1
    title = titles[index].lower()
    for file in files:
        lowered_file = file.lower()
        score = fuzz.ratio(title,lowered_file)
        if score > max_score:
            max_score = score
            matching_file = file
    if max_score>=65:
        matching_files.append(matching_file)
        scores.append(max_score)
        used_files.append(matching_file)
    else:
        matching_files.append('No match')
        scores.append(max_score)
        no_matches.append(titles[index])

matching_files = pd.DataFrame(matching_files, columns=['matching titles'])
scores = pd.DataFrame(scores, columns=['scores'])
titles = df['Title']
files = pd.DataFrame(files,columns=['files'])
no_matches = pd.DataFrame(no_matches, columns=['Title that didnt match'])

data = pd.concat([files, titles,matching_files,scores, no_matches], axis=1, sort=False)
data.to_csv('TitlesAndFiles.csv')

titles_and_files = pd.read_csv('TitlesAndFiles.csv')
web_of_science_titles = titles_and_files['matching titles']
web_of_science_titles = web_of_science_titles.tolist()
web_of_science_titles = [x for x in web_of_science_titles if str(x) != 'nan']
print(len(web_of_science_titles))

# Find all of the files in the input directory
os.chdir('')
files = os.listdir()
filesdf = pd.DataFrame(files)

for file in files:
    if file in web_of_science_titles:
        from shutil import copyfile
        copyfile(''+file, ''+file)


# Show titles and files together
test = pd.DataFrame(web_of_science_titles)
alldf = pd.concat([test,filesdf],axis=1)
alldf.to_csv('alltestdf.csv')

for title in web_of_science_titles:
    if title not in files:
        print(str(title) + ' not in folder')

```
