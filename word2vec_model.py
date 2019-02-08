# Include libraries
import pandas as pd
import numpy as np
import string

import os.path

#conmpute a vector for a story
def build_vector_for_story(story, model):
	size = model.vector_size
	story_vec = np.zeros(size)
	if len(story.split()) == 0:
		return story_vec
	for word in story.split():
		if word in model.vocab.keys():
			story_vec = np.add(story_vec, model[word])
	return story_vec/len(story) #Take average of word vectors

#Compute similarity score between key words and the data
def similarity_score(story, data, model):
    vec1 = build_vector_for_story(story, model)
    n = len(data)
    vec_data = np.zeros((n, model.vector_size))
   
    for i, line in enumerate(data):
        vec_data[i, :] = build_vector_for_story(line, model)

    res = np.zeros(n)
    for i in range(10):
        res[i] = np.dot(vec1, vec_data[i,:])/(np.linalg.norm(vec1) * np.linalg.norm(vec_data[i,:]))
    return res

#Find the index of most similar articles 
def find_article_idx(score, n):
	return np.argsort(score)[::-1][:n]

