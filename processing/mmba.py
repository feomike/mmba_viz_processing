#mike Byrne
#federal communications commission
#may 9, 2013
#import the .json file into a csv

#this script imports source json files for the measuring mobile broadband america (mmba)
#into a database for geospatial analysis.  the full data dictionary of the MMBA program
#can be found here https://github.com/FCC/mobile-mba-androidapp/wiki/Data-Representation
#this script does not import all fields, but only those fields which are useful for the
#map and data visualization aspects of the MMBA program.  in essence, this script creates
#a parallel data asset based off of the source json files delivered from SamKnows
#this script only works on files which meet the following conditions;
#	- files which are scheduled tests
#	- files which have 3 and only three tests (get, post and latency)
#	- files with a location
#	- files which have metrics (e.g. len(x["metrics"]) > 0

#the script can be changed such that it imports all files in subdirectories of a directory
#or based on the provided (e.g. only do files in the att directory).  right now it works
#on all files in one directory (not in say subdirectories)

#the way this script works, is that it reads through each source json file, and extracts
#only the data that the visualization output needs.  the script concatenates the 
#extracted information into a long comma separated string, then inserts those values
#into a table.  
#there are four sections of json file.  the script has a function call
#for each section of the json file.  every time each function is run, it passes the 
#current string of attributes to the function, AND returns a resulting string which is 
#the current string plus the new values from the section run appended to the end.  the
#resulting string after all four functions are run, contain all values to be used in 
#the data visualization and inserted into the table.
#the four sections are;
#	- topLevel - containing the top attributes like submission type and date
#	- Tests - containing the get, post and latency test
#	- metrics - containing network_type, phone_type etc
#	- location (which is actually part of metrics, but i have put in its one function
#		for ease of processing and debugging), containing latitude and longitude
#


#ASSUMPTIONS:
#	- this script works on the assumption that source MMBA files follow the above url 
#		data dictionary
#	- this script assumes to work on all folders/files in a directory, but best practice
#		for source file curation is to manage files by provider and month 
#		(e.g. download all files for ATT for September 2013 into the att/201309 folder).
#		this makes file curation easier

#DEPENDENCIES:
#	- MMBA data is from source (eg raw) MMBA json files, and exists in a directory
#		that is set in a variable in this script.  the user needs to change that path
#		appropriately
#	- the psycopg2 library needs to be loaded for making a connection to Postgres
#	- this script uses Postgres, for the insertion, the database, schema and tables
#		need to exist prior to running
 
#ISSUES:
#	- this script inserts all records into a database.  we need to work out how these 
#		inserts are managed.  what if someone runs the same parameters (e.g. provider / 
#		month) again, thereby duplicating records?; likewise further requirements / 
#		description of he table structure needs to be worked out
#	- there is an issue w/ the signal strength data; att and tmobile are gsm only, and 
#		sprint and vz are cdma only.  cdma and gsm have different returns for signal 
#		strength
#	- right now, dates are treated as string values, rather than date fields
#	- i am not using any values from the 'Conditions' dictionary. 
#	- better documentation on the idea of the update tables

#SOLVED ISSUES:
#	- any values that are strings in the JSON file that need to be integers are 
#		automatically converted
#	- it is unclear if get, post and latency are always the same ordinal location in the
#		tests dictionary in the json file.  my does not require that they are, but it 
#		might be an issue

import os
import json
import pprint
import string
import psycopg2
import time
now = time.localtime(time.time())
print "local time:", time.asctime(now)

#set up how the script should run; change this variables to load only specific data
#from a certain month 
#month variables
month = "09"
#set up a global array to hold values for the update of the 'type' tables
#this array is reset every loop of a json file, such that it can hold the appropriate
#values for updating;  we need to do this as a global array, b/c different fucntions
#return different values and i need one consistent place to hold the values to update


#global variables - database connection
myHost = "localhost"
myPort = "54321"
myUser = "postgres"
db = "feomike"
schema = "mmba"
myHex = "ptsinhex4"
	
#function for getting top level data
#accept 2 variables; the json data and the current string
#return the string w/ more attributes on it; the top level attributes
def topLevel(myData, theStr):
	#get top level data
	mySubType = myData["submission_type"] #only use 'scheduled_test'
	myTime = str(myData["timestamp"])  #is integer
	myDate = myData["datetime"]  #is there
	myTimeZone = str(myData["timezone"])  #is integer
	#print str(myData["app_version_name"])
	#append the new values to the end of the existing string, with quotes for text data
	theStr = theStr + "," + myTime + ",'" + myDate + "', " + myTimeZone
	return(theStr)
	
