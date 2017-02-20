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


if os.path.isfile(FlowDoneList):
    runcfglist = []
    for icfg in thiscfglist:
        if not CheckFlowDoneList(icfg.replace('\n','')):
            runcfglist.append(int(icfg.replace('\n','')))
else:
    runcfglist = [int(icfg.replace('\n','')) for icfg in thiscfglist]

# for icfg in runcfglist:
#     print icfg
thisjoblist = CreateFlowFilesWrap(InputFolder,ChromaFileFlag,runcfglist)

runfile = CreateFlowCSHWrap(runcfglist,thisjoblist,nproc)

print runfile
# if not DontRun: subprocess.call([runfile],cwd=basedir)
if not DontRun: os.system(runfile)

        
