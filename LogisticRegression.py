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

	def gradLoss(phiX, w, y):
		score = dotProduct(w, phiX)
		margin = score * y
		grad = 0
		if margin < 1:
			grad = -1 * features * y
		return grad

	for label in subredditLabels:
		weightVector = weightDict[label]
		for i in range(numIterations):
			for example in trainingSet:
				example = json.loads(example)
				title = example['title']
				subreddit = example['subreddit']

				features = FeatureExtractor.extractFeatures(title)

				# currentWeightVector = weightDict[subreddit]

				y = -1
				if label == subreddit:
					y = 1

				grad = gradLoss(features, currentWeightVector, y)




if __name__ == '__main__':
	train(trainingSet, subredditLabels)
