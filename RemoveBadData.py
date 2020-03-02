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