#CREATE HIVE TABLES

create table read_assignment (exp_id int, sample_id int, read_id string, taxonomy_id int, taxonomy_name string, taxonomy_level string, score float, analysis_id int, status string, misc string) ROW FORMAT DELIMITED FIELDS TERMINATED BY '\t' STORED AS TEXTFILE LOCATION '/user/data/m3db/read_assignment';

create table reads (exp_id int, sample_id int, read_id string, mee float, avgq float, read_length int, overlap_flag string, read_desc string, hq_flag string, sequence string, quality_seq string, forward_read string, forward_qual string, reverse_read string, reverse_qual string) ROW FORMAT DELIMITED FIELDS TERMINATED BY '\t' STORED AS TEXTFILE LOCATION '/user/data/m3db/reads'; 