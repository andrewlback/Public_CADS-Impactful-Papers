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