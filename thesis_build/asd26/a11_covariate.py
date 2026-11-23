"""Step 2.5.5 for the 2025-26 ASD leaf data: covariate (sensor-free) baseline models.
Inoculated, unsprayed plots only (healthy plots are fungicide-protected); same leave-one-replication-out folds; no look-ahead
(weather windows end the day before each sampling date).
  B1 statistical: logistic regression (A), proportional-odds ordinal logistic regression (B), linear model with DAI and DAI² (C)
  RF: random forest (tuned in inner folds grouped by plot)
  B2: best machine-learning model of Activity 2.2 for each task (A SVM, B XGBoost, C RF), tuned in inner folds
Inputs: covariates only, leaf spectra (fold-wise DSF), spectra + covariates.
M0 = stronger covariate-only model; M1 = B2 on spectra; M2 = B2 on spectra + covariates.
Gains ΔS = M1 − M0, ΔC = M2 − M1, ΔT = M2 − M0 with plot-block bootstrap 95% CI (2000 resamples) and DeLong test for AUC."""
import numpy as np, pandas as pd, json, os, warnings, time
warnings.filterwarnings('ignore')
from scipy import stats
from sklearn.linear_model import LogisticRegression, LinearRegression
from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor
from sklearn.svm import SVC
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import make_pipeline
from sklearn.model_selection import GridSearchCV, GroupKFold
from sklearn.metrics import roc_auc_score, cohen_kappa_score
from sklearn.utils.class_weight import compute_sample_weight
import xgboost as xgb
import statsmodels.api as sm
from statsmodels.miscmodels.ordinal_model import OrderedModel
from a5_metrics import cls_metrics, reg_metrics
D = os.path.dirname(os.path.abspath(__file__)) + '/data/'
GR = [0, 1, 3, 5, 7, 9]; enc = {g: i for i, g in enumerate(GR)}
M = pd.read_csv(D + 'meta.csv'); SEL = json.load(open(D + 'fold_selection.json'))
P = np.load(D + 'prep.npz'); w5, R5, FD5 = P['w5'], P['R5'], P['FD5']
BANDS = pd.DataFrame(np.hstack([R5, FD5]), columns=['R%d' % w for w in w5] + ['FD%d' % w for w in w5])
# ---------------- covariates (no look-ahead: windows end the day before each date) ----------------
W = pd.read_csv(D + 'weather_season.csv', parse_dates=['date']); WC = pd.read_csv(D + 'weather_covariates.csv')
inoc_day = pd.Timestamp('2026-02-05'); stag = []
for d in WC.date:
    t = pd.Timestamp(d); since = W[(W.date >= inoc_day) & (W.date < t)]
    stag.append(int(((since.Tmax.between(20, 29)) & (since.Tmin > 12) & (since.RH1 > 97)).sum()))
