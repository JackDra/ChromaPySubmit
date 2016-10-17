#!/usr/bin/env python

from RunParams import *
from CreateCfgFile import *
from CreateChromaFiles import *
from GetAndCheckData import *
from ReSubmit import RunNext
import sys
import subprocess

nproc = -1
for iin in sys.argv[1:]:
    if '-np=' in iin:
        nproc = int(iin.replace('-np=',''))

if nproc == -1:
    raise IOError('please give number of processors as -np=## ')
    
print 'Number of processors = ' , nproc

# if sys.argv[2] == 'a':
#     thisgfosnum = range(1,10)
# else:
#     thisgfosnum = map(int,sys.argv[2:])
# nproc = int(sys.argv[1])


thiscfglist = CreateCfgList()
cfgintervals = GetIcfgTOFcfg(nproc,len(thiscfglist))
for icfg,fcfg in cfgintervals:
    print 'Submitting icfg='+str(icfg)+' fcfg='+str(fcfg)
    RunNext(icfg,fcfg,Start=True)
