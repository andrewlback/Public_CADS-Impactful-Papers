# Documentation For Impactful Paper Project

# Table of Contents
[Goal of Analysis](#goal)
1. [Download the papers from asq.org](#Downloadthepapersfromasq.org)
2. [Convert the pdf files obtained to text files](#Convertthepdffiles)
3. [Combine the data from web of science](#Combinethedata)
4. [Match the text files to the titles of the files listed in Web of Science](#titlesAndFiles)
5. [Find the Keywords in the abstract of the papers and the number of figures and tables](#findText)
6. [Remove one instance of bad data](#baddata)
7. [Combined the data from the keywords, the number of figures and tables, and the Web of Science data](#combine)
8. [Additional Cleaning on the Data Set](#clean)
    - [Remove Years not needed on the data set](#clean-1)
    - [Remove columns with digital ID's](#clean-2)
    - [Remove columns from previous analysis](#clean-3)
    - [Create a column for number of pages](#clean-4)

# Goal of Analysis <a name="goal"></a>
The goal of this project is to analyze which papers will recieve the most number of citations. 

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
# 5. Find the keywords in the abstract of the papers and the number of figures and tables <a name="findText"></a>

In a recently published research article, it was found that men used more superlatives than women in research papers published in PubMed. In this study, we wanted to see if use of superlatives in the abstract of our papers led to more citations. We used the same list of 25 superlitives as included in the research paper cited below in this study. The superlatives are listed below as well. 

1. novel
2. favorable
3. promising
4. unique
5. excellent
6. robust
7. prominant
8. supportive
9. encouraging
10. remarkable
11. innovative
12. bright
13. unprecedented
14. reassuring 
15. enormous
16. hopeful
17. creative
18. assuring
19. astonishing
20. inventive
21. spectacular
22. amazing
23. groundbreaking
24. inspiring
25. phenomenal


Lerchenmueller, M. J., Sorenson, O., & Jena, A. B. (2019). Gender differences in how scientists present the importance of their research: observational study. Bmj, l6573. doi: 10.1136/bmj.l6573

Additionally, we wanted to know if the number of tables and columns led to more citations. In order to do this, we used the text files of the papers scraped from the Journal of Quality Technology and searched for the words figure and table. Regular expressions were used to acount for various abreviations for figure, such as fig or Fig. 

The used to accomplish both these tasks is called findText.py and is shown below. 

```python 
import os
import re
import numpy as np
import pandas as pd


key_words = [
    'novel',
    'favorable',
    'promising',
    'unique',
    'excellent',
    'robust',
    'prominant',
    'supportive',
    'encouraging',
    'remarkable'
    'innovative',
    'bright',
    'unprecedented',
    'reassuring',
    'enormous',
    'hopeful',
    'creative',
    'assuring',
    'astonishing',
    'inventive',
    'spectacular',
    'amazing',
    'groundbreaking',
    'inspiring',
    'phenomenal'
]

self_path = os.path.dirname(os.path.realpath(__file__))
self_path = re.sub(r'\\','/',self_path)
os.chdir(self_path)

text_files = []
files_to_join = []
for file in os.listdir():
    if file.endswith(".txt"):
        text_files.append(file)


number_of_figures = []
number_of_tables = []
number_of_equations = []
titles_and_files = pd.read_csv('TitlesAndFiles_BDR.csv')
combined_data = pd.read_csv('Citation_Export_BDR.csv')


number_of_occurances_data = [] 
for i, file in enumerate(text_files):
    with open(file, encoding="utf8") as f:
        text = f.read()
    try:
        # Some of the files match the wrong file so some of them had to be hardcoded in
        if file == 'Detection of location and dispersion effects from partially replicated two level factorial designs (1).txt':
            title = 'Detection of location and dispersion effects from partially replicated two-level factorial designs'
        elif file == 'PROCEDURES AND TABLES FOR CONSTRUCTION AND SELECTION OF CHAIN SAMPLING PLANS (CHSP-1) .2. TABLES FOR SELECTION OF CHAIN SAMPLING.txt':
            title = 'PROCEDURES AND TABLES FOR CONSTRUCTION AND SELECTION OF CHAIN SAMPLING PLANS (CHSP-1) .2. TABLES FOR SELECTION OF CHAIN SAMPLING PLANS'
        elif file == 'The Performance of MIL STD 105D Under the Switching Rules.txt':
            title = 'PERFORMANCE OF MIL-STD-105D UNDER SWITCHING RULES .1. EVALUATION'
        else:
            # Find the matching web of science title from the file
            title = titles_and_files[titles_and_files['matching titles'].str.match(file,na=False)]['Title'].iloc[0]
        
        # Get the web of science information for the file
        information_web_of_science = combined_data[combined_data['Title'].str.match(title,na=False)]
    except:
        print('Something went wrong with ' + file)
        number_of_occurances = [title,"Error","Error","Error","NaN","NaN","NaN","NaN","NaN","NaN","NaN","NaN","NaN","NaN","NaN","NaN","NaN","NaN","NaN","NaN","NaN","NaN","NaN","NaN","NaN"]
        number_of_occurances_data.append(number_of_occurances)
        if title == 'PROBLEMS WITH INTERVAL ESTIMATION WHEN DATA ARE ADJUSTED VIA CALIBRATION':
            print('hi')
        continue
    if title == 'PROBLEMS WITH INTERVAL ESTIMATION WHEN DATA ARE ADJUSTED VIA CALIBRATION':
        print('hi')

    # Get the abstract from the web of science data
    try:
        abstract = information_web_of_science['Abstract'].iloc[0]
        number_of_occurances = []
        # Look for the key words in the abstract
        for index, keyword in enumerate(key_words):
            number_of_occurances = number_of_occurances  + [str(str(abstract).lower().split().count(keyword))]

        number_of_occurances = [title] + number_of_occurances
        number_of_occurances_data.append(number_of_occurances)
    except:
        number_of_occurances = [title,"NaN","NaN","NaN","NaN","NaN","NaN","NaN","NaN","NaN","NaN","NaN","NaN","NaN","NaN","NaN","NaN","NaN","NaN","NaN","NaN","NaN","NaN","NaN","NaN"]
        number_of_occurances_data.append(number_of_occurances)

titles = []
for i, file in enumerate(text_files):
    with open(file, encoding="utf8") as f:
        text = f.read()

 # Some of the files match the wrong file so some of them had to be hardcoded in
    if file == 'Detection of location and dispersion effects from partially replicated two level factorial designs (1).txt':
        title = 'Detection of location and dispersion effects from partially replicated two-level factorial designs'
    elif file == 'PROCEDURES AND TABLES FOR CONSTRUCTION AND SELECTION OF CHAIN SAMPLING PLANS (CHSP-1) .2. TABLES FOR SELECTION OF CHAIN SAMPLING.txt':
        title = 'PROCEDURES AND TABLES FOR CONSTRUCTION AND SELECTION OF CHAIN SAMPLING PLANS (CHSP-1) .2. TABLES FOR SELECTION OF CHAIN SAMPLING PLANS'
    elif file == 'The Performance of MIL STD 105D Under the Switching Rules.txt':
        title = 'PERFORMANCE OF MIL-STD-105D UNDER SWITCHING RULES .1. EVALUATION'
    else:
        # Find the matching web of science title from the file
        title = titles_and_files[titles_and_files['matching titles'].str.match(file,na=False)]['Title'].iloc[0]
    titles.append(title)
    # Look for figure references
    figure_pattern = re.compile(r'(?i)figure\s\d{1,4}')

    # Look for table referances
    table_pattern = re.compile(r'(?i)table\s\d{1,4}')

    # Look for key words


    # Look for equation references
    #equation_pattern = re.compile(r'(?i)(eq(uation)?s?.?\s)?\[?\{?\(?\d{1,4}\]?\}?\)?')

    figures = figure_pattern.findall(text)
    tables = table_pattern.findall(text)
    #equations= equation_pattern.findall(text)

    for i in range(len(figures)):
        figures[i] = figures[i].lower()
        figures[i] = figures[i].replace('\n', ' ')

    for j in range(len(tables)):
        tables[j] = tables[j].lower()
        tables[j] = tables[j].replace('\n', ' ')

    # for k in range(len(equations)):
    #     equations[k] = equations[k].lower()
    #     equations[k] = equations[k].replace('\n', ' ')

    figures = np.unique(figures)
    tables = np.unique(tables)
    #equations = np.unique(equations)

    number_of_figures.append(len(figures))
    number_of_tables.append(len(tables))
    #number_of_equations.append(len(equations))


# Save the number of tables and figures to a pandas dataframe
df = pd.DataFrame({ 'Title': titles,
                    'file':text_files, 
                    'number of figures':number_of_figures, 
                    'number of tables':number_of_tables})

df.to_csv('findText.csv')

dataframe_occurances = pd.DataFrame(number_of_occurances_data, columns=['Title']+key_words)

dataframe_occurances.to_csv('Keywords.csv')
```

# 6. Remove on instance of bad data <a name="baddata"></a>
One paper was accidently published  in the Journal of Quality Technology with its tables missing, and so a follow up paper was published with the tables. The Web of Science database treats these as two different papers, and so the paper was deleted from the analysis. The code to delete this from the data set is shown below. 

```python
# There is one paper that was published without tables, and so a follow up paper 
# was published with the tables. Since web of science treats these as two seperate papers, both will be deleted
# in order to prevent the model from messing up. 

import pandas as pd

Citation_Export = pd.read_csv('combinedCitationExport.csv')
# BDR = Bad Data Removed
Citation_Export = Citation_Export[Citation_Export.Title != 'PERFORMANCE OF MIL-STD-105D UNDER SWITCHING RULES .1. EVALUATION']
Citation_Export_BDR = Citation_Export[Citation_Export.Title !='PERFORMANCE OF MIL-STD-105D UNDER SWITCHING RULES .2. TABLES']
Citation_Export_BDR.to_csv('Citation_Export_BDR.csv')


TitlesAndFiles = pd.read_csv('TitlesAndFiles.csv')
# BDR = Bad Data Removed
TitlesAndFiles = TitlesAndFiles[TitlesAndFiles.Title != 'PERFORMANCE OF MIL-STD-105D UNDER SWITCHING RULES .1. EVALUATION']
TitlesAndFiles_BDR = TitlesAndFiles[TitlesAndFiles.Title !='PERFORMANCE OF MIL-STD-105D UNDER SWITCHING RULES .2. TABLES']
TitlesAndFiles_BDR.to_csv('TitlesAndFiles_BDR.csv')
```

# 7. Combined the data from the keywords, the number of figures and tables, and the Web of Science data <a name="combine"></a>

The last step in creating the data set is to combine all of the data into a .csv file. The code for this is called TotalCombinedData.py and is shown below. 

```python
import pandas as pd


Citation_Export = pd.read_csv('Citation_Export_BDR.csv')
Citation_Export = Citation_Export.sort_values(by=['Title'])
Citation_Export = Citation_Export.reset_index(drop=True)

Keywords = pd.read_csv('Keywords.csv')
Keywords= Keywords.sort_values(by=['Title'])
Keywords = Keywords.reset_index(drop=True)

findText = pd.read_csv('findText.csv')
findText = findText.sort_values(by=['Title'])
findText = findText.reset_index(drop=True)

TotalCombined = pd.concat([Citation_Export, Keywords, findText], axis=1, sort = False)

# Remove all untitled columns from the total combined data
TotalCombined= TotalCombined.drop(columns = ['Unnamed: 0', 'Unnamed: 0.1', 'Title.1'])



TotalCombined.to_csv('TotalCombined.csv')
```
# 8. Additional Cleaning on the Data Set <a name="clean"></a>
This section describes the additional cleaning done on the data set. The additional cleaning is found in the file DataCleaning.py

## Remove Years not needed on the data set <a name="clean-1"></a>
The web of science data provided a column for each year from 1864 to the present. Since the data that is being studied only starts at 1977, there is no need for these additional columns. The code for this is shown below. 

```python 

data_set = pd.read_csv('TotalCombined.csv', index_col=0)

# Since the articles only go back to 1977, all previous years before then can be removed from the columns
bad_years = range(1864, 1976)
for year in bad_years:
    data_set = data_set.drop(columns=str(year))

data_set.to_csv('TotalCombinedCleaned.csv')
```

## Remove columns with digital ID's <a name="clean-2"></a>

The web of science data included digitial ID's for the papers. These will not be useful for the modelling so they were removed. 

```python
# Remove columns that were created for ID's
columns_to_drop = ["DOI", "ResearcherID Number", "ORCID Identifier (Open Researcher and Contributor ID)", 
                    "Digital Object Identifier (DOI)", "EA", "International Standard Serial Number (ISSN)", 
                    "Electronic International Standard Serial Number (eISSN)", "Accession Number / ISI Unique Article Identifier", 
                    "Full Source Title (includes title and subtitle)"]
data_set = data_set.drop(columns=columns_to_drop)
```

## Remove columns from previous analysis  <a name="clean-3"></a>
The columns that included the keywords from the paper surveying keywords in a medical journal did not apply well to the journal that is being studied. Thus the keywords columns were removed from the data set. 

```python
# Remove keywords from previous analysis
key_words = [
    'novel',
    'favorable',
    'promising',
    'unique',
    'excellent',
    'robust',
    'prominant',
    'supportive',
    'encouraging',
    'remarkable'
    'innovative',
    'bright',
    'unprecedented',
    'reassuring',
    'enormous',
    'hopeful',
    'creative',
    'assuring',
    'astonishing',
    'inventive',
    'spectacular',
    'amazing',
    'groundbreaking',
    'inspiring',
    'phenomenal'
]
data_set = data_set.drop(columns=key_words)
```
## Create a column for number of pages <a name="clean-4"></a>
There is a column for start page and end page. The code shown below will subtract the two to come up with a total number of pages for each paper. 




