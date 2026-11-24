"""Apply the 2025-26 ASD leaf models to the UAV hyperspectral plot spectra of 24 Feb 2026 and evaluate them.
Variants: (1) direct transfer of the frozen ASD models; (2) healthy-reference correction (wavelength-wise gain that maps the
healthy UAV plots onto the healthy ASD leaves of the same day; leave-one-out for healthy plots); (3) in-domain check: the best
ML model type refitted on the UAV plots with the ASD leave-one-replication-out folds (features inside UAV band gaps removed).
Outputs -> uavt/out/*.csv|json"""
import sys, os, json, glob, warnings, numpy as np, pandas as pd
warnings.filterwarnings('ignore')
HERE = os.path.dirname(os.path.abspath(__file__)); TB = os.path.join(HERE, '..')
MD = os.path.join(TB, 'outputs', 'ASD_2025-26_models'); AD = os.path.join(TB, 'asd26', 'data') + '/'
UAV = os.path.join(TB, 'uavhs', 'data', 'envi_plot_avg.txt'); OUT = os.path.join(HERE, 'out') + '/'
os.makedirs(OUT, exist_ok=True)
sys.path.insert(0, MD)
from wr_features import all_features, GRADES
import joblib, torch, wr_networks as NW
from sklearn.base import clone
from sklearn.metrics import (accuracy_score, balanced_accuracy_score, f1_score, recall_score, roc_auc_score, cohen_kappa_score,
                             r2_score, mean_squared_error, mean_absolute_error, confusion_matrix)
from sklearn.decomposition import PCA
DATE = '2026-02-24'; TASKS = {'A': 'Detection (healthy vs diseased)', 'B': 'Six-grade severity', 'C': 'Severity score (0-9)'}

# ---------------- UAV plot spectra ----------------
L = open(UAV).read().splitlines(); n = sum(l.startswith('Column') for l in L)
A = np.array([[float(x) for x in l.split()] for l in L[n + 1:] if l.strip()]); wlU, RU = A[:, 0], A[:, 1:].T          # 48 x 483
NP = RU.shape[0]
GAPS = [(wlU[i], wlU[i + 1]) for i in np.where(np.diff(wlU) > 8)[0]]

# ---------------- ground truth (ASD leaf scores of the same day) ----------------
M = pd.read_csv(AD + 'meta.csv'); X0 = np.load(AD + 'X_leaf.npy').astype(float); wl0 = np.load(AD + 'wl.npy')
d = M[M.date == DATE]
P = M.groupby('plot')[['block', 'variety', 'timing', 'fold']].first()
gt = pd.DataFrame(index=range(1, NP + 1)); gt.index.name = 'plot'
gt['block'] = P.block; gt['variety'] = P.variety; gt['sowing'] = P.timing; gt['fold'] = P.fold
gt['status'] = np.where(gt.block == 'C', 'Healthy', 'Diseased'); gt['A'] = (gt.status == 'Diseased').astype(int)
gt['n_leaves'] = d.groupby('plot').size()
gt['score'] = d.groupby('plot').score.mean()
gt['score_L3'] = d[d.leaf == 'L3'].groupby('plot').score.mean()
gt['PDI'] = gt.score / 9 * 100
gt['grade'] = [GRADES[int(np.argmin([abs(s - g) for g in GRADES]))] for s in gt.score]          # nearest grade (ties -> lower)
gt['DI_class'] = [0 if x == 0 else 1 if x <= 5 else 3 if x <= 10 else 5 if x <= 25 else 7 if x <= 50 else 9 for x in gt.PDI]
gt['stage'] = d.groupby('plot').stage.agg(lambda s: s.mode().iloc[0])
gt.to_csv(OUT + 'ground_truth.csv')

