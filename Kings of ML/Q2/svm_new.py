import os
import sys
import numpy as np
from keras.utils import np_utils
from sklearn import cross_validation
from sklearn.metrics import accuracy_score
from sklearn import metrics
from sklearn import grid_search
from sklearn.cross_validation import cross_val_score
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.neighbors import KNeighborsClassifier
from sklearn.ensemble import RandomForestClassifier, AdaBoostClassifier
from sklearn.naive_bayes import MultinomialNB
import warnings
from sklearn import svm
from sklearn.svm import SVC

warnings.filterwarnings("ignore")

vectorizer = CountVectorizer(ngram_range=(2,2))
tfidf_vectorizer = TfidfTransformer()
directory = os.getcwd()
nb_classes_coarse = 6
nb_classes_fine = 45

coarse_labels=['LOC', 'HUM', 'NUM', 'ABBR', 'ENTY', 'DESC'];
fine_labels=['code', 'dist', 'gr', 'weight', 'color', 'money', 'period', 'currency', 'manner', 'ind', 'sport', 'speed', 'event', 'perc', 'city', 'abb', 'techmeth', 'title', 'dismed', 'termeq', 'religion', 'state', 'other', 'animal', 'veh', 'body', 'lang', 'product', 'food', 'symbol', 'plant', 'reason', 'letter', 'volsize', 'date', 'word', 'ord', 'desc', 'count', 'substance', 'cremat', 'temp', 'country', 'mount', 'instru', 'exp', 'def'];

coarse_labels_dic={'LOC':0, 'HUM':1, 'NUM':2, 'ABBR':3, 'ENTY':4, 'DESC':5};
fine_labels_dic={'code':0, 'dist':1, 'gr':2, 'weight':3, 'color':4, 'money':5, 'period':6, 'currency':7, 'manner':8, 'ind':9, 'sport':10, 'speed':11, 'event':12, 'perc':13, 'city':14, 'abb':15, 'techmeth':16, 'title':17, 'dismed':18, 'termeq':19, 'religion':20, 'state':21, 'other':22, 'animal':23, 'veh':24, 'body':25, 'lang':26, 'product':27, 'food':28, 'symbol':29, 'plant':30, 'reason':31, 'letter':32, 'volsize':33, 'date':34, 'word':35, 'ord':36, 'desc':37, 'count':38, 'substance':39, 'cremat':40, 'temp':41, 'country':42, 'mount':43, 'instru':44, 'exp':45, 'def':46};

ABBR_dic={'abb':0,'exp':1}
DESC_dic={'def':0,'desc':1,'manner':2,'reason':3}

def preProcessing(path,istest=0,num=0):	# use num = 1 for coarse-grain classifier
	X = []
	y = []

	with open(directory + "/" + path, "r") as f:
		for row in f.read().split('\n')[1:]: 
			fc = row.split(':')
			if num == 0:
				label = fc[2]
			else:
				label = fc[1]
			
			X.append(" ".join(ele.lower() for ele in fc[3:] if len(ele)>3))
			if istest==0:
				#print(label)
				if num==0:
					y.append(fine_labels_dic[label])
				else:
					y.append(coarse_labels_dic[label])
	#print(y[1])				
	return X, y

def evaluateClassifier(questions, labels, clf,num=0):
	X_new_tfidf = vectorizer.transform(questions)
	X_new_tfidf = tfidf_vectorizer.transform(X_new_tfidf)
	scores = cross_validation.cross_val_score(clf, X_new_tfidf, labels, cv= 5, scoring="accuracy")
	print scores

