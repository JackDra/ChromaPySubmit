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
boundicfg = -1
boundfcfg = 100000
for iin in sys.argv[1:]:
    if '-np=' in iin:
        nproc = int(iin.replace('-np=',''))
    if '-fcfg=' in iin:
        boundfcfg = int(iin.replace('-fcfg=',''))
    if '-icfg=' in iin:
        boundicfg = int(iin.replace('-icfg=',''))
        
if nproc == -1:
    raise IOError('please give number of processors as -np=## ')
    
print 'Number of processors = ' , nproc

# if sys.argv[2] == 'a':
#     thisgfosnum = range(1,10)
# else:
#     thisgfosnum = map(int,sys.argv[2:])
# nproc = int(sys.argv[1])


thiscfglist = CreateCfgList()
# np.array([ithisc+'\n' for ithisc in thiscfglist]).tofile(cfgfile)
cfgintervals = GetIcfgTOFcfg(nproc,len(thiscfglist))


for icfg,fcfg in cfgintervals:
    if boundfcfg < fcfg: continue
    if boundicfg > icfg: continue
    print 'Submitting icfg='+str(icfg)+' fcfg='+str(fcfg)
    RunNext(icfg,fcfg,Start=True)
