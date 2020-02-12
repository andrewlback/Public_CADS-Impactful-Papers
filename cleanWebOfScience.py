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


