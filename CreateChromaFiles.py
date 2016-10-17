#!/usr/bin/env python

from RunParams import *
from FilenameFuns import *
import os
from OutputXmlData import WriteChromaXml
from collections import OrderedDict as OrdDict
from MiscFuns import Elongate
from ChromaXmlChunks import *


iterlist = iter(range(50))

def Chromaqlist(Minqsqrd,Maxqsqrd):
    qlist = []
    for iq1 in range(-Maxqsqrd,Maxqsqrd+1):
        for iq2 in range(-Maxqsqrd,Maxqsqrd+1):
            for iq3 in range(-Maxqsqrd,Maxqsqrd+1):
                if iq1**2 + iq2**2 + iq3**2 > Maxqsqrd: continue
                if iq1**2 + iq2**2 + iq3**2 < Minqsqrd: continue
                qlist.append(str(iq1) + ' ' + str(iq2) + ' ' + str(iq3))
    return qlist

def Remove2ptPropFiles(folder,fileprefix,icfg,thisismlist):
    for ism in map(str,thisismlist):
        thisfile = folder+'/prop2pt'+ism+'/'+fileprefix+str(icfg)
        if os.path.isfile(thisfile+'.xml'):os.remove(thisfile+'.xml')

def Create2ptPropFiles(folder,fileprefix,icfg,thisismlist):
    filelistsm = []
    for ism in map(str,thisismlist):
        nism = ism.replace('sm','')
        mkdir_p(folder+'/prop2pt'+ism+'/')
        mkdir_p(folder.replace('Input','Output')+'/prop2pt'+ism+'/')
        thisfile = folder+'/prop2pt'+ism+'/'+fileprefix+str(icfg)
        if os.path.isfile(thisfile):os.remove(thisfile)
        filelistsm.append(thisfile.replace(folder+'/','')+'.xml')
        DictOut = SetupDict()
        DictOut = AddToIM(DictOut,iterlist.next(),Add_Source,['default_gauge_field','default_source',icfg,nism])
        DictOut = AddToIM(DictOut,iterlist.next(),Add_Propagator,[kud,'default_gauge_field','default_source','k_prop'])
        DictOut = AddToIM(DictOut,iterlist.next(),Add_WriteNamedObject,['k_prop','LatticePropagator',Get2ptProp(icfg,ism),'SINGLEFILE'])
        DictOut['chroma']['RNG'] = Add_RNG()['RNG']
        DictOut['chroma']['Cfg'] = Add_cfg(icfg)['Cfg']
        WriteChromaXml(thisfile,DictOut)
    return filelistsm


def Remove2ptCorrFiles(folder,fileprefix,icfg,thisismlist):
    for ism in map(str,thisismlist):
        thisfile = folder+'/corr2pt'+ism+'/'+fileprefix+str(icfg)
        if os.path.isfile(thisfile):os.remove(thisfile)


def Create2ptCorrFiles(folder,fileprefix,icfg,thisismlist):
    filelistsm = []
    thisqlist = Chromaqlist(qmin,qmax)
    for ism in map(str,thisismlist):
        mkdir_p(folder+'/corr2pt'+ism+'/')
        mkdir_p(folder.replace('Input','Output')+'/corr2pt'+ism+'/')
        thisfile = folder+'/corr2pt'+ism+'/'+fileprefix+str(icfg)
        filelistsm.append(thisfile.replace(folder+'/','')+'.xml')
        DictOut = SetupDict()
        thisprop = 'prop_id_sm'+ism
        DictOut = AddToIM(DictOut,iterlist.next(),Add_ReadNamedObject,[thisprop,'LatticePropagator',Get2ptProp(icfg,ism)])
        for jsm in map(str,jsmlist):
            thissiprop = 'prop_id_sm'+ism+'_si'+jsm
            DictOut = AddToIM(DictOut,iterlist.next(),Add_Sink,['default_gauge_field',thisprop,thissiprop,jsm])
            DictOut = AddToIM(DictOut,iterlist.next(),Add_BarSpec,['default_gauge_field',thissiprop,thissiprop,icfg,ism,jsm,twoptinterps[0]])
            DictOut = AddToIM(DictOut,iterlist.next(),Add_EraseNamedObject,[thissiprop])
        DictOut['chroma']['RNG'] = Add_RNG()['RNG']
        DictOut['chroma']['Cfg'] = Add_cfg(icfg)['Cfg']
        WriteChromaXml(thisfile,DictOut)
    return filelistsm


