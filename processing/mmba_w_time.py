#mike Byrne 
#federal communications commission
#October, 2013
#post shutdown
#import the .json file into production tables for display and analysis

#this script imports source json files for the measuring mobile broadband america (mmba)
#into a database for geospatial analysis.  the full data dictionary of the MMBA program
#can be found here https://github.com/FCC/mobile-mba-androidapp/wiki/Data-Representation
#this script does not import all fields, but only those fields which are useful for the
#map and data visualization aspects of the MMBA program.  in essence, this script creates
#a parallel data asset based off of the source json files delivered from SamKnows
#this script only works on files which meet the following conditions;
#	- files which are scheduled or manual tests
#	- files which have 3 and only three tests (get, post and latency)
#	- files with a location; assumes the information is contained in the last metrics node
#	- files which have metrics (e.g. len(x["metrics"]) > 0

#the script can be changed such that it imports all files in subdirectories of a directory
#or based on the provided (e.g. only do files in the att dir/subdir).  right now it works
#on all files in one directory (not in say subdirectories).  the script assumes a 
#directory structure such that a set of providers (e.g. att, sprint, tmobile, vz) has
#a set of subdirectories under it called <provider>/json/<year><month>/ where <year> 
#is a the year eg 2013 and <month> is a 2 digit month eg <02>.  then all json files for 
#that provider, year and month to be imported are stored in that directory.

#the way this script works, is that it reads through each source json file, and extracts
#only the data that the visualization output needs.  the script concatenates the 
#extracted information into a long comma separated string, then inserts that string
#into a table.  it then also finds out which hexagon the test is within, and updates
#a set of tables to acquire the current sum, count and average of each test (get, put
#rtt and lost packets).  averages are created for every type desired (e.g. all, individual
#provider, provider and network_type and active_network_type etc).  these updates are 
#configurable, and require that the table of known values be generated a head of time.
#see 
#https://github.com/feomike/mmba_viz_processing/blob/master/processing/mk_mmba_tables.py
#to generate appropriate tables on the back end

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
#	- the script assumes there are tables both to insert to and to update.  these tables
#		can be created w/ the mk_mmba_tables.py script, which represent the sum, count,
#		and average of attribute types for tests (get, put, rtt, and lost packet).
#		attribute types include, 
#				all;
#				provider - att, sprint, tmobile, vz;
#				network_type - eg LTE, eHRPD, EVDO rev a, HPSH+
#				active_network_type - mobile, WIFI
#				multiple cross types are yet to be added (e.g. vz_LTE_mobile)
 
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

import os
import json
import pprint
import string
import psycopg2
import time
import datetime
from datetime import date

#set up how the script should run; change this variables to load only specific data
#from a certain month 
#month variables; needs leading 0 if the directory structure has a leading 0
month = "10"
print "    working on month: " + month + "..."

#set up a global array to hold values for the update of the 'type' tables
#this array is reset every loop of a json file, such that it can hold the appropriate
#values for updating;  we need to do this as a global array, b/c different fucntions
#return different values and i need one consistent place to hold the values to update

now = time.localtime(time.time())
print "    start time:", time.asctime(now)

#global variables - database connection
myHost = "localhost"
myPort = "54321"
myUser = "postgres"
db = "feomike"
schema = "mmba"
myHex = "hex_75000"
	
