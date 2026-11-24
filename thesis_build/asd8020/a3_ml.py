"""Objective 2, Activity 2.2: machine-learning models with sequential floating forward selection (SFFS) and grid search in the
inner grouped folds, trained on the training plots of the hold-out split and tested once on the held-out test plots.
Tasks: A detection (grade 0 vs > 0), B severity classes (0, 1, 3, 5, 7, 9), C severity score (regression)."""
import numpy as np, pandas as pd, os, json, time, sys, warnings
from split_cfg import FOLDS, TAG, LABEL
warnings.filterwarnings('ignore')
from sklearn.svm import SVC, SVR
from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor
from sklearn.neighbors import KNeighborsClassifier, KNeighborsRegressor
from sklearn.cross_decomposition import PLSRegression
from sklearn.base import BaseEstimator, ClassifierMixin, RegressorMixin
from sklearn.model_selection import GroupKFold, GridSearchCV
from sklearn.utils.class_weight import compute_sample_weight
from mlxtend.feature_selection import SequentialFeatureSelector as SFS
import xgboost as xgb
D = os.path.dirname(os.path.abspath(__file__)) + '/data/'
NJ = int(os.environ.get('NJ', '4'))
P = np.load(D + 'prep.npz'); w5, R5, FD5 = P['w5'], P['R5'], P['FD5']
M = pd.read_csv(D + 'meta.csv'); SEL = json.load(open(D + 'fold_selection.json'))
BANDS = pd.DataFrame(np.hstack([R5, FD5]), columns=['R%d' % w for w in w5] + ['FD%d' % w for w in w5])
GR = [0, 1, 3, 5, 7, 9]; enc = {g: i for i, g in enumerate(GR)}

from a3_ml_models import models          # identical model definitions and grids, shared with a9_final.py (saved models load anywhere)
import joblib
os.makedirs(D + 'ml_models', exist_ok=True)

rows, preds, selrec = [], [], []
for f in FOLDS:
    s = SEL[str(f)]; Ff = pd.read_csv(D + 'fold%d_indices.csv' % f); tr = (M.fold != f).values; te = ~tr
    ALL = pd.concat([BANDS, Ff], axis=1); groups = M['plot'].values[tr]
    inner = list(GroupKFold(3).split(np.zeros(tr.sum()), groups=groups))
    for task in 'ABC':
        cols = s['DSF'][task]; X = ALL[cols].values; mu, sd = X[tr].mean(0), X[tr].std(0) + 1e-12; Xs = (X - mu) / sd
        if task == 'A': y = M.diseased.values; scoring = 'f1_macro'
        elif task == 'B': y = M.grade.map(enc).values; scoring = 'f1_macro'
        else: y = M.grade.values.astype(float); scoring = 'neg_root_mean_squared_error'
        for name, (est, grid) in models(task, len(cols)).items():
            t0 = time.time()
            sfs = SFS(est, k_features=(1, min(15, len(cols))), forward=True, floating=True, scoring=scoring, cv=inner, n_jobs=NJ).fit(Xs[tr], y[tr])
            sc = {k: v['avg_score'] for k, v in sfs.subsets_.items()}; best = max(sc.values())
            tol = abs(best) * 0.01; kbest = min(k for k, v in sc.items() if v >= best - tol)
            idx = list(sfs.subsets_[kbest]['feature_idx'])
            g2 = dict(grid)
            if 'n_components' in g2: g2['n_components'] = [c for c in g2['n_components'] if c <= len(idx)]
            gs = GridSearchCV(est, g2, scoring=scoring, cv=inner, n_jobs=NJ).fit(Xs[tr][:, idx], y[tr])
            final = gs.best_estimator_
            if name in ('XGBoost',) and task in 'AB': final.fit(Xs[tr][:, idx], y[tr], sample_weight=compute_sample_weight('balanced', y[tr]))
            else: final.fit(Xs[tr][:, idx], y[tr])
            yp = final.predict(Xs[te][:, idx])
            sco = None
            if task == 'A':
                if hasattr(final, 'predict_proba') and name != 'SVM': sco = final.predict_proba(Xs[te][:, idx])[:, 1]
                elif hasattr(final, 'decision_function'): sco = final.decision_function(Xs[te][:, idx]); sco = sco if sco.ndim == 1 else sco[:, 1]
            for i, (ii, pp) in enumerate(zip(np.where(te)[0], yp)):
                preds.append(dict(task=task, model=name, fold=f, leaf=int(ii), y=float(y[ii]), pred=float(pp), score=(None if sco is None else float(sco[i]))))
            joblib.dump(dict(model=final, task=task, model_name=name, candidate_features=cols, idx=idx, features=[cols[i] for i in idx], scaler_mean=mu[:], scaler_sd=sd[:],
                             params=gs.best_params_, inner_cv_score=float(gs.best_score_), scoring=scoring, fold=f), D + 'ml_models/%s_%s.joblib' % (task, name.replace(' ', '_')), compress=3)
            selrec.append(dict(task=task, model=name, fold=f, n_candidates=len(cols), selected=[cols[i] for i in idx], params=json.dumps(gs.best_params_, default=str), inner_score=float(gs.best_score_)))
            print(f, task, name, len(idx), 'of', len(cols), gs.best_params_, '%.3f' % gs.best_score_, '%.0fs' % (time.time() - t0), flush=True)
pd.DataFrame(preds).to_csv(D + 'ml_predictions.csv', index=False); pd.DataFrame(selrec).to_csv(D + 'ml_selection.csv', index=False)
print('ML finished')
