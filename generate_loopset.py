from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import numpy as np
import argparse
import random
import h5py as hf
import sys, pickle
from loopalgo import *

L = 32
SAVEFIG = True
iceset = hf.File('squareice_states_5000x1024.h5', 'r')
ices = iceset['icestates'][:10]

for idx1, s1 in enumerate(ices):
    for idx2, s2 in enumerate(ices):
        if (idx2 == idx1):
            # or idx2 <= idx1
            continue
        print ('State {} transits to state {}'.format(idx1, idx2))
        s1 = ices[idx1]
        s2 = ices[idx2]
        trans = s1-s2
        d1loops = trans_subset(s1, trans, L, index=idx1, dilation_times=1, save_img=SAVEFIG)
        d2loops = trans_subset(s1, trans, L, index=idx1, dilation_times=2, save_img=SAVEFIG)
        loops = d1loops + d2loops
        print (' capture {} loops from {} to {}'.format(len(loops), idx1, idx2))
        np.save('loops/loopstate_{}'.format(idx1), loops)