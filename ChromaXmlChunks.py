#!/usr/bin/env python

from RunParams import *
from FilenameFuns import *
from collections import OrderedDict as OrdDict
from GetAndCheckData import *
import numpy as np

iterlistchunk = iter(range(50000))

def SetupDict():
    outputdict = {'chroma':OrdDict()}
    outputdict['chroma']['Param'] = OrdDict()
    outputdict['chroma']['Param']['InlineMeasurements'] = OrdDict()
    outputdict['chroma']['Param']['nrow'] = nxtstr
    return outputdict

def SetupGaugeDict(thistype):
    outputdict = {thistype:OrdDict()}
    if 'purgaug' in thistype:
        outputdict[thistype] = Add_cfg(1)
        hold = Add_MCControl(GetGaugeField(1).replace('.lime',''))
        outputdict[thistype]['MCControl'] = hold['MCControl']
        hold = Add_HBItr()
        outputdict[thistype]['HBItr'] = hold['HBItr']
    return outputdict
    


def AddToIM(thisdict,elemnum,AddFun,AddParams):
    thisdict['chroma']['Param']['InlineMeasurements']['elem'+str(elemnum)] = AddFun(*AddParams)
    return thisdict

def AlphaToChromaWidth(alpha,nsmear):
    return np.sqrt(2*int(nsmear)*float(alpha)/3)

def Add_SmearingParam(wvf_param,wvfIntPar,no_smear_dir,IsAlpha=True):
    thisdict = OrdDict()
    thisdict['wvf_kind'] = SmKind
    if IsAlpha:
        thisdict['wvf_param'] = AlphaToChromaWidth(float(wvf_param),int(wvfIntPar))
    else:
        thisdict['wvf_param'] = wvf_param
    thisdict['wvfIntPar'] = wvfIntPar
    thisdict['no_smear_dir'] = no_smear_dir
    return thisdict

def Add_Displacement():
    thisdict = OrdDict()
    thisdict['version'] = 1
    thisdict['DisplacementType'] = 'NONE'
    return thisdict

def Add_Weinberg():
    thisdict = OrdDict()
    thisdict['order'] = FlowOrderWein
    thisdict['k'] = kflowWein
    thisdict['calc_Wt'] = 'true'
    return thisdict

def Add_Qtop():
    thisdict = OrdDict()
    thisdict['order'] = FlowOrderQtop
    thisdict['k'] = kflowQtop
    thisdict['calc_Qt'] = 'true'
    return thisdict

def Add_Flow(gauge_id,icfg):
    thisdict = OrdDict()
    thisdict['Name'] = 'FLOW_OPERATORS'
    thisdict['Frequency'] = 1
    thisdict['Param'] = OrdDict()
    thisdict['Param']['file_dir'] = GetFlowDir(icfg)
    thisdict['Param']['wf_nsteps'] = flow_steps
    thisdict['Param']['wf_time'] = totflow_time
    thisdict['Param']['Nt'] = nt
    thisdict['Param']['Weinberg'] = Add_Weinberg()
    thisdict['Param']['Qtop'] = Add_Qtop()
    thisdict['NamedObject'] = OrdDict()
    thisdict['NamedObject']['gauge_id'] = gauge_id
    thisdict['xml_file'] = ''
    return thisdict


def Add_Source(gauge_id,source_id,icfg,sm,iPoF=0):
    thisdict = OrdDict()
    thisdict['Name'] = 'MAKE_SOURCE'
    thisdict['Frequency'] = 1
    thisdict['Param'] = OrdDict()
    thisdict['Param']['version'] = 6
    thisdict['Param']['Source'] = OrdDict()    
    thisdict['Param']['Source']['version'] = 1
    thisdict['Param']['Source']['SourceType'] = SmSourceType
    thisdict['Param']['Source']['j_decay'] = 3
    thisdict['Param']['Source']['t_srce'] = GetSourceString(icfg,iPoF=iPoF)
    # thisdict['Param']['Source']['quark_smear_lastP'] = 'false'
    thisdict['Param']['Source']['SmearingParam'] = Add_SmearingParam(alpha,sm,3)
    thisdict['Param']['Source']['Displacement'] = Add_Displacement()
    thisdict['NamedObject'] = OrdDict()
    thisdict['NamedObject']['gauge_id'] = gauge_id
    thisdict['NamedObject']['source_id'] = source_id
    return thisdict
    