#function for getting top level data
#accept 2 variables; the json data and the current string
#return the string w/ more attributes on it; the top level attributes
def topLevel(myData, theStr):
	#get top level data
	myVer = myData["app_version_name"] #track the version people are using
	mySubType = myData["submission_type"] #only use 'scheduled_test' or manual_test
	myTime = str(myData["timestamp"])  #is integer; no longer using this value
	myDate = myData["datetime"]  #no longer using this value
	myTimeZone = str(myData["timezone"])  #is integer
	#print str(myData["app_version_name"])
	#append the new values to the end of the existing string, with quotes for text data
	theStr = theStr + ",'" + myVer + "', '" + mySubType + "', " + myTimeZone + ", "
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
				myTime =  myData["tests"][t]["timestamp"]  	
				myDSDT = myData["tests"][t]["datetime"]
			if myData["tests"][t]["type"] == "JHTTPPOSTMT" or \
			          myData["tests"][t]["type"] == "JHTTPPOST": 
				myUS = myData["tests"][t]["bytes_sec"] 
				myUDt = myData["tests"][t]["datetime"]  
				#you might want a branch b/c of the value returned from 'success'
				myUSSuccess = myData["tests"][t]["success"] 
				myUSDT = myData["tests"][t]["datetime"]
			if  myData["tests"][t]["type"] == "JUDPLATENCY":
				myRTT =  myData["tests"][t]["rtt_avg"]
				myLost = myData["tests"][t]["lost_packets"]	
				myLTDT = myData["tests"][t]["datetime"]			
			t = t + 1
		#append to the updArray the results of the tests
		updArray.append(myDS)
		updArray.append(myUS)
		updArray.append(myRTT)
		updArray.append(myLost)
		updTime.append(myDSDT)
		#append the new values to the end of the existing string	
		theStr = theStr + "'" + myDSDT + "', " + str(myTime) + ", " 
		theStr = theStr + str(myDS) + "," + str(myUS) + "," 
		theStr = theStr + str(myRTT) + "," + str(myLost)
	return(theStr)

