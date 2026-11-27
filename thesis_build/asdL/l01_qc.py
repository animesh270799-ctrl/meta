"""STEP L1 - leaf table and data checks. Read the four ASD exports (one column = one leaf spectrum, 350-2500 nm, 7 header rows),
join the plot plan, keep L3/L5/LL, remove exact duplicates, check the detector join, screen outliers with Isolation Forest (date x grade)."""
import os, json, openpyxl, numpy as np, pandas as pd
from sklearn.ensemble import IsolationForest
import configL as C
meta, spec, wl = [], [], None
for date, fn in C.RAW_FILES.items():
    rows = list(openpyxl.load_workbook(C.UP + fn, read_only=True).worksheets[0].iter_rows(values_only=True))
    hdr, body = rows[:7], rows[7:]; w = np.array([r[0] for r in body], float); wl = w if wl is None else wl; assert np.array_equal(w, wl)
    for j in range(1, len(hdr[0])):
        name = hdr[0][j]
        if not (isinstance(name, str) and name.lower().endswith('.sco')): continue
        meta.append(dict(date=date, file_col=name, plot=int(hdr[1][j]), variety=str(hdr[2][j]).strip(), stage=str(hdr[3][j]).strip(), status=str(hdr[4][j]).strip(), leaf=str(hdr[5][j]).strip(), score=hdr[6][j]))
        spec.append([r[j] for r in body])
M = pd.DataFrame(meta); X = np.array(spec, float); chk = []; flow = [('Spectra read from the four files', len(M))]
chk.append(('L1.1', 'Spectra read', '4 files; 350-2500 nm; 2151 bands', '%d spectra; %d bands; %g-%g nm' % (len(M), X.shape[1], wl[0], wl[-1]), len(M) > 0 and X.shape[1] == 2151))
chk.append(('L1.2', 'Missing values', '0', str(int(np.isnan(X).sum())), not np.isnan(X).any()))
M['block'] = M['plot'].map(C.BLOCK); M['timing'] = M['plot'].map(lambda p: C.LAYOUT[p][:2]); bad = M['plot'].map(lambda p: C.LAYOUT[p][2:]) != M.variety
chk.append(('L1.3', 'Variety agrees with the plot plan', 'all leaves', '%d disagreements' % bad.sum(), not bad.any()))
drop = ~M.leaf.isin(C.LEAVES); flow.append(('Leaf position other than L3, L5, LL removed', int(drop.sum())))
chk.append(('L1.4', 'Leaf positions', 'L3, L5, LL only', 'removed %d (%s)' % (drop.sum(), M.loc[drop, 'leaf'].value_counts().to_dict()), True))
M, X = M[~drop].reset_index(drop=True), X[~drop.values]
_, inv = np.unique(X.round(6), axis=0, return_inverse=True); dup = pd.Series(inv.ravel()).duplicated().values
flow.append(('Exact duplicate spectra removed', int(dup.sum())))
M.loc[dup, ['date', 'plot', 'leaf', 'file_col']].to_csv(os.path.join(C.OUT, 'L1_duplicates_removed.csv'), index=False)
chk.append(('L1.5', 'Exact duplicate spectra', 'none', '%d removed (dates %s; plots %s)' % (dup.sum(), sorted(M.loc[dup, 'date'].unique()), sorted(M.loc[dup, 'plot'].unique().tolist())), True))
M, X = M[~dup].reset_index(drop=True), X[~dup]
i = int(np.where(wl == C.SPLICE_JOIN)[0][0]); step = X[:, i + 1] - X[:, i]; slope = 0.5 * ((X[:, i] - X[:, i - 1]) + (X[:, i + 2] - X[:, i + 1])); exc = step - slope
chk.append(('L1.6', 'Detector join 1000/1001 nm (splice)', 'no residual step', 'median excess step %.4f (IQR %.4f to %.4f) -> first-derivative bands 995-1005 nm excluded from band selection (DEV-1)' % (np.median(exc), *np.percentile(exc, [25, 75])), True))
M['grade'] = M.score.astype(int); assert set(M.grade) <= set(C.GRADES)
chk.append(('L1.7', 'Grades', '0, 1, 3, 5, 7, 9', str(sorted(M.grade.unique())), set(M.grade) <= set(C.GRADES)))
chk.append(('L1.8', 'Plots on every date', '48', str(M.groupby('date')['plot'].nunique().to_dict()), (M.groupby('date')['plot'].nunique() == 48).all()))
# Isolation Forest within date x grade (on 10-nm means of the raw spectrum, 400-2400 nm)
sel = (wl >= 400) & (wl <= 2400); Z = X[:, sel][:, :2000].reshape(len(X), -1, 10).mean(2); flag = np.zeros(len(M), bool); score = np.zeros(len(M))
for (d, g), idx in M.groupby(['date', 'grade']).groups.items():
    idx = np.asarray(idx)
    if len(idx) < 10: continue
    f = IsolationForest(n_estimators=300, contamination=C.IF_CONTAM, random_state=C.SEED).fit(Z[idx]); flag[idx] = f.predict(Z[idx]) == -1; score[idx] = f.score_samples(Z[idx])
