from RunParams import GeomPicked
from RunParams import nt,nx,totproc
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
