#!/usr/bin/env python
#
# Parsing Functions for M3DB api.
# TODO: Move parsing functions from API to this file.
# May be able to just have one parsing function that handles both RDP and STIRRUPS data
import re,sys,os
from collections import defaultdict

def reads(overlap,nonoverlap,outfile,samplename,sid,meep,expid,forwardfile,reversefile):
    # add a parse for forward and reverse files
    nucleotides={'dna':re.compile('^[acgtn]*$',re.I)}
    dic = defaultdict(defaultdict)
    overlap = open(overlap)
    nonoverlap = open(nonoverlap)
    forwardfile = open(forwardfile)
    reversefile = open(reversefile)
    outfile = open((outfile),'a')
    fasta = open((samplename + '.fasta'),'a')
    lines = overlap.readlines() + nonoverlap.readlines()
    raw_lines = forwardfile.readlines() + reversefile.readlines()
    linenum = 1
    for line in lines:
        if line.startswith('@') and linenum%4 != 0:
            key = re.split(' ', line.strip())[0]
            dic[key]['desc'] = re.split(' ',line.strip())[1]
            header = re.sub(' ',':',line.strip())
            header = re.split(':',header)
          #  dic[key]['read_id'] = header[14]
          #  dic[key]['plate_well'] = header[13] #this may not be necessary
            dic[key]['length'] = int(re.sub('len=','',header[-3]))
            dic[key]['MEE'] = float(re.sub('EE=','',header[-1]))
            dic[key]['avg_quality'] = int(re.sub('avgQ=','',header[-2]))
            if int(header[-4]) == 0:
                dic[key]['overlap_flag'] = "N"
            elif int(header[-4]) == 1:
                dic[key]['overlap_flag'] = "Y"
        if (linenum%4 == 0):
            dic[key]['quality'] = str(line.strip())
        elif re.search(nucleotides['dna'],line):
            dic[key]['sequence'] = line.strip()
        linenum +=1
    rawlinenum = 1
    for raw_line in raw_lines:
        if raw_line.startswith('@') and rawlinenum%4 != 0:
            key = re.split(' ', raw_line.strip())[0]
            desc = re.split(' ',raw_line.strip())[1]
            pos = desc.split(':')[0]
            quality = 'quality' + pos
            sequence = 'sequence' + pos
            if key not in dic:
                print "Key Not Found...Did something go wrong?"
                dic[key]['desc'] = desc
        if (rawlinenum%4 == 0):
            dic[key][quality] = str(raw_line.strip())
        elif re.search(nucleotides['dna'],raw_line):
            dic[key][sequence] = str(raw_line.strip())
        rawlinenum += 1
    for key in dic:
        if dic[key]['MEE'] >= (meep * dic[key]['length'] / 100.0):
            hq_flag = "Y"
        else:
            hq_flag = "N"
        outfile.write('%s\t%s\t%s\t%f\t%i\t%i\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\n' % (expid,sid,key,dic[key]['MEE'],dic[key]['avg_quality'],dic[key]['length'],dic[key]['overlap_flag'] ,dic[key]['desc'],hq_flag,dic[key]['sequence'],dic[key]['quality'],dic[key]['sequence1'],dic[key]['quality1'],dic[key]['sequence2'],dic[key]['quality2']))
        fasta.write('>%s\n%s\n' % (key,dic[key]['sequence']))
    fasta.close()
    outfile.close()

def rdpdata(expid,rdpout,aid,sampleid,samplename,taxdict,thresh,datadir):
    print "Parsing RDP data and preparing for database insertion"
    read_id = ""
    PS_Dict = {}
    level, name, score = ("", "", 0.0)
    ps_count, ps_tot_score, ps_perc_read, ps_avg_score = (0, 0.0, 0.0, 0.0)
    tot_read = 0
    taxa_level = {"rootrank":"1", "domain":"2", "phylum":"3", "class":"4", "subclass":"5", "order":"6", "suborder":"7", "family":"8", "genus":"9"}
    ra_outfile = open((datadir + samplename + '_ra.txt'), 'w')
    status = "AT" #Due to the nature of RDP all results are already "AT"
    misc = "RDP Testing, change me in parse"
