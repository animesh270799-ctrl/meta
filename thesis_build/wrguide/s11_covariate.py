"""STEP 11 (G1-G3): covariate baseline on the UNSPRAYED leaves of the same split: M0 covariates only, M1 spectra (DSF), M2 spectra + covariates;
gains with 2000 paired bootstrap resamples of the unsprayed test plots; DeLong test for the detection AUCs; interpretable model effects."""
import os, json, warnings, numpy as np, pandas as pd
warnings.filterwarnings('ignore')
import statsmodels.api as sm
from statsmodels.miscmodels.ordinal_model import OrderedModel
from sklearn.linear_model import LogisticRegression, LinearRegression
from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor
from sklearn.svm import SVC
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import make_pipeline
from sklearn.model_selection import GroupKFold, GridSearchCV
from sklearn.utils.class_weight import compute_sample_weight
import xgboost as xgb
import config as C
from lib_metrics import metric_value, delong, plot_boot_idx
O = C.OUT; M = pd.read_csv(os.path.join(O, '03_meta_split.csv')); T = pd.read_csv(os.path.join(O, '06_model_features.csv')); SEL = json.load(open(os.path.join(O, '06_selection_train.json')))
Wd = pd.read_csv(os.path.join(C.RAW_DIR, C.WEATHER_FILE), parse_dates=['date'])
fav_leaf = lambda d: int(((d.Tmax >= 16) & (d.Tmax <= 24) & (d.RH1 > 97) & (d.RH2 > 40)).sum()); fav_stag = lambda d: int(((d.Tmax >= 20) & (d.Tmax <= 29) & (d.Tmin > 12) & (d.RH1 > 97)).sum())
wx = {}
for dt in M.date.unique():
    t = pd.Timestamp(dt); w7 = Wd[(Wd.date < t) & (Wd.date >= t - pd.Timedelta(days=7))]                     # 7 days ending the day before sampling
    for tm, sow in C.SOWING.items():
        since = Wd[(Wd.date >= pd.Timestamp(sow)) & (Wd.date < t)]
        wx[(dt, tm)] = dict(Tmax7=w7.Tmax.mean(), Tmin7=w7.Tmin.mean(), RH1_7=w7.RH1.mean(), RH2_7=w7.RH2.mean(), rain7=w7.rain.sum(), fav_leaf=fav_leaf(since), fav_staghead=fav_stag(since))
WX = pd.DataFrame([wx[(d, t)] for d, t in zip(M.date, M.timing)])
COV2 = pd.concat([pd.get_dummies(M[['variety', 'timing']].astype(str)).astype(float), M[['DAS', 'stage_code']].astype(float), WX], axis=1)
dc = M.DAS - M.DAS.mean(); COV1 = pd.concat([pd.get_dummies(M[['variety', 'timing']].astype(str), drop_first=True).astype(float), M[['stage_code']].astype(float)], axis=1); COV1['DAS'] = dc; COV1['DAS2'] = dc ** 2
uns = (M.unsprayed == 1).values; tr = (M.fold == 1).values & uns; te = (M.fold == 0).values & uns; plots = M['plot'].values
Y = {'A': M.diseased.values, 'B': M.grade.map({g: i for i, g in enumerate(C.GRADES)}).values, 'C': M.grade.values.astype(float)}
cv = list(GroupKFold(C.INNER_FOLDS).split(np.zeros(tr.sum()), groups=plots[tr]))
def fit_predict(task, model, X):
    Xtr, Xte, ytr = X[tr], X[te], Y[task][tr]
    if model == 'B1':
        if task == 'A':
            g = GridSearchCV(make_pipeline(StandardScaler(), LogisticRegression(max_iter=5000, class_weight='balanced')), {'logisticregression__C': [0.01, 0.1, 1, 10, 100]}, scoring='f1_macro', cv=cv).fit(Xtr, ytr); return g.predict(Xte), g.predict_proba(Xte)[:, 1]
        ss = StandardScaler().fit(Xtr); keep = ss.scale_ > 1e-9
        if task == 'B':
            om = OrderedModel(ytr, ss.transform(Xtr)[:, keep], distr='logit').fit(method='bfgs', maxiter=2000, disp=False); return np.asarray(om.model.predict(om.params, exog=ss.transform(Xte)[:, keep])).argmax(1), None
        return np.clip(LinearRegression().fit(ss.transform(Xtr), ytr).predict(ss.transform(Xte)), 0, 9), None
    if model == 'RF' or (model == 'B2' and task == 'C'):
        grid = {'max_features': ['sqrt', 0.3], 'min_samples_leaf': [1, 3, 5]}
        if task == 'C': return GridSearchCV(RandomForestRegressor(500, random_state=C.SEED, n_jobs=4), grid, scoring='neg_root_mean_squared_error', cv=cv).fit(Xtr, ytr).predict(Xte), None
        g = GridSearchCV(RandomForestClassifier(500, class_weight='balanced', random_state=C.SEED, n_jobs=4), grid, scoring='f1_macro', cv=cv).fit(Xtr, ytr); return g.predict(Xte), (g.predict_proba(Xte)[:, 1] if task == 'A' else None)
    if task == 'A':
        g = GridSearchCV(make_pipeline(StandardScaler(), SVC(class_weight='balanced')), {'svc__C': [0.1, 1, 10, 100], 'svc__gamma': [0.001, 0.01, 0.1, 'scale']}, scoring='f1_macro', cv=cv).fit(Xtr, ytr); return g.predict(Xte), g.decision_function(Xte)
    g = GridSearchCV(xgb.XGBClassifier(subsample=0.8, n_jobs=4, random_state=C.SEED, verbosity=0), {'n_estimators': [200, 500], 'max_depth': [3, 5], 'learning_rate': [0.05, 0.1]}, scoring='f1_macro', cv=cv).fit(Xtr, ytr)
    return g.best_estimator_.fit(Xtr, ytr, sample_weight=compute_sample_weight('balanced', ytr)).predict(Xte), None
