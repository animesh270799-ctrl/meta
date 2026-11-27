"""Comparison part 2: how much does the answer depend on WHICH plots are in the test set, and what happens if the split ignores plots?
A fixed, light pipeline is run identically in every scheme so that only the validation scheme differs:
  feature selection inside the training part (effective ranges -> SHAP-CARS (10 runs) -> best NDSI/RSI, WRI -> redundancy filter ->
  ReliefF/RReliefF top 5 -> VIF < 10), then the best machine-learning model of each task in the LORO run (A SVM, B RF, C XGBoost),
  tuned by grid search in 3 inner folds (no SFFS, to keep 29 runs affordable), tested once.
Schemes
  LORO           the three leave-one-replication-out folds of the earlier analysis (pooled, as before)
  main <ratio>     the grouped, stratified split used in the full analysis (ratio from split_cfg.py: 70:30 or 80:20)
  grouped <ratio>  20 other rule-conforming grouped, stratified splits (split_lib.random_splits)  -> split-to-split variability
  leaf <ratio>     5 random splits of LEAVES stratified by grade, inner folds also by leaf (plots ignored) -> leakage check
References: Roberts et al. (2017); Vabalas et al. (2019); Xu and Goodacre (2018); Kohavi (1995).
Usage: python3 c1_repeat.py worker i n   (n parallel workers)   |   python3 c1_repeat.py merge"""
import numpy as np, pandas as pd, os, json, sys, time, warnings
warnings.filterwarnings('ignore')
os.environ.setdefault('OMP_NUM_THREADS', '1')
from alib import r2_maps, effective_ranges, shap_cars, best_pair, wri_search, wri_values, corr_filter, relieff, vif_filter
import split_lib as SL
from split_cfg import LABEL, TEST_FRAC
from sklearn.model_selection import GroupKFold, KFold, GridSearchCV, train_test_split
from sklearn.svm import SVC
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import roc_auc_score, cohen_kappa_score
import xgboost as xgb
B = os.path.dirname(os.path.abspath(__file__)) + '/'; D = B + 'data/'; L = B + '../asd26/data/'; OUTD = D + 'repeat/'; os.makedirs(OUTD, exist_ok=True)
P = np.load(L + 'prep.npz'); wl, w5, R1, R5, FD5 = P['wl'], P['w5'], P['R1'], P['R5'], P['FD5']
M = pd.read_csv(L + 'meta.csv'); F0 = pd.read_csv(L + 'indices.csv')          # LORO meta: column fold = LORO fold
BANDS = pd.DataFrame(np.hstack([R5, FD5]), columns=['R%d' % w for w in w5] + ['FD%d' % w for w in w5])
g = lambda lam: R1[:, int(round(lam - 400))]
GR = [0, 1, 3, 5, 7, 9]; enc = {v: i for i, v in enumerate(GR)}; plots = M['plot'].values
Y = {'A': M.diseased.values, 'B': M.grade.map(enc).values, 'C': M.grade.values.astype(float)}
MAIN = json.load(open(D + 'split.json'))['test_plots']

def jobs():
    J = [('LORO', f, None) for f in range(3)] + [('main ' + LABEL, 0, MAIN)]
    J += [('grouped ' + LABEL, r, sp) for r, sp in enumerate(SL.random_splits(M, TEST_FRAC, 20, seed=7))]
    J += [('leaf ' + LABEL, s, None) for s in range(5)]
    return J

def select(tr, seed):
    y = M.grade.values.astype(float); Nm, Sm = r2_maps(R5[tr], y[tr]); used, thr = effective_ranges(Nm, Sm, w5)
    re = (w5 >= 680) & (w5 <= 760); cR = np.where(used)[0]; cF = np.where(used | re)[0]
    Xc = np.hstack([R5[tr][:, cR], FD5[tr][:, cF]]); names = ['R%d' % w5[i] for i in cR] + ['FD%d' % w5[i] for i in cF]
    sc = shap_cars(Xc, y[tr], names, runs=10, n_iter=50, seed=seed)
    a, b, _ = best_pair(Nm, w5); c, d, _ = best_pair(Sm, w5); wr = wri_search(R5[tr], w5, y[tr], Nm)[0]
    F = F0.copy(); F['NDSI_best'] = (g(a) - g(b)) / (g(a) + g(b)); F['RSI_best'] = g(c) / g(d); F['WRI'] = wri_values(R1, wl, wr[2], wr[3], wr[4], wr[5])
    kept = corr_filter(F[tr].reset_index(drop=True), y[tr], 0.95); grp = plots[tr]
    W = {'A': relieff(F[kept].values[tr], M.diseased.values[tr], grp), 'B': relieff(F[kept].values[tr], M.grade.values[tr], grp), 'C': relieff(F[kept].values[tr], y[tr], grp, regression=True)}
    VI = {t: [kept[i] for i in np.argsort(-W[t])[:5]] for t in 'ABC'}; ALL = pd.concat([BANDS, F], axis=1)
    DSF = {t: vif_filter(pd.concat([BANDS[sc['names']], F[VI[t]]], axis=1)[tr], 10.0)[0] for t in 'ABC'}
    return ALL, dict(OW=sc['names'], VI=VI, DSF=DSF, ndsi=[int(a), int(b)], rsi=[int(c), int(d)])