def Add_Sink(gauge_id,prop_id,smeared_prop_id,sm):
    thisdict = OrdDict()
    thisdict['Name'] = 'SINK_SMEAR'
    thisdict['Frequency'] = 1
    thisdict['Param'] = OrdDict()
    thisdict['Param']['version'] = 5
    thisdict['Param']['Sink'] = OrdDict()    
    thisdict['Param']['Sink']['version'] = 2
    thisdict['Param']['Sink']['SinkType'] = SmSinkType
    thisdict['Param']['Sink']['j_decay'] = 3
    thisdict['Param']['Sink']['SmearingParam'] = Add_SmearingParam(alpha,sm,3)
    thisdict['Param']['Sink']['Displacement'] = Add_Displacement()
    thisdict['NamedObject'] = OrdDict()
    thisdict['NamedObject']['gauge_id'] = gauge_id
    thisdict['NamedObject']['prop_id'] = prop_id
    thisdict['NamedObject']['smeared_prop_id'] = smeared_prop_id
    return thisdict


def Add_FermionBC():
    thisdict = OrdDict()
    thisdict['FermBC'] = FermBC
    thisdict['boundary'] = boundstr
    if 'TWISTED' in FermBC:
        thisdict['phases_by_pi'] = phases
        thisdict['phases_dir'] = phasedirs
    return thisdict


def Add_AnisoParam():
    thisdict = OrdDict()
    thisdict['anisoP'] = anisoP
    thisdict['t_dir'] = t_dir
    thisdict['xi_0'] = xi_0
    thisdict['nu'] = GFnu
    return thisdict


def Add_FermState():
    thisdict = OrdDict()
    thisdict['Name'] = 'CLOVER'
    thisdict['n_smear'] = nstout
    thisdict['rho'] = rho
    thisdict['orthog_dir'] = 5
    thisdict['FermionBC'] = Add_FermionBC()
    return thisdict


def Add_FermionAction(kin):
    thisdict = OrdDict()
    thisdict['FermAct'] = FermAct
    thisdict['Kappa'] = '0.'+str(kin)
    thisdict['clovCoeff'] = csw
    thisdict['AnisoParam'] = Add_AnisoParam()
    thisdict['FermionBC'] = Add_FermionBC()
    return thisdict


def Add_CloverParams(kin):
    thisdict = OrdDict()
    thisdict['Kappa'] = '0.'+str(kin)
    thisdict['clovCoeff'] = csw
    return thisdict
    

def Add_InvertParam(kin):
    thisdict = OrdDict()
    thisdict['invType'] = invType
    thisdict['RsdBiCGStab'] = Prec
    thisdict['MaxBiCGStab'] = MaxIter
    thisdict['CloverParams'] = Add_CloverParams(kin)
    thisdict['AntiPeriodicT'] = anti_t
    return thisdict


def Add_Propagator(kin,gauge_id,source_id,prop_id,SeqSource=False):
    thisdict = OrdDict()
    thisdict['Name'] = 'PROPAGATOR'
    thisdict['Frequency'] = 1
    thisdict['Param'] = OrdDict()
    thisdict['Param']['version'] = 10
    # if SeqSource:
    #     thisdict['Param']['quarkSpinType'] = 'UPPER'
    # else:
    thisdict['Param']['quarkSpinType'] = 'FULL'
    thisdict['Param']['obsvP'] = 'false'
    # thisdict['Param']['numRetries'] = 1
    thisdict['Param']['FermionAction'] = Add_FermionAction(kin)
    thisdict['Param']['InvertParam'] = Add_InvertParam(kin)    
    thisdict['NamedObject'] = OrdDict()
    thisdict['NamedObject']['gauge_id'] = gauge_id
    thisdict['NamedObject']['source_id'] = source_id
    thisdict['NamedObject']['prop_id'] = prop_id
    return thisdict
    

