#!/usr/bin/env python 

from RunParams import *

def Get2ptProp(icfg,ism):
    return qpdir+CreateCfg(icfg)+'_k'+str(kud)+'_tsrc'+str(it)+'sm'+str(ism)+'.prop.lime'

def Get2ptCorr(icfg,ism,jsm,interp):
    return (cfdir+'twoptsm'+str(ism)+'si'+str(jsm)+'/'+CreateCfg(icfg)+'_k'+str(kud)+'_tsrc'+str(it)+'sm'+str(ism)+'si'+str(jsm)+'_'+interp+'.2cf.lime')

def Get2ptCorrFolders(icfg,ism,thisjsmlist):
    return [(cfdir+'twoptsm'+str(ism)+'si'+str(jsm)+'/') for jsm in thisjsmlist]

def Get2ptCorrOutput(icfg,ism,jsm,interp):
    return (cfdir+'/'+CreateCfg(icfg)+'_k'+str(kud)+'_tsrc'+str(it)+'sm'+str(ism)+'si'+str(jsm)+'_'+interp+'.2cf.lime')

def Get3ptCorr(icfg,ism,tsink,Projector,DS,ND):
    thisREvecDir = REvecFlag+'sm'+str(ism)+'_'+REvecFlag+'nD'+str(PoFShifts)+'GMA'+str(Projector)+'tsink'+str(tsink)+'p'+''.join(map(str,ppvec))+DS+'/'
    return (cf3ptdir+thisREvecDir+CreateCfg(icfg)+'_k'+str(kud)+'_tsrc'+str(it)+'sm'+str(ism)+'_'+REvecFlag+'nD'+str(PoFShifts)+'GMA'+str(Projector)+
            'tsink'+str(tsink)+'p'+''.join(map(str,ppvec))+DS+ND+'.3cf.lime')

def Get3ptCorrFolder(icfg,ism,tsink,Projector,DS):
    thisREvecDir = REvecFlag+'sm'+str(ism)+'_'+REvecFlag+'nD'+str(PoFShifts)+'GMA'+str(Projector)+'tsink'+str(tsink)+'p'+''.join(map(str,ppvec))+DS+'/'
    return cf3ptdir+thisREvecDir


def Get3ptCorrjsm(icfg,ism,jsm,tsink,Projector,DS,ND):
    thisCMDir = 'CMsm'+str(ism)+'_si'+str(jsm)+'GMA'+str(Projector)+'tsink'+str(tsink)+'p'+''.join(map(str,ppvec))+DS+'/'
    return (cf3ptdir+thisCMDir+CreateCfg(icfg)+'_k'+str(kud)+'_tsrc'+str(it)+'sm'+str(ism)+'_si'+str(jsm)+'GMA'+str(Projector)+
            'tsink'+str(tsink)+'p'+''.join(map(str,ppvec))+DS+ND+'.3cf.lime')

def Get3ptCorrFolderjsm(icfg,ism,jsm,tsink,Projector,DS):
    thisCMDir = 'CMsm'+str(ism)+'_si'+str(jsm)+'GMA'+str(Projector)+'tsink'+str(tsink)+'p'+''.join(map(str,ppvec))+DS+'/'
    return cf3ptdir+thisCMDir


