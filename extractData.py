import sys
import csv
import json
import random


def parseData(fileList):
    """ 
    Input: many files from the Reddit database input as command line
            arguments
    Output: text file with only the relevant information from each file in a
        JSON format ({'subreddit': [name of subreddit], 'title': [post title]})
    
    Note that the data.txt file is overwritten each time this script is called.
    This behavior may be modified in the future so that new data is appended.
    """
    cutoff = 10
    with open('TrainData.txt', 'wb') as trainFile:
        with open('TestData.txt', 'wb') as testFile:
            trainFile.truncate()
            testFile.truncate()
            for fileName in fileList:
                i = 0
                subreddit = fileName[5:-4]
                # subreddit = fileName.strip('.csv').strip('data/')
                with open(fileName, 'rb') as redditFile:
                    redditReader = csv.reader(redditFile)
                    for post in redditReader:
                        if i % cutoff == 0:
                            testFile.write(json.dumps({'title': post[4].lower(), 'subreddit': subreddit}) + '\n')
                        else:
                            trainFile.write(json.dumps({'title': post[4].lower(), 'subreddit': subreddit}) + '\n')
                        i += 1
    shuffleData()


# Shuffling a file: http://stackoverflow.com/questions/4618298/randomly-mix-lines-of-3-million-line-file
def shuffleData():
    with open('TrainData.txt', 'r') as train:
        data = [(random.random(), line) for line in train]
        data.sort()
        with open('TrainDataShuffled.txt', 'w') as actualTrain:
            actualTrain.truncate()
            for rand, line in data:
                actualTrain.write(line)

    with open('TestData.txt', 'r') as test:
        data = [(random.random(), line) for line in test]
        data.sort()
        with open('TestDataShuffled.txt', 'w') as actualTest:
            actualTest.truncate()
            for rand, line in data:
                actualTest.write(line)


def printData(fileName):
    """ Open the file and de-serialize each JSON string representing a 
    single title-subreddit pair. Print the title. This is the main logic 
    that will be used for reading the data file and training the weight 
    vector later on.
    """
    with open(fileName, 'rb') as dataFile:
        for line in dataFile:
            dataPoint = json.loads(line)
            print dataPoint['title']