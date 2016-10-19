#!/usr/bin/env python

import os
from RunParams import *
from shutil import copyfile,move,rmtree
import subprocess
from FilenameFuns import *

# def GetGaugeField(icfg):
#     limefile = CreateLimeCfg(icfg)
#     limepath = rdsigfdir+limefile
#     if os.path.isfile(limepath):
#         if os.path.isfile(gfdir+CreateCfg(icfg)):
#             print gfdir+CreateCfg(icfg) , ' Already present'
#         else:
#             print 'Copying Gf from: '+limepath
#             copyfile(limepath,gfdir+limefile)
#             subprocess.call([limedir+"lime_unpack",gfdir+limefile])
#             move(gfdir+limefile+'.contents/msg01.rec02.ildg-binary-data',gfdir+CreateCfg(icfg))
#             rmtree(gfdir+limefile+'.contents/')
#             os.remove(gfdir+limefile)
#             print 'Copying complete'
#     else:
#         print 'Warning: ' , limepath , ' Does not exist'

# def RemoveGaugeField(icfg):
#     gffile = gfdir+CreateCfg(icfg)
#     if os.path.isfile(gffile):
#         print 'Deleting: ' , gffile
#         os.remove(gffile)
#     # else:
#         # print gffile , ' not present'


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
        for jsm in thisjsmlist:
            for iterp in interplist:
                thisfile = Get2ptCorr(icfg,ism,jsm,iterp)
                if not os.path.isfile(thisfile): 
                    Present = False
    return Present

def Check3ptCorr(icfg,thisismlist,tsinklist,Projectorlist,DSlist):
    Present = True
    for ism in thisismlist:
        for tsink in tsinklist:
            for Projector in Projectorlist:
                for DS in DSlist:
                    for iDer in NDerList:
                        thisfile = Get3ptCorr(icfg,ism,tsink,Projector,DS,iDer)
                        if not os.path.isfile(thisfile): 
                            Present = False
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
                        
