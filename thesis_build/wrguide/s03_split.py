"""STEP 3 (B1-B2): the grouped, stratified 70:30 split (fixed test plots), the inner GroupKFold(3) folds and the network validation plots.
python s03_split.py           -> uses the fixed test plots of config.TEST_PLOTS (keep these for every analysis)
python s03_split.py --search  -> also re-runs the 5000-candidate search (split_lib.best_split) to show how the plots were chosen"""
import os, sys, json, numpy as np, pandas as pd
from sklearn.model_selection import GroupKFold
import config as C, split_lib as SL
M = pd.read_csv(os.path.join(C.OUT, '02_meta.csv'))
if '--search' in sys.argv:
    best, info = SL.best_split(M, C.TEST_FRAC, C.SEED_SPLIT, C.N_CAND); print('search result:', sorted(best), info)
M['fold'] = np.where(M['plot'].isin(C.TEST_PLOTS), 0, 1)          # 0 = TEST, 1 = TRAIN
tr = M.fold == 1; ptr = np.unique(M.loc[tr, 'plot'])
rng = np.random.default_rng(C.SEED); val = sorted(int(v) for v in rng.choice(ptr, len(ptr) // 3, replace=False))
inner = list(GroupKFold(C.INNER_FOLDS).split(np.zeros(tr.sum()), groups=M.loc[tr, 'plot']))
inner_plots = [sorted(int(p) for p in np.unique(M.loc[tr, 'plot'].values[va])) for _, va in inner]
info = dict(test_plots=C.TEST_PLOTS, n_train=int(tr.sum()), n_test=int((~tr).sum()), test_share=float((~tr).mean()), dl_val_plots=val,
            n_dl_val=int((tr & M['plot'].isin(val)).sum()), n_dl_fit=int((tr & ~M['plot'].isin(val)).sum()), inner_val_plots=inner_plots,
            n_unsprayed_train=int((tr & (M.unsprayed == 1)).sum()), n_unsprayed_test=int((~tr & (M.unsprayed == 1)).sum()))
M.to_csv(os.path.join(C.OUT, '03_meta_split.csv'), index=False); json.dump(info, open(os.path.join(C.OUT, '03_split.json'), 'w'), indent=1)
print('CHECK: TRAIN plots', len(ptr), 'leaves', info['n_train'], '| TEST plots', len(C.TEST_PLOTS), 'leaves', info['n_test'], '(%.1f%%)' % (100 * info['test_share']))
print('CHECK: network fit / validation leaves', info['n_dl_fit'], '/', info['n_dl_val'], '| validation plots', val)
print('CHECK: no plot on both sides:', set(M.loc[tr, 'plot']).isdisjoint(set(M.loc[~tr, 'plot'])))
print(pd.crosstab(M.fold, M.block))
