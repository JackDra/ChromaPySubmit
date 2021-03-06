#!/usr/bin/env python

##NB: if changing nx, or nt, MUST remove random list in ParamFiles directory
import socket
import re

Debug = False ## Debugging flag.... finnaly put it in

THISMACHINE = socket.gethostname()

# if 'juqueen' in THISMACHINE:
#     JackLibDir = '/homeb/jias40/jias4002/juqueen/Scripts/LQCDPythonAnalysis'
# elif 'JackLappy' in THISMACHINE:
#     JackLibDir = '/home/jackdra/PHD/CHROMA/TestVar/Scripts/LQCDPythonAnalysis'
#     # JackLibDir = '/home/jackdra/PHD/DataAnalysis/LQCDPythonAnalysis'
# elif 'dev' in THISMACHINE or 'gateway' in THISMACHINE or 'lac-' in THISMACHINE:
#     JackLibDir = '/mnt/home/dragosja/Scripts/LQCDPythonAnalysis'
# else:
#     JackLibDir = '../LQCDPythonAnalysis'


import os
# from shutil import copyfile
cwd = os.getcwd()



# if os.path.isfile(JackLibDir+'/setup.cfg'):copyfile(JackLibDir+'/setup.cfg', cwd+'/setup.cfg')
# print 'Running on ' , THISMACHINE

# if not os.path.isdir(JackLibDir):
#     print JackLibDir , 'not found, please set in PararmsGAM.py to point to jacks libary'
#     print 'Jacks libary can be found at https://github.com/JackDra/LQCDPythonAnalysis.git'
#     print 'Run "./Setup.py default" within the directory to set up jacks libary'
#     print 'Then make JackLibDir in RunParams.py point to correct directory'
#     sys.exit()

# sys.path.insert(0,JackLibDir)

# import errno
from MiscFuns import mkdir_p
import cPickle as pickle
import numpy as np

halfishalf = False ## runs half the jobs on half the number of nodes
Email = 'bea' ## b = begin, e = end , a = abort, Email = False Non
EmailAddress = 'jack.dragos@gmail.com'
Allkud = 1370000
OnDist = False
dash_stream = '-b-'
RunPTG = False ## Runs on our partition or not
ModuleList = []

mpirun_comm = 'mpirun'
if 'phoenix.rc' in THISMACHINE:
    thismachine = 'phoenixold'
    basedir = '/home/a1193348/'
    scratchdir = '/data/cssm/jdragos/'
    codedir = ''
    Scom = 'sbatch'
    quetype = 'batch'
    mem = '120GB'
    time = '5:00:00'
    GPU = False
    # GPU = '4'
    nproc = 4
    # nproc = 16
    nx = 32
    nt = 64
    limefolder = 'qdpxx_cpu_install'
    chromafolder = 'chroma_alex'
    chromaGPUfolder = 'chroma_gpu_nprmod_install'
    Submit = True
    it_sst = [13] ## ahnialation parameters (momenta)
elif 'phoenix' in THISMACHINE:
    thismachine = 'phoenix'
    basedir = '/home/a1193348/'
    scratchdir = '/data/cssm/jdragos/'
    codedir = ''
    Scom = 'sbatch'
    quetype = 'batch'
    mem = '120GB'
    time = '5:00:00'
    GPU = False
    # GPU = '4'
    nproc = 4
    # nproc = 16
    nx = 32
    nt = 64
    limefolder = 'qdpxx_cpu_install'
    chromafolder = 'chroma_alex'
    chromaGPUfolder = 'chroma_gpu_nprmod_install'
    Submit = True
    it_sst = [13] ## ahnialation parameters (momenta)
elif 'isaac' in THISMACHINE:
    thismachine = 'isaac'
    basedir = '/home/a1193348/'
    scratchdir = '/data/jdragos/'
    codedir = ''
    Scom = 'sbatch'
    quetype = 'batch'
    mem = '120GB'
    time = '5:00:00'
    GPU = False
    # GPU = '4'
    nproc = 4
    # nproc = 16
    nx = 32
    nt = 64
    limefolder = 'qdpxx_cpu_install'
    chromafolder = 'chroma_alex'
    chromaGPUfolder = 'chroma_gpu_nprmod_install'
    Submit = True
    it_sst = [13] ## ahnialation parameters (momenta)

