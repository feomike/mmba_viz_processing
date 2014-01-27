Workflow
========
- make mapbox projects for each higher level type (ds, us, rtt, lp) DONE

- for each lower level type (all, provider, network_type, active_network_type);
   export tiles
   use this structure:
   		cd /Applications/TileMill.app/Contents/Resources
   		./index.js export <proj> ~/Documents/MapBox/export/<name>.mbtiles
   			where <proj> is the project name (e.g. higher level)
   				  <name> is the output name you want
   before you export every time, replace the '{"datasource": {"tablename": }} 
   select statement, to get the right selection set

set attribution and naming on the tiles
- for each <name>.mbtiles file;
	change the tile name in the metadata
		update metadata set value = <value> where name = "name" 
	change the attribution to have the fcc logo
		update metadata set value = <logo> where name = "attribution"
- upload tiles to mapbox account


using mapbox.js examples things you want to add;
- toggle service - https://www.mapbox.com/mapbox.js/example/v1.0.0/wms/

- legend 	- https://www.mapbox.com/mapbox.js/example/v1.0.0/legend/
			- https://www.mapbox.com/mapbox.js/example/v1.0.0/legend-position/
			- https://www.mapbox.com/mapbox.js/example/v1.0.0/custom-legend/

			
- tool tip https://www.mapbox.com/mapbox.js/example/v1.0.0/marker-tooltips-outside-map/
- https://www.mapbox.com/mapbox.js/example/v1.0.0/custom-popup/
- moving tool tip - https://www.mapbox.com/mapbox.js/example/v1.0.0/movetip/
- map padding https://www.mapbox.com/mapbox.js/example/v1.0.0/paddingtopleft/
- tool tip https://www.mapbox.com/mapbox.js/example/v1.0.0/show-tooltips-on-hover/

- ui toggling https://www.mapbox.com/mapbox.js/example/v1.0.0/toggling-ui/#

- zoom lens https://www.mapbox.com/mapbox.js/example/v1.0.0/zoom-lens/
- https://www.mapbox.com/mapbox.js/example/v1.0.0/zoom-to-double-click/
- https://www.mapbox.com/mapbox.js/example/v1.0.0/interactivity-outside-map-layer/
- https://www.mapbox.com/mapbox.js/example/v1.0.0/layers/


- [example map 1 - all generic](http://bl.ocks.org/feomike/7129604)
- [example 2 - download speed](http://bl.ocks.org/feomike/7236848)