#function for getting tests data
#accept 2 variables; the json data and the current string
#return the string w/ more attributes on it; the test attributes
def myTests(myData, theStr):
	#get the test data
	#the loop is set up this way b/c i want to be sure i get the get and post test
	#and i am not sure if either test is first or second in the "tests" dictionary	
	if len(myData["tests"]) > 0:
		t = 0
		while t < len(myData["tests"]):
			if myData["tests"][t]["type"] == "JHTTPGETMT" or \
			          myData["tests"][t]["type"] == "JHTTPGET": 
				myDS = myData["tests"][t]["bytes_sec"] 
				mySDt = myData["tests"][t]["datetime"]  
				#you might want a branch b/c of the value returned from 'success'
				myDSSuccess = myData["tests"][t]["success"]  	
			if myData["tests"][t]["type"] == "JHTTPPOSTMT" or \
			          myData["tests"][t]["type"] == "JHTTPPOST": 
				myUS = myData["tests"][t]["bytes_sec"] 
				myUDt = myData["tests"][t]["datetime"]  
				#you might want a branch b/c of the value returned from 'success'
				myUSSuccess = myData["tests"][t]["success"]  								
			t = t + 1
		#append to the updArray the results of the tests
		updArray.append(myDS)
		updArray.append(myUS)
		#append the new values to the end of the existing string	
		theStr = theStr + "," + str(myDS) + "," + str(myUS)
	return(theStr)

#function for getting metrics
#accept 2 variables; the json data and the current string
#return the string w/ more attributes on it; the metrics attributes
def myMetrics(myData, theStr):
	#phone_identity is always position 0 in the metrics dictionary
	myMan = myData["metrics"][0]["manufacturer"]
	myModel = myData["metrics"][0]["model"]
	myOSType = myData["metrics"][0]["os_type"]
	myOSV = myData["metrics"][0]["os_version"]	
	#network_data is always position 1 in the metrics dictionary
	myNetType = myData["metrics"][1]["network_type"] #is there
	myConnected = myData["metrics"][1]["connected"]  #is there and might need to use it
	myNetOpName = myData["metrics"][1]["network_operator_name"]
	myPhoneType = myData["metrics"][1]["phone_type"]
	#sometimes there is no active_network_type in the network_data
	#dictionary, this code below takes care of that by checking to see 
	#if the active_network_type exists in that list first, if it does, use it; if 
	#not, then set ActNetType = "None"
	if "active_network_type" in myData["metrics"][1]:
		#print myData["metrics"][1]["active_network_type"]
		myActNetType = myData["metrics"][1]["active_network_type"]
	else:
		myActNetType = "None"
	#ISSUE
	#position #2 is NOT always either cdma or gsm cell location
	#need to work this through; cdma is the problem
	#sometimes it is not there and network_data is in position #2
	if myData["metrics"][2]["type"] <> "gsm_cell_location" or \
			myData["metrics"][2]["type"] <> "cdma_cell_location":
		mySigStren = "-99999"
		myCellID = "test"
	if myData["metrics"][2]["type"] == "gsm_cell_location":			
		mySigStren = str(myData["metrics"][2]["signal_strength"])
		myCellID = str(myData["metrics"][2]["cell_tower_id"])
	if myData["metrics"][2]["type"] == "cdma_cell_location":
		if "dbm" in myData["metrics"][2]:
			mySigStren = str(myData["metrics"][2]["dbm"])
		else:
			mySigStren = "-99999"
		myCellID = str(myData["metrics"][2]["base_station_id"])
		myBaseLat = str(myData["metrics"][2]["base_station_latitude"])
		myBaseLong = str(myData["metrics"][2]["base_station_longitude"])			
		myCellID = myCellID #+ "|" + myBaseLong + "|" + myBaseLat
	#append to the updArray the results of the metrics
	updArray.append(myNetType)
	updArray.append(myActNetType)
	#append the new values to the end of the existing string, 
	#with quotes for text data
	theStr = theStr + ",'" + myMan + "','" + myModel + "','" + myOSType + "',"
	theStr = theStr + str(myOSV) + ",'" + myNetType + "','" + myNetOpName + "','"
	theStr = theStr + myPhoneType + "','" + myActNetType + "'"	
	theStr = theStr + "," + mySigStren + ",'" + myCellID + "'"
	return(theStr)


#find the locations
#accept 2 variables; the json data and the current string
#return the string w/ more attributes on it; the location attributes
#right now, the LAST lat/long is returned
def myLocation(myData, theStr):
	#cycle through every value in the 'metrics' dictionary, and see if it is a location.
	#if it is, then get the latitude and longitude of the location
	#the easiest way is to get the first or the last location in the list
	#another way will be to average the list
	l = len(myData["metrics"]) - 1
	while l > 0:
		if myData["metrics"][l]["type"] == "location":
			myLon = str(myData["metrics"][l]["longitude"])
			myLat = str(myData["metrics"][l]["latitude"])
		l = l - 1
	myGID = myHexGID(myLon, myLat)
	#append to the updArray the results of the myLocation
	updArray.append(myGID)
	#append the new values to the end of the existing string, 
	theStr = theStr + "," + myLon + "," + myLat + "," + myGID
	return(theStr)