elif 'JackLappy' in THISMACHINE:
    # jobtimebuffer2pt = 200 ## overestimate of length of time to complete one set of inverisons for 2 point correlators (use output files to deturmine this)
    # jobtimebuffer3pt = 4000 ## overestimate of length of time to complete one set of inverisons for 3 point correlators (use output files to deturmine this)
    # jobtimebufferflow = 1200 ## as above for flow jobs

    jobtimebuffer2pt = 0 ## overestimate of length of time to complete one set of inverisons for 2 point correlators (use output files to deturmine this)
    jobtimebuffer3pt = 0 ## overestimate of length of time to complete one set of inverisons for 3 point correlators (use output files to deturmine this)
    jobtimebufferflow = 0 ## as above for flow jobs

    mpirun_comm = 'mpirun.openmpi'
    thismachine = 'JackLappy'
    basedir = '/home/jackdra/PHD/CHROMA/TestVar/'
    scratchdir = '/home/jackdra/PHD/CHROMA/TestVar/scratch/'
    diskdir = ''
    codedir = '/home/jackdra/PHD/CHROMA/install/'
    flowdir = '/home/jackdra/PHD/CHROMA/flowOps/'
    gfdir = scratchdir+'/gaugefields/TestWeak/'
    gfdir_store = gfdir
    Scom = 'sbatch'
    quetype = 'batch'
    mem = '120GB'
    time = '5:00:00'
    # time = '00:03:25'
    GPU = False
    nGPU = '4'
    # GPU = '4'
    nproc = 32
    # nproc = 4
    RPN = 16 ## 16,32,64 threads per node, NOTE: only 16 physical cores per node.
    totproc = nproc*RPN
    # nproc = 16
    nx = 20
    nt = 40
    kud = 12 # kappa (quark hopping) params
    ks = 12
    kappastr = 'Kud0'+str(kud)+'Ks0'+str(ks)
    limename = 'Testing.lime'
    limefolder = 'qdpxx_cpu_install'
    chromafolder = 'chroma_alex'
    chromaGPUfolder = 'chroma_gpu_nprmod_install'
    Submit = False ## submits the script to the que, disable to run on local machine
    it_sst = [2] ## ahnialation parameters (momenta) MUST BE len(it_sst) == len(RVec)/PoFShifts
    MaxIter = 20
    RVec = [ 0.5,0.5,0.5 ]
    OnlyTwoPt = False ## Only calculates two-point correlation functions.

