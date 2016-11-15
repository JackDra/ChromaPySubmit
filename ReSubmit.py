#!/usr/bin/env python

from RunParams import *
from GetAndCheckData import *
from CreateChromaFiles import *
import sys,os
import subprocess
import commands
from CreateCSH import CreateCSHWrap,RemoveCSH

DefParams = [it_sst[0],ProjectorList[0],DSList[0]]

def IncrementRun(stage,ism):
    if OnlyGauge: return ['Done',ismlist[0]]
    if 'twoptcorr' in stage:
        if OnlyTwoPt:
            if ism == ismlist[-1]:
                stage,ism = ['Done',ismlist[0]]
            else:
                stage,ism = ['twoptcorr',ismlist[ismlist.index(ism)+1]]
            return stage,ism
        else:
            stage = 'threeptcorr'
            return [stage,ism]
    if 'threeptcorr' in stage:
        if ism == ismlist[-1]:
            stage,ism = ['Done',ismlist[0]]
        else:
            stage,ism = ['twoptcorr',ismlist[ismlist.index(ism)+1]]
        return stage,ism

def RunNext(icfg,fcfg,stage='twoptcorr',ism=ismlist[0],Errored='Complete',Start=False):
    
    icfg,fcfg,ism = map(int,[icfg,fcfg,ism])
    RemoveCSH(icfg,ism,stage)
    #removes fort parameter files

    if OnlyGauge:
        while icfg <=fcfg:
            if CheckGaugeField(icfg) :
                icfg += 1
            else:
                [thisjobid] = CreateGaugeFieldFiles(InputFolder,ChromaFileFlag,icfg)
                if Submit:
                    runfile = Scom+' '+CreateCSHWrap(icfg,fcfg,ism,thisjobid,'gfield')
                else:
                    runfile = CreateCSHWrap(icfg,fcfg,ism,thisjobid,'gfield')
                print runfile
                # if not DontRun:subprocess.call([runfile],cwd=basedir)
                if not DontRun:os.system(runfile)
                return
        print 'All Complete'
        return


    if 'twoptcorr' in stage:
        Remove2ptCorrFiles(InputFolder,ChromaFileFlag,icfg,[ism])    
    elif 'threeptcorr' in stage:
        Remove3ptCorrFiles(InputFolder,ChromaFileFlag,icfg,[ism])    
        
    if Errored == 'Failed':
        print 'Error on config' + icfg
        # RemoveGaugeField(icfg)
        Remove2ptCorr(icfg,ismlist,jsmlist)
        Remove3ptCorr(icfg,ismlist,it_sst,ProjectorList,DSList)
        if icfg<fcfg and not ExitOnFail:
            RunNext(icfg+1,fcfg,Start=True)
        else:
            print 'All Complete'
        return
        

        #check if whole run is done
    if OnlyTwoPt:
        boolcheck = Check2ptCorr(icfg,[ism],jsmlist,twoptinterps)
    else:
        boolcheck = Check2ptCorr(icfg,[ism],jsmlist,twoptinterps) and Check3ptCorr(icfg,[ism],it_sst,ProjectorList,DSList)

    if boolcheck:
        RemoveProp(icfg,[ism])
        if ism == ismlist[-1]:
            # RemoveGaugeField(icfg)
            if icfg<fcfg:
                RunNext(icfg+1,fcfg,Start=True)
                return 
            else:
                print 'All Complete'
                return
        else:
            RunNext(icfg,fcfg,ism=ismlist[ismlist.index(ism)+1],Start=True)
            return

    # GetGaugeField(icfg)
    Move2ptCorr(icfg,[ism],jsmlist,twoptinterps)
    prevism = ism
    if not Start: stage,ism = IncrementRun(stage,ism)
        
    StillInc = True
    while StillInc:
        StillInc = False
        if 'twoptcorr' in stage:
            Move2ptCorr(icfg,[ism],jsmlist,twoptinterps)
            if Check2ptCorr(icfg,[ism],jsmlist,twoptinterps):
                stage,ism, = IncrementRun(stage,ism)
                if 'Done' not in stage: StillInc = True
        elif 'threeptcorr' in stage:
            if Check3ptCorr(icfg,[ism],it_sst,ProjectorList,DSList):
                stage,ism = IncrementRun(stage,ism)
                if 'Done' not in stage: StillInc = True
    if prevism != ism:
        RemoveProp(icfg,[prevism])


    if 'twopt' in stage:
        [thisjobid] = Create2ptCorrFiles(InputFolder,ChromaFileFlag,icfg,[ism])
        if Submit:
            runfile = Scom+' '+CreateCSHWrap(icfg,fcfg,ism,thisjobid,stage)
        else:
            runfile = CreateCSHWrap(icfg,fcfg,ism,thisjobid,stage)
        print runfile
        # if not DontRun: subprocess.call([runfile],cwd=basedir)
        if not DontRun: os.system(runfile)
    elif 'three' in stage:
        [thisjobid] = Create3ptCorrFiles(InputFolder,ChromaFileFlag,icfg,[ism])    
        map(mkdir_p,Get3ptCorrFolderList(icfg,ism))
        if Submit:
            runfile = Scom+' '+CreateCSHWrap(icfg,fcfg,ism,thisjobid,stage)
        else:
            runfile = CreateCSHWrap(icfg,fcfg,ism,thisjobid,stage)
        print runfile
        # if not DontRun: subprocess.call([runfile],cwd=basedir)
        if not DontRun: os.system(runfile)
    elif 'Done' in stage:
        if icfg<fcfg:
            RunNext(icfg+1,fcfg,Start=True)
        else:
            print 'All Complete'
        

if len(sys.argv) > 1 and 'ReSubmit' in sys.argv[0]:
    RunNext(*sys.argv[1:])
    # RunNext(*sys.argv[1:],Start=False)
