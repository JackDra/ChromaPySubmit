#!/usr/bin/env python

import os
from RunParams import *
from MiscFuns import mkdir_p
from operator import itemgetter
import numpy as np

## used to pick which of the allowable geometries in geomlist
def PickGeom(geomlist,Split=GeomPicked):
    geomout = np.array([-100,-1,1,100])
    if 'EvenSpread' in Split:
        for igeom in geomlist:
            npgeom = np.array(igeom)
            if np.sum(np.abs(npgeom-np.roll(npgeom,1))) <= np.sum(np.abs(geomout-np.roll(geomout,1))):
                geomout = npgeom
    elif 'Tsplit' in Split:
        maxt = max(geomlist,key=itemgetter(3))[-1]
        for igeom in geomlist:
            npgeom = np.array(igeom)
            if igeom[-1] == maxt:
                if np.sum(np.abs(npgeom[:-1]-np.roll(npgeom[:-1],1))) <= np.sum(np.abs(geomout[:-1]-np.roll(geomout[:-1],1))):
                    geomout = npgeom            
    elif 'Spacesplit' in Split:
        minimt = min(geomlist,key=itemgetter(3))[-1]
        for igeom in geomlist:
            npgeom = np.array(igeom)
            if igeom[-1] == minimt:
                if np.sum(np.abs(npgeom[:-1]-np.roll(npgeom[:-1],1))) <= np.sum(np.abs(geomout[:-1]-np.roll(geomout[:-1],1))):
                    geomout = npgeom            
    return geomout
    
## uses nx, nt, totproc from RunParams.py
def GetGeomInput(Split=GeomPicked):
    geomlist = []
    for in_t in range(1,nt+1):
        if nt % in_t != 0: continue
        for in_z in range(1,nx+1):
            if nx % in_z != 0: continue
            for in_y in range(1,nx+1):
                if nx % in_y != 0: continue
                for in_x in range(1,nx+1):
                    if nx % in_x != 0: continue
                    if in_t*in_x*in_y*in_z == totproc:
                        geomlist.append((in_x,in_y,in_z,in_t))
    # print geomlist
    if len(geomlist) == 0: raise IOError('No Geometries are allowable by the choice of nx, nt, nproc and RPN')
    # if len(geomlist) == 1 and geomlist[0] == (1,1): print 'WARNING, no geometry has been found'
    npx,npy,npz,npt = PickGeom(geomlist,Split=Split)
    npxtvec = [npx,npy,npz,npt]
    return ' '.join(map(str,npxtvec))

## uses nx, nt, totproc from RunParams.py
def GetIOGeomInput():
    geomlist = []
    npx,npt = 4,4
    for in_x in range(1,npx+1):
        for in_t in range(1,npt+1):
            if totproc % in_t*in_x == 0 and nx % npx == 0 and nt % npt == 0:
                geomlist.append((in_x,in_t))
    if len(geomlist) == 1: raise IOError('ParaIO cannot be done on this choise of nx, nt, nproc and RPN')
    multlist = [ix*it for ix,it in geomlist]
    npx,npt = geomlist[multlist.index(max(multlist))]
    npxtvec = [1,1,npx,npt]
    return ' '.join(map(str,npxtvec))


def CreateCSHFile(thisfile,outputlist):
    with open(thisfile,'w') as f:
        for iout in outputlist:
            f.write("%s\n" % iout)
        f.write('\n')
    os.system("chmod u+x "+thisfile)

