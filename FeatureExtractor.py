import json
import collections

def extractFeatures(title):
	"""
	Get word features for title
	Use word frequencies (to start)
	Return dictionary
	"""
	tokens = title.split()
	featureVector = collections.Counter(tokens)
	return featureVector