# Read the input file, store data in dictionary

    for line in open(rdpout).readlines():
        line = line.strip()
        line = re.sub("\"", "", line)
        # convert line string into a list
        line_lst = line.split("\t")

        # get read info
        read_id = line_lst[0]

        tot_read += 1       # counter for total readsra_outfile = open((sampleid + '_ra.txt'), 'w')
        # iterate within the list to get Taxa-Level, Taxa-Name and Taxa-Score
        for i in range(3, len(line_lst), 3):
            level = line_lst[i]
            level_ct = taxa_level[level]
            name = line_lst[i-1]
            #name = re.sub(r'\s+', '_', name)
            score = float(line_lst[i+1])        

            # compare score to threshold cutoff and proceed
            if score >= thresh:
                ra_outfile.write("%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\n" % (expid,sampleid,read_id,int(taxdict[name]),name,level,score,aid,status,misc))

                # store data for profile summary dictionary
                PS_Dict.setdefault(level,{}).setdefault(level_ct,{})
                if name in PS_Dict.get(level,{}).get(level_ct,{}):
                    new_ps_count = PS_Dict[level][level_ct][name]['count'] + 1
                    PS_Dict[level][level_ct][name]['count'] = new_ps_count
                    new_ps_tot_score = PS_Dict[level][level_ct][name]['tot_score'] + score
                    PS_Dict[level][level_ct][name]['tot_score'] = new_ps_tot_score
                else:
                    PS_Dict.setdefault(level,{}).setdefault(level_ct,{}).setdefault(name,{})
                    ps_count = 1
                    PS_Dict[level][level_ct][name]['count'] = ps_count
                    ps_tot_score = score
                    PS_Dict[level][level_ct][name]['tot_score'] = ps_tot_score
            
            else:
                break
    ps_outfile = open((datadir + samplename + '_ps.txt'), 'w')
    # write ProfileSummary Output File
    for (level, level_cts) in sorted(PS_Dict.iteritems(), key=lambda x:x[1]):
        for(level_ct, names) in level_cts.iteritems():
            for (name, attrs) in names.iteritems():
                ps_perc_read = ( PS_Dict[level][level_ct][name]['count'] / float(tot_read) ) * 100.00
                ps_avg_score = PS_Dict[level][level_ct][name]['tot_score'] / PS_Dict[level][level_ct][name]['count']
                ps_printlst = [str(sampleid), str(level), str(name), str(PS_Dict[level][level_ct][name]['count']), str("%.2f" % ps_perc_read), str("%.2f" % ps_avg_score),str(aid),str(taxdict[name]),str(expid),status,misc] 
                ps_printstr = "\t".join(ps_printlst)
                print >> ps_outfile, ps_printstr
    return (datadir + samplename + '_ps.txt'),(samplename + '_ra.txt')

def stirdata(expid,abundanceprof,readassign,aid,sampleid,taxdict):
   # profile_id | experiment_name | sample_name | analysis_id | taxonomy_id | num_reads | abundance | avg  | status | miscellaneous | taxonomy_level |  taxonomy_name | sample_id
    taxlevel = "species"
    misc = "STIRRUPS TESTING (change in parse)"
    with open(abundanceprof) as ap:
        #samplename = re.split("\/",abundanceprof)[-1].split("_")[0]
        apoutname = abundanceprof + '_pg.txt'
        apout = apoutname
        apoutfile = open(apout,'w')
        keepgoing = True
        while keepgoing:
            try:
                line = (ap.next().strip()).split("|")
            except:
                break
            samplename = line[0]
            taxname = line[1]
            threshold = line[2]
            numhits = line[3]
            percenthit = line[4]
            matchpercent = line[5]
            try:
                taxid = int(taxdict[taxname])
            except:
                taxid = 0
            apoutfile.write("%i\t%i\t%i\t%i\t%s\t%s\t%s\t%s\t%s\t%s\t%s\n" % (expid,sampleid,aid,taxid,numhits,percenthit,matchpercent,threshold,misc,'species',taxname))#,sampleid)) Sampleid not currently in abundance_profile table
    with open(readassign) as ra:
        raoutname = readassign + '_hs.txt'
        raout = raoutname
        raoutfile = open(raout,'w')
        keepgoing = True
        while keepgoing:
            try:
                line = (ra.next().strip()).split("|")
            except:
                break
            samplename = line[0]
            readid = line[1]
            taxname = line[2]
            status = line[3]
            score = line[4]
            try:
                taxid = taxdict[taxname]
            except:
                taxid = 0
            raoutfile.write("%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\n" % (expid,sampleid,readid,taxid,taxname,taxlevel,score,aid,status,misc))
    return apoutname,(raoutname.split("/")[-1])