def CreateCSHList(icfg,fcfg,ism,jobid,stage,tsink='',Proj='',DS=''):
    inputfile = InputFolder+jobid
    outputfile = OutputFolder+jobid.replace('.xml','.out')
    logfile = OutputFolder+jobid.replace('.xml','.log')
    if os.path.isfile(outputfile):os.remove(outputfile)
    if os.path.isfile(logfile):os.remove(logfile)
    icfg,fcfg,ism,tsink,Proj = str(icfg),str(fcfg),str(ism),str(tsink),str(Proj)

    outlist = []
    outlist.append(r'#! /bin/tcsh')
    outlist.append('')
    outlist.append(r'#SBATCH -p '+quetype)
    outlist.append(r'#SBATCH -n '+str(nproc))
    outlist.append(r'#SBATCH --time='+time)
    if GPU != False:
        outlist.append(r'#SBATCH --gres=gpu:'+GPU)
    outlist.append(r'#SBATCH --mem='+mem)
    outlist.append('')
    if not Submit:
        for imod in ModuleList:
            outlist.append(r'module load '+imod)
    outlist.append('')
    outlist.append(r'cd '+scriptdir)
    outlist.append('')
    if 'twopt' in stage:
        outlist.append(r'    echo "icfg='+icfg+', fcfg='+fcfg+', ism='+ism+', '+stage+' "')
    elif 'threept' in stage:
        outlist.append(r'    echo "icfg='+icfg+', fcfg='+fcfg+', ism='+ism+', t_sink='+tsink+', Proj='+Proj+', DS='+DS+', '+stage+' "')
    elif 'gfield' in stage:
        outlist.append(r'    echo "icfg='+icfg+', fcfg='+fcfg+', '+stage+' "')
    outlist.append(r'    echo "starting "`date`')
    if 'gfield' in stage:
        outlist.append(r'    mpirun -np '+str(nproc)+' '+chromacpu+GFexe+r' -i '+inputfile+r' -o '+outputfile+r' -l '+logfile+
                       ' -geom '+GetGeomInput()+' -iogeom '+GetIOGeomInput())
    else:
        outlist.append(r'    mpirun -np '+str(nproc)+' '+chromacpu+exe+r' -i '+inputfile+r' -o '+outputfile+r' -l '+logfile+
                       ' -geom '+GetGeomInput()+' -iogeom '+GetIOGeomInput())
    outlist.append(r'    if ($? != 0) then')
    outlist.append(r'        echo "Error with: '+inputfile+r'"')
    outlist.append(r'        echo ""')
    outlist.append(r'cat <<EOF >> '+paramdir+r'errlist.2ptprop')
    outlist.append(r''+inputfile)
    outlist.append(r'EOF')
    if 'twopt' in stage:
        outlist.append(r'python '+scriptdir+r'ReSubmit.py '+"'"+"' '".join([icfg,fcfg,stage,ism,'Error'])+"'")
    elif 'threept' in stage:
        outlist.append(r'python '+scriptdir+r'ReSubmit.py '+"'"+"' '".join([icfg,fcfg,stage,ism,'Error',tsink,Proj,DS])+"'")
    elif 'gfield' in stage:
        outlist.append(r'python '+scriptdir+r'ReSubmit.py '+"'"+"' '".join([str(int(icfg)+1),fcfg,'gfield',ism,'Error'])+"'")
    outlist.append(r'        exit 1')
    outlist.append(r'    endif')
    outlist.append(r'    echo "finished "`date`')
    outlist.append('')
    if 'twopt' in stage:
        outlist.append(r'python '+scriptdir+r'ReSubmit.py '+"'"+"' '".join([icfg,fcfg,stage,ism,'Complete'])+"'")
    elif 'threept' in stage:
        outlist.append(r'python '+scriptdir+r'ReSubmit.py '+"'"+"' '".join([icfg,fcfg,stage,ism,'Complete',tsink,Proj,DS])+"'")
    elif 'gfield' in stage:
        outlist.append(r'python '+scriptdir+r'ReSubmit.py '+"'"+"' '".join([str(int(icfg)+1),fcfg,'gfield',ism,'Complete'])+"'")
    return outlist


