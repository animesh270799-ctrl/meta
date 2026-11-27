"""STEP 2 (A5): quality control -> one checked leaf table.
(1) join the plot plan  (2) remove L4 spectra  (3) remove duplicated spectra  (4) splice correction at the detector joins  (5) checks and labels."""
import os, numpy as np, pandas as pd
import config as C
from lib_spec import splice_correct
M = pd.read_csv(os.path.join(C.OUT, '01_meta_raw.csv')); X = np.load(os.path.join(C.OUT, '01_X_raw.npy')); wl = np.load(os.path.join(C.OUT, '01_wl.npy'))
rep = []
# (1) plot plan
M['block'] = M['plot'].map(C.BLOCK); M['timing'] = M['plot'].map(lambda p: C.LAYOUT[p][:2]); lay_var = M['plot'].map(lambda p: C.LAYOUT[p][2:])
bad = (lay_var != M.variety); rep.append('plots whose variety differs from the plan: %d' % M.loc[bad, 'plot'].nunique()); assert not bad.any(), M.loc[bad, ['date', 'plot', 'variety']]
# (2) leaf positions
drop = ~M.leaf.isin(C.LEAF_POSITIONS); rep.append('spectra with a leaf position other than L3/L5/LL removed: %d %s' % (drop.sum(), M.loc[drop, 'leaf'].value_counts().to_dict()))
M, X = M[~drop].reset_index(drop=True), X[~drop.values]
# (3) duplicated spectra (identical values at every wavelength) - keep the first copy
_, inv = np.unique(X.round(6), axis=0, return_inverse=True); dup = pd.Series(inv.ravel()).duplicated().values
rep.append('duplicated spectra removed: %d (dates %s, plots %s)' % (dup.sum(), M.loc[dup, 'date'].unique().tolist(), sorted(M.loc[dup, 'plot'].unique().tolist())))
pd.DataFrame({'removed_file_col': M.loc[dup, 'file_col'], 'date': M.loc[dup, 'date'], 'plot': M.loc[dup, 'plot']}).to_csv(os.path.join(C.OUT, '02_removed_duplicates.csv'), index=False)
M, X = M[~dup].reset_index(drop=True), X[~dup]
# (4) splice correction (Hueni and Bialek, 2017)
X, before, after, applied = splice_correct(X, wl)
for J in C.SPLICE_JOINS: rep.append('join %d/%d nm: median excess jump %.5f -> %.5f (%s)' % (J, J + 1, before[J], after[J], 'corrected' if applied[J] else 'no step, unchanged'))
# (5) labels and checks
M['grade'] = M.score.astype(int); assert set(M.grade) <= set(C.GRADES), 'unexpected grade'
M['diseased'] = (M.grade > 0).astype(int); M['unsprayed'] = (M.block != 'C').astype(int)
M['sowing'] = M.timing.map(C.SOWING); M['DAS'] = (pd.to_datetime(M.date) - pd.to_datetime(M.sowing)).dt.days; M['stage_code'] = M.stage.map(C.STAGE_CODE)
assert M.stage_code.notna().all(), 'unknown growth stage label'; assert not np.isnan(X).any()
assert (M.groupby('date')['plot'].nunique() == 48).all(), 'a date misses plots'
rep.append('healthy-block leaves with grade > 0: %d' % ((M.block == 'C') & (M.grade > 0)).sum())
rep.append('leaves after quality control: %d; reflectance range %.3f-%.3f' % (len(M), X.min(), X.max()))
rep.append('grades: %s' % M.grade.value_counts().sort_index().to_dict()); rep.append('dates: %s' % M.groupby('date').size().to_dict())
np.save(os.path.join(C.OUT, '02_X.npy'), X); M.to_csv(os.path.join(C.OUT, '02_meta.csv'), index=False)
open(os.path.join(C.OUT, '02_qc_report.txt'), 'w').write('\n'.join(rep)); print('\n'.join('CHECK: ' + r for r in rep))
