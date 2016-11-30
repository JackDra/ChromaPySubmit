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
            if icfg >= fcfg:
                stage,icfg = ['Done',icfg]
            else:
                stage,icfg = ['twoptcorr',icfg+1]
            return stage,icfg
        else:
            stage = 'threeptcorr'
            return stage,icfg
    if 'threeptcorr' in stage:
        if icfg >= fcfg:
            stage,icfg = ['Done',icfg]
        else:
            stage,icfg = ['twoptcorr',icfg+1]
        return stage,icfg

def RunNext(icfg,fcfg,cfgindicies='FromFile',stage='twoptcorr',Errored='Complete',Start=False):
    
    icfg,fcfg = map(int,[icfg,fcfg])
    if cfgindicies == 'FromFile':
        with open(paramdir+indexfilename,'r'):
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
        for thecfg in cfgindicies[icfg-1:fcfg]:
            if DoJsm3pt:
                boolcheck = all([Check2ptCorr(thecfg,ismlist,jsmlist,twoptinterps) and
                                 Check3ptCorrjsm(thecfg,ismlist,jsmlist,it_sst,ProjectorList,DSList) for thecfg in cfgindicies[icfg-1:fcfg]])
            else:
                boolcheck = all([Check2ptCorr(thecfg,ismlist,jsmlist,twoptinterps) and
                                 Check3ptCorr(thecfg,ismlist,it_sst,ProjectorList,DSList) for thecfg in cfgindicies[icfg-1:fcfg]])
                
            
    if boolcheck:
        if not Save2ptProp:
            for thecfg in cfgindicies[icfg-1:fcfg]:
                RemoveProp(thecfg,ismlist)
        print 'All Complete'
        return

    # GetGaugeField(icfg)
        
    curricfg = icfg
    if not Start: stage,curricfg = IncrementRun(stage,curricfg,fcfg)
    StillInc = True
    while StillInc:
        StillInc = False
        if 'twoptcorr' in stage:
            if Check2ptCorr(cfgindicies[curricfg],ismlist,jsmlist,twoptinterps):
                stage,curricfg = IncrementRun(stage,curricfg,fcfg)
                if 'Done' in stage:
                    if not Save2ptProp:
                        for thecfg in cfgindicies[icfg-1:fcfg]:
                            RemoveProp(thecfg,ismlist)
                    print 'All Done'
                    return
                else:
                    StillInc = True
        elif 'threeptcorr' in stage:
            if DoJsm3pt:
                if Check3ptCorrjsm(cfgindicies[curricfg],ismlist,jsmlist,it_sst,ProjectorList,DSList):
                    stage,curricfg = IncrementRun(stage,curricfg,fcfg)
                    if 'Done' in stage:
                        if not Save2ptProp:
                            for thecfg in cfgindicies[icfg-1:fcfg]:
                                RemoveProp(thecfg,ismlist)
                        print 'All Done'
                        return
                    else:
                        StillInc = True
            else:
                if Check3ptCorr(cfgindicies[curricfg],ismlist,it_sst,ProjectorList,DSList):
                    stage,curricfg = IncrementRun(stage,curricfg,fcfg)
                    if 'Done' in stage:
                        if not Save2ptProp:
                            for thecfg in cfgindicies[icfg-1:fcfg]:
                                RemoveProp(thecfg,ismlist)
                        print 'All Done'
                        return
                    else:
                        StillInc = True

                

        
    if DoJsm3pt:
        thisjoblist = CreateCombCorrWrap(InputFolder,ChromaFileFlag,curricfg,fcfg,cfgindicies)    
        for ism in ismlist:
            map(mkdir_p,Get3ptCorrFolderjsmList(cfgindicies[curricfg],ism))
        if Submit:
            runfile = Scom+' '+CreateCSHWrap(cfgindicies,curricfg,fcfg,thisjoblist,'Comb')
        else:
            runfile = CreateCSHWrap(cfgindicies,curricfg,fcfg,thisjoblist,'Comb')
        print runfile
        # if not DontRun: subprocess.call([runfile],cwd=basedir)
        if not DontRun: os.system(runfile)
    elif 'twopt' in stage:        
        thisjoblist = Create2ptCorrWrap(InputFolder,ChromaFileFlag,curricfg,fcfg,cfgindicies)
        if Submit:
            runfile = Scom+' '+CreateCSHWrap(cfgindicies,curricfg,fcfg,thisjoblist,stage)
        else:
            runfile = CreateCSHWrap(cfgindicies,curricfg,fcfg,thisjoblist,stage)
        print runfile
        # if not DontRun: subprocess.call([runfile],cwd=basedir)
        if not DontRun: os.system(runfile)
    elif 'three' in stage:
        thisjoblist = Create3ptCorrWrap(InputFolder,ChromaFileFlag,curricfg,fcfg,cfgindicies)    
        for ism in ismlist:
            map(mkdir_p,Get3ptCorrFolderList(cfgindicies[curricfg],ism))
        if Submit:
            runfile = Scom+' '+CreateCSHWrap(cfgindicies,curricfg,fcfg,thisjoblist,stage)
        else:
            runfile = CreateCSHWrap(cfgindicies,curricfg,fcfg,thisjoblist,stage)
        print runfile
        # if not DontRun: subprocess.call([runfile],cwd=basedir)
        if not DontRun: os.system(runfile)

            

if len(sys.argv) > 1 and 'ReSubmit' in sys.argv[0]:
    RunNext(*sys.argv[1:])
    # RunNext(*sys.argv[1:],Start=False)
