#!/usr/bin/env python 

from RunParams import *
import glob

def GetFlowDir(icfg):
    mkdir_p(flowdirout+'cfg'+str(icfg)+'/')
    return flowdirout+'cfg'+str(icfg)+'/'


def CheckFlowDoneList(icfglist):
    listout = []
    for icfg in icfglist:
        with open(FlowDoneList,'r') as f:
            for lines in f:
                if str(icfg) == lines.replace('\n',''):
                    listout.append(icfg)
    return listout

def CheckFlowDoneListFF(icfglist):
    listout = []
    for icfg in icfglist:
        thisdir = GetFlowDir(icfg.replace('\n',''))
        # print glob.glob(thisdir)
        # print icfg.replace('\n','') , len(glob.glob(thisdir+'*')), 2*(flow_steps+1)
        if len(glob.glob(thisdir+'*')) == 2*(flow_steps+1):
            listout.append(icfg)
    return listout
            
               

def Get2ptProp(icfg,ism,iPoF=0):
    return qpdir+''.join(CreateCfg(icfg,DelLime=True))+'_tsrc'+str(iPoF)+'_sm'+str(ism)+'.prop'

def Get2ptCorr(icfg,ism,jsm,interp,iPoF=0):
    if OutXml:
        fileend = '.xml'
    else:
        fileend = '.lime'
    return (cfdir+'twoptsm'+str(ism)+'si'+str(jsm)+'/'+''.join(CreateCfg(icfg,DelLime=True))+'_k'+str(kud)+'_tsrc'+str(iPoF)+
            'sm'+str(ism)+'si'+str(jsm)+'_'+interp+'.2cf'+fileend)

def Get2ptCorrFolders(icfg,ism,thisjsmlist):
    return [(cfdir+'twoptsm'+str(ism)+'si'+str(jsm)+'/') for jsm in thisjsmlist]

def Get2ptCorrOutput(icfg,ism,jsm,interp,iPoF=0):
    if OutXml:
        fileend = '.xml'
    else:
        fileend = '.lime'
    return (cfdir+'/'+''.join(CreateCfg(icfg,DelLime=True))+'_k'+str(kud)+'_tsrc'+str(iPoF)+'sm'+str(ism)+'si'+str(jsm)+'_'+interp+'.2cf'+fileend)


def Get3ptCorrFolder(icfg,ism,tsink,Projector,DS):
    thisREvecDir = (REvecFlag+'sm'+str(ism)+'PoF'+str(PoFShifts)+'D'+str(PoFDelta)
                    +'GMA'+str(Projector)+'tsink'+str(tsink)+'p'+''.join(map(str,ppvec))+DS+'/')
    return cf3ptdir+thisREvecDir

def Get3ptCorr(icfg,ism,tsink,Projector,DS,ND,iPoF=0):
    # thisREvecDir = ('sm'+str(ism)+REvecFlag+'PoF'+str(PoFShifts)+'D'+str(PoFDelta)+
    #                 'GMA'+str(Projector)+'tsink'+str(tsink)+'p'+''.join(map(str,ppvec))+DS+'/')
    thisREvecDir = Get3ptCorrFolder(icfg,ism,tsink,Projector,DS)
    return (thisREvecDir+''.join(CreateCfg(icfg,DelLime=True))+'_k'+str(kud)+'_tsrc'+str(iPoF)+'sm'+str(ism)+'_'+REvecFlag+'PoF'+str(PoFShifts)+'D'+str(PoFDelta)+
            'GMA'+str(Projector)+'tsink'+str(tsink)+'p'+''.join(map(str,ppvec))+DS+ND+'.3cf')

def Get3ptCorrFolderList(icfg,ism):
    outlist = []
    for it in it_sst:
        for iDS in DSList:
            for iProj in ProjectorList:
                outlist.append(Get3ptCorrFolder(icfg,ism,it,iProj,iDS))
    return outlist
                               

def Get3ptCorrFolderjsm(icfg,ism,jsm,tsink,Projector,DS):
    thisCMDir = 'sm'+str(ism)+'_CMsi'+str(jsm)+'GMA'+str(Projector)+'tsink'+str(tsink)+'p'+''.join(map(str,ppvec))+DS+'/'
    return cf3ptdir+thisCMDir

def Get3ptCorrjsm(icfg,ism,jsm,tsink,Projector,DS,ND,iPoF=0):
    # thisCMDir = 'sm'+str(ism)+'_CMsi'+str(jsm)+'GMA'+str(Projector)+'tsink'+str(tsink)+'p'+''.join(map(str,ppvec))+DS+'/'
    thisCMDir = Get3ptCorrFolderjsm(icfg,ism,jsm,tsink,Projector,DS)
    return (thisCMDir+''.join(CreateCfg(icfg,DelLime=True))+'_k'+str(kud)+'_tsrc'+str(iPoF)+'sm'+str(ism)+'_si'+str(jsm)+'GMA'+str(Projector)+
            'tsink'+str(tsink)+'p'+''.join(map(str,ppvec))+DS+ND+'.3cf')


def Get3ptCorrFolderjsmList(icfg,ism):
    outlist = []
    for jsm in jsmlist:
        for it in it_sst:
            for iDS in DSList:
                for iProj in ProjectorList:
                    outlist.append(Get3ptCorrFolderjsm(icfg,ism,jsm,it,iProj,iDS))
    return outlist


