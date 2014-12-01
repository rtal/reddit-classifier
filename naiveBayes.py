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

def runMultinomialNaiveBayes(trainX, trainY, testX, testY, numLabels, testYTitles):
	clf = MultinomialNB()

	crossValidate(clf, trainX, trainY, numLabels)
	clf.fit(trainX, trainY.ravel())
	print clf.score(testX, testY.ravel())
	predY = clf.predict(testX)
	cm = confusion_matrix(testY, predY)
	print cm
	runErrorAnalysis(testY, predY, testYTitles)


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

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('fileNames', nargs='*',
    	help='add an arbitary number of subreddit CSV files')
    parser.add_argument('--opt1', action='store_true',
    	help='removes punctuation (except apostrophes) from the title')
    parser.add_argument('--opt2', action='store_true',
    	help='changes contractions to their root words')
    parser.add_argument('--opt3', action='store_true',
    	help='removes common filler words from the feature vector')
    parser.add_argument('--naivebayes', action='store_true', default=True,
    	help='tells the feature extractor to optimize for naive bayes')
    args = parser.parse_args()

    numLabels = len(args.fileNames)
    (trainX, trainY, testX, testY, testYTitles) = parse_files(args.fileNames, args)
    runMultinomialNaiveBayes(trainX, trainY, testX, testY, numLabels, testYTitles)


    