"""Final (deployable) models trained on ALL leaves (L3, L5, LL) after the leave-one-replication-out evaluation.
The evaluation numbers come from the outer folds (a3_ml.py, a4_dl.py); these files are the models refitted on the full data set
with the same procedure, for prediction on new leaves.
  python3 a9_final.py ml   -> per-task feature set (Objective 1 optimal wavelengths + top-5 ReliefF indices -> VIF < 10),
                              SFFS + grid search in GroupKFold(3) by plot, refit on all leaves, saved with joblib
  python3 a9_final.py dl   -> DNN-F1, DT-EDNet, EfficientNet-B0, ResNet18, ConvNeXt V2-Atto on all leaves for the median best epoch
                              found in the outer folds (no data held back), saved as PyTorch state dicts"""
import numpy as np, pandas as pd, os, json, sys, time, shutil, warnings, platform
warnings.filterwarnings('ignore')
from alib import vif_filter
from wr_features import PLSDA, PLSR, all_features, GRADES
B = os.path.dirname(os.path.abspath(__file__)) + '/'; D = B + 'data/'
OUT = B + '../outputs/ASD_2025-26_models/'; os.makedirs(OUT + 'ml', exist_ok=True); os.makedirs(OUT + 'dl', exist_ok=True)
M = pd.read_csv(D + 'meta.csv'); O1 = json.load(open(D + 'o1_results.json'))
SEL = dict(ndsi=O1['best_ndsi'][:2], rsi=O1['best_rsi'][:2], wri={k: O1['WRI'][k] for k in ('l1', 'l2', 'w', 'l3')})
X0 = np.load(D + 'X_leaf.npy').astype(float); wl0 = np.load(D + 'wl.npy')
ALL = all_features(X0, wl0, SEL)
# check: identical to the training tables
P = np.load(D + 'prep.npz'); Ff = pd.read_csv(D + 'indices_full.csv')
assert np.allclose(ALL[['R%d' % w for w in P['w5']]].values, P['R5'], atol=1e-5) and np.allclose(ALL[Ff.columns].values, Ff.values, rtol=1e-4, atol=1e-6), 'feature mismatch'
VI = {'A': O1['VI_binary'], 'B': O1['VI_classes'], 'C': O1['VI_score']}
DSF = {t: vif_filter(ALL[O1['OW'] + [c for c in VI[t] if c not in O1['OW']]], 10.0)[0] for t in 'ABC'}
SEL.update(OW=O1['OW'], VI=VI, DSF=DSF); json.dump(SEL, open(OUT + 'feature_selection.json', 'w'), indent=1)
enc = {g: i for i, g in enumerate(GRADES)}
def target(task):
    if task == 'A': return M.diseased.values
    if task == 'B': return M.grade.map(enc).values
    return M.grade.values.astype(float)
TASKN = {'A': 'detection (0 = healthy, 1 = diseased)', 'B': 'six severity grades (class index 0-5 = grade 0, 1, 3, 5, 7, 9)', 'C': 'severity score (0-9, regression)'}
part = sys.argv[1] if len(sys.argv) > 1 else 'ml'

if part == 'ml':
    import joblib, sklearn, xgboost
    from sklearn.model_selection import GroupKFold, GridSearchCV
    from sklearn.utils.class_weight import compute_sample_weight
    from mlxtend.feature_selection import SequentialFeatureSelector as SFS
    import a3_ml_models as MM
    NJ = int(os.environ.get('NJ', '2')); inner = list(GroupKFold(3).split(np.zeros(len(M)), groups=M['plot'].values)); rec = []
    for task in 'ABC':
        cols = DSF[task]; X = ALL[cols].values; mu, sd = X.mean(0), X.std(0) + 1e-12; Xs = (X - mu) / sd; y = target(task)
        scoring = 'f1_macro' if task in 'AB' else 'neg_root_mean_squared_error'
        for name, (est, grid) in MM.models(task, len(cols)).items():
            t0 = time.time()
            sfs = SFS(est, k_features=(1, min(15, len(cols))), forward=True, floating=True, scoring=scoring, cv=inner, n_jobs=NJ).fit(Xs, y)
            sc = {k: v['avg_score'] for k, v in sfs.subsets_.items()}; best = max(sc.values()); kbest = min(k for k, v in sc.items() if v >= best - abs(best) * 0.01)
            idx = list(sfs.subsets_[kbest]['feature_idx']); g2 = dict(grid)
            if 'n_components' in g2: g2['n_components'] = [c for c in g2['n_components'] if c <= len(idx)]
            gs = GridSearchCV(est, g2, scoring=scoring, cv=inner, n_jobs=NJ).fit(Xs[:, idx], y); final = gs.best_estimator_
            if name == 'XGBoost' and task in 'AB': final.fit(Xs[:, idx], y, sample_weight=compute_sample_weight('balanced', y))
            else: final.fit(Xs[:, idx], y)
            fn = '%s_%s.joblib' % ({'A': 'A_detection', 'B': 'B_six_grades', 'C': 'C_severity_score'}[task], name.replace(' ', '_'))
            bundle = dict(model=final, task=task, task_description=TASKN[task], model_name=name, features=[cols[i] for i in idx], candidate_features=cols, idx=idx,
                          scaler_mean=mu, scaler_sd=sd, grades=GRADES, params=gs.best_params_, inner_cv_score=float(gs.best_score_), scoring=scoring,
                          trained_on='%d leaves (L3, L5, LL), 4 dates (11 Feb - 13 Mar 2026), IARI 2025-26, natural infection' % len(M), versions=dict(sklearn=sklearn.__version__, xgboost=xgboost.__version__, python=platform.python_version()))
            joblib.dump(bundle, OUT + 'ml/' + fn, compress=3)
            rec.append(dict(file='ml/' + fn, task=task, model=name, n_features=len(idx), features=', '.join(bundle['features']), params=json.dumps(gs.best_params_, default=str), inner_cv_score=round(float(gs.best_score_), 4), scoring=scoring))
            print(task, name, len(idx), gs.best_params_, '%.3f' % gs.best_score_, '%.0fs' % (time.time() - t0), flush=True)
    pd.DataFrame(rec).to_csv(OUT + 'ml_models_index.csv', index=False); print('ML final models saved')