#function for getting metrics
#accept 2 variables; the json data and the current string
#return the string w/ more attributes on it; the metrics attributes
def myMetrics(myData, theStr):
	#instantiate the signal strength and cellID variables; do this because 
	#they don't exist in all tests 
	mySigStren = "-99999"
	myCellID = "-99999"
	#cycle through each node in the metrics dictionary, to determine the 'type'
	#then grab the appropriate values from the dictionaries
	#the ISSUE this comes up w/ is that for any dictionary whose TYPE is repeated, 
	#this approach takes the values of the last dictionary
	m = 0
	while m < len(myData["metrics"]):
		#print "m is: " + str(m)
		if myData["metrics"][m]["type"] == "phone_identity":
			#phone_identity is usually position 0 in the metrics dictionary
			myMan = myData["metrics"][m]["manufacturer"]
			myModel = myData["metrics"][m]["model"]
			myOSType = myData["metrics"][m]["os_type"]
			myOSV = myData["metrics"][m]["os_version"]
		if myData["metrics"][m]["type"] == "network_data":
			#print myData["metrics"][m]
			#network_data is usually position 1 in the metrics dictionary
			myNetType = myData["metrics"][m]["network_type"] #is there
			#print "myNetType is: " + myNetType
			myConnected = myData["metrics"][m]["connected"]  #is there and might need to use it
			myNetOpName = myData["metrics"][m]["network_operator_name"]
			myPhoneType = myData["metrics"][m]["phone_type"]
			#sometimes there is no active_network_type in the network_data
			#dictionary, this code below takes care of that by checking to see 
			#if the active_network_type exists in that list first, if it does, use it; if 
			#not, then set ActNetType = "None"
			if "active_network_type" in myData["metrics"][m]:
				#print myData["metrics"][m]["active_network_type"]
				myActNetType = myData["metrics"][m]["active_network_type"]
			else:
				myActNetType = "None"
		if myData["metrics"][m]["type"] == "gsm_cell_location":
			mySigStren = str(myData["metrics"][m]["signal_strength"])
			myCellID = str(myData["metrics"][m]["cell_tower_id"])
		if myData["metrics"][m]["type"] == "cdma_cell_location":
			if "dbm" in myData["metrics"][m]:
				mySigStren = str(myData["metrics"][m]["dbm"])
			else:
				mySigStren = "-99999"
			myCellID = str(myData["metrics"][m]["base_station_id"])
			myBaseLat = str(myData["metrics"][m]["base_station_latitude"])
			myBaseLong = str(myData["metrics"][m]["base_station_longitude"])			
			myCellID = myCellID #+ "|" + myBaseLong + "|" + myBaseLat				
		m = m + 1
	
	#append to the updArray the results of the metrics
	updArray.append(myNetType)
	updArray.append(myActNetType)
	#append the new values to the end of the existing string, 
	#with quotes for text data
	theStr = theStr + ",'" + myMan + "','" + myModel + "','" + myOSType + "',"
	#print theStr
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
	mySQL = mySQL + "ST_TRANSFORM(ST_SetSRID(ST_MakePoint(" + myLon + ", " + myLat 
	mySQL = mySQL + "), 4326), 900913));"
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
	#at this point, we are using the updArray to update each table
	#the updArray has this structure;
	#0=Provider, 1=ds, 2=us, 3=rtt, 4=lp, 5=network_type, 6=active_network_type and
	#7=gid
	tables = ["all", "provider", "network_type", "active_network_type", 
		"provider_network_type", "provider_active_network_type"]
	tables = ["all"]
	#get the value out of the current tables
	#tables to get; all, provider, network_type, active_network_type, 
	#provider_network_type, provider_active_network_type
	#for each table, get the current value at a hex cell,
	#and update it w/ the values in the updArray.  
	returnMyTime()
	t = 1
	for tab in tables:
		while t < 6:  #t<6 is the position in the updTime array; there are 7 values
			mySQL = "UPDATE " + schema + "." + tab + " set ds_sum = ds_sum + " 
			mySQL = mySQL + str(updArray[1]) + ", ds_count = ds_count + 1, "
			mySQL = mySQL + "ds_average = (ds_sum + " + str(updArray[1]) + ") / (ds_count "
			mySQL = mySQL + "+ 1), us_sum = us_sum + " + str(updArray[2]) + ", us_count = "
			mySQL = mySQL + "us_count + 1, us_average = (us_sum + " + str(updArray[2]) 
			mySQL = mySQL + ") / (us_count + 1), "
			mySQL = mySQL + "rtt_sum = rtt_sum + " + str(updArray[3]) + ", rtt_count = "
			mySQL = mySQL + "rtt_count + 1,  rtt_average = (rtt_sum + " + str(updArray[3]) 
			mySQL = mySQL + ") / (rtt_count + 1), " + "lp_sum = lp_sum + " + str(updArray[4])
			mySQL = mySQL + ", lp_count = lp_count + 1, lp_average = (lp_sum + "
			mySQL = mySQL + str(updArray[4]) + ") / (lp_count + 1) "
			mySQL = mySQL + " where gid = " + str(updArray[7])

			if tab == "provider":
				mySQL = mySQL + " and mytype = '"  + updArray[0] + "' "
			if tab == "network_type":
				mySQL = mySQL + " and mytype = '" + updArray[5] + "' "
			if tab == "active_network_type":
				mySQL = mySQL + " and mytype = '" + updArray[6] + "' "
			if tab == "provider_network_type":
				mySQL = mySQL + " and mytype = '" + updArray[0] + "/" + updArray[5] + "' "
			if tab == "provider_active_network_type":
				mySQL = mySQL + " and mytype = '" + updArray[0] + "/" + updArray[6] + "' "
			#append on the time element
			mySQL = mySQL + " and mytime = '" + updTime[t] + "'"
			mySQL = mySQL + "; COMMIT; "
			cur.execute(mySQL)
			t = t + 1
	return()

