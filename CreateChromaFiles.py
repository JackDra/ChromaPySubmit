#!/usr/bin/env python

from RunParams import GaugeType,ismlist,PoFList,kud,Save2ptProp
from RunParams import SaveMem,jsmlist,twoptinterps,DSList,ProjectorList
from RunParams import it_sst,GetSourceString,RVec,ModuloT,flow_fermions
from ChromaXmlChunks import SetupGaugeDict,SetupDict
from ChromaXmlChunks import AddToIM,Add_Flow,Add_RNG,Add_cfg
from ChromaXmlChunks import Add_Source,Add_Propagator,Add_ReadNamedObject
from ChromaXmlChunks import Add_EraseNamedObject,Add_Sink,Add_HadSpec
from ChromaXmlChunks import Add_SeqSource,Add_qPropAdd,Add_Bar3ptTieUp
from ChromaXmlChunks import Add_Bar3ptTieUpjsm
from FilenameFuns import Get2ptProp

import os
# from collections import OrderedDict as OrdDict
from MiscFuns import Elongate,WriteChromaXml,mkdir_p
import shutil

iterlist = iter(range(10**7))

def Chromaqlist(Minqsqrd,Maxqsqrd):
    qlist = []
    for iq1 in range(-Maxqsqrd,Maxqsqrd+1):
        for iq2 in range(-Maxqsqrd,Maxqsqrd+1):
            for iq3 in range(-Maxqsqrd,Maxqsqrd+1):
                if iq1**2 + iq2**2 + iq3**2 > Maxqsqrd: continue
                if iq1**2 + iq2**2 + iq3**2 < Minqsqrd: continue
                qlist.append(str(iq1) + ' ' + str(iq2) + ' ' + str(iq3))
    return qlist


def RemoveGaugeFieldFiles(folder):
    thisfolder = folder+'/gfield'
    if os.path.isfile(thisfolder):shutil.rmtree(thisfolder)



def CreateGaugeFieldFiles(folder,fileprefix):
    mkdir_p(folder+'/gfield/')
    mkdir_p(folder.replace('Input','Output')+'/gfield/')
    thisfile = folder+'/gfield/'+fileprefix
    if os.path.isfile(thisfile):os.remove(thisfile)
    filelist = [thisfile.replace(folder+'/','')+'.xml']
    DictOut = SetupGaugeDict(GaugeType)

    # DictOut = AddToIM(DictOut,iterlist.next(),Add_CoulombGF,['default_gauge_field','gfix_id','grot_id'])
    # DictOut = AddToIM(DictOut,iterlist.next(),Add_WriteNamedObject,['default_gauge_field','Multi1dLatticeColorMatrixD',GetGaugeField(icfg),'SINGLEFILE'])
    # DictOut = AddToIM(DictOut,iterlist.next(),Add_WriteNamedObject,['gfix_id','Multi1dLatticeColorMatrix',GetGaugeField(icfg).replace('.lime','_gfix.lime'),'SINGLEFILE'])
    # DictOut = AddToIM(DictOut,iterlist.next(),Add_WriteNamedObject,['grot_id','Multi1dLatticeColorMatrix',GetGaugeField(icfg).replace('.lime','_grot.lime'),'SINGLEFILE'])
    # DictOut['chroma']['RNG'] = Add_RNG()['RNG']
    # DictOut['chroma']['Cfg'] = Add_cfg(icfg)['Cfg']
    WriteChromaXml(thisfile,DictOut)
    return filelist


def RemoveFlowFiles(folder):
    thisfolder = folder+'/flow'
    if os.path.isdir(thisfolder):shutil.rmtree(thisfolder)



def CreateFlowFilesWrap(folder,fileprefix,cfgindicies):
    filelist = []
    for thecfg in cfgindicies:
        filelist += CreateFlowFiles(folder,fileprefix,thecfg)
    return filelist

