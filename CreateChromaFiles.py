#!/usr/bin/env python

from RunParams import *
from FilenameFuns import *
import os
from OutputXmlData import WriteChromaXml
from collections import OrderedDict as OrdDict
from MiscFuns import Elongate
from ChromaXmlChunks import *


iterlist = iter(range(500))

def Chromaqlist(Minqsqrd,Maxqsqrd):
    qlist = []
    for iq1 in range(-Maxqsqrd,Maxqsqrd+1):
        for iq2 in range(-Maxqsqrd,Maxqsqrd+1):
            for iq3 in range(-Maxqsqrd,Maxqsqrd+1):
                if iq1**2 + iq2**2 + iq3**2 > Maxqsqrd: continue
                if iq1**2 + iq2**2 + iq3**2 < Minqsqrd: continue
                qlist.append(str(iq1) + ' ' + str(iq2) + ' ' + str(iq3))
    return qlist

def RemoveGaugeFieldFiles(folder,fileprefix,icfg):
    thisfile = folder+'/gfield/'+fileprefix+str(icfg)
    if os.path.isfile(thisfile+'.xml'):os.remove(thisfile+'.xml')



def CreateGaugeFieldFiles(folder,fileprefix,icfg):
    mkdir_p(folder+'/gfield/')
    mkdir_p(folder.replace('Input','Output')+'/gfield/')
    thisfile = folder+'/gfield/'+fileprefix+str(icfg)
    if os.path.isfile(thisfile):os.remove(thisfile)
    filelist = [thisfile.replace(folder+'/','')+'.xml']
    DictOut = SetupGaugeDict(GaugeType,icfg)
    
    # DictOut = AddToIM(DictOut,iterlist.next(),Add_CoulombGF,['default_gauge_field','gfix_id','grot_id'])
    # DictOut = AddToIM(DictOut,iterlist.next(),Add_WriteNamedObject,['default_gauge_field','Multi1dLatticeColorMatrixD',GetGaugeField(icfg),'SINGLEFILE'])
    # DictOut = AddToIM(DictOut,iterlist.next(),Add_WriteNamedObject,['gfix_id','Multi1dLatticeColorMatrix',GetGaugeField(icfg).replace('.lime','_gfix.lime'),'SINGLEFILE'])
    # DictOut = AddToIM(DictOut,iterlist.next(),Add_WriteNamedObject,['grot_id','Multi1dLatticeColorMatrix',GetGaugeField(icfg).replace('.lime','_grot.lime'),'SINGLEFILE'])
    # DictOut['chroma']['RNG'] = Add_RNG()['RNG']
    # DictOut['chroma']['Cfg'] = Add_cfg(icfg)['Cfg']
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
    

def Remove2ptCorrFiles(folder,fileprefix,icfg,thisismlist):
    for ism in map(str,thisismlist):
        thisfile = folder+'/corr2pt'+ism+'/'+fileprefix+str(icfg)
        if os.path.isfile(thisfile):os.remove(thisfile)



def Create2ptCorrWrap(folder,filepref,icfg,fcfg,ism):
    filelist = []
    for thecfg in range(icfg,fcfg+1):
        filelist.append(Create2ptCorrFiles(folder,fileprefix,thecfg,[ism])[0])
    return filelist
        
def Create2ptCorrFiles(folder,fileprefix,icfg,thisismlist):
    filelistsm = []
    thisqlist = Chromaqlist(qmin,qmax)
    for ism in map(str,thisismlist):
        nism = ism.replace('sm','')
        mkdir_p(folder+'/corr2pt'+ism+'/')
        mkdir_p(folder.replace('Input','Output')+'/corr2pt'+ism+'/')
        thisfile = folder+'/corr2pt'+ism+'/'+fileprefix+str(icfg)
        filelistsm.append(thisfile.replace(folder+'/','')+'.xml')
        DictOut = SetupDict()
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


def Remove3ptCorrFiles(folder,fileprefix,icfg,thisismlist):
    for ism in map(str,thisismlist):
        thisfolder = folder+'/corr3pt'+ism+'/'
        thisfile = thisfolder+fileprefix+str(icfg)
        if os.path.isfile(thisfile):os.remove(thisfile)


def Create3ptCorrWrap(folder,filepref,icfg,fcfg,ism):
    filelist = []
    for thecfg in range(icfg,fcfg+1):
        filelist.append(Create3ptCorrFiles(folder,fileprefix,thecfg,[ism])[0])
    return filelist

        
def Create3ptCorrFiles(folder,fileprefix,icfg,thisismlist):
    filelistsm = []
    for ism in map(str,thisismlist):
        nism = ism.replace('sm','')
        thisfolder = folder+'/corr3pt'+ism+'/'
        mkdir_p(thisfolder)
        mkdir_p(thisfolder.replace('Input','Output'))
        thisfile = thisfolder+fileprefix+str(icfg)
        filelistsm.append(thisfile.replace(folder+'/','')+'.xml')
        DictOut = SetupDict()
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
                            # thissiprop = 'prop_id_sm'+ism+'_srcPoF'+str(srcPoF)+'_si'+jsm+'_PoF'+str(iPoF)
                            if njsm == 0:
                                thisseqsource = totseqsourcelist[0]
                            else:
                                thisseqsource = 'seqsource_id_sm'+ism+'_srcPoF'+str(srcPoF)+'_si'+jsm+'_PoF'+str(iPoF)+DS+'_Proj'+Projector+'_tsink'+iTS
                            # ## smear sink
                            # DictOut = AddToIM(DictOut,iterlist.next(),Add_Sink,['default_gauge_field',thisprop,thissiprop,jsm])

                            ## create seq source
                            DictOut = AddToIM(DictOut,iterlist.next(),Add_SeqSource,['default_gauge_field',thisprop,thisprop,thisseqsource,
                                                                       DS,Projector,twoptinterps[0],str(int(iTS)+iPoF),jsm])

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


def Create3ptCorrFilesjsm(folder,fileprefix,icfg,thisismlist,thisjsmlist,thisDSList,thisProjectorList,thisit_sst):
    filelistsm = []
    for ism in map(str,thisismlist):
        nism = ism.replace('sm','')
        thisfolder = folder+'/corr3pt'+ism+'/'
        mkdir_p(thisfolder)
        mkdir_p(thisfolder.replace('Input','Output'))
        thisfile = thisfolder+fileprefix+str(icfg)
        filelistsm.append(InputFolderPref+'/'+thisfile.replace(folder+'/','')+'.xml')
        DictOut = SetupDict()
        for srcPoF in PoFList:
            thisprop = 'prop_id_sm'+ism+'_srcPoF'+str(srcPoF)
            ## Read 2pt prop in
            if Save2ptProp:
                DictOut = AddToIM(DictOut,iterlist.next(),Add_ReadNamedObject,[thisprop,'LatticePropagator',Get2ptProp(icfg,ism,iPoF=srcPoF)])
            else:
                DictOut = AddToIM(DictOut,iterlist.next(),Add_Source,['default_gauge_field','default_source'+str(srcPoF),icfg,nism,srcPoF])
                DictOut = AddToIM(DictOut,iterlist.next(),Add_Propagator,[kud,'default_gauge_field','default_source'+str(srcPoF),thisprop])
                if SaveMem: DictOut = AddToIM(DictOut,iterlist.next(),Add_EraseNamedObject,['default_source'+str(srcPoF)])
            for jsm in map(str,thisjsmlist):
                for DS in thisDSList:
                    for Projector in map(str,thisProjectorList):
                        for iTS in map(str,thisit_sst):                    
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

