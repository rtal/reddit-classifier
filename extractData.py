import sys
import csv
import json


def parseData(fileList):
    """ Input: many files from the Reddit database input as command line arguments
        Output: text file with only the relevant information from each file in a
                JSON format ({'subreddit': [name of subreddit], 'title': [post title]})
        Note that the data.txt file is overwritten each time this script is called.
        This behavior may be modified in the future so that new data is appended.
    """
    with open('Data.txt', 'wb') as dataFile:
        dataFile.truncate()
        for fileName in fileList:
            subreddit = fileName.strip('.csv').strip('data/')
            with open(fileName, 'rb') as redditFile:
                redditReader = csv.reader(redditFile)
                for post in redditReader:
                    dataFile.write(json.dumps({'title': post[4], 'subreddit': subreddit}) + '\n')


def printData():
    """ Open the data.txt file and de-serialize each JSON string representing a single
        title-subreddit pair. Print the title. This is the main logic that will be used
        for reading the data file and training the weight vector later on.
    """
    with open('data.txt', 'rb') as dataFile:
        for line in dataFile:
            dataPoint = json.loads(line)
            print dataPoint['title']