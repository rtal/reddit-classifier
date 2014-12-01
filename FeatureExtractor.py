import collections
import string
import copy
import nltk
from nltk.stem.wordnet import WordNetLemmatizer
from nltk.stem.porter import PorterStemmer
from nltk.stem.lancaster import LancasterStemmer
from nltk.stem.snowball import SnowballStemmer
from nltk.corpus import wordnet

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

    # more info: http://textminingonline.com/tag/wordnet-lemmatizer
    # and: http://nlp.stanford.edu/IR-book/html/htmledition/stemming-and-lemmatization-1.html

    tokens = title.split()
    featureVector = collections.Counter(tokens)

    # Optimization: lemmatization using WordNet corpus
    if args.lemmatize:
        # from: http://stackoverflow.com/questions/15586721/wordnet-lemmatization-and-pos-tagging-in-python
        def getWordNetPos(tag):
            if tag.startswith('J'):
                return wordnet.ADJ
            elif tag.startswith('V'):
                return wordnet.VERB
            elif tag.startswith('N'):
                return wordnet.NOUN
            elif tag.startswith('R'):
                return wordnet.ADV
            else:
                return None
        newTokens = list()
        lemmatizer = WordNetLemmatizer()
        wordTags = nltk.pos_tag(tokens)
        for (token, tag) in wordTags:
            wordnetTag = getWordNetPos(tag)
            if wordnetTag is not None:
                newTokens.append(lemmatizer.lemmatize(token, wordnetTag))
            else:
                newTokens.append(lemmatizer.lemmatize(token))
        tokens = copy.deepcopy(newTokens)

    # Optimization: Stemming using PorterStemmer
    # stemming relies on language's spelling rules, without
    # semantic understanding of the language itself
    if args.stem:
        newTokens = list()
        stemmer = PorterStemmer()
        for t in tokens:
            newToken = stemmer.stem(t)
            # print newToken
            newTokens.append(newToken)
        tokens = copy.deepcopy(newTokens)

        return featureVector


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