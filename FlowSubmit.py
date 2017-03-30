#!/usr/bin/env python

from RunParams import *
from CreateCfgFile import *
from CreateCSH import *
from CreateChromaFiles import *
from GetAndCheckData import *
from ReSubmit import RunNext
import sys
import subprocess
import numpy as np

        


njobs = 1
SingJobIndex = False
for iin in sys.argv[1:]:
    if '-np=' in iin:
        njobs = int(iin.replace('-np=',''))
    if '-ijob=' in iin:
        SingJobIndex = int(iin.replace('-ijob=',''))
        
        
thiscfglist,totncfg = CreateCfgList(njobs,Src=False)


runcfglist = []
for icfg in CheckFlowDoneListFF(thiscfglist):
    runcfglist.append(int(icfg.replace('\n','')))

# for icfg in runcfglist:
#     print icfg
thisjoblist = CreateFlowFilesWrap(InputFolder,ChromaFileFlag,runcfglist)

if SingJobIndex != False:
    icfglist,ijoblist = np.array_split(np.array(runcfglist),njobs)[SingJobIndex],np.array_split(np.array(thisjoblist),njobs)[SingJobIndex]
    runfile = CreateFlowCSHWrap(icfglist,ijoblist,nproc,SingJobIndex,njobs)
    if Submit:
        runfile = Scom+' '+runfile
    print runfile
    # if not DontRun: subprocess.call([runfile],cwd=basedir)
    if not DontRun: os.system(runfile)
else:
    for ijob,(icfglist,ijoblist) in enumerate(zip(np.array_split(np.array(runcfglist),njobs),np.array_split(np.array(thisjoblist),njobs))):
        runfile = CreateFlowCSHWrap(icfglist,ijoblist,nproc,ijob,njobs)
        if Submit:
            runfile = Scom+' '+runfile
        print runfile
        # if not DontRun: subprocess.call([runfile],cwd=basedir)
        if not DontRun: os.system(runfile)

        
