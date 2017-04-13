#!/usr/bin/env python

from RunParams import *
from CreateCfgFile import *
from CreateChromaFiles import *
from GetAndCheckData import *
from ReSubmit import RunNext
import sys
import subprocess
import numpy as np

njobs = -1
forcecfg = False
ncfg = False
nsrc = DupCfgs
FromFile = False
startcfg = 0
nppick = False
OnlyThree = False
for iin in sys.argv[1:]:
    if '-h' in iin:
        print ''
        print '-np=#             Specifies number of jobs to submit to the cluster'
        print '-ncfg=#           Specify number of gauge fields (default behaviour is to use all gauge fields)'
        print '                  NOTE: code does maximal distance between numbered gauge fields, i.e. -ncfg=100 for total 200 skips every second gauge field.'   
        print '-nsrc=#           Number of sources to calculate per gauge field (default is 100 which is max supported [change DupCfgs in ./RunParams.py to larger if need])'
        print ''
        print '-nppick=#,#,...   Only submit jobs # to the cluster (used for resubmitting single jobs that crash'
        print '-OnlyThree        Flag to only calculate the remaining 3-point correlators (usefull for finishing off runs early)'
        print '-startcfg=#       Can be used to set the start configuration (default =0)'
        print '-fromfile         Can be specified to be True to use the already generated configuration list in ./ParamFiles/cfglistMACHINENAME.txt'
        print ''
        print 'Example:  ./Submit.py -np=10 -nsrc=20 -ncfg=100'
        print 'Will produce 20 sources for all of 100 cfgs. The total 2000 measurements will then be split up over 10 jobs'
        print ''
        sys.exit()
    if '-np=' in iin:
        njobs = int(iin.replace('-np=',''))
    elif '-startcfg=' in iin:
        startcfg = int(iin.replace('-startcfg=',''))
    elif '-ncfg=' in iin:
        ncfg = int(iin.replace('-ncfg=',''))
    elif '-nsrc=' in iin:
        nsrc = int(iin.replace('-nsrc=',''))
    elif '-fromfile' in iin:
        FromFile = True
    elif '-nppick' in iin:
        nppick = map(int,iin.replace('-nppick=','').split(','))
    elif '-onlythree' in iin or '-justthree' in iin:
        OnlyThree = True
        
        
if njobs == -1:
    raise IOError('please give number of processors as -np=## ')
if nppick == False: nppick = range(1,njobs+1)
    
print 'Number of jobs = ' , njobs

# if sys.argv[2] == 'a':
#     thisgfosnum = range(1,10)
# else:
#     thisgfosnum = map(int,sys.argv[2:])
# nproc = int(sys.argv[1])


# np.array([ithisc+'\n' for ithisc in thiscfglist]).tofile(cfgfile)

thiscfglist,totncfg = CreateCfgList(njobs,FromFile=FromFile)

if ncfg == False:
    ncfg = totncfg
cfgindicies = GetCfgIndicies(totncfg,ncfg,nsrc,startcfg)



# if forcecfg == False:
cfgintervals = GetIcfgTOFcfg(njobs,ncfg*nsrc )
for iin,(icfg,fcfg) in enumerate(cfgintervals):
    if iin+1 in nppick:
        thisnproc = nproc
        if iin >= len(cfgintervals)/2 and halfishalf: thisnproc=nproc/2
        print 'Submitting icfg='+str(icfg)+' fcfg='+str(fcfg)    
        RunNext(icfg,fcfg,'twoptcorr',OnlyThree,thisnproc,cfgindicies=cfgindicies)
# else:
#     RunNext(forcecfg[0],forcecfg[1],Start=True,cfgindicies=cfgindicies)
        