def CreateFlowFiles(folder,fileprefix,icfg):
    filelist = []
    mkdir_p(folder+'/flow/')
    mkdir_p(folder.replace('Input','Output')+'/flow/')
    thisfile = folder+'/flow/'+fileprefix+str(icfg)
    filelist.append(thisfile.replace(folder+'/','')+'.xml')
    DictOut = SetupDict()
    if flow_fermions:
        thisprop = 'prop_to_flow'
        DictOut = AddToIM(DictOut,iterlist.next(),Add_Source,['default_gauge_field','default_source',icfg,'0','0','NONE'])
        DictOut = AddToIM(DictOut,iterlist.next(),Add_Propagator,[kud,'default_gauge_field','default_source',thisprop])
        if SaveMem: DictOut = AddToIM(DictOut,iterlist.next(),Add_EraseNamedObject,['default_source'])
        DictOut = AddToIM(DictOut,iterlist.next(),Add_Flow,['default_gauge_field',icfg,thisprop])
    else:
        DictOut = AddToIM(DictOut,iterlist.next(),Add_Flow,['default_gauge_field',icfg])        
    DictOut['chroma']['RNG'] = Add_RNG()['RNG']
    DictOut['chroma']['Cfg'] = Add_cfg(icfg,Flow=True)['Cfg']
    WriteChromaXml(thisfile,DictOut)
    return filelist


# def Remove2ptPropFiles(folder,fileprefix,icfg,thisismlist):
#     for ism in map(str,thisismlist):
#         thisfile = folder+'/prop2pt'+ism+'/'+fileprefix+str(icfg)
#         if os.path.isfile(thisfile+'.xml'):os.remove(thisfile+'.xml')

# def Create2ptPropFiles(folder,fileprefix,icfg,thisismlist):
#     filelistsm = []
#     for ism in map(str,thisismlist):
#         nism = ism.replace('sm','')
#         mkdir_p(folder+'/prop2pt'+ism+'/')
#         mkdir_p(folder.replace('Input','Output')+'/prop2pt'+ism+'/')
#         thisfile = folder+'/prop2pt'+ism+'/'+fileprefix+str(icfg)
#         if os.path.isfile(thisfile):os.remove(thisfile)
#         filelistsm.append(thisfile.replace(folder+'/','')+'.xml')
#         DictOut = SetupDict()
#         for iPoF in PoFList:
#             DictOut = AddToIM(DictOut,iterlist.next(),Add_Source,['default_gauge_field','default_source'+str(iPoF),icfg,nism,iPoF])
#             DictOut = AddToIM(DictOut,iterlist.next(),Add_Propagator,[kud,'default_gauge_field','default_source'+str(iPoF),'k_prop'+str(iPoF)])
#             DictOut = AddToIM(DictOut,iterlist.next(),Add_WriteNamedObject,['k_prop'+str(iPoF),'LatticePropagator',Get2ptProp(icfg,ism,iPoF=iPoF),'SINGLEFILE'])
#             if iPoF != PoFList[-1]:
#                 DictOut = AddToIM(DictOut,iterlist.next(),Add_EraseNamedObject,['k_prop'+str(iPoF)])
#                 DictOut = AddToIM(DictOut,iterlist.next(),Add_EraseNamedObject,['default_source'+str(iPoF)])
#         DictOut['chroma']['RNG'] = Add_RNG()['RNG']
#         DictOut['chroma']['Cfg'] = Add_cfg(icfg)['Cfg']
#         WriteChromaXml(thisfile,DictOut)
#     return filelistsm


def Remove2ptCorrFiles(folder):
    thisfolder = folder+'/corr2pt'
    if os.path.isdir(thisfolder):shutil.rmtree(thisfolder)



def Create2ptCorrWrap(folder,fileprefix,cfgindicies):
    filelist = []
    for thecfg in cfgindicies:
        filelist += Create2ptCorrFiles(folder,fileprefix,thecfg,ismlist)
    return filelist

