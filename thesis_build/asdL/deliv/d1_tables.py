"""Collect every step output of Part L into tidy tables (one source for the Excel workbook, the PPT charts and the Word figures).
Writes deliv/tables.pkl (dict of DataFrames) and deliv/facts.json (numbers quoted in the text)."""
import os, sys, ast, json, glob, pickle, numpy as np, pandas as pd
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, os.path.join(HERE, '..'))
import configL as C
O = C.OUT; T = {}; F = {}
rd = lambda f, **k: pd.read_csv(os.path.join(O, f), **k)
M = rd('L2_meta.csv'); GR = C.GRADES; DATES = sorted(M.date.unique()); DLAB = {d: pd.Timestamp(d).strftime('%d %b') for d in DATES}
S = np.load(os.path.join(O, 'L3_spectra.npz')); SEL = json.load(open(os.path.join(O, 'L5_selection.json')))
# ---------------- L1
T['l1_flow'] = rd('L1_flow.csv').rename(columns={'step': 'Stage', 'n': 'Spectra'})
ck = rd('L1_checks.csv'); ck['result'] = ck['result'].str.replace(r'np\.int64\((\d+)\)', r'\1', regex=True); ck['pass'] = ck['pass'].map({True: 'PASS', False: 'CHECK'})
T['l1_checks'] = ck.rename(columns={'code': 'Code', 'check': 'Check', 'expected': 'Expected', 'result': 'Result', 'pass': 'Status'})
def ctab(col, order=None, lab=None):
    t = pd.crosstab(M.grade, M[col]).reindex(index=GR, fill_value=0); t = t[order] if order else t
    if lab: t.columns = [lab(c) for c in t.columns]
    t.index = ['Grade %d' % g for g in GR]; t.index.name = 'Grade'; return t.reset_index()
T['l1_grade_date'] = ctab('date', DATES, lambda d: DLAB[d] + ' 2026'); T['l1_grade_leaf'] = ctab('leaf', C.LEAVES); T['l1_grade_stage'] = ctab('stage', ['Vegetative', 'Flowering', 'Pod formation'])
T['l1_grade_variety'] = ctab('variety', ['V1', 'V2', 'V3']); T['l1_grade_sowing'] = ctab('timing', ['D1', 'D2', 'D3', 'D4'], lambda t: '%s (%s)' % (t, pd.Timestamp(C.SOWING[t]).strftime('%d %b')))
dd = rd('L1_duplicates_removed.csv'); T['l1_dups'] = dd
fl = rd('L1_isolation_forest_flags.csv'); T['l1_if'] = fl
ifs = M.groupby(['date', 'grade']).agg(leaves=('IF_flag', 'size'), flagged=('IF_flag', 'sum')).reset_index(); ifs['date'] = ifs.date.map(lambda d: DLAB[d]); T['l1_if_summary'] = ifs
leaf = M[['date', 'file_col', 'plot', 'block', 'variety', 'timing', 'sowing', 'DAS', 'stage', 'leaf', 'score', 'grade', 'diseased', 'IF_flag', 'split', 'nn_part', 'inner_fold']].copy()
leaf.insert(0, 'leaf_id', np.arange(len(leaf))); T['leaf_table'] = leaf
F['n_read'], F['n_L4'], F['n_dup'], F['n_final'] = [int(x) for x in rd('L1_flow.csv').n.values[[0, 1, 2, 4]]]; F['n_if'] = int(M.IF_flag.sum())
F['grade_counts'] = {int(g): int((M.grade == g).sum()) for g in GR}
# ---------------- L2
sc = rd('L2_split_counts.csv'); T['l2_counts'] = sc
pl = M.groupby('plot').agg(block=('block', 'first'), variety=('variety', 'first'), sowing=('timing', 'first'), split=('split', 'first'), network_part=('nn_part', 'first'),
                          inner_fold=('inner_fold', 'first'), leaves=('grade', 'size'), mean_grade=('grade', 'mean'), diseased_leaves=('diseased', 'sum')).reset_index()
