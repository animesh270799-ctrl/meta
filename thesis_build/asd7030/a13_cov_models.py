"""Covariate-baseline models (Step 2.5.5) fitted on the unsprayed (naturally infected) leaves of the TRAINING plots of the hold-out
split with the same tuning as in a11_covariate.py (inner GroupKFold(3) by plot), saved with joblib in outputs/ASD_2025-26_70-30_models/covariate/.
Per task: B1 statistical, random forest and best ML on covariates only (M0 candidates) and best ML on spectra + covariates (M2).
Expected accuracy = the hold-out test numbers in cov2_metrics.csv (stored in each file)."""
import numpy as np, pandas as pd, os, json, shutil, warnings, joblib, platform
warnings.filterwarnings('ignore')
import sklearn, xgboost as xgb, statsmodels
from sklearn.model_selection import GroupKFold, GridSearchCV
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression, LinearRegression
from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor
from sklearn.svm import SVC
from sklearn.utils.class_weight import compute_sample_weight
from statsmodels.miscmodels.ordinal_model import OrderedModel
import wr_covariates as wc
from wr_features import all_features
B = os.path.dirname(os.path.abspath(__file__)) + '/'; D = B + 'data/'; OUT = B + '../outputs/ASD_2025-26_70-30_models/'; CO = OUT + 'covariate/'; os.makedirs(CO, exist_ok=True)
M = pd.read_csv(D + 'meta.csv'); W = pd.read_csv(D + 'weather_season.csv'); SEL = json.load(open(OUT + 'feature_selection.json')); MT = pd.read_csv(D + 'cov2_metrics.csv')
inoc = ((M.unsprayed == 1) & (M.fold != 0)).values   # unsprayed leaves of the training plots only
plots = M['plot'].values; enc = {g: i for i, g in enumerate(wc.GRADES)}
DAS_MEAN = float(M.DAS.mean())
COV2, COV1 = wc.leaf_covariates(M, W, wc.SOWING_2025_26, DAS_MEAN)
# check against the covariates used in the evaluation
chk = pd.read_csv(D + 'cov2_covariates_by_date.csv'); cw = wc.window7(W, M.date)
assert np.allclose(cw[['Tmax7', 'Tmin7', 'RH1_7', 'RH2_7', 'rain7']].values, chk[['Tmax7', 'Tmin7', 'RH1_7', 'RH2_7', 'rain7']].values), 'weather covariates differ from the evaluation'
for t in wc.TIMINGS:
    for d, v in zip(chk.date, chk['fav_leaf_' + t]): assert COV2.fav_leaf[(M.date == d) & (M.timing == t)].eq(v).all(), 'favourable days differ'
ALL = all_features(np.load(D + 'X_leaf.npy').astype(float), np.load(D + 'wl.npy'), SEL)
Y = {'A': M.diseased.values, 'B': M.grade.map(enc).values, 'C': M.grade.values.astype(float)}
cv = list(GroupKFold(3).split(np.zeros(inoc.sum()), groups=plots[inoc]))
VERS = dict(python=platform.python_version(), sklearn=sklearn.__version__, xgboost=xgb.__version__, statsmodels=statsmodels.__version__)
TASKN = {'A': 'detection (0 = healthy, 1 = diseased)', 'B': 'six severity grades (0, 1, 3, 5, 7, 9)', 'C': 'severity score (0-9, regression)'}
rec = []
def fit(task, model, X, y):
    """same estimators and grids as a11_covariate.py; returns (fitted model, kind, params, extra)"""
    if model == 'Statistical':
        if task == 'A':
            g = GridSearchCV(make_pipeline(StandardScaler(), LogisticRegression(max_iter=5000, class_weight='balanced')), {'logisticregression__C': [0.01, 0.1, 1, 10, 100]}, scoring='f1_macro', cv=cv).fit(X, y)
            return g.best_estimator_, 'sklearn', g.best_params_, {}
        if task == 'B':
            mu, sd = X.mean(0), X.std(0); keep = sd > 1e-9; Xs = ((X - mu) / np.where(keep, sd, 1))[:, keep]
            om = OrderedModel(y, Xs, distr='logit').fit(method='bfgs', maxiter=2000, disp=False); om.remove_data()
            return om, 'ordinal', {}, dict(scaler_mean=mu, scaler_sd=np.where(keep, sd, 1), keep=keep)
        return make_pipeline(StandardScaler(), LinearRegression()).fit(X, y), 'sklearn', {}, {}
    if model == 'RF' or (model == 'B2' and task == 'C'):
        grid = {'max_features': ['sqrt', 0.3], 'min_samples_leaf': [1, 3, 5]}
        if task in 'AB': g = GridSearchCV(RandomForestClassifier(500, class_weight='balanced', random_state=42, n_jobs=4), grid, scoring='f1_macro', cv=cv).fit(X, y)
        else: g = GridSearchCV(RandomForestRegressor(500, random_state=42, n_jobs=4), grid, scoring='neg_root_mean_squared_error', cv=cv).fit(X, y)
        return g.best_estimator_, 'sklearn', g.best_params_, {}
    if task == 'A':
        g = GridSearchCV(make_pipeline(StandardScaler(), SVC(class_weight='balanced', probability=True, random_state=42)), {'svc__C': [0.1, 1, 10, 100], 'svc__gamma': [0.001, 0.01, 0.1, 'scale']}, scoring='f1_macro', cv=cv).fit(X, y)
        return g.best_estimator_, 'sklearn', g.best_params_, {}
    g = GridSearchCV(xgb.XGBClassifier(subsample=0.8, n_jobs=4, random_state=42, verbosity=0), {'n_estimators': [200, 500], 'max_depth': [3, 5], 'learning_rate': [0.05, 0.1]}, scoring='f1_macro', cv=cv).fit(X, y)
    m = xgb.XGBClassifier(subsample=0.8, n_jobs=4, random_state=42, verbosity=0, **g.best_params_).fit(X, y, sample_weight=compute_sample_weight('balanced', y))
    return m, 'sklearn', g.best_params_, {}