WC['fav_staghead'] = stag; WC = WC.rename(columns={'fav_days': 'fav_leaf'})
WC[['date', 'Tmax7', 'Tmin7', 'RH1_7', 'RH2_7', 'rain7', 'fav_leaf', 'fav_staghead']].to_csv(D + 'cov2_covariates_by_date.csv', index=False)
wx = M[['date']].merge(WC[['date', 'Tmax7', 'Tmin7', 'RH1_7', 'RH2_7', 'rain7', 'fav_leaf', 'fav_staghead']], on='date', how='left').drop(columns='date')
COV2 = pd.concat([pd.get_dummies(M[['variety', 'timing']].astype(str)).astype(float), M[['DAI', 'stage_code']].astype(float), wx], axis=1)   # B2 / RF covariates
dai_c = M.DAI - M.DAI.mean()
COV1 = pd.concat([pd.get_dummies(M[['variety', 'timing']].astype(str), drop_first=True).astype(float), M[['stage_code']].astype(float)], axis=1)
COV1['DAI'] = dai_c; COV1['DAI2'] = dai_c ** 2                                       # B1 covariates (date effect via DAI, DAI²)
inoc = (M.inoculated == 1).values; plots = M['plot'].values
Y = {'A': M.diseased.values, 'B': M.grade.map(enc).values, 'C': M.grade.values.astype(float)}
BEST = {'A': 'SVM', 'B': 'XGBoost', 'C': 'RF'}
def inner(tr): return list(GroupKFold(3).split(np.zeros(tr.sum()), groups=plots[tr]))
def fit_predict(task, model, Xtr, ytr, Xte, cv):
    """returns predictions and a score (probability of disease for A, None otherwise)"""
    sc = None
    if model == 'Statistical':
        if task == 'A':
            g = GridSearchCV(make_pipeline(StandardScaler(), LogisticRegression(max_iter=5000, class_weight='balanced')), {'logisticregression__C': [0.01, 0.1, 1, 10, 100]}, scoring='f1_macro', cv=cv).fit(Xtr, ytr)
            return g.predict(Xte), g.predict_proba(Xte)[:, 1]
        if task == 'B':
            ss = StandardScaler().fit(Xtr); keep = ss.scale_ > 1e-9
            om = OrderedModel(ytr, ss.transform(Xtr)[:, keep], distr='logit').fit(method='bfgs', maxiter=2000, disp=False)
            pr = np.asarray(om.model.predict(om.params, exog=ss.transform(Xte)[:, keep])); return pr.argmax(1), None
        ss = StandardScaler().fit(Xtr); lr = LinearRegression().fit(ss.transform(Xtr), ytr); return np.clip(lr.predict(ss.transform(Xte)), 0, 9), None
    if model == 'RF' or (model == 'B2' and task == 'C'):
        grid = {'max_features': ['sqrt', 0.3], 'min_samples_leaf': [1, 3, 5]}
        if task in 'AB':
            g = GridSearchCV(RandomForestClassifier(500, class_weight='balanced', random_state=42, n_jobs=4), grid, scoring='f1_macro', cv=cv).fit(Xtr, ytr)
            return g.predict(Xte), (g.predict_proba(Xte)[:, 1] if task == 'A' else None)
        g = GridSearchCV(RandomForestRegressor(500, random_state=42, n_jobs=4), grid, scoring='neg_root_mean_squared_error', cv=cv).fit(Xtr, ytr); return g.predict(Xte), None
    if task == 'A':   # best ML: SVM
        g = GridSearchCV(make_pipeline(StandardScaler(), SVC(class_weight='balanced')), {'svc__C': [0.1, 1, 10, 100], 'svc__gamma': [0.001, 0.01, 0.1, 'scale']}, scoring='f1_macro', cv=cv).fit(Xtr, ytr)
        return g.predict(Xte), g.decision_function(Xte)
    g = GridSearchCV(xgb.XGBClassifier(subsample=0.8, n_jobs=4, random_state=42, verbosity=0), {'n_estimators': [200, 500], 'max_depth': [3, 5], 'learning_rate': [0.05, 0.1]}, scoring='f1_macro', cv=cv).fit(Xtr, ytr)
    m = xgb.XGBClassifier(subsample=0.8, n_jobs=4, random_state=42, verbosity=0, **g.best_params_).fit(Xtr, ytr, sample_weight=compute_sample_weight('balanced', ytr)); return m.predict(Xte), None

rows = []; t0 = time.time()
REUSE = os.environ.get('REUSE') == '1' and os.path.exists(D + 'cov2_predictions.csv')   # REUSE=1: skip refitting, use saved test predictions
for f in ([] if REUSE else range(3)):
    Ff = pd.read_csv(D + 'fold%d_indices.csv' % f); ALL = pd.concat([BANDS, Ff], axis=1)
    tr = (M.fold != f).values & inoc; te = (M.fold == f).values & inoc; cv = inner(tr)
    for task in 'ABC':
        dsf = ALL[SEL[str(f)]['DSF'][task]].values; y = Y[task]
        for inp in ('covariates only', 'leaf spectra', 'spectra + covariates'):
            for model in ('Statistical', 'RF', 'B2'):
                if task == 'C' and model == 'B2': continue          # best ML for the score is RF (computed above)
                cov = COV1.values if model == 'Statistical' else COV2.values
                X = {'covariates only': cov, 'leaf spectra': dsf, 'spectra + covariates': np.hstack([dsf, cov])}[inp]
                yp, sc = fit_predict(task, model, X[tr], y[tr], X[te], cv)
                for i, ii in enumerate(np.where(te)[0]):
                    rows.append(dict(task=task, input=inp, model=model, fold=f, leaf=int(ii), plot=int(plots[ii]), y=float(y[ii]), pred=float(yp[i]), score=None if sc is None else float(sc[i])))
        print('fold', f, 'task', task, 'done %.0fs' % (time.time() - t0), flush=True) if False else None
    print('fold', f, 'done %.0fs' % (time.time() - t0), flush=True)
if REUSE: PR = pd.read_csv(D + 'cov2_predictions.csv')
else:
    PR = pd.DataFrame(rows)
    # best ML for C is RF: duplicate under the B2 label for the comparison
    PR = pd.concat([PR, PR[(PR.task == 'C') & (PR.model == 'RF')].assign(model='B2')], ignore_index=True)
    PR.to_csv(D + 'cov2_predictions.csv', index=False)
