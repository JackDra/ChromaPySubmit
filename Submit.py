#!/usr/bin/env python

from RunParams import *
from CreateCfgFile import *
from CreateChromaFiles import *
from GetAndCheckData import *
from ReSubmit import RunNext
import sys
import subprocess
import numpy as np

njobs = -1
forcecfg = False
ncfg = False
nsrc = DupCfgs
FromFile = False
startcfg = 0
nppick = False
OnlyThree = False
for iin in sys.argv[1:]:
    if '-np=' in iin:
        njobs = int(iin.replace('-np=',''))
    elif '-startcfg=' in iin:
        startcfg = int(iin.replace('-startcfg=',''))
    elif '-ncfg=' in iin:
        ncfg = int(iin.replace('-ncfg=',''))
    elif '-nsrc=' in iin:
        nsrc = int(iin.replace('-nsrc=',''))
    elif '-fromfile' in iin:
        FromFile = True
    elif '-nppick' in iin:
        nppick = map(int,iin.replace('-nppick=','').split(','))
    elif '-onlythree' in iin:
        OnlyThree = True
        
        
if njobs == -1:
    raise IOError('please give number of processors as -np=## ')
if nppick == False: nppick = range(1,njobs+1)
    
print 'Number of jobs = ' , njobs

# if sys.argv[2] == 'a':
#     thisgfosnum = range(1,10)
# else:
#     thisgfosnum = map(int,sys.argv[2:])
# nproc = int(sys.argv[1])


# np.array([ithisc+'\n' for ithisc in thiscfglist]).tofile(cfgfile)

thiscfglist,totncfg = CreateCfgList(njobs,FromFile=FromFile)

if ncfg == False:
    ncfg = totncfg
cfgindicies = GetCfgIndicies(totncfg,ncfg,nsrc,startcfg)



# if forcecfg == False:
cfgintervals = GetIcfgTOFcfg(njobs,ncfg*nsrc )
for iin,(icfg,fcfg) in enumerate(cfgintervals):
    if iin+1 in nppick:
        thisnproc = nproc
        if iin >= len(cfgintervals)/2 and halfishalf: thisnproc=nproc/2
        print 'Submitting icfg='+str(icfg)+' fcfg='+str(fcfg)    
        RunNext(icfg,fcfg,Start=True,cfgindicies=cfgindicies,thisnproc=thisnproc,othree=OnlyThree)
# else:
#     RunNext(forcecfg[0],forcecfg[1],Start=True,cfgindicies=cfgindicies)
        