# ---------------- spectra variants ----------------
md = M.date == DATE
Hasd = X0[(md & (M.status == 'Healthy')).values].mean(0); Dasd = X0[(md & (M.status == 'Diseased')).values].mean(0)
HasdU = np.interp(wlU, wl0, Hasd)
hidx = np.where(gt.status.values == 'Healthy')[0]
RC = np.empty_like(RU)
for p in range(NP):
    ref = [h for h in hidx if h != p]                      # a healthy plot never corrects itself
    RC[p] = RU[p] * HasdU / RU[ref].mean(0)
RB = RC * HasdU.mean() / RC.mean(1, keepdims=True)          # + brightness normalisation: same mean reflectance as the ASD healthy leaves (shape only)
SPEC = {'Direct': RU, 'Healthy-reference corrected': RC, 'Corrected + brightness-normalised': RB}
VTAG = {'Direct': 'direct', 'Healthy-reference corrected': 'corrected', 'Corrected + brightness-normalised': 'normalised'}
pd.DataFrame({'wavelength': wlU, 'ASD healthy (24 Feb)': HasdU, 'ASD diseased (24 Feb)': np.interp(wlU, wl0, Dasd),
              'UAV healthy': RU[hidx].mean(0), 'UAV diseased': RU[gt.A.values == 1].mean(0),
              'UAV healthy corrected': RC[hidx].mean(0), 'UAV diseased corrected': RC[gt.A.values == 1].mean(0), 'UAV healthy normalised': RB[hidx].mean(0), 'UAV diseased normalised': RB[gt.A.values == 1].mean(0)}).to_csv(OUT + 'spectra_compare.csv', index=False)
pd.DataFrame(RC.T, columns=['P%d' % p for p in range(1, NP + 1)]).assign(wavelength=wlU).to_csv(OUT + 'uav_corrected_spectra.csv', index=False)

sel = json.load(open(os.path.join(MD, 'feature_selection.json')))
FE = {v: all_features(S, wlU, sel) for v, S in SPEC.items()}
FA = all_features(X0, wl0, sel)                            # ASD leaves (all dates) for the domain check

# ---------------- metrics ----------------
GI = {g: i for i, g in enumerate(GRADES)}
def metrics(task, y, yp, s=None):
    y, yp = np.asarray(y), np.asarray(yp)
    if task == 'A':
        out = dict(OA=accuracy_score(y, yp), balanced_acc=balanced_accuracy_score(y, yp), macro_F1=f1_score(y, yp, average='macro'),
                   sensitivity=recall_score(y, yp, pos_label=1, zero_division=0), specificity=recall_score(y, yp, pos_label=0, zero_division=0),
                   pred_diseased=int(yp.sum()), pred_healthy=int((yp == 0).sum()))
        out['AUC'] = roc_auc_score(y, s) if s is not None and len(np.unique(s)) > 1 else np.nan
        return out
    if task == 'B':
        yi, pi = np.array([GI[int(v)] for v in y]), np.array([GI[int(v)] for v in yp])
        return dict(OA=accuracy_score(y, yp), macro_F1=f1_score(y, yp, average='macro'), QWK=cohen_kappa_score(yi, pi, labels=list(range(len(GRADES))), weights='quadratic') if len(np.unique(np.r_[yi, pi])) > 1 else np.nan,
                    within1=np.mean(np.abs(yi - pi) <= 1), pred_grades=' '.join('%d:%d' % (g, (yp == g).sum()) for g in GRADES if (yp == g).any()))
    rmse = np.sqrt(mean_squared_error(y, yp))
    return dict(R2=r2_score(y, yp), RMSE=rmse, MAE=mean_absolute_error(y, yp), bias=float(np.mean(yp - y)), r=np.corrcoef(y, yp)[0, 1] if np.std(yp) > 0 else np.nan,
                RPD=np.std(y, ddof=1) / rmse, r_diseased=np.corrcoef(y[gt.A.values == 1], yp[gt.A.values == 1])[0, 1] if np.std(yp[gt.A.values == 1]) > 0 else np.nan,
                pred_min=float(yp.min()), pred_max=float(yp.max()))
