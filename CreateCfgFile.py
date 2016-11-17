#!/usr/bin/env python

from RunParams import *
import os,re
import numpy as np

def SortConfigs(setfilelist):
    if all([ia.isdigit() for ia in setfilelist]):
        # sortlist = [int(iset.split('.')[-1]) for iset in setfilelist]
        # doublist = sorted(zip(setfilelist,sortlist),key=lambda k : k[1])
        # return [ia for ia,ib in doublist]
        return map(str,np.sort(map(int,setfilelist)))
    else:
        return np.sort(setfilelist)

def CreateCfgList():
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
            setfilelist.append(ifile.replace(limename,''))
            # if '.lime' in ifile:
                # setfilelist.append('.'+'.'.join(ifile.split('.')[1:3]))
            # setfilelist.append(str(int(re.sub(r'.*lime','',ifile))))
        setfilelist = SortConfigs(setfilelist)
    with open(filelists+cfgfile,'w') as f:
        f.writelines([iset+'\n' for iset in setfilelist.tolist()*DupCfgs])
    # np.array([iset+'\n' for iset in setfilelist]).tofile(filelists+cfgfile)
    return setfilelist
    

def GetIcfgTOFcfg(nproc,nconf):
    confbreak = nconf/nproc
    if confbreak == 0:
        return [(1,1)]
    outarray = []    
    for istart,iend in zip(range(1,nconf+1,confbreak),range(confbreak,nconf+1+confbreak,confbreak)):
        outarray.append((istart,iend))
    return outarray