def Create2ptCorrFiles(folder,fileprefix,icfg,thisismlist):
    filelistsm = []
    mkdir_p(folder+'/corr2pt/')
    mkdir_p(folder.replace('Input','Output')+'/corr2pt/')
    thisfile = folder+'/corr2pt/'+fileprefix+str(icfg)
    filelistsm.append(thisfile.replace(folder+'/','')+'.xml')
    DictOut = SetupDict()
    for ism in map(str,thisismlist):
        nism = ism.replace('sm','')
        for iPoF in map(str,PoFList):
            thisprop = 'prop_id_sm'+ism+'_PoF'+iPoF
            DictOut = AddToIM(DictOut,iterlist.next(),Add_Source,['default_gauge_field','default_source'+str(iPoF),icfg,nism,iPoF])
            DictOut = AddToIM(DictOut,iterlist.next(),Add_Propagator,[kud,'default_gauge_field','default_source'+str(iPoF),thisprop])
            if Save2ptProp: DictOut = AddToIM(DictOut,iterlist.next(),Add_ReadNamedObject,[thisprop,'LatticePropagator',Get2ptProp(icfg,ism,iPoF=iPoF)])
            if SaveMem: DictOut = AddToIM(DictOut,iterlist.next(),Add_EraseNamedObject,['default_source'+str(iPoF)])
            for jsm in map(str,jsmlist):
                thissiprop = 'prop_id_sm'+ism+'_si'+jsm+'_PoF'+iPoF
                DictOut = AddToIM(DictOut,iterlist.next(),Add_Sink,['default_gauge_field',thisprop,thissiprop,jsm])
                DictOut = AddToIM(DictOut,iterlist.next(),Add_HadSpec,['default_gauge_field',thissiprop,thissiprop,icfg,ism,jsm,twoptinterps[0],iPoF])
                if SaveMem: DictOut = AddToIM(DictOut,iterlist.next(),Add_EraseNamedObject,[thissiprop])
            if iPoF != PoFList[-1] and SaveMem: DictOut = AddToIM(DictOut,iterlist.next(),Add_EraseNamedObject,[thisprop])
    DictOut['chroma']['RNG'] = Add_RNG()['RNG']
    DictOut['chroma']['Cfg'] = Add_cfg(icfg)['Cfg']
    WriteChromaXml(thisfile,DictOut)
    return filelistsm


def Remove3ptCorrFiles(folder):
    thisfolder = folder+'/corr3pt'
    if os.path.isdir(thisfolder):shutil.rmtree(thisfolder)


def Create3ptCorrWrap(folder,fileprefix,cfgindicies):
    filelist = []
    for thecfg in cfgindicies:
        filelist += Create3ptCorrFiles(folder,fileprefix,thecfg,ismlist)
    return filelist


