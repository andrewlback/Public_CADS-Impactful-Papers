import os
import io
import pandas as pd
from fuzzywuzzy import fuzz,process
from tqdm import tqdm

#Specify the directory for the papers
input_directory = 'C:/Users/backal/Desktop/CADS-Impactful-Papers/webOfScienceCleaning/AllTextPapers'
#input_directory = 'C:/Users/Me/Desktop/CADS-Impactful-Papers/webOfScienceCleaning/AllTextPapers'
#os.chdir('C:/Users/Me/Desktop/CADS-Impactful-Papers/webOfScienceCleaning')
os.chdir('C:/Users/backal/Desktop/CADS-Impactful-Papers/webOfScienceCleaning')

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
os.chdir('C:/Users/backal/Desktop/CADS-Impactful-Papers/webOfScienceCleaning/AllTextPapers')
files = os.listdir()
filesdf = pd.DataFrame(files)

for file in files:
    if file in web_of_science_titles:
        from shutil import copyfile
        #copyfile('C:/Users/Me/Desktop/CADS-Impactful-Papers/webOfScienceCleaning/AllTextPapers/'+file, 'C:/Users/Me/Desktop/CADS-Impactful-Papers/webOfScienceCleaning/TextPapersInWebOfScience/'+file)
        copyfile('C:/Users/backal/Desktop/CADS-Impactful-Papers/webOfScienceCleaning/AllTextPapers/'+file, 'C:/Users/backal/Desktop/CADS-Impactful-Papers/webOfScienceCleaning/TextPapersInWebOfScience/'+file)


# Show titles and files together
test = pd.DataFrame(web_of_science_titles)
alldf = pd.concat([test,filesdf],axis=1)
alldf.to_csv('alltestdf.csv')

for title in web_of_science_titles:
    if title not in files:
        print(str(title) + ' not in folder')