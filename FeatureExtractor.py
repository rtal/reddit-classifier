import json
import collections

IGNORED_WORDS = [
    'the', 'The',
    'a', 'A',
    'an', 'An',
    'or', 'Or',
    'is', 'Is',
    'and',
    'which',
    'on'
]

def extractFeatures(title):
    """
    Get word features for title
    Use word frequencies (to start)
    Return dictionary
    """
    tokens = title.split()

    featureVector = collections.Counter(tokens)

    # Remove the IGNORED_WORDS from the feature vector
    for word in IGNORED_WORDS:
        featureVector.pop(word, None)

    return featureVector