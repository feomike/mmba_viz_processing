Processing_Readme.md
==============

The processing folder contains several scripts and folders;

Folders
-------

- The [alpha](https://github.com/feomike/mmba_viz_processing/tree/master/processing/alpha) folder contains original alpha processing scripts used to parse and populate alpha version maps circa Oct. 2013.


Files
-----
- The [mmba_import.py]() script is the basic import script for importing raw json files into a postgres dataset
- The [mmba_investigate.py]() script contains a framework for search through all of the json files
- [myUtar.py]() script extracts all of the .json files from the .tar file(s) in the current directory to a ./json/ subdirectory (which is configurable in the script)
- The [workflow.md]() file contains basic workflow to process the data