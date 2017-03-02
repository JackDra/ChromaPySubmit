#!/usr/bin/env python

from RunParams import *
from GetAndCheckData import *
from CreateChromaFiles import *
import sys,os
import subprocess
import commands
from CreateCSH import CreateCSHWrap,RemoveCSH

DefParams = [it_sst[0],ProjectorList[0],DSList[0]]

def IncrementRun(stage):
    if OnlyGauge: return 'Done'
    if 'twoptcorr' in stage:
        if OnlyTwoPt:
            return 'Done'
        else:
            return  'threeptcorr'
    if 'threeptcorr' in stage:
        return 'Done'

def RunNext(icfg,fcfg,stage='twoptcorr',thisnproc=nproc,Start=False,cfgindicies='FromFile',othree=False):

    thisnproc = int(thisnproc)
    icfg,fcfg = map(int,[icfg,fcfg])
    if cfgindicies == 'FromFile':
        with open(paramdir+indexfilename,'r') as f:
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
        
    if not Start: stage = IncrementRun(stage)
    if othree: stage = 'threeptcorr'
    newstage = stage
    NewCfgList = []
    while len(NewCfgList) == 0:
        NewCfgList = []
        stage = newstage
        for thecfg in cfgindicies[icfg-1:fcfg]:
            if 'twoptcorr' in stage:
                if not Check2ptCorr(thecfg,ismlist,jsmlist,twoptinterps):
                    NewCfgList.append(thecfg)
            elif 'threeptcorr' in stage:
                if DoJsm3pt:
                    if not Check3ptCorrjsm(thecfg,ismlist,jsmlist,it_sst,ProjectorList,DSList):
                        if not othree or Check2ptCorr(thecfg,ismlist,jsmlist,twoptinterps):
                            NewCfgList.append(thecfg)
                else:
                    if not Check3ptCorr(thecfg,ismlist,it_sst,ProjectorList,DSList):
                        if not othree or Check2ptCorr(thecfg,ismlist,jsmlist,twoptinterps):
                            NewCfgList.append(thecfg)
            elif 'Done' in stage:
                break
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
            runfile = Scom+' '+CreateCSHWrap(NewCfgList,icfg,fcfg,thisjoblist,'Comb',thisnproc=thisnproc)
        else:
            runfile = CreateCSHWrap(NewCfgList,icfg,fcfg,thisjoblist,'Comb',thisnproc)
        print runfile
        # if not DontRun: subprocess.call([runfile],cwd=basedir)
        if not DontRun: os.system(runfile)
    elif 'twopt' in stage:        
        thisjoblist = Create2ptCorrWrap(InputFolder,ChromaFileFlag,NewCfgList)
        if Submit:
            runfile = Scom+' '+CreateCSHWrap(NewCfgList,icfg,fcfg,thisjoblist,stage,thisnproc)
        else:
            runfile = CreateCSHWrap(NewCfgList,icfg,fcfg,thisjoblist,stage,thisnproc)
        print runfile
        # if not DontRun: subprocess.call([runfile],cwd=basedir)
        if not DontRun: os.system(runfile)
    elif 'three' in stage:
        thisjoblist = Create3ptCorrWrap(InputFolder,ChromaFileFlag,NewCfgList)    
        for ism in ismlist:
            for curricfg in NewCfgList:
                map(mkdir_p,Get3ptCorrFolderList(curricfg,ism))
        if Submit:
            runfile = Scom+' '+CreateCSHWrap(NewCfgList,icfg,fcfg,thisjoblist,stage,thisnproc)
        else:
            runfile = CreateCSHWrap(NewCfgList,icfg,fcfg,thisjoblist,stage,thisnproc)
        print runfile
        # if not DontRun: subprocess.call([runfile],cwd=basedir)
        if not DontRun: os.system(runfile)

            

if len(sys.argv) > 1 and 'ReSubmit' in sys.argv[0]:
    RunNext(*sys.argv[1:])
    # RunNext(*sys.argv[1:],Start=False)