def buildClassifier(questions, labels, classifierName,num=0):
	X_old = vectorizer.fit_transform(questions)
	X_old = tfidf_vectorizer.fit_transform(X_old).todense()
	X_old = np.asarray(X_old)
	print(X_old.shape)
	labels=np.asarray(labels)
	print(labels.shape)
	#print(set(labels))
	# clf = KNeighborsClassifier()
	if classifierName == "KNN":
		parameters = {'weights': ['uniform', 'distance'], 'n_neighbors': [5, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100]}
		clf = KNeighborsClassifier()
		clf = grid_search.GridSearchCV(clf, parameters)
		return clf.fit(X_old, labels)

	elif classifierName == "MNB":
		parameters = {'alpha':[0, 0.2, 0.5, 0.7, 0.9, 1], 'fit_prior':[True, False]}
		clf = MultinomialNB()
		clf = grid_search.GridSearchCV(clf, parameters)
		score = cross_val_score(clf, X_old, labels, n_jobs=8)
		print score
		return clf.fit(X_old, labels)

	elif classifierName == "RF":
		max_depth = [3,5,7,10,12,15,20,25,32]
		bestmax=0
		#n_estimators = [10,25,50,75,100,150,200,300,500]
		#for i in max_depth:
	    #	clf = RandomForestClassifier(max_depth=i, n_estimators=300, n_jobs=8, class_weight='balanced')
		#	score = cross_val_score(clf, X_old, labels, n_jobs=-1)
		#	print score
		#for i in n_estimators:
		#	clf = RandomForestClassifier(max_depth=32, n_estimators=i, n_jobs=8, class_weight='balanced')
		#	score = cross_val_score(clf, X_old, labels, n_jobs=-1)
		#	print score
		clf = RandomForestClassifier(max_depth=32, n_estimators=300, n_jobs=8, class_weight='balanced')
		score = cross_val_score(clf, X_old, labels, n_jobs=-1)
		print score
		clf.fit(X_old,labels)
		return clf

	elif classifierName == "SVM":
		parameters = {'kernel':(['linear']), 'C':[10], 'gamma':[0.1]}
		clf = svm.SVC()
		#clf = grid_search.GridSearchCV(clf, parameters)
		clf = clf.fit(X_old, labels)
		#print clf.best_params_
		return clf

def customQuestionScorer(question, clf,num=0):
	X_new_tfidf = tfidf_vectorizer.transform(vectorizer.transform(question)).todense()
	print(len(set(X_new_tfidf)))
	X_new_tfidf = np.asarray(X_new_tfidf)
	y_pred = clf.predict(X_new_tfidf)
	print(X_new_tfidf.shape)
		
	y_pred=np.asarray(y_pred).flatten()
	print(y_pred.shape)
	print(set(y_pred))
	if num==0:
		f=open('testSubmission.csv')
		f_new=open('finalSubmission.csv','w+')
		lines=f.read().split('\n')[1:]

	if num==1:
		f=open('finalSubmission.csv')
		f_new=open('finalSubmission2.csv','w+')
		lines=f.read().split('\n')[1:-1]


	print(len(lines))
	f_new.write('IDVal,Coarse_Label,Fine_Label\n')
	for no in xrange(len(lines)):
		#print(no)
		lines[no] =lines[no].split(',')
		if num==0:
			fine_val=y_pred[no]
			f_new.write(lines[no][0]+','+lines[no][1]+','+str(fine_labels[fine_val])+'\n')

		else:
			coarse_val=y_pred[no]
			f_new.write(lines[no][0]+','+str(coarse_labels[coarse_val])+','+lines[no][2]+'\n')

	f_new.close()
	
def main():
	X_train = X_test = y_train = y_test = []

	classifierName = "RF"
	
	X_train, y_train = preProcessing("training_data.txt")
	X_test, y_test = preProcessing("testing_data.txt",istest=1)


	print "Training"
	clf = buildClassifier(X_train, y_train, classifierName)
	
	print "Testing"
	#evaluateClassifier(X_test, y_test, clf)
	
	customQuestionScorer(X_test, clf)

	X_train = X_test = y_train = y_test = []

	classifierName = "RF"
	
	X_train, y_train = preProcessing("training_data.txt",num=1)
	X_test, y_test = preProcessing("testing_data.txt",istest=1,num=1)


	print "Training"
	clf = buildClassifier(X_train, y_train, classifierName,num=1)
	
	print "Testing"
	#evaluateClassifier(X_test, y_test, clf)
	
	q = "Who is the  director of IIIT?"
	customQuestionScorer(X_test, clf,num=1)

if __name__ == '__main__' :
	vectorizer = CountVectorizer(ngram_range = (1,2))
	tfidf_vectorizer = TfidfTransformer()
	directory = os.getcwd()
	main()