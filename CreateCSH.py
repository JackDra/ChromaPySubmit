#!/usr/bin/env python

import os
from RunParams import *
from MiscFuns import mkdir_p

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
    outlist.append(r'    echo "starting "`date`')
    outlist.append(r'    mpirun -np '+str(nproc)+' '+chromacpu+exe+r' -i '+inputfile+r' -o '+outputfile+r' -l '+logfile)
    outlist.append(r'    if ($? != 0) then')
    outlist.append(r'        echo "Error with: '+inputfile+r'"')
    outlist.append(r'        echo ""')
    outlist.append(r'cat <<EOF >> '+paramdir+r'errlist.2ptprop')
    outlist.append(r''+inputfile)
    outlist.append(r'EOF')
    if 'twopt' in stage:
        outlist.append(r'        python '+scriptdir+r'ReSubmit.py '+' '.join([icfg,fcfg,stage,ism,'Error']))
    elif 'threept' in stage:
        outlist.append(r'        python '+scriptdir+r'ReSubmit.py '+' '.join([icfg,fcfg,stage,ism,'Error',tsink,Proj,DS]))
    outlist.append(r'        exit 1')
    outlist.append(r'    endif')
    outlist.append(r'    echo "finished "`date`')
    outlist.append('')
    if 'twopt' in stage:
        outlist.append(r'python '+scriptdir+r'ReSubmit.py '+' '.join([icfg,fcfg,stage,ism,'Complete']))
    elif 'threept' in stage:
        outlist.append(r'python '+scriptdir+r'ReSubmit.py '+' '.join([icfg,fcfg,stage,ism,'Complete',tsink,Proj,DS]))
    return outlist



def CreateCSHWrap(icfg,fcfg,ism,jobid,stage,tsink='',Proj='',DS=''):
    outlist = CreateCSHList(icfg,fcfg,ism,jobid,stage,tsink=tsink,Proj=Proj,DS=DS)
    icfg,fcfg,ism,tsink,Proj = str(icfg),str(fcfg),str(ism),str(tsink),str(Proj)
    fileDS = DS.replace('doub','D').replace('sing','S')
    if 'twopt' in stage:
        outfile = cshdir+'Run'+stage+'cfg'+icfg+'sm'+ism+'.csh'
    else:
        outfile = cshdir+'Run'+stage+'cfg'+icfg+'sm'+ism+'ts'+tsink+'P'+Proj+fileDS+'.csh'
    CreateCSHFile(outfile,outlist)
    return outfile
    
def RemoveCSH(icfg,ism,stage,tsink='',Proj='',DS=''):
    icfg,ism,tsink,Proj = str(icfg),str(ism),str(tsink),str(Proj)
    fileDS = DS.replace('doub','D').replace('sing','S')
    if 'twopt' in stage:
        outfile = cshdir+'Run'+stage+'cfg'+icfg+'sm'+ism+'.csh'
    else:
        outfile = cshdir+'Run'+stage+'cfg'+icfg+'sm'+ism+'ts'+tsink+'P'+Proj+fileDS+'.csh'
    if os.path.isfile(outfile): os.remove(outfile)
