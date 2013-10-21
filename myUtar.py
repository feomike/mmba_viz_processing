#mike byrne
#federal communications commission
#july 23, 2013
#
#a python script used to untar and separare mmba files into appropriate locations
import os
import fnmatch

theSourceDir = 'vz'
theJson = 'json'

#untar the file
#move the tar file to a drirectory
#crawl the parent directory for a json file, and move it to the files director
for dirpath, dirs, files in os.walk(theSourceDir):
    for filename in fnmatch.filter(files, '*.tar'):
        print dirpath + "/" + filename
        os.system('tar -xvf ' + dirpath + "/" + filename + " -C " + theSourceDir + "/" + theJson)
