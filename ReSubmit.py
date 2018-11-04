#!/usr/bin/env python

from RunParams import paramdir,indexfilename
from RunParams import ismlist,jsmlist,twoptinterps
from RunParams import it_sst,ProjectorList,DSList
from RunParams import InputFolder,ChromaFileFlag
from RunParams import Submit,Scom,DontRun,OnlyGauge
from RunParams import OnlyTwoPt,DoJsm3pt,Save2ptProp
from MiscFuns import mkdir_p
from GetAndCheckData import Check2ptCorr,Check3ptCorr
from GetAndCheckData import Check3ptCorrjsm,RemoveProp
from CreateChromaFiles import CreateCombCorrWrap,Create2ptCorrWrap
from CreateChromaFiles import Create3ptCorrWrap
from FilenameFuns import Get3ptCorrFolderList,Get3ptCorrFolderjsmList
import sys,os
# import subprocess
# import commands
from CreateCSH import CreateCSHWrap


def IncrementRun(stage):
    if OnlyGauge: return 'Done'
    if 'twoptcorr' in stage:
        if OnlyTwoPt:
            return 'Done'
        else:
            return  'threeptcorr'
    if 'threeptcorr' in stage:
        return 'Done'
    if 'Done' in stage:
        return 'Done'

def RunNext(icfg,fcfg,stage,othree,thisnproc,cfgindicies='FromFile'):

    if isinstance(othree,basestring):
        if 'True' in othree:
            othree = True
        else:
            othree = False

    thisnproc = int(thisnproc)
    icfg,fcfg = map(int,[icfg,fcfg])
    if cfgindicies == 'FromFile':
        with open(paramdir+indexfilename,'r') as f:
            # cfgindicies = map(int,f.readlines())
            cfgindicies = map(int,f.readlines())



    # for ism in ismlist:
    #     for thecfg in cfgindicies[icfg-1:fcfg]:
    #         RemoveCSH(thecfg,ism,stage)
    #removes fort parameter files
    # if OnlyGauge:
    #     RemoveGaugeFieldFiles(InputFolder)
    #     thisjoblist = CreateGaugeFieldFiles(InputFolder,ChromaFileFlag)
    #     if Submit:
    #         runfile = Scom+' '+CreateCSHWrap(icfg,fcfg,thisjoblist,'gfield')
    #     else:
    #         runfile = CreateCSHWrap(icfg,fcfg,thisjoblist,'gfield')
    #     print runfile
    #     # if not DontRun: subprocess.call([runfile],cwd=basedir)
    #     if not DontRun: os.system(runfile)
    #     return



    # if DoJsm3pt:
    #     RemoveCombCorrFiles(InputFolder)
    # elif 'twoptcorr' in stage:
    #     Remove2ptCorrFiles(InputFolder)
    # elif 'threeptcorr' in stage:
    #     Remove3ptCorrFiles(InputFolder)


            ##check if whole run is done
    if OnlyTwoPt:
        boolcheck = all([Check2ptCorr(thecfg,ismlist,jsmlist,twoptinterps) for thecfg in cfgindicies[icfg-1:fcfg]])
    else:
        if DoJsm3pt:
            boolcheck = all([Check2ptCorr(thecfg,ismlist,jsmlist,twoptinterps) and
                             Check3ptCorrjsm(thecfg,ismlist,jsmlist,it_sst,ProjectorList,DSList) for thecfg in cfgindicies[icfg-1:fcfg]])
        else:
            boolcheck = all([(Check2ptCorr(thecfg,ismlist,jsmlist,twoptinterps) and
                             Check3ptCorr(thecfg,ismlist,it_sst,ProjectorList,DSList)) for thecfg in cfgindicies[icfg-1:fcfg]])


    if boolcheck:
        if not Save2ptProp:
            for thecfg in cfgindicies[icfg-1:fcfg]:
                RemoveProp(thecfg,ismlist)
        print 'All Complete'
        return

    # GetGaugeField(icfg)

    if othree: stage = 'threeptcorr'
    newstage = stage
    NewCfgList = []
    while len(NewCfgList) == 0:
        stage = newstage
        if 'Done' in newstage:
            break
        NewCfgList = []
        for thecfg in cfgindicies[icfg-1:fcfg]:
            if 'twoptcorr' in stage:
                if not Check2ptCorr(thecfg,ismlist,jsmlist,twoptinterps):
                    NewCfgList.append(thecfg)
            elif 'threeptcorr' in stage:
                if DoJsm3pt:
                    if not Check3ptCorrjsm(thecfg,ismlist,jsmlist,it_sst,ProjectorList,DSList):
                        if (not othree) or Check2ptCorr(thecfg,ismlist,jsmlist,twoptinterps):
                            NewCfgList.append(thecfg)
                else:
                    if not Check3ptCorr(thecfg,ismlist,it_sst,ProjectorList,DSList):
                        if (not othree) or Check2ptCorr(thecfg,ismlist,jsmlist,twoptinterps):
                            NewCfgList.append(thecfg)
        newstage = IncrementRun(stage)

    if len(NewCfgList) == 0:
        print 'All Done'
        return



    if DoJsm3pt:
        thisjoblist = CreateCombCorrWrap(InputFolder,ChromaFileFlag,NewCfgList)
        for ism in ismlist:
            for curricfg in NewCfgList:
                map(mkdir_p,Get3ptCorrFolderjsmList(curricfg,ism))
        if Submit:
            runfile = Scom+' '+CreateCSHWrap(NewCfgList,icfg,fcfg,thisjoblist,'Comb',thisnproc,othree)
        else:
            runfile = CreateCSHWrap(NewCfgList,icfg,fcfg,thisjoblist,'Comb',thisnproc,othree)
        print runfile
        # if not DontRun: subprocess.call([runfile],cwd=basedir)
        if not DontRun: os.system(runfile)
    elif 'twopt' in stage:
        thisjoblist = Create2ptCorrWrap(InputFolder,ChromaFileFlag,NewCfgList)
        if Submit:
            runfile = Scom+' '+CreateCSHWrap(NewCfgList,icfg,fcfg,thisjoblist,stage,thisnproc,othree)
        else:
            runfile = CreateCSHWrap(NewCfgList,icfg,fcfg,thisjoblist,stage,thisnproc,othree)
        print runfile
        # if not DontRun: subprocess.call([runfile],cwd=basedir)
        if not DontRun: os.system(runfile)
    elif 'three' in stage:
        thisjoblist = Create3ptCorrWrap(InputFolder,ChromaFileFlag,NewCfgList)
        for ism in ismlist:
            for curricfg in NewCfgList:
                map(mkdir_p,Get3ptCorrFolderList(curricfg,ism))
        if Submit:
            runfile = Scom+' '+CreateCSHWrap(NewCfgList,icfg,fcfg,thisjoblist,stage,thisnproc,False)
        else:
            runfile = CreateCSHWrap(NewCfgList,icfg,fcfg,thisjoblist,stage,thisnproc,False)
        print runfile
        # if not DontRun: subprocess.call([runfile],cwd=basedir)
        if not DontRun: os.system(runfile)



if len(sys.argv) > 1 and 'ReSubmit' in sys.argv[0]:
    RunNext(*sys.argv[1:])
    # RunNext(*sys.argv[1:],Start=False)
