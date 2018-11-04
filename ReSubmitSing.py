#!/usr/bin/env python

from RunParams import paramdir,indexfilename
from RunParams import ismlist,jsmlist,twoptinterps
from RunParams import it_sst,ProjectorList,DSList
from RunParams import InputFolder,ChromaFileFlag
from RunParams import Submit,Scom,DontRun
from MiscFuns import mkdir_p
from GetAndCheckData import Check2ptCorr,Check3ptCorr
from CreateChromaFiles import CreateCombCorrWrap
from FilenameFuns import Get3ptCorrFolderList
import sys,os
# import subprocess
# import commands
from CreateCSH import CreateCSHWrap



def RunNextComb(icfg,fcfg,thisnproc,cfgindicies='FromFile'):

    thisnproc = int(thisnproc)
    icfg,fcfg = map(int,[icfg,fcfg])
    if cfgindicies == 'FromFile':
        with open(paramdir+indexfilename,'r') as f:
            # cfgindicies = map(int,f.readlines())
            cfgindicies = map(int,f.readlines())

    ##check if whole run is done
    boolcheck = all([Check2ptCorr(thecfg,ismlist,jsmlist,twoptinterps) and
                     Check3ptCorr(thecfg,ismlist,it_sst,ProjectorList,DSList) for thecfg in cfgindicies[icfg-1:fcfg]])

    if boolcheck:
        print 'All Complete'
        return

    # GetGaugeField(icfg)

    NewCfgList = []
    for thecfg in cfgindicies[icfg-1:fcfg]:
        if (not Check3ptCorr(thecfg,ismlist,it_sst,ProjectorList,DSList)) or (not Check2ptCorr(thecfg,ismlist,jsmlist,twoptinterps)):
            NewCfgList.append(thecfg)

    if len(NewCfgList) == 0:
        print 'All Done'
        return



    thisjoblist = CreateCombCorrWrap(InputFolder,ChromaFileFlag,NewCfgList)
    for ism in ismlist:
        for curricfg in NewCfgList:
            map(mkdir_p,Get3ptCorrFolderList(curricfg,ism))
    if Submit:
        runfile = Scom+' '+CreateCSHWrap(NewCfgList,icfg,fcfg,thisjoblist,'Comb',thisnproc,False)
    else:
        runfile = CreateCSHWrap(NewCfgList,icfg,fcfg,thisjoblist,'Comb',thisnproc,False)
    print runfile
    # if not DontRun: subprocess.call([runfile],cwd=basedir)
    if not DontRun: os.system(runfile)



if __name__ == '__main__':
    if len(sys.argv) > 1 and 'ReSubmit' in sys.argv[0]:
        RunNextComb(*sys.argv[1:])
        # RunNext(*sys.argv[1:],Start=False)
