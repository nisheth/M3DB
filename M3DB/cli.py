#!/usr/bin/env python
# m3dbcli.py
# Written by: Shaun Norris, VCU Microbiology & Immunology
# For VMC and MOMS-PI
#import m3db.py
from M3DB import api as m3dbapi
import re,sys,argparse,textwrap
# TODO:
# Add an option to use qsub to:
# RDP, STIRRUPS and maybe mefit
# Consider adding generate fasta or fastq in order to restore read files.
# Need to accept a configuration file.
# This needs to find and accept a YAML configuration file.

HELP = { 
"createproject" : "Create a new project",
"createexp" : "Create a new experiment",
"uploadsample" : "Merge, Filter and Upload a new sample",
"rdp" : "Run RDP Analysis on a sample",
"stirrups" : "Run stirrups Analysis on a sample",
"version" : "Alpha 0.3a Released for internal testing"
}

HELP_SUB = { 
"cproj" : "Specify each argument in order to create a new project.\n E.G. m3dbcli createproject --name PROJECTNAME --pi PIFIRST PILAST --email you@you.com --description PROJECTDESC --user USERNAME",
"email" : "E-mail format: you@yourdomain.com",
"pi" : "The name of the PI for the experiment. Format: Lastname,Firstname \n E.G. Smith,John",
"name" : "The name you wish to give the project/experiment.",
"pdesc" : "The description of the experiment you're creating",
"user" : "Your username. \nTypically this is your VCU eid.",

"cexp" : "Specify each argument to create a new experiment. \n E.G. m3dbcli createexp --name EXPERIMENTNAME --date MM-DD-YYYY --plat ILLUMINA/454 --project PROJECTNAME --region GENEREGION --user USERNAME",
"date" : "Input date in the 2 digit day/month and 4 digit year format (MM-DD-YYYY). \n E.G. 01-30-2015",
"proj" : "The name of the project you previously created.\n E.G. MyProject",
"reg" : "The gene region for which you are examining.",
"plat" : "Specify the platform where the sequence files were generated. \n E.G. 454 or Illumina",

"usamp" : "Upload Samplefiles",
"pexp" : "The name of the experiment you previously created.\n E.G. MyExperiment",
"fastq" : "The name of the forward and reverse fastq files you which to be merged, filtered and analyzed",
"meep" : "Specify the meep value to be used.\n Default: 1.0",
"over" : "Specify if you wish to use overlap",
"patch" : "Specify the patch length you wish you use. \n Default: 10",

"rdp" : "RDP Classifier is a naive Bayesian classifier that can rapidly and accurately provides taxonomic assignments from domain to genus, with confidence estimates for each assignment. More information can be found at http://rdp.cme.msu.edu/",
"trsh" : "Specify the threshold value that you would like to use a cutoff. Default: 0.8",
"infl" : "Specify the sample name that you would like to analyze",

"stir" : "The STIRRUPS script takes a collection of reference fasta files and read fasta files and runs a USEARCH alignment. Using the resulting output from USEARCH it formats the output and calculates statistics based on percentage make up of a strain and species for a particular sample id.",
"lib" : "Specify the fasta file you would like to use as a reference database. Default: vaginal_16S_V1V3_refdb1-1",
"faa" : "", # Not Implemented Currently - Will be used to generate fasta or fastq files on the fly.
"faq" : "" # Not Implemented Currently - Will be used to generate fastq or fasta files on the fly.
}

parser = argparse.ArgumentParser(prog='m3dbcli',formatter_class=argparse.RawDescriptionHelpFormatter,description=textwrap.dedent('''
   
   M3DB - developed by Shaun Norris for VCU Human Microbiome Project (MOMS-PI/VAHMP)
   M3DB is a new command line tool for analysis and storage of microbiome data.
   -------------------------------------------------------------------

  For detailed information about a command type m3dbcli.py <command> -h
  Ex: m3dbcli.py createexp -h (will provide additional information about the createxp command)

   -------------------------------------------------------------------

  Once an operation completes successfully the results are viewable through the M3DB webpage.
  http://bccldev.csbc.vcu.edu:9090/

   -------------------------------------------------------------------
	'''))
subparsers = parser.add_subparsers(dest='mode')
cproj_parser = subparsers.add_parser("createproject", help=HELP['createproject'])
cproj_parser.add_argument("createproject",help=HELP_SUB['cproj'],nargs='*')
cproj_parser.add_argument("--name",help=HELP_SUB['name'])
cproj_parser.add_argument("--pi",help=HELP_SUB['pi'])
cproj_parser.add_argument("--email",help=HELP_SUB['email'])
cproj_parser.add_argument("--desc",help=HELP_SUB['pdesc'])
cproj_parser.add_argument("--user",help=HELP_SUB['user'])
cproj_parser.set_defaults(which="createproject")
# cproj_parser.set_defaults(run=m3dbapi.createproject())

