Map/visualization generation
-------------------------------------
This set of visualizations are considered the alpha versions generated for testing in October 2013.

- for demo purposes, mapbox tiles for certain types were created.  this directory contains example mapbox project and style files
- again for demo purposes, example web interfaces were created.  these are purely for pilot or demonstration purposes and will be thrown away.  production visualizations have yet to be created

this directory contains example mapbox projects (mmba_ds, mmba_us, mmba_rtt, and mmba_lp).  these example projects work off of a) hexagon cells in postgres, with a selection set for a table aggregation based on a selected 'mytype' field to get the interested values.  see the files [maps_ds.md](https://github.com/feomike/mmba_viz_processing/blob/master/visualization/maps_ds.md), [maps_us.md](https://github.com/feomike/mmba_viz_processing/blob/master/visualization/maps_us.md), [maps_rtt.md](https://github.com/feomike/mmba_viz_processing/blob/master/visualization/maps_rtt.md), and [maps_lp.md](https://github.com/feomike/mmba_viz_processing/blob/master/visualization/maps_lp.md) for example sql statements to modify the project.mml files for generating different tiles.
