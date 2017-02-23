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

        



thiscfglist,totncfg = CreateCfgList(1,Src=False)


runcfglist = []
for icfg in CheckFlowDoneListFF(thiscfglist):
    runcfglist.append(int(icfg.replace('\n','')))

# for icfg in runcfglist:
#     print icfg
thisjoblist = CreateFlowFilesWrap(InputFolder,ChromaFileFlag,runcfglist)

runfile = CreateFlowCSHWrap(runcfglist,thisjoblist,nproc)
if Submit:
    runfile = Scom+' '+runfile

print runfile
# if not DontRun: subprocess.call([runfile],cwd=basedir)
if not DontRun: os.system(runfile)

        