def Add_WriteNamedObject(object_id,object_type,file_name,file_volfmt):
    thisdict = OrdDict()
    thisdict['Name'] = 'QIO_WRITE_NAMED_OBJECT'
    thisdict['Frequency'] = 1
    thisdict['NamedObject'] = OrdDict()
    thisdict['NamedObject']['object_id'] = object_id
    thisdict['NamedObject']['object_type'] = object_type
    thisdict['File'] = OrdDict()
    thisdict['File']['file_name'] = file_name
    thisdict['File']['file_volfmt'] = file_volfmt
    return thisdict

def Add_ReadNamedObject(object_id,object_type,file_name):
    thisdict = OrdDict()
    thisdict['Name'] = 'QIO_READ_NAMED_OBJECT'
    thisdict['Frequency'] = 1
    thisdict['NamedObject'] = OrdDict()
    thisdict['NamedObject']['object_id'] = object_id
    thisdict['NamedObject']['object_type'] = object_type
    thisdict['File'] = OrdDict()
    thisdict['File']['file_name'] = file_name
    return thisdict


def Add_EraseNamedObject(object_id):
    thisdict = OrdDict()
    thisdict['Name'] = 'ERASE_NAMED_OBJECT'
    thisdict['NamedObject'] = {'object_id' : object_id}
    return thisdict

def Add_SeqSource(gauge_id,prop_id1,prop_id2,seqsource_id,DS,Proj,Interp,t_sink,sm):
    thisdict = OrdDict()
    thisdict['Name'] = 'SEQSOURCE'
    thisdict['Frequency'] = 1
    thisdict['Param'] = OrdDict()
    thisdict['Param']['version'] = 1
    thisdict['Param']['seq_src'] = GetSmSeqSourceType(Interp,DS,Proj)
    thisdict['Param']['t_sink'] = str(t_sink)
    thisdict['Param']['sink_mom'] = ppstr
    thisdict['PropSink'] = OrdDict()
    thisdict['PropSink']['version'] = 5
    thisdict['PropSink']['Sink'] = OrdDict()    
    thisdict['PropSink']['Sink']['version'] = 2
    thisdict['PropSink']['Sink']['SinkType'] = SmSinkType
    thisdict['PropSink']['Sink']['j_decay'] = 3
    thisdict['PropSink']['Sink']['SmearingParam'] = Add_SmearingParam(alpha,sm,3)
    thisdict['NamedObject'] = OrdDict()
    thisdict['NamedObject']['gauge_id'] = gauge_id
    thisdict['NamedObject']['prop_ids'] = OrdDict()
    if 'sing' in DS: 
        thisdict['NamedObject']['prop_ids']['elem'] = prop_id1
    else:
        thisdict['NamedObject']['prop_ids']['elem1'] = prop_id1
        thisdict['NamedObject']['prop_ids']['elem2'] = prop_id2
    thisdict['NamedObject']['seqsource_id'] = seqsource_id
    return thisdict