def Create3ptCorrFiles(folder,fileprefix,icfg,thisismlist):
    filelistsm = []
    thisfolder = folder+'/corr3pt/'
    mkdir_p(thisfolder)
    mkdir_p(thisfolder.replace('Input','Output'))
    thisfile = thisfolder+fileprefix+str(icfg)
    filelistsm.append(thisfile.replace(folder+'/','')+'.xml')
    DictOut = SetupDict()
    for ism in map(str,thisismlist):
        nism = ism.replace('sm','')
        for srcPoF in PoFList:
            thisprop = 'prop_id_sm'+ism+'_srcPoF'+str(srcPoF)
            ## Read 2pt prop in
            if Save2ptProp:
                DictOut = AddToIM(DictOut,iterlist.next(),Add_ReadNamedObject,[thisprop,'LatticePropagator',Get2ptProp(icfg,ism,iPoF=srcPoF)])
            else:
                DictOut = AddToIM(DictOut,iterlist.next(),Add_Source,['default_gauge_field','default_source'+str(srcPoF),icfg,nism,srcPoF])
                DictOut = AddToIM(DictOut,iterlist.next(),Add_Propagator,[kud,'default_gauge_field','default_source'+str(srcPoF),thisprop])
                if SaveMem: DictOut = AddToIM(DictOut,iterlist.next(),Add_EraseNamedObject,['default_source'+str(srcPoF)])
            for DS in DSList:
                for Projector in map(str,ProjectorList):
                    for iTS in map(str,it_sst):
                        PoFjsmlist = Elongate(PoFList,map(str,jsmlist))
                        totseqsourcelist = ['seqsource_id_sm'+ism+'_srcPoF'+str(srcPoF)+DS+'_Proj'+Projector+'_tsink'+iTS
                                            +'_PoF'+str(i) for i in range(len(PoFjsmlist))]
                        totseqprop = 'seqprop_id_sm'+ism+'_srcPoF'+str(srcPoF)+DS+'_Proj'+Projector+'_tsink'+iTS


                        for njsm,(iPoF,jsm) in enumerate(PoFjsmlist):
                            corr_tsink = str(ModuloT(int(iTS)+ int(iPoF)+ int(GetSourceString(icfg,iPoF=srcPoF).split()[-1])))
                            # thissiprop = 'prop_id_sm'+ism+'_srcPoF'+str(srcPoF)+'_si'+jsm+'_PoF'+str(iPoF)
                            if njsm == 0:
                                thisseqsource = totseqsourcelist[0]
                            else:
                                thisseqsource = 'seqsource_id_sm'+ism+'_srcPoF'+str(srcPoF)+'_si'+jsm+'_PoF'+str(iPoF)+DS+'_Proj'+Projector+'_tsink'+iTS
                            # ## smear sink
                            # DictOut = AddToIM(DictOut,iterlist.next(),Add_Sink,['default_gauge_field',thisprop,thissiprop,jsm])

                            ## create seq source
                            DictOut = AddToIM(DictOut,iterlist.next(),Add_SeqSource,['default_gauge_field',thisprop,thisprop,thisseqsource,
                                                                       DS,Projector,twoptinterps[0],corr_tsink,jsm])

                            # ## delete sink smeared 2pt source
                            # DictOut = AddToIM(DictOut,iterlist.next(),Add_EraseNamedObject,[thissiprop])

                            ## add to previous seq source with weightings
                            if njsm == 1:
                                DictOut = AddToIM(DictOut,iterlist.next(),Add_qPropAdd,[totseqsourcelist[0],thisseqsource,RVec[0],RVec[1],totseqsourcelist[1]])
                                ## delete sink smeared 2pt source
                                DictOut = AddToIM(DictOut,iterlist.next(),Add_EraseNamedObject,[thisseqsource])
                                ## delete sink smeared 2pt source
                                DictOut = AddToIM(DictOut,iterlist.next(),Add_EraseNamedObject,[totseqsourcelist[0]])
                            elif njsm > 1:
                                DictOut = AddToIM(DictOut,iterlist.next(),Add_qPropAdd,[totseqsourcelist[njsm-1],thisseqsource,1.0,RVec[njsm],
                                                                                        totseqsourcelist[njsm]])
                                ## delete sink smeared 2pt source
                                DictOut = AddToIM(DictOut,iterlist.next(),Add_EraseNamedObject,[thisseqsource])
                                ## delete sink smeared 2pt source
                                DictOut = AddToIM(DictOut,iterlist.next(),Add_EraseNamedObject,[totseqsourcelist[njsm-1]])


                        ## create FS prop
                        DictOut = AddToIM(DictOut,iterlist.next(),Add_Propagator,[kud,'default_gauge_field',totseqsourcelist[-1],totseqprop,True])


                        ## delete total sink smeared 2pt source
                        DictOut = AddToIM(DictOut,iterlist.next(),Add_EraseNamedObject,[totseqsourcelist[-1]])

                        ## Tie up FS prop to make 3pt corr
                        DictOut = AddToIM(DictOut,iterlist.next(),Add_Bar3ptTieUp, ['default_gauge_field',thisprop,totseqprop,icfg,ism,iTS,Projector,DS,srcPoF])

                        ## delete total sequential source propagator
                        DictOut = AddToIM(DictOut,iterlist.next(),Add_EraseNamedObject,[totseqprop])

    DictOut['chroma']['RNG'] = Add_RNG()['RNG']
    DictOut['chroma']['Cfg'] = Add_cfg(icfg)['Cfg']
    WriteChromaXml(thisfile,DictOut)
    return filelistsm



