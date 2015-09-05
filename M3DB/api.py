import re,subprocess,sys,os,logging
from M3DB import parse as m3dbparse
from M3DB import pipeline as run
import Pyro4

datadir = "/gpfs_fs/bccl/M3DB/data/"
#dbp =  Pyro4.Proxy("PYRO:Pyro.NameServer@128.172.190.159:9090")
dbp = Pyro4.Proxy("PYRONAME:m3db.cli@128.172.190.159:9090")
def createproject(args):
    # Create a new project #
    opts = vars(args)
    dbp.createproject(opts)
    print "Project has been created:",args.name
def createexp(args):
    opts = vars(args)
    try:
        dbp.createexp(opts)
        print "Experiment has been created:",args.name        
    except Exception as error:
        print "Something went wrong during experiment creation:\n",error
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
    except Exception as error:
        print "Something went wrong with MeFit Pipeline\n Error: %s \n Exiting..." % error
        sys.exit(1)
    #Write to postgres database table "sample_statistics"
    print "Inserting Sample Statistics Data..."#,sampfile
    sampfile = open((datadir + (samplename + '_stats.txt')))
    try:
        sampleid,expid = dbp.insertsampstat((datadir + (samplename + '_stats.txt')),exp,samplename,args.forward)
    except Exception as error:
        print "An error occured during database insertion... \n Exiting...",error
        sys.exit(2)
    # Parse Read data and prepare it for insertion #
    print "Parsing Merged/Filtered sequence data..."
    try:
        if expid == None:
            expid = dbp.getexpid(exp)
        if sampleid == None:
            sampleid = db.getsampleid(samplename,expid)
        m3dbparse.reads((datadir + 'hq_out' + '/' + (fastq1)),(datadir + 'hq_out' + '/' + (fastq3)),outpath,samplename,sampleid,meep,expid,args.forward,args.reverse)
    except Exception as error:
        print "An error occured while parsing read files: %s" % error
        if os.path.isfile((datadir + 'hq_out' + '/' + (fastq3))):
            print "Continuing..."
        else:
            print "Critical failure, exiting..."
            sys.exit(3)
    #Write reads to hive database table "reads"
    print "Inserting Sequence Data..."
    try:
        dbp.insertreads(outname)
    except Exception as error:
        print "An error has occured while inserting reads...\nExiting...",error
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
    taxdict = dbp.gettax(1)
    expid = dbp.getexpid(exp)
    sampleid = dbp.getsampleid(samplename,expid)
    print "Generating FASTA from database... for sample: %s" % samplename
    dbp.getfasta(sampleid,fastaname) # get a fasta file.
    # Run RDP against the newly created FASTA file #
    print "Executing RDP Analysis Pipeline...\nPlease be patient this may take a while while we examine your sample:", samplename
    rdpout = run.rdpclassifier(fastaname,thresh,datadir)
    print "Inserting RDP results into database..."
    analysisid = dbp.getaid(thresh)
    apout,raout = m3dbparse.rdpdata(expid,rdpout,analysisid,sampleid,samplename,taxdict,thresh,datadir)
    dbp.insertabundance(apout,rdp)
    dbp.insertreadassign(raout)
    print "Completed RDP Analysis!"
def stirrups(args):
    # Run the STIRRUPS Pipeline #
   # datadir = config["general.datadir"]
    rdp = False
    library = args.library
    exp = args.exp
    samplename = args.samplename
    fastaname = datadir + samplename + '.fasta'
    taxdict = dbp.gettax(2)
    expid = dbp.getexpid(exp)
    sampleid = dbp.getsampleid(samplename,expid)
    print "Generating FASTA from database... for sample: %s" % samplename
    dbp.getfasta(sampleid,fastaname)
    print "Running STIRRUPS Analysis..."
    run.stirrupsclassifier(library,fastaname,samplename)
    #subprocess.Popen([perlpath,stirrupspath,'-L',library,'-R',fastaname]).wait()
    analysisid = 3 #this is okay if using the standard 16s vaginal database.
    profilesummary = datadir + samplename + '_summary_97.txt'
    readassignment = datadir + samplename + '_assignment_97.txt'
    print "Parsing results and preparing for upload..."
    apout,raout = m3dbparse.stirdata(expid,profilesummary,readassignment,analysisid,sampleid,taxdict)
    print "Inserting STIRRUPS results..."
    dbp.insertabundance(apout,rdp)
    dbp.insertreadassign(raout)
    print "Completed STIRRUPS Analysis!"
