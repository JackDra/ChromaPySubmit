#!/usr/bin/env python

# from RunParams import *
from RunParams import GeomPicked
from RunParams import nt,nx,totproc
from RunParams import quetype,time,EmailAddress
from RunParams import Scom,GPU,mem,Email,RPN
from RunParams import nGPU,thismachine,RunPTG,Submit
from RunParams import ModuleList,InputFolder,OutputFolder
from RunParams import jobseconds2pt,jobseconds3pt,nproc,nodeoutputdir
from RunParams import mpirun_comm,chromacpu,exe,scriptdir,OnlyTwoPt
from RunParams import Debug,cshdir,Flowchromacpu,Flowexe,flowjobseconds
from RunParams import FlowDoneList
# from MiscFuns import mkdir_p,Elongate
import os
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
    if len(geomlist) == 0:
        return '1 1 1 1'
        # raise IOError('No Geometries are allowable by the choice of nx, nt, nproc and RPN')
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
    if len(geomlist) == 1:
        print '1 1 1 1'
        # raise IOError('ParaIO cannot be done on this choise of nx, nt, nproc and RPN')
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

def MakeName(stage,icfg,fcfg):
    if 'twopt' in stage:
        return '2p-'+str(icfg)+'-'+str(fcfg)
    elif 'threept' in stage:
        return '3p-'+str(icfg)+'-'+str(fcfg)

def GetCSHHeader(Jstring,thisnproc):
    outlist = []
    outlist.append(r'#! /bin/tcsh')
    outlist.append('')
    if quetype == 'bluegene':
        outlist.append(r'# @ job_name = '+Jstring)
        outlist.append(r'# @ error = $(job_name).$(jobid).out')
        outlist.append(r'# @ output = $(job_name).$(jobid).out')
        outlist.append(r'# @ environment = COPY_ALL')
        outlist.append(r'# @ wall_clock_limit = '+time)
        outlist.append(r'# @ notification = error')
        outlist.append(r'# @ notify_user = '+EmailAddress)
        outlist.append(r'# @ job_type = bluegene')
        outlist.append(r'# @ bg_size = '+str(thisnproc))
        outlist.append(r'# @ queue')
    else:
        if Scom == 'sbatch':
            outlist.append(r'#SBATCH -p '+quetype)
            outlist.append(r'#SBATCH -n '+str(thisnproc))
            outlist.append(r'#SBATCH --time='+time)
            if GPU != False:
                outlist.append(r'#SBATCH --gres=gpu:'+GPU)
            outlist.append(r'#SBATCH --mem='+mem)
        elif Scom == 'qsub':
            if Email != False:
                outlist.append(r'#PBS -m '+Email)
                outlist.append(r'#PBS -M '+EmailAddress)
            outlist.append(r'#PBS -l walltime='+time+',nodes='+str(thisnproc)+':ppn='+str(RPN)+',mem='+mem)
            if GPU != False:
                outlist.append(r'#PBS --gres gpu:'+nGPU)
            outlist.append(r'#PBS -N '+Jstring)
            if thismachine == 'hpcc':
                if RunPTG:
                    outlist.append(r'#PBS -A ptg')
                else:
                    outlist.append(r'#PBS -A hpccdefault')
    outlist.append('')
    if len(ModuleList) > 0:
        outlist.append('module purge')
        for imod in ModuleList:
            outlist.append(r'module load '+imod)
    outlist.append('')
    return outlist

