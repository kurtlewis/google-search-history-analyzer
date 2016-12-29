"""
Kurt Lewis
Taking json data from an export of my google and looking at it
"""
import json
import argparse
import matplotlib.pyplot as plt
import numpy
import math
from os import listdir
from os.path import isfile, join

#Configure arguments
parser = argparse.ArgumentParser(
    description="A Tool to examine a folder containing json data from google's takeout tool",
    epilog="If any plots are displayed, they must be closed before the program can complete")
parser.add_argument("directory", type=str, 
    help="The name of the folder containing json dumps. Typically Takeout/Searches/")
parser.add_argument("-f", "--frequentSearches", action="store_true",
    help="Display the most frequently made searches")
parser.add_argument("-d", "--searchesPerDay", action="store_true",
    help="Display a graph of how many searches have been made per day")
parser.add_argument("-w", "--searchesPerDayOfWeek", action="store_true",
    help="Display average number of searches per day of the week")

args = parser.parse_args()

jsonFiles = [f for f in listdir(args.directory) if isfile(join(args.directory, f))]

# queries is a dictionary where each key is a specific search, and
# each key returns a list of timestamps where that key was searched for
queries = dict()
# queriesTimeStamps holds a list of every timestamp from every search
queriesTimeStamps = list()

for jsonFile in jsonFiles:
    with open(args.directory + jsonFile, 'r') as data_file:
        data = json.loads(data_file.read())
        for query in data['event']:
            query = query['query']
            query_text = query['query_text']
            timestamps = list()
            for timestamp in query['id']:
                timestamps.append(timestamp['timestamp_usec'])
            if query_text in queries:
                l = queries[query_text]
                # The list of timestamps might not exist, even if its been added to the dictionary
                if l:
                    queries[query_text] = l + timestamps
                else:
                    queries[query_text] = timestamps

            else:
                queries[query_text] = timestamps
            queriesTimeStamps = queriesTimeStamps + timestamps

# Plot the time frequency of searching
if args.searchesPerDay or args.searchesPerDayOfWeek:
    conversionToSecs = 1000000
    conversionToDays = 86400000000
    queriesTimeStamps.sort()
    queriesDays = [math.floor(int(timestamp)/conversionToDays) for timestamp in queriesTimeStamps]
    firstSearch = int(min(queriesDays))
    lastSearch = int(max(queriesDays))


    if args.searchesPerDay:
        xAxis = numpy.linspace(firstSearch,
            lastSearch, lastSearch-firstSearch)


        yAxis = list()
        last = 0
        for i in range(lastSearch - firstSearch):
            num = 0
            for j in range(len(queriesDays) + 1 - last):
                if (math.floor(queriesDays[j + last])/(firstSearch+i) == 1):
                    num = num + 1
                else:
                    last = j + last
                    break
            yAxis.append(num)

        plt.bar(xAxis, yAxis)
        plt.show()

    if args.searchesPerDayOfWeek:
        xTicks = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
        xAxis = [1,2,3,4,5,6,7]
        yAxis = [1,2,3,4,5,6,7]
        plt.bar(xAxis, yAxis)
        plt.xticks([1,2,3,4,5,6,7], xTicks)
        plt.show()

if args.frequentSearches:
    # Top searched items
    # I should learn how to use tuples
    topSearches = ["Temp"]
    topSearchesNums = [0]
    for key in queries:
        numSearches = len(queries[key])
        for i, num in enumerate(topSearchesNums):
            if numSearches > num:
                topSearches.insert(i, key)
                topSearchesNums.insert(i, numSearches)
                break
            if i == 100:
                break

    for i, search in enumerate(topSearches):
        print(str(i) + ":(" + str(topSearchesNums[i])+ ") " + search)
        if i == 100:
            break
