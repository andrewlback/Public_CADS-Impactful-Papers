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