NAME = {'Statistical': {'A': 'Logistic regression', 'B': 'Ordinal logistic regression', 'C': 'Linear regression (DAS, DAS2)'}, 'RF': {t: 'Random forest' for t in 'ABC'}, 'B2': {'A': 'SVM', 'B': 'XGBoost', 'C': 'Random forest'}}
SUM = json.load(open(D + 'cov2_summary.json'))
for task in 'ABC':
    y = Y[task][inoc]
    for inp, model in (('covariates only', 'Statistical'), ('covariates only', 'RF'), ('covariates only', 'B2'), ('spectra + covariates', 'B2')):
        if task == 'C' and inp == 'covariates only' and model == 'B2': continue        # best ML for C is the random forest
        cset = 'COV1' if model == 'Statistical' else 'COV2'; cov = COV1 if cset == 'COV1' else COV2
        spec = SEL['DSF'][task] if inp == 'spectra + covariates' else []
        X = pd.concat([ALL[spec].reset_index(drop=True), cov.reset_index(drop=True)], axis=1).values[inoc] if spec else cov.values[inoc]
        est, kind, params, extra = fit(task, model, X, y)
        r = MT[(MT.task == task) & (MT.input == inp) & (MT.model == model)].iloc[0]
        perf = ('macro-F1 %.3f, AUC %.3f, balanced accuracy %.3f' % (r.macro_F1, r.AUC, r.balanced_acc)) if task == 'A' else (('macro-F1 %.3f, QWK %.3f' % (r.macro_F1, r.QWK)) if task == 'B' else 'R2 %.3f, RMSE %.2f' % (r.R2, r.RMSE))
        role = [k for k, v in SUM[task].items() if v['input'] == inp and v['model'] == model]
        name = NAME[model][task]
        fn = '%s_%s_%s.joblib' % (task, inp.replace(' + ', '_plus_').replace(' ', '_'), name.replace(' ', '_').replace('(', '').replace(')', '').replace(',', ''))
        bundle = dict(model=est, kind=kind, task=task, task_description=TASKN[task], model_name=name, input=inp, role=', '.join(role) if role else 'candidate',
                      covariate_set=cset, covariate_columns=list(cov.columns), spectral_columns=list(spec), uses_weather=cset == 'COV2', sowing=wc.SOWING_2025_26, das_mean=DAS_MEAN,
                      params={k: (v if isinstance(v, (int, float, str)) else str(v)) for k, v in params.items()}, training='unsprayed (naturally infected) leaves of the training plots of the grouped hold-out split, IARI 2025-26 (n = %d); tuning GroupKFold(3) by plot' % inoc.sum(),
                      test_performance=perf, grades=wc.GRADES, versions=VERS, **extra)
        joblib.dump(bundle, CO + fn, compress=3)
        # functional check on the training leaves (in-sample)
        P = wc.predict(bundle, M[inoc].reset_index(drop=True), W, ALL[inoc].reset_index(drop=True) if spec else None)
        col = P.columns[0]; obs = (Y[task][inoc] if task != 'B' else M.grade.values[inoc]); fit_in = float(np.mean(P[col].values == obs)) if task in 'AB' else float(np.corrcoef(P[col], obs)[0, 1] ** 2)
        rec.append(dict(file='covariate/' + fn, task=task, input=inp, model=name, role=bundle['role'], n_features=X.shape[1], features=', '.join(list(spec) + list(cov.columns)),
                        params=json.dumps(bundle['params']), test_performance=perf, in_sample_check=round(fit_in, 3)))
        print(fn, bundle['role'], perf, 'in-sample', round(fit_in, 3), flush=True)
pd.DataFrame(rec).to_csv(OUT + 'covariate_models_index.csv', index=False)
shutil.copy(B + 'wr_covariates.py', OUT + 'wr_covariates.py'); shutil.copy(D + 'weather_season.csv', CO + 'IARI_daily_weather_2025-26.csv')
print('covariate models saved:', len(rec))