pl['inner_fold'] = pl.inner_fold.where(pl.split == 'TRAIN', '—'); T['l2_plots'] = pl
F['n_train'], F['n_test'] = int((M.split == 'TRAIN').sum()), int((M.split == 'TEST').sum()); F['n_fit'], F['n_val'] = int((M.nn_part == 'fit').sum()), int((M.nn_part == 'validation').sum())
F['fold_sizes'] = [int((M.inner_fold == k).sum()) for k in (1, 2, 3)]
# ---------------- L3
X = np.load(os.path.join(O, 'L1_X.npy')); wl = np.load(os.path.join(O, 'L1_wl.npy')); w1, R1, FD1 = S['w1'], S['R1'], S['FD1']
i9 = int(np.where(M.grade.values == 9)[0][0]); i0 = int(np.where(M.grade.values == 0)[0][0]); w5i = np.arange(0, len(w1), 5)
k1 = np.searchsorted(wl, w1[w5i])
T['l3_example'] = pd.DataFrame({'Wavelength (nm)': w1[w5i], 'Raw, grade-0 leaf': X[i0, k1], 'Smoothed, grade-0 leaf': R1[i0, w5i], 'Raw, grade-9 leaf': X[i9, k1], 'Smoothed, grade-9 leaf': R1[i9, w5i],
                                'First derivative, grade-0 leaf': FD1[i0, w5i], 'First derivative, grade-9 leaf': FD1[i9, w5i]})
F['l3_example_leaves'] = [int(i0), int(i9)]
j = (wl >= 985) & (wl <= 1015); T['l3_splice'] = pd.DataFrame({'Wavelength (nm)': wl[j], **{'Grade %d' % g: X[M.grade.values == g][:, j].mean(0) for g in GR}})
T['l3_summary'] = rd('L3_summary.csv')
# ---------------- L4
src = open('/home/user/meta/thesis_build/method3/mf3_end.py').read(); tree = ast.parse(src); defs = {}
for node in tree.body:
    if isinstance(node, ast.Assign) and isinstance(node.targets[0], ast.Name) and node.targets[0].id in ('H', 'H2T'): defs[node.targets[0].id] = ast.literal_eval(node.value)
rows, grp = [], ''
for r in defs['H'][1:] + defs['H2T'][1:-1]:
    grp = r[0] or grp; names = [n.strip() for n in r[1].split(';')]; forms = [f.strip() for f in r[2].split(';')]
    for n, f in zip(names, forms if len(forms) == len(names) else [r[2]] * len(names)):
        ref = r[3].replace('Ramalingam et al. 2026', 'Selvaprakash et al. 2026')
        if n.startswith('RBI_{R}'): f = '(R_{1068} − R_{1560})/(R_{1068} + R_{1560})'
        rows.append(dict(Group=grp.split(' (')[0], Index=n.replace('HI (healthy index)', 'HI').replace('Moisture stress index (MSI)', 'MSI').replace('RBI_{M}', 'RBI_M').replace('RBI_{R}', 'RBI_R').replace('D_{r}', 'Dr').replace('SD_{r}', 'SDr'),
                         Formula=f.replace('^{2}', '²').replace('_{', '').replace('}', ''), Reference=ref))
L4D = pd.DataFrame(rows); idx = pd.read_csv(os.path.join(O, 'L4_indices.csv')); assert set(L4D.Index) == set(idx.columns), set(idx.columns) ^ set(L4D.Index)
ir = rd('L5_1_index_r.csv', index_col=0); L4D['r with grade (all leaves)'] = L4D.Index.map(ir.r_with_grade); T['l4_defs'] = L4D
T['l4_values'] = pd.concat([leaf[['leaf_id', 'date', 'plot', 'leaf', 'grade', 'split']], idx.round(6)], axis=1)
# ---------------- L5.1
sp = rd('L5_1_spectra_by_grade.csv'); T['l51_spectra'] = sp
T['l51_index_r'] = ir.reset_index().rename(columns={'index': 'Index', 'r_with_grade': 'r', 'abs_r': '|r|'}).merge(L4D[['Index', 'Group', 'Reference']], on='Index', how='left')
im = rd('L5_1_index_means_by_grade.csv', index_col=0); T['l51_index_means'] = im.reset_index().rename(columns={'index': 'Index'})
re_ = pd.concat([M[['grade']], idx[['REP', 'Dr', 'SDr']]], axis=1).groupby('grade').agg(['mean', 'std'])
T['l51_rededge'] = pd.DataFrame({'Grade': ['Grade %d' % g for g in GR], 'REP mean (nm)': re_[('REP', 'mean')].values, 'REP SD (nm)': re_[('REP', 'std')].values,
                                 'Dr mean (×10⁻³ nm⁻¹)': re_[('Dr', 'mean')].values * 1000, 'Dr SD (×10⁻³ nm⁻¹)': re_[('Dr', 'std')].values * 1000, 'SDr mean': re_[('SDr', 'mean')].values, 'Leaves': [int((M.grade == g).sum()) for g in GR]})
