#mmba_investigate.py
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

now = time.localtime(time.time())
print "    start time:", time.asctime(now)

myConn = "dbname=" + db + " host=" + myHost + " port=" + myPort + " user=" + myUser
conn = psycopg2.connect(myConn)
cur = conn.cursor()


myDir = "/Users/feomike/downloads/mmba_downloads/json/"    	    
#directory, and process each json file one at a time
for dirpath, dirs, files in os.walk(myDir):
	for file in fnmatch.filter(files, '*.json'):
		try:
#			print file		
			json_data = open(dirpath + "/" + file)
			data = json.load(json_data)     
			json_data.close() 
			myNetType = 'netType'
			myNetOpName = 'NetOpName'
			myNetOpCode = 'netOpCode'
			if data["metrics"][1]["type"] == "network_data":
				#network_data is usually position 1 in the metrics dictionary
				myNetType = data["metrics"][1]["network_type"] #is there
				#some names are non-ascii, do a conversion to take care of this
				myNetOpName = data["metrics"][1]["network_operator_name"].encode('ascii','ignore')
				myNetOpCode = data["metrics"][1]["network_operator_code"]				
				myNetOpName = string.replace(myNetOpName, "'", "")
			myVer = data["app_version_name"]
			mySubType = data["submission_type"]
			myTests = len(data["tests"])
			t = 0
			myDS = -9999
			while t < len(data["tests"]):
				if data["tests"][t]["type"] == "JHTTPGETMT" or \
						data["tests"][t]["type"] == "JHTTPGET": 
					myDS = data["tests"][t]["bytes_sec"]   
				t = t + 1
			myMetrics = len(data["metrics"])
			locExists = 0
			l = len(data["metrics"]) - 1
			while l > 0: 
				if data["metrics"][l]["type"] == "location":
					locExists = 1
				l = l - 1
			theStr = "'" + file + "','"
			theStr = theStr + myNetType + "','" + myNetOpName + "','"
			theStr = theStr + myNetOpCode + "','" + myVer + "','" + mySubType + "'," 
			theStr = theStr + str(myTests) + "," + str(myDS) + ","
			theStr = theStr + str(myMetrics) + "," + str(locExists)
			mySQL = "INSERT INTO " + schema + ".log VALUES (" 
			mySQL = mySQL + theStr + "); Commit;"
#			print mySQL
			cur.execute(mySQL)
		except ValueError:
			print '      file: ' + dirpath + '/' + file + ' is not valid'
					
now = time.localtime(time.time())
print "    end   time:", time.asctime(now)
