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

#global variables - database connection
myHost = "localhost"
myPort = "54321"
myUser = "postgres"
db = "feomike"
schema = "mmba"

#set up how the script should run; change this variables to load only specific data
#from a certain month 
#month variables
month = "09"
print "    working on month: " + month + "..."

#set up a global array to hold values for the update of the 'type' tables
#this array is reset every loop of a json file, such that it can hold the appropriate
#values for updating;  we need to do this as a global array, b/c different fucntions
#return different values and i need one consistent place to hold the values to update

now = time.localtime(time.time())
print "    start time:", time.asctime(now)

myConn = "dbname=" + db + " host=" + myHost + " port=" + myPort + " user=" + myUser
conn = psycopg2.connect(myConn)
cur = conn.cursor()


#global variables - directory / provider 
provList = ["att","sprint","tmobile","vz"]
for prov in provList:
	#loop through all files w/i the myDir varibale
	myDir = "/Users/feomike/documents/analysis/2013/mmba/data/" + prov + \
    	    "/json/" + "2013" + month + "/"
	os.chdir(myDir)
	for file in os.listdir("."):
		if file.endswith(".json"):
			#print file		
			json_data = open(file)
			data = json.load(json_data)     
			json_data.close() 
			mySubType = data["submission_type"]
			myTests = len(data["tests"])
			myMetrics = len(data["metrics"])
			locExists = 0
			l = len(data["metrics"]) - 1
			while l > 0: 
				if data["metrics"][l]["type"] == "location":
					locExists = 1
				l = l - 1
			theStr = "'" + prov + "','" + file + "','" + mySubType + "'," 
			theStr = theStr + str(myTests) + "," + str(myMetrics) + "," + str(locExists)
			mySQL = "INSERT INTO " + schema + ".log VALUES (" 
			mySQL = mySQL + theStr + "); Commit;"
			cur.execute(mySQL)
					
now = time.localtime(time.time())
print "    end   time:", time.asctime(now)
