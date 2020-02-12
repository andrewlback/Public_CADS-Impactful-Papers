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