"""STEP 7 (E3-E5): machine-learning models on the TRAINING plots: pipeline scaling, SFFS in inner GroupKFold(3), grid search, refit, ONE prediction of TEST."""
import os, json, time, warnings, numpy as np, pandas as pd, joblib
warnings.filterwarnings('ignore')
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.svm import SVC, SVR
from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor
from sklearn.neighbors import KNeighborsClassifier, KNeighborsRegressor
from sklearn.model_selection import GroupKFold, GridSearchCV
from sklearn.utils.class_weight import compute_sample_weight
from mlxtend.feature_selection import SequentialFeatureSelector as SFS
import xgboost as xgb
import config as C
from lib_spec import PLSDA, PLSR
O = C.OUT; M = pd.read_csv(os.path.join(O, '03_meta_split.csv')); T = pd.read_csv(os.path.join(O, '06_model_features.csv')); SEL = json.load(open(os.path.join(O, '06_selection_train.json')))
tr = (M.fold == 1).values; te = ~tr; groups = M['plot'].values[tr]; inner = list(GroupKFold(C.INNER_FOLDS).split(np.zeros(tr.sum()), groups=groups))
Y = {'A': M.diseased.values, 'B': M.grade.map({g: i for i, g in enumerate(C.GRADES)}).values, 'C': M.grade.values.astype(float)}
SCORING = {'A': 'f1_macro', 'B': 'f1_macro', 'C': 'neg_root_mean_squared_error'}

def models(task, p):
    pipe = lambda est: Pipeline([('scale', StandardScaler()), ('m', est)])
    if task in 'AB':
        return {'SVM': (pipe(SVC(C=10, gamma='scale', class_weight='balanced')), {'m__C': [0.1, 1, 10, 100], 'm__gamma': [0.001, 0.01, 0.1, 'scale']}),
                'RF': (pipe(RandomForestClassifier(100, class_weight='balanced', random_state=C.SEED, n_jobs=1)), {'m__n_estimators': [500], 'm__max_features': ['sqrt', 0.3], 'm__min_samples_leaf': [1, 3, 5]}),
                'XGBoost': (pipe(xgb.XGBClassifier(n_estimators=100, max_depth=4, learning_rate=0.1, subsample=0.8, n_jobs=1, random_state=C.SEED, verbosity=0)), {'m__n_estimators': [200, 500], 'm__max_depth': [3, 5], 'm__learning_rate': [0.05, 0.1]}),
                'k-NN': (pipe(KNeighborsClassifier(7, weights='distance')), {'m__n_neighbors': [3, 5, 7, 9, 11], 'm__weights': ['uniform', 'distance']}),
                'PLS-DA': (pipe(PLSDA(min(5, p))), {'m__n_components': list(range(1, min(15, p) + 1))})}
    return {'SVR': (pipe(SVR(C=10, gamma='scale')), {'m__C': [0.1, 1, 10, 100], 'm__gamma': [0.001, 0.01, 0.1, 'scale'], 'm__epsilon': [0.1, 0.5]}),
            'RF': (pipe(RandomForestRegressor(100, random_state=C.SEED, n_jobs=1)), {'m__n_estimators': [500], 'm__max_features': ['sqrt', 0.3], 'm__min_samples_leaf': [1, 3, 5]}),
            'XGBoost': (pipe(xgb.XGBRegressor(n_estimators=100, max_depth=4, learning_rate=0.1, subsample=0.8, n_jobs=1, random_state=C.SEED, verbosity=0)), {'m__n_estimators': [200, 500], 'm__max_depth': [3, 5], 'm__learning_rate': [0.05, 0.1]}),
            'k-NN': (pipe(KNeighborsRegressor(7, weights='distance')), {'m__n_neighbors': [3, 5, 7, 9, 11], 'm__weights': ['uniform', 'distance']}),
            'PLSR': (pipe(PLSR(min(5, p))), {'m__n_components': list(range(1, min(15, p) + 1))})}

os.makedirs(os.path.join(O, '07_ml_models'), exist_ok=True); preds, rec = [], []
for task in 'ABC':
    cols = SEL['DSF'][task]; X = T[cols].values; y = Y[task]
    for name, (est, grid) in models(task, len(cols)).items():
        t0 = time.time()
        sfs = SFS(est, k_features=(1, min(C.SFFS_MAX, len(cols))), forward=True, floating=True, scoring=SCORING[task], cv=inner, n_jobs=4).fit(X[tr], y[tr])
        sc = {k: v['avg_score'] for k, v in sfs.subsets_.items()}; best = max(sc.values()); kbest = min(k for k, v in sc.items() if v >= best - abs(best) * C.SFFS_TOL)
        idx = list(sfs.subsets_[kbest]['feature_idx']); g2 = dict(grid)
        if 'm__n_components' in g2: g2['m__n_components'] = [c for c in g2['m__n_components'] if c <= len(idx)]
        gs = GridSearchCV(est, g2, scoring=SCORING[task], cv=inner, n_jobs=4).fit(X[tr][:, idx], y[tr]); final = gs.best_estimator_
        if name == 'XGBoost' and task in 'AB': final.fit(X[tr][:, idx], y[tr], m__sample_weight=compute_sample_weight('balanced', y[tr]))
        else: final.fit(X[tr][:, idx], y[tr])
        yp = final.predict(X[te][:, idx]); s = None                                         # the ONLY use of the test leaves
        if task == 'A': s = final.decision_function(X[te][:, idx]) if name == 'SVM' else final.predict_proba(X[te][:, idx])[:, 1]
        for i, (leaf, p) in enumerate(zip(np.where(te)[0], yp)): preds.append(dict(task=task, model=name, family='ML', leaf=int(leaf), y=float(y[leaf]), pred=float(p), score=(None if s is None else float(s[i]))))
        joblib.dump(dict(model=final, task=task, name=name, features=[cols[i] for i in idx], params=gs.best_params_, inner_score=gs.best_score_), os.path.join(O, '07_ml_models', '%s_%s.joblib' % (task, name)))
        rec.append(dict(task=task, model=name, n_candidates=len(cols), n_selected=len(idx), selected=' '.join(cols[i] for i in idx), params=json.dumps(gs.best_params_, default=str), inner_score=gs.best_score_))
        print('task %s %-8s %d of %d features  inner score %.3f  %.0fs' % (task, name, len(idx), len(cols), gs.best_score_, time.time() - t0), flush=True)
pd.DataFrame(preds).to_csv(os.path.join(O, '07_ml_predictions.csv'), index=False); pd.DataFrame(rec).to_csv(os.path.join(O, '07_ml_selection.csv'), index=False)
print('CHECK: 15 models saved in 07_ml_models; predictions of %d test leaves per model' % te.sum())
