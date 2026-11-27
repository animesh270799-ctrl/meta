"""STEP 4 (C2-C10): pre-processing and the three feature families for every leaf (leaf by leaf, nothing learned from other leaves)."""
import os, json, numpy as np, pandas as pd
import config as C
from lib_spec import preprocess, indices, continuum_removed, cwt
X = np.load(os.path.join(C.OUT, '02_X.npy')); wl = np.load(os.path.join(C.OUT, '01_wl.npy'))
w1, R1, FD1, w5, R5, FD5 = preprocess(X, wl)                         # C2-C6
F44 = indices(R1, FD1)                                                 # C7-C8: 41 indices + REP, Dr, REarea (1 nm)
CR = continuum_removed(R1, w1)                                         # C9
W = cwt(R1)                                                            # C10
np.savez_compressed(os.path.join(C.OUT, '04_spectra.npz'), w1=w1, R1=R1.astype(np.float32), FD1=FD1.astype(np.float32), w5=w5, R5=R5, FD5=FD5)
F44.to_csv(os.path.join(C.OUT, '04_indices.csv'), index=False); CR.to_csv(os.path.join(C.OUT, '04_continuum.csv'), index=False); np.save(os.path.join(C.OUT, '04_cwt.npy'), W)
print('CHECK: 1-nm bands', len(w1), '(%d-%d nm) | 5-nm bands' % (w1[0], w1[-1]), len(w5), '| indices', F44.shape[1], '| continuum features', CR.shape[1], '| wavelet array', W.shape)
print('CHECK: missing values in features:', int(F44.isna().sum().sum() + CR.isna().sum().sum()), '| REP range', F44.REP.min(), '-', F44.REP.max())