createexp_parser = subparsers.add_parser("createexp",help=HELP['createexp'])
createexp_parser.add_argument("createexp",help=HELP_SUB['cexp'],nargs='*')
createexp_parser.add_argument("--name",help=HELP_SUB['name'])
createexp_parser.add_argument("--date",help=HELP_SUB['date'])
createexp_parser.add_argument("--plat",help=HELP_SUB['plat'])
createexp_parser.add_argument("--project",help=HELP_SUB['proj'])
createexp_parser.add_argument("--region",help=HELP_SUB['reg'])
createexp_parser.add_argument("--user",help=HELP_SUB['user'])
createexp_parser.set_defaults(which="createxp")
# createexp_parser.set_defaults(run=m3dbapi.createexp)

upsamp_parser = subparsers.add_parser("uploadsample",help=HELP['uploadsample'])
upsamp_parser.add_argument("uploadsample",help=HELP_SUB['usamp'],nargs='*')
upsamp_parser.add_argument("--project",help=HELP_SUB['proj'])
upsamp_parser.add_argument("--exp",help=HELP_SUB['pexp'])
upsamp_parser.add_argument("--samplename",help=HELP_SUB['infl'],default=None)
upsamp_parser.add_argument("--forward",help=HELP_SUB['fastq'])
upsamp_parser.add_argument("--reverse",help=HELP_SUB['fastq'])
upsamp_parser.add_argument("--meep",help=HELP_SUB['meep'],default=1.0,type=float)
upsamp_parser.add_argument("--overlap",action='store_true',default=False,help=HELP_SUB['over'])
upsamp_parser.add_argument("--patch_length",help=HELP_SUB['patch'],default=10,type=int)
upsamp_parser.set_defaults(which="uploadsample")
# upsamp_parser.set_defaults(run=m3dbapi.insertfile)

rdp_parser = subparsers.add_parser("rdp",help=HELP['rdp'])
rdp_parser.add_argument("rdp",help=HELP_SUB['rdp'],nargs='*')
rdp_parser.add_argument("--threshold",help=HELP_SUB['trsh'],default=0.8,type=float)
rdp_parser.add_argument("--exp",help=HELP_SUB['pexp'])
rdp_parser.add_argument("--samplename",help=HELP_SUB['infl'])
rdp_parser.set_defaults(which="rdp")
# rdp_parser.set_defaults(run=m3dbapi.runrdp)

stir_parser = subparsers.add_parser("stirrups",help=HELP['stirrups'])
stir_parser.add_argument("stirrups",help=HELP_SUB['stir'],nargs='*')
stir_parser.add_argument("--library",help=HELP_SUB['lib'],default='/gpfs_fs/bccl/stirrups/stirrups_ref_library.fa')
stir_parser.add_argument("--exp",help=HELP_SUB['pexp'])
stir_parser.add_argument("--samplename",help=HELP_SUB['infl'])
# stir_parser.add_argument("--fasta",help=HELP_SUB['faa'])
stir_parser.set_defaults(which="stirrups")
# stir_parser.set_defaults(run=m3dbapi.runstir)
if len(sys.argv) < 2:
  parser.print_help()
  sys.exit(1)
args = parser.parse_args()

if args.mode == 'createproject':
  if len(sys.argv) < 10:
    print "Insufficient arguments provided..."
    cproj_parser.print_help()
    sys.exit(1)
  else:
    print "Creating Project..."
    m3dbapi.createproject(args)
if args.mode == 'createexp':
  if len(sys.argv) < 13:
    print "Insufficient arguments provided..."
    createexp_parser.print_help()
    sys.exit(1)
  else:
    print "Creating Experiment..."
    m3dbapi.createexp(args)
if args.mode == 'uploadsample':
  if len(sys.argv) < 10:
    print "Insufficient arguments provided..."
    upsamp_parser.print_help()
    sys.exit(1)
  else:
    print "Uploading Samples..."
    m3dbapi.mefit(args)
if args.mode == 'rdp':
  if len(sys.argv) < 5:
    print "Insufficient arguments provided..."
    rdp_parser.print_help()
    sys.exit(1)
  else:
    print "Running RDP Analysis..."
    m3dbapi.rdp(args)
if args.mode == 'stirrups':
  if len(sys.argv) < 5:
    print "Insufficient arguments provided..."
    stir_parser.print_help()
    sys.exit(1)
  else:
    print "Running STIRRUPS Analysis..."
    m3dbapi.stirrups(args)