def CreateCSHJuqeen(outfile,icfg,fcfg,ism,jobid,stage,tsink='',Proj='',DS=''):
    inputfile = InputFolder+jobid
    outputfile = OutputFolder+jobid.replace('.xml','.out')
    logfile = OutputFolder+jobid.replace('.xml','.log')
    if os.path.isfile(outputfile):os.remove(outputfile)
    if os.path.isfile(logfile):os.remove(logfile)
    icfg,fcfg,ism,tsink,Proj = str(icfg),str(fcfg),str(ism),str(tsink),str(Proj)
    outlist = []
    outlist.append(r'#! /bin/tcsh')
    outlist.append('')
    outlist.append(r'# @ job_name = '+outfile)
    outlist.append(r'# @ error = $(job_name).$(jobid).out')
    outlist.append(r'# @ output = $(job_name).$(jobid).out')
    outlist.append(r'# @ environment = COPY_ALL')
    outlist.append(r'# @ wall_clock_limit = '+time)
    outlist.append(r'# @ notification = error')
    outlist.append(r'# @ notify_user = '+email)
    outlist.append(r'# @ job_type = bluegene')
    outlist.append(r'# @ bg_size = '+str(nproc))
    outlist.append(r'# @ queue')
    outlist.append('')
    if not Submit:
        for imod in ModuleList:
            outlist.append(r'module load '+imod)
    outlist.append('')
    outlist.append(r'cd '+scriptdir)
    outlist.append('')
    if 'twopt' in stage:
        outlist.append(r'    echo "icfg='+icfg+', fcfg='+fcfg+', ism='+ism+', '+stage+' "')
    elif 'threept' in stage:
        outlist.append(r'    echo "icfg='+icfg+', fcfg='+fcfg+', ism='+ism+', t_sink='+tsink+', Proj='+Proj+', DS='+DS+', '+stage+' "')
    elif 'gfield' in stage:
        outlist.append(r'    echo "icfg='+icfg+', fcfg='+fcfg+', '+stage+' "')
    outlist.append(r'    echo "starting "`date`')
    if 'gfield' in stage:
        outlist.append(r'    runjob --ranks-per-node '+str(RPN)+' : '+chromacpu+GFexe+r' -i '+inputfile+r' -o '+outputfile+r' -l '+logfile+
                       ' -geom '+GetGeomInput()+' -iogeom '+GetIOGeomInput())
    else:
        outlist.append(r'    runjob --ranks-per-node '+str(RPN)+' : '+chromacpu+exe+r' -i '+inputfile+r' -o '+outputfile+r' -l '+logfile+
                       ' -geom '+GetGeomInput()+' -iogeom '+GetIOGeomInput())

    # outlist.append(r'    if ($? != 0) then')
    # outlist.append(r'        echo "Error with: '+inputfile+r'"')
    # outlist.append(r'        echo ""')
    # outlist.append(r'cat <<EOF >> '+paramdir+r'errlist.2ptprop')
    # outlist.append(r''+inputfile)
    # outlist.append(r'EOF')
    # if 'twopt' in stage:
    #     outlist.append(r'python '+scriptdir+r'ReSubmit.py '+"'"+"' '".join([icfg,fcfg,stage,ism,'Error'])+"'")
    # elif 'threept' in stage:
    #     outlist.append(r'python '+scriptdir+r'ReSubmit.py '+"'"+"' '".join([icfg,fcfg,stage,ism,'Error',tsink,Proj,DS])+"'")
    # elif 'gfield' in stage:
    #     outlist.append(r'python '+scriptdir+r'ReSubmit.py '+"'"+"' '".join([str(int(icfg)+1),fcfg,'gfield',ism,'Error'])+"'")
    # outlist.append(r'        exit 1')
    # outlist.append(r'    endif')
    outlist.append(r'    echo "finished "`date`')
    outlist.append('')
    if 'twopt' in stage:
        outlist.append(r'python '+scriptdir+r'ReSubmit.py '+"'"+"' '".join([icfg,fcfg,stage,ism,'Complete'])+"'")
    elif 'threept' in stage:
        outlist.append(r'python '+scriptdir+r'ReSubmit.py '+"'"+"' '".join([icfg,fcfg,stage,ism,'Complete',tsink,Proj,DS])+"'")
    elif 'gfield' in stage:
        outlist.append(r'python '+scriptdir+r'ReSubmit.py '+"'"+"' '".join([str(int(icfg)+1),fcfg,'gfield',ism,'Complete'])+"'")
    return outlist



def CreateCSHWrap(icfg,fcfg,ism,jobid,stage,tsink='',Proj='',DS=''):
    icfg,fcfg,ism,tsink,Proj = str(icfg),str(fcfg),str(ism),str(tsink),str(Proj)
    fileDS = DS.replace('doub','D').replace('sing','S')
    if 'twopt' in stage:
        outfile = cshdir+'Run'+stage+'cfg'+icfg+'sm'+ism+'.csh'
    elif 'threept' in stage:
        outfile = cshdir+'Run'+stage+'cfg'+icfg+'sm'+ism+'ts'+tsink+'P'+Proj+fileDS+'.csh'
    elif 'gfield' in stage:
        outfile = cshdir+'Run'+stage+'cfg'+icfg+'.csh'
    if 'juqueen' in thismachine:
        outlist = CreateCSHJuqueen(outfile,icfg,fcfg,ism,jobid,stage,tsink=tsink,Proj=Proj,DS=DS)
    else:
        outlist = CreateCSHList(icfg,fcfg,ism,jobid,stage,tsink=tsink,Proj=Proj,DS=DS)
    CreateCSHFile(outfile,outlist)
    return outfile

def RemoveCSH(icfg,ism,stage,tsink='',Proj='',DS=''):
    icfg,ism,tsink,Proj = str(icfg),str(ism),str(tsink),str(Proj)
    fileDS = DS.replace('doub','D').replace('sing','S')
    if 'twopt' in stage:
        outfile = cshdir+'Run'+stage+'cfg'+icfg+'sm'+ism+'.csh'
    elif 'threept' in stage:
        outfile = cshdir+'Run'+stage+'cfg'+icfg+'sm'+ism+'ts'+tsink+'P'+Proj+fileDS+'.csh'
    elif 'gfield' in stage:
        outfile = cshdir+'Run'+stage+'cfg'+icfg+'.csh'
    if os.path.isfile(outfile): os.remove(outfile)
