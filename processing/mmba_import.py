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
import unicodedata
import fnmatch

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
outTB = "tests_2014_01"
myDir = "/Users/feomike/downloads/mmba_downloads/json/"   
	
#function for getting top level data
#accept 2 variables; the json data and the current string
#return the string w/ more attributes on it; the top level attributes
def topLevel(myData, theStr):
	#get top level data
	myVer = myData["app_version_name"] #track the version people are using
	mySubType = myData["submission_type"] #only use 'scheduled_test' or manual_test
	myTime = str(myData["timestamp"])  #is integer; no longer using this value	
	myDate = myData["datetime"]  #no longer using this value
	myDate = myDate[:19] + ' 2014' #myDate[len(myDate)-4:]
	myTimeZone = str(myData["timezone"])  #is integer
	mySim = str(myData["sim_operator_code"])
	myID = str(myData["enterprise_id"])
	#append the new values to the end of the existing string, with quotes for text data
	theStr = theStr + ",'" + myVer + "', '" + mySubType + "', " + myTime + ", '"
	theStr = theStr + myDate + "', " + myTimeZone + ",'" + mySim + "', '" + myID + "', "  
	return(theStr)
	
#function for getting tests data
#accept 2 variables; the json data and the current string
#return the string w/ more attributes on it; the test attributes
def myTests(myData, theStr):
	#get the test data
	#the loop is set up this way b/c i want to be sure i get the get and post test
	#and i am not sure if either test is first or second in the "tests" dictionary
	myDS = '-9'
	myDSSuc = '0'
	myDSDT = 'Wed May 14 18:48:52 1952'  #initialize a bogus date in case null
	myDSTS = '-556502400'  #initialize a bogus date incase null
	myUS = '-9'
	myUSSuc = '0'	
	myUSDT = 'Wed May 14 18:48:52 1952'  #initialize a bogus date in case null
	myUSTS = '-556502400'  #initialize a bogus date incase null
	myRTT = '-9'
	myLost = '-9'
	myLatSuc = '0'	
	if 'tests' in myData:
#		print myData["tests"]
		if len(myData["tests"]) > 0:
			t = 0
			while t < len(myData["tests"]):
				if myData["tests"][t]["type"] == "JHTTPGETMT" or \
				          myData["tests"][t]["type"] == "JHTTPGET": 
					myDS = str(myData["tests"][t]["bytes_sec"])
					#you might want a branch b/c of the value returned from 'success'
					myDSSuc = str(myData["tests"][t]["success"])
					myDSDT = myData["tests"][t]["datetime"]
					#changed the variable myDSDT to be the first 20 characters
					#concatenated with the last 4 characters (e.g. year); this solves
					#a time error i was getting when inserting non-standard time zones
					myDSDT = myDSDT[:19] + ' 2014' #myDSDT[len(myDSDT)-4:]				
					myDSTS =  str(myData["tests"][t]["timestamp"])
				if myData["tests"][t]["type"] == "JHTTPPOSTMT" or \
				          myData["tests"][t]["type"] == "JHTTPPOST": 
					myUS = str(myData["tests"][t]["bytes_sec"])
					myUSSuc = str(myData["tests"][t]["success"])
					myUSDT = myData["tests"][t]["datetime"]
					myUSDT = myUSDT[:19] + ' 2014' #myUSDT[len(myUSDT)-4:]
					myUSTS =  str(myData["tests"][t]["timestamp"])
				if  myData["tests"][t]["type"] == "JUDPLATENCY":
					myRTT =  myData["tests"][t]["rtt_avg"]
					myLost = myData["tests"][t]["lost_packets"]	
					myLTDT = myData["tests"][t]["datetime"]	
					myLatSuc = myData["tests"][t]["success"]		
				t = t + 1			
	#append the new values to the end of the existing string
	theStr = theStr + myDS + ",'" + myDSSuc + "','" + myDSDT + "'," + myDSTS + ","
	theStr = theStr + myUS + ",'" + myUSSuc + "','" + myUSDT + "'," + myUSTS + ","
	theStr = theStr + str(myRTT) + "," + str(myLost) + ",'" 
	theStr = theStr + str(myLatSuc) + "'"
	return(theStr)

