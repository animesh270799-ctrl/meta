"""STEP L2 - same 7:3 split by whole plots (methodology D1) and inner validation (D2): GroupKFold(3) by plot for ML, 11 fixed validation plots for networks."""
import os, json, numpy as np, pandas as pd
from sklearn.model_selection import GroupKFold
import configL as C
M = pd.read_csv(os.path.join(C.OUT, 'L1_meta.csv'))
M['split'] = np.where(M['plot'].isin(C.TEST_PLOTS), 'TEST', 'TRAIN'); M['nn_part'] = np.where(M.split == 'TEST', 'test', np.where(M['plot'].isin(C.VAL_PLOTS), 'validation', 'fit'))
tr = M.split == 'TRAIN'; trp = sorted(M.loc[tr, 'plot'].unique()); fold_of = {}
for k, (_, te) in enumerate(GroupKFold(C.INNER).split(np.zeros(len(trp)), groups=trp)):
    for j in te: fold_of[trp[j]] = k + 1
M['inner_fold'] = M['plot'].map(fold_of).fillna(0).astype(int)
M.to_csv(os.path.join(C.OUT, 'L2_meta.csv'), index=False)
rows = []
for part, d in [('All', M), ('TRAIN (33 plots)', M[tr]), ('  network fit (22 plots)', M[M.nn_part == 'fit']), ('  network validation (11 plots)', M[M.nn_part == 'validation']), ('TEST (15 plots)', M[~tr])]:
    r = dict(part=part, plots=d['plot'].nunique(), leaves=len(d)); r.update({'grade %d' % g: int((d.grade == g).sum()) for g in C.GRADES}); rows.append(r)
for k in (1, 2, 3):
    d = M[M.inner_fold == k]; r = dict(part='  GroupKFold fold %d (scoring plots)' % k, plots=d['plot'].nunique(), leaves=len(d)); r.update({'grade %d' % g: int((d.grade == g).sum()) for g in C.GRADES}); rows.append(r)
T = pd.DataFrame(rows); T.to_csv(os.path.join(C.OUT, 'L2_split_counts.csv'), index=False); print(T.to_string(index=False))
json.dump(dict(test_plots=C.TEST_PLOTS, val_plots=C.VAL_PLOTS, folds={str(k): sorted([int(p) for p, f in fold_of.items() if f == k]) for k in (1, 2, 3)}), open(os.path.join(C.OUT, 'L2_split.json'), 'w'), indent=1)
assert set(M.loc[M.split == 'TEST', 'plot']) & set(M.loc[M.split == 'TRAIN', 'plot']) == set()
print('test share %.1f%%' % (100 * (~tr).mean()))
