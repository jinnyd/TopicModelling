from flask import render_template
from flask import redirect
from flask import send_from_directory
from flaskexample import app
from flask import request
#some functions defined under doc2vec.py file
from flaskexample import doc2vec
import gensim
import os.path
import pandas as pd
from gensim.models.doc2vec import Doc2Vec, TaggedDocument

mypath = os.path.abspath(os.path.dirname("data_clean.csv"))
path = os.path.join(mypath, "flaskexample/doc2vec_model")
model = Doc2Vec.load(path)

@app.route('/')
@app.route('/index')
def index():
	return render_template("index.html")

@app.route('/search_story')
def search_story():
	return render_template("search_story.html")

@app.route('/channel')
def channel():
	return redirect("https://www.youtube.com/channel/UCWENB1OaGA9402PKzEVl0ow")

@app.route('/company')
def company():
	return redirect("https://www.storybooth.com")
	
@app.route('/topic_model')
def topic_model():
	return render_template("topic_model.html")

@app.route('/lda')
def lda():
	return render_template("lda1.html")

@app.route('/slide')
def slide():
	return render_template("slide.html")
	
@app.route('/output2')
def output2():
	topicnum = int(request.args.get("topicnumber"))
	names = ["School friendship", "Puberty", "Love and Romance", "Anxiety", 
			"Pet and health", "Bully", "Athletic Activity", "Family troubles"
			"Outdoor events", "Embarrassing stories"]
	storylen = int(request.args.get("storylength"))
	if storylen == 0: 
		lower = 0
		upper = 150
	if storylen ==  1:
		lower = 150
		upper = 300
	if storylen == 2:
		lower = 300
		upper = 500
	if storylen == 3:
		lower = 500
		upper = 10000
	filepath = os.path.join(mypath, "flaskexample/data_topics.csv")
	data = pd.read_csv(filepath)
	data = data.loc[ data['topics'] == topicnum]
	n = len(data)
	res = []
	for i in range(n):
		if len(data.iloc[i, 1].split()) > lower and len(data.iloc[i, 1].split()) <= upper:
			res.append([data.iloc[i, 0], data.iloc[i, 1]])
		
	return render_template("output2.html", result = res, name = names[topicnum])

@app.route('/output')
def output():
	#pull keywords from input field and store it
	keywords = request.args.get("keywords")
	num = request.args.get("numbers")

	filepath = os.path.join(mypath, "flaskexample/data_clean.csv")
	data = pd.read_csv(filepath)
	score = doc2vec.similarity_score(keywords, model)
	index = doc2vec.find_article_idx(score, n = int(num))
	#find articles
	res = []
	for i in index:
		res.append(list(data.iloc[i][1:3]))
	
	return render_template("output.html", result=res, name = keywords)

'''
@app.route('/mp3')
def download_file(filename):
    return send_from_directory('Users/Jinny/flaskexample/', filename)

'''