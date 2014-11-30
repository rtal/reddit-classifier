import collections
import string

IGNORED_WORDS = [
    'the','a', 'an', 'or', 'is', 'and',
    'which','on', 'who', 'they', 'of', 'he',
    'she', 'anybody', 'it', 'without', 'between',
    'that', 'my', 'more', 'much', 'either',
    'neither', 'when', 'while', 'although', 'be',
    'am', 'are', 'got', 'do', 'no', 'nor', 'as'
]

CONTRACTIONS = {
    "can't": ['can', 'not'],
    "cannot": ['can', 'not'],
    "won't": ['will', 'not'],
    "shouldn't": ['should', 'not'],
    "i'm": ['I', 'am'],
    "he's": ['he' 'is'],
    "she's": ['she', 'is'],
    "it's": ['it', 'is'],
    "wouldn't": ['would', 'not'],
    "couldn't": ['could', 'not']
}

def extractFeatures(title, args):
    """
    Get word features for title
    Use word frequencies (to start)
    Return dictionary
    """
    
    # Optimization 1: Remove punctuation
    if args.opt1:
        exlusionSet = set(string.punctuation)
        exlusionSet.remove("\'")
        if args.naivebayes:
            exlusionSet.remove("-")
        title = title.replace("-", " ")
        title = ''.join(c for c in title if c not in exlusionSet)

    if args.charFeatures:
        noSpaces = list(''.join(title.split()))
        featureVector = collections.Counter()
        if (len(noSpaces)) < args.n:
            return featureVector
        for i in range(0, len(noSpaces) - (args.n - 1), 1):
            nGram = ''.join(noSpaces[i : i+args.n])
            featureVector[nGram] = featureVector[nGram] + 1

        return featureVector


    tokens = title.split()
    featureVector = collections.Counter(tokens)

    # Optimization 2: Change contractions to their component words
    if args.opt2:
        for word in CONTRACTIONS:
            exists = featureVector.pop(word, 0)
            if exists > 0:
                for replacement in CONTRACTIONS[word]:
                    featureVector[replacement] = exists

    # Optimization 3: remove IGNORED_WORDS from the feature vector
    if args.opt3:
        for word in IGNORED_WORDS:
            featureVector.pop(word, None)

    return featureVector