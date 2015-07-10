#!/usr/bin/env
# Pipeline Recreation for M3DBcli
import subprocess, os, sys
def mefit(args):
  # This will run mefit #
    exp = args.exp
    fline = args.forward
    rline = args.reverse
    overlap = args.overlap
    meep = str(args.meep) #strings only when using subprocess
    patch_length = str(args.patch_length)
    samplename = args.samplename
    merger = 'MeFit_m3db'
    if overlap:
        subprocess.Popen([merger,'-r1',fline,'-r2',rline,'-meep',meep,'-a','-n',patch_length,'--samplename',samplename]).wait()
    else:
        subprocess.Popen([merger,'-r1',fline,'-r2',rline,'-meep',meep,'--samplename',samplename]).wait()
def stirrupsclassifier(library,fastaname,samplename):
  # This will run stirrups #
    perlpath = 'perl'
    stirrupspath ='/gpfs_fs/bccl/stirrups/stirrups_pipeline_v5.pl'
    subprocess.Popen([perlpath,stirrupspath,'-L',library,'-R',fastaname,'-ID',samplename]).wait()
def rdpclassifier(fastafile,cutoff,datadir):
  # This will run RDP #
    classjar = '/usr/global/blp/rdp_classifier_2.9/dist/classifier.jar'
    java = 'java'
    cutoff = str(cutoff)
    fastaname = os.path.basename(fastafile).split(".")[-2]
    RDPOut= datadir + '%s_rdp.out' % fastaname
  #rdp command
    subprocess.Popen([java,'-Xmx4g','-jar',classjar,'classify','-c',cutoff,'-o',RDPOut,fastafile]).wait()
    return RDPOut #  parseRDP -i $RDPOut -s $CUTOFF -id $ID -ra $RAFILE -ps $PSFILE
