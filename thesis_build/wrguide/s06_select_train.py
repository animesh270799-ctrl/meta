"""STEP 6 (E2): the same selection chain on the TRAINING plots only -> the model inputs. TEST leaves are not used."""
import os, json, numpy as np, pandas as pd
import config as C
from lib_select import select_chain, feature_table
O = C.OUT; M = pd.read_csv(os.path.join(O, '03_meta_split.csv')); Z = np.load(os.path.join(O, '04_spectra.npz')); S = {k: Z[k] for k in Z.files}
F44 = pd.read_csv(os.path.join(O, '04_indices.csv')); CR = pd.read_csv(os.path.join(O, '04_continuum.csv')); W = np.load(os.path.join(O, '04_cwt.npy'))
tr = (M.fold == 1).values; log = open(os.path.join(O, '06_select_log.txt'), 'w')
def L(*a): print(*a); print(*a, file=log)
sel = select_chain(tr, S, F44, CR, W, M, log=L)
T = feature_table(sel, S, F44, CR, W)                                  # index values of the TEST leaves use the wavelengths chosen on TRAIN
keep = sorted(set(sum([sel['DSF'][t] + sel['VI'][t] + sel['WF'][t] for t in 'ABC'], [])) | set(sel['OW']))
T[keep].to_csv(os.path.join(O, '06_model_features.csv'), index=False); json.dump(sel, open(os.path.join(O, '06_selection_train.json'), 'w'), indent=1, default=float)
print('CHECK: selection used %d training leaves; DSF A %s | B %s | C %s' % (tr.sum(), sel['DSF']['A'], sel['DSF']['B'], sel['DSF']['C']))