def CreateCSHList(cfgindicies,icfg,fcfg,jobidlist,stage,thisnproc,othree):
    inputfilelist = [InputFolder+jobid for jobid in jobidlist]
    outputfilelist = [OutputFolder+jobid.replace('.xml','.out') for jobid in jobidlist]
    logfilelist = [OutputFolder+jobid.replace('.xml','.log') for jobid in jobidlist]
    icfg,fcfg = str(icfg),str(fcfg)
    # Jstring = MakeName(stage,icfg,fcfg)
    if 'twopt' in stage:
        jobseconds = jobseconds2pt
    else:
        jobseconds = jobseconds3pt
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
    outlist.append(r'module purge')
    for imod in ModuleList:
        outlist.append(r'module load '+imod)
    outlist.append('')
    outlist.append(r'cd '+nodeoutputdir)
    outlist.append('')

    outlist.append(r'echo "icfg='+icfg+', fcfg='+fcfg+', '+stage+' "')

    outlist.append(r'set start = `date +%s`')
    for inputfile,outputfile,logfile,thiscfg in zip(inputfilelist,outputfilelist,logfilelist,cfgindicies):
        if os.path.isfile(outputfile):os.remove(outputfile)
        if os.path.isfile(logfile):os.remove(logfile)
        outlist.append(r'    echo "thiscfg='+str(thiscfg)+' starting "`date`')
        outlist.append(r'    '+mpirun_comm+' -np '+str(nproc)+' '+chromacpu+exe+r' -i '+inputfile+r' -o '+outputfile+r' -l '+logfile+
                       ' -geom '+GetGeomInput()+' -iogeom '+GetIOGeomInput())

        outlist.append(r'    echo ""')
        outlist.append(r'    echo "last command had return value: $?"')
        outlist.append(r'    set end = `date +%s`')
        outlist.append(r'    set curr = `expr $end - $start`')
        outlist.append(r'    echo "been running for $curr seconds, cut off time is '+jobseconds+'"')
        outlist.append(r'    if ( `echo "$curr > '+jobseconds+'" | bc` ) then')
        outlist.append(r'        echo "Time ran out, resubmitting same script "')
        outlist.append(r'        python '+scriptdir+r'ReSubmit.py '+"'"+"' '".join([icfg,fcfg,stage,str(othree),str(thisnproc)])+"'")
        outlist.append(r'        exit 2')
        outlist.append(r'    endif')
        outlist.append(r'    if ($? != 0) then')
        outlist.append(r'        echo "Job Crashed, error code $? , exiting"')
        outlist.append(r'        exit 1')
        outlist.append(r'    endif')
        outlist.append(r'    echo ""')
        outlist.append(r'')

    outlist.append(r'    echo "finished "`date`')
    if 'twopt' in stage and not OnlyTwoPt:
        outlist.append('')
        outlist.append(r'python '+scriptdir+r'ReSubmit.py '+"'"+"' '".join([icfg,fcfg,stage,str(othree),str(thisnproc)])+"'")
    return outlist



