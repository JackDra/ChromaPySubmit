#!/usr/bin/env python

import os
from RunParams import gfdir,gfdir_store,CreateCfg,jsmlist
from RunParams import PoFList,diskdir,scratchdir,Debug
from RunParams import OnDist,NDerList
from FilenameFuns import Get2ptProp,Get2ptCorrFolders
from FilenameFuns import Get2ptCorrOutput,Get2ptCorr
from FilenameFuns import Get3ptCorr,Get3ptCorrjsm
from MiscFuns import mkdir_p
from shutil import move
# import subprocess

def GetGaugeField(icfg,Flow=False):
    this_file = gfdir+CreateCfg(icfg,Flow=Flow)[0]
    if os.path.isfile(this_file):
        return this_file
    else:
        return gfdir_store+CreateCfg(icfg,Flow=Flow)[0]


# def RemoveGaugeField(icfg):
#     gffile = gfdir+CreateCfg(icfg)
#     if os.path.isfile(gffile):
#         print 'Deleting: ' , gffile
#         os.remove(gffile)
#     # else:
#         # print gffile , ' not present'

def CheckGaugeField(icfg):
    gffile = gfdir+CreateCfg(icfg)[0]
    print 'Checking existance of: ', gffile
    return os.path.isfile(gffile)

def RemoveProp(icfg,thisismlist):
    for ism in thisismlist:
        thisfile = Get2ptProp(icfg,ism)
        if os.path.isfile(thisfile):
            print 'Removing: ',thisfile
            os.remove(thisfile)
        if os.path.isfile(thisfile+'.metadata'):
            os.remove(thisfile+'.metadata')
        # else:
        #     print thisfile,' not present'


## also makes directory
def Move2ptCorr(icfg,thisismlist,thisjsmlist,interplist):
    for ism in thisismlist:
        map(mkdir_p,Get2ptCorrFolders(icfg,ism,jsmlist))
        for jsm in thisjsmlist:
            for iterp in interplist:
                thisoutfile = Get2ptCorrOutput(icfg,ism,jsm,iterp)
                thisfile = Get2ptCorr(icfg,ism,jsm,iterp)
                if os.path.isfile(thisoutfile):
                    move(thisoutfile,thisfile)
                # else:
                #     print thisoutfile, ' not present'

def Check2ptProp(icfg,thisismlist):
    Present = True
    for ism in thisismlist:
        thisfile = Get2ptProp(icfg,ism)
        if not os.path.isfile(thisfile):
            Present = False
    return Present

def Check2ptCorr(icfg,thisismlist,thisjsmlist,interplist):
    Present = True
    for ism in thisismlist:
        for iPoF in PoFList:
            for jsm in thisjsmlist:
                for iterp in interplist:
                    thisfile = Get2ptCorr(icfg,ism,jsm,iterp,iPoF=iPoF)
                    if len(diskdir) > 0:
                        thisfiledisk = thisfile.replace(scratchdir,diskdir)
                        logic = os.path.isfile(thisfile) or os.path.isfile(thisfiledisk)
                    else:
                        logic = os.path.isfile(thisfile)
                    if not logic:
                        if Debug:
                            print 'Not Present: ', thisfile
                        Present = False
                    else:
                        if Debug:
                            print 'Present: ', thisfile
                    if OnDist:
                        raise EnvironmentError('OnDist not implemented yet')
                        # thisfile = Get2ptCorrOD(icfg,ism,jsm,iterp,iPoF=iPoF)
                        # if not os.path.isfile(thisfile):
                        #     if Debug:
                        #         print 'Not Present: ', thisfile
                        #     Present = False
                        # else:
                        #     if Debug:
                        #         print 'Present: ', thisfile

    return Present

def Check3ptCorr(icfg,thisismlist,tsinklist,Projectorlist,DSlist):
    Present = True
    for ism in thisismlist:
        for iPoF in PoFList:
            for tsink in tsinklist:
                for Projector in Projectorlist:
                    for DS in DSlist:
                        for iDer in NDerList:
                            thisfile = Get3ptCorr(icfg,ism,tsink,Projector,DS,iDer,iPoF=iPoF)
                            if len(diskdir) > 0:
                                thisfiledisk = thisfile.replace(scratchdir,diskdir)
                                logic = os.path.isfile(thisfile) or os.path.isfile(thisfiledisk)
                            else:
                                logic = os.path.isfile(thisfile)
                            if not logic:
                                if Debug:
                                    print 'Not Present: ', thisfile
                                Present = False
                            else:
                                if Debug:
                                    print 'Present: ', thisfile
                            if OnDist:
                                raise EnvironmentError('OnDist not implemented yet')
                                # thisfile = Get3ptCorrOD(icfg,ism,tsink,Projector,DS,iDer,iPoF=iPoF)
                                # if not os.path.isfile(thisfile):
                                #     if Debug:
                                #         print 'Not Present: ', thisfile
                                #     Present = False
                                # else:
                                #     if Debug:
                                #         print 'Present: ', thisfile
    return Present

def Check3ptCorrjsm(icfg,thisismlist,thisjsmlist,tsinklist,Projectorlist,DSlist):
    Present = True
    for ism in thisismlist:
        for jsm in thisjsmlist:
            for iPoF in PoFList:
                for tsink in tsinklist:
                    for Projector in Projectorlist:
                        for DS in DSlist:
                            for iDer in NDerList:
                                thisfile = Get3ptCorrjsm(icfg,ism,jsm,tsink,Projector,DS,iDer,iPoF=iPoF)
                                if len(diskdir) > 0:
                                    thisfiledisk = thisfile.replace(scratchdir,diskdir)
                                    logic = os.path.isfile(thisfile) or os.path.isfile(thisfiledisk)
                                else:
                                    logic = os.path.isfile(thisfile)
                                if not logic:
                                    # print 'Not Present: ', thisfile
                                    Present = False
                                # else:
    return Present


def Remove2ptCorr(icfg,thisismlist,thisjsmlist,interplist):
    for ism in thisismlist:
        for jsm in thisjsmlist:
            for iterp in interplist:
                thisfile = Get2ptCorr(icfg,ism,jsm,iterp)
                if os.path.isfile(thisfile): os.remove(thisfile)

def Remove3ptCorr(icfg,thisismlist,tsinklist,Projectorlist,DSlist):
    for ism in thisismlist:
        for tsink in tsinklist:
            for Projector in Projectorlist:
                for DS in DSlist:
                    for iDer in NDerList:
                        thisfile = Get3ptCorr(icfg,ism,tsink,Projector,DS,iDer)
                        if os.path.isfile(thisfile): os.remove(thisfile)
