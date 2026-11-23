"""Activity 2.5-2.6 and Step 2.5.5 for the leaf data: metric tables, weather covariates and covariate baseline (unsprayed leaves),
results by stratum, leave-one-variety-out and leave-one-timing-out tests, SHAP of the best tree model, selection stability,
and the exploratory test of symptomless leaves of unsprayed plots vs leaves of the sprayed healthy plots."""
import numpy as np, pandas as pd, os, json, warnings
warnings.filterwarnings('ignore')
from a5_metrics import *
from alib import *
from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor
from sklearn.svm import SVC
from sklearn.neighbors import KNeighborsClassifier
import xgboost as xgb, shap
D = os.path.dirname(os.path.abspath(__file__)) + '/data/'
P = np.load(D + 'prep.npz'); wl, w5, R1, FD1, R5, FD5 = P['wl'], P['w5'], P['R1'], P['FD1'], P['R5'], P['FD5']
M = pd.read_csv(D + 'meta.csv'); SEL = json.load(open(D + 'fold_selection.json')); O1 = json.load(open(D + 'o1_results.json'))
BANDS = pd.DataFrame(np.hstack([R5, FD5]), columns=['R%d' % w for w in w5] + ['FD%d' % w for w in w5]); Fall = pd.read_csv(D + 'indices_full.csv')
enc = {g: i for i, g in enumerate(GR)}

# ---------------- metric tables (ML + DL) ----------------
ml = pd.read_csv(D + 'ml_predictions.csv'); ml['source'] = 'ML'
dl = []
for fn in ['dl_main.json']:
    if os.path.exists(D + fn):
        for r in json.load(open(D + fn)):
            for i, (lf, yy, pp) in enumerate(zip(r['leaf'], r['y'], r['pred'])):
                dl.append(dict(task=r['task'], model=r['net'], fold=r['fold'], leaf=lf, y=yy, pred=pp, score=(r['score'][i] if r['score'] else None), source='DL'))
dl = pd.DataFrame(dl); allp = pd.concat([ml, dl], ignore_index=True)
allp.loc[allp.task == 'C', 'pred'] = allp.loc[allp.task == 'C', 'pred'].clip(0, 9)
MT, CMS = summarise(allp); MT.to_csv(D + 'metrics_all.csv', index=False); allp.to_csv(D + 'all_predictions.csv', index=False)
# DL configuration and ablation summaries (six classes)
def dlsum(fn, tag):
    if not os.path.exists(D + fn): return None
    rows = []
    for r in json.load(open(D + fn)):
        for i, (lf, yy, pp) in enumerate(zip(r['leaf'], r['y'], r['pred'])): rows.append(dict(task=r['task'], model=r['net'], cfg=r['tag'], fold=r['fold'], y=yy, pred=pp))
    d = pd.DataFrame(rows); out = []
    for (mname, cfg), g in d.groupby(['model', 'cfg']):
        m, _ = cls_metrics(g.y.values, g.pred.values, 6); out.append(dict(net=mname, config=cfg, **{k: m[k] for k in ('OA', 'kappa', 'macro_R', 'macro_F1', 'QWK')}))
    return pd.DataFrame(out)
cf = dlsum('dl_config.json', 'config')
if cf is not None:
    mainB = MT[(MT.task == 'B') & MT.model.isin(['DT-EDNet', 'EfficientNet-B0', 'ResNet18', 'ConvNeXt V2-Atto'])]
    cf = pd.concat([cf, pd.DataFrame([dict(net=r.model, config='DSF', OA=r.OA, kappa=r.kappa, macro_R=r.macro_R, macro_F1=r.macro_F1, QWK=r.QWK) for r in mainB.itertuples()])], ignore_index=True)
    cf.to_csv(D + 'dl_summary_config.csv', index=False)
ab = dlsum('dl_ablation.json', 'ablation')
if ab is not None:
    full = MT[(MT.task == 'B') & (MT.model == 'DT-EDNet')].iloc[0]
    ab = pd.concat([pd.DataFrame([dict(net='DT-EDNet', config='ablation', OA=full.OA, kappa=full.kappa, macro_R=full.macro_R, macro_F1=full.macro_F1, QWK=full.QWK)]), ab], ignore_index=True)
    ab.to_csv(D + 'dl_summary_ablation.csv', index=False)
# DL run information (epochs, parameters)
if os.path.exists(D + 'dl_main.json'):
    pd.DataFrame([dict(net=r['net'], task=r['task'], fold=r['fold'], k=r['k'], p=r['p'], epochs=r['epochs'], best_val=r['best_val'], nparam=r['nparam']) for r in json.load(open(D + 'dl_main.json'))]).to_csv(D + 'dl_runs.csv', index=False)