# ---------------- metrics ----------------
NAME = {'Statistical': {'A': 'Logistic regression', 'B': 'Ordinal logistic regression', 'C': 'Linear regression (DAI, DAI²)'}, 'RF': {t: 'Random forest' for t in 'ABC'}, 'B2': {'A': 'SVM (best ML)', 'B': 'XGBoost (best ML)', 'C': 'Random forest (best ML)'}}
def metrics(task, d):
    if task in 'AB':
        m, _ = cls_metrics(d.y.values, d.pred.values, 2 if task == 'A' else 6, d.score.values if task == 'A' and d.score.notna().all() else None)
        keep = ['OA', 'balanced_acc', 'macro_F1', 'AUC', 'sensitivity', 'specificity', 'kappa'] if task == 'A' else ['OA', 'kappa', 'macro_F1', 'QWK', 'within1']
        return {k: m.get(k) for k in keep}
    m = reg_metrics(d.y.values, d.pred.values); return {k: m[k] for k in ('R2', 'RMSE', 'MAE', 'RPD', 'bias')}
MT = []
for (task, inp, model), d in PR.groupby(['task', 'input', 'model'], sort=False):
    r = dict(task=task, input=inp, model=model, model_name=NAME[model][task], n=len(d), **metrics(task, d))
    fm = [metrics(task, g)['macro_F1' if task in 'AB' else 'RMSE'] for _, g in d.groupby('fold')]; r['fold_sd'] = float(np.std(fm, ddof=1)); MT.append(r)
MT = pd.DataFrame(MT); MT.to_csv(D + 'cov2_metrics.csv', index=False); print(MT.round(3).to_string())
# ---------------- M0, M1, M2 and gains ----------------
PRIM = {'A': ['macro_F1', 'AUC', 'balanced_acc'], 'B': ['macro_F1', 'QWK'], 'C': ['R2', 'RMSE']}
def mfast(task, k, y, p, s):
    if k == 'macro_F1':
        K = 2 if task == 'A' else 6; f = []
        for c in range(K):
            tp = np.sum((p == c) & (y == c)); fp = np.sum((p == c) & (y != c)); fn = np.sum((p != c) & (y == c)); f.append(0 if tp == 0 else 2 * tp / (2 * tp + fp + fn))
        return np.mean(f)
    if k == 'AUC': return roc_auc_score(y, s)
    if k == 'balanced_acc': return 0.5 * (np.mean(p[y == 1] == 1) + np.mean(p[y == 0] == 0))
    if k == 'QWK': return cohen_kappa_score(y, p, weights='quadratic')
    if k == 'R2': return 1 - np.sum((y - p) ** 2) / np.sum((y - y.mean()) ** 2)
    if k == 'RMSE': return np.sqrt(np.mean((y - p) ** 2))
def delong(y, s1, s2):
    """DeLong test for two correlated AUCs (fast algorithm of Sun and Xu, 2014)"""
    pos, neg = s1[y == 1], s1[y == 0]; pos2, neg2 = s2[y == 1], s2[y == 0]; m, n = len(pos), len(neg)
    def comp(p, q):
        allv = np.concatenate([p, q]); r = stats.rankdata(allv); rp = stats.rankdata(p); rq = stats.rankdata(q)
        auc = (r[:m].sum() - m * (m + 1) / 2) / (m * n); v10 = (r[:m] - rp) / n; v01 = 1 - (r[m:] - rq) / m; return auc, v10, v01
    a1, v10a, v01a = comp(pos, neg); a2, v10b, v01b = comp(pos2, neg2)
    s10 = np.cov(np.vstack([v10a, v10b])); s01 = np.cov(np.vstack([v01a, v01b])); S = s10 / m + s01 / n
    var = S[0, 0] + S[1, 1] - 2 * S[0, 1]; z = (a1 - a2) / np.sqrt(var); return a1, a2, z, 2 * stats.norm.sf(abs(z))
