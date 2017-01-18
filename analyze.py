"""
Kurt Lewis
Taking json data from an export of my google and looking at it
"""
import json
import argparse
import matplotlib.pyplot as plt
import numpy
import math
import time
import operator
from os import listdir
from os.path import isfile, join

#
# Define constants
#
CONVERSION_TO_SECS = 1000000
CONVERSION_TO_DAYS = 86400
#
# Define variables to be used program long
#
# Queries is a dictionary where each key is a specific search, and
## each key returns a list of timestamps where that key was searched for
queries = dict()
# QueriesTimeStamps holds a list of every timestamp from every search
queriesTimeStamps = list()
# Number of plots
numPlots = 3
numPlotsX = 3
numPlotsY = 1
currentPlot = 1

#
# Configure arguments
#
parser = argparse.ArgumentParser(
    description="A Tool to examine a folder containing json data from google's takeout tool",
    epilog="If any plots are displayed, they must be closed before the program can complete")
parser.add_argument("directory", type=str, 
    help="The name of the folder containing json dumps. Typically Takeout/Searches/")
args = parser.parse_args()

jsonFiles = [f for f in listdir(args.directory) if isfile(join(args.directory, f))]

#
# Read data
#
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

#
# Plot the time frequency of searching in searches per day
#
plt.subplot(numPlotsX,numPlotsY, currentPlot)
currentPlot = currentPlot + 1

queriesTimeStamps.sort()
#queriesTimeStamps = [math.floor(int(timestamp)/CONVERSION_TO_SECS) for timestamp in queriesTimeStamps]
queriesDays = [math.floor(int(timestamp)/(CONVERSION_TO_DAYS * CONVERSION_TO_SECS)) for timestamp in queriesTimeStamps]
firstSearch = int(min(queriesDays))
lastSearch = int(max(queriesDays))

totalNumOfDays = lastSearch - firstSearch
xAxis = numpy.linspace(firstSearch, lastSearch, totalNumOfDays)
xLabels = list()  
searchesPerDay = list()
last = 0
for i in range(totalNumOfDays):
    num = 0
    for j in range(len(queriesDays) + 1 - last):
        if (math.floor(queriesDays[j + last])/(firstSearch+i) == 1):
            num = num + 1
        else:
            last = j + last
            break
    searchesPerDay.append(num)
    if i % 100 == 0:
        xLabels.append(time.strftime("%Y/%m/%d", time.localtime(xAxis[i]*CONVERSION_TO_DAYS)))
    else:
        xLabels.append("")



plt.bar(xAxis, searchesPerDay)
plt.xticks(xAxis, xLabels)
plt.title("Searches Per Day")

#
# Plot the number of searches per week
#
plt.subplot(numPlotsX,numPlotsY, currentPlot)
currentPlot = currentPlot + 1

totalNumOfWeeks = math.ceil(totalNumOfDays / 7)
xAxis = numpy.linspace(firstSearch, lastSearch, totalNumOfWeeks-1)
searchesPerWeek = list()
xLabels = list()
for i in range(totalNumOfWeeks-1):
    num = 0
    for j in range(7):
        num = num + searchesPerDay[i * 7 + j]
    searchesPerWeek.append(num)
    if i % 8 == 0:
        xLabels.append(time.strftime("%Y/%m", time.localtime(xAxis[i]*CONVERSION_TO_DAYS)))
    else:
        xLabels.append("")



plt.plot(xAxis, searchesPerWeek)
plt.xticks(xAxis, xLabels)
plt.title("Searches Per Week")

#
# Plot the average number of searches per day of the week
#
plt.subplot(numPlotsX, numPlotsY, currentPlot)
currentPlot = currentPlot + 1

searchesOnDays = {"Monday": 0, "Tuesday": 0, "Wednesday": 0, "Thursday": 0, "Friday": 0, "Saturday": 0, "Sunday": 0}
for stamp in queriesTimeStamps:
    day = time.strftime("%A", time.localtime(int(stamp)))
    searchesOnDays[day] = searchesOnDays[day] + 1

weeksInDataSet = totalNumOfDays/7
for day in searchesOnDays:
    searchesOnDays[day] = searchesOnDays[day] / weeksInDataSet

yAxis = list(searchesOnDays.values())
xAxis = [1,2,3,4,5,6,7]
plt.bar(xAxis, yAxis)
plt.xticks([1,2,3,4,5,6,7], ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"])
plt.title("Average Searches Per Day of the Week")


# This command must come after the last plot has been created
plt.draw()




#
# Top searched items
#
print("********************************************************************************")
print("                            Top Searched Queries")
print("********************************************************************************")
topSearches = list()
# add a temporary search for comparing
topSearches.append(("Temporary", -1))
for key in queries:
    numSearches = len(queries[key])
    for i, search in enumerate(topSearches):
        if numSearches > search[1]:
            topSearches.insert(i, (key, numSearches))
            break
        # There only needs to be a list of the top 100
        if i == 100:
            break

for i, search in enumerate(topSearches):
    print(str(i + 1) + ":(" + str(search[1])+ ") " + search[0])
    if i == 100:
        break

#
# Number of searches per word
#
print("\n\n\n")
print("********************************************************************************")
print("                            Top Searched Words")
print("********************************************************************************")
searchedWords = dict()
for key in queries:
    key = key.strip(',')
    words = key.split(" ")
    for word in words:
        if word in searchedWords:
            searchedWords[word] += 1
        else:
            searchedWords[word] = 1

# This algorithm sorts the words in advancing order, so reverse it
topSearchedWords = sorted(searchedWords.items(), key=operator.itemgetter(1))
topSearchedWords.reverse()
#set max 
tableMax = 200
if len(topSearchedWords) < tableMax * 3:
    tableMax = math.floor(len(topSearchedWords)/3) - 1

for i in range(len(topSearchedWords)):
    print("{:3d}:({:4d}) {:12}    {:3d}:({:4d}) {:12}    {:3d}:({:4d}) {:12}".format(i, topSearchedWords[i][1], topSearchedWords[i][0], i + tableMax, topSearchedWords[i+tableMax][1], topSearchedWords[i+tableMax][0], i + tableMax * 2, topSearchedWords[i + tableMax * 2][1], topSearchedWords[i+ tableMax * 2][0]))
    if i > tableMax:
        break

plt.show()