np.save(D + 'confusion.npy', {f'{k[0]}|{k[1]}': v for k, v in CMS.items()}, allow_pickle=True)
best = {}
for t, key in (('A', 'macro_F1'), ('B', 'macro_F1'), ('C', 'RMSE')):
    d = MT[MT.task == t]; asc = key == 'RMSE'
    best[t] = dict(overall=d.sort_values(key, ascending=asc).model.iloc[0], ML=d[d.model.isin(ml.model.unique())].sort_values(key, ascending=asc).model.iloc[0])
    dd = d[d.model.isin(dl.model.unique())] if len(dl) else d.iloc[:0]
    best[t]['DL'] = dd.sort_values(key, ascending=asc).model.iloc[0] if len(dd) else None
json.dump(best, open(D + 'best_models.json', 'w'), indent=1); print(MT[['task', 'model', 'OA', 'kappa', 'macro_F1', 'QWK', 'AUC', 'R2', 'RMSE', 'RPD']].round(3).to_string()); print(best)

# ---------------- results by stratum for the best ML and DL models ----------------
strat = []
for t in 'ABC':
    for src in ('ML', 'DL'):
        mname = best[t][src]
        if mname is None: continue
        d = allp[(allp.task == t) & (allp.model == mname)].copy(); d = d.merge(M[['variety', 'stage', 'leaf', 'date', 'timing']], left_on='leaf', right_index=True, how='left', suffixes=('', '_m'))
        d = d.rename(columns={'leaf_m': 'leafpos'}) if 'leaf_m' in d else d
        lp = M.loc[d['leaf'].values, 'leaf'].values; d['leafpos'] = lp
        for fac in ('variety', 'stage', 'leafpos', 'date', 'timing'):
            for lev, g in d.groupby(fac):
                if t in 'AB':
                    K = 2 if t == 'A' else 6; m, _ = cls_metrics(g.y.values, g.pred.values, K); val = m['macro_F1']; oa = m['OA']
                    strat.append(dict(task=t, source=src, model=mname, factor=fac, level=lev, n=len(g), macro_F1=val, OA=oa))
                else:
                    m = reg_metrics(g.y.values, g.pred.values); strat.append(dict(task=t, source=src, model=mname, factor=fac, level=lev, n=len(g), RMSE=m['RMSE'], R2=m['R2']))
pd.DataFrame(strat).to_csv(D + 'strata_metrics.csv', index=False)

# ---------------- weather covariates (IARI observatory) ----------------
W = pd.read_excel('/root/.claude/uploads/c5704ca0-f1ca-5695-b9e0-a810fbe166a9/96b9a6e5-WEATHER_DATA_Jan_2024_to_tilldate_1.xlsx')
W.columns = ['date', 'Tmax', 'Tmin', 'rain', 'wind', 'wd1', 'wd2', 'wc1', 'wc2', 'RH1', 'RH2', 'BSS', 'evap']; W['date'] = pd.to_datetime(W.date)
for c in ['Tmax', 'Tmin', 'rain', 'wind', 'RH1', 'RH2', 'BSS', 'evap']: W[c] = pd.to_numeric(W[c], errors='coerce')
season = W[(W.date >= '2025-12-01') & (W.date <= '2026-03-20')].copy(); season.to_csv(D + 'weather_season.csv', index=False)
# natural infection: favourable days (Chattopadhyay et al., 2011) counted in the 7-day window and from the first sowing (9 Dec 2025)
FAVL = lambda w: int(((w.Tmax.between(16, 24)) & (w.RH1 > 97) & (w.RH2 > 40)).sum()); FAVS = lambda w: int(((w.Tmax.between(20, 29)) & (w.Tmin > 12) & (w.RH1 > 97)).sum())
sow1 = pd.Timestamp('2025-12-09'); wc = []
for dt in sorted(M.date.unique()):
    t = pd.Timestamp(dt); win = W[(W.date < t) & (W.date >= t - pd.Timedelta(days=7))]; since = W[(W.date >= sow1) & (W.date < t)]
    wc.append(dict(date=dt, Tmax7=win.Tmax.mean(), Tmin7=win.Tmin.mean(), RH1_7=win.RH1.mean(), RH2_7=win.RH2.mean(), rain7=win.rain.sum(), wind7=win.wind.mean(), BSS7=win.BSS.mean(), evap7=win.evap.mean(),
                   fav7_leaf=FAVL(win), fav_leaf_season=FAVL(since), fav_staghead_season=FAVS(since), last_fav_leaf_day=str(since[(since.Tmax.between(16, 24)) & (since.RH1 > 97) & (since.RH2 > 40)].date.max())[:10]))
