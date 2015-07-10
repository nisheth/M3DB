#!/usr/bin/env python
# Toying with the idea of separating out the database entirely from the api.
import psycopg2, psycopg2.extras, re, os
from pyhive import presto
from collections import defaultdict

def __init__(config):
    # Initialize the database connections when needed. #
    pg_host = config["pg_server.host"]
    pg_user = config["pg_server.user"]
    pg_port = int(config["pg_server.port"])
    pg_pass = config["pg_server.password"]
    pg_db = config["pg_server.database"]
    hive_host = config["hive_server.host"]
    hive_port = int(config["hive_server.port"])
    hive_user = config["hive_server.user"]
    hive_pass = config["hive_server.password"]
    hive_auth = config["hive_server.auth"]
    _db_connection = psycopg2.connect(host=pg_host,user=pg_user,database=pg_db,port=pg_port) # TRUST current used
    _db_cur = _db_connection.cursor()
    _hs_connection = presto.connect(hive_host) #default account
    _hs_cur = _hs_connection.cursor()
    return _db_connection,_db_cur,_hs_connection,_hs_cur
def createproject(config,args):
    # Create a new project #
    _db_connection,_db_cur,_hs_connection,_hs_cur = __init__(config)
    _db_cur.execute("INSERT INTO project VALUES (default, '%s','%s','%s','%s','%s','%s')" % (args.name,args.pi,args.email,args.desc,args.user,args.user))
    _db_connection.commit()
    __del__(_db_connection,_hs_connection)
def getprojectid(config,expname):
    # This may not be necessary or may need a different method #
    _db_connection,_db_cur,_hs_connection,_hs_cur = __init__(config)
   # _db_cur.execute("SELECT project_id FROM project WHERE name='%s'" % args.project)
    _db_cur.execute("SELECT a.project_id FROM project a INNER JOIN experiment b ON a.project_id = b.project_id WHERE b.exp_name = '%s'" % expname)
    return _db_cur.fetchone()
    __del__(_db_connection,_hs_connection)
def createexp(config,args):
    # Create a new experiment #
    _db_connection,_db_cur,_hs_connection,_hs_cur = __init__(config)
    _db_cur.execute("SELECT project_id FROM project WHERE name = '%s'" % args.project)
    projectid = int(re.sub('\W','',str(_db_cur.fetchone())))
    _db_cur.execute("INSERT INTO experiment VALUES(default,%i,'%s','%s','%s','%s','%s')" % (projectid,args.name,args.date,args.plat,args.region,args.user))
    _db_connection.commit()
    __del__(_db_connection,_hs_connection)
def insertfile(config,args):
    # Generic insert file in to postgres database #
    _db_connection,_db_cur,_hs_connection,_hs_cur = __init__(config)
    table = args.table
    filename = open(args.filename)
    _db_cur.copy_from(filename,table)
    #_db_cur.execute("COPY %s FROM '%s' WITH DELIMITER E'\t';" % (table,filename))
    filename.close()
    __del__(_db_connection,_hs_connection)
def query(config,query):
    # Not implemented in CLI currently, used to run SQL lanaguage to interact postgres db #
    _db_connection,_db_cur,_hs_connection,_hs_cur = __init__(config)
    _db_cur.execute(query)
    i = _db_cur.fetchone()
    while i:
        print i[0]
        i = _db_cur.fetchone()
    __del__(_db_connection,_hs_connection)

def gettax(config,dbver):
    # Not Implemented inCLI currently, used to generate a dictionary from the taxonomy table #
    taxdict = defaultdict()
    _db_connection,_db_cur,_hs_connection,_hs_cur = __init__(config)
    dict_cur = _db_connection.cursor(cursor_factory=psycopg2.extras.DictCursor)
    dict_cur.execute("select tax_name,tax_id from taxonomy where refdb_id = %i" % dbver)
    for row in dict_cur.fetchall():
        taxdict[row[0]] = row[1]
    __del__(_db_connection,_hs_connection)
    return taxdict
