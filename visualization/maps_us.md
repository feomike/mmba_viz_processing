all
===
--all (1)
- (select  hex_75000.gid, geom, us_average, us_count from mmba.hex_75000, mmba.\"all\" where hex_75000.gid=\"all\".gid and us_count > 1) as hex_us


Provider (4)
--------
--att
- (select  hex_75000.gid, geom, us_average, us_count from mmba.hex_75000, mmba.provider where hex_75000.gid=provider.gid and us_count > 1 and mytype = 'att') as hex_us

--sprint
- (select  hex_75000.gid, geom, us_average, us_count from mmba.hex_75000, mmba.provider where hex_75000.gid=provider.gid and us_count > 1 and mytype = 'sprint') as hex_us

--tmobile
- (select  hex_75000.gid, geom, us_average, us_count from mmba.hex_75000, mmba.provider where hex_75000.gid=provider.gid and us_count > 1 and mytype = 'tmobile') as hex_us

--vz
- (select  hex_75000.gid, geom, us_average, us_count from mmba.hex_75000, mmba.provider where hex_75000.gid=provider.gid and us_count > 1 and mytype = 'vz') as hex_us


Network_type (4)
------------
--LTE
- (select  hex_75000.gid, geom, us_average, us_count from mmba.hex_75000, mmba.network_type where hex_75000.gid=network_type.gid and us_count > 1 and mytype = 'LTE') as hex_us

--eHRPD
- (select  hex_75000.gid, geom, us_average, us_count from mmba.hex_75000, mmba.network_type where hex_75000.gid=network_type.gid and us_count > 1 and mytype = 'eHRPD') as hex_us

--"EVDO rev A"
- (select  hex_75000.gid, geom, us_average, us_count from mmba.hex_75000, mmba.network_type where hex_75000.gid=network_type.gid and us_count > 1 and mytype = 'EVDO rev A') as hex_us

--"HSPA+"
- (select  hex_75000.gid, geom, us_average, us_count from mmba.hex_75000, mmba.network_type where hex_75000.gid=network_type.gid and us_count > 1 and mytype = 'HSPA+') as hex_us


Active_Network_type (2)
------------
--mobile
- (select  hex_75000.gid, geom, us_average, us_count from mmba.hex_75000, mmba.active_network_type where hex_75000.gid=active_network_type.gid and us_count > 1 and mytype = 'mobile') as hex_us

--WIFI
- (select  hex_75000.gid, geom, us_average, us_count from mmba.hex_75000, mmba.active_network_type where hex_75000.gid=active_network_type.gid and us_count > 1 and mytype = 'WIFI') as hex_us
