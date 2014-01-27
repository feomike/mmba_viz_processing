all
===
--all (1)
- (select  hex_75000.gid, geom, lp_average, lp_count from mmba.hex_75000, mmba.\"all\" where hex_75000.gid=\"all\".gid and lp_count > 1) as hex_lp


Provider (4)
--------
--att
- (select  hex_75000.gid, geom, lp_average, lp_count from mmba.hex_75000, mmba.provider where hex_75000.gid=provider.gid and lp_count > 1 and mytype = 'att') as hex_lp

--sprint
- (select  hex_75000.gid, geom, lp_average, lp_count from mmba.hex_75000, mmba.provider where hex_75000.gid=provider.gid and lp_count > 1 and mytype = 'sprint') as hex_lp

--tmobile
- (select  hex_75000.gid, geom, lp_average, lp_count from mmba.hex_75000, mmba.provider where hex_75000.gid=provider.gid and lp_count > 1 and mytype = 'tmobile') as hex_lp

--vz
- (select  hex_75000.gid, geom, lp_average, lp_count from mmba.hex_75000, mmba.provider where hex_75000.gid=provider.gid and lp_count > 1 and mytype = 'vz') as hex_lp


Network_type (4)
------------
--LTE
- (select  hex_75000.gid, geom, lp_average, lp_count from mmba.hex_75000, mmba.network_type where hex_75000.gid=network_type.gid and lp_count > 1 and mytype = 'LTE') as hex_lp

--eHRPD
- (select  hex_75000.gid, geom, lp_average, lp_count from mmba.hex_75000, mmba.network_type where hex_75000.gid=network_type.gid and lp_count > 1 and mytype = 'eHRPD') as hex_lp

--"EVDO rev A"
- (select  hex_75000.gid, geom, lp_average, lp_count from mmba.hex_75000, mmba.network_type where hex_75000.gid=network_type.gid and lp_count > 1 and mytype = 'EVDO rev A') as hex_lp

--"HSPA+"
- (select  hex_75000.gid, geom, lp_average, lp_count from mmba.hex_75000, mmba.network_type where hex_75000.gid=network_type.gid and lp_count > 1 and mytype = 'HSPA+') as hex_lp


Active_Network_type (2)
------------
--mobile
- (select  hex_75000.gid, geom, lp_average, lp_count from mmba.hex_75000, mmba.active_network_type where hex_75000.gid=active_network_type.gid and lp_count > 1 and mytype = 'mobile') as hex_lp

--WIFI
- (select  hex_75000.gid, geom, lp_average, lp_count from mmba.hex_75000, mmba.active_network_type where hex_75000.gid=active_network_type.gid and lp_count > 1 and mytype = 'WIFI') as hex_lp
