"""STEP L8: leaf covariate baseline (as Step 2.9 with leaf data). M0 = random forest on the covariates only (DAS, variety, sowing date, growth stage,
leaf position, 7-day weather ending the day before sampling, favourable days since sowing), tuned with GroupKFold(3) by plot (grid of Step 2.4);
M1 = best leaf model of the task (L7), unchanged; M2 = the M1 model type on DSF + covariates (SFFS and grid search repeated for ML; network retrained).
Gains dS = M1 - M0 and dC = M2 - M1 on the 684 test leaves (main metric), per task and for Task A per date; plot-bootstrap 95% CI as a check."""
import os, sys, json, warnings, numpy as np, pandas as pd
warnings.filterwarnings('ignore')
from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor
from sklearn.model_selection import GridSearchCV
from mlxtend.feature_selection import SequentialFeatureSelector as SFS
import configL as C
O = C.OUT; M = pd.read_csv(os.path.join(O, 'L2_meta.csv')); ALL = pd.read_csv(os.path.join(O, 'L5_all_features.csv')); SEL = json.load(open(os.path.join(O, 'L5_selection.json')))
B = json.load(open(os.path.join(O, 'L7_best.json')))['best']; P6 = pd.concat([pd.read_csv(os.path.join(O, f)) for f in os.listdir(O) if f.startswith('L6_') and 'predictions' in f], ignore_index=True)
Wd = pd.read_csv(C.WEATHER, parse_dates=['date'])
fav_leaf = lambda d: int(((d.Tmax >= 16) & (d.Tmax <= 24) & (d.RH1 > 97) & (d.RH2 > 40)).sum()); fav_stag = lambda d: int(((d.Tmax >= 20) & (d.Tmax <= 29) & (d.Tmin > 12) & (d.RH1 > 97)).sum())
wx = {}
for dt in M.date.unique():
    t = pd.Timestamp(dt); w7 = Wd[(Wd.date < t) & (Wd.date >= t - pd.Timedelta(days=7))]
    for tm, sow in C.SOWING.items():
        since = Wd[(Wd.date >= pd.Timestamp(sow)) & (Wd.date < t)]
        wx[(dt, tm)] = dict(Tmax7=w7.Tmax.mean(), Tmin7=w7.Tmin.mean(), RH1_7=w7.RH1.mean(), RH2_7=w7.RH2.mean(), rain7=w7.rain.sum(), fav_leaf=fav_leaf(since), fav_staghead=fav_stag(since))
