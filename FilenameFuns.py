#!/usr/bin/env python 

from RunParams import *


def Get2ptProp(icfg,ism,iPoF=0):
    return qpdir+CreateCfg(icfg,DelLime=True)+'_tsrc'+str(iPoF)+'_sm'+str(ism)+'.prop.lime'

def Get2ptCorr(icfg,ism,jsm,interp,iPoF=0):
    return (cfdir+'twoptsm'+str(ism)+'si'+str(jsm)+'/'+CreateCfg(icfg,DelLime=True)+'_k'+str(kud)+'_tsrc'+str(iPoF)+
            'sm'+str(ism)+'si'+str(jsm)+'_'+interp+'.2cf.xml')

def Get2ptCorrFolders(icfg,ism,thisjsmlist):
    return [(cfdir+'twoptsm'+str(ism)+'si'+str(jsm)+'/') for jsm in thisjsmlist]

def Get2ptCorrOutput(icfg,ism,jsm,interp,iPoF=0):
    return (cfdir+'/'+CreateCfg(icfg,DelLime=True)+'_k'+str(kud)+'_tsrc'+str(iPoF)+'sm'+str(ism)+'si'+str(jsm)+'_'+interp+'.2cf.xml')


def Get3ptCorrFolder(icfg,ism,tsink,Projector,DS):
    thisREvecDir = (REvecFlag+'sm'+str(ism)+'PoF'+str(PoFShifts)+'D'+str(PoFDelta)
                    +'GMA'+str(Projector)+'tsink'+str(tsink)+'p'+''.join(map(str,ppvec))+DS+'/')
    return cf3ptdir+thisREvecDir

def Get3ptCorr(icfg,ism,tsink,Projector,DS,ND,iPoF=0):
    # thisREvecDir = ('sm'+str(ism)+REvecFlag+'PoF'+str(PoFShifts)+'D'+str(PoFDelta)+
    #                 'GMA'+str(Projector)+'tsink'+str(tsink)+'p'+''.join(map(str,ppvec))+DS+'/')
    thisREvecDir = Get3ptCorrFolder(icfg,ism,tsink,Projector,DS)
    return (thisREvecDir+CreateCfg(icfg,DelLime=True)+'_k'+str(kud)+'_tsrc'+str(iPoF)+'sm'+str(ism)+'_'+REvecFlag+'PoF'+str(PoFShifts)+'D'+str(PoFDelta)+
            'GMA'+str(Projector)+'tsink'+str(tsink)+'p'+''.join(map(str,ppvec))+DS+ND+'.3cf.lime')

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
    return (thisCMDir+CreateCfg(icfg,DelLime=True)+'_k'+str(kud)+'_tsrc'+str(iPoF)+'sm'+str(ism)+'_si'+str(jsm)+'GMA'+str(Projector)+
            'tsink'+str(tsink)+'p'+''.join(map(str,ppvec))+DS+ND+'.3cf.lime')


def Get3ptCorrFolderjsmList(icfg,ism):
    outlist = []
    for jsm in jsmlist:
        for it in it_sst:
            for iDS in DSList:
                for iProj in ProjectorList:
                    outlist.append(Get3ptCorrFolderjsm(icfg,ism,jsm,it,iProj,iDS))
    return outlist


