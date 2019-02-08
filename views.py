from flask import render_template
from flaskexample import app
from flask import request
from flaskexample import word2vec_model
import gensim
import os.path
import pandas as pd

mypath = os.path.abspath(os.path.dirname("data_clean.csv"))
path = os.path.join(mypath, "GoogleNews-vectors-negative300.bin")
model = gensim.models.KeyedVectors.load_word2vec_format(path, binary=True, limit=500000) 

@app.route('/')
@app.route('/index')
def index():
	return render_template("index.html")

@app.route('/search_story')
def search_story():
	return render_template("search_story.html")

@app.route('/hello')
def hello():
	return render_template("hello.html")
@app.route('/topic_model')
def topic_model():
	return render_template("topic_model.html")

@app.route('/output2')
def output2():
	topicnum = request.args.get("topicnumber")
	
	filepath = os.path.join(mypath, "flaskexample/data_topics.csv")
	data = pd.read_csv(filepath)
	data = data.loc[ data['topics'] == int(topicnum)]
	data = data["text"].values
	n = len(data)
	if n >= 20:
		n = 20
	res = []
	for i, line in enumerate(data):
		res.append(line)
		if i == 10:
			break
	return render_template("output2.html", result = res)

#@app.route('/channel')
#def channel():
#	return redirect("www.youtube.com", code = 302)

@app.route('/output')
def output():
	#pull keywords from input field and store it
	keywords = request.args.get("keywords")
	num = request.args.get("numbers")

	filepath = os.path.join(mypath, "flaskexample/data_clean.csv")
	data = pd.read_csv(filepath)
	score=word2vec_model.similarity_score(keywords, data['text'], model)
	index = word2vec_model.find_article_idx(score, n = int(num))
	#find articles
	res = []
	for i in index:
		res.append(list(data.iloc[i][1:3]))
	
	return render_template("output.html", result=res)