def Add_HadSpec(gauge_id,k1_prop_id,k2_prop_id,icfg,ism,jsm,interp,iPoF=0):
    thisdict = OrdDict()
    thisdict['Name'] = 'HADRON_SPECTRUM'
    thisdict['Frequency'] = 1
    thisdict['Param'] = OrdDict()
    thisdict['Param']['version'] = 1
    thisdict['Param']['MesonP'] = 'true'
    thisdict['Param']['CurrentP'] = 'true'
    thisdict['Param']['BaryonP'] = 'true'
    thisdict['Param']['time_rev'] = 'false'    
    thisdict['Param']['mom2_max'] = qmax    
    if AveMom2pt:
        thisdict['Param']['avg_equiv_mom'] = 'true'    
    else:
        thisdict['Param']['avg_equiv_mom'] = 'false'    
    if OutXml:
        thisdict['Param']['xml'] = 'true'
        thisdict['Param']['lime'] = 'false'        
    else:
        thisdict['Param']['xml'] = 'false'
        thisdict['Param']['lime'] = 'true'        
    thisdict['NamedObject'] = OrdDict()
    thisdict['NamedObject']['gauge_id'] = gauge_id
    thisdict['NamedObject']['sink_pairs'] = {'elem':OrdDict()}
    thisdict['NamedObject']['sink_pairs']['elem']['first_id'] = k1_prop_id
    thisdict['NamedObject']['sink_pairs']['elem']['second_id'] = k2_prop_id
    mkdir_p(Get2ptCorrFolders(icfg,ism,[jsm])[0])
    # if OutXml:
    thisdict['xml_file'] = Get2ptCorr(icfg,ism,jsm,interp,iPoF=iPoF)
    # else:
    #     thisdict['lime_file'] = Get2ptCorr(icfg,ism,jsm,interp,iPoF=iPoF).replace('.xml','.lime')
    return thisdict


# def Add_MesSpec(gauge_id,k1_prop_id,k2_prop_id,icfg,ism,jsm,interp):
#     thisdict = OrdDict()
#     thisdict['Name'] = 'MESON_SPECTRUM-QCDSF'
#     thisdict['Frequency'] = 1
#     thisdict['Param'] = OrdDict()
#     thisdict['Param']['version'] = 1
#     thisdict['Param']['fwdbwd_average'] = 'false'
#     thisdict['Param']['time_rev'] = 'false'    
#     thisdict['Param']['mom2_max'] = qmax    
#     thisdict['Param']['avg_equiv_mom'] = 'false'    
#     if XmlOut:
#         thisdict['Param']['xml'] = 'true'
#     else:
#         thisdict['Param']['xml'] = 'false'
#     thisdict['Param']['lime'] = 'true'        
#     thisdict['NamedObject'] = OrdDict()
#     thisdict['NamedObject']['gauge_id'] = gauge_id
#     thisdict['NamedObject']['sink_pairs'] = {'elem':OrdDict()}
#     thisdict['NamedObject']['sink_pairs']['elem']['first_id'] = k1_prop_id
#     thisdict['NamedObject']['sink_pairs']['elem']['second_id'] = k2_prop_id
#     thisdict['lime_file'] = Get2ptCorr(icfg,ism,jsm,interp)
#     thisdict['xml_file'] = Get2ptCorr(icfg,ism,jsm,interp).replace('.lime','.xml')
#     return thisdict


def Add_Bar3ptTieUp(gauge_id,prop_id,seqprop_id,icfg,ism,tsink,Proj,DS,iPoF=0):
    thisdict = OrdDict()
    thisdict['Name'] = 'BAR3PTFN'
    thisdict['Frequency'] = 1
    thisdict['Param'] = OrdDict()
    thisdict['Param']['version'] = 7
    thisdict['Param']['j_decay'] = 3    
    thisdict['Param']['mom2_max'] = qmax    
    thisdict['Param']['deriv'] = NDer
    thisdict['NamedObject'] = OrdDict()
    thisdict['NamedObject']['gauge_id'] = gauge_id
    thisdict['NamedObject']['prop_id'] = prop_id
    thisdict['NamedObject']['bar3ptfn_file'] = Get3ptCorr(icfg,ism,tsink,Proj,DS,'NDer0',iPoF=iPoF)
    if NDer > 0:
        for iDer in range(1,NDer+1):
            thisdict['NamedObject']['bar3ptfn_'+str(iDer)+'D_file'] = Get3ptCorr(icfg,ism,tsink,Proj,DS,'NDer'+str(iDer),iPoF=iPoF)
    # thisdict['NamedObject']['bar3ptfn_2D_file'] = Get3ptCorr(icfg,ism,tsink,Proj,DS,'NDer2',iPoF=iPoF)
    thisdict['NamedObject']['seqprops'] = {'elem':OrdDict()}
    thisdict['NamedObject']['seqprops']['elem']['seqprop_id'] = seqprop_id
    thisdict['NamedObject']['seqprops']['elem']['gamma_insertion'] = 0
    return thisdict