def CreateCSHJuqueen(cfgindicies,outfile,icfg,fcfg,jobidlist,stage,thisnproc,othree):
    inputfilelist = [InputFolder+jobid for jobid in jobidlist]
    outputfilelist = [OutputFolder+jobid.replace('.xml','.out') for jobid in jobidlist]
    logfilelist = [OutputFolder+jobid.replace('.xml','.log') for jobid in jobidlist]
    icfg,fcfg = str(icfg),str(fcfg)
    Jstring = MakeName(stage,icfg,fcfg)
    if 'twopt' in stage:
        jobseconds = jobseconds2pt
    elif 'threept' in stage:
        jobseconds = jobseconds3pt
    elif 'Comb' in stage:
        jobseconds = jobseconds2pt+jobseconds3pt ## this needs changing XO
    else:
        raise IOError('stage type not recognised')


    outlist = GetCSHHeader(Jstring,thisnproc)
    outlist.append(r'cd '+nodeoutputdir)
    outlist.append('')
    # if 'hpcc' in thismachine:
    #     outlist.append('export OMP_NUM_THREADS='+str(RPN))
    #     outlist.append('')

    outlist.append(r'echo "icfg='+icfg+', fcfg='+fcfg+', '+stage+' "')

    outlist.append(r'set start = `date +%s`')
    for inputfile,outputfile,logfile,thiscfg in zip(inputfilelist,outputfilelist,logfilelist,cfgindicies):
        if os.path.isfile(outputfile):os.remove(outputfile)
        if os.path.isfile(logfile):os.remove(logfile)
        outlist.append(r'    echo "thiscfg='+str(thiscfg)+' starting "`date`')
        if quetype == 'bluegene':
            if Debug:
                outlist.append(r'    runjob --verbose 4 --ranks-per-node '+str(RPN)+' : '+chromacpu+exe+r' -i '+inputfile+r' -o '+outputfile+r' -l '+logfile+
                               ' -geom '+GetGeomInput()+' -iogeom '+GetIOGeomInput())
            else:
                outlist.append(r'    runjob --ranks-per-node '+str(RPN)+' : '+chromacpu+exe+r' -i '+inputfile+r' -o '+outputfile+r' -l '+logfile+
                               ' -geom '+GetGeomInput()+' -iogeom '+GetIOGeomInput())
        else:
            outlist.append(r'    '+mpirun_comm+' -np '+str(RPN*thisnproc)+' '+chromacpu+exe+r' -i '+inputfile+r' -o '+outputfile+r' -l '+logfile+
                           ' -geom '+GetGeomInput()+' -iogeom '+GetIOGeomInput())
        outlist.append(r'    set end = `date +%s`')
        outlist.append(r'    set curr = `expr $end - $start`')
        outlist.append(r'    echo "been running for $curr seconds"')
        outlist.append(r'    if ( `echo "$curr > '+jobseconds+'" | bc` ) then')
        outlist.append(r'        echo "Time ran out, resubmitting same script "')
        if 'Comb' in stage:
            outlist.append(r'        python '+scriptdir+r'ReSubmit.py '+"'"+"' '".join([icfg,fcfg,str(thisnproc)])+"'")
        else:
            outlist.append(r'        python '+scriptdir+r'ReSubmit.py '+"'"+"' '".join([icfg,fcfg,stage,str(othree),str(thisnproc)])+"'")
        outlist.append(r'        exit 2')
        outlist.append(r'    endif')
        outlist.append(r'    if ($? != 0) then')
        outlist.append(r'        echo "Job Crashed, error code $? , exiting"')
        outlist.append(r'        exit 1')
        outlist.append(r'    endif')
        outlist.append(r'')

    outlist.append(r'    echo "finished "`date`')
    # outlist.append(r'    if ($? != 0) then')
    # outlist.append(r'        echo "Error with: '+inputfile+r'"')
    # outlist.append(r'        echo ""')
    # outlist.append(r'cat <<EOF >> '+paramdir+r'errlist.'+stage)
    # outlist.append(r''+inputfile)
    # outlist.append(r'EOF')
    # outlist.append(r'python '+scriptdir+r'ReSubmit.py '+"'"+"' '".join([nextcfg,fcfg,stage,ism,'Error'])+"'")
    # outlist.append(r'        exit 1')
    # outlist.append(r'    endif')
    # nextcfg = icfg
    # if 'gfield' in stage: nextcfg = str(int(icfg)+1)
    if 'twopt' in stage and not OnlyTwoPt:
        outlist.append('')
        outlist.append(r'python '+scriptdir+r'ReSubmit.py '+"'"+"' '".join([icfg,fcfg,stage,str(othree),str(thisnproc)])+"'")
    return outlist



def CreateCSHWrap(cfgindicies,icfg,fcfg,jobid,stage,thisnproc,othree):
    icfg,fcfg = str(icfg),str(fcfg)
    if 'gfield' in stage:
        outfile = cshdir+'Run'+stage+'.csh'
    else:
        outfile = cshdir+'Run'+stage+'cfg'+icfg+'fcfg'+fcfg+'.csh'
    if 'juqueen' in thismachine or 'hpcc' in thismachine:
        outlist = CreateCSHJuqueen(cfgindicies,outfile,icfg,fcfg,jobid,stage,thisnproc,othree)
    else:
        outlist = CreateCSHList(cfgindicies,icfg,fcfg,jobid,stage,thisnproc,othree)
    CreateCSHFile(outfile,outlist)
    return outfile