elif 'juqueen' in THISMACHINE:
    jobtimebuffer2pt = 200 ## overestimate of length of time to complete one set of inverisons for 2 point correlators (use output files to deturmine this)
    jobtimebuffer3pt = 4000 ## overestimate of length of time to complete one set of inverisons for 3 point correlators (use output files to deturmine this)
    jobtimebufferflow = 1200 ## as above for flow jobs


    thismachine = 'juqueen'
    basedir = '/homeb/jias40/jias4002/juqueen/'
    scratchdir = '/work/jias40/jias4002/juqueen/'
    diskdir = ''
    # kud = 1370000
    # kud = 1375400 # kappa (quark hopping) params
    kud = Allkud # kappa (quark hopping) params
    kudgf = str(kud/100)
    ks = 1364000
    ksgf = str(ks/1000)
    # codedir = '/homeb/jias40/jias4002/juqueen/Chroma/chroma/install_bgq_clang/'
    codedir = '/homeb/jias40/jias4002/juqueen/Chroma/chroma_bup_recomple/install/'
    # flowdir = '/homeb/jias40/jias4002/juqueen/Chroma/flowOps/'
    # flowdir = '/homeb/jias40/jias4002/juqueen/Chroma/flowOpsNew/'
    flowdir = '/homeb/jias40/jias4002/juqueen/Chroma/flowOpsEnergy/'
    # gfdir = '/work/jias40/jias4000/conf/Nf2p1/b1.9kl0.13754ks0.1364/'
    gfdir = '/work/jias40/jias4000/conf/Nf2p1/b1.9kl0.'+kudgf+'ks0.'+ksgf+'/'
    gfdir_store = gfdir
    Scom = 'llsubmit'
    quetype = 'bluegene'
    mem = ''
    # time = '23:50:00'
    # time = '11:50:00'
    time = '01:55:00'

    # time = '05:50:00'
    GPU = False
    nGPU = '4'
    # GPU = '4'
    nproc = 128
    RPN = 64 ## 16,32,64 threads per node, NOTE: only 16 physical cores per node.
    if Debug:
        time = '01:00:00'
        nproc = 256
        RPN = 32 ## 16,32,64 threads per node, NOTE: only 16 physical cores per node.

    # nproc = 16
    totproc = nproc*RPN ## number of nodes
    if RPN not in [16,32,64]: raise  EnvironmentError('RPN (ranks per node) must be 16 (physical), 32 or 64/ RPN='+str(RPN))
    # if totproc % RPN != 0: raise  EnvironmentError('nproc must be multiple of RPN/ nproc/RPN='+str(nproc)+'/'+str(RPN)+'='+str(nproc/float(RPN)))
    nx = 32
    nt = 64
    limefolder = 'qdp++'
    chromafolder = 'chroma'
    chromaGPUfolder = ''
    kappastr = 'Kud0'+str(kud)+'Ks0'+str(ks)
    # limename = 'RC'+str(nx)+'x'+str(nt)+'_B1900'+kappastr+'C1715'
    # limename = 'RC'+str(nx)+'x'+str(nt)+'_B1900'+kappastr+'C1715'+dash_stream+'00' ## for kud = 1375400
    # limename = 'RC'+str(nx)+'x'+str(nt)+'_B1900'+kappastr+'C1715'+dash_stream+'00'
    Submit = True ## submits the script to the que, disable to run on local machine
    it_sst = [13] ## ahnialation parameters (momenta)
    MaxIter = 5000
    OnlyTwoPt = False ## Only calculates two-point correlation functions.

    #Taken from
    if kud == 1375400:
        RVec = [ 0.0000005522,-0.0001589143,0.9999999874 ]
        limename = 'RC'+str(nx)+'x'+str(nt)+'_B1900'+kappastr+'C1715'+dash_stream+'00' ## for kud = 1375400
    else:
        RVec = [ 0.0000,0.000,1.0 ]
        limename = 'RC'+str(nx)+'x'+str(nt)+'_B1900'+kappastr+'C1715'+dash_stream+'00'

