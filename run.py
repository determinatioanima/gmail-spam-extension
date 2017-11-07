from flask import Flask
from flask import request
from flask import jsonify
from sklearn.externals import joblib
import pickle
import time
import thread

import spam_not_spam as checker

app = Flask(__name__)

file_name = "data/train_data"

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

    return jsonify(status="OK")


# find features of a mail content
def find_feature(word_features, content):
    feature = {}
    mail_content = content.lower()
    for word in word_features:
        feature[word] = word.decode('utf-8').strip() in mail_content
        
    return feature



if __name__ == '__main__':
    app.run()
