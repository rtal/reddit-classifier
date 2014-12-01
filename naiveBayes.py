import collections
import argparse
import csv
import numpy as np
import FeatureExtractor
from sklearn.feature_extraction import DictVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics import confusion_matrix
from sklearn import cross_validation

#global variables
labelToSubreddit = []


#parse data into format readable by Sci-kit Learn
def parse_files(fileList, args): 
	numPostsPerSubTrain = [] #to construct labels
	numPostsPerSubTest = []
	trainX = []
	testX = []
	cutoff = 10
	testYTitles = []
	for fileName in fileList:
		subreddit = fileName[5:-4]
		labelToSubreddit.append(subreddit)
		with open(fileName, 'rb') as redditFile:
			redditReader = csv.reader(redditFile)
			numTrainPosts = 0
			numTestPosts = 0
			i = 0
			for post in redditReader:
				#title = post[4].split()
				#words = collections.Counter()
				#for word in title:
				#	words[word] += 1
				words = FeatureExtractor.extractFeatures(post[4], args)
				#binarize_features(words)
				if i % cutoff == 0:
					numTestPosts += 1
					testX.append(dict(words))
					testYTitles.append((words, subreddit))
				else:
					numTrainPosts += 1
					trainX.append(dict(words))
				i += 1
			numPostsPerSubTrain.append(numTrainPosts)
			numPostsPerSubTest.append(numTestPosts)
	dictVectorizer = DictVectorizer()
	dictVectorizer.fit(trainX + testX)
	trainX=dictVectorizer.transform(trainX)
	trainY = createLabels(numPostsPerSubTrain)
	testX =dictVectorizer.transform(testX)
	testY = createLabels(numPostsPerSubTest)
	return (trainX, trainY, testX, testY, testYTitles)
<<<<<<< HEAD
	
=======


def remove_punctuation(title):
	exlusionSet = set(string.punctuation)
	exlusionSet.remove("\'")
	#exlusionSet.remove("-")
	title = title.replace("-", " ")
	return ''.join(c for c in title if c not in exlusionSet)


#read in files, output them into train and test as required for libshorttxt format
#label<tab>title 
def parse_files_for_libsvm_shorttxt(fileList, out_train_file, out_test_file, args):
	train_f = open(out_train_file, 'wb')
	test_f = open(out_test_file, 'wb')
	test_cutoff = 10
	for fileName in fileList:
		subreddit = fileName[5:-4]
		with open(fileName, 'rb') as redditFile:
			redditReader = csv.reader(redditFile)
			i = 0
			for post in redditReader:
				words = remove_punctuation(post[4])
				if i % test_cutoff == 0:
					#testX.append(dict(words))
					#testYTitles.append((words, subreddit))
					test_f.write("%s\t%s\n" %  (subreddit, words))
					
				else:
					train_f.write("%s\t%s\n"% (subreddit, words))

				i += 1



>>>>>>> 5c59245528e7fc38f19e2cbb54ce9f2720621890
#unused (not helpful)
#takes a counter dict, replaces all non-zero values with 1
def binarize_features(featureDict):
	for key in featureDict.iterkeys():
		if featureDict[key] != 0:
			featureDict[key] = 1


#takes in a list of number of posts per sub, 
#returns corresponding numpy array of labels, 
#e.g. [4, 3] -> [0,0,0,0,1,1,1]
def createLabels(numPostsPerSub):
	size = sum(numPostsPerSub)
	labels = np.empty((size, 1))
	index = 0
	for y in range(len(numPostsPerSub)):
		for _ in range(numPostsPerSub[y]):
			labels[index] = y
			index += 1
	return labels


def runErrorAnalysis(testY, predY, testYTitles, numExamples = 10):
    count = 0
    for test, pred, title in zip(testY, predY, testYTitles):
        if test != pred:
            count+= 1
            print str(title) + " predicted: " + str(labelToSubreddit[ int(pred)])
            if count == numExamples:
                break


def crossValidate(clf, trainX, trainY, cv):
    scores = cross_validation.cross_val_score(clf, trainX, trainY.ravel(), cv=cv)
    print scores
    print "average: " + str(sum(scores)/len(scores))


def runMultinomialNaiveBayes(trainX, trainY, testX, testY, numLabels, testYTitles):
	clf = MultinomialNB()

	crossValidate(clf, trainX, trainY, numLabels)
	clf.fit(trainX, trainY.ravel())
	print clf.score(testX, testY.ravel())
	predY = clf.predict(testX)
	cm = confusion_matrix(testY, predY)
	print cm
	runErrorAnalysis(testY, predY, testYTitles)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
# <<<<<<< HEAD
#     parser.add_argument('fileNames', nargs='*')
#     parser.add_argument('--opt1', action='store_true')
#     parser.add_argument('--opt2', action='store_true')
#     parser.add_argument('--opt3', action='store_true')
#     parser.add_argument('--charFeatures', action = 'store_true', default=False)
#     parser.add_argument('--naivebayes', action='store_true', default=True)
#     parser.add_argument('--lemmatize', default=False)
#     parser.add_argument('--stem', default = False)
# =======
    parser.add_argument('fileNames', nargs='*',
        help='add an arbitary number of subreddit CSV files')
    parser.add_argument('--opt1', action='store_true',
        help='removes punctuation (except apostrophes) from the title')
    parser.add_argument('--opt2', action='store_true',
        help='changes contractions to their root words')
    parser.add_argument('--opt3', action='store_true',
        help='removes common filler words from the feature vector')
    parser.add_argument('--charFeatures', action='store_true',
        help='changes from word features to character features')
    parser.add_argument('--n', type=int, default=5,
        help='specify the number of characters in an n-gram feature vector')
    parser.add_argument('--noShuffle', action='store_true',
        help='do not shuffle the training and test data files')
    parser.add_argument('--stem', action='store_true',
        help='add word stemming')
    parser.add_argument('--lemmatize', action='store_true',
        help='add lematization to the feature vector')
    parser.add_argument('--naivebayes', action='store_true', default=True,
        help='this is only here to fix the namespace. naivebayes is a separate \
        file')
#>>>>>>> 5c59245528e7fc38f19e2cbb54ce9f2720621890
    args = parser.parse_args()

    numLabels = len(args.fileNames)
    (trainX, trainY, testX, testY, testYTitles) = parse_files(args.fileNames, args)
    runMultinomialNaiveBayes(trainX, trainY, testX, testY, numLabels, testYTitles)


    