elif 'dev' in THISMACHINE or 'gateway' in THISMACHINE or 'lac-' in THISMACHINE:
    jobtimebuffer2pt = 200 ## overestimate of length of time to complete one set of inverisons for 2 point correlators (use output files to deturmine this)
    jobtimebuffer3pt = 4000 ## overestimate of length of time to complete one set of inverisons for 3 point correlators (use output files to deturmine this)
    jobtimebufferflow = 30000 ## as above for flow jobs
    thismachine = 'hpcc'
    ModuleList = ['GNU/6.2','OpenMPI/2.0.2','autoconf/2.69','automake/1.15','powertools/1.2','CMake/2.8.5']
    RunPTG = True ## Runs on our partition or not
    basedir = '/mnt/home/dragosja/'
    scratchdir = '/mnt/scratch/dragosja/data/'
    diskdir = '/mnt/research/lqcd/CfunAnalysis/'
    codedir = '/mnt/home/dragosja/Chroma/install/'
    flowdir = '/mnt/research/lqcd/code_new/FlowOpsAndrea/codes'
    # gfdir = '/mnt/scratch/dragosja/data/gfields/Nf2p1/b1.9kl0.13754ks0.1364/'
    kud = Allkud
    # kud = 1375400
    # kud = 1375400 # kappa (quark hopping) params
    # kud = Allkud # kappa (quark hopping) params
    kudgf = str(kud/100)
    ks = 1364000
    ksgf = str(ks/1000)
    # gfdir = '/mnt/research/lqcd/conf/Nf2p1/b1.9kl0.'+kudgf+'ks0.'+ksgf+'/'
    # if kud == 1375400:
    #     gfdir = '/mnt/scratch/shindle7/'
    # else:
        # gfdir = '/mnt/research/lqcd/conf/Nf2p1/b1.9kl0.'+kudgf+'ks0.'+ksgf+'/'
    gfdir = '/mnt/scratch/dragosja/data/gfields/Nf2p1/b1.9kl0.'+kudgf+'ks0.'+ksgf+'/'
    gfdir_store = '/mnt/research/lqcd/conf/Nf2p1/b1.9kl0.'+kudgf+'ks0.'+ksgf+'/'
    Scom = 'qsub'
    quetype = 'dev-intel16'
    mem = '512GB'
    time = '23:59:00'
    GPU = False
    nGPU = '4'
    # GPU = '4'
    nproc = 16
    halfishalf = False ## runs half the jobs on half the number of nodes
    RPN = 16 ## 16,32,64 threads per node, NOTE: only 16 physical cores per node.
    # nproc = 16
    totproc = nproc*RPN ## number of nodes
    # if RPN not in [16,32,64]: raise  EnvironmentError('RPN (ranks per node) must be 16 (physical), 32 or 64/ RPN='+str(RPN))
    # if totproc % RPN != 0: raise  EnvironmentError('nproc must be multiple of RPN/ nproc/RPN='+str(nproc)+'/'+str(RPN)+'='+str(nproc/float(RPN)))
    nx = 32
    nt = 64
    # nx = 20
    # nt = 40
    limefolder = 'qdp++'
    chromafolder = 'chroma'
    chromaGPUfolder = ''
    kappastr = 'Kud0'+str(kud)+'Ks0'+str(ks)
    # limename = 'RC'+str(nx)+'x'+str(nt)+'_B1900'+kappastr+'C1715'
    Submit = True ## submits the script to the que, disable to run on local machine
    it_sst = [13] ## ahnialation parameters (momenta)
    MaxIter = 5000
    OnlyTwoPt = True ## Only calculates two-point correlation functions.

    #set to sm64
    if kud == 1375400:
        RVec = [ 0.0000005522,-0.0001589143,0.9999999874 ]
        limename = 'RC'+str(nx)+'x'+str(nt)+'_B1900'+kappastr+'C1715'+dash_stream+'00' ## for kud = 1375400
    else:
        RVec = [ 0.0000,0.000,1.0 ]
        limename = 'RC'+str(nx)+'x'+str(nt)+'_B1900'+kappastr+'C1715'+dash_stream+'00'

    # if nx == 20:
    #     # limename = 'RC'+str(nx)+'x'+str(nt)+'_B1900'+kappastr+'C1715-1-00' ## 271 configs
    #     limename = 'RC'+str(nx)+'x'+str(nt)+'_B1900'+kappastr+'0C1715-2-00' ## 329 configs
    #     gfdir = '/mnt/scratch/dragosja/data/gfields/Nf2p1/b1.9L20kl0.'+kudgf+'ks0.'+ksgf+'/'
    #     # limename = 'RC'+str(nx)+'x'+str(nt)+'_B1900'+kappastr+'C1715-3-00' ## 100 configs
    #     # limename = 'RC'+str(nx)+'x'+str(nt)+'_B1900'+kappastr+'C1715-4-00' ## 90 configs
    kappastr = 'RC'+str(nx)+'x'+str(nt)+'_'+kappastr
else:
    raise EnvironmentError(THISMACHINE + ' is not recognised, add to RunParams.py if statement')
    # exit()

if len(codedir) == 0:
    raise EnvironmentError('No code directory set for '+thismachine+'. Go into RunParams.py and add where chroma is into codedir')

print 'Corresonds to thismachine',thismachine
ChromaFileFlag = 'params_runTwoPt_'
# runflag = '' ## Old run
runflag = 'PChroma'


