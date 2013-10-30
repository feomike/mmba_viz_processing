-- Table: mmba.tests

-- DROP TABLE mmba.tests;

CREATE TABLE mmba.tests
(
  file_name character varying(75),
  submission_type character varying(15),
  unix_timezone numeric,
  test_date character varying(35),
  unix_time numeric,
  downspeed numeric,
  upspeed numeric,
  rtt numeric,
  lost_packets numeric,
  manufacturer character varying(15),
  model character varying(30),
  os_type character varying(15),
  os_version numeric,
  network_type character varying(10),
  network_operator_name character varying(30),
  phone_type character varying(10),
  active_network_type character varying(10),
  signal_strength numeric,
  cell_id character varying(100),
  longitude numeric,
  latitude numeric,
  gid numeric
)
WITH (
  OIDS=FALSE
);
ALTER TABLE mmba.tests
  OWNER TO postgres;



-- Table: mmba."all"

-- DROP TABLE mmba."all";

CREATE TABLE mmba."all"
(
  ds_sum numeric,
  ds_count numeric,
  ds_average numeric,
  us_sum numeric,
  us_count numeric,
  us_average numeric,
  rtt_sum numeric,
  rtt_count numeric,
  rtt_average numeric,
  lp_sum numeric,
  lp_count numeric,
  lp_average numeric,
  mytype character varying(200),
  gid integer
)
WITH (
  OIDS=TRUE
);
ALTER TABLE mmba."all"
  OWNER TO postgres;

-- Index: mmba.mmba_all_gid_btree

-- DROP INDEX mmba.mmba_all_gid_btree;

CREATE INDEX mmba_all_gid_btree
  ON mmba."all"
  USING btree
  (gid );

-- Index: mmba.mmba_all_mytype_btree

-- DROP INDEX mmba.mmba_all_mytype_btree;

CREATE INDEX mmba_all_mytype_btree
  ON mmba."all"
  USING btree
  (mytype COLLATE pg_catalog."default" );


-- Table: mmba.provider

-- DROP TABLE mmba.provider;

CREATE TABLE mmba.provider
(
  ds_sum numeric,
  ds_count numeric,
  ds_average numeric,
  us_sum numeric,
  us_count numeric,
  us_average numeric,
  rtt_sum numeric,
  rtt_count numeric,
  rtt_average numeric,
  lp_sum numeric,
  lp_count numeric,
  lp_average numeric,
  mytype character varying(200),
  gid integer
)
WITH (
  OIDS=TRUE
);
ALTER TABLE mmba.provider
  OWNER TO postgres;

-- Index: mmba.mmba_provider_gid_btree

-- DROP INDEX mmba.mmba_provider_gid_btree;

CREATE INDEX mmba_provider_gid_btree
  ON mmba.provider
  USING btree
  (gid );

-- Index: mmba.mmba_provider_mytype_btree

-- DROP INDEX mmba.mmba_provider_mytype_btree;

CREATE INDEX mmba_provider_mytype_btree
  ON mmba.provider
  USING btree
  (mytype COLLATE pg_catalog."default" );


-- Table: mmba.network_type

-- DROP TABLE mmba.network_type;

CREATE TABLE mmba.network_type
(
  ds_sum numeric,
  ds_count numeric,
  ds_average numeric,
  us_sum numeric,
  us_count numeric,
  us_average numeric,
  rtt_sum numeric,
  rtt_count numeric,
  rtt_average numeric,
  lp_sum numeric,
  lp_count numeric,
  lp_average numeric,
  mytype character varying(200),
  gid integer
)
WITH (
  OIDS=TRUE
);
ALTER TABLE mmba.network_type
  OWNER TO postgres;

-- Index: mmba.mmba_network_type_gid_btree

-- DROP INDEX mmba.mmba_network_type_gid_btree;

CREATE INDEX mmba_network_type_gid_btree
  ON mmba.network_type
  USING btree
  (gid );

