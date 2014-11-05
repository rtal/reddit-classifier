import json
import collections

IGNORED_WORDS = [
    'the', 'The',
    'a', 'A',
    'an', 'An',
    'or', 'Or',
    'is', 'Is',
    'and', 'And',
    'which', 'Which',
    'on', 'Or',
    'who', 'Who',
]

CONTRACTIONS = {
    "can't": ['can', 'not'],
    "Can't": ['can', 'not'],
    "cannot": ['can', 'not'],
    "Cannot": ['can', 'not'],
    "won't": ['will', 'not'],
    "Won't": ['will', 'not'],
    "shouldn't": ['should', 'not'],
    "Shouldn't": ['should', 'not'],
    "I'm": ['I', 'am'],
    "i'm": ['I', 'am'],
    "He's": ['He' 'is'],
    "he's": ['He' 'is'],
    "She's": ['She', 'is'],
    "she's": ['She', 'is']
}

def extractFeatures(title, args):
    """
    Get word features for title
    Use word frequencies (to start)
    Return dictionary
    """
    tokens = title.split()

    featureVector = collections.Counter(tokens)

    # Optimization 1: Change contractions to their component words
    if args.opt1:
        toAdd = {}
        for word in CONTRACTIONS:
            exists = featureVector.pop(word, 0)
            if exists > 0:
                for replacement in CONTRACTIONS[word]:
                    featureVector[replacement] = exists

    # Optimization 2: remove IGNORED_WORDS from the feature vector
    if args.opt2:
        for word in IGNORED_WORDS:
            featureVector.pop(word, None)

    return featureVector