def Add_Bar3ptTieUpjsm(gauge_id,prop_id,seqprop_id,icfg,ism,jsm,tsink,Proj,DS,iPoF=0):
    thisdict = OrdDict()
    thisdict['Name'] = 'BAR3PTFN'
    thisdict['Frequency'] = 1
    thisdict['Param'] = OrdDict()
    thisdict['Param']['version'] = 7
    thisdict['Param']['j_decay'] = 3    
    thisdict['Param']['mom2_max'] = qmax    
    thisdict['Param']['deriv'] = NDer
    thisdict['NamedObject'] = OrdDict()
    thisdict['NamedObject']['gauge_id'] = gauge_id
    thisdict['NamedObject']['prop_id'] = prop_id
    thisdict['NamedObject']['bar3ptfn_file'] = Get3ptCorrjsm(icfg,ism,jsm,tsink,Proj,DS,'NDer0',iPoF=iPoF)
    if NDer > 0:
        for iDer in range(1,NDer):
            thisdict['NamedObject']['bar3ptfn_'+str(iDer)+'D_file'] = Get3ptCorrjsm(icfg,ism,jsm,tsink,Proj,DS,'NDer'+str(iDer),iPoF=iPoF)
    # thisdict['NamedObject']['bar3ptfn_2D_file'] = Get3ptCorr(icfg,ism,jsm,tsink,Proj,DS,'NDer2')
    thisdict['NamedObject']['seqprops'] = {'elem':OrdDict()}
    thisdict['NamedObject']['seqprops']['elem']['seqprop_id'] = seqprop_id
    thisdict['NamedObject']['seqprops']['elem']['gamma_insertion'] = 0
    return thisdict


def Add_RMS(gauge_id,source_id):
    thisdict = OrdDict()
    thisdict['Name'] = 'RMS'
    thisdict['Frequency'] = 1
    thisdict['Param'] = OrdDict()
    thisdict['Param']['version'] = 1
    thisdict['Param']['psi_wfn'] = 'true'    
    thisdict['Param']['psi_dag_psi_wfn'] = 'true'    
    thisdict['NamedObject'] = OrdDict()
    thisdict['NamedObject']['gauge_id'] = gauge_id
    thisdict['NamedObject']['source_id'] = source_id
    return thisdict

def Add_qPropAdd(propA,propB,factorA,factorB,propApB):
    thisdict = OrdDict()
    thisdict['Name'] = 'QPROPADD'
    thisdict['Frequency'] = 1
    thisdict['NamedObject'] = OrdDict()
    thisdict['NamedObject']['propA'] = propA
    thisdict['NamedObject']['propB'] = propB
    thisdict['NamedObject']['factorA'] = factorA
    thisdict['NamedObject']['factorB'] = factorB
    thisdict['NamedObject']['propApB'] = propApB
    return thisdict


def Add_RNG():
    thisdict = OrdDict()
    thisdict['RNG'] = OrdDict()
    thisdict['RNG']['Seed'] = OrdDict()
    thisdict['RNG']['Seed']['elem1'] = Seed1
    thisdict['RNG']['Seed']['elem2'] = Seed2
    thisdict['RNG']['Seed']['elem3'] = Seed3
    thisdict['RNG']['Seed']['elem4'] = Seed4
    return thisdict

