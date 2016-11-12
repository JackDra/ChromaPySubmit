#!/usr/bin/env python

##NB: if changing nx, or nt, MUST remove random list in ParamFiles directory

JackLibDir = '/homeb/jias40/jias4002/juqueen/Scripts/LQCDPythonAnalysis'
import os, sys

if not os.path.isdir(JackLibDir):
    print JackLibDir , 'not found, please set in PararmsGAM.py to point to jacks libary'
    print 'Jacks libary can be found at https://github.com/JackDra/LQCDPythonAnalysis.git'
    print 'Run "./Setup.py default" within the directory to set up jacks libary'
    print 'Then make JackLibDir in RunParams.py point to this directory'
    sys.exit()

sys.path.append(JackLibDir)

import errno
import socket
from MiscFuns import mkdir_p
import cPickle as pickle
import numpy as np


email = 'jack.dragos@gmail.com'
THISMACHINE = socket.gethostname()

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
elif 'JackLappy' in THISMACHINE:
    thismachine = 'JackLappy'
    basedir = '/home/jackdra/PHD/CHROMA/TestVar/'
    scratchdir = '/home/jackdra/PHD/CHROMA/TestVar/scratch/'
    codedir = '/home/jackdra/PHD/CHROMA/install/'
    Scom = 'sbatch'
    quetype = 'batch'
    mem = '120GB'
    time = '5:00:00'
    GPU = False
    # GPU = '4'
    nproc = 4
    # nproc = 4
    RPN = 1 ## 16,32,64 threads per node, NOTE: only 16 physical cores per node.
    totproc = nproc*RPN
    # nproc = 16
    nx = 4
    nt = 8
    limefolder = 'qdpxx_cpu_install'
    chromafolder = 'chroma_alex'
    chromaGPUfolder = 'chroma_gpu_nprmod_install'
elif 'juqueen' in THISMACHINE:
    thismachine = 'juqueen'
    basedir = '/homeb/jias40/jias4002/juqueen/'
    scratchdir = '/work/jias40/jias4002/juqueen/'
    codedir = '/homeb/jias40/jias4002/juqueen/Chroma/chroma/install_bgq_clang/'
    Scom = 'llsubmit'
    quetype = 'bluegene'
    mem = ''
    time = '00:29:00'
    GPU = False
    # GPU = '4'
    nproc = 128 ## number of nodes
    RPN = 16 ## 16,32,64 threads per node, NOTE: only 16 physical cores per node.
    totproc = nproc*RPN
    # nproc = 16
    if RPN not in [16,32,64]: raise  EnvironmentError('RPN (ranks per node) must be 16 (physical), 32 or 64/ RPN='+str(RPN))
    if nproc % RPN != 0: raise  EnvironmentError('nproc must be multiple of RPN/ nproc/RPN='+str(nproc)+'/'+str(RPN)+'='+str(nproc/float(RPN)))
    nx = 32
    nt = 64
    limefolder = 'qdp++'
    chromafolder = 'chroma'
    chromaGPUfolder = ''
else:
    raise EnvironmentError(THISMACHINE + ' is not recognised, add to RunParams.py if statement')
    # exit()

if len(codedir) == 0:
    raise EnvironmentError('No code directory set for '+thismachine+'. Go into RunParams.py and add where chroma is into codedir')

ChromaFileFlag = 'params_run1_'

ExitOnFail = False
Submit = False
DontRun = True

# Submit = True
#james prop gf source index parameter




randlistsize = 2000

## csh run parameters (slurm)

exe = 'chroma'
# ModuleList = ['intel/2015c','OpenMPI/1.8.8-iccifort-2015.3.187','CUDA/7.0.28']
ModuleList = []




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


# OnlyTwoPt = True ## Only calculates two-point correlation functions.
OnlyTwoPt = False ## Only calculates two-point correlation functions.
OnlyGauge = False ## Only calculates Gauge field
# OnlyGauge = False ## Only calculates Gauge Field
NumGFCreate = 10
# GFFormat = 'ILDG'
# GFFormat = 'UNIT'
GFFormat = 'WEAK_FIELD'
# GFFormat = 'SZIN'
# GFFormat = 'SZINQIO'


##RVec must be len(smlist) * PoFShifts
#Taken from /home/accounts/jdragos/scripts/PythonAnalysis/REvecSave/k12090/PoF1to16dt2LREM.txt
# RVec = [ 76.3260613436,  -161.5448230802, 264086.1917824702, -321.4016231030, 4390.5310121576, -893677.8525444396 ]

#Taken mokup
RVec = [ 0.5,  0.5  ]


# Testing, should be same as tsink sm128
# RVec = ( 0.0 0.0 0.0 0.0 0.0 1.0 )

##n.b. PoFShifts = 1 means 1 tsink value (so no PoF)
PoFShifts = 1
PoFDelta = 2
PoFList = range(PoFShifts)

REvecFlag = 'REPoFto16dt2'
# REvecFlag = 'REPoFTest'
####COLA PARAMETERS

# Propagator Params
it = 16 # creation parameters
ix = 1 #put at ix,ix,ix
# kud = 121040 # kappa (quark hopping) params
# ks = 120620
kud = 120900 # kappa (quark hopping) params
ks = 120900
# Prec = '1.0d-5'
Prec = '5.0e-11'
MaxIter = 10000
# Projector = 4
GammaRep = 'sakurai'
ProjectorList = [4,3]
DSList = ['doub','sing']

ParaIO = 'true'


### GAUGEFIELD GENERATION PARAMETERS ###

GaugeType = 'purgaug'
GFexe = GaugeType

