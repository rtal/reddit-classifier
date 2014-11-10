import sys
import json
import collections
import extractData
import FeatureExtractor
import util
import argparse
import operator

# One-vs-All learner
def train(trainingSet, subredditLabels, args):
    numIterations = 20
    eta = 0.05

    #dictionary of dictionaries (weights)
    weightDict = {}
    for label in subredditLabels:
        weightDict[label] = {}


    def gradLoss(phiX, w, y):
        score = util.dotProduct(w, phiX)
        margin = score * y
        if margin < 1:
            for name, feature in phiX.iteritems():
                phiX[name] = -1 * y * feature
            return phiX
        else:
            return 0


    for label in subredditLabels:
        trainingSet.seek(0)
        weightVector = weightDict[label]
        for i in range(numIterations):
            for example in trainingSet:
                example = json.loads(example)
                title = example['title']
                subreddit = example['subreddit']

                features = FeatureExtractor.extractFeatures(title, args)

                y = -1
                if label == subreddit:
                    y = 1

                grad = gradLoss(features, weightVector, y)

                if grad != 0:
                    util.increment(weightVector, -1 * eta, grad)
                    weightDict[label] = weightVector
                else:
                    weightDict[label] = weightVector

    return weightDict


def predict(weights, testSet, args):
    correct = 0
    incorrect = 0
    total = 0
    for data in testSet:
        data = json.loads(data)
        title = data['title']
        subreddit = data['subreddit']
        features = FeatureExtractor.extractFeatures(title, args)
        maxScore = float('-inf')
        prediction = ''

        for key in weights.keys():
            weightVector = weights[key]

            score = util.dotProduct(weightVector, features)
            if score > maxScore:
                prediction = key
                maxScore = score

        if prediction == subreddit:
            correct += 1
        else:
            # try:
            #     print title
            #     print "predicted: " + prediction.encode('utf-8')
            #     print features
            #     # printRelevantWeights(weights, features)
            #     print "-----------------"


            # except UnicodeEncodeError:
            #     print "error"
            incorrect += 1
        total += 1


    print 'accuracy ' + str(float(correct) / total)
    print 'wrong ' + str(float(incorrect) / total)

def printRelevantWeights(weightDict, wordFeatures):
    for subredditKey in weightDict.keys():
        print "subreddit: " + str(subredditKey) 
        for wordKey in wordFeatures.keys():
            print "key: " + str(wordKey)
            print "weight: " + str(weightDict[subredditKey].get(wordKey, 0))


def printSortedWeights(weightDict):
    for key in weightDict.keys():
        print "for key: " + str(key)
        sorted_x = sorted(weightDict[key].items(), key=operator.itemgetter(1))
        print sorted_x
        print "========================================"
        print "========================================"
        print "========================================"
        print "========================================"


""" To run this program:
python LogisticRegression.py [fileNames] [--opt1] [--opt2] [...]

fileNames (required): as many csv files as you want, separated by spaces.
--opt1 (optional): Optimization to remove punctuation (except apostrophes)
        from the title
--opt2 (optional): optimization to remove common filler words from the
        feature vector.
--opt3 (optional): optimization to change contractions to expanded words,
        preserving the count of the contraction
"""

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('fileNames', nargs='*')
    parser.add_argument('--opt1', action='store_true')
    parser.add_argument('--opt2', action='store_true')
    parser.add_argument('--opt3', action='store_true')
    args = parser.parse_args()

    subredditLabels = []
    for f in args.fileNames:
        subredditLabels.append(f[5:-4])

    extractData.parseData(args.fileNames)
    with open('TrainDataShuffled.txt', 'r') as trainingSet:
        weightDict = train(trainingSet, subredditLabels, args)
    with open('TestDataShuffled.txt', 'r') as testSet:
        predict(weightDict, testSet, args)
    
    # printSortedWeights(weightDict)