#the function that extracts and formats the time element for each row
#accepts one variable of the timestamp as a string
#returns an array of the stripped out and formated time elements to update
#array positions are -  1: all; 2: year; 3: quarter; 4: month; 5: week
#for the date parsing, you need output which is the year, quarter, month and week of
#year as an integers.  year is the only value in the datestamp in source json files which
#are available for use as extracted from the string.  so we have to transform the 
#timestamp data from the json file to a python date type.
#then use the date library from the datetime library to acquire the quarter, the 
#the two digit month, and the week of the year
def returnMyTime():
	dt = updTime[0]
	#dt[4:7] beginning at place 4 through place 7 in the string is the Month
	#dt[8:10] beginning at place 8 through place 10 is the day of the month
	#dt[-4:] the last 4 digits is the year
	myYear = int(dt[-4:])
	myDay = int(dt[8:10])

	if dt[4:7] == "Jan":
		myMonth = 1
	if dt[4:7] == "Feb":
		myMonth = 2
	if dt[4:7] == "Mar":
		myMonth = 3
	if dt[4:7] == "Apr":
		myMonth = 4
	if dt[4:7] == "May":
		myMonth = 5
	if dt[4:7] == "Jun":
		myMonth = 6
	if dt[4:7] == "Jul":
		myMonth = 7
	if dt[4:7] == "Aug":
		myMonth = 8
	if dt[4:7] == "Sep":
		myMonth = 9
	if dt[4:7] == "Oct":
		myMonth = 10
	if dt[4:7] == "Nov":
		myMonth = 11
	if dt[4:7] == "Dec":
		myMonth = 12

	#format a date object by inserting (year, month, day of month) in the date function
	dt = datetime.date(myYear, myMonth, myDay)
	#use python to acquire needed date values
	myQuarter = (myMonth-1)//3+1
	myWeek = int(dt.strftime("%W"))

	updTime.append("all")
	updTime.append("year:" + str(myYear))
	updTime.append(str(myYear) + ":quarter:" + str(myQuarter))
	updTime.append(str(myYear) + ":month:" + str(myMonth))
	updTime.append(str(myYear) + ":week:" + str(myWeek))
	return()

#at some point we need to figure out how to slice time.  one approach is to add a 
#mytime field to each table, and aggregate the timestamp to an appropriate level
#such that time could be filtered along with any other variable (e.g. sprint, wifi, lte
#and day of week) or something like that.  below is just some notes on performing these
#time insertions/updates	
#insert week, insert month, insert year, insert total

#table structure could be:
#ds_sum, ds_count, ds_avg, us_sum, us_count, us_avg, 
#rtt_sum, rtt_count, rtt_avg, lp_sum, lp_count, lp_avg
#mytype, mytime
#perhaps appropriate myTime intervals would be:
#total, year, month or week

#this function is not being used, but left in as a code example for future extraction
#of data in the conditions node/dictionary
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

#create the connection string to postgre
myConn = "dbname=" + db + " host=" + myHost + " port=" + myPort + " user=" + myUser
conn = psycopg2.connect(myConn)
cur = conn.cursor()

#global variables - directory / provider 
provList = ["att","sprint","tmobile","vz"]
#for each provider (read directory) in the list, find all json files in the /json/<month>
#directory, and process each json file one at a time
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
			#clear and initialize the time array
			updTime = []
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
			if (data["submission_type"] == "scheduled_tests" \
					or data["submission_type"] == "manual_test") \
					and len(data["tests"]) == 3 \
			        and len(data["metrics"]) > 0 \
			        and data["metrics"][l]["type"] == "location":
			    #each function returns a string containing the values extracted from the
			    #individual json files, and concatenates it for insertion into the tests
			    #table.
				#get the toplevel metrics
				myStr = "'" + file + "'"
				myStr = topLevel(data, myStr)
				#get the tests
				myStr = myTests(data, myStr)
				#get the metrics
				myStr = myMetrics(data, myStr)
				myStr = myLocation(data, myStr)
				#insert the values as a new string in the tests table
				insertRaw(myStr)
				#update all other applicable tables based on the data in the individual
				#json file
				updateTable()
conn.commit()
cur.close
now = time.localtime(time.time())
print "    end   time:", time.asctime(now)