def Create3ptCorrWrapjsm(folder,fileprefix,icfg,fcfg):
    filelist = []
    for thecfg in range(icfg,fcfg+1):
        filelist += Create3ptCorrFilesjsm(folder,fileprefix,thecfg,ismlist)
    return filelist

def Create3ptCorrFilesjsm(folder,fileprefix,icfg,thisismlist):
    filelistsm = []
    thisfolder = folder+'/corr3pt/'
    mkdir_p(thisfolder)
    mkdir_p(thisfolder.replace('Input','Output'))
    thisfile = thisfolder+fileprefix+str(icfg)
    filelistsm.append(thisfile.replace(folder+'/','')+'.xml')
    DictOut = SetupDict()
    for ism in map(str,thisismlist):
        nism = ism.replace('sm','')
        for srcPoF in PoFList:
            thisprop = 'prop_id_sm'+ism+'_srcPoF'+str(srcPoF)
            ## Read 2pt prop in
            if Save2ptProp:
                DictOut = AddToIM(DictOut,iterlist.next(),Add_ReadNamedObject,[thisprop,'LatticePropagator',Get2ptProp(icfg,ism,iPoF=srcPoF)])
            else:
                DictOut = AddToIM(DictOut,iterlist.next(),Add_Source,['default_gauge_field','default_source'+str(srcPoF),icfg,nism,srcPoF])
                DictOut = AddToIM(DictOut,iterlist.next(),Add_Propagator,[kud,'default_gauge_field','default_source'+str(srcPoF),thisprop])
                if SaveMem: DictOut = AddToIM(DictOut,iterlist.next(),Add_EraseNamedObject,['default_source'+str(srcPoF)])
            for jsm in map(str,jsmlist):
                for DS in DSList:
                    for Projector in map(str,ProjectorList):
                        for iTS in map(str,it_sst):
                            corr_tsink = str(ModuloT(int(iTS) + int(GetSourceString(icfg,iPoF=srcPoF).split()[-1])))

                            # thissiprop = 'prop_id_sm'+ism+'_srcPoF'+str(srcPoF)+'_si'+jsm
                            thisseqsource = 'seqsource_id_sm'+ism+'_srcPoF'+str(srcPoF)+'_si'+jsm+DS+'_Proj'+Projector+'_tsink'+iTS
                            thisseqprop = 'seqprop_id_sm'+ism+'_srcPoF'+str(srcPoF)+'_si'+jsm+DS+'_Proj'+Projector+'_tsink'+iTS

                            # ## smear sink
                            # DictOut = AddToIM(DictOut,iterlist.next(),Add_Sink,['default_gauge_field',thisprop,thissiprop,jsm])

                            ## create seq source
                            DictOut = AddToIM(DictOut,iterlist.next(),Add_SeqSource,['default_gauge_field',thisprop,thisprop,thisseqsource,
                                                                                     DS,Projector,twoptinterps[0],corr_tsink,jsm])

                            # ## delete sink smeared 2pt propagator
                            # DictOut = AddToIM(DictOut,iterlist.next(),Add_EraseNamedObject,[thissiprop])

                            ## create FS prop
                            DictOut = AddToIM(DictOut,iterlist.next(),Add_Propagator,[kud,'default_gauge_field',thisseqsource,thisseqprop,True])

                            ## delete seq source
                            DictOut = AddToIM(DictOut,iterlist.next(),Add_EraseNamedObject,[thisseqsource])

                            ## Tie up FS prop to make 3pt corr
                            DictOut = AddToIM(DictOut,iterlist.next(),Add_Bar3ptTieUpjsm, ['default_gauge_field',thisprop,thisseqprop,icfg,ism,jsm,
                                                                                           iTS,Projector,DS,srcPoF])

                            ## delete total sequential source propagator
                            DictOut = AddToIM(DictOut,iterlist.next(),Add_EraseNamedObject,[thisseqprop])


    DictOut['chroma']['RNG'] = Add_RNG()['RNG']
    DictOut['chroma']['Cfg'] = Add_cfg(icfg)['Cfg']
    WriteChromaXml(thisfile,DictOut)
    return filelistsm





