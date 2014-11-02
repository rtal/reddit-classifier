import sys
import json
import collections
import extractData
import FeatureExtractor
import util

def train(trainingSet, subredditLabels):
	numIterations = 20
	eta = 0.05

	#dictionary of dictionaries (weights)
	weightDict = {}

	for i in range(numIterations):
		for example in trainingSet:
			example = json.loads(example)
			title = example['title']
			subreddit = example['subreddit']

			features = FeatureExtractor.extractFeatures(title)

			currentWeightVector = weightDict[subreddit]

			maxScore = float('-inf')
			for label in subredditLabels:
				weightVector = weightDict[label]

				score = dotProduct(weightVector, features) - dotProduct(currentWeightVector, features)
				if label != subreddit:
					score = score + 1

				if score > maxScore:
					maxScore = score

			currentWeightVector = currentWeightVector - eta * 


if __name__ == '__main__':
	train(trainingSet, subredditLabels)
