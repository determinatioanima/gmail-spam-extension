#coding:utf-8
from flask import Flask, redirect, url_for, session
from flask_oauth import OAuth
from flask import request
from sklearn.externals import joblib
import pickle
import os
import quopri
import base64
import random
import re
from flask import render_template
from flask import jsonify
import logging
from flask import session
from logging.handlers import RotatingFileHandler
import json

import spam_not_spam as checker

# You must configure these 3 values from Google APIs console
# https://code.google.com/apis/console
GOOGLE_CLIENT_ID = "222968144930-4rprefi5arv6bb7fcqph03693gof8hvt.apps.googleusercontent.com"
GOOGLE_CLIENT_SECRET = "2Wd1b5XQlG6u-29a9OYR2YG3"
REDIRECT_URI = '/authorized'  # one of the Redirect URIs from Google APIs console

SECRET_KEY = 'development key'
DEBUG = True

app = Flask(__name__)
app.debug = DEBUG
app.secret_key = SECRET_KEY
oauth = OAuth()

google = oauth.remote_app('google',
						  base_url='https://www.google.com/accounts/',
						  authorize_url='https://accounts.google.com/o/oauth2/auth',
						  request_token_url=None,
						  request_token_params={'scope': 'https://www.googleapis.com/auth/gmail.readonly',
												'response_type': 'code'},
						  access_token_url='https://accounts.google.com/o/oauth2/token',
						  access_token_method='POST',
						  access_token_params={'grant_type': 'authorization_code'},
						  consumer_key=GOOGLE_CLIENT_ID,
						  consumer_secret=GOOGLE_CLIENT_SECRET)

global_token = ""

def cleanhtml(raw_html):
  cleanr = re.compile('<.*?>')
  cleantext = re.sub(cleanr, '', raw_html)
  return cleantext

@app.route('/')
def index():
	global global_token
	access_token = session.get('access_token')
	if len(global_token) != 0 and access_token is None:
		access_token = global_token
	elif access_token is None:
		return redirect(url_for('login'))
	
	global_token = access_token
	app.logger.info('Info:'+str(access_token))
	access_token = access_token[0]
	from urllib2 import Request, urlopen, URLError

	headers = {'Authorization': 'OAuth '+access_token}
	req = Request('https://www.googleapis.com/gmail/v1/users/me/messages',
				  None, headers)
	try: 
		res = urlopen(req)
	except URLError, e:
		if e.code == 401:
			# Unauthorized - bad token
			app.logger.info('ERROR')
			session.pop('access_token', None)
			return redirect(url_for('login'))
		return res.read()

	return res.read()

@app.route('/gmail/<string:email_id>')
def get_gmail_email(email_id):
	global global_token
	access_token = session.get('access_token')
	if len(global_token) != 0:
		access_token = global_token
	elif access_token is None:
		return redirect(url_for('login'))
	
	global_token = access_token
	app.logger.info('Info get_gmail_email:'+str(access_token))
	access_token = access_token[0]
	from urllib2 import Request, urlopen, URLError

	headers = {'Authorization': 'OAuth '+access_token}
	req = Request('https://www.googleapis.com/gmail/v1/users/me/messages/'+email_id+'?format=full',
				  None, headers)
	try: 
		res = urlopen(req)
		parsed_data = json.loads(res.read())
		#parsed_data = base64.urlsafe_b64decode(parsed_data['raw'].encode('ASCII'))
		payload = ""
		part_count = len(parsed_data["payload"]["parts"])
		for i in range(part_count):
			payload += parsed_data["payload"]["parts"][part_count-i-1]["body"]["data"]
		decode_payload = base64.urlsafe_b64decode(payload.encode('ASCII'))
		parsed_data['hahaha'] = cleanhtml(decode_payload.replace('\r\n>', '')).replace('\r\n', '')
	except URLError, e:
		if e.code == 401:
			# Unauthorized - bad token
			session.pop('access_token', None)
			return redirect(url_for('login'))
		return res.read()

	return jsonify(parsed_data)
	