TRUE = {'A': gt.A.values, 'B': gt.grade.values, 'C': gt.score.values}

# ---------------- frozen ASD models on the UAV spectra ----------------
rows, mrows, used = [], [], {}
for f in sorted(glob.glob(os.path.join(MD, 'ml', '*.joblib'))):
    b = joblib.load(f); used[(b['task'], b['model_name'])] = b['features']
    for v, F in FE.items():
        Z = (F[b['candidate_features']].values - b['scaler_mean']) / b['scaler_sd']; Z = Z[:, b['idx']]
        yp = b['model'].predict(Z); s = None
        if b['task'] == 'A':
            yp = yp.astype(int)
            s = b['model'].decision_function(Z) if b['model_name'] == 'SVM' else b['model'].predict_proba(Z)[:, 1]
        elif b['task'] == 'B': yp = np.array([GRADES[int(i)] for i in yp])
        else: yp = np.clip(yp, 0, 9)
        for p in range(NP): rows.append(dict(task=b['task'], model=b['model_name'], source='ML', variant=v, plot=p + 1, y=TRUE[b['task']][p], pred=yp[p], score=None if s is None else float(s[p])))
        mrows.append(dict(task=b['task'], model=b['model_name'], source='ML', variant=v, **metrics(b['task'], TRUE[b['task']], yp, s)))
for f in sorted(glob.glob(os.path.join(MD, 'dl', '*.pt'))):
    b = torch.load(f, map_location='cpu', weights_only=False); used[(b['task'], b['net'])] = b['features']
    m = NW.build(b['net'], b['k'], len(b['features']), b['n_out'], 0.03); m.load_state_dict(b['state_dict']); m.eval()
    for v, F in FE.items():
        Z = ((F[b['features']].values - b['scaler_mean']) / b['scaler_sd']).astype(np.float32)
        Zi = Z.reshape(-1, 1, 1, Z.shape[1]) if b['net'] == 'DNN-F1' else NW.pseudo(Z)[0]
        with torch.no_grad(): o = m(torch.tensor(Zi))
        s = None
        if b['task'] == 'A': pr = torch.softmax(o, 1).numpy(); yp = pr.argmax(1); s = pr[:, 1]
        elif b['task'] == 'B': yp = np.array([GRADES[i] for i in o.argmax(1).numpy()])
        else: yp = np.clip(o.ravel().numpy(), 0, 9)
        for p in range(NP): rows.append(dict(task=b['task'], model=b['net'], source='DL', variant=v, plot=p + 1, y=TRUE[b['task']][p], pred=yp[p], score=None if s is None else float(s[p])))
        mrows.append(dict(task=b['task'], model=b['net'], source='DL', variant=v, **metrics(b['task'], TRUE[b['task']], yp, s)))
pred = pd.DataFrame(rows); met = pd.DataFrame(mrows)

# ---------------- best ASD models (leave-one-replication-out on the leaves) ----------------
best = json.load(open(AD + 'best_models.json')); asd = pd.read_csv(AD + 'metrics_all.csv')
KEY = {'A': 'macro_F1', 'B': 'macro_F1', 'C': 'R2'}
best_rows = []
for t in 'ABC':
    for role in ('overall', 'ML', 'DL'):
        mname = best[t][role]; a = asd[(asd.task == t) & (asd.model == mname)]
        best_rows.append(dict(task=t, role=role, model=mname, asd_metric=KEY[t], asd_value=float(a[KEY[t]].iloc[0]) if len(a) else np.nan,
                              asd_n=int(a.n.iloc[0]) if len(a) else np.nan))
bestdf = pd.DataFrame(best_rows)

