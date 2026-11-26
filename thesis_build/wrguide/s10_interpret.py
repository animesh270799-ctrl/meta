"""STEP 10 (F5-F7): SHAP of XGBoost on the Objective 1 DSF; metrics by stratum of the best ML and DL six-grade models; transfer to a held-out
variety, sowing date and sampling date (selection repeated inside each training part); stability of the optimal wavelengths across training sets."""
import os, json, numpy as np, pandas as pd
import config as C
from lib_select import select_chain, feature_table
from lib_metrics import cls_metrics, reg_metrics
from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor
import xgboost as xgb, shap
O = C.OUT; M = pd.read_csv(os.path.join(O, '03_meta_split.csv')); Z = np.load(os.path.join(O, '04_spectra.npz')); S = {k: Z[k] for k in Z.files}
F44 = pd.read_csv(os.path.join(O, '04_indices.csv')); CR = pd.read_csv(os.path.join(O, '04_continuum.csv')); W = np.load(os.path.join(O, '04_cwt.npy'))
enc = {g: i for i, g in enumerate(C.GRADES)}; quiet = lambda *a: None
# F5 SHAP (descriptive, all leaves, Objective 1 DSF of task C)
s5 = json.load(open(os.path.join(O, '05_obj1_selection.json'))); T5 = feature_table(s5, S, F44, CR, W)[s5['DSF']['C']]
mC = xgb.XGBRegressor(random_state=C.SEED, n_jobs=4, **C.XGB_SHAP).fit(T5, M.grade); sv = shap.TreeExplainer(mC).shap_values(T5)
pd.DataFrame({'feature': T5.columns, 'mean_abs_SHAP': np.abs(sv).mean(0)}).sort_values('mean_abs_SHAP', ascending=False).to_csv(os.path.join(O, '10_shap_importance.csv'), index=False)
# F6a strata of the best ML and best DL six-grade models
R = pd.read_csv(os.path.join(O, '09_test_metrics.csv')); P = pd.concat([pd.read_csv(os.path.join(O, '07_ml_predictions.csv')), pd.read_csv(os.path.join(O, '08_dl_predictions_main.csv'))]); st = []
for fam in ('ML', 'DL'):
    best = R[(R.task == 'B') & (R.family == fam)].sort_values('macro_F1').model.iloc[-1]; d = P[(P.task == 'B') & (P.model == best)].merge(M[['stage', 'variety', 'leaf', 'date', 'timing']], left_on='leaf', right_index=True, suffixes=('_id', ''))
    for f in ('stage', 'variety', 'leaf', 'date', 'timing'):
        for lev, g in d.groupby(f): st.append(dict(model=best, factor=f, level=lev, n=len(g), macro_F1=cls_metrics(g.y, g.pred, 6)[0]['macro_F1']))
pd.DataFrame(st).to_csv(os.path.join(O, '10_strata.csv'), index=False)
# F6b transfer: leave one variety / sowing date / sampling date out (all leaves; selection repeated inside each training part)
tt = []; groups = [('variety', sorted(M.variety.unique())), ('timing', sorted(M.timing.unique())), ('date', sorted(M.date.unique()))]
if C.FAST: groups = [('variety', [sorted(M.variety.unique())[0]])]
for fac, levels in groups:
    for lev in levels:
        te = (M[fac] == lev).values; sel = select_chain(~te, S, F44, CR, W, M, log=quiet); T = feature_table(sel, S, F44, CR, W)
        for t in 'BC':
            X = T[sel['DSF'][t]].values
            if t == 'B':
                y = M.grade.map(enc).values; p = RandomForestClassifier(500, class_weight='balanced', random_state=C.SEED, n_jobs=4).fit(X[~te], y[~te]).predict(X[te]); tt.append(dict(held_out=fac, level=lev, task=t, n=int(te.sum()), macro_F1=cls_metrics(y[te], p, 6)[0]['macro_F1']))
            else:
                y = M.grade.values.astype(float); p = RandomForestRegressor(500, random_state=C.SEED, n_jobs=4).fit(X[~te], y[~te]).predict(X[te]); m = reg_metrics(y[te], p); tt.append(dict(held_out=fac, level=lev, task=t, n=int(te.sum()), RMSE=m['RMSE'], R2=m['R2']))
        print('transfer', fac, lev, 'done', flush=True)
pd.DataFrame(tt).to_csv(os.path.join(O, '10_transfer.csv'), index=False)
# F7 stability: optimal wavelengths in TRAIN and in the three leave-one-replication-out training parts
sets = {'70:30 TRAIN': json.load(open(os.path.join(O, '06_selection_train.json')))['OW']}
for f, tp in ([] if C.FAST else C.LORO_TEST.items()):
    sets['LORO fold %d' % f] = select_chain(~M['plot'].isin(tp).values, S, F44, CR, W, M, log=quiet)['OW']
allw = sorted(set(sum(sets.values(), []))); pd.DataFrame([dict(feature=w, n_sets=sum(w in v for v in sets.values()), **{k: w in v for k, v in sets.items()}) for w in allw]).sort_values('n_sets', ascending=False).to_csv(os.path.join(O, '10_stability.csv'), index=False)
print('CHECK: 10_shap_importance.csv, 10_strata.csv, 10_transfer.csv, 10_stability.csv written')
