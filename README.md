Reddit Classifier
=================
Classify Reddit post titles to the most likely subreddit

## Prerequisites
### nltk
Install the python nltk package by following the directions [here](http://www.nltk.org/install.html)
### scikit-learn
Install the scikit-learn package by following the directions [here](http://scikit-learn.org/stable/install.html)

## How to run classification using linear regression
usage: linearRegression.py   [-h] [--opt1] [--opt2] [--opt3] [--charFeatures]
                             [--n N] [--noShuffle] [--stem] [--lemmatize]
                             [--naivebayes] [--verbose]
                             [fileNames [fileNames ...]]

positional arguments:
  fileNames       add an arbitary number of subreddit CSV files

optional arguments:
  -h, --help      show this help message and exit
  
  --opt1          removes punctuation (except apostrophes) from the title
  
  --opt2          changes contractions to their root words
  
  --opt3          removes common filler words from the feature vector
  
  --charFeatures  changes from word features to character features
  
  --n N           specify the number of characters in an n-gram feature vector
  
  --noShuffle     do not shuffle the training and test data files
  
  --stem          add word stemming
  
  --lemmatize     add lematization to the feature vector
  
  --naivebayes    this is only here to fix the namespace. naivebayes is a separate file
  
  --verbose       print out useful statistical information regarding classification

### Notes on combining optimizations:
    --opt1, --opt2, and --opt3 can be used in conjunction or by themselves
    --charFeatures has a default feature length of 5, use --n [integer] to set the feature size
    --charFeatures and --opt1 can be used together
    --stem and --opt1, and --opt3 can be used together
    --lemmatize, --opt1 and --opt3 can be used together

## How to run classification using naive Bayes
usage: naiveBayes.py [-h] [--opt1] [--opt2] [--opt3] [--naivebayes]
                     [fileNames [fileNames ...]]

positional arguments:
  fileNames     add an arbitary number of subreddit CSV files

optional arguments:
  -h, --help    show this help message and exit
  
  --opt1        removes punctuation (except apostrophes) from the title
  
  --opt2        changes contractions to their root words
  
  --opt3        removes common filler words from the feature vector
  
  --naivebayes  tells the feature extractor to optimize for naive bayes