#find the gid of the hexagon (or any regular grid) which contains this point
#accept 2 variables; the longitude and latitude
#return the gid of the polygon containing that point
def myHexGID (myLon, myLat):
	mySQL = "SELECT gid from " + schema + "." + myHex + " where ST_CONTAINS(geom, "
	mySQL = mySQL + "ST_SetSRID(ST_MakePoint(" + myLon + ", " + myLat + "), 4326));"
	cur.execute(mySQL)
	r = cur.fetchone()
	if r <> None:
		myGID = str(r[0])
	else:
		myGID = "-9999"
	return(myGID)

#insert into raw table
def insertRaw(theStr):
	#set up python connection
	#write insert string
	#insert
	#set up the connection to the database
	mySQL = "INSERT INTO " + schema + ".tests VALUES (" 
	mySQL = mySQL + myStr + "); Commit;"
	cur.execute(mySQL)
	return()	

#update the current production tables
def updateTable():
	tables = ["all", "provider", "network_type", "active_network_type", 
		"provider_network_type", "provider_active_network_type"]
	#tables = ["all"]
	#get the value out of the current tables
	#tables to get; all, provider, network_type, active_network_type, 
	#provider_network_type, provider_active_network_type
	for tab in tables:
		mySQL = "UPDATE " + schema + "." + tab + " set ds_sum = ds_sum + " 
		mySQL = mySQL + str(updArray[1]) + ", ds_count = ds_count + 1, "
		mySQL = mySQL + "ds_average = (ds_sum + " + str(updArray[1]) + ") / (ds_count "
		mySQL = mySQL + "+ 1), us_sum = us_sum + " + str(updArray[2]) + ", us_count = "
		mySQL = mySQL + "us_count + 1, us_average = (us_sum + " + str(updArray[2]) 
		mySQL = mySQL + ") / (us_count + 1) where gid = " + str(updArray[5])
		if tab == "provider":
			mySQL = mySQL + " and mytype = '"  + updArray[0] + "' "
		if tab == "network_type":
			mySQL = mySQL + " and mytype = '" + updArray[3] + "' "
		if tab == "active_network_type":
			mySQL = mySQL + " and mytype = '" + updArray[4] + "' "
		if tab == "provider_network_type":
			mySQL = mySQL + " and mytype = '" + updArray[0] + "/" + updArray[3] + "' "
		if tab == "provider_active_network_type":
			mySQL = mySQL + " and mytype = '" + updArray[0] + "/" + updArray[4] + "' "
		mySQL = mySQL + "; COMMIT; "
		cur.execute(mySQL)
	return()
	
#insert week
#insert month
#insert year
#insert total

#table is
#time, ds sum, ds num, ds average, us sum, us num, us average, carrier, \
#      network_type, active_network
#total
#year
#month
#week

#function for getting conditions
def myConditions(myData):
	c = 0
	while m < len(myData["conditions"]):
		if myData["conditions"][c]["type"] == "PARAM_EXPIRED":
			myExpiredSuccess = str(myData["conditions"][m]["success"])
		if myData["conditions"][c]["type"] == "NETACTIVITY":
			myNetSuccess = str(myData["conditions"][m]["success"])
		if myData["conditions"][c]["type"] == "CPUACTIVITY":
			myCPUSuccess = str(myData["conditions"][m]["success"])
	return()


myConn = "dbname=" + db + " host=" + myHost + " port=" + myPort + " user=" + myUser
conn = psycopg2.connect(myConn)
cur = conn.cursor()

#global variables - directory / provider 
provList = ["att","sprint","tmobile","vz"]
print "     working on month: " + month + "..."
for prov in provList:
	#loop through all files w/i the myDir varibale
	myDir = "/Users/feomike/documents/analysis/2013/mmba/data/" + prov + \
    	    "/json/" + "2013" + month + "/"
	os.chdir(myDir)
	for file in os.listdir("."):
		if file.endswith(".json"):
			#clear and initialize the updArray with the provider name
			updArray = []
			updArray.append(prov)
			# the value returned from json.load is a Python dictionary.
			#print file		
			json_data = open(file)
			data = json.load(json_data)     
			json_data.close() 
			#for this purpose we are only using scheduled tests, and those which have 3
			#and only 3 entries in the tests dictionary; if it is a scheduled test, i have 
			#determined that there is either 0 or 3 tests, so the following logic works
			#select scheduled_tests and length of tests = 3 and there is a location
			#need this next line, b/c location is always in the last position in the dict.
			l = len(data["metrics"]) - 1 
			if data["submission_type"] == "scheduled_tests" and len(data["tests"]) == 3 \
			        and len(data["metrics"]) > 0 \
			        and data["metrics"][l]["type"] == "location":
				#get the toplevel metrics
				myStr = "'" + file + "'"
				myStr = topLevel(data, myStr)
				#get the tests
				myStr = myTests(data, myStr)
				#get the metrics
				myStr = myMetrics(data, myStr)
				myStr = myLocation(data, myStr)
				insertRaw(myStr)
				updateTable()
conn.commit()
cur.close
now = time.localtime(time.time())
print "local time:", time.asctime(now)
