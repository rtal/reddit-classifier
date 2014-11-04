import sys
import json
import collections
import extractData
import FeatureExtractor
import util

# One-vs-All learner
def train(trainingSet, subredditLabels):
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

                features = FeatureExtractor.extractFeatures(title)

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


def predict(weights, testSet):
    correct = 0
    incorrect = 0
    total = 0
    for data in testSet:
        data = json.loads(data)
        title = data['title']
        subreddit = data['subreddit']
        features = FeatureExtractor.extractFeatures(title)
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
            incorrect += 1
        total += 1


    print 'accuracy ' + str(float(correct) / total)
    print 'wrong ' + str(float(incorrect) / total)



if __name__ == '__main__':
    subredditLabels = ['ArtHistory', 'Disneyland']
    extractData.parseData(sys.argv[1:])
    with open('TrainData.txt', 'r') as trainingSet:
        weightDict = train(trainingSet, subredditLabels)
        # print weightDict['ArtHistory']
        # print
        # print 
        # print
        # print weightDict['Disneyland']
    with open('TestData.txt', 'r') as testSet:
        predict(weightDict, testSet)
