"""Stage 3: Objective 2 on leaf ASD data - six-grade classification (leaves) and PDI regression (plots), nested leave-one-replication-out."""
import numpy as np, pandas as pd, json, os, time, warnings
from joblib import Parallel, delayed
from sklearn.svm import SVC, SVR
from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor
from sklearn.neighbors import KNeighborsClassifier, KNeighborsRegressor
from sklearn.neural_network import MLPClassifier, MLPRegressor
from sklearn.cross_decomposition import PLSRegression
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import GroupKFold
from sklearn.base import BaseEstimator, RegressorMixin
class PLSc(BaseEstimator, RegressorMixin):
    """PLSR whose number of components is capped at the number of features."""
    def __init__(self, nc=3): self.nc = nc
    def fit(self, X, y): self.m_ = PLSRegression(min(self.nc, X.shape[1])).fit(X, y); return self
    def predict(self, X): return np.ravel(self.m_.predict(X))
from sklearn.metrics import f1_score, accuracy_score, cohen_kappa_score, confusion_matrix, precision_recall_fscore_support, r2_score, mean_squared_error
import lib
warnings.filterwarnings('ignore')
D = os.path.dirname(os.path.abspath(__file__)) + '/data/'
Z = np.load(D + 'prep.npz'); M = pd.read_csv(D + 'meta_leaf2.csv'); P = pd.read_csv(D + 'plot_table.csv')
F = pd.read_csv(D + 'feat_leaf_wri.csv'); Fp = pd.read_csv(D + 'feat_plot_wri.csv')
wl = Z['b5']; Bl = {t: Z[t] for t in ('R', 'FD', 'SD')}; Bp = {t: Z[t + 'p'] for t in ('R', 'FD', 'SD')}
y = M.grade.values; grp = M['plot'].values; fold = M.fold.values; pdi = P.PDI.values; pfold = P.fold.values; pgrp = P['plot'].values
G6 = np.array([0, 1, 3, 5, 7, 9]); gi = lambda v: np.searchsorted(G6, v)
featnames = list(F.columns[:51]) + ['WRI_VNIR', 'WRI_SWIR']
t0 = time.time(); KMAX = 8

def bandval(B, L, rows=None):
    d = pd.DataFrame({'%s%d' % (t, w): B[t][:, list(wl).index(w)] for t, w in L})
    return d if rows is None else d.iloc[rows].reset_index(drop=True)

# ---------------- models ----------------
CLS = {'SVM': lambda **k: make_pipeline(StandardScaler(), SVC(C=k.get('C', 10), gamma=k.get('gamma', 'scale'), class_weight='balanced')),
       'RF': lambda **k: RandomForestClassifier(k.get('n', 100), max_features=k.get('mf', 'sqrt'), min_samples_leaf=k.get('leaf', 1), class_weight='balanced', random_state=0, n_jobs=1),
       'k-NN': lambda **k: make_pipeline(StandardScaler(), KNeighborsClassifier(k.get('k', 7), weights=k.get('wt', 'distance')))}
REG = {'SVR': lambda **k: make_pipeline(StandardScaler(), SVR(C=k.get('C', 100), epsilon=k.get('eps', 2), gamma=k.get('gamma', 'scale'))),
       'RFR': lambda **k: RandomForestRegressor(k.get('n', 100), max_features=k.get('mf', 1.0), min_samples_leaf=k.get('leaf', 2), random_state=0, n_jobs=1),
       'k-NN': lambda **k: make_pipeline(StandardScaler(), KNeighborsRegressor(k.get('k', 5), weights=k.get('wt', 'distance'))),
       'PLSR': lambda **k: make_pipeline(StandardScaler(), PLSc(k.get('nc', 3)))}
GRID = {'SVM': [dict(C=c, gamma=g) for c in (1, 10, 100) for g in ('scale', 0.05)], 'RF': [dict(n=300, mf=m, leaf=l) for m in ('sqrt', 0.5) for l in (1, 3)],
        'k-NN': [dict(k=k, wt=w) for k in (5, 9, 15) for w in ('uniform', 'distance')],
        'SVR': [dict(C=c, eps=e) for c in (10, 100, 1000) for e in (1, 3)], 'RFR': [dict(n=300, mf=m, leaf=l) for m in (0.5, 1.0) for l in (1, 3)],
        'PLSR': [dict(nc=c) for c in range(1, 9)]}