-- Index: mmba.mmba_network_type_mytype_btree

-- DROP INDEX mmba.mmba_network_type_mytype_btree;

CREATE INDEX mmba_network_type_mytype_btree
  ON mmba.network_type
  USING btree
  (mytype COLLATE pg_catalog."default" );


-- Table: mmba.active_network_type

-- DROP TABLE mmba.active_network_type;

CREATE TABLE mmba.active_network_type
(
  ds_sum numeric,
  ds_count numeric,
  ds_average numeric,
  us_sum numeric,
  us_count numeric,
  us_average numeric,
  rtt_sum numeric,
  rtt_count numeric,
  rtt_average numeric,
  lp_sum numeric,
  lp_count numeric,
  lp_average numeric,
  mytype character varying(200),
  gid integer
)
WITH (
  OIDS=TRUE
);
ALTER TABLE mmba.active_network_type
  OWNER TO postgres;

-- Index: mmba.mmba_active_network_type_gid_btree

-- DROP INDEX mmba.mmba_active_network_type_gid_btree;

CREATE INDEX mmba_active_network_type_gid_btree
  ON mmba.active_network_type
  USING btree
  (gid );

-- Index: mmba.mmba_active_network_type_mytype_btree

-- DROP INDEX mmba.mmba_active_network_type_mytype_btree;

CREATE INDEX mmba_active_network_type_mytype_btree
  ON mmba.active_network_type
  USING btree
  (mytype COLLATE pg_catalog."default" );


-- Table: mmba.provider_active_network_type

-- DROP TABLE mmba.provider_active_network_type;

CREATE TABLE mmba.provider_active_network_type
(
  ds_sum numeric,
  ds_count numeric,
  ds_average numeric,
  us_sum numeric,
  us_count numeric,
  us_average numeric,
  rtt_sum numeric,
  rtt_count numeric,
  rtt_average numeric,
  lp_sum numeric,
  lp_count numeric,
  lp_average numeric,
  mytype character varying(200),
  gid integer
)
WITH (
  OIDS=TRUE
);
ALTER TABLE mmba.provider_active_network_type
  OWNER TO postgres;

-- Index: mmba.mmba_provider_active_network_type_gid_btree

-- DROP INDEX mmba.mmba_provider_active_network_type_gid_btree;

CREATE INDEX mmba_provider_active_network_type_gid_btree
  ON mmba.provider_active_network_type
  USING btree
  (gid );

-- Index: mmba.mmba_provider_active_network_type_mytype_btree

-- DROP INDEX mmba.mmba_provider_active_network_type_mytype_btree;

CREATE INDEX mmba_provider_active_network_type_mytype_btree
  ON mmba.provider_active_network_type
  USING btree
  (mytype COLLATE pg_catalog."default" );


-- Table: mmba.provider_network_type

-- DROP TABLE mmba.provider_network_type;

CREATE TABLE mmba.provider_network_type
(
  ds_sum numeric,
  ds_count numeric,
  ds_average numeric,
  us_sum numeric,
  us_count numeric,
  us_average numeric,
  rtt_sum numeric,
  rtt_count numeric,
  rtt_average numeric,
  lp_sum numeric,
  lp_count numeric,
  lp_average numeric,
  mytype character varying(200),
  gid integer
)
WITH (
  OIDS=TRUE
);
ALTER TABLE mmba.provider_network_type
  OWNER TO postgres;

-- Index: mmba.mmba_provider_network_type_gid_btree

-- DROP INDEX mmba.mmba_provider_network_type_gid_btree;

CREATE INDEX mmba_provider_network_type_gid_btree
  ON mmba.provider_network_type
  USING btree
  (gid );

-- Index: mmba.mmba_provider_network_type_mytype_btree

-- DROP INDEX mmba.mmba_provider_network_type_mytype_btree;

CREATE INDEX mmba_provider_network_type_mytype_btree
  ON mmba.provider_network_type
  USING btree
  (mytype COLLATE pg_catalog."default" );

