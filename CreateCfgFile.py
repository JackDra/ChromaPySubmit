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

def CreateCfgList(ncfg,forcecfg,thisDupCfgs=DupCfgs):
    # filelist = os.listdir(rdsigfdir)
    if OnlyGauge:
        # setfilelist = map(str,range(1,NumGFCreate+1))
        # setfilelist = [n.zfill(5) for n in setfilelist]
        setfilelist = ['']
    else:
        filelist = os.listdir(gfdir)
        
        # print filelist
        setfilelist = []
        if forcecfg == False:
            forcecfg = 1,len(filelist)
        else:
            if forcecfg[-1] == -1: forcecfg[-1] = len(filelist)
        for icf,ifile in enumerate(filelist):
            if (limename in ifile) and (icf+1 >= forcecfg[0]) and (icf+1 <= forcecfg[0]):
                setfilelist.append(ifile.replace(limename,''))
            # if '.lime' in ifile:
                # setfilelist.append('.'+'.'.join(ifile.split('.')[1:3]))
            # setfilelist.append(str(int(re.sub(r'.*lime','',ifile))))
        setfilelist = SortConfigs(setfilelist)
        totncfg = len(setfilelist)
        # setfilelist = np.roll(setfilelist,machineroll*(totncfg/ncfg)/(totroll))
        # if ncfg != 0 and ncfg <= len(setfilelist):
        #     setfilelist = setfilelist[:ncfg]
    outfile = []
    for iDup in range(1,int(thisDupCfgs)+1):
        outfile += [iset+'_xsrc'+str(iDup)+'\n' for iset in setfilelist]
    with open(filelists+cfgfile,'w') as f:
        f.writelines(outfile)
    # np.array([iset+'\n' for iset in setfilelist]).tofile(filelists+cfgfile)
    return outfile,totncfg



def GetCfgIndicies(totncfg,ncfg,nsrc):
    outindicies = []
    for isrc in range(nsrc):
        outindicies += map(int,map(round,np.linspace(start=isrc*totncfg, stop=(isrc+1)*totncfg, num=ncfg+1).tolist())[:-1])
    with open(paramdir+indexfilename,'w') as f:
        for iout in outindicies:
            f.write(str(iout)+'\n')
    return outindicies

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
    # outarray[-1][-1] -= 1
    return outarray