def RemoveCombCorrFiles(folder):
    thisfolder = folder+'/corrComb'
    if os.path.isfile(thisfolder):os.remove(thisfolder)

def CreateCombCorrWrap(folder,fileprefix,cfgindicies):
    filelist = []
    for thecfg in cfgindicies:
        filelist += CreateCombCorrFiles(folder,fileprefix,thecfg,ismlist)
    return filelist


def CreateCombCorrFilesjsm(folder,fileprefix,icfg,thisismlist):
    filelistsm = []
    thisfolder = folder+'/corrComb/'
    mkdir_p(thisfolder)
    mkdir_p(thisfolder.replace('Input','Output'))
    thisfile = thisfolder+fileprefix+str(icfg)
    filelistsm.append(thisfile.replace(folder+'/','')+'.xml')
    DictOut = SetupDict()
    for ism in map(str,thisismlist):
        nism = ism.replace('sm','')
        for srcPoF in PoFList:
            thisprop = 'prop_id_sm'+ism+'_srcPoF'+str(srcPoF)
            DictOut = AddToIM(DictOut,iterlist.next(),Add_Source,['default_gauge_field','default_source'+str(srcPoF),icfg,nism,str(srcPoF)])
            DictOut = AddToIM(DictOut,iterlist.next(),Add_Propagator,[kud,'default_gauge_field','default_source'+str(srcPoF),thisprop])
            if Save2ptProp: DictOut = AddToIM(DictOut,iterlist.next(),Add_ReadNamedObject,[thisprop,'LatticePropagator',Get2ptProp(icfg,ism,iPoF=srcPoF)])
            if SaveMem: DictOut = AddToIM(DictOut,iterlist.next(),Add_EraseNamedObject,['default_source'+str(srcPoF)])
            for jsm in map(str,jsmlist):
                thissiprop = 'prop_id_sm'+ism+'_si'+jsm+'_PoF'+str(srcPoF)
                DictOut = AddToIM(DictOut,iterlist.next(),Add_Sink,['default_gauge_field',thisprop,thissiprop,jsm])
                DictOut = AddToIM(DictOut,iterlist.next(),Add_HadSpec,['default_gauge_field',thissiprop,thissiprop,icfg,ism,jsm,twoptinterps[0],str(srcPoF)])
                if SaveMem: DictOut = AddToIM(DictOut,iterlist.next(),Add_EraseNamedObject,[thissiprop])
            # if str(srcPoF) != PoFList[-1] and SaveMem: DictOut = AddToIM(DictOut,iterlist.next(),Add_EraseNamedObject,[thisprop])



            # ## Read 2pt prop in
            # if Save2ptProp:
            #     DictOut = AddToIM(DictOut,iterlist.next(),Add_ReadNamedObject,[thisprop,'LatticePropagator',Get2ptProp(icfg,ism,iPoF=srcPoF)])
            # else:
            #     DictOut = AddToIM(DictOut,iterlist.next(),Add_Source,['default_gauge_field','default_source'+str(srcPoF),icfg,nism,srcPoF])
            #     DictOut = AddToIM(DictOut,iterlist.next(),Add_Propagator,[kud,'default_gauge_field','default_source'+str(srcPoF),thisprop])
            #     if SaveMem: DictOut = AddToIM(DictOut,iterlist.next(),Add_EraseNamedObject,['default_source'+str(srcPoF)])
            for jsm in map(str,jsmlist):
                for DS in DSList:
                    for Projector in map(str,ProjectorList):
                        for iTS in map(str,it_sst):
                            # corr_tsink = str(ModuloT(int(iTS) + int(GetSourceString(icfg,iPoF=srcPoF).split()[-1])))
                            # thissiprop = 'prop_id_sm'+ism+'_srcPoF'+str(srcPoF)+'_si'+jsm
                            thisseqsource = 'seqsource_id_sm'+ism+'_srcPoF'+str(srcPoF)+'_si'+jsm+DS+'_Proj'+Projector+'_tsink'+iTS
                            thisseqprop = 'seqprop_id_sm'+ism+'_srcPoF'+str(srcPoF)+'_si'+jsm+DS+'_Proj'+Projector+'_tsink'+iTS

                            # ## smear sink
                            # DictOut = AddToIM(DictOut,iterlist.next(),Add_Sink,['default_gauge_field',thisprop,thissiprop,jsm])

                            ## create seq source
                            DictOut = AddToIM(DictOut,iterlist.next(),Add_SeqSource,['default_gauge_field',thisprop,thisprop,thisseqsource,
                                                                                     DS,Projector,twoptinterps[0],iTS,jsm])

                            # ## delete sink smeared 2pt propagator
                            # DictOut = AddToIM(DictOut,iterlist.next(),Add_EraseNamedObject,[thissiprop])

                            ## create FS prop
                            DictOut = AddToIM(DictOut,iterlist.next(),Add_Propagator,[kud,'default_gauge_field',thisseqsource,thisseqprop,True])

                            ## delete seq source
                            DictOut = AddToIM(DictOut,iterlist.next(),Add_EraseNamedObject,[thisseqsource])

                            ## Tie up FS prop to make 3pt corr
                            DictOut = AddToIM(DictOut,iterlist.next(),Add_Bar3ptTieUpjsm, ['default_gauge_field',thisprop,thisseqprop,icfg,ism,jsm,
                                                                                           iTS,Projector,DS,srcPoF])

                            ## delete total sequential source propagator
                            DictOut = AddToIM(DictOut,iterlist.next(),Add_EraseNamedObject,[thisseqprop])


    DictOut['chroma']['RNG'] = Add_RNG()['RNG']
    DictOut['chroma']['Cfg'] = Add_cfg(icfg)['Cfg']
    WriteChromaXml(thisfile,DictOut)
    return filelistsm