# ---------------- in-domain check: best ML model type refitted on the UAV plots (LORO, same folds) ----------------
def bands(name):
    if name[:2] == 'FD' and name[2:].isdigit(): return [int(name[2:])]
    if name[:1] == 'R' and name[1:].isdigit(): return [int(name[1:])]
    IDX = {'WI': [900, 970], 'WBI': [970, 900], 'NDSI_best': list(sel['ndsi']), 'RSI_best': list(sel['rsi']), 'WRI': [sel['wri']['l1'], sel['wri']['l2'], sel['wri']['l3']]}
    return IDX.get(name, [])
in_gap = lambda name: any(lo < w < hi for w in bands(name) for lo, hi in GAPS)
irows, imet = [], []
for t in 'ABC':
    mname = best[t]['ML']; b = joblib.load(glob.glob(os.path.join(MD, 'ml', '%s_*_%s.joblib' % (t, mname)))[0])
    feats = [c for c in b['features'] if not in_gap(c)]
    F = FE['Direct'][feats].values; y = TRUE[t]; yp = np.zeros(NP, dtype=float); s = np.full(NP, np.nan)
    for k in sorted(gt.fold.unique()):
        te = gt.fold.values == k; tr = ~te
        mu, sd = F[tr].mean(0), F[tr].std(0) + 1e-12; Ztr, Zte = (F[tr] - mu) / sd, (F[te] - mu) / sd
        mdl = clone(b['model'])
        if t == 'B':
            cls = np.unique(y[tr]); enc = {c: i for i, c in enumerate(cls)}
            mdl.fit(Ztr, np.array([enc[c] for c in y[tr]])); yp[te] = cls[mdl.predict(Zte).astype(int)]
        elif t == 'A':
            mdl.fit(Ztr, y[tr]); yp[te] = mdl.predict(Zte)
            s[te] = mdl.decision_function(Zte) if hasattr(mdl, 'decision_function') and mname == 'SVM' else mdl.predict_proba(Zte)[:, 1]
        else: mdl.fit(Ztr, y[tr]); yp[te] = np.clip(mdl.predict(Zte), 0, 9)
    if t != 'C': yp = yp.astype(int)
    for p in range(NP): irows.append(dict(task=t, model=mname, plot=p + 1, fold=int(gt.fold.values[p]), y=y[p], pred=yp[p], score=None if t != 'A' else float(s[p])))
    imet.append(dict(task=t, model=mname, variant='UAV-trained (LORO)', features=', '.join(feats), n_features=len(feats),
                     dropped_gap_features=', '.join(c for c in b['features'] if in_gap(c)), **metrics(t, y, yp, s if t == 'A' else None)))
ipred = pd.DataFrame(irows); imetdf = pd.DataFrame(imet)

# ---------------- uncertainty: plot bootstrap CIs (best models + UAV-trained) and permutation test of the UAV-trained models ----------------
rng = np.random.default_rng(42); NB = 2000; KEYM = {'A': ['macro_F1', 'AUC', 'balanced_acc'], 'B': ['macro_F1', 'QWK', 'within1'], 'C': ['R2', 'RMSE', 'r']}
hi_, di_ = np.where(gt.A.values == 0)[0], np.where(gt.A.values == 1)[0]
boots = [np.r_[rng.choice(hi_, len(hi_)), rng.choice(di_, len(di_))] for _ in range(NB)]       # stratified by status so both classes stay present
def ci(task, y, yp, s=None):
    out = {}
    vals = {k: [] for k in KEYM[task]}
    for bi in boots:
        try: mm = metrics(task, y[bi], yp[bi], None if s is None else s[bi])
        except Exception: continue
        for k in KEYM[task]: vals[k].append(mm.get(k, np.nan))
    for k in KEYM[task]:
        v = np.array(vals[k], float); v = v[np.isfinite(v)]
        out[k + '_lo'], out[k + '_hi'] = (np.percentile(v, 2.5), np.percentile(v, 97.5)) if len(v) else (np.nan, np.nan)
    return out