def cv_score(X, yy, gg, make, task, kw={}):
    sc = []
    for tr, te in GroupKFold(3).split(X, yy, gg):
        m = make(**kw).fit(X[tr], yy[tr]); p = np.ravel(m.predict(X[te]))
        sc.append(f1_score(yy[te], p, average='macro') if task == 'c' else -np.sqrt(mean_squared_error(yy[te], p)))
    return float(np.mean(sc))

def sffs(Xdf, yy, gg, make, task, kmax=KMAX):
    """ML-SFFS (Pudil et al., 1994) with the model's grouped-CV score as criterion."""
    X = Xdf.values; nf = X.shape[1]; sel = []; best = {}; kmax = min(kmax, nf)
    ev = lambda cols: cv_score(X[:, cols], yy, gg, make, task)
    while len(sel) < kmax:
        cand = [j for j in range(nf) if j not in sel]
        s = Parallel(n_jobs=4)(delayed(ev)(sel + [j]) for j in cand); j = cand[int(np.argmax(s))]; sel = sel + [j]; cur = max(s)
        if cur > best.get(len(sel), (-1e9,))[0]: best[len(sel)] = (cur, list(sel))
        while len(sel) > 2:                                     # floating step: conditional exclusion
            rem = Parallel(n_jobs=4)(delayed(ev)([q for q in sel if q != r]) for r in sel)
            r = sel[int(np.argmax(rem))]
            if max(rem) > best.get(len(sel) - 1, (-1e9,))[0] + 1e-9: sel = [q for q in sel if q != r]; best[len(sel)] = (max(rem), list(sel))
            else: break
    ks = sorted(best); top = max(best[k][0] for k in ks); tol = 0.01 if task == 'c' else 0.02 * abs(top)
    kopt = min(k for k in ks if best[k][0] >= top - tol)
    return [Xdf.columns[q] for q in best[kopt][1]], {k: best[k][0] for k in ks}

def tune(X, yy, gg, name, task):
    make = (CLS if task == 'c' else REG)[name]
    s = Parallel(n_jobs=4)(delayed(cv_score)(X, yy, gg, make, task, kw) for kw in GRID[name])
    return GRID[name][int(np.argmax(s))]

