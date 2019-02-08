import pandas as pd
import numpy as np
import string
#import json files
import json
import os.path

# filenames.txt contains the names of .json files 
# Save names into variable file_names
mypath = os.path.abspath(os.path.dirname('filenames.txt'))

filepath = os.path.join(mypath, "filenames.txt")
f = open(filepath, mode="r")
file_names = []
for line in f:
    file_names.append(line.rstrip())
f.close()

#Read stoies into a data frame each story is a row of string
data_raw = []
for names in file_names:
    path = os.path.join(mypath, "data", names)
    f = open(path, "r")
    story_line = json.load(f)
    data_raw.append([names, story_line["results"]["transcripts"][0]["transcript"]])
    f.close()


    #Eclude empty strings:
data = []
for i, line in enumerate(data_raw):
    if not data_raw[i][1]:
        continue
    else:
        data.append(line)

#Save the file to .csv file:
data_noempty = pd.DataFrame(data, columns=['filename', 'text'])
data_noempty.to_csv('data_raw.csv')

#modify file names to extract common part
data = pd.read_csv('data_raw.csv')
n = len(data)
anothername = []
for i in range(n):
    if data.iloc[i, 1][:-14][-1] == '-':
        anothername.append(data.iloc[i,1][:-15])
    else:
        anothername.append(data.iloc[i,1][:-14])
#save another name to data frame
data['anothername'] = anothername 

#Add another column showing the number of words in the text
wdlen = []
for line in data["text"]:
    wdlen.append(len(line.split()))
data['word_len'] = wdlen

# find the rows group by another name where text length is the biggest
idx = data.groupby(['anothername'])['word_len'].transform(max) == data['word_len']
data = data[idx]
data_clean = data[['filename', 'text']].copy()

#Create the data_clean.csv file
data_clean.to_csv('data_clean.csv')