MAIN = {'A': 'macro_F1', 'B': 'macro_F1', 'C': 'R2'}; res, preds = [], {}
for task in 'ABC':
    spec = T[SEL['DSF'][task]].values
    for inp, X in (('covariates', None), ('spectra', spec), ('spectra+covariates', None)):
        for model in ('B1', 'RF', 'B2'):
            Xm = (COV1 if model == 'B1' else COV2).values if inp == 'covariates' else (spec if inp == 'spectra' else np.hstack([spec, (COV1 if model == 'B1' else COV2).values]))
            p, s = fit_predict(task, model, Xm); preds[(task, inp, model)] = (p, s)
            res.append(dict(task=task, input=inp, model=model, value=metric_value(task, MAIN[task], Y[task][te], p, s)))
R = pd.DataFrame(res); R.to_csv(os.path.join(O, '11_covariate_models.csv'), index=False); gains = []; dl = []
for task in 'ABC':
    d = R[(R.task == task) & (R.input == 'covariates')]; m0 = d.sort_values('value').model.iloc[-1]                  # M0 = the stronger covariate-only model
    sets = {'M0': preds[(task, 'covariates', m0)], 'M1': preds[(task, 'spectra', 'B2')], 'M2': preds[(task, 'spectra+covariates', 'B2')]}; y = Y[task][te]; pl = plots[te]
    val = {k: metric_value(task, MAIN[task], y, *v) for k, v in sets.items()}; boots = {k: [] for k in sets}
    for ii in plot_boot_idx(pl, C.N_BOOT_GAIN, C.SEED):
        for k, (p, s) in sets.items(): boots[k].append(metric_value(task, MAIN[task], y[ii], p[ii], None if s is None else s[ii]))
    for g, a, b in (('dS = M1 - M0', 'M1', 'M0'), ('dC = M2 - M1', 'M2', 'M1'), ('dT = M2 - M0', 'M2', 'M0')):
        bd = np.array(boots[a]) - np.array(boots[b]); lo, hi = np.percentile(bd, [2.5, 97.5])
        gains.append(dict(task=task, metric=MAIN[task], M0_model=m0, gain=g, delta=val[a] - val[b], CI_low=lo, CI_high=hi, real=bool(lo > 0 or hi < 0)))
    if task == 'A' and all(v[1] is not None for v in sets.values()):
        for a, b in (('M1', 'M0'), ('M2', 'M0'), ('M2', 'M1')): dl.append(dict(zip(('AUC_a', 'AUC_b', 'z', 'p'), delong(y, sets[a][1], sets[b][1])), pair='%s vs %s' % (a, b)))
pd.DataFrame(gains).to_csv(os.path.join(O, '11_gains.csv'), index=False); pd.DataFrame(dl).to_csv(os.path.join(O, '11_delong.csv'), index=False)
Xs = (COV1[uns] - COV1[uns].mean()) / COV1[uns].std(); Xs = Xs.loc[:, COV1[uns].std() > 0]
om = OrderedModel(Y['B'][uns], Xs.values, distr='logit').fit(method='bfgs', maxiter=2000, disp=False); ci = om.conf_int()
pd.DataFrame([dict(term=k, estimate=om.params[j], ci_low=ci[j, 0], ci_high=ci[j, 1], p=om.pvalues[j]) for j, k in enumerate(Xs.columns)]).to_csv(os.path.join(O, '11_ordinal_effects.csv'), index=False)
print('CHECK: unsprayed leaves TRAIN %d / TEST %d; 11_covariate_models.csv, 11_gains.csv, 11_delong.csv, 11_ordinal_effects.csv written' % (tr.sum(), te.sum()))
