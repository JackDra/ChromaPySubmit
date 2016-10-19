#!/usr/bin/env python

from RunParams import *
from GetAndCheckData import *
from CreateChromaFiles import *
import sys
import subprocess
import commands
from CreateCSH import CreateCSHWrap,RemoveCSH

DefParams = [it_sst[0],ProjectorList[0],DSList[0]]

def IncrementRun(stage,ism,tsink,Projector,DS):
    if 'twoptprop' in stage:
        stage = 'twoptcorr'
        return [stage,ism]+DefParams
    if 'twoptcorr' in stage:
        if OnlyTwoPt:
            if ism == ismlist[-1]:
                stage,ism,tsink,Projector,DS = ['Done',ismlist[0]]+DefParams
            else:
                stage,ism,tsink,Projector,DS = ['twoptprop',ismlist[ismlist.index(ism)+1]]+DefParams
            return stage,ism,tsink,Projector,DS
        else:
            stage = 'threeptcorr'
            return [stage,ism]+DefParams
    if 'threeptcorr' in stage:
        if tsink == it_sst[-1]:
            if Projector == ProjectorList[-1]:
                if DS == DSList[-1]:
                    if ism == ismlist[-1]:
                        stage,ism,tsink,Projector,DS = ['Done',ismlist[0]]+DefParams
                    else:
                        stage,ism,tsink,Projector,DS = ['twoptprop',ismlist[ismlist.index(ism)+1]]+DefParams
                else:
                    tsink = it_sst[0]
                    Projector = ProjectorList[0]                    
                    DS = DSList[DSList.index(DS)+1]
            else:
                tsink = it_sst[0]
                Projector = ProjectorList[ProjectorList.index(Projector)+1]
        else:
            tsink = it_sst[it_sst.index(tsink)+1]
        return stage,ism,tsink,Projector,DS

def RunNext(icfg,fcfg,stage='twoptprop',ism=ismlist[0],Errored='Complete',tsink=it_sst[0],Projector=ProjectorList[0],DS=DSList[0],Start=False):
    
    icfg,fcfg,ism,tsink,Projector = map(int,[icfg,fcfg,ism,tsink,Projector])
    RemoveCSH(icfg,ism,stage,tsink=tsink,Proj=Projector,DS=DS)
    #removes fort parameter files
    if 'twoptprop' in stage:
        Remove2ptPropFiles(InputFolder,ChromaFileFlag,icfg,[ism])    
    elif 'twoptcorr' in stage:
        Remove2ptCorrFiles(InputFolder,ChromaFileFlag,icfg,[ism])    
    elif 'threeptcorr' in stage:
        Remove3ptCorrFiles(InputFolder,ChromaFileFlag,icfg,[ism],[DS],[Projector],[tsink])    
        

    if Errored == 'Failed':
        print 'Error on config' + icfg
        RemoveProp(icfg,ismlist)
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
        boolcheck = Check2ptCorr(icfg,[ism],jsmlist,twoptinterps[0])
    else:
        boolcheck = Check2ptCorr(icfg,[ism],jsmlist,twoptinterps[0]) and Check3ptCorr(icfg,[ism],it_sst,ProjectorList,DSList)

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
    Move2ptCorr(icfg,[ism],jsmlist,twoptinterps[0])
    prevism = ism
    if not Start: stage,ism,tsink,Projector,DS = IncrementRun(stage,ism,tsink,Projector,DS)
        
    StillInc = True
    while StillInc:
        StillInc = False
        if 'twoptprop' in stage:
            if Check2ptProp(icfg,[ism]):
                stage,ism,tsink,Projector,DS = IncrementRun(stage,ism,tsink,Projector,DS)
                StillInc = True
        elif 'twoptcorr' in stage:
            Move2ptCorr(icfg,[ism],jsmlist,twoptinterps[0])
            if Check2ptCorr(icfg,[ism],jsmlist,twoptinterps[0]):
                stage,ism,tsink,Projector,DS = IncrementRun(stage,ism,tsink,Projector,DS)
                if 'Done' not in stage: StillInc = True
        elif 'threeptcorr' in stage:
            if Check3ptCorr(icfg,[ism],[tsink],[Projector],[DS]):
                stage,ism,tsink,Projector,DS = IncrementRun(stage,ism,tsink,Projector,DS)
                if 'Done' not in stage: StillInc = True
    if prevism != ism:
        RemoveProp(icfg,[prevism])


    if 'twopt' in stage:
        if 'prop' in stage:
            [thisjobid] = Create2ptPropFiles(InputFolder,ChromaFileFlag,icfg,[ism])
        else:
            [thisjobid] = Create2ptCorrFiles(InputFolder,ChromaFileFlag,icfg,[ism])
        if Submit:
            runfile = 'sbatch '+CreateCSHWrap(icfg,fcfg,ism,thisjobid,stage)
        else:
            runfile = CreateCSHWrap(icfg,fcfg,ism,thisjobid,stage)
        print runfile
        subprocess.call([runfile],cwd=basedir)
    elif 'three' in stage:
        [thisjobid] = Create3ptCorrFiles(InputFolder,ChromaFileFlag,icfg,[ism],[DS],[Projector],[tsink])    
        mkdir_p(Get3ptCorrFolder(icfg,ism,tsink,Projector,DS))
        if Submit:
            runfile = 'sbatch '+CreateCSHWrap(icfg,fcfg,ism,thisjobid,stage,tsink=tsink,Proj=Projector,DS=DS)
        else:
            runfile = CreateCSHWrap(icfg,fcfg,ism,thisjobid,stage,tsink=tsink,Proj=Projector,DS=DS)
        print runfile
        subprocess.call([runfile],cwd=basedir)
    elif 'Done' in stage:
        if icfg<fcfg:
            RunNext(icfg+1,fcfg,Start=True)
        else:
            print 'All Complete'
        

if len(sys.argv) > 1 and 'ReSubmit' in sys.argv[0]:
    RunNext(*sys.argv[1:])
    # RunNext(*sys.argv[1:],Start=False)