#function for getting metrics
#accept 2 variables; the json data and the current string
#return the string w/ more attributes on it; the metrics attributes
def myMetrics(myData, theStr):
	#instantiate the signal strength and cellID variables; do this because 
	#they don't exist in all tests 
	myMan = 'None'
	myModel = 'None'
	myOSType = 'None'
	myOSV = -9
	myNetType = 'None'
	myNetOpName = 'None'
	myNetOpCode = 'None'
	myPhoneType = 'None'
	myRoam = '0'
	myActNetType = 'None'
	mySigStren = '-99999'
	myCellID = '-99999'
	sourceCellLL = 'None'
	cellidLon = "0"
	cellidLat = "0"
	#cycle through each node in the metrics dictionary, to determine the 'type'
	#then grab the appropriate values from the dictionaries
	#the ISSUE this comes up w/ is that for any dictionary whose TYPE is repeated, 
	#this approach takes the values of the last dictionary
	m = 0
	while m < len(myData["metrics"]):
		if myData["metrics"][m]["type"] == "phone_identity":
			myMan = myData["metrics"][m]["manufacturer"]
			myModel = myData["metrics"][m]["model"]
			myOSType = myData["metrics"][m]["os_type"]
			myOSV = myData["metrics"][m]["os_version"]
		if myData["metrics"][m]["type"] == "network_data":
			myNetType = myData["metrics"][m]["network_type"] 
			myConnected = myData["metrics"][m]["connected"]  
			#some names are non-ascii, do a conversion to take care of this
			myNetOpName = myData["metrics"][m]["network_operator_name"].encode('ascii','ignore')
			myNetOpCode = myData["metrics"][m]["network_operator_code"]
			myNetOpName = string.replace(myNetOpName, "'", "")
			myPhoneType = myData["metrics"][m]["phone_type"]
			myRoam = str(myData["metrics"][m]["roaming"])
			if myRoam <> 'True' and myRoam <> 'False':
				myRoam = '0'
			#sometimes there is no active_network_type in the network_data
			#dictionary, this code below takes care of that by checking to see 
			#if the active_network_type exists in that list first, if it does, use it; if 
			#not, then set ActNetType = "None"
			if "active_network_type" in myData["metrics"][m]:
				myActNetType = myData["metrics"][m]["active_network_type"]
			else:
				myActNetType = "None"
		if myData["metrics"][m]["type"] == "gsm_cell_location":
			if 'signal_strength' in myData["metrics"][m]:
				mySigStren = str(myData["metrics"][m]["signal_strength"])
			else:
				mySigStren = '-99999'
			myCellID = str(myData["metrics"][m]["cell_tower_id"]).encode('ascii','ignore')
			cellidLon = "0"
			cellidLat = "0"
		if myData["metrics"][m]["type"] == "cdma_cell_location":
			if "dbm" in myData["metrics"][m]:
				mySigStren = str(myData["metrics"][m]["dbm"])
			else:
				mySigStren = "-99999"
			myCellID = str(myData["metrics"][m]["base_station_id"]).encode('ascii','ignore')
			myBaseLong = str(myData["metrics"][m]["base_station_longitude"]).encode('ascii','ignore')
			myBaseLat = str(myData["metrics"][m]["base_station_latitude"]).encode('ascii','ignore')
			sourceCellLL = myBaseLong + "; " + myBaseLat
			cellidLon = str(float(myBaseLong) / 14400) #returnDD(myBaseLong)
			cellidLat = str(float(myBaseLat) / 14400) #returnDD(myBaseLat)		
		m = m + 1
	#append the new values to the end of the existing string, 
	#with quotes for text data
	theStr = theStr + ",'" + myMan + "','" + myModel + "','" + myOSType + "','"
	theStr = theStr + str(myOSV) + "','" + myNetType + "','" + myNetOpName + "','"
	theStr = theStr + myNetOpCode + "','" + myPhoneType + "','" + myRoam + "', '" 	
	theStr = theStr + myActNetType + "'" + "," + mySigStren + ",'" + myCellID + "','"
	theStr = theStr + sourceCellLL + "', " + cellidLon + "," + cellidLat
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
	myLon = '0'
	myLat = '0'
	myAcc = '-9'
	l = len(myData["metrics"]) - 1
	while l > 0:
		if myData["metrics"][l]["type"] == "location":
			#need to convert these values to ascii characters, b/c you use the 'float'
			#function and sometimes these are 'unicode' types.
			myLon = str(myData["metrics"][l]["longitude"]).encode('ascii','ignore')
			myLat = str(myData["metrics"][l]["latitude"]).encode('ascii','ignore')
			#if the longitude is > than 180, or the latitude is > 90 make them 0
			myAcc = str(myData["metrics"][l]["accuracy"]).encode('ascii','ignore')
			if type(myAcc) is not int:
				myAcc = '-9'
			if abs(float(myLon)) > 180 or abs(float(myLat)) > 90:
				myLon = '0'
				myLat = '0'
		l = l - 1
	theStr = theStr + "," + myLon + "," + myLat + "," + myAcc
	theHexs = ["hex_75k","hex_50k","hex_25k","hex_10k","hex_5k"]
	for theHex in theHexs:
		myGID = myHexGID(myLon, myLat, theHex)
		theStr = theStr + "," + myGID
	return(theStr)

