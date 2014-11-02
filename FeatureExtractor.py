import json
import collections

def extractFeatures(title):
	"""
	Get word features for title
	Use word frequencies (to start)
	Return dictionary
	"""
	featureVector = collections.Counter()
	tokens = title.split()
	# FIXME: we can remove stop words here
	[featureVector.update([word]) for word in tokens]
	return featureVector