from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import numpy as np
import sys, os

def get_ices():
    import h5py as hf
    iceset = hf.File('squareice_states_5000x1024.h5', 'r')
    ices = iceset['icestates'][:]
    iceset.close()
    return ices

def get_ice_images():
    import h5py as hf
    iceset = hf.File('SQUAREICE_STATES_5000x32x32.h5', 'r')
    ices = iceset['ICESTATES'][:]
    iceset.close()
    return ices

def get_filelist(source_idx, prefix='loopstate', dirname='loops'):
    files = os.listdir(dirname)
    filelist = []
    for f in files:
        if str.startswith(f, prefix):
            fname = f.rstrip('.npy')
            trans = fname.split('_')[-1]
            from_idx, to_idx = trans.split('-')
            if (int(from_idx) == source_idx):
                #print ('read file: {}'.format(fname))
                filelist.append(f)
    return filelist

def read_filelist(filelist, dirname='loops'):
    loops = []
    for f in filelist:
        loops.extend(np.load('/'.join([dirname, f]))[0])
    return loops

def get_loopsize(loops):
    return [len(np.nonzero(l)[0]) for l in loops]

def combine_isolated_loopsites(loopsites, indices):
    '''
        loopsites: list of numpy array
        indices: specify which loopsite would be combine
    '''
    try:
        print('number of total loops: {}'.format(len(indices)))
        filtered_loops = []
        marked = {}
        for idx in indices:
            l = loopsites[idx][0]
            checked = True
            for p in l:
                if marked.get(p):
                    checked = False
                    break
                else:
                    marked[p] = 1
            if checked:
                filtered_loops.append(l)
        print('number of remaining loops: {}'.format(len(filtered_loops)))
        return combine_loopsites(filtered_loops)
    except:
        print ('list is empty')
        return

def combine_isolated_loops(loops):
    try:
        print('number of total loops: {}'.format(len(loops)))
        filtered_loops = []
        marked = {}
        for l in loops:
            checked = True
            for p in np.nonzero(l)[0]:
                if marked.get(p):
                    checked = False
                    break
                else:
                    marked[p] = 1
            if checked:
                filtered_loops.append(l)
                
        print('number of remaining loops: {}'.format(len(filtered_loops)))
        return combine_loopstates(filtered_loops)
    except:
        print ('list is empty')
        return

def combine_loopstates(loops):
    if loops:
        combined = np.zeros_like(loops[0])
        for l in loops:
            combined += l
            # should prevent combining same loop twice
            # conflict check
        combined = combined.astype(np.int32)
        return combined
    else:
        print ('list is empty')
        return

def combine_loopsites(loopsites):
    try:
        cloop = np.concatenate(loopsites)
        return cloop
    except:
        print ('list is empty')
        return

def convert_onehot(loops):
    loops[loops > 0] = 1
    loops[loops < 0] = -1