StartUpdateNum = 0
NWarmUpUpdates = 2
NProductionUpdates = 1000
NUpdatesThisRun = 100
SaveInterval = 5

GActName = 'WILSON_GAUGEACT'
beta = '6.0'
anisoP = 'true'
t_dir ='3'
xi_0 ='2.464'
GFnu = '1.0'
GaugeBC = 'PERIODIC_GAUGEBC'
nOver = '3'
NmaxHB = '1'

# GFPrec = '5.0e-5'
# GFMaxIter = 200
# GFDoOr = 'false'
# GFOrPara = '1.0'

def GetSourceString(icfg):
    return str(SRCX[icfg]) + ' ' + str(SRCY[icfg]) + ' ' + str(SRCZ[icfg]) + ' ' + str(SRCT[icfg])
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

FermAct = 'UNPRECONDITIONED_SLRC'
# FermAct = 'SLRC'
invType = 'BICGSTAB_INVERTER'

# SST Propagator Parameters
# it_sst = '32 35 38' ## ahnialation parameters (momenta)
# it_sst = [26, 27, 28] ## ahnialation parameters (momenta)
it_sst = [4] ## ahnialation parameters (momenta) MUST BE len(it_sst) == len(RVec)/PoFShifts
# it_sst = [26, 27, 28, 29, 30] ## ahnialation parameters (momenta)
ppvec = [0,0,0]
ppstr = ' '.join(map(str,ppvec))
qmin = 0
qmax = 9
NDer = 2
NDerList = ['NDer'+str(ider) for ider in range(NDer+1)]

# Sm Parameters
SmSourceType = 'SHELL_SOURCE'
def GetSmSeqSourceType(interp,DS,Proj):
    return interp.replace('nucleon','nucl').upper()+'_'+DStoUD(DS).upper()+'_'+ProjToPol(Proj)+'_NONREL'
SmSinkType = 'SHELL_SINK'
# SmKind = 'GAUGE_INV_JACOBI'
SmKind = 'GAUGE_INV_GAUSSIAN'
alpha = 0.7
StoutLink = 'T'
alphaStout = 0.1
gfsweeps = 4
smu0 = 1.0
smvalues = [32, 64, 128, 'V0']
# ismlist = smvalues[:-1]
# jsmlist = smvalues[:-1]
ismlist = [smvalues[0]]
jsmlist = [smvalues[0]]


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
# boundstr = str(bx) + ' ' +str(by) + ' ' +str(bz) + ' ' +str(bt)
boundstr = str(int(bx)) + ' ' +str(int(by)) + ' ' +str(int(bz)) + ' ' +str(int(bt))
u0 = 1.0
# csw = 2.65
csw = 1.0
rho = 0.1
nstout = 1

OutXml = False


# Configuration data
# limename = 'qcdsf'
limename = 'RC'+str(nx)+'x'+str(nt)+'_B1900Kud'+str(kud)+'Ks'+str(kud)+'C1715-a-'
ensemble = 'b5p50kp'+str(kud)+'kp'+str(ks)

#### configuration/file parameters
scriptdir = basedir+'Scripts/ChromaPySubmit/'
if scriptdir[:-1] not in os.getcwd():
    print 'Warning, you are not running from the script dir'
cshdir = scriptdir+'CSHFiles/'
paramdir = scriptdir+'ParamFiles/'
datadir = scratchdir
InputFolderPref = 'InputFiles'
InputFolder = scriptdir+InputFolderPref+'/'
OutputFolderPref = 'OutputFiles'
OutputFolder = scriptdir+OutputFolderPref+'/'
gfdir = '/work/jias40/jias4000/conf/Nf2p1/b1.9kl0.13754ks0.1364/'
# gfdir = scratchdir+'/gaugefields/qcdsf.655/'
# gfdir = scratchdir+'/gaugefields/TestWeak/'
# rdsigfdir = '/data/jzanotti/confs/32x64/b5p50kp121040kp120620/'
# rdsigfdir = scratchdir+'/gaugefields/limes/
# ##for heavier kappa
# rdsigfdir = scratchdir+'/gaugefields/qcdsf.655/'
# gfdir = '/rdsi/PACS-CS/ensemble+'/'
qpdir = scratchdir+'/qprops/k'+str(kud)+'/'
cfdir = scratchdir+'/cfun/k'+str(kud)+'/twopt/'
cf3ptdir = scratchdir+'/cfun/k'+str(kud)+'/threept/'
debugdir = scratchdir+'/debug/k'+str(kud)+'/'
tempdir = '/tmp/'
filelists = paramdir
chromacpu = codedir+'/'+chromafolder+'/bin/'
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
mkdir_p(InputFolder)
mkdir_p(OutputFolder)
mkdir_p(gfdir)
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

SRCX,SRCY,SRCZ,SRCT = ReadRands(ChromaFileFlag,randlistsize,nx,nt)


def CreateGFnum(icfg):
    if not os.path.isfile(filelists+cfgfile):
        raise IOError(filelists+cfgfile + ' not found, run cfglist creation script')
    with open(filelists+cfgfile,'r') as f:
        thisfile = f.readlines()
        if len(thisfile) == 0: return 'Null'
        if len(thisfile) <= icfg:
            icfg = len(thisfile)-1
        thisgfnum = thisfile[icfg].replace('\n','')
    return thisgfnum

# def CreateCfg(icfg):
#     return ensemble+CreateGFnum(icfg)

# def CreateLimeCfg(icfg):
#     return limename+CreateGFnum(icfg)+'.lime'

def CreateCfg(icfg):
    # return limename+CreateGFnum(icfg)+'.lime'
    # return limename+'.lime'+CreateGFnum(icfg)
    return limename+CreateGFnum(icfg)



