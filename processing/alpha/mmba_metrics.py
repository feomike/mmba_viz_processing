#mmba_metrics.py
#mike Byrne
#federal communications commission
#oct. 28, 2013
#import the .json file into a csv

import os
import json
import pprint
import string
import psycopg2
import time
import unicodedata
import fnmatch

#global variables - database connection
myHost = "localhost"
myPort = "54321"
myUser = "postgres"
db = "feomike"
schema = "mmba_5k"
cnt = 0
#set up a global array to hold values for the update of the 'type' tables
#this array is reset every loop of a json file, such that it can hold the appropriate
#values for updating;  we need to do this as a global array, b/c different fucntions
#return different values and i need one consistent place to hold the values to update

now = time.localtime(time.time())
print "    start time:", time.asctime(now)

myDir = "/Users/feomike/downloads/mmba_downloads/json/"    	    
#directory, and process each json file one at a time
for dirpath, dirs, files in os.walk(myDir):
	for file in fnmatch.filter(files, '*.json'):
		try:
			json_data = open(dirpath + "/" + file)
			data = json.load(json_data)     
			json_data.close() 
			if len(data["metrics"]) == 45:
				print dirpath + "/" + file		
				m = len(data["metrics"]) - 1
				while m > 0:
					print data["metrics"][m]["type"]
					m = m - 1
		except ValueError:
			cnt = cnt + 1
					
now = time.localtime(time.time())
print "    end   time:", time.asctime(now)
