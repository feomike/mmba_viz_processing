#mike byrne
#federal communications commission
#july 23, 2013
#
#a python script used to untar and separare mmba files into appropriate locations
#this is critical to file curation
#general workflow;
#	- download tar.gzip files w/ safari.  safari will automatically unzip 
#		the files to .tar files
#	- once downloaded, place the .tar files in a subdirectory called tar under
#		the provider directory (e.g. ~/downloads/mmba/att/tar/
#   - from command line, cd into the directory ~/downloads/mmba
#	- edit the script to change the varibale named the theSourceDir to 
#		the appropriate provider name.  make sure that the provider name you edit to
#		the same name of the subdirectory for that provider.  for instance, for att
#		the directory structure needs to be called ~/downloads/mmba/att
#	- there needs to be two directories under the provider directory
#		one called tar, which contains all the .tar files
#		one called json.
#	- run this script.  it will extract all of the json files from the .tar files and 
#		and place them into the /json directory for that provider

import os
import fnmatch

theSourceDir = 'tmobile'
theJson = 'json'

#untar the file
#move the tar file to a drirectory
#crawl the parent directory for a json file, and move it to the files director
for dirpath, dirs, files in os.walk(theSourceDir):
    for filename in fnmatch.filter(files, '*.tar'):
        print dirpath + "/" + filename
        os.system('tar -xvf ' + dirpath + "/" + filename + " -C " + theSourceDir + "/" + theJson)
