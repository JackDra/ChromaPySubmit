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
for iin in sys.argv[1:]:
    if '-np=' in iin:
        njobs = int(iin.replace('-np=',''))
    elif '-forcecfg=' in iin:
        forcecfg = map(int,iin.replace('-forcecfg=','').split(','))
        print 'WARNING: currenlty forcecfg stuffs up the random list, need to be fixed'
    elif '-ncfg=' in iin:
        ncfg = int(iin.replace('-ncfg=',''))
    elif '-nsrc=' in iin:
        nsrc = int(iin.replace('-nsrc=',''))
        
        
if njobs == -1:
    raise IOError('please give number of processors as -np=## ')
    
print 'Number of jobs = ' , njobs

# if sys.argv[2] == 'a':
#     thisgfosnum = range(1,10)
# else:
#     thisgfosnum = map(int,sys.argv[2:])
# nproc = int(sys.argv[1])


# np.array([ithisc+'\n' for ithisc in thiscfglist]).tofile(cfgfile)

thiscfglist,totncfg = CreateCfgList(njobs,forcecfg)

if ncfg == False:
    ncfg = totncfg
cfgindicies = GetCfgIndicies(totncfg,ncfg,nsrc)



# if forcecfg == False:
cfgintervals = GetIcfgTOFcfg(njobs,ncfg*nsrc )
for iin,(icfg,fcfg) in enumerate(cfgintervals):
    thisnproc = nproc
    if iin > len(cfgintervals) and halfishalf: thisnproc=nproc/2
    print 'Submitting icfg='+str(icfg)+' fcfg='+str(fcfg)    
    RunNext(icfg,fcfg,Start=True,cfgindicies=cfgindicies,thisnproc=thisnproc)
# else:
#     RunNext(forcecfg[0],forcecfg[1],Start=True,cfgindicies=cfgindicies)
        