ExitOnFail = True ## Reimplemented: exits if there was a failed run (on for debugging?)
DontRun = False ## creates input files but does not run (for looking at .csh and .xml files
SaveMem = True ## saves memory in run by deleting sources and propagators when not needed.
Save2ptProp = False ## Saves 2 point propagators for use in the 3 point correlator construction
AveMom2pt = True ## Averages over all 2 point propagator momenta for a Q^2
DoJsm3pt = False ## Creates n*n matrix for the three point correlators, instead of doing sequential source combination trick
DupCfgs = 100 ## random sources per gauge field
# Submit = True
#james prop gf source index parameter

totroll = 2



randlistsize = 2000

## csh run parameters (slurm)

Cexe = 'chroma'
# ModuleList = ['intel/2015c','OpenMPI/1.8.8-iccifort-2015.3.187','CUDA/7.0.28']




# lattice params, note that cube so no need for ny/nz
# nx = 32
# nt = 64
nxtvec = [nx,nx,nx,nt]
nxtstr = ' '.join(map(str,nxtvec))

GeomPicked = 'EvenSpread' ## closes npx and npt, making npt larger of the two
# GeomPicked = 'Tsplit'
# GeomPicked = 'Spacesplit'

Seed1,Seed2,Seed3,Seed4 = 11,11,11,0
# SRCX = [ 0, 16,  0, 16,  0,  0, 16, 16, 16, 16 ]#0  0  0 16  0 16 )
# SRCY = [ 0, 16,  0,  0, 16, 16,  0,  0, 16, 16 ]#0 16 16  0  0 16 )
# SRCZ = [ 0, 16,  0, 16,  0, 16,  0, 16,  0, 16 ]#16  0 16  0 16  0 )
# SRCT = [ 0,  4, 32, 60, 24, 48, 12, 28, 20, 36 ]#40 56 16 44  8 52 )

##### WARNING, if OnlyTwoPt = True, please set DoJsm3pt = False #####
# OnlyTwoPt = True ## Only calculates two-point correlation functions.
if OnlyTwoPt: DoJsm3pt = False

OnlyGauge = False ## Only calculates Gauge field
# OnlyGauge = False ## Only calculates Gauge Field
NumGFCreate = 100
# GFFormat = 'ILDG'
# GFFormat = 'UNIT'
# GFFormat = 'SZIN'
GFFormat = 'SZINQIO'

# GFFormat = 'WEAK_FIELD'


##RVec must be len(smlist) * PoFShifts
#Taken from /home/accounts/jdragos/scripts/PythonAnalysis/REvecSave/k12090/PoF1to16dt2LREM.txt
# RVec = [ 76.3260613436,  -161.5448230802, 264086.1917824702, -321.4016231030, 4390.5310121576, -893677.8525444396 ]

# #Taken mokup
# RVec = [ 1  ]


# Testing, should be same as tsink sm128
# RVec = ( 0.0 0.0 0.0 0.0 0.0 1.0 )

##n.b. PoFShifts = 1 means 1 tsink value (so no PoF)
# PoFShifts = 1
# PoFDelta = 2
PoFShifts = 0
PoFDelta = 1
PoFList = range(0,PoFShifts*PoFDelta+1,PoFDelta)

REvecFlag = '' ## flag for identiftying variational method parameters (only in filename, not acutally needed)'
# REvecFlag = 'REPoFto16dt2'
# REvecFlag = 'REPoFTest'
####COLA PARAMETERS

# Propagator Params
# it = 16 # creation parameters
# ix = 1 #put at ix,ix,ix
# kud = 121040 # kappa (quark hopping) params
# ks = 120620
# kud = 120900 # kappa (quark hopping) params
# ks = 120900
# Prec = '1.0d-5'
# Prec = '5.0e-11'
Prec = '1.0e-8'
# Projector = 4
GammaRep = 'sakurai'
ProjectorList = [4,3]
DSList = ['doub','sing']

ParaIO = 'true'


### GAUGEFIELD GENERATION PARAMETERS ###

