import re,subprocess,sys,os,logging
from M3DB import parse as m3dbparse
from M3DB import db as db
from M3DB import pipeline as run
from M3DB import configparse as cfg
import Pyro4
#
_ConfigDefault = {
    "pg_server.dbms":            "PostgreSQL",
    "pg_server.database":            "m3db",
    "pg_server.user":            "postgres",
    "pg_server.password":        "password",
    "pg_server.host":            "myserver.mydomain.com",
    "pg_server.port":            "5432",
    "hive_server.dbms":          "Hive",
    "hive_server.database":      "m3db",
    "hive_server.user":          "hiveuser",
    "hive_server.password":      "password",
    "hive_server.host":          "myserver.mydomain.com",
    "hive_server.port":          "10000",
    "hive_server.auth":          "PLAIN",
    "general.datadir":           "/path/to/data/"
    }
config = cfg.LoadConfig('m3db.conf',_ConfigDefault)
datadir = config["general.datadir"]
dbp =  Pyro4.Proxy("PYRO:m3db.taxonomy@localhost:44517")
def createproject(args):
    # Create a new project #
    opts = vars(args)
    dbp.createproject(config,opts)
    print "Project has been created:",args.name
def createexp(args):
    db.createexp(config,args)
    print "Experiment has been created:",args.name        
def mefit(args):
    # Run the Merging and Filter pipeline and insert the data #
    project = args.project
    exp = args.exp
    samplename = args.samplename
    meep = float(args.meep)
    outname = samplename + '_out.txt'
    outpath = datadir + outname
    outfile = open(outpath,'w')
    outfile.close()
    fastq1 = samplename + '.ovlp.fastq' 
    fastq3 = samplename + '.nonovlp.fastq'
    sampleid,expid = None,None
    # Run the MeFit pipeline with the appropriate flags
    print "Running MeFit..."
    try:
        run.mefit(args)
    except (RuntimeError, TypeError, NameError) as e:
        print "Something went wrong with MeFit Pipeline\n Error: %s \n Exiting..." % e
        sys.exit(1)
    #Write to postgres database table "sample_statistics"
    print "Inserting Sample Statistics Data..."#,sampfile
    try:
        sampleid,expid = db.insertsampstat(config,(datadir + (samplename + '_stats.txt')),exp,samplename,args.forward)
    except:
        print "An error occured during database insertion... \n Exiting..."
        sys.exit(2)
    # Parse Read data and prepare it for insertion #
    print "Parsing Merged/Filtered sequence data..."
    try:
        if expid == None:
            expid = db.getexpid(config,exp)
        if sampleid == None:
            sampleid = db.getsampleid(config,samplename,expid)
        m3dbparse.reads((datadir + 'hq_out' + '/' + (fastq1)),(datadir + 'hq_out' + '/' + (fastq3)),outpath,samplename,sampleid,meep,expid,args.forward,args.reverse)
    except (RuntimeError, TypeError, NameError) as e:
        print "An error occured while parsing read files: %s" % e
        if os.path.isfile((datadir + 'hq_out' + '/' + (fastq3))):
            print "Continuing..."
        else:
            print "Critical failure, exiting..."
            sys.exit(3)
    #Write reads to hive database table "reads"
    print "Inserting Sequence Data..."
    try:
        db.insertreads(config,outname)
    except:
        print "An error has occured while inserting reads...\nExiting..."
        sys.exit(2)
    print "Completed Merge, Filter and upload of Sample"

def rdp(args):
    # Run the RDP pipeline and insert the data #
   # datadir = config["general.datadir"]
    rdp = True
    thresh = args.threshold
    exp = args.exp
    samplename = args.samplename
    analysisname = samplename + "_RDP"
    fastaname = datadir + samplename + '.fasta'
    rdppipe = '/home/parikhhi/bin/RDPpipeline.sh'
    taxdict = db.gettax(config,1)
    expid = db.getexpid(config,exp)
    sampleid = db.getsampleid(config,samplename,expid)
    print "Generating FASTA from database... for sample: %s" % samplename
    db.getfasta(config,sampleid,fastaname) # get a fasta file.
    # Run RDP against the newly created FASTA file #
    print "Executing RDP Analysis Pipeline...\nPlease be patient this may take a while while we examine your sample:", samplename
    rdpout = run.rdpclassifier(fastaname,thresh,datadir)
    print "Inserting RDP results into database..."
    analysisid = db.getaid(config,thresh)
    apout,raout = m3dbparse.rdpdata(expid,rdpout,analysisid,sampleid,samplename,taxdict,thresh,datadir)
    db.insertabundance(config,apout,rdp)
    db.insertreadassign(config,raout)
    print "Completed RDP Analysis!"
def stirrups(args):
    # Run the STIRRUPS Pipeline #
   # datadir = config["general.datadir"]
    rdp = False
    library = args.library
    exp = args.exp
    samplename = args.samplename
    fastaname = datadir + samplename + '.fasta'
    taxdict = db.gettax(config,2)
    expid = db.getexpid(config,exp)
    sampleid = db.getsampleid(config,samplename,expid)
    print "Generating FASTA from database... for sample: %s" % samplename
    db.getfasta(config,sampleid,fastaname)
    print "Running STIRRUPS Analysis..."
    run.stirrupsclassifier(library,fastaname,samplename)
    #subprocess.Popen([perlpath,stirrupspath,'-L',library,'-R',fastaname]).wait()
    analysisid = 3 #this is okay if using the standard 16s vaginal database.
    profilesummary = datadir + samplename + '_summary_97.txt'
    readassignment = datadir + samplename + '_assignment_97.txt'
    print "Parsing results and preparing for upload..."
    apout,raout = m3dbparse.stirdata(expid,profilesummary,readassignment,analysisid,sampleid,taxdict)
    print "Inserting STIRRUPS results..."
    db.insertabundance(config,apout,rdp)
    db.insertreadassign(config,raout)
    print "Completed STIRRUPS Analysis!"
