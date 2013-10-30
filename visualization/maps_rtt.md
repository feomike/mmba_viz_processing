all
===
--all (1)
(select  hex_75000.gid, geom, rtt_average, rtt_count from mmba.hex_75000, mmba.\"all\" where hex_75000.gid=\"all\".gid and rtt_count > 1) as hex_rtt


Provider (4)
--------
--att
(select  hex_75000.gid, geom, rtt_average, rtt_count from mmba.hex_75000, mmba.provider where hex_75000.gid=provider.gid and rtt_count > 1 and mytype = 'att') as hex_rtt

--sprint
- (select  hex_75000.gid, geom, rtt_average, rtt_count from mmba.hex_75000, mmba.provider where hex_75000.gid=provider.gid and rtt_count > 1 and mytype = 'sprint') as hex_rtt

--tmobile
- (select  hex_75000.gid, geom, rtt_average, rtt_count from mmba.hex_75000, mmba.provider where hex_75000.gid=provider.gid and rtt_count > 1 and mytype = 'tmobile') as hex_rtt

--vz
- (select  hex_75000.gid, geom, rtt_average, rtt_count from mmba.hex_75000, mmba.provider where hex_75000.gid=provider.gid and rtt_count > 1 and mytype = 'vz') as hex_rtt


Network_type (4)
------------
--LTE
- (select  hex_75000.gid, geom, rtt_average, rtt_count from mmba.hex_75000, mmba.network_type where hex_75000.gid=network_type.gid and rtt_count > 1 and mytype = 'LTE') as hex_rtt

--eHRPD
- (select  hex_75000.gid, geom, rtt_average, rtt_count from mmba.hex_75000, mmba.network_type where hex_75000.gid=network_type.gid and rtt_count > 1 and mytype = 'eHRPD') as hex_rtt

--"EVDO rev A"
- (select  hex_75000.gid, geom, rtt_average, rtt_count from mmba.hex_75000, mmba.network_type where hex_75000.gid=network_type.gid and rtt_count > 1 and mytype = 'EVDO rev A') as hex_rtt

--"HSPA+"
- (select  hex_75000.gid, geom, rtt_average, rtt_count from mmba.hex_75000, mmba.network_type where hex_75000.gid=network_type.gid and rtt_count > 1 and mytype = 'HSPA+') as hex_rtt


Active_Network_type (2)
------------
--mobile
- (select  hex_75000.gid, geom, rtt_average, rtt_count from mmba.hex_75000, mmba.active_network_type where hex_75000.gid=active_network_type.gid and rtt_count > 1 and mytype = 'mobile') as hex_rtt

--WIFI
- (select  hex_75000.gid, geom, rtt_average, rtt_count from mmba.hex_75000, mmba.active_network_type where hex_75000.gid=active_network_type.gid and rtt_count > 1 and mytype = 'WIFI') as hex_rtt
