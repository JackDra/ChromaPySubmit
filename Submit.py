#!/usr/bin/env python

from RunParams import *
from CreateCfgFile import *
from CreateChromaFiles import *
from GetAndCheckData import *
from ReSubmit import RunNext
import sys
import subprocess
import numpy as np

nproc = -1
forcecfg = False
ncfg = False
nsrc = DupCfgs
for iin in sys.argv[1:]:
    if '-np=' in iin:
        nproc = int(iin.replace('-np=',''))
    elif '-forcecfg=' in iin:
        forcecfg = map(int,iin.replace('-forcecfg=','').split(','))
    elif '-ncfg=' in iin:
        ncfg = int(iin.replace('-ncfg=',''))
    elif '-nsrc=' in iin:
        nsrc = int(iin.replace('-nsrc=',''))
        
        
if nproc == -1:
    raise IOError('please give number of processors as -np=## ')
    
print 'Number of processors = ' , nproc

# if sys.argv[2] == 'a':
#     thisgfosnum = range(1,10)
# else:
#     thisgfosnum = map(int,sys.argv[2:])
# nproc = int(sys.argv[1])


thiscfglist,totncfg = CreateCfgList()
# np.array([ithisc+'\n' for ithisc in thiscfglist]).tofile(cfgfile)
if ncfg == False:
    ncfg = totncfg


cfgindicies = GetCfgIndicies(totncfg,ncfg,nsrc)


if forcecfg == False:
    cfgintervals = GetIcfgTOFcfg(nproc,ncfg*nsrc )
    for icfg,fcfg in cfgintervals:
        print 'Submitting icfg='+str(icfg)+' fcfg='+str(fcfg)
        RunNext(icfg,fcfg,cfgindicies,Start=True)
else:
    RunNext(forcecfg[0],forcecfg[1],cfgindicies,Start=True)
        
