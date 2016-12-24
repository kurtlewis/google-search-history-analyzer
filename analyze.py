"""
Kurt Lewis
Taking json data from an export of my google and looking at it
"""
import json
import argparse
from os import listdir
from os.path import isfile, join

#Configure arguments
parser = argparse.ArgumentParser(
    description="A Tool to examine a folder containing json data from google's takeout tool")
parser.add_argument("directory", type=str, 
    help="The name of the folder containing json dumps. Typically Takeout/Searches/")

args = parser.parse_args()

jsonFiles = [f for f in listdir(args.directory) if isfile(join(args.directory, f))]

queries = dict()
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
                    queries[query_text] = l.append(timestamps)
                else:
                    queries[query_text] = timestamps

            else:
                queries[query_text] = timestamps
            queriesTimeStamps.append(timestamps)

print(queries)
print(len(queriesTimeStamps))  

#text of search at following:
#print(data[2]['event'][0]['query']['query_text'])
#timestamp of query at following:
#print(data[2]['event'][0]['query']['id'][0]['timestamp_usec'])