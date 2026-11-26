"""STEP 12 (H1-H3): check of the validation design with a light pipeline (selection on the training part; A SVM, B RF, C XGBoost; grid search; no SFFS):
LORO (3 folds), the main 70:30 split, other grouped 70:30 splits, random leaf-level 70:30 splits; paired comparison LORO vs 70:30 on the same test leaves."""
import os, json, warnings, numpy as np, pandas as pd
warnings.filterwarnings('ignore')
from sklearn.model_selection import GroupKFold, KFold, GridSearchCV, train_test_split
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.svm import SVC
from sklearn.ensemble import RandomForestClassifier
import xgboost as xgb
import config as C, split_lib as SL
from lib_select import select_chain, feature_table
from lib_metrics import metric_value, plot_boot_idx
C.CARS_RUNS = max(2, C.CARS_RUNS // 2)                                  # light pipeline: 10 CARS runs instead of 20
O = C.OUT; M = pd.read_csv(os.path.join(O, '03_meta_split.csv')); Z = np.load(os.path.join(O, '04_spectra.npz')); S = {k: Z[k] for k in Z.files}
F44 = pd.read_csv(os.path.join(O, '04_indices.csv')); CR = pd.read_csv(os.path.join(O, '04_continuum.csv')); W = np.load(os.path.join(O, '04_cwt.npy'))
plots = M['plot'].values; Y = {'A': M.diseased.values, 'B': M.grade.map({g: i for i, g in enumerate(C.GRADES)}).values, 'C': M.grade.values.astype(float)}
MAIN = {'A': 'macro_F1', 'B': 'macro_F1', 'C': 'R2'}
def light(te, by_leaf=False):
    tr = ~te; sel = select_chain(tr, S, F44, CR, W, M, log=lambda *a: None); T = feature_table(sel, S, F44, CR, W)
    cv = list((KFold(3, shuffle=True, random_state=0).split(np.zeros(tr.sum())) if by_leaf else GroupKFold(3).split(np.zeros(tr.sum()), groups=plots[tr]))); out = {}
    for t in 'ABC':
        X = T[sel['DSF'][t]].values
        if t == 'A': g = GridSearchCV(make_pipeline(StandardScaler(), SVC(class_weight='balanced')), {'svc__C': [0.1, 1, 10, 100], 'svc__gamma': [0.001, 0.01, 0.1, 'scale']}, scoring='f1_macro', cv=cv)
        elif t == 'B': g = GridSearchCV(RandomForestClassifier(500, class_weight='balanced', random_state=C.SEED, n_jobs=4), {'max_features': ['sqrt', 0.3], 'min_samples_leaf': [1, 3, 5]}, scoring='f1_macro', cv=cv)
        else: g = GridSearchCV(xgb.XGBRegressor(subsample=0.8, random_state=C.SEED, n_jobs=4, verbosity=0), {'n_estimators': [200, 500], 'max_depth': [3, 5], 'learning_rate': [0.05, 0.1]}, scoring='neg_root_mean_squared_error', cv=cv)
        out[t] = g.fit(X[tr], Y[t][tr]).predict(X[te])
    return out
runs, loro_pred = [], {t: np.full(len(M), np.nan) for t in 'ABC'}
for f, tp in C.LORO_TEST.items():                                                       # H3: LORO predictions of every leaf
    te = M['plot'].isin(tp).values; p = light(te)
    for t in 'ABC': loro_pred[t][te] = p[t]
    print('LORO fold', f, 'done', flush=True)
runs.append(dict(scheme='LORO', k=0, **{t: metric_value(t, MAIN[t], Y[t], loro_pred[t]) for t in 'ABC'}))
te0 = (M.fold == 0).values; main = light(te0); runs.append(dict(scheme='main 70:30', k=0, **{t: metric_value(t, MAIN[t], Y[t][te0], main[t]) for t in 'ABC'}))
for k, sp in enumerate(SL.random_splits(M, C.TEST_FRAC, C.N_REPEAT_SPLITS, seed=7)):         # H1: other grouped splits
    te = M['plot'].isin(sp).values; p = light(te); runs.append(dict(scheme='grouped 70:30', k=k, **{t: metric_value(t, MAIN[t], Y[t][te], p[t]) for t in 'ABC'})); print('grouped split', k, 'done', flush=True)
for k in range(C.N_LEAF_SPLITS):                                                        # H2: random leaf-level splits (leakage check)
    te = np.zeros(len(M), bool); te[train_test_split(np.arange(len(M)), test_size=C.TEST_FRAC, stratify=M.grade, random_state=100 + k)[1]] = True
    p = light(te, by_leaf=True); runs.append(dict(scheme='leaf-level 70:30', k=k, **{t: metric_value(t, MAIN[t], Y[t][te], p[t]) for t in 'ABC'})); print('leaf split', k, 'done', flush=True)
pd.DataFrame(runs).to_csv(os.path.join(O, '12_design_runs.csv'), index=False)
pair = []                                                                               # H3 paired comparison on the main test leaves
for t in 'ABC':
    y = Y[t][te0]; a, b = main[t], loro_pred[t][te0]; bd = []
    for ii in plot_boot_idx(plots[te0], C.N_BOOT_GAIN, 11): bd.append(metric_value(t, MAIN[t], y[ii], a[ii]) - metric_value(t, MAIN[t], y[ii], b[ii]))
    lo, hi = np.percentile(bd, [2.5, 97.5]); pair.append(dict(task=t, metric=MAIN[t], main_7030=metric_value(t, MAIN[t], y, a), LORO_same_leaves=metric_value(t, MAIN[t], y, b), CI_low=lo, CI_high=hi))
pd.DataFrame(pair).to_csv(os.path.join(O, '12_paired_LORO_vs_7030.csv'), index=False); print('CHECK: 12_design_runs.csv and 12_paired_LORO_vs_7030.csv written')
