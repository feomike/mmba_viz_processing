federal communications commission


This repo contains the data, processing, and visualization steps for creating the FCC's Measuring Mobile Broadband America visualizations DEMO/PILOT.

Data
----
The data directory contains back end table structure, dependent data (e.g hexagon cells) and other assets required to help support the process.  Source JSON files from the MMBA program are NOT stored or referred to in this repo. For more information on the source data file, please [the source Data Representation git repo](https://github.com/FCC/mobile-mba-androidapp/wiki/Data-Representation).

Processing
----------
The processing directory contains the procesisng steps and code used to transform the data from the source JSON files into aggregate data, statistics and visualizations.  
- the primary parsing script is [mmba_import.py](https://github.com/feomike/mmba_viz_processing/blob/master/processing/mmba_import.py).

Visualization
-------------
The visualization directory contains code and/or assets used to create the visualizations for end user interaction.
- [Alpha example map 1 - all generic](http://bl.ocks.org/feomike/7129604)
- [Alpha example map 2 - download speed](http://bl.ocks.org/feomike/7236848)
- [Beta example map 1 - download speed](http://bl.ocks.org/feomike/8429802)

License
-------

The project is a public domain work and is not subject to domestic or international copyright protection. See [the license file](https://github.com/feomike/mmba_viz_processing/blob/master/license.md) for additional information.

Members of the public and US government employees who wish to contribute are encourage to do so, but by contributing, dedicate their work to the public domain and waive all rights to their contribution under the terms of the [CC0 Public Domain Dedication](http://creativecommons.org/publicdomain/zero/1.0/).