def RemoveCSH(icfg,ism,stage):
    icfg,ism = str(icfg),str(ism)
    if 'gfield' in stage:
        outfile = cshdir+'Run'+stage+'cfg'+icfg+'.csh'
    else:
        outfile = cshdir+'Run'+stage+'cfg'+icfg+'sm'+ism+'.csh'
    if os.path.isfile(outfile): os.remove(outfile)





def CreateFlowCSHWrap(cfgindicies,jobid,thisnproc,ijob,njobs):
    outfile = cshdir+'RunFlow'+str(cfgindicies[0])+'-'+str(cfgindicies[-1])+'.csh'
    outlist = CreateFlowCSH(cfgindicies,outfile,jobid,thisnproc,ijob,njobs)
    CreateCSHFile(outfile,outlist)
    return outfile


def CreateFlowCSH(cfgindicies,outfile,jobidlist,thisnproc,ijob,njobs):
    inputfilelist = [InputFolder+jobid for jobid in jobidlist]
    outputfilelist = [OutputFolder+jobid.replace('.xml','.out') for jobid in jobidlist]
    logfilelist = [OutputFolder+jobid.replace('.xml','.log') for jobid in jobidlist]
    Jstring = 'QWJob'+str(cfgindicies[0])+'-'+str(cfgindicies[-1])
    outlist = GetCSHHeader(Jstring,thisnproc)
    outlist.append(r'cd '+nodeoutputdir)
    outlist.append('')

    # if 'hpcc' in thismachine:
    #     outlist.append('export OMP_NUM_THREADS='+str(RPN))
    #     outlist.append('')
    outlist.append(r'set start = `date +%s`')

    for inputfile,outputfile,logfile,thiscfg in zip(inputfilelist,outputfilelist,logfilelist,cfgindicies):
        if os.path.isfile(outputfile):os.remove(outputfile)
        if os.path.isfile(logfile):os.remove(logfile)
        outlist.append(r'    echo "thiscfg='+str(thiscfg)+' starting "`date`')
        if quetype == 'bluegene':
            outlist.append(r'    runjob --ranks-per-node '+str(RPN)+' : '+Flowchromacpu+Flowexe+r' -i '+inputfile+r' -o '+outputfile+r' -l '+logfile+
                           ' -geom '+GetGeomInput()+' -iogeom '+GetIOGeomInput())
        else:
            outlist.append(r'    '+mpirun_comm+' -np '+str(RPN*thisnproc)+' '+Flowchromacpu+Flowexe+r' -i '+inputfile+r' -o '+outputfile+r' -l '+logfile+
                           ' -geom '+GetGeomInput()+' -iogeom '+GetIOGeomInput())
        outlist.append(r'    set end = `date +%s`')
        outlist.append(r'    set curr = `expr $end - $start`')
        outlist.append(r'    echo "been running for $curr seconds"')
        outlist.append(r'    if ( `echo "$curr > '+flowjobseconds+'" | bc` ) then')
        outlist.append(r'        echo "Time ran out, resubmitting same script "')
        outlist.append(r'        python '+scriptdir+'FlowSubmit.py '+ijob)
        outlist.append(r'        exit 1')
        outlist.append(r'    endif')
        outlist.append(r'    if ($? != 0) then')
        outlist.append(r'        echo "Job Crashed, error code $? , exiting"')
        outlist.append(r'        exit 1')
        outlist.append(r'    endif')
        outlist.append(r'')
        outlist.append('echo "'+str(thiscfg)+'" >> '+FlowDoneList)
    outlist.append(r'    echo "finished "`date`')
    return outlist
