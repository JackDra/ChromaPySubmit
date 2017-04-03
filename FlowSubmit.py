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
mach_jobs = 1
this_mach_job = 1

for iin in sys.argv[1:]:
    if '-np=' in iin:
        njobs = int(iin.replace('-np=',''))
    if '-ijob=' in iin:
        SingJobIndex = int(iin.replace('-ijob=',''))
    if '-SplitJob=' in iin:
        mach_jobs = int(iin.replace('-SplitJob=',''))
    if '-ThisJob=' in iin:
        this_mach_job = int(iin.replace('-ThisJob=',''))
    if '-help' in iin:
        print 
        print ' -np=#        Specifies how many jobs to submit to the machine'
        print " -ijob=#      Used for re-running. Picks the ijob'th job out of np jobs"
        print ' -SplitJob=#  Used when running over multiple machines. Specifies total number of machines to run over'
        print ' -ThisJob=#   Used when running over multiple machines. Specifies which machine number this is (e.g. juqueen=1, laconia=2 etc..)'
        print 
        exit()
        

for ics,isys in enumerate(sys.argv[1:]):
    if '-np=' in isys:
        del sys.argv[ics+1]
resubflags = ' '.join(sys.argv[1:])



thiscfglist,totncfg = CreateCfgList(njobs,Src=False)

if mach_jobs > 1:
    thiscfglist = np.array_split(thiscfglist,mach_jobs)[this_mach_job-1]

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
        thisresub = resubflags+' -ijob='+str(ijob)
        runfile = CreateFlowCSHWrap(icfglist,ijoblist,nproc,thisresub,njobs)
        if Submit:
            runfile = Scom+' '+runfile
        print runfile
        # if not DontRun: subprocess.call([runfile],cwd=basedir)
        if not DontRun: os.system(runfile)

        
