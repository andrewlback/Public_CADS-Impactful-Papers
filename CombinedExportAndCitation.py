import pandas as pd

data1 = pd.read_csv('combinedDataCitationReport.csv',index_col=0)
data2 = pd.read_csv('combinedDataExport.csv',index_col=0)

combinedData = [data1, data2]
combinedData = pd.concat(combinedData, axis=1, sort=False)
combinedData = combinedData.dropna(axis=1,how='all')
combinedData.to_csv('combinedCitationExport.csv')