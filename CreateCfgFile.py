#!/usr/bin/env python

from RunParams import *
import os,re
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

def CreateCfgList(thisDubCfgs=DubCfgs,ncfg=0):
    # filelist = os.listdir(rdsigfdir)
    if OnlyGauge:
        # setfilelist = map(str,range(1,NumGFCreate+1))
        # setfilelist = [n.zfill(5) for n in setfilelist]
        setfilelist = ['']
    else:
        filelist = os.listdir(gfdir)
        # print filelist
        setfilelist = []
        for ifile in filelist:
            if limename in ifile:
                setfilelist.append(ifile.replace(limename,''))
            # if '.lime' in ifile:
                # setfilelist.append('.'+'.'.join(ifile.split('.')[1:3]))
            # setfilelist.append(str(int(re.sub(r'.*lime','',ifile))))
        setfilelist = SortConfigs(setfilelist)
        if ncfg != 0 and ncfg <= len(setfilelist):
            setfilelist = setfilelist[:ncfg]
    outfile = []
    for iDub in range(1,thisDupCfgs+1):
        outfile += [iset+'_xsrc'+str(iDub)+'\n' for iset in setfilelist]
    with open(filelists+cfgfile,'w') as f:
        f.writelines(outfile)
    # np.array([iset+'\n' for iset in setfilelist]).tofile(filelists+cfgfile)
    return outfile


        
def GetIcfgTOFcfg(nproc,nconf):
    confbreak = int(math.ceil(nconf/float(nproc)))
    rem = nconf%nproc
    if confbreak == 0:
        return [[1,1]]
    outarray = []    
    startlist = range(1,nconf+1,confbreak)
    endlist = range(confbreak,nconf+1+confbreak,confbreak)
    # startlist,endlist = extendstartend(startlist,endlist,rem)
    for istart,iend in zip(startlist,endlist):
        outarray.append([istart,iend])
    outarray[-1][-1] -= 1
    return outarray