F['rededge'] = dict(rep=[float(x) for x in re_[('REP', 'mean')].values], dr=[float(x) * 1000 for x in re_[('Dr', 'mean')].values], r_rep=float(ir.loc['REP', 'r_with_grade']), r_dr=float(ir.loc['Dr', 'r_with_grade']), r_sdr=float(ir.loc['SDr', 'r_with_grade']))
T['l51_strata'] = rd('L5_1_strata.csv'); rs = rd('L5_1_r_by_stratum.csv'); T['l51_r_strata'] = rs
F['l51'] = json.load(open(os.path.join(O, 'L5_1_summary.json')))
# ---------------- L5.7 PCA
T['l57_var'] = rd('L5_7_pca_variance.csv'); T['l57_load'] = rd('L5_7_pca_loadings.csv'); T['l57_scores'] = rd('L5_7_pca_scores.csv'); T['l57_ell'] = rd('L5_7_pca_ellipses.csv')
T['l57_means'] = rd('L5_7_pca_grade_means.csv', index_col=0).reset_index().rename(columns={'index': 'grade'})
# ---------------- L5.2
w5 = S['w5']; N = np.load(os.path.join(O, 'L5_2_NDSI_R2.npy')); Rs = np.load(os.path.join(O, 'L5_2_RSI_R2.npy'))
sub = np.arange(0, len(w5), 4)                                                                     # 20-nm grid for the editable Excel heat table
for nm, A in (('l52_ndsi20', N), ('l52_rsi20', Rs)):
    B = A[np.ix_(sub, sub)]; T[nm] = pd.DataFrame(B, index=w5[sub], columns=w5[sub])
e = np.array(SEL['effective_bands']); br = np.where(np.diff(e) > 5)[0]; st = [e[0]] + list(e[br + 1]); en = list(e[br]) + [e[-1]]
T['l52_ranges'] = pd.DataFrame(dict(Range=['%d–%d nm' % (a, b) for a, b in zip(st, en)], Start=st, End=en, Bands=[int(((e >= a) & (e <= b)).sum()) for a, b in zip(st, en)]))
T['l52_shap'] = rd('L5_2_shap.csv'); T['l52_mccv'] = rd('L5_2_mccv.csv'); T['l52_cars'] = rd('L5_2_cars.csv')
ow = SEL['OW']; T['l52_ow'] = pd.DataFrame(dict(Feature=ow, Type=['First derivative' if o.startswith('FD') else 'Reflectance' for o in ow], Wavelength=[int(o.lstrip('FDR')) for o in ow])).sort_values('Wavelength')
sh = T['l52_shap'].set_index('feature').mean_abs_SHAP; T['l52_ow']['mean |SHAP|'] = T['l52_ow'].Feature.map(sh)
F['l52'] = dict(maxR2_ndsi=SEL['map_max_R2']['NDSI'], maxR2_rsi=SEL['map_max_R2']['RSI'], thr=SEL['thresholds'], n_eff=len(e), ranges=list(T['l52_ranges'].Range), n_cand=SEL['n_candidates'],
                n_shap=SEL['n_shap_kept'], ncomp=SEL['pls_components'], n_ow=len(ow), cars_it=SEL['cars_best_iteration'], cars_rmse=SEL['cars_best_rmse'])