rng = np.random.default_rng(42); NB = 2000; gains = []; summary = {}; dl = []
for task in 'ABC':
    covm = MT[(MT.task == task) & (MT.input == 'covariates only')]
    m0 = covm.sort_values('RMSE').iloc[0] if task == 'C' else covm.sort_values('macro_F1', ascending=False).iloc[0]
    sets = {'M0': (m0.input, m0.model), 'M1': ('leaf spectra', 'B2'), 'M2': ('spectra + covariates', 'B2')}
    summary[task] = {k: dict(input=v[0], model=v[1], model_name=NAME[v[1]][task]) for k, v in sets.items()}
    dd = {k: PR[(PR.task == task) & (PR.input == v[0]) & (PR.model == v[1])].sort_values('leaf').reset_index(drop=True) for k, v in sets.items()}
    y = dd['M0']['y'].values; pl = dd['M0']['plot'].values; fo = dd['M0']['fold'].values; up = np.unique(pl); idx_by = {p_: np.where(pl == p_)[0] for p_ in up}
    arrs = {k: (d.pred.values, d.score.values.astype(float) if d.score.notna().all() else None) for k, d in dd.items()}
    for kname in PRIM[task]:
        if kname == 'AUC' and any(arrs[k][1] is None for k in arrs): continue
        val = {k: mfast(task, kname, y, arrs[k][0], arrs[k][1]) for k in arrs}
        boots = {k: [] for k in arrs}
        for b in range(NB):
            ii = np.concatenate([idx_by[p_] for p_ in rng.choice(up, len(up), replace=True)])
            for k in arrs: boots[k].append(mfast(task, kname, y[ii], arrs[k][0][ii], None if arrs[k][1] is None else arrs[k][1][ii]))
        boots = {k: np.array(v) for k, v in boots.items()}
        perfold = {k: [mfast(task, kname, y[fo == f], arrs[k][0][fo == f], None if arrs[k][1] is None else arrs[k][1][fo == f]) for f in range(3)] for k in arrs}
        for gname, a, b_ in (('ΔS = M1 − M0', 'M1', 'M0'), ('ΔC = M2 − M1', 'M2', 'M1'), ('ΔT = M2 − M0', 'M2', 'M0')):
            delta = val[a] - val[b_]; bd = boots[a] - boots[b_]; lo, hi = np.percentile(bd, [2.5, 97.5]); pf = np.array(perfold[a]) - np.array(perfold[b_])
            fsd = max(np.std(perfold[a], ddof=1), np.std(perfold[b_], ddof=1)); better = delta < 0 if kname == 'RMSE' else delta > 0
            excl = (hi < 0 or lo > 0); same = bool(np.all(np.sign(pf) == np.sign(delta)))
            gains.append(dict(task=task, metric=kname, gain=gname, value_a=val[a], value_b=val[b_], delta=delta, ci_low=lo, ci_high=hi, fold_d1=pf[0], fold_d2=pf[1], fold_d3=pf[2],
                              fold_sd=fsd, ci_excludes_0=excl, same_sign_all_folds=same, exceeds_fold_sd=abs(delta) > fsd, real_gain=bool(excl and same and abs(delta) > fsd), direction='improves' if better else 'worsens'))
    if task == 'A':
        for a, b_ in (('M1', 'M0'), ('M2', 'M0'), ('M2', 'M1')):
            a1, a2, z, p = delong(y, arrs[a][1], arrs[b_][1]); dl.append(dict(comparison='%s vs %s' % (a, b_), AUC_a=a1, AUC_b=a2, z=z, p=p))
G = pd.DataFrame(gains); G.to_csv(D + 'cov2_gains.csv', index=False); print(G.round(3).to_string())
pd.DataFrame(dl).to_csv(D + 'cov2_delong.csv', index=False); print(pd.DataFrame(dl).round(4).to_string())
json.dump(summary, open(D + 'cov2_summary.json', 'w'), indent=1); print(summary)
# ---------------- B1 interpretable fit on all inoculated leaves (standardised covariates) ----------------
Xs = (COV1[inoc] - COV1[inoc].mean()) / COV1[inoc].std(); Xs = Xs.loc[:, COV1[inoc].std() > 0]; coef = []
try:
    lg = sm.Logit(Y['A'][inoc], sm.add_constant(Xs)).fit(disp=False, maxiter=500)
    for k in Xs.columns: coef.append(dict(model='Logistic (detection)', term=k, estimate=lg.params[k], ci_low=lg.conf_int().loc[k, 0], ci_high=lg.conf_int().loc[k, 1], p=lg.pvalues[k], odds_ratio=np.exp(lg.params[k])))
except Exception as e: print('logit failed', e)
try:
    om = OrderedModel(Y['B'][inoc], Xs.values, distr='logit').fit(method='bfgs', maxiter=2000, disp=False); ci = om.conf_int()
    for j, k in enumerate(Xs.columns): coef.append(dict(model='Ordinal logistic (six grades)', term=k, estimate=om.params[j], ci_low=ci[j, 0], ci_high=ci[j, 1], p=om.pvalues[j], odds_ratio=np.exp(om.params[j])))
except Exception as e: print('ordinal failed', e)
ol = sm.OLS(Y['C'][inoc], sm.add_constant(Xs)).fit(); ci = ol.conf_int()
for k in Xs.columns: coef.append(dict(model='Linear (score)', term=k, estimate=ol.params[k], ci_low=ci.loc[k, 0], ci_high=ci.loc[k, 1], p=ol.pvalues[k], odds_ratio=np.nan))
pd.DataFrame(coef).to_csv(D + 'cov2_b1_coef.csv', index=False); print(pd.DataFrame(coef).round(3).to_string())
print('covariate analysis done %.0fs' % (time.time() - t0))