faulty = flag & ((X[:, sel].min(1) < 0) | (X[:, sel].max(1) > 1))
M['IF_flag'] = flag.astype(int); M['IF_score'] = score
fl = M[flag].copy(); fl['min_R'] = X[flag][:, sel].min(1); fl['max_R'] = X[flag][:, sel].max(1); fl['NIR800'] = X[flag][:, wl == 800].ravel(); fl['faulty'] = faulty[flag]
fl[['date', 'plot', 'leaf', 'grade', 'file_col', 'IF_score', 'min_R', 'max_R', 'NIR800', 'faulty']].to_csv(os.path.join(C.OUT, 'L1_isolation_forest_flags.csv'), index=False)
chk.append(('L1.9', 'Isolation Forest screening (date x grade)', 'flagged spectra checked; removed only if faulty', '%d flagged; %d faulty (reflectance < 0 or > 1) removed' % (flag.sum(), faulty.sum()), True))
flow.append(('Faulty spectra removed after Isolation Forest check', int(faulty.sum())))
M, X = M[~faulty].reset_index(drop=True), X[~faulty]
M['diseased'] = (M.grade > 0).astype(int); M['unsprayed'] = (M.block != 'C').astype(int); M['sowing'] = M.timing.map(C.SOWING)
M['DAS'] = (pd.to_datetime(M.date) - pd.to_datetime(M.sowing)).dt.days; M['stage_code'] = M.stage.map(C.STAGE_CODE); assert M.stage_code.notna().all()
chk.append(('L1.10', 'Readings per leaf', '2 readings averaged (methodology)', 'one spectrum per leaf in the files (instrument average) - averaging not applicable', True))
chk.append(('L1.11', 'Healthy-block leaves with grade > 0', 'expected few', str(int(((M.block == 'C') & (M.grade > 0)).sum())), True))
flow.append(('Leaves in the final leaf table', len(M)))
np.save(os.path.join(C.OUT, 'L1_X.npy'), X); np.save(os.path.join(C.OUT, 'L1_wl.npy'), wl); M.to_csv(os.path.join(C.OUT, 'L1_meta.csv'), index=False)
pd.DataFrame(chk, columns=['code', 'check', 'expected', 'result', 'pass']).to_csv(os.path.join(C.OUT, 'L1_checks.csv'), index=False)
pd.DataFrame(flow, columns=['step', 'n']).to_csv(os.path.join(C.OUT, 'L1_flow.csv'), index=False)
for c in chk: print('CHECK', c)
print(M.groupby(['date', 'leaf']).size().unstack(fill_value=0)); print(M.grade.value_counts().sort_index().to_dict())
