Reddit Classifier
=================
Classify Reddit post titles to the most likely subreddit

## Prerequisites
### nltk
Install the python nltk package by following the directions [here](http://www.nltk.org/install.html)
### scikit-learn
Install the scikit-learn package by following the directions [here](http://scikit-learn.org/stable/install.html)
### numpy
Install the numpy package by following the directions [here](http://www.numpy.org)
### LibShortText
Package and installation instructions can be found [here](http://www.csie.ntu.edu.tw/~cjlin/libshorttext/)


## How to run classification using linear regression
```
python linearRegression.py [-h] [--opt1] [--opt2] [--opt3] [--charFeatures]
                           [--n N] [--noShuffle] [--stem] [--lemmatize]
                           [--verbose] [fileNames [fileNames ...]]
```
example:
```
python linearRegression.py --opt1 --opt3 data/ArtHistory.csv data/BBQ.csv data/Pizza.csv
```

positional arguments:
```
  fileNames                  an arbitary number of subreddit CSV files
```
optional arguments:
```
  -h, --help                 show this help message and exit
  --opt1                     removes punctuation (except apostrophes) from the title. Replaces dashes with spaces
  --opt2                     change contractions to their root words
  --opt3                     removes common filler words from the feature vector
  --charFeatures             changes from word-based features (default) to character-based features
  --n N                      specify the number of characters (N) in an n-gram feature (default is 5)
  --noShuffle                do not shuffle the data sets (useful for testing and debugging)
  --stem                     add word stemming
  --lemmatize                add lemmatization to the word feature
  --verbose                  print out statistics about classification accuracy and errors
```

## How to run classification using Naive Bayes
```
python naiveBayes.py [-h] [--opt1] [--opt2] [--opt3]
                     [--noShuffle] [--stem] [--lemmatize] [--naivebayes]
                     [--verbose] [fileNames [fileNames ...]]
```
example:
```
python naiveBayes.py --lemmatize data/ArtHistory.csv data/BBQ.csv data/Pizza.csv
```

positional arguments:
```
  fileNames                  an arbitary number of subreddit CSV files
```
optional arguments:
```
  -h, --help                 show this help message and exit
  --opt1                     removes punctuation (except apostrophes) from the title. Replaces dashes with spaces
  --opt2                     change contractions to their root words
  --opt3                     removes common filler words from the feature vector
  --stem                     add word stemming
  --lemmatize                add lemmatization to the word feature
```

## How to run classification using support vector machines (SVM)
```
./run_svm.sh
```
The first line of this file parses the files of the relevant subreddits into training and test files to be used by the SVM. The number of CSV is arbitrary and more or different ones can be added.
The subsequent lines train and test the SVM. The meanings of the flags can be read within the README provided by LibShortText.
