import nltk
import random
import os
import os.path
import pickle
from nltk.corpus import stopwords
from sklearn.externals import joblib
from sklearn.model_selection import cross_val_score
from nltk.classify.scikitlearn import SklearnClassifier
from sklearn.naive_bayes import MultinomialNB,BernoulliNB
from sklearn.linear_model import LogisticRegression,SGDClassifier
import string
import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)
	
if os.name == 'nt':
	clear_screen = "cls"
else:
	clear_screen = "clear"
os.system(clear_screen)

# -------- data!!!!! -------------
file_name = "data/train_data"
# -------- data!!!!! -------------

def find_feature(word_features, message):
	# find features of a message
	feature = {}
	for word in word_features:
		feature[word] = word in message.lower()
	return feature

def create_mnb_classifier(trainingset, testingset):
    # Multinomial Naive Bayes Classifier
    MNB_classifier = SklearnClassifier(MultinomialNB())
    MNB_classifier.train(trainingset)
    accuracy = nltk.classify.accuracy(MNB_classifier, testingset)*100
    # print("MultinomialNB Classifier accuracy = " + str(accuracy))
    return MNB_classifier

def create_bnb_classifier(trainingset, testingset):
    # Bernoulli Naive Bayes Classifier
    BNB_classifier = SklearnClassifier(BernoulliNB())
    BNB_classifier.train(trainingset)
    # accuracy = nltk.classify.accuracy(BNB_classifier, testingset)*100
    # print("BernoulliNB accuracy percent = " + str(accuracy))
    return BNB_classifier

def create_logistic_regression_classifier(trainingset, testingset):
    # Logistic Regression classifier
    LogisticRegression_classifier = SklearnClassifier(LogisticRegression())
    LogisticRegression_classifier.train(trainingset)
    # print("Logistic Regression classifier accuracy = "+ str((nltk.classify.accuracy(LogisticRegression_classifier, testingset))*100))
    return LogisticRegression_classifier

def create_sgd_classifier(trainingset, testingset):
    SGDClassifier_classifier = SklearnClassifier(SGDClassifier())
    SGDClassifier_classifier.train(trainingset)
    # print("SGD Classifier classifier accuracy = " + str((nltk.classify.accuracy(SGDClassifier_classifier, testingset))*100))
    return SGDClassifier_classifier

def create_nb_classifier(trainingset, testingset):
    # Naive Bayes Classifier
    NB_classifier = nltk.NaiveBayesClassifier.train(trainingset)
    accuracy = nltk.classify.accuracy(NB_classifier, testingset)*100
    # print("Naive Bayes Classifier accuracy = " + str(accuracy))
    # NB_classifier.show_most_informative_features(20)
    return NB_classifier

def create_training_testing(train_file):
	"""
	function that creates the feature set, training set, and testing set
	"""
	with open(train_file) as f:
		messages = f.read().split('\n')

	# print("Creating bag of words....")
	all_messages = []														# stores all the messages along with their classification
	all_words = []															# bag of words
	for message in messages:
		label,payload = message.split('\t')
		all_messages.append([payload, label])
		
		for s in string.punctuation:		# Remove punctuations
			if s in payload:
				payload = payload.replace(s, " ")
		
		stop = stopwords.words('english')
		for word in payload.split():				# Remove stopwords
			if not word in stop:
				all_words.append(word.lower())
	# print("Bag of words created.")

	random.shuffle(all_messages)
	random.shuffle(all_messages)
	random.shuffle(all_messages)

	all_words = nltk.FreqDist(all_words)
	word_features = list(all_words.keys())[:2000]		# top 2000 words are our features

	# print("\n----------------------------")
	# print("Creating feature set....")
	featureset = [(find_feature(word_features, message), category) for (message, category) in all_messages]
	# print("Feature set created.")
	trainingset = featureset[:int(len(featureset)*3/4)]
	testingset = featureset[int(len(featureset)*3/4):]

	return word_features, featureset, trainingset, testingset

def train(train_file):
	# get data (word_features = top 2000 words are our features , trainingset = 3/4 * featureset , trainingset = 1/4 * featureset)
	word_features, featureset, trainingset, testingset = create_training_testing(train_file)

	#saving word_feature
	with open('word/word_feature.pickle', 'w') as f:
		pickle.dump(word_features,f)

	# training model
	NB_classifier = create_nb_classifier(featureset, testingset)
	BNB_classifier = create_bnb_classifier(featureset, testingset)
	
	# saving model
	joblib.dump(NB_classifier,"model/NB_classifier")
	joblib.dump(BNB_classifier,"model/BNB_classifier")

if __name__ == '__main__':
	print("|| =========== ||")
	print("|| Start train ||")
	train(file_name)
	print("||  train end  ||")
	print("|| =========== ||")