# def getsidexp(config,samplename):
#     _db_connection,_db_cur,_hs_connection,_hs_cur = __init__(config)
#     _db_cur.execute("SELECT exp_name FROM sample WHERE name = '%s';" % samplename)
#     expname = re.sub("\'|\(|\)|\,","",str(_db_cur.fetchone()))
#     _db_cur.execute("SELECT exp_id FROM sample WHERE name = '%s';" % samplename)
#     expname = re.sub("\'|\(|\)|\,","",str(_db_cur.fetchone()))
#     _db_cur.execute("SELECT sample_id FROM sample WHERE name = '%s';" % samplename)
#     sampleid= re.sub("\'|\(|\)|\,","",str(_db_cur.fetchone()))
#     __del__(_db_connection,_hs_connection)
#     return expname,sampleid
def getfasta(config,sampleid,fastaname):
    # Select the appropriate reads and create a fasta file from the HIVE reads table #
    if not os.path.isfile(fastaname):
        outfile = open(fastaname,'w')
        try:
            _db_connection,_db_cur,_hs_connection,_hs_cur = __init__(config)
        except:
            print ""
        _hs_cur.execute("SELECT read_id,read_desc,sequence from m3db.reads where sample_id = %i" % sampleid)
        for i in _hs_cur.fetch():
            outfile.write(">%s\t%s\n%s\n" % (i[0],i[1],i[2]))
        outfile.close()
        __del__(_db_connection,_hs_connection)
        print "Done generating FASTA file"
    else:
        print "Found FASTA file already...\n This is okay if you already ran an analysis on this sample... Otherwise please remove this file and re-run the script\n Continuing..."
def getaid(config,value):
    _db_connection,_db_cur,_hs_connection,_hs_cur = __init__(config)
    _db_cur.execute("SELECT analysis_id FROM analysis WHERE parameters = 'Cutoff: %0.1f';" % float(value))
    analysisid = re.sub("\'|\(|\)|\,","",str(_db_cur.fetchone()))
    if analysisid == None:
        desc = "The RDP Classifier is a naive Bayesian classifier which was developed to provide rapid taxonomic placement based on rRNA sequence data. The RDP Classifier can rapidly and accurately classify bacterial and archaeal 16s rRNA sequences, and Fungal LSU sequences. It provides taxonomic assignments from domain to genus, with confidence estimates for each assignment. The RDP Classifier likely can be adapted to additional phylogenetically coherent bacterial taxonomies."
        tool = "RDP Classifier"
        _db_cur.execute("INSERT INTO analysis (name,description,parameters,comments,refdb_id) SELECT '%s','%s','Cutoff: %0.1f','%s',%i WHERE NOT EXISTS (select parameters from analysis where parameters = 'Cutoff: %f');" % (tool,desc,float(thresh),"Added through m3dbcli",1,float(thresh)))
        _db_connection.commit()
        _db_cur.execute("SELECT analysis_id FROM analysis WHERE parameters = 'Cutoff: %0.1f';" % float(thresh))
        analysisid = re.sub("\'|\(|\)|\,","",str(_db_cur.fetchone()))
    __del__(_db_connection,_hs_connection)
    return analysisid
def insertsample(config,args):
    # Not currently implemented in CLI, will be used if someone has already demultiplexed/merged/filtered their reads #
    # Will probably just use the web interface function here (though I can reimplement it as a CLI feature) #
    pass
def getexpid(config,expname):
    _db_connection,_db_cur,_hs_connection,_hs_cur = __init__(config)
    # Do not insert if the sample already exists (covered by the WHERE NOT EXISTS...)
    try:
        _db_cur.execute("SELECT exp_id FROM experiment WHERE name = '%s';" % expname)
        expid = int(re.sub('\W','',str(_db_cur.fetchone())))
    except:
        print "Failed to get Experiment ID, Check Experiment ID and try again"
    __del__(_db_connection,_hs_connection)
    return expid
def getsampleid(config,sname,expid):
    _db_connection,_db_cur,_hs_connection,_hs_cur = __init__(config)
    # Do not insert if the sample already exists (covered by the WHERE NOT EXISTS...)
    _db_cur.execute("SELECT sample_id FROM sample WHERE name = '%s' and exp_id = %i;" % (sname,expid))
    sampleid = int(re.sub('\W','',str(_db_cur.fetchone())))
    __del__(_db_connection,_hs_connection)
    return sampleid
