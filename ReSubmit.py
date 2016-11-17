#!/usr/bin/env python

from RunParams import *
from GetAndCheckData import *
from CreateChromaFiles import *
import sys,os
import subprocess
import commands
from CreateCSH import CreateCSHWrap,RemoveCSH

DefParams = [it_sst[0],ProjectorList[0],DSList[0]]

def IncrementRun(stage,icfg,fcfg):
    if OnlyGauge: return ['Done',ismlist[0]]
    if 'twoptcorr' in stage:
        if OnlyTwoPt:
            if icfg == fcfg:
                stage,icfg = ['Done',icfg]
            else:
                stage,icfg = ['twoptcorr',icfg+1]
            return stage,icfg
        else:
            stage = 'threeptcorr'
            return [stage,icfg]
    if 'threeptcorr' in stage:
        if icfg == fcfg:
            stage,ism = ['Done',icfg]
        else:
            stage,ism = ['twoptcorr',icfg+1]
        return stage,ism

def RunNext(icfg,fcfg,stage='twoptcorr',Errored='Complete',Start=False):
    
    icfg,fcfg = map(int,[icfg,fcfg])
    for ism in ismlist:
        for thecfg in range(icfg,fcfg+1):
            RemoveCSH(thecfg,ism,stage)
    #removes fort parameter files

    if 'twoptcorr' in stage:
        for thecfg in range(icfg,fcfg+1):
            Remove2ptCorrFiles(InputFolder,ChromaFileFlag,thecfg,ismlist)    
    elif 'threeptcorr' in stage:
        for thecfg in range(icfg,fcfg+1):
            Remove3ptCorrFiles(InputFolder,ChromaFileFlag,thecfg,ismlist)    
                

            ##check if whole run is done
    boolcheck = True
    if OnlyTwoPt:
        for thecfg in range(icfg,fcfg+1):
            boolcheck = boolcheck and Check2ptCorr(thecfg,ismlist,jsmlist,twoptinterps)
    else:
        for thecfg in range(icfg,fcfg+1):
            if DoJsm3pt:
                boolcheck = boolcheck and (Check2ptCorr(thecfg,ismlist,jsmlist,twoptinterps) and Check3ptCorrjsm(thecfg,ismlist,jsmlist,it_sst,ProjectorList,DSList))
            else:
                boolcheck = boolcheck and (Check2ptCorr(thecfg,ismlist,jsmlist,twoptinterps) and Check3ptCorr(thecfg,ismlist,it_sst,ProjectorList,DSList))
                
            
    if boolcheck:
        for thecfg in range(icfg,fcfg+1):
            RemoveProp(icfg,ismlist)
        print 'All Complete'
        return

    # GetGaugeField(icfg)
        
    curricfg = icfg
    if not Start: stage,curricfg = IncrementRun(stage,curricfg,fcfg)
    StillInc = True
    while StillInc:
        StillInc = False
        if 'twoptcorr' in stage:
            if Check2ptCorr(icfg,ismlist,jsmlist,twoptinterps):
                stage,curricfg = IncrementRun(stage,curricfg,fcfg)
                if 'Done' in stage:
                    print 'All Done'
                    return
                else:
                    StillInc = True
        elif 'threeptcorr' in stage:
            if DoJsm3pt:
                if Check3ptCorrjsm(icfg,ismlist,jsmlist,it_sst,ProjectorList,DSList):
                    stage = IncrementRun(stage,curricfg,fcfg)
                    if 'Done' in stage:
                        print 'All Done'
                        return
                    else:
                        StillInc = True
            else:
                if Check3ptCorr(icfg,ismlist,it_sst,ProjectorList,DSList):
                    stage = IncrementRun(stage,curricfg,fcfg)
                    if 'Done' in stage:
                        print 'All Done'
                        return
                    else:
                        StillInc = True

                
    if 'twopt' in stage:
        thisjoblist = Create2ptCorrWrap(InputFolder,ChromaFileFlag,curricfg,fcfg)
        if Submit:
            runfile = Scom+' '+CreateCSHWrap(curricfg,fcfg,thisjoblist,stage)
        else:
            runfile = CreateCSHWrap(curricfg,fcfg,thisjoblist,stage)
        print runfile
        # if not DontRun: subprocess.call([runfile],cwd=basedir)
        if not DontRun: os.system(runfile)
    elif 'three' in stage:
        if DoJsm3pt:
            thisjoblist = Create3ptCorrWrapjsm(InputFolder,ChromaFileFlag,curricfg,fcfg)    
            for ism in ismlist:
                map(mkdir_p,Get3ptCorrFolderjsmList(curricfg,ism))
        else:
            thisjoblist = Create3ptCorrWrap(InputFolder,ChromaFileFlag,curricfg,fcfg)    
            for ism in ismlist:
                map(mkdir_p,Get3ptCorrFolderList(curricfg,ism))
        if Submit:
            runfile = Scom+' '+CreateCSHWrap(curricfg,fcfg,thisjoblist,stage)
        else:
            runfile = CreateCSHWrap(curricfg,fcfg,thisjoblist,stage)
        print runfile
        # if not DontRun: subprocess.call([runfile],cwd=basedir)
        if not DontRun: os.system(runfile)

            

if len(sys.argv) > 1 and 'ReSubmit' in sys.argv[0]:
    RunNext(*sys.argv[1:])
    # RunNext(*sys.argv[1:],Start=False)
