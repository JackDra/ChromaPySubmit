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
thisnDup=DubCfgs
thisncfg=0
for iin in sys.argv[1:]:
    if '-np=' in iin:
        nproc = int(iin.replace('-np=',''))
    elif '-forcecfg=' in iin:
        forcecfg = map(int,iin.replace('-forcecfg=','').split(','))
    elif '-ncfg=' in iin:
        thisncfg = map(int,iin.replace('-ncfg=',''))
    elif '-nDup=' in iin:
        thisnDup = map(int,iin.replace('-nDup=',''))
        
if nproc == -1:
    raise IOError('please give number of processors as -np=## ')
    
print 'Number of processors = ' , nproc

# if sys.argv[2] == 'a':
#     thisgfosnum = range(1,10)
# else:
#     thisgfosnum = map(int,sys.argv[2:])
# nproc = int(sys.argv[1])


thiscfglist = CreateCfgList(thisDubCfgs=thisnDup,ncfg=thisncfg)
# np.array([ithisc+'\n' for ithisc in thiscfglist]).tofile(cfgfile)


if forcecfg == False:
    cfgintervals = GetIcfgTOFcfg(nproc,len(thiscfglist))
    for icfg,fcfg in cfgintervals:
        print 'Submitting icfg='+str(icfg)+' fcfg='+str(fcfg)
        RunNext(icfg,fcfg,Start=True)
else:
    RunNext(forcecfg[0],forcecfg[1],Start=True)
        