# ---------------- L5.3
T['l53_wri'] = rd('L5_3_wri_search_all.csv').head(50); T['l53_wri_w'] = rd('L5_3_wri_best_by_w.csv'); wri = dict(SEL['wri']); wri['l3'] = None if wri['w'] == 0 else wri['l3']
ALL = rd('L5_all_features.csv'); tr = (M.split == 'TRAIN').values
T['l53_by_grade'] = pd.DataFrame([dict(Grade=g, **{f + ' mean': ALL.loc[(M.grade == g).values & tr, f].mean() for f in ('NDSI_best', 'RSI_best', 'WRI')}, **{f + ' SD': ALL.loc[(M.grade == g).values & tr, f].std() for f in ('NDSI_best', 'RSI_best', 'WRI')}) for g in GR])
wnz = T['l53_wri_w'][T['l53_wri_w'].w != 0].iloc[0]
F['l53'] = dict(ndsi=SEL['ndsi'], rsi=SEL['rsi'], wri=wri, wri_best_nonzero=dict(l1=int(wnz.l1), l2=int(wnz.l2), w=float(wnz.w), l3=int(wnz.l3), r=float(wnz.r)))
# ---------------- L5.4
T['l54_relief'] = rd('L5_4_relieff.csv'); cl = SEL['clusters']
T['l54_clusters'] = pd.DataFrame([dict(Kept=k, Removed=', '.join(v) if v else '—', n_removed=len(v)) for k, v in cl.items()])
T['l54_vi'] = pd.DataFrame({'Rank': range(1, 6), **{'Task %s' % t: SEL['VI'][t] for t in 'ABC'}})
F['l54'] = dict(n_before=int(ALL.shape[1] - 802), n_kept=len(SEL['kept_after_filter']), VI=SEL['VI'])
# ---------------- L5.5
vr = rd('L5_5_vif_rounds.csv'); T['l55_rounds'] = vr
last = vr.groupby('task')['round'].max(); T['l55_final'] = pd.concat([vr[(vr.task == t) & (vr['round'] == last[t])] for t in 'ABC'])
T['l55_steps'] = vr.loc[vr.groupby(['task', 'round']).VIF.idxmax()].rename(columns={'feature': 'largest-VIF feature', 'VIF': 'largest VIF'})
T['l55_dsf'] = pd.DataFrame([dict(Task=t, Pool=len(set(SEL['OW']) | set(SEL['VI'][t])), Rounds=int(last[t]), DSF_size=len(SEL['DSF'][t]), DSF=', '.join(SEL['DSF'][t])) for t in 'ABC'])
# ---------------- L5.6
jm = rd('L5_6_jm.csv'); T['l56_jm'] = jm; Mx = pd.DataFrame(np.nan, index=GR, columns=GR)
for _, r in jm.iterrows(): Mx.loc[r.grade_a, r.grade_b] = r.JM; Mx.loc[r.grade_b, r.grade_a] = r.JM
for g in GR: Mx.loc[g, g] = 0.0
T['l56_matrix'] = Mx
# ---------------- L6 / L7 / L8 / L9
def cat(pat): fs = sorted(glob.glob(os.path.join(O, pat))); return pd.concat([pd.read_csv(f) for f in fs], ignore_index=True) if fs else pd.DataFrame()
T['l6_ml'] = cat('L6_ml_summary_*.csv'); T['l6_paths'] = cat('L6_sffs_paths_*.csv'); T['l6_dl'] = cat('L6_dl_summary*.csv'); T['l6_hist'] = cat('L6_dl_history*.csv')
for nm, f in (('l6_stab_runs', 'L6_stability_runs.csv'), ('l6_stab_freq', 'L6_stability_frequency.csv'), ('l7_metrics', 'L7_metrics.csv'), ('l7_conf', 'L7_confusion.csv'), ('l7_strata', 'L7_strata.csv'),
              ('l7_low', 'L7_low_severity.csv'), ('l8_models', 'L8_models.csv'), ('l8_gains', 'L8_gains.csv'), ('l8_weather', 'L8_weather_windows.csv'), ('l8_pred', 'L8_predictions.csv'), ('l8_imp', 'L8_importance.csv'),
              ('l9_band', 'L9_bandwise.csv'), ('l9_transfer', 'L9_transfer.csv'), ('l9_plots', 'L9_plots.csv')):
    if os.path.isfile(os.path.join(O, f)): T[nm] = rd(f)
if os.path.isfile(os.path.join(O, 'L7_best.json')):
    B = json.load(open(os.path.join(O, 'L7_best.json'))); F['best'] = B['best']; F['best_ml'] = B['best_ml']
    P = pd.concat([cat('L6_ml_predictions_*.csv'), cat('L6_dl_predictions*.csv')], ignore_index=True).drop_duplicates(['task', 'model', 'leaf'], keep='last')
    te = M[M.split == 'TEST'][['plot', 'date', 'stage', 'leaf', 'variety', 'grade']].rename(columns={'leaf': 'leaf_pos'}); te.insert(0, 'leaf_id', te.index)
    for t in 'ABC':
        for m in P[P.task == t].model.unique():
            d = P[(P.task == t) & (P.model == m)].set_index('leaf'); te['%s|%s' % (t, m)] = te.leaf_id.map(d.pred)
            if t == 'A': te['A score|%s' % m] = te.leaf_id.map(d.score)
    te['A observed'] = (te.grade > 0).astype(int); te['B observed class'] = te.grade.map({g: i for i, g in enumerate(GR)}); T['l7_pred'] = te
    from sklearn.metrics import roc_curve
    d = P[(P.task == 'A') & (P.model == B['best']['A'])].sort_values('leaf'); fpr, tpr, thr = roc_curve(d.y, d.score); keep = np.unique(np.linspace(0, len(fpr) - 1, min(len(fpr), 120)).astype(int))
    T['l7_roc'] = pd.DataFrame({'False positive rate': fpr[keep], 'True positive rate': tpr[keep]})
if os.path.isfile(os.path.join(O, 'L9_summary.json')): F['l9'] = json.load(open(os.path.join(O, 'L9_summary.json')))
F['DSF'] = SEL['DSF']; F['OW'] = SEL['OW']
pickle.dump(T, open(os.path.join(HERE, 'tables.pkl'), 'wb')); json.dump(F, open(os.path.join(HERE, 'facts.json'), 'w'), indent=1, default=float)
print('tables', len(T)); print({k: (v.shape if hasattr(v, 'shape') else None) for k, v in T.items()})
