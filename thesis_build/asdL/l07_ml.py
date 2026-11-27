"""STEP L6 (machine learning): SVM/SVR, random forest, k-NN and PLS-DA/PLSR on the leaf DSF of each task.
For each model x task: SFFS (mlxtend, floating, 1-15 features, default settings, GroupKFold(3) by plot on the TRAINING leaves) ->
grid search on the chosen features (same folds) -> refit on all training leaves -> ONE prediction of the 684 test leaves."""
import os, sys, json, time, warnings, numpy as np, pandas as pd
warnings.filterwarnings('ignore')
from sklearn.model_selection import GridSearchCV
from mlxtend.feature_selection import SequentialFeatureSelector as SFS
import joblib
import configL as C
from lmods import base, grid, score_of
O = C.OUT; M = pd.read_csv(os.path.join(O, 'L2_meta.csv')); ALL = pd.read_csv(os.path.join(O, 'L5_all_features.csv')); SEL = json.load(open(os.path.join(O, 'L5_selection.json')))
tr = (M.split == 'TRAIN').values; te = ~tr; folds = M.inner_fold.values[tr]; SPLITS = [(np.where(folds != k)[0], np.where(folds == k)[0]) for k in (1, 2, 3)]
Y = {'A': M.diseased.values.astype(int), 'B': M.grade.map({g: i for i, g in enumerate(C.GRADES)}).values.astype(int), 'C': M.grade.values.astype(float)}
SCORING = {'A': 'f1_macro', 'B': 'f1_macro', 'C': 'neg_root_mean_squared_error'}

MODELS = ['SVM', 'RF', 'k-NN', 'PLS']; jobs = [(m, t) for t in 'ABC' for m in MODELS]
if len(sys.argv) > 1: jobs = [j for j in jobs if j[0] in sys.argv[1].split(',')]
os.makedirs(os.path.join(O, 'L6_models'), exist_ok=True); rows, preds, paths = [], [], []
for model, task in jobs:
    t0 = time.time(); cols = SEL['DSF'][task]; X = ALL[cols].values; Xtr, ytr = X[tr], Y[task][tr]; p = len(cols)
    sfs = SFS(base(model, task), k_features=(1, min(C.SFFS_MAX, p)), forward=True, floating=True, scoring=SCORING[task], cv=SPLITS, n_jobs=(1 if model == 'RF' else 4)).fit(Xtr, ytr)
    chosen = [cols[i] for i in sfs.k_feature_idx_]
    for k_, d in sfs.subsets_.items(): paths.append(dict(task=task, model=model, n_features=k_, cv_score=float(d['avg_score']), features=' '.join(cols[i] for i in d['feature_idx'])))
    ci = [cols.index(c) for c in chosen]; g = GridSearchCV(base(model, task), grid(model, task, len(ci)), scoring=SCORING[task], cv=SPLITS, n_jobs=(1 if model == 'RF' else 4), refit=True).fit(Xtr[:, ci], ytr)
    est = g.best_estimator_; yp = est.predict(X[te][:, ci]); s = score_of(est, X[te][:, ci], task)
    if task == 'C': yp = np.clip(yp, 0, 9)
    joblib.dump(dict(model=est, features=chosen, task=task, name=model), os.path.join(O, 'L6_models', '%s_%s.joblib' % (task, model.replace('-', ''))))
    for i, leaf in enumerate(np.where(te)[0]): preds.append(dict(task=task, model=model, family='ML', leaf=int(leaf), y=float(Y[task][leaf]), pred=float(yp[i]), score=(None if s is None else float(s[i]))))
    rows.append(dict(task=task, model=model, dsf_size=p, sffs_n=len(chosen), sffs_features=' '.join(chosen), sffs_cv=float(sfs.k_score_), grid_best=json.dumps(g.best_params_), grid_cv=float(g.best_score_), seconds=round(time.time() - t0)))
    print('task %s %-5s SFFS %2d/%2d cv %.3f | grid %s cv %.3f | %.0fs' % (task, model, len(chosen), p, sfs.k_score_, g.best_params_, g.best_score_, time.time() - t0), flush=True)
tag = '' if len(sys.argv) == 1 else '_' + sys.argv[1].replace(',', '_').replace('-', '')
pd.DataFrame(rows).to_csv(os.path.join(O, 'L6_ml_summary%s.csv' % tag), index=False); pd.DataFrame(preds).to_csv(os.path.join(O, 'L6_ml_predictions%s.csv' % tag), index=False)
pd.DataFrame(paths).to_csv(os.path.join(O, 'L6_sffs_paths%s.csv' % tag), index=False); print('CHECK done: %d model x task runs' % len(jobs))