crow = []
for t in 'ABC':
    for role in ('overall', 'ML', 'DL'):
        for v in SPEC:
            d = pred[(pred.task == t) & (pred.model == best[t][role]) & (pred.variant == v)].sort_values('plot')
            s = d.score.values.astype(float) if t == 'A' else None
            crow.append(dict(task=t, role=role, model=best[t][role], variant=v, **metrics(t, d.y.values, d.pred.values, s), **ci(t, d.y.values.astype(float) if t == 'C' else d.y.values, d.pred.values, s)))
    d = ipred[ipred.task == t].sort_values('plot'); s = d.score.values.astype(float) if t == 'A' else None
    crow.append(dict(task=t, role='UAV-trained', model=d.model.iloc[0], variant='UAV-trained (LORO)', **metrics(t, d.y.values, d.pred.values, s), **ci(t, d.y.values, d.pred.values, s)))
cidf = pd.DataFrame(crow)
def loro(t, y, feats_, model):
    F = FE['Direct'][feats_].values; yp = np.zeros(NP, dtype=float); s = np.full(NP, np.nan)
    for k in sorted(gt.fold.unique()):
        te = gt.fold.values == k; tr = ~te; mu_, sd_ = F[tr].mean(0), F[tr].std(0) + 1e-12; Ztr, Zte = (F[tr] - mu_) / sd_, (F[te] - mu_) / sd_; mdl = clone(model)
        if t == 'B':
            cls = np.unique(y[tr]); enc = {c: i for i, c in enumerate(cls)}; mdl.fit(Ztr, np.array([enc[c] for c in y[tr]])); yp[te] = cls[mdl.predict(Zte).astype(int)]
        elif t == 'A':
            mdl.fit(Ztr, y[tr]); yp[te] = mdl.predict(Zte); s[te] = mdl.decision_function(Zte) if hasattr(mdl, 'decision_function') and type(mdl).__name__ == 'SVC' else mdl.predict_proba(Zte)[:, 1]
        else: mdl.fit(Ztr, y[tr]); yp[te] = np.clip(mdl.predict(Zte), 0, 9)
    return (yp.astype(int) if t != 'C' else yp), s
prow_ = []
NPERM = {'A': 999, 'B': 199, 'C': 199}; PK = {'A': 'AUC', 'B': 'macro_F1', 'C': 'R2'}
for t in 'ABC':
    mname = best[t]['ML']; b = joblib.load(glob.glob(os.path.join(MD, 'ml', '%s_*_%s.joblib' % (t, mname)))[0]); feats_ = [c for c in b['features'] if not in_gap(c)]
    obs = imetdf[imetdf.task == t][PK[t]].iloc[0]; y0 = TRUE[t].copy(); null = []
    for i in range(NPERM[t]):
        yperm = y0.copy()
        for k in sorted(gt.fold.unique()):                     # permute labels within each fold (keeps the fold structure)
            ix = np.where(gt.fold.values == k)[0]; yperm[ix] = rng.permutation(yperm[ix])
        yp, s = loro(t, yperm, feats_, b['model']); null.append(metrics(t, yperm, yp, s if t == 'A' else None)[PK[t]])
    null = np.array(null, float); p = (1 + np.sum(null >= obs)) / (1 + len(null))
    prow_.append(dict(task=t, model=mname, metric=PK[t], observed=obs, null_mean=np.nanmean(null), null_p95=np.nanpercentile(null, 95), n_perm=len(null), p_value=p))
permdf = pd.DataFrame(prow_)

# ---------------- domain check of the best models' input features ----------------
feat_union = []
for t in 'ABC':
    for role in ('overall', 'ML', 'DL'):
        for c in used.get((t, best[t][role]), []):
            if c not in feat_union: feat_union.append(c)