# ---------------- nested LORO ----------------
out = {'cls': {}, 'reg': {}, 'folds': []}
predC = {m: np.zeros(len(y), int) for m in list(CLS) + ['MLP', 'PLS-DA (full spectrum)', 'RF (all 53 features)']}
predR = {m: np.zeros(len(pdi)) for m in list(REG) + ['MLP', 'PLSR (full spectrum)', 'RFR (all 53 features)']}
for f in range(3):
    tr, te = np.where(fold != f)[0], np.where(fold == f)[0]; ptr, pte = np.where(pfold != f)[0], np.where(pfold == f)[0]
    S = lib.select_bands({t: Bl[t][tr] for t in Bl}, {t: Bp[t][ptr] for t in Bp}, wl, y[tr], grp[tr], pdi[ptr])
    cb, rb = S['robust'] + S['clsonly'], S['robust'] + S['regonly']
    XcA = pd.concat([bandval(Bl, cb), F[featnames]], axis=1); XrA = pd.concat([bandval(Bp, rb), Fp[featnames]], axis=1)
    bc = lib.boruta(XcA.values[tr], y[tr], 'c', seed=f); br = lib.boruta(XrA.values[ptr], pdi[ptr], 'r', seed=f)
    poolC = list(XcA.columns[bc.support_]); poolR = list(XrA.columns[br.support_])
    vC = lib.vif_filter(XcA.iloc[tr][poolC], 10); vR = lib.vif_filter(XrA.iloc[ptr][poolR], 10)
    info = dict(fold=f, test_rep='R%d' % (f + 1), n_cls_bands=len(cb), n_reg_bands=len(rb), boruta_cls=len(poolC), boruta_reg=len(poolR), vif_cls=vC, vif_reg=vR, ofc={})
    print('fold', f, 'bands', len(cb), len(rb), 'Boruta', len(poolC), len(poolR), 'VIF', len(vC), len(vR), '%.0fs' % (time.time() - t0), flush=True)
    for name in CLS:
        ofc, curve = sffs(XcA.iloc[tr][vC].reset_index(drop=True), y[tr], grp[tr], CLS[name], 'c')
        kw = tune(XcA.iloc[tr][ofc].values, y[tr], grp[tr], name, 'c')
        m = CLS[name](**kw).fit(XcA.iloc[tr][ofc].values, y[tr]); predC[name][te] = m.predict(XcA.iloc[te][ofc].values)
        info['ofc'][name] = dict(features=ofc, params=kw, curve=curve); print('  ', name, ofc, kw, '%.0fs' % (time.time() - t0), flush=True)
    # MLP (small DNN) on the VIF-filtered Boruta pool
    mlp = make_pipeline(StandardScaler(), MLPClassifier(hidden_layer_sizes=(16, 8), alpha=1e-2, early_stopping=True, max_iter=2000, random_state=0))
    predC['MLP'][te] = mlp.fit(XcA.iloc[tr][vC].values, y[tr]).predict(XcA.iloc[te][vC].values)
    # baselines: PLS-DA on full reflectance spectrum (349 bands) and RF on all 53 features without selection
    Ytr = np.eye(6)[gi(y[tr])]; best_nc = max(range(2, 16, 2), key=lambda nc: np.mean([f1_score(y[tr][b], G6[PLSRegression(nc).fit(Bl['R'][tr][a], Ytr[a]).predict(Bl['R'][tr][b]).argmax(1)], average='macro') for a, b in GroupKFold(3).split(tr, groups=grp[tr])]))
    predC['PLS-DA (full spectrum)'][te] = G6[PLSRegression(best_nc).fit(Bl['R'][tr], Ytr).predict(Bl['R'][te]).argmax(1)]
    predC['RF (all 53 features)'][te] = RandomForestClassifier(300, class_weight='balanced', random_state=0, n_jobs=-1).fit(F[featnames].values[tr], y[tr]).predict(F[featnames].values[te])
    info['plsda_nc'] = best_nc
    for name in REG:
        ofc, curve = sffs(XrA.iloc[ptr][vR].reset_index(drop=True), pdi[ptr], pgrp[ptr], REG[name], 'r')
        kw = tune(XrA.iloc[ptr][ofc].values, pdi[ptr], pgrp[ptr], name, 'r')
        m = REG[name](**kw).fit(XrA.iloc[ptr][ofc].values, pdi[ptr]); predR[name][pte] = np.clip(np.ravel(m.predict(XrA.iloc[pte][ofc].values)), 0, 100)
        info['ofc']['R_' + name] = dict(features=ofc, params=kw, curve=curve); print('  ', name, ofc, kw, flush=True)
    mlpr = make_pipeline(StandardScaler(), MLPRegressor(hidden_layer_sizes=(16, 8), alpha=1e-1, early_stopping=True, max_iter=5000, random_state=0))
    predR['MLP'][pte] = np.clip(mlpr.fit(XrA.iloc[ptr][vR].values, pdi[ptr]).predict(XrA.iloc[pte][vR].values), 0, 100)
    nc = tune(Bp['R'][ptr], pdi[ptr], pgrp[ptr], 'PLSR', 'r')['nc']
    predR['PLSR (full spectrum)'][pte] = np.clip(np.ravel(REG['PLSR'](nc=nc).fit(Bp['R'][ptr], pdi[ptr]).predict(Bp['R'][pte])), 0, 100)
    predR['RFR (all 53 features)'][pte] = np.clip(RandomForestRegressor(300, random_state=0, n_jobs=-1).fit(Fp[featnames].values[ptr], pdi[ptr]).predict(Fp[featnames].values[pte]), 0, 100)
    info['plsr_nc'] = nc
    out['folds'].append(info)

