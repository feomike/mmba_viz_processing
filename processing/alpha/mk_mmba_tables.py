#mk_mmba_tables.py
#mike byrne
#federal communications commission
#generate the mmba back end tables

import os
import psycopg2
import time
now = time.localtime(time.time())
print "local time:", time.asctime(now)

#global variables - database connection
myHost = "localhost"
myPort = "54321"
myUser = "postgres"
db = "feomike"
schema = "mmba_5k"
totalRecs = 639713 #2835

tables = ["all","provider"] #, "network_type", "active_network_type"] #, 
#		"provider_network_type", "provider_active_network_type"]

#make the table
def makeTable(myTab):
	mySQL = "DROP TABLE IF EXISTS " + schema + "." + myTab + ";"
	mySQL = mySQL + "CREATE TABLE " + schema + "." + myTab + "("
	mySQL = mySQL + "ds_sum numeric, ds_count numeric, ds_average numeric, "
	mySQL = mySQL + "us_sum numeric, us_count numeric, us_average numeric, "
	mySQL = mySQL + "rtt_sum numeric, rtt_count numeric, rtt_average numeric, "	
	mySQL = mySQL + "lp_sum numeric, lp_count numeric, lp_average numeric, "	
	mySQL = mySQL + "mytype character varying (200),  "
	mySQL = mySQL + "gid integer ) with ( OIDS=TRUE); "
	mySQL = mySQL + "ALTER TABLE " + schema + "." + myTab + " owner to postgres; "
	mySQL = mySQL + "CREATE INDEX " + schema + "_" + myTab + "_gid_btree ON "
	mySQL = mySQL + schema + "." + myTab + " USING btree (gid); "	
	mySQL = mySQL + "CREATE INDEX " + schema + "_" + myTab + "_mytype_btree ON "
	mySQL = mySQL + schema + "." + myTab + " USING btree (mytype); "
	mySQL = mySQL + "COMMIT;"
	cur.execute(mySQL)
	return()

#return the unique combinations to make of the types
def returnTypes(myTab):
	if myTab == "all":
		myTypes = ["all"]
	if myTab == "provider":
		myTypes = ["att", "sprint", "tmobile", "vz"]
	if myTab == "network_type":
		myTypes = ["LTE", "EVDO rev A", "eHRPD", "UMTS", "HSPA", "unknown", "HSPA+", 
					"HSDPA", "EDGE", "1xRTT", "EVDO rev 0", "GPRS"]
	if myTab == "active_network_type":
		myTypes = ["WIFI", "mobile", "WIMAX"]
	if myTab == "provider_network_type":
		myTypes = ["att/LTE", "att/EVDO rev A", "att/eHRPD", "att/UMTS", 
					"att/HSPA", "att/unknown", "att/HSPA+", "att/HSDPA", 
					"att/EDGE", "att/1xRTT", "att/EVDO rev 0", "att/GPRS",
					"sprint/LTE", "sprint/EVDO rev A", "sprint/eHRPD", "sprint/UMTS", 
					"sprint/HSPA", "sprint/unknown", "sprint/HSPA+", "sprint/HSDPA", 
					"sprint/EDGE", "sprint/1xRTT", "sprint/EVDO rev 0", "sprint/GPRS",
					"tmobile/LTE", "tmobile/EVDO rev A", "tmobile/eHRPD", "tmobile/UMTS", 
					"tmobile/HSPA", "tmobile/unknown", "tmobile/HSPA+", "tmobile/HSDPA", 
					"tmobile/EDGE", "tmobile/1xRTT", "tmobile/EVDO rev 0", "tmobile/GPRS",
					"vz/LTE", "vz/EVDO rev A", "vz/eHRPD", "vz/UMTS", 
					"vz/HSPA", "vz/unknown", "vz/HSPA+", "vz/HSDPA", 
					"vz/EDGE", "vz/1xRTT", "vz/EVDO rev 0", "vz/GPRS"]
	if myTab == "provider_active_network_type":
		myTypes = ["att/WIFI", "att/mobile", "att/WIMAX", 
					"sprint/WIFI", "sprint/mobile", "sprint/WIMAX",
					"tmobile/WIFI", "tmobile/mobile", "tmobile/WIMAX",
					"vz/WIFI", "vz/mobile", "vz/WIMAX"]
	return(myTypes)

#initialize the tables with the same number of gid's as the hext grid
#and all of the appropriate values we expect from the data
def insertRows(myTab):
	i = 0
	while i < totalRecs:
		i = i + 1
		types = returnTypes(myTab)
		for myType in types:
			mySQL = "INSERT INTO " + schema + "." + myTab + " VALUES ( "
			mySQL = mySQL + "0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,'"
			mySQL = mySQL + myType + "', "
			mySQL = mySQL + str(i) + "); "
			mySQL = mySQL + "COMMIT;" 
			cur.execute(mySQL)

#make the production tests table
def mkTests():
	mySQL = "DROP TABLE IF EXISTS " + schema + ".tests; CREATE TABLE " + schema + "." 
	mySQL = mySQL + "tests ( file_name character varying(75), "
	mySQL = mySQL + "app_version character varying(10), "
	mySQL = mySQL + "submission_type character varying(15), "
	mySQL = mySQL + "unix_timezone numeric, "  
	mySQL = mySQL + "test_date timestamp, unix_time numeric, " #character varying(35)
	mySQL = mySQL + "downspeed numeric, upspeed numeric, "
	mySQL = mySQL + "rtt numeric, lost_packets numeric, "	
	mySQL = mySQL + "manufacturer character varying(25), model character varying(50), "
	mySQL = mySQL + "os_type character varying(15), os_version numeric, "
	mySQL = mySQL + "network_type character varying(10), "
	mySQL = mySQL + "network_operator_name character varying(50), "
	mySQL = mySQL + "phone_type character varying(10), roaming boolean, "
	mySQL = mySQL + "active_network_type character varying(10), "
	mySQL = mySQL + "signal_strength numeric, cell_id character varying(100), "
	mySQL = mySQL + "longitude numeric, latitude numeric, accuracy numeric, gid numeric) "
	mySQL = mySQL + "WITH (OIDS=FALSE);  ALTER TABLE " + schema + ".tests OWNER TO  "
	mySQL = mySQL + "postgres; COMMIT; "
	cur.execute(mySQL)
	return()

myConn = "dbname=" + db + " host=" + myHost + " port=" + myPort + " user=" + myUser
conn = psycopg2.connect(myConn)
cur = conn.cursor()

#make the production tests table
mkTests()
	
#make the individual aggregation tables 
for tab in tables:
	makeTable(tab)
	insertRows(tab)
conn.commit()
cur.close
now = time.localtime(time.time())
print "local time:", time.asctime(now)
