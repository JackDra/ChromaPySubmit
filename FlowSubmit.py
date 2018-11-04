#!/usr/bin/env python

from RunParams import InputFolder,ChromaFileFlag,nproc
from RunParams import Submit,Scom,DontRun
from CreateCfgFile import CreateCfgList
from FilenameFuns import CheckFlowDoneList,CheckFlowDoneListFF
from CreateCSH import CreateFlowCSHWrap
from CreateChromaFiles import CreateFlowFilesWrap
# from GetAndCheckData import *
# from ReSubmit import RunNext

import sys,os
# import subprocess
import numpy as np




njobs = 1
SingJobIndex = 'None'
mach_jobs = 1
this_mach_job = 1
use_done_list = False

for iin in sys.argv[1:]:
    if '-np=' in iin:
        njobs = int(iin.replace('-np=',''))
    if '-ijob=' in iin:
        SingJobIndex = int(iin.replace('-ijob=',''))
    if '-SplitJob=' in iin:
        mach_jobs = int(iin.replace('-SplitJob=',''))
    if '-ThisJob=' in iin:
        this_mach_job = int(iin.replace('-ThisJob=',''))
    if '-UseDoneList=' in iin:
        use_done_list = bool(iin)
    if '-help' in iin:
        print
        print ' -np=#        Specifies how many jobs to submit to the machine'
        print " -ijob=#      Used for re-running. Picks the ijob'th job out of np jobs"
        print ' -SplitJob=#  Used when running over multiple machines. Specifies total number of machines to run over'
        print ' -ThisJob=#   Used when running over multiple machines. Specifies which machine number this is (e.g. juqueen=1, laconia=2 etc..)'
        print ' -UseDoneList=#   uses the done list, instead of checking spesifically what is not done'
        print
        exit()


# for ics,isys in enumerate(sys.argv[1:]):
#     if '-np=' in isys:
#         del sys.argv[ics+1]
resubflags = ' '.join(sys.argv[1:])

if use_done_list:
    print 'using ***DoneList.txt in ./ParamFiles/ to keep track of completed configurations'
else:
    print 'manually checking output directory to keep track of completed configurations'


thiscfglist,totncfg = CreateCfgList(njobs,Src=False)

if mach_jobs > 1:
    thiscfglist = np.array_split(thiscfglist,mach_jobs)[this_mach_job-1]

runcfglist = []
if use_done_list:
    checkfun = CheckFlowDoneList
else:
    checkfun = CheckFlowDoneListFF

# print 'DEBUG'
# print thiscfglist
# print checkfun(thiscfglist)

for icfg in checkfun(thiscfglist):
    runcfglist.append(int(icfg.replace('\n','')))

# print 'DEBUG2'
# for icfg in runcfglist:
#     print icfg
if len(runcfglist) == 0:
    print 'Run Complete'
    exit()
thisjoblist = CreateFlowFilesWrap(InputFolder,ChromaFileFlag,runcfglist)

if SingJobIndex != 'None':
    icfglist,ijoblist = np.array_split(np.array(runcfglist),njobs)[SingJobIndex],np.array_split(np.array(thisjoblist),njobs)[SingJobIndex]
    runfile = CreateFlowCSHWrap(icfglist,ijoblist,nproc,resubflags,njobs)
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