drows = []
for c in feat_union:
    a = FA[c].values; lo, hi = np.percentile(a, 1), np.percentile(a, 99)
    r = dict(feature=c, in_uav_gap=in_gap(c), asd_mean=a.mean(), asd_sd=a.std(), asd_p1=lo, asd_p99=hi)
    for v, F in FE.items():
        u = F[c].values; tag = VTAG[v]
        r['uav_%s_mean' % tag] = u.mean(); r['uav_%s_sd' % tag] = u.std(); r['uav_%s_out_pct' % tag] = 100 * np.mean((u < lo) | (u > hi))
        r['uav_%s_z' % tag] = (u.mean() - a.mean()) / a.std()
    drows.append(r)
dom = pd.DataFrame(drows)
# PCA on the ASD leaves (standardised union features), UAV plots projected
mu, sd = FA[feat_union].values.mean(0), FA[feat_union].values.std(0)
pca = PCA(2).fit((FA[feat_union].values - mu) / sd)
pa = pca.transform((FA[feat_union].values - mu) / sd)
prow = [dict(source='ASD leaf', group='Healthy' if s == 'Healthy' else 'Diseased', date=dt, PC1=x[0], PC2=x[1]) for x, s, dt in zip(pa, M.status, M.date)]
for v, F in FE.items():
    pu = pca.transform((F[feat_union].values - mu) / sd)
    prow += [dict(source='UAV plot (%s)' % v.lower(), group=gt.status.values[p], date=DATE, PC1=pu[p, 0], PC2=pu[p, 1], plot=p + 1) for p in range(NP)]
pcadf = pd.DataFrame(prow)

# ---------------- save ----------------
pred.to_csv(OUT + 'predictions_frozen.csv', index=False); met.to_csv(OUT + 'metrics_frozen.csv', index=False)
ipred.to_csv(OUT + 'predictions_uav_trained.csv', index=False); imetdf.to_csv(OUT + 'metrics_uav_trained.csv', index=False)
bestdf.to_csv(OUT + 'best_models.csv', index=False); cidf.to_csv(OUT + 'ci.csv', index=False); permdf.to_csv(OUT + 'permutation.csv', index=False); dom.to_csv(OUT + 'domain_features.csv', index=False); pcadf.to_csv(OUT + 'pca_domain.csv', index=False)
for v, F in FE.items(): F.assign(plot=range(1, NP + 1)).to_csv(OUT + 'uav_features_%s.csv' % VTAG[v], index=False)
summary = dict(date=DATE, n_plots=NP, n_bands=len(wlU), gaps=[[float(a), float(b)] for a, b in GAPS], feature_union=feat_union,
               pca_var=[float(x) for x in pca.explained_variance_ratio_], best=best, gt_counts=dict(status=gt.status.value_counts().to_dict(), grade=gt.grade.value_counts().sort_index().to_dict()),
               asd_models_trained_on=int(len(M)))
json.dump(summary, open(OUT + 'summary.json', 'w'), indent=1, default=str)
pd.set_option('display.width', 250)
print(bestdf.to_string())
for t in 'ABC':
    cols = {'A': ['macro_F1', 'balanced_acc', 'sensitivity', 'specificity', 'AUC', 'pred_diseased'], 'B': ['OA', 'macro_F1', 'QWK', 'within1', 'pred_grades'], 'C': ['R2', 'RMSE', 'bias', 'r', 'r_diseased', 'pred_min', 'pred_max']}[t]
    print('\n', t, TASKS[t]); print(met[met.task == t][['model', 'source', 'variant'] + cols].round(3).to_string(index=False))
    print(imetdf[imetdf.task == t][['model', 'variant', 'n_features'] + cols].round(3).to_string(index=False))
print(permdf.round(4).to_string(index=False)); print(cidf[[c for c in cidf.columns if c in ('task', 'role', 'model', 'variant', 'macro_F1', 'macro_F1_lo', 'macro_F1_hi', 'AUC', 'AUC_lo', 'AUC_hi', 'R2', 'R2_lo', 'R2_hi')]].round(3).to_string(index=False))
print(dom[['feature', 'in_uav_gap'] + [c for c in dom.columns if c.endswith('out_pct')]].round(1).to_string(index=False))