# ---------------- metrics ----------------
def cmetrics(p):
    cm = confusion_matrix(y, p, labels=G6); Pp, Rr, F1, _ = precision_recall_fscore_support(y, p, labels=G6, zero_division=0)
    det = ((p > 0) == (y > 0)).mean()
    return dict(oa=accuracy_score(y, p), kappa=cohen_kappa_score(y, p), macro_f1=f1_score(y, p, average='macro'), adj=float(np.mean(np.abs(gi(p) - gi(y)) <= 1)),
                detection_acc=float(det), P=Pp.tolist(), R=Rr.tolist(), F1=F1.tolist(), cm=cm.tolist(),
                fold_mf1=[f1_score(y[fold == f], p[fold == f], average='macro') for f in range(3)])
def rmetrics(p, obs=pdi):
    rmse = np.sqrt(mean_squared_error(obs, p))
    return dict(r2=r2_score(obs, p), rmse=rmse, nrmse=rmse / obs.mean(), rpd=obs.std() / rmse, fold_r2=[r2_score(obs[pfold == f], p[pfold == f]) for f in range(3)])
for k, p in predC.items(): out['cls'][k] = cmetrics(p)
for k, p in predR.items(): out['reg'][k] = rmetrics(p)
bestC = max(CLS, key=lambda k: out['cls'][k]['macro_f1']); bestR = max(list(REG) + ['MLP'], key=lambda k: out['reg'][k]['r2'])
# bottom-up PDI from predicted leaf grades of the best classifier
order = {k: i for i, k in enumerate(P.pd)}; gidx = M.pd.map(order).values
pdi_bu = np.array([predC[bestC][gidx == i].sum() / (9 * (gidx == i).sum()) * 100 for i in range(len(P))])
out['reg']['Bottom-up (from %s leaf grades)' % bestC] = rmetrics(pdi_bu); predR['Bottom-up (from %s leaf grades)' % bestC] = pdi_bu
# by date and variety (best models)
out['by_date'] = {d: dict(macro_f1=f1_score(y[M.date == d], predC[bestC][M.date == d], average='macro'), oa=accuracy_score(y[M.date == d], predC[bestC][M.date == d]),
                         r2=r2_score(pdi[P.date == d], predR[bestR][P.date == d]) if pdi[P.date == d].std() > 0 else None,
                         rmse=float(np.sqrt(mean_squared_error(pdi[P.date == d], predR[bestR][P.date == d])))) for d in sorted(M.date.unique())}
out['by_variety'] = {v: dict(macro_f1=f1_score(y[M.variety == v], predC[bestC][M.variety == v], average='macro'), r2=r2_score(pdi[P.variety == v], predR[bestR][P.variety == v])) for v in sorted(M.variety.unique())}
out['best'] = dict(cls=bestC, reg=bestR)
pd.DataFrame({'date': M.date, 'plot': M['plot'], 'fold': fold, 'observed': y, **{'pred_' + k: v for k, v in predC.items()}}).to_csv(D + 'pred_cls.csv', index=False)
pd.DataFrame({'date': P.date, 'plot': P['plot'], 'fold': pfold, 'variety': P.variety, 'observed_PDI': pdi, **{'pred_' + k: v for k, v in predR.items()}}).to_csv(D + 'pred_reg.csv', index=False)
json.dump(out, open(D + 'res2.json', 'w'), indent=1, default=lambda o: o.item() if hasattr(o, 'item') else str(o))
print('best', bestC, out['cls'][bestC]['macro_f1'], bestR, out['reg'][bestR]['r2'], 'total %.0fs' % (time.time() - t0))
for k, v in out['cls'].items(): print('C %-26s OA %.3f kappa %.3f mF1 %.3f adj %.3f det %.3f' % (k, v['oa'], v['kappa'], v['macro_f1'], v['adj'], v['detection_acc']))
for k, v in out['reg'].items(): print('R %-34s R2 %.3f RMSE %.2f RPD %.2f' % (k, v['r2'], v['rmse'], v['rpd']))