#return the Decimal Degree of the Tower pushed into the value
def returnDD (dms):
	dms = int(dms)
	#if there are 6 characters in the dms, then it is a two degree value
	if len(str(abs(dms))) == 6:
		myD = int(str(abs(dms))[:2])
		myM = int(str(abs(dms))[2:4])
		myS = int(str(abs(dms))[4:])
	if len(str(abs(dms))) == 7:
		myD = int(str(abs(dms))[:3])
		myM = int(str(abs(dms))[3:5])
		myS = int(str(abs(dms))[5:])
	myDD = "-118"
	if str(dms)[:1] == '-':
		myWest = '-'
	else:
		myWest = ''
	if len(str(abs(dms))) == 6 or len(str(abs(dms))) == 7:
		myDD = myWest + str(myD + (float(myM) / 60) + (float(myS) / 3600))
	else:
		myDD = str(dms)
	return(myDD)

#find the gid of the hexagon (or any regular grid) which contains this point
#accept 2 variables; the longitude and latitude
#return the gid of the polygon containing that point
def myHexGID (myLon, myLat, myHex):
	mySQL = "SELECT hexid from " + schema + "." + myHex + " where ST_CONTAINS(geom, "
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
	mySQL = "INSERT INTO " + schema + "." + outTB + " VALUES (" 
	mySQL = mySQL + myStr + "); Commit;"
#	print mySQL
	cur.execute(mySQL)
	return()	

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
 	    
#directory, and process each json file one at a time
for dirpath, dirs, files in os.walk(myDir):
	for file in fnmatch.filter(files, '*.json'):
		try:
			#clear and initialize the updArray with the provider name
			#updArray = []
			#updArray.append(prov)
			#clear and initialize the time array
			# the value returned from json.load is a Python dictionary.
#			print dirpath + "/" + file
			json_data = open(dirpath + "/" + file)
			data = json.load(json_data)     
			json_data.close() 
			#for this purpose we are only using scheduled or manual tests, and those with
			#3 entries in the tests dictionary;   									
			if (data["submission_type"] == "scheduled_tests" \
					or data["submission_type"] == "manual_test"): 
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
#				os.system('rm ' + dirpath + "/" + file)
#			else:
#				#is an initial test
#				os.system('rm ' + dirpath + "/" + file)
		except ValueError:
			#is a malformed json file
			print '      file: ' + dirpath + '/' + file + ' is not valid'
conn.commit()
cur.close
now = time.localtime(time.time())
print "    end   time:", time.asctime(now)