if part == 'dl':
    import torch, torch.nn as nn
    torch.set_num_threads(int(os.environ.get('TT', '4')))
    import wr_networks as NW
    R = json.load(open(D + 'dl_main.json')); rec = []
    for task in 'ABC':
        cols = DSF[task]; X = ALL[cols].values.astype(np.float32); mu, sd = X.mean(0), X.std(0) + 1e-6; X = (X - mu) / sd; y = target(task); K = {'A': 2, 'B': 6, 'C': 1}[task]
        for net in (sys.argv[2].split(',') if len(sys.argv) > 2 else ['DNN-F1', 'DT-EDNet', 'EfficientNet-B0', 'ResNet18', 'ConvNeXt V2-Atto']):
            runs = [r for r in R if r['net'] == net and r['task'] == task]
            if not runs: continue
            E = int(np.median([int(np.array(r['hist'])[:, 3].argmax()) + 1 for r in runs])); E = max(E, 10); lr = runs[0]['lr']
            torch.manual_seed(42); rng = np.random.default_rng(42)
            Xi, k = (X.reshape(-1, 1, 1, X.shape[1]), 1) if net == 'DNN-F1' else NW.pseudo(X); model = NW.build(net, k, X.shape[1], K, 0.03)
            opt = torch.optim.AdamW(model.parameters(), lr=lr, weight_decay=1e-5); sch = torch.optim.lr_scheduler.CosineAnnealingLR(opt, E, eta_min=1e-6)
            if K > 1: cw = torch.tensor(len(y) / (K * np.bincount(y, minlength=K).clip(1)), dtype=torch.float32); lossf = nn.CrossEntropyLoss(weight=cw, label_smoothing=0.01)
            else: lossf = nn.MSELoss()
            Xt = torch.tensor(Xi); yt = torch.tensor(y, dtype=torch.long if K > 1 else torch.float32); t0 = time.time()
            for ep in range(E):
                model.train(); perm = rng.permutation(len(y))
                for b in range(0, len(perm), 32):
                    ii = perm[b:b + 32]
                    if len(ii) < 2: continue
                    opt.zero_grad(); out = model(Xt[ii]); loss = lossf(out, yt[ii]) if K > 1 else lossf(out.ravel(), yt[ii]); loss.backward()
                    nn.utils.clip_grad_norm_(model.parameters(), 1.2); opt.step()
                sch.step()
            model.eval()
            with torch.no_grad(): o = model(Xt[:256]); tr_s = float((o.argmax(1).numpy() == y[:256]).mean()) if K > 1 else float(np.sqrt(((o.ravel().numpy() - y[:256]) ** 2).mean()))
            fn = '%s_%s.pt' % ({'A': 'A_detection', 'B': 'B_six_grades', 'C': 'C_severity_score'}[task], net.replace(' ', '_'))
            torch.save(dict(state_dict=model.state_dict(), net=net, task=task, task_description=TASKN[task], features=cols, scaler_mean=mu, scaler_sd=sd, k=k, n_out=K, epochs=E, lr=lr,
                            grades=GRADES, input='pseudo-image k x k (features in order, zero padded)' if net != 'DNN-F1' else 'feature vector', torch=torch.__version__), OUT + 'dl/' + fn)
            rec.append(dict(file='dl/' + fn, task=task, model=net, n_features=len(cols), features=', '.join(cols), epochs=E, lr=lr, pseudo_image_k=k, n_parameters=sum(p.numel() for p in model.parameters())))
            print(task, net, 'epochs', E, '%.0fs' % (time.time() - t0), 'train-subset check %.3f' % tr_s, flush=True)
    tag = sys.argv[3] if len(sys.argv) > 3 else 'all'
    pd.DataFrame(rec).to_csv(OUT + 'dl_models_index_%s.csv' % tag, index=False); print('DL final models saved', tag)
for f in ('wr_features.py', 'wr_networks.py'):
    if os.path.exists(B + f): shutil.copy(B + f, OUT + f)
