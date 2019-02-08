# Include libraries
import pandas as pd
import numpy as np
import string

#for absolute path
import os.path
#import library
from gensim.models.doc2vec import Doc2Vec, TaggedDocument

mypath = os.path.abspath(os.path.dirname("data_clean.csv"))
filepath = os.path.join(mypath, "data_clean.csv")

#load cleaned data
data = pd.read_csv(filepath)

content = data['text']
def Tokenize(doc):
    res = []
    for line in doc:
        res.append(line.split())
    return res

tokenizer = Tokenize(content)

documents = [TaggedDocument(doc, [i]) for i, doc in enumerate(tokenizer)]
model = Doc2Vec(documents, vector_size=50, window=2, min_count=1, workers=2)

model.save('doc2vec_model')

similarity_score = []
tokenizer = Tokenize(story)
story_vec = model.infer_vector(tokenizer)

for i in len(model.docvecs):
	res = np.dot(story_vec, model.docvecs[i])/(np.linalg.norm(story_vec) * np.linalg.norm(model.docvecs[i]))
	similarity_score.append()

#Find the index of most similar articles 
def find_article_idx(score, n):
	return np.argsort(score)[::-1][:n]