def fit_eval(ALL, sel, tr, te, cv):
    out = {}
    for t in 'ABC':
        cols = sel['DSF'][t]; X = ALL[cols].values; mu, sd = X[tr].mean(0), X[tr].std(0) + 1e-12; Xs = (X - mu) / sd; y = Y[t]
        if t == 'A': gs = GridSearchCV(SVC(class_weight='balanced'), {'C': [0.1, 1, 10, 100], 'gamma': [0.001, 0.01, 0.1, 'scale']}, scoring='f1_macro', cv=cv)
        elif t == 'B': gs = GridSearchCV(RandomForestClassifier(500, class_weight='balanced', random_state=42, n_jobs=1), {'max_features': ['sqrt', 0.3], 'min_samples_leaf': [1, 3, 5]}, scoring='f1_macro', cv=cv)
        else: gs = GridSearchCV(xgb.XGBRegressor(subsample=0.8, n_jobs=1, random_state=42, verbosity=0), {'n_estimators': [200, 500], 'max_depth': [3, 5], 'learning_rate': [0.05, 0.1]}, scoring='neg_root_mean_squared_error', cv=cv)
        gs.fit(Xs[tr], y[tr]); m = gs.best_estimator_; yp = m.predict(Xs[te])
        out[t] = dict(leaf=np.where(te)[0].tolist(), y=y[te].tolist(), pred=np.asarray(yp, float).tolist(), score=(m.decision_function(Xs[te]).tolist() if t == 'A' else None),
                      params={k: str(v) for k, v in gs.best_params_.items()}, n_features=len(cols))
    return out

def run(job):
    scheme, k, sp = job; t0 = time.time()
    if scheme == 'LORO': te = (M.fold == k).values
    elif scheme.startswith('leaf'):
        te = np.zeros(len(M), bool); _, ite = train_test_split(np.arange(len(M)), test_size=TEST_FRAC, stratify=M.grade.values, random_state=100 + k); te[ite] = True
    else: te = M['plot'].isin(sp).values
    tr = ~te
    cv = list(KFold(3, shuffle=True, random_state=0).split(np.zeros(tr.sum()))) if scheme.startswith('leaf') else list(GroupKFold(3).split(np.zeros(tr.sum()), groups=plots[tr]))
    ALL, sel = select(tr, seed=42 + k); res = fit_eval(ALL, sel, tr, te, cv)
    return dict(scheme=scheme, k=k, test_plots=sp, n_train=int(tr.sum()), n_test=int(te.sum()), selection=sel, results=res, seconds=time.time() - t0)

def macro_f1(y, p, K):
    cm = np.bincount(np.asarray(y, int) * K + np.asarray(p, int), minlength=K * K).reshape(K, K); tp = np.diag(cm); den = cm.sum(0) + cm.sum(1)
    return float(np.mean(np.where(tp > 0, 2 * tp / np.maximum(den, 1), 0.0)))
def metrics(t, y, p, s=None):
    y = np.asarray(y); p = np.asarray(p)
    if t == 'A': return dict(macro_F1=macro_f1(y, p, 2), OA=float((y == p).mean()), AUC=float(roc_auc_score(y, s)) if s is not None else np.nan)
    if t == 'B': return dict(macro_F1=macro_f1(y, p, 6), OA=float((y == p).mean()), QWK=float(cohen_kappa_score(y.astype(int), p.astype(int), weights='quadratic')))
    p = np.clip(p, 0, 9); rmse = float(np.sqrt(np.mean((y - p) ** 2))); return dict(R2=float(1 - np.sum((y - p) ** 2) / np.sum((y - y.mean()) ** 2)), RMSE=rmse)

if __name__ == '__main__':
    J = jobs()
    if sys.argv[1] == 'worker':
        i, n = int(sys.argv[2]), int(sys.argv[3])
        for j, job in enumerate(J):
            if j % n != i: continue
            fn = OUTD + 'job%02d.json' % j
            if os.path.exists(fn): continue
            r = run(job); json.dump(r, open(fn, 'w')); print(j, job[0], job[1], '%.0fs' % r['seconds'], {t: round(metrics(t, r['results'][t]['y'], r['results'][t]['pred'], r['results'][t]['score'])['macro_F1' if t != 'C' else 'R2'], 3) for t in 'ABC'}, flush=True)
        print('WORKER DONE', flush=True)
    if sys.argv[1] == 'merge':
        R = [json.load(open(OUTD + 'job%02d.json' % j)) for j in range(len(J)) if os.path.exists(OUTD + 'job%02d.json' % j)]
        rows = []
        loro = [r for r in R if r['scheme'] == 'LORO']
        if len(loro) == 3:   # pooled over the three folds, as in the LORO analysis
            for t in 'ABC':
                y = sum([r['results'][t]['y'] for r in loro], []); p = sum([r['results'][t]['pred'] for r in loro], []); s = sum([r['results'][t]['score'] for r in loro], []) if t == 'A' else None
                rows.append(dict(scheme='LORO', run=0, task=t, n_test=len(y), **metrics(t, y, p, s)))
        for r in R:
            if r['scheme'] == 'LORO': continue
            for t in 'ABC': rows.append(dict(scheme=r['scheme'], run=r['k'], task=t, n_test=r['n_test'], **metrics(t, r['results'][t]['y'], r['results'][t]['pred'], r['results'][t]['score'])))
        df = pd.DataFrame(rows); df.to_csv(D + 'cmp_repeat_runs.csv', index=False)
        sel = [dict(scheme=r['scheme'], run=r['k'], OW=', '.join(r['selection']['OW']), DSF_A=', '.join(r['selection']['DSF']['A']), DSF_B=', '.join(r['selection']['DSF']['B']),
                    DSF_C=', '.join(r['selection']['DSF']['C']), test_plots=', '.join(str(p) for p in (r['test_plots'] or [])), n_train=r['n_train'], n_test=r['n_test']) for r in R]
        pd.DataFrame(sel).to_csv(D + 'cmp_repeat_selection.csv', index=False)
        print(df.groupby(['scheme', 'task']).agg(['mean', 'std', 'min', 'max']).round(3).to_string()); print('merged', len(R), 'of', len(J))