WC = pd.DataFrame(wc); WC.to_csv(D + 'weather_covariates.csv', index=False); print(WC.round(2).to_string())
prog = M.groupby('date').agg(mean_grade=('grade', 'mean'), pct_diseased=('diseased', 'mean'), n=('grade', 'size')).reset_index(); prog['pct_diseased'] *= 100
prog.merge(WC, on='date').to_csv(D + 'disease_progress.csv', index=False)

# ---------------- quick covariate check (random forest; the full Step 2.5.5 analysis is in a11_covariate.py): unsprayed leaves only ----------------
inoc_m = (M.unsprayed == 1).values
COV = pd.get_dummies(M[['variety', 'timing']].astype(str)).astype(float); COV['DAS'] = M.DAS; COV['stage'] = M.stage_code
COV = pd.concat([COV, M[['date']].merge(WC.drop(columns='last_fav_leaf_day'), on='date', how='left').drop(columns='date')], axis=1)
cb = []
for t in 'ABC':
    for variant in ('covariates only', 'leaf spectra (DSF)', 'leaf spectra + covariates'):
        ys, ps = [], []
        for f in range(3):
            Ff = pd.read_csv(D + 'fold%d_indices.csv' % f); ALL = pd.concat([BANDS, Ff], axis=1); dsf = SEL[str(f)]['DSF'][t]
            X = {'covariates only': COV.values, 'leaf spectra (DSF)': ALL[dsf].values, 'leaf spectra + covariates': np.hstack([ALL[dsf].values, COV.values])}[variant]
            tr = (M.fold != f).values & inoc_m; te = (M.fold == f).values & inoc_m
            if t == 'A': y = M.diseased.values; mdl = RandomForestClassifier(500, class_weight='balanced', random_state=42, n_jobs=4)
            elif t == 'B': y = M.grade.map(enc).values; mdl = RandomForestClassifier(500, class_weight='balanced', random_state=42, n_jobs=4)
            else: y = M.grade.values.astype(float); mdl = RandomForestRegressor(500, random_state=42, n_jobs=4)
            mdl.fit(X[tr], y[tr]); ys += list(y[te]); ps += list(mdl.predict(X[te]))
        m = cls_metrics(ys, ps, 2 if t == 'A' else 6)[0] if t in 'AB' else reg_metrics(ys, ps)
        cb.append(dict(task=t, variant=variant, **{k: m[k] for k in (('OA', 'kappa', 'macro_F1') if t in 'AB' else ('R2', 'RMSE', 'RPD'))}))
pd.DataFrame(cb).to_csv(D + 'covariate_baseline.csv', index=False); print(pd.DataFrame(cb).round(3).to_string())

# ---------------- leave-one-variety-out and leave-one-timing-out (best ML model type, selection inside each training set) ----------------
def select_feats(tr, task):
    y = M.grade.values.astype(float); Nm, Sm = r2_maps(R5[tr], y[tr]); used, _ = effective_ranges(Nm, Sm, w5)
    re = (w5 >= 680) & (w5 <= 760); cR = np.where(used)[0]; cF = np.where(used | re)[0]
    Xc = np.hstack([R5[tr][:, cR], FD5[tr][:, cF]]); names = ['R%d' % w5[i] for i in cR] + ['FD%d' % w5[i] for i in cF]
    sc = shap_cars(Xc, y[tr], names, runs=10, n_iter=50, seed=7)
    kept = corr_filter(Fall[tr].reset_index(drop=True), y[tr], 0.95); grp = M['plot'].values[tr]
    yl = M.diseased.values if task == 'A' else (M.grade.values if task == 'B' else y)
    Wt = relieff(Fall[kept].values[tr], yl[tr], grp, regression=(task == 'C')); vi = [kept[i] for i in np.argsort(-Wt)[:5]]
    pool = pd.concat([BANDS[sc['names']], Fall[vi]], axis=1)[tr]; return vif_filter(pool, 10.0)[0]
tt = []
for fac, levels in ([] if os.environ.get('SKIP_TRANSFER') else (('variety', ['V1', 'V2', 'V3']), ('timing', ['D1', 'D2', 'D3', 'D4']))):
    for lev in levels:
        te = (M[fac] == lev).values; tr = ~te
        for t in 'BC':
            cols = select_feats(tr, t); ALL = pd.concat([BANDS, Fall], axis=1); X = ALL[cols].values
            if t == 'B': y = M.grade.map(enc).values; mdl = RandomForestClassifier(500, class_weight='balanced', random_state=42, n_jobs=4)
            else: y = M.grade.values.astype(float); mdl = RandomForestRegressor(500, random_state=42, n_jobs=4)
            mdl.fit(X[tr], y[tr]); yp = mdl.predict(X[te])
            m = cls_metrics(y[te], yp, 6)[0] if t == 'B' else reg_metrics(y[te], yp)
            tt.append(dict(test=fac, level=lev, task=t, n_test=int(te.sum()), **({'macro_F1': m['macro_F1'], 'OA': m['OA']} if t == 'B' else {'RMSE': m['RMSE'], 'R2': m['R2']})))
            print('transfer', fac, lev, t, tt[-1], flush=True)