def Add_cfg(icfg,Flow=False):
    thisdict = OrdDict()
    thisdict['Cfg'] = OrdDict()
    thisdict['Cfg']['cfg_type'] = GFFormat
    # if GFFormat == 'UNIT' or 'WEAK' in GFFormat:
    #     thisdict['Cfg']['cfg_file'] = 'dummy'
    # else:
    #     thisdict['Cfg']['cfg_file'] = GetGaugeField(icfg)
    if GFFormat == 'UNIT' :
        thisdict['Cfg']['cfg_file'] = 'dummy'
    else:
        thisdict['Cfg']['cfg_file'] = GetGaugeField(icfg,Flow=Flow)
    thisdict['Cfg']['parallel_io'] = ParaIO
    return thisdict



def Add_CoulombGF(gauge_id,gfix_id,grot_id):
    thisdict = OrdDict()
    thisdict['Name'] = 'COULOMB_GAUGEFIX'
    thisdict['Frequency'] = 1
    thisdict['Param'] = OrdDict()
    thisdict['Param']['version'] = 1
    thisdict['Param']['GFAccu'] = GFPrec  
    thisdict['Param']['GFMax'] = GFMaxIter    
    thisdict['Param']['OrDo'] = GFDoOr
    thisdict['Param']['OrPara'] = GFOrPara
    thisdict['Param']['j_decay'] = 3
    thisdict['NamedObject'] = OrdDict()
    thisdict['NamedObject']['gauge_id'] = gauge_id
    thisdict['NamedObject']['gfix_id'] = gfix_id
    thisdict['NamedObject']['gauge_rot_id'] = grot_id
    return thisdict



def Add_MCControl(Pref):
    thisdict = OrdDict()
    thisdict['MCControl'] = Add_RNG()
    thisdict['MCControl']['StartUpdateNum']= StartUpdateNum
    thisdict['MCControl']['NWarmUpUpdates']= NWarmUpUpdates
    thisdict['MCControl']['NProductionUpdates']= NProductionUpdates
    thisdict['MCControl']['NUpdatesThisRun']= NUpdatesThisRun
    thisdict['MCControl']['SaveInterval']= SaveInterval
    thisdict['MCControl']['SavePrefix']= Pref
    thisdict['MCControl']['SaveVolfmt']= 'SINGLEFILE'
    return thisdict

def Add_HBItr():
    thisdict = OrdDict()
    thisdict['HBItr'] = OrdDict()
    thisdict['HBItr']['GaugeAction'] = OrdDict()
    thisdict['HBItr']['GaugeAction']['Name'] = GActName
    thisdict['HBItr']['GaugeAction']['beta'] = beta
    thisdict['HBItr']['GaugeAction']['AnisoParam'] = OrdDict()
    thisdict['HBItr']['GaugeAction']['AnisoParam']['anisoP'] = anisoP
    thisdict['HBItr']['GaugeAction']['AnisoParam']['t_dir'] = t_dir
    thisdict['HBItr']['GaugeAction']['AnisoParam']['xi_0'] = xi_0
    thisdict['HBItr']['GaugeAction']['AnisoParam']['nu'] = GFnu
    thisdict['HBItr']['GaugeAction']['GaugeState'] = OrdDict()
    thisdict['HBItr']['GaugeAction']['GaugeState']['Name'] = 'SIMPLE_GAUGE_STATE'
    thisdict['HBItr']['GaugeAction']['GaugeState']['GaugeBC'] = {'Name':GaugeBC}
    thisdict['HBItr']['HBParams'] = OrdDict()
    thisdict['HBItr']['HBParams']['nOver'] = nOver
    thisdict['HBItr']['HBParams']['NmaxHB'] = NmaxHB
    thisdict['HBItr']['nrow'] = nxtstr
    return thisdict
    
    
    
    
    
    
    
    