def Remove3ptCorrFiles(folder,fileprefix,icfg,thisismlist,thisDSList,thisProjectorList,thisit_sst):
    for ism in map(str,thisismlist):
        for DS in thisDSList:
            for Projector in map(str,thisProjectorList):
                for iTS in map(str,thisit_sst):                    
                    thisfolder = folder+'/corr3pt'+ism+'/'+DS+'GMA'+Projector+'tsink'+iTS+'/'
                    thisfile = thisfolder+fileprefix+str(icfg)
                    if os.path.isfile(thisfile):os.remove(thisfile)


def Create3ptCorrFiles(folder,fileprefix,icfg,thisismlist,thisDSList,thisProjectorList,thisit_sst):
    filelistsm = []
    for ism in map(str,thisismlist):
        for DS in thisDSList:
            for Projector in map(str,thisProjectorList):
                for iTS in map(str,thisit_sst):                    
                    thisfolder = folder+'/corr3pt'+ism+'/'+DS+'GMA'+Projector+'tsink'+iTS+'/'
                    mkdir_p(thisfolder)
                    mkdir_p(thisfolder.replace('Input','Output'))
                    thisfile = thisfolder+fileprefix+str(icfg)
                    filelistsm.append(thisfile.replace(folder+'/','')+'.xml')
                    thisprop = 'prop_id_sm'+ism
                    PoFjsmlist = Elongate(PoFList,map(str,jsmlist))
                    totseqsourcelist = ['seqsource_id_sm'+ism+DS+'_Proj'+Projector+'_tsink'+iTS+'no'+str(i) for i in range(len(PoFjsmlist))]
                    totseqprop = 'seqprop_id_sm'+ism+DS+'_Proj'+Projector+'_tsink'+iTS
                    DictOut = SetupDict()

                    ## Read 2pt prop in
                    DictOut = AddToIM(DictOut,iterlist.next(),Add_ReadNamedObject,[thisprop,'LatticePropagator',Get2ptProp(icfg,ism)])

                    for njsm,(iPoF,jsm) in enumerate(PoFjsmlist):
                        thissiprop = 'prop_id_sm'+ism+'_si'+jsm+'_PoF'+str(iPoF)
                        if njsm == 0:
                            thisseqsource = totseqsourcelist[0]
                        else:
                            thisseqsource = 'seqsource_id_sm'+ism+'_si'+jsm+'_PoF'+str(iPoF)+DS+'_Proj'+Projector+'_tsink'+iTS
                        ## smear sink
                        DictOut = AddToIM(DictOut,iterlist.next(),Add_Sink,['default_gauge_field',thisprop,thissiprop,jsm])

                        ## create seq source
                        DictOut = AddToIM(DictOut,iterlist.next(),Add_SeqSource,['default_gauge_field',thissiprop,thissiprop,thisseqsource,
                                                                   DS,Projector,twoptinterps[0],str(int(iTS)+iPoF),jsm])

                        ## delete sink smeared 2pt source
                        DictOut = AddToIM(DictOut,iterlist.next(),Add_EraseNamedObject,[thissiprop])

                        ## add to previous seq source with weightings
                        if njsm == 1:
                            DictOut = AddToIM(DictOut,iterlist.next(),Add_qPropAdd,[totseqsourcelist[0],thisseqsource,RVec[0],RVec[1],totseqsourcelist[1]])
                            ## delete sink smeared 2pt source
                            DictOut = AddToIM(DictOut,iterlist.next(),Add_EraseNamedObject,[thisseqsource])
                            ## delete sink smeared 2pt source
                            DictOut = AddToIM(DictOut,iterlist.next(),Add_EraseNamedObject,[totseqsourcelist[0]])
                        elif njsm > 1:
                            DictOut = AddToIM(DictOut,iterlist.next(),Add_qPropAdd,[totseqsourcelist[njsm-1],thisseqsource,1.0,RVec[njsm],totseqsourcelist[njsm]])
                            ## delete sink smeared 2pt source
                            DictOut = AddToIM(DictOut,iterlist.next(),Add_EraseNamedObject,[thisseqsource])
                            ## delete sink smeared 2pt source
                            DictOut = AddToIM(DictOut,iterlist.next(),Add_EraseNamedObject,[totseqsourcelist[njsm-1]])


                    ## create FS prop
                    DictOut = AddToIM(DictOut,iterlist.next(),Add_Propagator,[kud,'default_gauge_field',totseqsourcelist[-1],totseqprop,True])


                    ## delete total sink smeared 2pt source
                    DictOut = AddToIM(DictOut,iterlist.next(),Add_EraseNamedObject,[totseqsourcelist[-1]])

                    ## Tie up FS prop to make 3pt corr                        
                    DictOut = AddToIM(DictOut,iterlist.next(),Add_Bar3ptTieUp, ['default_gauge_field',thisprop,totseqprop,icfg,ism,iTS,Projector,DS])

                    DictOut['chroma']['RNG'] = Add_RNG()['RNG']
                    DictOut['chroma']['Cfg'] = Add_cfg(icfg)['Cfg']
                    WriteChromaXml(thisfile,DictOut)
    return filelistsm


