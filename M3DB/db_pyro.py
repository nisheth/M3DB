import psycopg2, psycopg2.extras, re, os, stat, pyhs2, Pyro4
from collections import defaultdict
from M3DB import configparse as cfg
#
_ConfigDefault = {
	"pg_server.dbms":            "PostgreSQL",
	"pg_server.database":            "m3db",
	"pg_server.user":            "user",
	"pg_server.password":        "pass",
	"pg_server.host":            "localhost",
	"pg_server.port":            "5445",
	"hive_server.dbms":          "Hive",
	"hive_server.database":      "m3db",
	"hive_server.user":          "hiveuser",
	"hive_server.password":      "hivepass",
	"hive_server.host":          "localhost",
	"hive_server.port":          "10000",
	"hive_server.auth":          "PLAIN",
	"general.datadir":           "/path/to/data/"
	}
config = cfg.LoadConfig('m3db.conf',_ConfigDefault)
datadir = "/path/to/m3db_data/"

class CLI(object):
	def __init__(self):
		pg_host = config["pg_server.host"]
		pg_user = config["pg_server.user"]
		pg_port = int(config["pg_server.port"])
		pg_pass = config["pg_server.password"]
		pg_db = config["pg_server.database"]
		self.config = config
		self._db_connection = psycopg2.connect(host=pg_host,user=pg_user,password=pg_pass,database=pg_db,port=pg_port)
		self._db_cur = self._db_connection.cursor()

	def createproject(self,args):
	# Create a new project #
		try:
			self._db_cur.execute("INSERT INTO project VALUES (default, '%s','%s','%s','%s','%s','%s')" % (args['name'],args['pi'],args['email'],args['desc'],args['user'],args['user']))
			self._db_connection.commit()
			self.__del__()
		except psycopg2.Error as e:
			self._db_connection.rollback()
			self.__del__()
			raise Exception(e.pgerror)

	def createexp(self,args):
		# Create a new experiment #
		try:
			self._db_cur.execute("SELECT project_id FROM project WHERE name = '%s'" % args['project'])
			projectid = int(re.sub('\W','',str(self._db_cur.fetchone())))
			self._db_cur.execute("INSERT INTO experiment VALUES(default,%i,'%s','%s','%s','%s','%s')" % (projectid,args['name'],args['date'],args['plat'],args['region'],args['user']))
			self._db_connection.commit()
			self.__del__()
		except psycopg2.Error as e:
			#self._db_connection.rollback()
			self.__del__()
			raise Exception(e.pgerror)

	def getprojectid(self,expname):
    # This may not be necessary or may need a different method #
		self._db_cur.execute("SELECT a.project_id FROM project a INNER JOIN experiment b ON a.project_id = b.project_id WHERE b.exp_name = '%s'" % expname)
		projectid = self._db_cur.fetchone()
		self.__del__()
		return projectid

	def insertfile(self,args):
    # Generic insert file in to postgres database #
		table = args['table']
		filename = open(args['filename'])
		self._db_cur.copy_from(filename,table)
		filename.close()
		self.__del__()

	def query(self,query):
	# Not implemented in CLI currently, used to run SQL lanaguage to interact postgres db #
		pass
		self._db_cur.execute(query)
		i = self._db_cur.fetchone()
		while i:
			print i[0]
			i = _db_cur.fetchone()
		self.__del__()

	def gettax(self,dbver):
    # Not Implemented inCLI currently, used to generate a dictionary from the taxonomy table #
		taxdict = defaultdict()
		dict_cur = self._db_connection.cursor(cursor_factory=psycopg2.extras.DictCursor)
		dict_cur.execute("select tax_name,tax_id from taxonomy where refdb_id = %i" % dbver)
		for row in dict_cur.fetchall():
			taxdict[row[0]] = row[1]
		return taxdict

	def getfasta(self,sampleid,fastaname):
    # Select the appropriate reads and create a fasta file from the HIVE reads table #
		try:
			if not os.path.isfile(fastaname):
            	hive_dir = "/path/to/M3DB/data/" # THIS HAS TO BE HARDCODED FOR NOW
	        	hive_host = self.config["hive_server.host"]
				hive_port = int(self.config["hive_server.port"])
				hive_user = str(self.config["hive_server.user"])
				hive_pass = self.config["hive_server.password"]
				hive_auth = self.config["hive_server.auth"]
				hive_db = self.config["hive_server.database"]
				_hs_connection = pyhs2.connect(host=hive_host, port=hive_port, authMechanism=hive_auth, user=hive_user,password=hive_pass, database=hive_db)
				_hs_cur =_hs_connection.cursor()

				outfile = open(fastaname,'w')
				_hs_cur.execute("SELECT read_id,read_desc,sequence from m3db.reads_tsv where sample_id = %i" % sampleid)
				for i in _hs_cur.fetch():
					outfile.write(">%s\t%s\n%s\n" % (i[0],i[1],i[2]))
				outfile.close()
				return "Done generating FASTA file"
			else:
				return "Found FASTA file already...\n This is okay if you already ran an analysis on this sample... Otherwise please remove this file and re-run the script\n Continuing..."
	:$	except Exception as e:
			print e
			raise Exception(e)
	def getaid(self,value):
		self._db_cur.execute("SELECT analysis_id FROM analysis WHERE parameters = 'Cutoff: %0.1f';" % float(value))
		analysisid = re.sub("\'|\(|\)|\,","",str(self._db_cur.fetchone()))
		if analysisid == None:
			desc = "The RDP Classifier is a naive Bayesian classifier which was developed to provide rapid taxonomic placement based on rRNA sequence data. The RDP Classifier can rapidly and accurately classify bacterial and archaeal 16s rRNA sequences, and Fungal LSU sequences. It provides taxonomic assignments from domain to genus, with confidence estimates for each assignment. The RDP Classifier likely can be adapted to additional phylogenetically coherent bacterial taxonomies."
			tool = "RDP Classifier"
			self._db_cur.execute("INSERT INTO analysis (name,description,parameters,comments,refdb_id) SELECT '%s','%s','Cutoff: %0.1f','%s',%i WHERE NOT EXISTS (select parameters from analysis where parameters = 'Cutoff: %f');" % (tool,desc,float(thresh),"Added through m3dbcli",1,float(thresh)))
			self._db_connection.commit()
			self._db_cur.execute("SELECT analysis_id FROM analysis WHERE parameters = 'Cutoff: %0.1f';" % float(thresh))
			analysisid = re.sub("\'|\(|\)|\,","",str(self._db_cur.fetchone()))
			self.__del__()
		return analysisid

	def insertsample(self,args):
    # Not currently implemented in CLI, will be used if someone has already demultiplexed/merged/filtered their reads #
    # Will probably just use the web interface function here (though I can reimplement it as a CLI feature) #
		pass

	def getexpid(self,expname):
		try:
			self._db_cur.execute("SELECT exp_id FROM experiment WHERE name = '%s';" % expname)
			expid = int(re.sub('\W','',str(self._db_cur.fetchone())))
		except Exception as e:
			print e
			raise Exception(e)
		return expid
	def getsampleid(self,sname,expid):
    # Do not insert if the sample already exists (covered by the WHERE NOT EXISTS...)
		self._db_cur.execute("SELECT sample_id FROM sample WHERE name = '%s' and exp_id = %i;" % (sname,expid))
		sampleid = int(re.sub('\W','',str(self._db_cur.fetchone())))
		return sampleid
	def getsamplename(self,fastq):
		nucleotides={'dna':re.compile('^[acgtn]*$',re.I)}
		def checknucleotides(header):
			if re.search(nucleotides['dna'],header) and len(header) > 1:
				return True
			else:
				return False
			with open(fastq) as fq:
				fqheader = re.split(':',fq.next().strip())
				matches = filter(checknucleotides, fqheader)
			try:
				index1 = matches[0]
				index2 = matches[1]
			except:
				index1 = "NA"
				index2 = "NA"
			return index1,index2

	def insertsampstat(self,sampstats,exp,samplename,fastq):
	# This inserts the sample statistics file created by MEFIT. It also creates an entry in the sample table if the sample has not already been created.
		# Do not insert if the sample already exists (covered by the WHERE NOT EXISTS...)
		try:
			expid = self.getexpid(exp)
		except psycopg2.Error as e:
			raise Exception(e.pgerror)
		sampstats.insert(0,expid)
		try:
			self._db_cur.execute("INSERT INTO sample (exp_id,name,index1,index2) SELECT %i,'%s','%s','%s' WHERE NOT EXISTS (SELECT name from sample where name='%s' and exp_id = %i);" % (expid,samplename,"index1","index2",samplename,expid))
			self._db_connection.commit()
		except psycopg2.Error as e:
			self._db_connection.rollback()
			print e.pgerror
		sampleid = self.getsampleid(samplename,expid)
		sampstats.insert(0,sampleid)
		try: # Insert the data
			dict_cur = self._db_connection.cursor(cursor_factory=psycopg2.extras.DictCursor)
			dict_cur.execute("INSERT INTO sample_statistics VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",sampstats)
			self._db_connection.commit()
		except psycopg2.Error as e: # The table has a check/trigger so if data already exists the Postgres Database will throw an error, this will catch it.
			self._db_connection.rollback()
			self.__del__()
		#	raise Exception(e.pgerror)
		self.__del__()
		return sampleid,expid

	def insertabundance(self,abundanceprof,flag):
		os.chmod((abundanceprof),0664)
		if flag:
		    abundanceprof = open(abundanceprof)
		    self._db_cur.copy_from(abundanceprof,'abundance_profile',sep='\t',columns=('sample_id','taxonomy_level','taxonomy_name','num_reads','abundance','score','analysis_id','taxonomy_id','exp_id','status','miscellaneous'))
		    self._db_connection.commit()
		    abundanceprof.close()
		else:
		    abundanceprof = open(abundanceprof)
		    self._db_cur.copy_from(abundanceprof,'abundance_profile',sep='\t',columns=('exp_id','sample_id','analysis_id','taxonomy_id','num_reads','abundance','score','status','miscellaneous','taxonomy_level','taxonomy_name'))
		    self._db_connection.commit()
		    abundanceprof.close()
		self.__del__()
    
	def insertreadassign(self,readassign):
    # See TODO above, this will eventually be called by STIRRUPS and RDP to inset their data
		hive_dir = "/path/to/M3DB/data/" # THIS HAS TO BE HARDCODED FOR NOW
                hive_host = self.config["hive_server.host"]
                hive_port = int(self.config["hive_server.port"])
                hive_user = str(self.config["hive_server.user"])
                hive_pass = self.config["hive_server.password"]
                hive_auth = self.config["hive_server.auth"]
                hive_db = self.config["hive_server.database"]
		readassign = readassign.split('/')[-1]
		os.chmod((hive_dir + readassign),0664)
                try:
                        _hs_connection = pyhs2.connect(host=hive_host, port=hive_port, authMechanism=hive_auth, user=hive_user,password=hive_pass, database=hive_db)
                        _hs_cur =_hs_connection.cursor()
			_hs_cur.execute("LOAD DATA LOCAL INPATH '%s' INTO TABLE m3db.read_assignment" % (hive_dir + readassign))
			self.__del__()
		except Exception as e:
			print e
			raise Exception(e)

	def insertreads(self,fastq):
	# Insert parsed sequence data after MeFit has run #
		hive_dir = "/path/to/M3DB/data/" # THIS HAS TO BE HARDCODED FOR NOW
		hive_host = self.config["hive_server.host"]
                hive_port = int(self.config["hive_server.port"])
                hive_user = str(self.config["hive_server.user"])
                hive_pass = self.config["hive_server.password"]
                hive_auth = self.config["hive_server.auth"]
                hive_db = self.config["hive_server.database"]

		try:
			_hs_connection = pyhs2.connect(host=hive_host, port=hive_port, authMechanism=hive_auth, user=hive_user,password=hive_pass, database=hive_db)
	                _hs_cur =_hs_connection.cursor()
			os.chmod((hive_dir + fastq),0664)
			_hs_cur = _hs_connection.cursor()
			_hs_cur.execute("LOAD DATA LOCAL INPATH '%s' INTO TABLE m3db.reads_tsv" % (hive_dir + fastq))
			self.__del__()
		except Exception as e:
			print e
			raise Exception(e)

	def __del__(self):
		self._db_connection.close()
		try:
			self._hs_connection.close()
		except:
			pass

def main():
	daemon = Pyro4.Daemon(host="127.0.0.1")
	ns = Pyro4.locateNS()
	uri = daemon.register(CLI)
	ns.register("m3db.cli",uri)
	print uri
	daemon.requestLoop()
if __name__ == "__main__":
	main()