@app.route('/gmail_score/<string:email_id>')
def get_gmail_score_email(email_id):
	global global_token
	access_token = session.get('access_token')
	if len(global_token) != 0:
		access_token = global_token
	elif access_token is None:
		return redirect(url_for('login'))
	
	global_token = access_token
	app.logger.info('Info get_gmail_email:'+str(access_token))
	access_token = access_token[0]
	from urllib2 import Request, urlopen, URLError

	headers = {'Authorization': 'OAuth '+access_token}
	req = Request('https://www.googleapis.com/gmail/v1/users/me/messages/'+email_id+'?format=full',
				  None, headers)
	try: 
		res = urlopen(req)
		parsed_data = json.loads(res.read())
		#parsed_data = base64.urlsafe_b64decode(parsed_data['raw'].encode('ASCII'))
		payload = ""
		part_count = len(parsed_data["payload"]["parts"])
		for i in range(part_count):
			payload += parsed_data["payload"]["parts"][part_count-i-1]["body"]["data"]
		decode_payload = base64.urlsafe_b64decode(payload.encode('ASCII'))
		parsed_data['hahaha'] = cleanhtml(decode_payload.replace('\r\n>', '')).replace('\r\n', '')
		#start here
		input = parsed_data
		json_payload = input["payload"]
	
		if len(json_payload["filename"]) > 0 :
			file_exist = 1
		else :
			file_exist = 0 
		
		json_arc = json_payload["headers"]
		spf_score = 0
		dkim_score = 0
		dmarc_score = 0 
	
		for test in json_arc :
		#	if "spf=pass" in test["value"] and spf_flag == 1:
			if test["value"].find("spf=pass")>0:
				spf_score = 1
	
			if "dkim=pass" in test["value"] :
				dkim_score = 1
	
			if "dmarc=pass" in test["value"] :
				dmarc_score = 1
	
		mail_content = input["hahaha"]
	
		# load model & word_features
		NB_classifier = joblib.load("model/NB_classifier")
		BNB_classifier = joblib.load("model/BNB_classifier")
		with open('word/word_feature.pickle') as f:
			word_features = pickle.load(f)
		
		# predict 1
		feature = find_feature(word_features, mail_content)
		result_NB = NB_classifier.classify(feature)
		# predict 2
		feature = find_feature(word_features, mail_content)
		result_BNB = BNB_classifier.classify(feature)
	
		# give score
		score = 1
		if(spf_score == 1):
			score += 2
		if(dkim_score == 1):
			score += 2
		if(dmarc_score == 1):
			score += 1
		if(file_exist == 0):
			score += 1
		if(result_NB == "ham"):
			score += 1.5
		if(result_BNB == "ham"):
			score += 1.5
		
		response={
			"score":score,
			"spf_score": spf_score,
			"dkim_score": dkim_score,
			"dmarc_score": dmarc_score,
			"file_exist": file_exist,
			"result_NB": result_NB,
			"result_BNB": result_BNB,
		}
		
		return jsonify(response)
		
		
	except URLError, e:
		if e.code == 401:
			# Unauthorized - bad token
			session.pop('access_token', None)
			return redirect(url_for('login'))
		return res.read()

	return score

@app.route('/login')
def login():
	callback=url_for('authorized', _external=True)
	return google.authorize(callback=callback)

@app.route(REDIRECT_URI)
@google.authorized_handler
def authorized(resp):
	access_token = resp['access_token']
	global global_token
	global_token = access_token
	session['access_token'] = access_token, ''
	return redirect(url_for('index'))

@google.tokengetter
def get_access_token():
	return session.get('access_token')

@app.route('/auth')
def auth(name=None):
	return render_template('quickstart.html', name=name)

@app.route('/clear')
def clear(name=None):
	global global_token
	app.logger.info(global_token)
	session.clear()
	global_token = ""
	if global_token is None or len(global_token) == 0:
		return "true"
	else:
		return str(global_token[0])

@app.route('/score/<int:email_order>')
def email(email_order):
	return str(random.randint(1,10))

@app.route('/check/', methods=["POST"])
def check():
	# get data
	input = request.get_json()
	json_payload = input["payload"]

	if len(json_payload["filename"]) > 0 :
		file_exist = 1
	else :
		file_exist = 0 
	
	json_arc = json_payload["headers"]
	spf_score = 0
	dkim_score = 0
	dmarc_score = 0 

	for test in json_arc :
	#	if "spf=pass" in test["value"] and spf_flag == 1:
		if test["value"].find("spf=pass")>0:
			spf_score = 1

		if "dkim=pass" in test["value"] :
			dkim_score = 1

		if "dmarc=pass" in test["value"] :
			dmarc_score = 1

	mail_content = input["hahaha"]

	# load model & word_features
	NB_classifier = joblib.load("model/NB_classifier")
	BNB_classifier = joblib.load("model/BNB_classifier")
	with open('word/word_feature.pickle') as f:
		word_features = pickle.load(f)
	
	# predict 1
	feature = find_feature(word_features, mail_content)
	result_NB = NB_classifier.classify(feature)
	# predict 2
	feature = find_feature(word_features, mail_content)
	result_BNB = BNB_classifier.classify(feature)

	# give score
	score = 1
	if(spf_score == 1):
		score += 2
	if(dkim_score == 1):
		score += 2
	if(dmarc_score == 1):
		score += 1
	if(file_exist == 0):
		score += 1
	if(result_NB == "ham"):
		score += 1.5
	if(result_BNB == "ham"):
		score += 1.5

	return jsonify(score=score)

@app.route('/payback/<label>', methods=["POST"])
def payback(label):
	# get data
	app.logger.info('Info:'+request.form["level"] +" "+request.form["often"]+" "+request.form["category"])
	return jsonify(status="OK")


# find features of a mail content
def find_feature(word_features, content):
	feature = {}
	mail_content = content.decode('utf-8').strip().lower()
	for word in word_features:
		feature[word] = word.decode('utf-8').strip() in mail_content
		
	return feature

def main():
	app.run(host=os.getenv('IP', '0.0.0.0'),port=int(os.getenv('PORT', 8080)))

if __name__ == '__main__':
	main()