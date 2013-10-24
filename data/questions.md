ASSUMPTIONS
===========
- all this come from https://github.com/FCC/mobile-mba-androidapp/wiki/Data-Representation
	lots of these questions are just things that are not explicit in the documentation 
	above, and in order to write this vis app, we (and anyone else wanting to use the 
	data, needs to know the answers to this)
- I am operating on the source json files, importing them into a DB
- the general goal we have is  creating a vis data structure.  this structure is 
	intended for our vis purposes only.  it might have other purposes, but that is not 
	my goal.  to do this, we will transform from the json files (right now, will need 
	a decision point at some point) to some other set of data structure.
- I am using the word 'dictionary' below as an array w/i the json files


Top Level
---------
- do we include wifi tests, or exclude them?  Knowing that [GSM|CDMA] location may 
		be unavailable on a WIFI test.
- which dictionary's are active, and which ones are passive?  
- there are language differences between what we talk and what is in the written data
		documentation (eg bearer channel)
- which attributes at the top level are a function of which dictionaries?  in other words,
	does timestamp at the top level relate to tests?  to metrics?  is the 
	json heirarchical?
- do we want to track the app version in the visualizations?  if so, do we use 
		app_version_code or app_version_name?
	
	
Dictionaries
------------	
tests
	get, post, latency
metrics
	phone_identity, network_data, gsm_cell_location, cdma_cell_location, 
		cell_neighbour_tower_data, location
Conditions
	param_expired, netactivity, cpuactivity

Tests 
-----
1) why is there two different kinds of tags for tests?  ( eg. JHTTPGETMT vs JHTTPGET)? 
		I need to TEST THIS, but think it is possible.  could be a function of 
 	 	application version.
 	 	
2) what does the 'success' at the test type level (e.g. get) in tests dictionary mean?

3) i am ignoring latency as metric.  i am also ignoring packet loss is that ok?

4) what should we do about files w/ multiple tests?  how can i trap these for sure? 

		i need t TEST THIS - eg look at the build number
	- 20130210184839_166.147.72.176_5117eb8719bb1.json
	- sprint is only 1 set of test dictionaries per file
	- tmbole has cases where there are 2 sets of tests (not sure how many) per file
	- 20130211204833_208.54.32.161_51195921ec765.json
	- vz has cases where there are 2 sets of tests (not sure how many)  per file
	- 20130210184837_70.196.34.40_5117eb854b698.json
	- is there cases where there is a get test, and not a put test?  put test and  not get test?
	
Metrics	
-------
5) metrics seems to have nested structure.  i am assuming;
	- phone_identity is always position 0 in the metrics dictionary
	- network_data is always position 1 in the metrics dictionary
	- what is with the metrics after position 1 (e.g. 2 through n?)
		- cdma or gsm should be in position 2, but is sometimes network_data.  why?

6) why is network_data repeated after position 1 in the dictionary?

7) 'active_network_type' is sometimes null.  why is that?  is it a function of some 
	other attribute?

8) i am using the last lat/long in the list.  is that ok?  would you 
	prefer something else?  this can be changed relatively easily.

9)  when is there a dictionary called cdma_cell_location or gsm_cell_location?  
		why would it be absent?  would it be absent if it is a wifi connection?

10) since cdma and gsm have different attributes, where is what we are proposing;
	- from gsm use signal_strength and cell_tower_id
	- from cdma use dbm and concatenate longitude and latitude for cell_tower_id
	is this ok?

11) what conditions exist to map when metrics (phone_identity, network_data, 
		gsm_cell_location, cdma_cell_location, cell_neighbour_tower_data, and
		location) exists or doesn't in the file?  what i am after here are attributes 
		in the json file which show a dependency or pattern of metrics typing.

12) The location's are associated with the active metric events.  As a mobile recordes 
		the new locatiouns they would be recorded.  Only one locations means it's 
		stationary.. a bunch would mean it's moving.   LETS TALK THIS ONE THROUGH.

13) what are negative signal strengths?
 
Conditions
----------
14) i am not doing anything w/ the 'Conditions' dictionary.  should we be?

