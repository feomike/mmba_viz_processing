all
===
--all (1)
`(select  hex_75000.gid, geom, ds_average, ds_count from mmba.hex_75000, mmba.\"all\" where hex_75000.gid=\"all\".gid and ds_count > 1) as hex_ds`


Provider (4)
--------
--att
`(select  hex_75000.gid, geom, ds_average, ds_count from mmba.hex_75000, mmba.provider where hex_75000.gid=provider.gid and ds_count > 1 and mytype = 'att') as hex_ds`

--sprint
`(select  hex_75000.gid, geom, ds_average, ds_count from mmba.hex_75000, mmba.provider where hex_75000.gid=provider.gid and ds_count > 1 and mytype = 'sprint') as hex_ds`

--tmobile
`(select  hex_75000.gid, geom, ds_average, ds_count from mmba.hex_75000, mmba.provider where hex_75000.gid=provider.gid and ds_count > 1 and mytype = 'tmobile') as hex_ds`

--vz
`(select  hex_75000.gid, geom, ds_average, ds_count from mmba.hex_75000, mmba.provider where hex_75000.gid=provider.gid and ds_count > 1 and mytype = 'vz') as hex_ds`


Network_type (4)
------------
--LTE
`(select  hex_75000.gid, geom, ds_average, ds_count from mmba.hex_75000, mmba.network_type where hex_75000.gid=network_type.gid and ds_count > 1 and mytype = 'LTE') as hex_ds`

--eHRPD
`(select  hex_75000.gid, geom, ds_average, ds_count from mmba.hex_75000, mmba.network_type where hex_75000.gid=network_type.gid and ds_count > 1 and mytype = 'eHRPD') as hex_ds`

--"EVDO rev A"
`(select  hex_75000.gid, geom, ds_average, ds_count from mmba.hex_75000, mmba.network_type where hex_75000.gid=network_type.gid and ds_count > 1 and mytype = 'EVDO rev A') as hex_ds`

--"HSPA+"
`(select  hex_75000.gid, geom, ds_average, ds_count from mmba.hex_75000, mmba.network_type where hex_75000.gid=network_type.gid and ds_count > 1 and mytype = 'HSPA+') as hex_ds`


Active_Network_type (2)
------------
--mobile
`(select  hex_75000.gid, geom, ds_average, ds_count from mmba.hex_75000, mmba.active_network_type where hex_75000.gid=active_network_type.gid and ds_count > 1 and mytype = 'mobile') as hex_ds`

--WIFI
`(select  hex_75000.gid, geom, ds_average, ds_count from mmba.hex_75000, mmba.active_network_type where hex_75000.gid=active_network_type.gid and ds_count > 1 and mytype = 'WIFI') as hex_ds`