if tt: pd.DataFrame(tt).to_csv(D + 'transfer_tests.csv', index=False)

# ---------------- SHAP of the best tree model on the Objective 1 disease-specific feature set ----------------
dsf = O1['DSF']; Xd = pd.concat([BANDS, Fall], axis=1)[dsf]
mC = xgb.XGBRegressor(n_estimators=300, max_depth=4, learning_rate=0.05, subsample=0.8, random_state=42, n_jobs=4).fit(Xd, M.grade.values)
svC = shap.TreeExplainer(mC).shap_values(Xd); np.save(D + 'shap_C.npy', svC); Xd.to_csv(D + 'shap_X.csv', index=False)
mB = xgb.XGBClassifier(n_estimators=300, max_depth=4, learning_rate=0.05, subsample=0.8, random_state=42, n_jobs=4).fit(Xd, M.grade.map(enc).values)
svB = shap.TreeExplainer(mB).shap_values(Xd); svB = np.abs(np.array(svB)); imp = svB.mean(0) if svB.ndim == 3 and svB.shape[0] == len(Xd) else svB.mean(1)
impB = pd.DataFrame(imp, index=dsf) if imp.ndim == 2 else pd.DataFrame({'all': imp}, index=dsf)
impB.to_csv(D + 'shap_B_importance.csv')

# ---------------- selection stability across folds ----------------
st = []
for key in ('OW',):
    allf = [x for f in range(3) for x in SEL[str(f)][key]]
    for feat in sorted(set(allf)): st.append(dict(group='optimal wavelengths', feature=feat, folds=allf.count(feat)))
for t in 'ABC':
    allf = [x for f in range(3) for x in SEL[str(f)]['VI'][t]]
    for feat in sorted(set(allf)): st.append(dict(group='indices task ' + t, feature=feat, folds=allf.count(feat)))
mls = pd.read_csv(D + 'ml_selection.csv')
for (t, mname), d in mls.groupby(['task', 'model']):
    allf = [x for s in d.selected for x in eval(s)]
    for feat in sorted(set(allf)): st.append(dict(group='SFFS %s %s' % (t, mname), feature=feat, folds=allf.count(feat)))
pd.DataFrame(st).to_csv(D + 'selection_stability.csv', index=False)

# ---------------- exploratory: symptomless leaves of unsprayed (naturally infected) plots vs leaves of the sprayed healthy plots ----------------
mask = (M.grade == 0).values; y = M.unsprayed.values; ex = []
preds = []
for name in ('SVM', 'RF', 'XGBoost', 'k-NN'):
    for f in range(3):
        Ff = pd.read_csv(D + 'fold%d_indices.csv' % f); ALL = pd.concat([BANDS, Ff], axis=1); cols = SEL[str(f)]['DSF']['A']
        X = ALL[cols].values; tr = (M.fold != f).values & mask; te = (M.fold == f).values & mask
        mu, sd = X[tr].mean(0), X[tr].std(0) + 1e-12; Xs = (X - mu) / sd
        mdl = {'SVM': SVC(C=10, gamma='scale', class_weight='balanced'), 'RF': RandomForestClassifier(500, class_weight='balanced', random_state=42, n_jobs=4),
               'XGBoost': xgb.XGBClassifier(n_estimators=300, max_depth=3, learning_rate=0.05, random_state=42, n_jobs=4), 'k-NN': KNeighborsClassifier(7)}[name]
        mdl.fit(Xs[tr], y[tr]); yp = mdl.predict(Xs[te])
        sc = mdl.predict_proba(Xs[te])[:, 1] if hasattr(mdl, 'predict_proba') and name != 'SVM' else mdl.decision_function(Xs[te])
        for i, ii in enumerate(np.where(te)[0]): preds.append(dict(task='X', model=name, fold=f, leaf=int(ii), y=int(y[ii]), pred=int(yp[i]), score=float(sc[i])))
EX, _ = summarise(pd.DataFrame(preds)); EX.to_csv(D + 'exploratory_asymptomatic.csv', index=False); print(EX[['model', 'balanced_acc', 'AUC', 'sensitivity', 'specificity']].round(3))
print('extra done')