def getsamplename(config,fastq):
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
def insertsampstat(config,filename,exp,samplename,fastq):
    # This inserts the sample statistics file created by MEFIT. It also creates an entry in the sample table if the sample has not already been created.
    with open(filename,'r') as f: # Read out the data...
        header = re.split('\t',f.next().strip())
        line = re.split('\t',re.sub('\%','',f.next().strip()))
    index1,index2 = getsamplename(config,fastq)
    _db_connection,_db_cur,_hs_connection,_hs_cur = __init__(config)
    # Do not insert if the sample already exists (covered by the WHERE NOT EXISTS...)
    expid = getexpid(config,exp)
    line.pop(0) #remove the samplename
    line.insert(0,expid)
    try:
        _db_cur.execute("INSERT INTO sample (exp_id,name,index1,index2) SELECT %i,'%s','%s','%s' WHERE NOT EXISTS (SELECT name from sample where name='%s' and exp_id = %i);" % (expid,samplename,index1,index2,samplename,expid))
        _db_connection.commit()
    except:
        _db_connection.rollback()
        print "Found Sample... continuing..."
    sampleid = getsampleid(config,samplename,expid)
    line.insert(0,sampleid)
    with open(filename,'w') as o: # Reformat the data so that its ready for insertion to Postgres DB
        header,line = re.sub(' ','\t',re.sub('\'|,|\[|\]','',repr(header))),re.sub(' ','\t',re.sub('\'|,|\[|\]','',repr(line)))
    	o.write("%s\n" % header)
        o.write(line)
    try: # Insert the data
    	filename = open(filename)
    	_db_cur.copy_expert("COPY sample_statistics FROM STDIN with DELIMITER E'\t' CSV HEADER;",filename)
    	_db_connection.commit()
    	filename.close()
    #	__del__(_db_connection,_hs_connection)
    except: # The table has a check/trigger so if data already exists the Postgres Database will throw an error, this will catch it.
        print "Sample Statistics data already exists for sample '%s'...\nEither this sample has already been inserted OR you need check that your sample name is correct\n TIP: Sample Names are captured from the filename of the forward/reverse files" % samplename
        # quit()  # TEMPORARILY DISABLE FOR TESTING
        _db_connection.rollback()
    __del__(_db_connection,_hs_connection)
    return sampleid,expid
def insertabundance(config,abundanceprof,flag):
    # See TODO above, this will eventually be called by STIRRUPS and RDP to inset their data     def insertstirdata(abundanceprof,readassign):
        # This will go away once the insertabundance and insertreadassign functions are completed.
    try:
        _db_connection,_db_cur,_hs_connection,_hs_cur = __init__(config)
    except:
        print ""
    print "Inserting Abundance Profile..."
    if flag:
        abundanceprof = open(abundanceprof)
        _db_cur.copy_from(abundanceprof,'abundance_profile',sep='\t',columns=('sample_id','taxonomy_level','taxonomy_name','num_reads','abundance','score','analysis_id','taxonomy_id','exp_id','status','miscellaneous'))
        #_db_cur.execute("COPY abundance_profile(sample_name,taxonomy_level,taxonomy_name,num_reads,abundance,avg,analysis_id,taxonomy_id,experiment_name,status,miscellaneous,sample_id) FROM '%s' with DELIMITER E'\t' CSV HEADER;" % abundanceprof)
        _db_connection.commit()
        abundanceprof.close()
    else:
        abundanceprof = open(abundanceprof)
        _db_cur.copy_from(abundanceprof,'abundance_profile',sep='\t',columns=('exp_id','sample_id','analysis_id','taxonomy_id','num_reads','abundance','score','status','miscellaneous','taxonomy_level','taxonomy_name'))
        #_db_cur.execute("COPY abundance_profile(experiment_name,sample_name,analysis_id,taxonomy_id,num_reads,abundance,avg,status,miscellaneous,taxonomy_level,taxonomy_name,sample_id) FROM '%s' with DELIMITER E'\t';" % abundanceprof)
        _db_connection.commit()
        abundanceprof.close()
    __del__(_db_connection,_hs_connection)
    
def insertreadassign(config,readassign):
    # See TODO above, this will eventually be called by STIRRUPS and RDP to inset their data
    try:
        _db_connection,_db_cur,_hs_connection,_hs_cur = __init__(config)
    except:
        print ""
    print "Inserting Read Assignments..."
    datadir = '/home/norrissw/m3db_data/' # THIS HAS TO BE HARDCODED FOR NOW
    _hs_cur.execute("LOAD DATA LOCAL INPATH '%s' INTO TABLE m3db.read_assignment" % (datadir + readassign))
    __del__(_db_connection,_hs_connection)
def insertreads(config,fastq):
	# Insert parsed sequence data after MeFit has run #
    _db_connection,_db_cur,_hs_connection,_hs_cur = __init__(config)
    datadir = '/home/norrissw/m3db_data/' # THIS HAS TO BE HARDCODED FOR NOW
    _hs_cur.execute("LOAD DATA LOCAL INPATH '%s' INTO TABLE m3db.reads" % (datadir + fastq))
    __del__(_db_connection,_hs_connection)
def __del__(pg,hs):
    pg.close()
    hs.close()
