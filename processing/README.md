Processing Steps
----------------
This file describes the general processing steps for processing the MMBA data. I CANNOT OVERSTRESS CLEAN INDIVIDUAL FILE CURATION ENOUGH.   I store individual JSON files in `<provider>/json/<year><month>` subdirectories to keep file curation easier.  lacking significant process around file curation will result in hard to trap errors down the line.

Step 1 - database back end set up
---------------------------------
the resulting data visualizations we are making are aggregate statistics of <type>, at a given location, where <type> are the set of attributes in the tests we wish to highlight in the visualizations.  So far, <type> includes:
	- test types - download speed, upload speed, latency (rtt), and packet loss
	- providers - att, sprint, tmobile, and verizon (vz)
	- network type - eg LTE, eHRPD, EVDO rev a, HPSA+
	- active_network_type - mobile, WIFI

Additionally, we need an aggregate spatial container to which we can quantify 'tests' by type.  For this purpose, the FCC is using a 75,000 meter centroid to centroid hexagon cell for spatial aggregation.  a test that falls within one hexagon is averaged with all other tests that fall within that hexagon.  smaller resolution hexagons (or other grid patterns) should be investigated for better time/space representation.  at this stage, however, for small scale visualizations, a 75k meter hexagon is very appropriate.

- Using the [hexagon](https://raw.github.com/feomike/mmba_viz_processing/master/data/hex_75000.geojson) data, change the variable in the [table creation script](https://github.com/feomike/mmba_viz_processing/blob/master/processing/mk_mmba_tables.py) for maximum unique id number (also known as GID in PostGIS) prior to running.  
- Modify the `tables` variable to decide which tables you want to create.
- Modify the `myTypes` variables to pre-generate the maximum variation of data to be averaged
- Modify the `returnMyTime` function to adjust the number of time elements you want captured.  if modified, you also need to have these values modified in the mk_mmba_tables.py script.
- Then run this script.  this script will create one row for each GID/unique type value in the myTypes variable for each table in the tables collection.  
- CAUTION:  this script deletes all tables that currently exist with the names of the tables given, in the schema given in the script.
- the positive thing about these tables, if they all have the same [exact data definitions](https://github.com/feomike/mmba_viz_processing/blob/master/data/create_tables.sql).  

Step 2 - file processing
------------------------
- download individual daily .tar files from the secure ftp site.  in fact these files are gziped .tar files.  if you use safari, it will automatically unzip the downloaded files, so that you are left with one .tar file per day per provider.  i store these in individual <provider>/tar directories.

- using [the myUtar.py script](https://github.com/feomike/mmba_viz_processing/blob/master/processing/myUtar.py), untar each daily .tar file to obtain the full list of daily JSON files.  it is critical that daily json files not be mixed in with other files, as file sloppy curation will result in significant downstream errors.  i store individual json files in <provider>/json/<year><month> directories


Step 3 - table insertion and data aggregation
---------------------------------------------
- modify the month variable to run in [the mmba.py](https://github.com/feomike/mmba_viz_processing/blob/master/processing/mmba.py) script line 101
- ensure the directory variables and file curation are in the appropriate places (see lines 368-369
- ensure that the dependencies are met.
- run [the mmba.py](https://github.com/feomike/mmba_viz_processing/blob/master/processing/mmba.py) script


Step 4 - map/visualization generation
-------------------------------------
- go generate some from the resulting aggreated tables
