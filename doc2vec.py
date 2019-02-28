# Include libraries
import pandas as pd
import numpy as np
import string

def similarity_score(story, model):
    story_vec = model.infer_vector(story.split(), steps=40)
    res = []
    size = len(model.docvecs)
    for i in range(size):
        tmp = np.dot(story_vec, model.docvecs[i])/(np.linalg.norm(story_vec) * np.linalg.norm(model.docvecs[i]))
        res.append(tmp)
    return res

#Find the index of most similar articles 
def find_article_idx(score, n):
	return np.argsort(score)[::-1][:n]

