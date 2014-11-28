import collections
import string
import copy
from nltk.stem.wordnet import WordNetLemmatizer
from nltk.stem.porter import PorterStemmer
from nltk.stem.lancaster import LancasterStemmer
from nltk.stem.snowball import SnowballStemmer


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
        title = ''.join(c for c in title if c not in exlusionSet)
    
    tokens = title.split()

    # more info: http://textminingonline.com/tag/wordnet-lemmatizer
    # and: http://nlp.stanford.edu/IR-book/html/htmledition/stemming-and-lemmatization-1.html
    # and also this: http://stackoverflow.com/questions/15586721/wordnet-lemmatization-and-pos-tagging-in-python

    # newTokens = list()
    # lemmatizer = WordNetLemmatizer()
    # for t in tokens:
    #     newTokens.append(lemmatizer.lemmatize(t))
    # tokens = copy.deepcopy(newTokens)

    if args.opt4:
        newTokens = list()
        stemmer = PorterStemmer()
        for t in tokens:
            newToken = stemmer.stem(t)
            print newToken
            newTokens.append(newToken)
        tokens = copy.deepcopy(newTokens)

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