def CreateCombCorrFiles(folder,fileprefix,icfg,thisismlist):
    filelistsm = []
    thisfolder = folder+'/corrComb/'
    mkdir_p(thisfolder)
    mkdir_p(thisfolder.replace('Input','Output'))
    thisfile = thisfolder+fileprefix+str(icfg)
    filelistsm.append(thisfile.replace(folder+'/','')+'.xml')
    DictOut = SetupDict()
    for ism in map(str,thisismlist):
        nism = ism.replace('sm','')
        for srcPoF in PoFList:
            thisprop = 'prop_id_sm'+ism+'_srcPoF'+str(srcPoF)
            ## Read 2pt prop in
            DictOut = AddToIM(DictOut,iterlist.next(),Add_Source,['default_gauge_field','default_source'+str(srcPoF),icfg,nism,srcPoF])
            DictOut = AddToIM(DictOut,iterlist.next(),Add_Propagator,[kud,'default_gauge_field','default_source'+str(srcPoF),thisprop])
            if SaveMem: DictOut = AddToIM(DictOut,iterlist.next(),Add_EraseNamedObject,['default_source'+str(srcPoF)])
            for DS in DSList:
                for Projector in map(str,ProjectorList):
                    for iTS in map(str,it_sst):
                        PoFjsmlist = Elongate(PoFList,map(str,jsmlist))
                        totseqsourcelist = ['seqsource_id_sm'+ism+'_srcPoF'+str(srcPoF)+DS+'_Proj'+Projector+'_tsink'+iTS
                                            +'_PoF'+str(i) for i in range(len(PoFjsmlist))]
                        totseqprop = 'seqprop_id_sm'+ism+'_srcPoF'+str(srcPoF)+DS+'_Proj'+Projector+'_tsink'+iTS


                        for njsm,(iPoF,jsm) in enumerate(PoFjsmlist):
                            corr_tsink = str(ModuloT(int(iTS)+ int(iPoF)+ int(GetSourceString(icfg,iPoF=srcPoF).split()[-1])))
                            # thissiprop = 'prop_id_sm'+ism+'_srcPoF'+str(srcPoF)+'_si'+jsm+'_PoF'+str(iPoF)
                            if njsm == 0:
                                thisseqsource = totseqsourcelist[0]
                            else:
                                thisseqsource = 'seqsource_id_sm'+ism+'_srcPoF'+str(srcPoF)+'_si'+jsm+'_PoF'+str(iPoF)+DS+'_Proj'+Projector+'_tsink'+iTS
                            # ## smear sink
                            # DictOut = AddToIM(DictOut,iterlist.next(),Add_Sink,['default_gauge_field',thisprop,thissiprop,jsm])

                            ## create seq source
                            DictOut = AddToIM(DictOut,iterlist.next(),Add_SeqSource,['default_gauge_field',thisprop,thisprop,thisseqsource,
                                                                       DS,Projector,twoptinterps[0],corr_tsink,jsm])

                            # ## delete sink smeared 2pt source
                            # DictOut = AddToIM(DictOut,iterlist.next(),Add_EraseNamedObject,[thissiprop])

                            ## add to previous seq source with weightings
                            if njsm == 1:
                                DictOut = AddToIM(DictOut,iterlist.next(),Add_qPropAdd,[totseqsourcelist[0],thisseqsource,RVec[0],RVec[1],totseqsourcelist[1]])
                                ## delete sink smeared 2pt source
                                DictOut = AddToIM(DictOut,iterlist.next(),Add_EraseNamedObject,[thisseqsource])
                                ## delete sink smeared 2pt source
                                DictOut = AddToIM(DictOut,iterlist.next(),Add_EraseNamedObject,[totseqsourcelist[0]])
                            elif njsm > 1:
                                DictOut = AddToIM(DictOut,iterlist.next(),Add_qPropAdd,[totseqsourcelist[njsm-1],thisseqsource,1.0,RVec[njsm],
                                                                                        totseqsourcelist[njsm]])
                                ## delete sink smeared 2pt source
                                DictOut = AddToIM(DictOut,iterlist.next(),Add_EraseNamedObject,[thisseqsource])
                                ## delete sink smeared 2pt source
                                DictOut = AddToIM(DictOut,iterlist.next(),Add_EraseNamedObject,[totseqsourcelist[njsm-1]])


                        ## create FS prop
                        DictOut = AddToIM(DictOut,iterlist.next(),Add_Propagator,[kud,'default_gauge_field',totseqsourcelist[-1],totseqprop,True])


                        ## delete total sink smeared 2pt source
                        DictOut = AddToIM(DictOut,iterlist.next(),Add_EraseNamedObject,[totseqsourcelist[-1]])

                        ## Tie up FS prop to make 3pt corr
                        DictOut = AddToIM(DictOut,iterlist.next(),Add_Bar3ptTieUp, ['default_gauge_field',thisprop,totseqprop,icfg,ism,iTS,Projector,DS,srcPoF])

                        ## delete total sequential source propagator
                        DictOut = AddToIM(DictOut,iterlist.next(),Add_EraseNamedObject,[totseqprop])


    DictOut['chroma']['RNG'] = Add_RNG()['RNG']
    DictOut['chroma']['Cfg'] = Add_cfg(icfg)['Cfg']
    WriteChromaXml(thisfile,DictOut)
    return filelistsm