GaugeType = 'purgaug'
GFexe = GaugeType
Flowexe = 'flowChroma'

if OnlyGauge:
    exe = GFexe
    GFFormat = 'WEAK_FIELD'
else:
    exe = Cexe



StartUpdateNum = 0
NWarmUpUpdates = 2
NProductionUpdates = 1000
NUpdatesThisRun = 1000
SaveInterval = 5

GActName = 'WILSON_GAUGEACT'
beta = '6.0'
# anisoP = 'true'
anisoP = 'false'
t_dir ='3'
# xi_0 ='2.464'
xi_0 ='1.0'
GFnu = '1.0'
GaugeBC = 'PERIODIC_GAUGEBC'
nOver = '3'
NmaxHB = '1'

#### Flow Parameters ###

flow_steps = 1000
totflow_time = 10

Do_Wflow = 'true'
FlowOrderWein = 6
kflowWein = '0.0'

Do_Qflow = 'true'
FlowOrderQtop = 6
kflowQtop = '0.0'

Do_Eflow = 'false'
FlowOrderE = 6
kflowE = '0.0'


flow_fermions = False
flowed_meson_Gamma = '15'
calc_freq = 4
if flow_fermions:
    calc_Adj = 'true' ## i think this is broken, must be on
else:
    calc_Adj = 'false' ## i think this is broken, must be on

## The nb and ns flags are related to parameters in Luscher's Hierarchical scheme,
## which he defines in Appendix E.4 of http://inspirehep.net/record/1220572
mes_flow_nb = 2
mes_flow_ns = 4


GFPrec = '5.0e-5'
GFMaxIter = 200
GFDoOr = 'false'
GFOrPara = '1.0'

def ModuloT(itsrc):
    if itsrc >= nt:
        itsrc = itsrc - nt
    return itsrc


def ModuloTsrc(icfg,iPoF):
    itsrc = int(SRCT[icfg])+int(iPoF)
    # if itsrc < 0:
    #     itsrc = itsrc+nt
    if itsrc >= nt:
        itsrc = itsrc - nt
    return itsrc

def GetSourceString(icfg,iPoF=0):
    return str(SRCX[icfg]) + ' ' + str(SRCY[icfg]) + ' ' + str(SRCZ[icfg]) + ' ' + str(ModuloTsrc(icfg,iPoF))
    ##DEBUGGING STUFF##
    # return str(SRCX[icfg]) + ' ' + str(SRCY[icfg]) + ' ' + str(SRCZ[icfg]) + ' ' + str(iPoF)
    # return str(SRCX[icfg]) + ' ' + str(SRCY[icfg]) + ' ' + str(SRCZ[icfg]) + ' ' + str(int(iPoF)+4)
    # return str(SRCX[icfg]) + ' ' + str(SRCY[icfg]) + ' ' + str(SRCZ[icfg]) + ' ' + str(it)


def DStoUD(DS):
    if 'doub' in DS:
        return 'U'
    elif 'sing' in DS:
        return 'D'
    else:
        return ''

def ProjToPol(Proj):
    if int(Proj) < 4:
        return 'POL'
    elif int(Proj) == 4:
        return 'UNPOL'
    else:
        return ''


def TimeInSeconds(time,as_str=True):
    hours,minutes,seconds = map(int,time.split(':'))
    secondtime = seconds + minutes*60 + hours*3600
    if as_str:
        return str(secondtime)
    else:
        return secondtime


secondstime = TimeInSeconds(time,as_str=False)
jobseconds2pt = str(secondstime - jobtimebuffer2pt)
jobseconds3pt = str(secondstime - jobtimebuffer3pt)
flowjobseconds = str(secondstime - jobtimebufferflow)


# FermAct = 'UNPRECONDITIONED_SLRC'
FermAct = 'CLOVER'
# FermAct = 'SLRC'
invType = 'BICGSTAB_INVERTER'

