all
===
--all (1)
(select  ptsinhex4.gid, geom, ds_average, ds_count 
  from mmba.ptsinhex4, mmba.all
  where ptsinhex4.gid="all".gid
  and ds_count > 1
) as hex

Provider (4)
--------
--att
(select  ptsinhex4.gid, geom, ds_average, ds_count 
  from mmba.ptsinhex4, mmba.provider
  where ptsinhex4.gid=provider.gid
  and ds_count > 1 and mytype = 'att'
) as hex

--sprint
(select  ptsinhex4.gid, geom, ds_average, ds_count 
  from mmba.ptsinhex4, mmba.provider
  where ptsinhex4.gid=provider.gid
  and ds_count > 1 and mytype = 'sprint'
) as hex

--tmobile
(select  ptsinhex4.gid, geom, ds_average, ds_count 
  from mmba.ptsinhex4, mmba.provider
  where ptsinhex4.gid=provider.gid
  and ds_count > 1 and mytype = 'tmobile'
) as hex

--vz
(select  ptsinhex4.gid, geom, ds_average, ds_count 
  from mmba.ptsinhex4, mmba.provider
  where ptsinhex4.gid=provider.gid
  and ds_count > 1 and mytype = 'vz'
) as hex

Network_type (4)
------------
--LTE
(select  ptsinhex4.gid, geom, ds_average, ds_count 
  from mmba.ptsinhex4, mmba.network_type
  where ptsinhex4.gid=network_type.gid
  and ds_count > 1 and mytype = 'LTE'
) as hex

--eHRPD
(select  ptsinhex4.gid, geom, ds_average, ds_count 
  from mmba.ptsinhex4, mmba.network_type
  where ptsinhex4.gid=network_type.gid
  and ds_count > 1 and mytype = 'eHRPD'
) as hex

--"EVDO rev A"
(select  ptsinhex4.gid, geom, ds_average, ds_count 
  from mmba.ptsinhex4, mmba.network_type
  where ptsinhex4.gid=network_type.gid
  and ds_count > 1 and mytype = 'EVDO rev A'
) as hex

--"HSPA+"
(select  ptsinhex4.gid, geom, ds_average, ds_count 
  from mmba.ptsinhex4, mmba.network_type
  where ptsinhex4.gid=network_type.gid
  and ds_count > 1 and mytype = 'HSPA+'
) as hex

Active_Network_type (2)
------------
--mobile
(select  ptsinhex4.gid, geom, ds_average, ds_count 
  from mmba.ptsinhex4, mmba.active_network_type
  where ptsinhex4.gid=active_network_type.gid
  and ds_count > 1 and mytype = 'mobile'
) as hex

--WIFI
(select  ptsinhex4.gid, geom, ds_average, ds_count 
  from mmba.ptsinhex4, mmba.active_network_type
  where ptsinhex4.gid=active_network_type.gid
  and ds_count > 1 and mytype = 'WIFI'
) as hex

- example map 1 - all - http://bl.ocks.org/feomike/raw/7129604/
- example map 2 - att - http://bl.ocks.org/feomike/raw/7129721
- example map 3 - sprint - http://bl.ocks.org/feomike/raw/7129750
- example map 4 - tmobile - http://bl.ocks.org/feomike/7129763
- example map 5 - vz - http://bl.ocks.org/feomike/raw/7129779
- example map 6 - lte - http://bl.ocks.org/feomike/raw/7129790
- example map 7 - eHRPD - http://bl.ocks.org/feomike/raw/7129805
- example map 8 - evdo_rev_a - http://bl.ocks.org/feomike/raw/7129814
- example map 9 - hpsa+ - http://bl.ocks.org/feomike/raw/7129834
- example map 10 - mobile - http://bl.ocks.org/feomike/raw/7129841
- example map 11 - WIFI - http://bl.ocks.org/feomike/7129855

GIST
- add index.html

<!DOCTYPE html>
<html>
<head>
	<meta name='viewport' content='width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no' />
  	<script src='//api.tiles.mapbox.com/mapbox.js/v1.3.1/mapbox.js'></script>
  	<link href='//api.tiles.mapbox.com/mapbox.js/v1.3.1/mapbox.css' rel='stylesheet' />
	<style>
    	body { margin:0; padding:0; }
    	#map { position:absolute; top:0; bottom:0; width:100%; }
  	</style>
</head>
<body>
<div id='map'></div>
<script type='text/javascript'>
        //string multiple maps in the next statement
	L.mapbox.map('map', 'fcc.map-kzt95hy6,fcc.mmba_all')
        .setView([40, -94.50], 4);;
</script>
</body>
</html>

-add readme.md
this is example map 1
