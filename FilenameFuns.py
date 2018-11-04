#!/usr/bin/env python

from MiscFuns import mkdir_p
from RunParams import flowdirout,FlowDoneList,data_flowdirout
from RunParams import flow_steps,qpdir,CreateCfg,OutXml,Do_Wflow,Do_Qflow,Do_Eflow
from RunParams import cfdir,kud,REvecFlag,PoFShifts,PoFDelta
from RunParams import ppvec,cf3ptdir,it_sst,DSList,ProjectorList
from RunParams import jsmlist
import numpy as np
import os
import glob

def GetFlowDir(icfg):
    mkdir_p(flowdirout+'cfg'+str(icfg)+'/')
    return flowdirout+'cfg'+str(icfg)+'/'

def GetFlowDataDir(icfg):
    mkdir_p(data_flowdirout+'cfg'+str(icfg)+'/')
    return data_flowdirout+'cfg'+str(icfg)+'/'


def CheckFlowDoneList(icfglist):
    if os.path.isfile(FlowDoneList):
        filecfglist = np.loadtxt(FlowDoneList,dtype=str)
        listout = []
        for icfg in icfglist:
            if icfg.replace('\n','') not in filecfglist:
                listout.append(icfg)
        return listout
    else:
        return icfglist


def CheckFlowDoneListFF(icfglist):
    listout = []
    print 'List of directories with missing results:'
    for icfg in icfglist:
        thisicfg = icfg.replace('\n','')
        thisdir = GetFlowDir(thisicfg)
        this_data_dir = GetFlowDataDir(thisicfg)
        # print 'DEBUG'
        # print 'checking',(flow_steps+1)
        # print len(glob.glob(thisdir+'_Wt_t*'))
        # print len(glob.glob(this_data_dir+'_Wt_t*'))
        # print len(glob.glob(thisdir+'_Qt_t*'))
        # print len(glob.glob(this_data_dir+'_Qt_t*'))
        len_Wt = len(glob.glob(thisdir+'_Wt_t*'))
        len_Wt_data = len(glob.glob(this_data_dir+'_Wt_t*'))
        len_Qt = len(glob.glob(thisdir+'_Qt_t*'))
        len_Qt_data = len(glob.glob(this_data_dir+'_Qt_t*'))
        len_Et = len(glob.glob(thisdir+'_Et_t*'))
        len_Et_data = len(glob.glob(this_data_dir+'_Et_t*'))
        w_bool,q_bool,e_bool = False,False,False
        if Do_Wflow == 'true':
            w_bool_new = not os.path.isfile(this_data_dir+'_Wt') and not os.path.isfile(thisdir+'_Wt')
            w_bool = not (len_Wt >= (flow_steps+1) or len_Wt_data >= (flow_steps+1)) \
                        and w_bool_new
        if Do_Qflow == 'true':
            q_bool_new = os.path.isfile(this_data_dir+'_Qt') and not os.path.isfile(thisdir+'_Qt')
            q_bool = not (len_Qt >= (flow_steps+1) or len_Qt_data >= (flow_steps+1)) \
                        and q_bool_new
        if Do_Eflow == 'true':
            e_bool_new = os.path.isfile(this_data_dir+'_Et') and not os.path.isfile(thisdir+'_Et')
            e_bool = not (len_Et >= (flow_steps+1) or len_Et_data >= (flow_steps+1)) \
                        and e_bool_new
        # print glob.glob(thisdir)
        # print icfg.replace('\n','') , len(glob.glob(thisdir+'*')), 2*(flow_steps+1)
        # print 'w_bool',w_bool,'q_bool',q_bool,'e_bool',e_bool
        if w_bool or q_bool or e_bool:
        # if len(glob.glob(thisdir+'*')) == 6:
            print this_data_dir
            print thisdir
            print
            listout.append(thisicfg)
    print 'Total missing=' ,len(listout)
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