# SST Propagator Parameters
# it_sst = '32 35 38' ## ahnialation parameters (momenta)
# it_sst = [26, 27, 28, 29, 30] ## ahnialation parameters (momenta)
ppvec = [0,0,0]
ppstr = ' '.join(map(str,ppvec))
qmin = 0
# qmax = 9
qmax = 4
phases = '0 0 0'
phasedirs = '0 1 2'

NDer = 0 ## seems like only working for no derivatives
NDerList = ['NDer'+str(ider) for ider in range(NDer+1)]

# Sm Parameters
SmSourceType = 'SHELL_SOURCE'
def GetSmSeqSourceType(interp,DS,Proj):
    # return interp.replace('nucleon','nucl').upper()+'_'+DStoUD(DS).upper()+'_'+ProjToPol(Proj)+'_NONREL'
    return interp.replace('nucleon','nucl').upper()+'_'+DStoUD(DS).upper()+'_'+ProjToPol(Proj)
SmSinkType = 'SHELL_SINK'
# SmKind = 'GAUGE_INV_JACOBI'
SmKind = 'GAUGE_INV_GAUSSIAN'
alpha = 0.7
StoutLink = 'T'
alphaStout = 0.1
gfsweeps = 4
smu0 = 1.0
smvalues = [16, 32, 64, 'V0']
ismlist = smvalues[:-1]
jsmlist = smvalues[:-1]
# ismlist = smvalues[:-1]
# ismlist = [smvalues[-2]] ## largest smearing at source
# jsmlist = smvalues[:-1]


# twoptinterps = 'nucleon nucleon2 nucleon_nucleon2 nucleon2_nucleon'
twoptinterps = ['nucleon']

# REvecFlag = 'REvec'
##PUT RESum##to####

# Boundary Conditions (clover)
FermBC = 'SIMPLE_FERMBC'
bx = 1.0
by = 1.0
bz = 1.0
bt = -1.0
anti_t = 'false'
if bt == -1: anti_t = 'true'
# boundstr = str(bx) + ' ' +str(by) + ' ' +str(bz) + ' ' +str(bt)
boundstr = str(int(bx)) + ' ' +str(int(by)) + ' ' +str(int(bz)) + ' ' +str(int(bt))
u0 = 1.0
# csw = 2.65
# csw = 1.0
csw = 1.715
print 'csw set to ', csw, ' please check this!'
rho = 0.1
nstout = 1

OutXml = True


# Configuration data
# limename = 'qcdsf'
# ensemble = 'b5p50kp'+str(kud)+'kp'+str(ks)

#### configuration/file parameters
scriptdir = basedir+'Scripts/Chroma_Py_Submit/'
if scriptdir[:-1] not in os.getcwd():
    print 'Warning, you are not running from the script dir'
nodeoutputdir = scriptdir+ 'NodeOutput/'+ChromaFileFlag+'/'
cshdir = scriptdir+'CSHFiles/'
paramdir = scriptdir+'ParamFiles/'
FlowDoneList = paramdir+limename+'_DoneList.txt'
indexfilename = 'cfgindicies.list'
datadir = scratchdir
InputFolderPref = 'InputFiles'
InputFolder = scriptdir+InputFolderPref+'/'
OutputFolderPref = 'OutputFiles'
OutputFolder = scriptdir+OutputFolderPref+'/'
# gfdi r= scratchdir+'/gaugefields/qcdsf.655/'
# gfdir = scratchdir+'/gaugefields/TestWeak/'
# rdsigfdir = '/data/jzanotti/confs/32x64/b5p50kp121040kp120620/'
# rdsigfdir = scratchdir+'/gaugefields/limes/
# ##for heavier kappa
# rdsigfdir = scratchdir+'/gaugefields/qcdsf.655/'
# gfdir = '/rdsi/PACS-CS/ensemble+'/'
qpdir = scratchdir+'/qprops/'+kappastr+'/'
flowdirout = scratchdir+'/Flow/'+kappastr+dash_stream+'/'
data_flowdirout = diskdir+'/Flow/'+kappastr+dash_stream+'/'
cfdir = scratchdir+'/cfun'+runflag+'/'+kappastr+'/twoptRandT/'
cf3ptdir = scratchdir+'/cfun'+runflag+'/'+kappastr+'/threept/'

