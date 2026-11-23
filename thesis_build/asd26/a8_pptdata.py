"""Collect every number, table and chart series used by the seminar deck and the Word report into one JSON file."""
import numpy as np, pandas as pd, os, json
B = os.path.dirname(os.path.abspath(__file__)) + '/'; D = B + 'data/'
M = pd.read_csv(D + 'meta.csv'); O1 = json.load(open(D + 'o1_results.json')); SEL = json.load(open(D + 'fold_selection.json'))
GR = [0, 1, 3, 5, 7, 9]; out = {'n': len(M), 'O1': O1}
r3 = lambda x: None if x is None or (isinstance(x, float) and np.isnan(x)) else round(float(x), 3)
def ct(fac):
    c = pd.crosstab(M[fac].astype(str), M.grade); return {'labels': list(c.index), 'series': [{'name': 'grade %d' % g, 'values': [int(v) for v in c[g]]} for g in GR]}
out['counts'] = {f: ct(f) for f in ['date', 'stage', 'variety', 'leaf', 'timing', 'block']}
out['grade_n'] = {str(g): int((M.grade == g).sum()) for g in GR}
out['dates'] = [dict(date=d, DAI=int(g.DAI.iloc[0]), n=len(g), mean_grade=r3(g.grade.mean()), pct=r3(100 * g.diseased.mean()), stages=', '.join(sorted(g.stage.unique()))) for d, g in M.groupby('date')]
ms = pd.read_csv(D + 'o1_mean_spectra.csv'); sel10 = ms.wl % 10 == 0
out['mean_spectra'] = {'labels': [int(w) for w in ms.wl[sel10]], 'series': [{'name': 'grade %d' % g, 'values': [r3(v) for v in ms['mean_%d' % g][sel10]]} for g in GR]}
fs = pd.read_csv(D + 'o1_mean_fd.csv'); s2 = (fs.wl >= 500) & (fs.wl <= 800)
out['fd_rededge'] = {'labels': [int(w) for w in fs.wl[s2]], 'series': [{'name': 'grade %d' % g, 'values': [r3(v) for v in fs['mean_%d' % g][s2]]} for g in GR]}
cc = pd.read_csv(D + 'o1_corr_curves.csv'); s3 = cc.wl % 10 == 0
out['corr'] = {'labels': [int(w) for w in cc.wl[s3]], 'series': [{'name': 'reflectance', 'values': [r3(v) for v in cc.r_R[s3]]}, {'name': 'first derivative', 'values': [r3(v) for v in cc.r_FD[s3]]}]}
F = pd.read_csv(D + 'indices_full.csv')
out['wri_by_grade'] = [r3(F.WRI[M.grade == g].mean()) for g in GR]
rl = pd.read_csv(D + 'o1_relief.csv')
out['relief'] = {k: rl.sort_values(k, ascending=False).head(10)[['index', k]].values.tolist() for k in ['ReliefF_classes', 'ReliefF_binary', 'RReliefF_score']}
out['relief_r'] = rl.set_index('index').r_score.round(3).to_dict()
out['grade_by'] = {f: [[str(k), r3(v)] for k, v in M.groupby(f).grade.mean().items()] for f in ['stage', 'variety', 'leaf', 'timing']}
out['folds'] = {f: dict(OW=SEL[f]['OW'], VI=SEL[f]['VI'], DSF=SEL[f]['DSF'], ndsi=SEL[f]['ndsi'], rsi=SEL[f]['rsi'], wri=SEL[f]['wri']) for f in SEL}
out['fold_sizes'] = [dict(fold=f + 1, test=int((M.fold == f).sum()), train=int((M.fold != f).sum()), test_healthy=int(((M.fold == f) & (M.block == 'C')).sum())) for f in range(3)]
mls = pd.read_csv(D + 'ml_selection.csv'); mls['n'] = mls.selected.map(lambda s: len(eval(s)))
out['sffs'] = mls.groupby(['task', 'model']).agg(n_mean=('n', 'mean'), n_cand=('n_candidates', 'mean'), inner=('inner_score', 'mean')).round(2).reset_index().values.tolist()
out['sffs_params'] = mls[mls.fold == 0][['task', 'model', 'params']].values.tolist()
MT = pd.read_csv(D + 'metrics_all.csv'); out['metrics'] = json.loads(MT.round(4).to_json(orient='records')); out['best'] = json.load(open(D + 'best_models.json'))
for fn, key in (('dl_summary_config.csv', 'config'), ('dl_summary_ablation.csv', 'ablation'), ('strata_metrics.csv', 'strata'), ('transfer_tests.csv', 'transfer'), ('covariate_baseline.csv', 'covariates'),
                ('weather_covariates.csv', 'weather'), ('exploratory_asymptomatic.csv', 'exploratory'), ('selection_stability.csv', 'stability'), ('dl_runs.csv', 'dl_runs')):
    if os.path.exists(D + fn): out[key] = json.loads(pd.read_csv(D + fn).round(4).to_json(orient='records'))
