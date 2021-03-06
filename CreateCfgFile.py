#!/usr/bin/env python

from RunParams import DupCfgs,filelists,cfgfile
from RunParams import OnlyGauge,gfdir,gfdir_store,limename,paramdir,indexfilename
import os
import numpy as np
import math

def SortConfigs(setfilelist):
    if all([ia.isdigit() for ia in setfilelist]):
        # sortlist = [int(iset.split('.')[-1]) for iset in setfilelist]
        # doublist = sorted(zip(setfilelist,sortlist),key=lambda k : k[1])
        # return [ia for ia,ib in doublist]
        return map(str,np.sort(map(int,setfilelist)))
    else:
        return np.sort(setfilelist)

def CreateCfgList(ncfg,thisDupCfgs=DupCfgs,FromFile=False,Src=True):
    # filelist = os.listdir(rdsigfdir)
    if FromFile:
        with open(filelists+cfgfile,'r') as f:
            outfile = f.readlines()
        outfile = [x.strip() for x in outfile]
        totncfg = len(outfile)
        return outfile,totncfg
    if OnlyGauge:
        # setfilelist = map(str,range(1,NumGFCreate+1))
        # setfilelist = [n.zfill(5) for n in setfilelist]
        setfilelist = ['']
    else:
        print 'Reading gauge fields from:'
        print gfdir
        filelist = os.listdir(gfdir)
        store_filelist = os.listdir(gfdir_store)
        store_filelist = [ifile.replace(gfdir_store,gfdir) for ifile in store_filelist]
        comp_fl,comp_fls = set(filelist),set(store_filelist)
        print
        print 'Searching for file regex:'
        print limename+'*'
        if not comp_fl.issubset(comp_fls):
            print 'Warning, these files are in scratch, but not in storage:'
            for ifile in comp_fl.difference(comp_fls):
                print ifile
            filelist = list(comp_fl.union(comp_fls))
        elif not comp_fls.issubset(comp_fl):
            print 'Scrach space is missing these configs:'
            for ifile in comp_fls.difference(comp_fl):
                print ifile
            filelist = list(comp_fl.union(comp_fls))
        setfilelist = []
        for icf,ifile in enumerate(filelist):
            if not os.path.isfile(ifile):
                ifile = ifile.replace(gfdir,gfdir_store)
            if limename in ifile:
                setfilelist.append(ifile.replace(limename,''))
            else:
                print 'limename NF:',ifile
            # if '.lime' in ifile:
                # setfilelist.append('.'+'.'.join(ifile.split('.')[1:3]))
            # setfilelist.append(str(int(re.sub(r'.*lime','',ifile))))
        setfilelist = SortConfigs(setfilelist)
        print 'configurations found:'
        for ifile in setfilelist: print ifile
        print
        totncfg = len(setfilelist)
        # setfilelist = np.roll(setfilelist,machineroll*(totncfg/ncfg)/(totroll))
        # if ncfg != 0 and ncfg <= len(setfilelist):
        #     setfilelist = setfilelist[:ncfg]
    if Src:
        outfile = []
        for iDup in range(1,int(thisDupCfgs)+1):
            outfile += [iset+'_xsrc'+str(iDup)+'\n' for iset in setfilelist]
    else:
        outfile = [iset+'\n' for iset in setfilelist]
    with open(filelists+cfgfile,'w') as f:
        f.writelines(outfile)
    # np.array([iset+'\n' for iset in setfilelist]).tofile(filelists+cfgfile)
    return outfile,totncfg



def GetCfgIndicies(totncfg,ncfg,nsrc,squashcfg):
    outindicies = []
    for isrc in range(nsrc):
        outindicies += map(int,map(round,np.linspace(start=squashcfg+(isrc*totncfg), stop=(isrc+1)*totncfg, num=ncfg+1).tolist())[:-1])
    with open(paramdir+indexfilename,'w') as f:
        for iout in outindicies:
            f.write(str(iout)+'\n')
    return outindicies

def GetIcfgTOFcfg(nproc,nconf):
    confbreak = int(math.ceil(nconf/float(nproc)))
    # rem = nconf%nproc
    if confbreak == 0:
        return [[1,1]]
    outarray = []
    startlist = range(1,nconf+1,confbreak)
    endlist = range(confbreak,nconf+1+confbreak,confbreak)
    # startlist,endlist = extendstartend(startlist,endlist,rem)
    for istart,iend in zip(startlist,endlist):
        outarray.append([istart,iend])
    # outarray[-1][-1] -= 1
    return outarray
