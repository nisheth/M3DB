Massive Multiomic Microbiome Database (M3DB)
=============
Description: This is a software tool written to merge, filter and perform metagomic analysis on 16S reads obtained from NGS data then store said data in Hadoop/Hive and PostgreSQL Data Warehouses.

Author: Shaun Norris (norrissw [at] vcu.edu)

Date: June 22, 2015

Version : v1.0

Contact: Nihar U. Sheth (nsheth [at] vcu.edu)

#Requirements: 
Python 2.6 or 2.7 (not tested on version 3.x)

##Python Modules:

* psycopg2 (available via pip install psycopg2) Project Page: http://initd.org/psycopg/

* pyhs2 (available via pip install pyhs2) Project Page: https://github.com/BradRuderman/pyhs2

* configparser (available via pip install configparser) Project Page: http://docs.python.org/3/library/configparser.html

* numpy (available via pip install numpy) http://www.numpy.org/

* HTSeq (available via pip install HTSeq) https://pypi.python.org/pypi/HTSeq [required]
 
##Hadoop/Hive & PostgreSQL
###M3DB is developed and compatible with all of the following options for Hadoop/Hive/PostgreSQL:

Use our Setup: To request access to these services at VCU, contact Nihar Sheth at nsheth [at] vcu.edu

Setup your Own Cluster:

[ Manually ]
Most Difficult, requires own hardware and extensive configuration
* Hadoop 2.6.0: https://hadoop.apache.org/releases.html
* Hive 0.14.0: https://hive.apache.org/downloads.html
* PostgreSQL 9.4: http://www.postgresql.org/download/
* Hadoop FDW for PostgreSQL: https://bitbucket.org/openscg/hadoop_fdw

[Assisted Setup]
Proprietary solutions easy configuration but still requires own hardware

* HortonWorks: http://www.hortonworks.com
* Cloudera: http://www.cloudera.com
* Datastax: http://www.datastax.com

[ Cloud Solutions ]
Utilizing cloud based solutions extremely simplifies the setup of this step
Microsoft Azure Services:
* HDInsight: http://azure.microsoft.com/en-us/services/hdinsight/
* HortonWorks v2.2: http://hortonworks.com/partner/microsoft/
* DataStax v2.0: https://academy.datastax.com/demos/enterprise-deployment-microsoft-azure-cloud
* Cloudera: http://azure.microsoft.com/blog/2014/12/17/how-to-deploy-the-cloudera-evaluation-cluster-in-azure/

## Classification Tools:
* Jellyfish (mer counter): http://www.genome.umd.edu/jellyfish.html
* CASPER (Context-Aware Scheme for Paired-End Read): http://best.snu.ac.kr/casper
* STIRRUPS: http://sourceforge.net/projects/stirrups/files/
* RDP: https://github.com/rdpstaff/classifier
* Kracken: (not yet supported)
* CHIIME: (not yet supported)

# M3DB Command Line Tool: 
	## Installation:
	[This assumes you already have appropriately setup the requirements]
	$ source bin/setup_m3dbcli.sh
	(Incorporate m3dbcli into PATH)
	$ psql < m3db_postgre.sql
	(Create PostgreSQL Tables)
	$ hive -f m3db_hive.sql
	(Create Hive Tables)

	## Usage:

	$ m3dbcli --help
	[displays help information]

	$ m3dbcli <argument> --help
	[displays specific help information]

	## Example:
	
	[1. Create Project]
	$ m3dbcli createproject --name MyProject --pi FirstName,LastName --email you@yourdomain.com --desc Description --user youruserid
	
	[2. Create Experiment]
	$ m3dbcli createexp --name MyExperiment --date 12-31-2015 --plat ILLUMINA --project MyProject --region 16S --user youruserid
	
	[3. Merge/Filter, Upload & Store Sequence Data]
	$ m3dbcli uploadsample --project MyProject --exp MyExperiment --samplename Sample01 --forward forward_16sreads.fastq --reverse reverse_16sreads.fastq --overlap 
	(optionally --meep N.N and --patch_length NN may be specified otherwise defaults of 1.0 and 10 are used)

	[4. Analyze Using STIRRUPS]
	$ m3dbcli stirrups --exp MyExperiment --samplename Sample01
	(optionally --library reference.fasta may be used to specify a different reference file)

	[5. Analyze Using RDP]
	$ m3dbcli rdp --exp MyExperiment --samplename Sample01
	(optionally --threshold may be specified if a value other than 0.8 is preferred)

# M3DB Web Interface Setup:
  In order to use the web interface you must have Django 1.7.x or newer. Customize the settings.py file to match your system(s) architecture. To serve the content Gunicorn (19.2.x or newer) and Nginx (1.6.x or newer) are recommend for production environments.
  