debugdir = scratchdir+'/debug/'+kappastr+'/'
tempdir = '/tmp/'
filelists = paramdir

chromacpu = codedir+'/'+chromafolder+'/bin/'
Flowchromacpu = flowdir+'/'

# print 'DEBUGGING, Check this line when runing on cluster!!'
# chromacpu = '/home/jackdra/PHD/CHROMAnew/install/chroma/bin/'
# Flowchromacpu = '/home/jackdra/PHD/CHROMAnew/src/flowOps/'

chromagpu = codedir+'/'+chromaGPUfolder+'/bin/'
limedir = codedir+'/'+limefolder+'/bin/'

# gfnum = `head -n $icfg ${filelists}${cfglist} | tail -n 1`
# cfg = ensemble+str(gfnum)
# limecfg = limename+str(gfnum)+'.lime'

# cfglist = "cfglist"+thismachine+str(gfosnum)
# cfdir3pt = scratchdir+'/cfun/2ndk'+str(kud)+'/source'+str(gfosnum)+'/'

cfgfile = "cfglist"+thismachine+'.txt'


##Make directories

mkdir_p(datadir)
mkdir_p(nodeoutputdir)
mkdir_p(InputFolder)
mkdir_p(OutputFolder)
# mkdir_p(gfdir)
mkdir_p(qpdir)
mkdir_p(cfdir)
# mkdir_p(cfdir3pt)
# mkdir_p(tempdir)
mkdir_p(debugdir)
mkdir_p(cshdir)
mkdir_p(paramdir)
# mkdir_p(rdsigfdir)


def ReadRands(fflag,rsize,thisnx,thisnt):
    thispfile = paramdir+fflag+'.rlist.p'
    if not os.path.isfile(thispfile):
        intx,inty,intz = np.random.randint(0,thisnx,(3,rsize))
        intt = np.random.randint(0,thisnt,(rsize))
        with open( thispfile, "wb" ) as pfile:
            pickle.dump( [intx,inty,intz,intt], pfile )
    with open(thispfile,'rb') as pfile:
        outdata = pickle.load( pfile )
    return outdata

## Time is shifted away from nt as the PoF will wrap around the boundary
## anti-periodic boundary contitions make it weird, so I avoid it.
SRCX,SRCY,SRCZ,SRCT = ReadRands(ChromaFileFlag,randlistsize,nx,nt-(PoFShifts*PoFDelta))

SRCX2,SRCY2,SRCZ2,SRCT2 = ReadRands(ChromaFileFlag+'Ext',randlistsize*10,nx,nt-(PoFShifts*PoFDelta))

SRCX = SRCX.tolist()+SRCX2.tolist()
SRCY = SRCY.tolist()+SRCY2.tolist()
SRCZ = SRCZ.tolist()+SRCZ2.tolist()
SRCT = SRCT.tolist()+SRCT2.tolist()

def CreateGFnum(icfg):
    if not os.path.isfile(filelists+cfgfile):
        raise IOError(filelists+cfgfile + ' not found, run cfglist creation script')
    with open(filelists+cfgfile,'r') as f:
        thisfile = f.readlines()
        if len(thisfile) == 0: return 'Null','_xsrc-1'
        if len(thisfile) <= icfg:
            icfg = icfg - len(thisfile)
        thisgfnum = thisfile[icfg].replace('\n','')
    return re.sub(r'_xsrc.*','',thisgfnum),re.findall(r'_xsrc.*',thisgfnum)[0]
# def CreateCfg(icfg):
#     return ensemble+CreateGFnum(icfg)

# def CreateLimeCfg(icfg):
#     return limename+CreateGFnum(icfg)+'.lime'

def CreateCfg(icfg,DelLime=False,Flow=False):
    # return limename+CreateGFnum(icfg)+'.lime'
    # return limename+'.lime'+CreateGFnum(icfg)
    if Flow:
        return limename+str(icfg),''
    else:
        gfnum,xsrc = CreateGFnum(icfg)
        return limename+gfnum,xsrc
