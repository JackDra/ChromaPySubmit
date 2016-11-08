#!/usr/bin/env python

from RunParams import *
import os

def SortConfigs(setfilelist):
    sortlist = [int(iset.split('.')[-1]) for iset in setfilelist]
    doublist = sorted(zip(setfilelist,sortlist),key=lambda k : k[1])
    return [ia for ia,ib in doublist]

def CreateCfgList():
    # filelist = os.listdir(rdsigfdir)
    filelist = os.listdir(gfdir)
    setfilelist = []
    for ifile in filelist:
        if '.lime' in ifile:
            setfilelist.append('.'+'.'.join(ifile.split('.')[1:3])+'\n')
    setfilelist = SortConfigs(setfilelist)
    thisfile = open(filelists+cfgfile,'w')
    thisfile.writelines(setfilelist)
    thisfile.close()
    return setfilelist
    

def GetIcfgTOFcfg(nproc,nconf):
    confbreak = nconf/nproc
    if confbreak == 0:
        return [1,1]
    outarray = []    
    for istart,iend in zip(range(1,nconf+1,confbreak),range(confbreak,nconf+1+confbreak,confbreak)):
        outarray.append((istart,iend))
    return outarray