if os.path.exists(D + 'dl_main.json'):
    R = json.load(open(D + 'dl_main.json')); rr = [x for x in R if x['net'] == 'DT-EDNet' and x['task'] == 'B' and x['fold'] == 0]
    if rr: h = np.array(rr[0]['hist']); out['lc'] = {'labels': [int(e) for e in h[:, 0]], 'series': [{'name': 'training loss', 'values': [r3(v) for v in h[:, 1]]}, {'name': 'validation loss', 'values': [r3(v) for v in h[:, 2]]}, {'name': 'validation macro-F1', 'values': [r3(v) for v in h[:, 3]]}]}
allp = pd.read_csv(D + 'all_predictions.csv')
for src in ('ML', 'DL'):
    mname = out['best']['C'][src]
    if mname:
        d = allp[(allp.task == 'C') & (allp.model == mname)]; sub = d.sample(min(700, len(d)), random_state=1)
        out['scatter_' + src] = dict(model=mname, x=[r3(v) for v in sub.y + np.random.default_rng(2).uniform(-0.25, 0.25, len(sub))], y=[r3(v) for v in sub.pred], mean=[r3(d[d.y == g].pred.mean()) for g in GR])
if os.path.exists(D + 'shap_C.npy'):
    sv = np.load(D + 'shap_C.npy'); X = pd.read_csv(D + 'shap_X.csv'); out['shap_C'] = sorted([[c, r3(v)] for c, v in zip(X.columns, np.abs(sv).mean(0))], key=lambda t: -t[1])

out['rep'] = [r3(F.REP[M.grade == g].mean()) for g in GR]; out['dr'] = [r3(F.Dr[M.grade == g].mean()) for g in GR]
out['bands'] = [[w] + [r3(ms.loc[ms.wl == w, 'mean_%d' % g].iloc[0]) for g in GR] for w in (550, 680, 760, 800, 1450, 1650, 1940, 2200)]
out['vif'] = O1['VIF_final']; out['das0'] = {'D1': 58, 'D2': 49, 'D3': 40, 'D4': 27}
P_ = '../outputs/ASD_2025-26_models/'
for fn, key in (('ml_models_index.csv', 'ml_files'), ('dl_models_index.csv', 'dl_files')):
    if os.path.exists(B + P_ + fn): out[key] = json.loads(pd.read_csv(B + P_ + fn).to_json(orient='records'))
out['refs'] = json.load(open(D + 'refs_used.json')) if os.path.exists(D + 'refs_used.json') else []
st_ = pd.read_csv(D + 'selection_stability.csv'); out['sffs_top'] = list(st_[st_.group.str.startswith('SFFS')].groupby('feature').folds.sum().sort_values(ascending=False).index[:5])
out['prog'] = json.loads(pd.read_csv(D + 'disease_progress.csv').round(3).to_json(orient='records'))
for fn, key in (('cov2_metrics.csv', 'cov2_metrics'), ('cov2_gains.csv', 'cov2_gains'), ('cov2_delong.csv', 'cov2_delong'), ('cov2_b1_coef.csv', 'cov2_coef'), ('cov2_covariates_by_date.csv', 'cov2_dates')):
    if os.path.exists(D + fn): out[key] = json.loads(pd.read_csv(D + fn).round(4).to_json(orient='records'))
if os.path.exists(D + 'cov2_summary.json'): out['cov2_summary'] = json.load(open(D + 'cov2_summary.json'))
lp = pd.crosstab(M.date, M.leaf); pp = M.groupby(['date', 'plot']).size(); Xl = np.load(D + 'X_leaf.npy')
out['leafpos'] = [dict(date=d, **{c: int(lp.loc[d].get(c, 0)) for c in ('L3', 'L4', 'L5', 'LL')}, n=int(lp.loc[d].sum()), plots=int(M[M.date == d]['plot'].nunique()),
                       med=int(pp.loc[d].median()), mn=int(pp.loc[d].min()), mx=int(pp.loc[d].max())) for d in sorted(M.date.unique())]
out['qc'] = dict(n_healthy_block=int((M.block == 'C').sum()), healthy_block_diseased=int(((M.block == 'C') & (M.grade > 0)).sum()), n_inoc=int((M.inoculated == 1).sum()),
                 n_inoc_healthy=int(((M.inoculated == 1) & (M.grade == 0)).sum()), n_inoc_dis=int(((M.inoculated == 1) & (M.grade > 0)).sum()),
                 rmin=round(float(Xl.min()), 3), rmax=round(float(Xl.max()), 3), nan=int(np.isnan(Xl).sum()), bands=int(Xl.shape[1]), med=int(pp.median()), mn=int(pp.min()), mx=int(pp.max()))
json.dump(out, open(D + 'ppt_data.json', 'w'), indent=0, default=float); print('ppt data ok', len(json.dumps(out)) // 1000, 'kB')
