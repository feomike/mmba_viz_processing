mmba processing steps workflow
==============================

- download file (w/ safari, b/c it unzips the .gzip files and stores a local .tar file)
- move the .tar file(s) in the same directory with the processing scripts (e.g. .py) files.
- copy the .tar file(s) to the ./tar file for back up, if necessary.
- make sure there is a .json subdirectory
- run myutar.py script to untar the file, it moves all json files from the current (e.g. source) directory to the ./json subdirectory
- make sure you edit and know what table the data wants to end up in (e.g. postgres table/schema); edit the mmba_import.py script accordingly; similarly make sure the dependencies exist (check mmba_import.py script for details)
- run the mmba_import.py script


	
