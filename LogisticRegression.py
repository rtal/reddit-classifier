import sys
import json
import collections
import extractData
import FeatureExtractor
import util

def makeTrainingSet(subredditFiles):
	extractData.parseData(subredditFiles)
	with open('data.txt', 'r') as dataFile:
		






if __name__ == '__main__':
	makeTrainingSet(sys.argv[1:])