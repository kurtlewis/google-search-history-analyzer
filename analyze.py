"""
Kurt Lewis
Taking json data from an export of my google and looking at it
"""
import json
import argparse

#Configure arguments
parser = argparse.ArgumentParser(
    description="A Tool to examine a folder containing json data from google's takeout tool")
parser.add_argument("directory", type=str, 
    help="The name of the folder containing json dumps. Typically Takeout/Searches/")

args = parser.parse_args()


