import sys
import extractData
import json

extractData.parseData(sys.argv[1:])
with open('data.txt', 'r') as f:
    for line in f:
        line = json.loads(line)
        print line