def Create3ptCorrFilesjsm(folder,fileprefix,icfg,thisismlist,thisjsmlist,thisDSList,thisProjectorList,thisit_sst):
    filelistsm = []
    for ism in map(str,thisismlist):
        for jsm in map(str,thisjsmlist):
            for DS in thisDSList:
                for Projector in map(str,thisProjectorList):
                    for iTS in map(str,thisit_sst):                    
                        thisfolder = folder+'/corr3pt'+ism+'/'+DS+'GMA'+Projector+'tsink'+iTS+'/'
                        mkdir_p(thisfolder)
                        mkdir_p(thisfolder.replace('Input','Output'))
                        thisfile = thisfolder+fileprefix+str(icfg)
                        filelistsm.append(InputFolderPref+'/'+thisfile.replace(folder+'/','')+'.xml')
                        thisprop = 'prop_id_sm'+ism
                        thissiprop = 'prop_id_sm'+ism+'_si'+jsm
                        thisseqsource = 'seqsource_id_sm'+ism+'_si'+jsm+DS+'_Proj'+Projector+'_tsink'+iTS
                        thisseqprop = 'seqprop_id_sm'+ism+'_si'+jsm+DS+'_Proj'+Projector+'_tsink'+iTS
                        DictOut = SetupDict()

                        ## Read 2pt prop in
                        DictOut = AddToIM(DictOut,iterlist.next(),Add_ReadNamedObject,[thisprop,'LatticePropagator',Get2ptProp(icfg,ism)])

                        ## smear sink
                        DictOut = AddToIM(DictOut,iterlist.next(),Add_Sink,['default_gauge_field',thisprop,thissiprop,jsm])

                        ## create seq source
                        DictOut = AddToIM(DictOut,iterlist.next(),Add_SeqSource,['default_gauge_field',thissiprop,thissiprop,thisseqsource,DS,Projector,twoptinterps[0],iTS,jsm])

                        ## delete sink smeared 2pt propagator
                        DictOut = AddToIM(DictOut,iterlist.next(),Add_EraseNamedObject,[thissiprop])

                        ## create FS prop
                        DictOut = AddToIM(DictOut,iterlist.next(),Add_Propagator,[kud,'default_gauge_field',thisseqsource,thisseqprop,True])

                        ## delete seq source 
                        DictOut = AddToIM(DictOut,iterlist.next(),Add_EraseNamedObject,[thisseqsource])

                        ## Tie up FS prop to make 3pt corr                        
                        DictOut = AddToIM(DictOut,iterlist.next(),Add_Bar3ptTieUpjsm, ['default_gauge_field',thisprop,thisseqprop,icfg,ism,jsm,iTS,Projector,DS])

                        DictOut['chroma']['RNG'] = Add_RNG()['RNG']
                        DictOut['chroma']['Cfg'] = Add_cfg(icfg)['Cfg']
                        WriteChromaXml(thisfile,DictOut)
    return filelistsm