WX = pd.DataFrame([wx[(d, t)] for d, t in zip(M.date, M.timing)])
COV = pd.concat([pd.get_dummies(M[['variety', 'timing', 'leaf']].astype(str), prefix=['var', 'sow', 'leaf']).astype(float), M[['DAS', 'stage_code']].astype(float), WX], axis=1)
COV.assign(date=M.date, plot=M['plot']).to_csv(os.path.join(O, 'L8_covariates.csv'), index=False)
WXd = pd.DataFrame([dict(date=d, sowing=t, **v) for (d, t), v in wx.items()]).sort_values(['date', 'sowing']); WXd.to_csv(os.path.join(O, 'L8_weather_windows.csv'), index=False)
tr = (M.split == 'TRAIN').values; te = ~tr; folds = M.inner_fold.values[tr]; SPL = [(np.where(folds != k)[0], np.where(folds == k)[0]) for k in (1, 2, 3)]
Y = {'A': M.diseased.values.astype(int), 'B': M.grade.map({g: i for i, g in enumerate(C.GRADES)}).values.astype(int), 'C': M.grade.values.astype(float)}
MAIN = {'A': 'macro_F1', 'B': 'macro_F1', 'C': 'R2'}; SC = {'A': 'f1_macro', 'B': 'f1_macro', 'C': 'neg_root_mean_squared_error'}
import lmods as L6
def mval(task, y, p, s=None): return L6.metrics(task, y, p, s)[0][MAIN[task]]
res, gains, preds, imps = [], [], [], []
for task in 'ABC':
    grid = {'max_features': ['sqrt', 0.3], 'min_samples_leaf': [1, 3, 5]}
    rf = RandomForestClassifier(500, class_weight='balanced', random_state=C.SEED, n_jobs=4) if task != 'C' else RandomForestRegressor(500, random_state=C.SEED, n_jobs=4)
    g0 = GridSearchCV(rf, grid, scoring=SC[task], cv=SPL).fit(COV.values[tr], Y[task][tr]); p0 = g0.predict(COV.values[te]); s0 = g0.predict_proba(COV.values[te])[:, 1] if task == 'A' else None
    if task == 'C': p0 = np.clip(p0, 0, 9)
    imp = pd.Series(g0.best_estimator_.feature_importances_, COV.columns).sort_values(ascending=False)
    imps += [dict(task=task, covariate=k, importance=float(x)) for k, x in imp.items()]
    m1 = B[task]; d1 = P6[(P6.task == task) & (P6.model == m1)].sort_values('leaf'); p1, s1 = d1.pred.values, (d1.score.values if task == 'A' else None)
    cols = SEL['DSF'][task]; X2 = np.hstack([ALL[cols].values, COV.values]); names2 = cols + list(COV.columns)
    if d1.family.iloc[0] == 'ML':
        sfs = SFS(L6.base(m1, task), k_features=(1, min(C.SFFS_MAX, X2.shape[1])), forward=True, floating=True, scoring=SC[task], cv=SPL, n_jobs=(1 if m1 == 'RF' else 4)).fit(X2[tr], Y[task][tr])
        ci = list(sfs.k_feature_idx_); g2 = GridSearchCV(L6.base(m1, task), L6.grid(m1, task, len(ci)), scoring=SC[task], cv=SPL, n_jobs=(1 if m1 == 'RF' else 4)).fit(X2[tr][:, ci], Y[task][tr])
        p2 = g2.predict(X2[te][:, ci]); s2 = L6.score_of(g2.best_estimator_, X2[te][:, ci], task); chosen2 = [names2[i] for i in ci]
        if task == 'C': p2 = np.clip(p2, 0, 9)
    else:
        import l08_nets as L6N
        p2, s2, _, _, _ = L6N.run(m1, task, Xin=X2, cols=names2, save=False); chosen2 = names2
    yt = Y[task][te]; v = {'M0': mval(task, yt, p0, s0), 'M1': mval(task, yt, p1, s1), 'M2': mval(task, yt, p2, s2)}
    res.append(dict(task=task, metric=MAIN[task], M0_model='RF (covariates)', M0_params=json.dumps(g0.best_params_), M1_model=m1, M2_features=' '.join(chosen2), **v,
                    dS=v['M1'] - v['M0'], dC=v['M2'] - v['M1'], top_covariates=', '.join('%s %.2f' % (k, x) for k, x in imp.head(5).items())))
    for i, leaf in enumerate(np.where(te)[0]):
        preds.append(dict(task=task, leaf=int(leaf), y=float(yt[i]), M0=float(p0[i]), M1=float(p1[i]), M2=float(p2[i]), sM0=(None if s0 is None else float(s0[i])), sM1=(None if s1 is None else float(s1[i])), sM2=(None if s2 is None else float(s2[i]))))
    pl = M['plot'].values[te]; rng = np.random.default_rng(C.SEED); tp = np.unique(pl); hp, up = tp[tp <= 12], tp[tp > 12]; ix = {q: np.where(pl == q)[0] for q in tp}; bs = {'dS': [], 'dC': []}
    for _ in range(1000):
        ii = np.concatenate([ix[q] for q in np.concatenate([rng.choice(hp, len(hp)), rng.choice(up, len(up))])])
        try:
            a0, a1, a2 = (mval(task, yt[ii], p[ii], None if s is None else s[ii]) for p, s in ((p0, s0), (p1, s1), (p2, s2))); bs['dS'].append(a1 - a0); bs['dC'].append(a2 - a1)
        except ValueError: pass
    for gname in ('dS', 'dC'):
        lo, hi = np.percentile(bs[gname], [2.5, 97.5]); gains.append(dict(task=task, scope='all test leaves', gain=gname, value=res[-1][gname], CI_low=lo, CI_high=hi))
    if task == 'A':
        for dt in sorted(M.date[te].unique()):
            k = (M.date.values[te] == dt); vv = {n: mval(task, yt[k], p[k], None if s is None else s[k]) for n, (p, s) in (('M0', (p0, s0)), ('M1', (p1, s1)), ('M2', (p2, s2)))}
            gains.append(dict(task=task, scope='date ' + dt, gain='dS', value=vv['M1'] - vv['M0'], M0=vv['M0'], M1=vv['M1'], M2=vv['M2'])); gains.append(dict(task=task, scope='date ' + dt, gain='dC', value=vv['M2'] - vv['M1'], M0=vv['M0'], M1=vv['M1'], M2=vv['M2']))
    print(task, {k: round(x, 3) for k, x in v.items()}, 'M1 =', m1, '| top covariates', imp.head(4).round(2).to_dict(), flush=True)
pd.DataFrame(res).to_csv(os.path.join(O, 'L8_models.csv'), index=False); pd.DataFrame(gains).to_csv(os.path.join(O, 'L8_gains.csv'), index=False); pd.DataFrame(preds).to_csv(os.path.join(O, 'L8_predictions.csv'), index=False); pd.DataFrame(imps).to_csv(os.path.join(O, 'L8_importance.csv'), index=False)
print(pd.DataFrame(gains).round(3).to_string(index=False))
