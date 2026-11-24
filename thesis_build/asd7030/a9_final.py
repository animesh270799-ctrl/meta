"""Deliverable models of the grouped hold-out design: the SAME models whose accuracy is reported on the held-out test plots.
They were trained on the training plots only (a3_ml.py: SFFS + grid search in GroupKFold(3) by plot, then fit on all training
leaves; a4_dl.py: early stopping on one third of the training plots). Nothing is refitted on the test plots, so the reported
test accuracy is the expected accuracy of exactly these files (hold-out practice: Kuhn and Johnson, 2013; Raschka, 2018).
  python3 a9_final.py ml   -> packs data/ml_models/*.joblib and checks that they reproduce the test predictions
  python3 a9_final.py dl   -> packs data/dl_models/*.pt (PyTorch state dicts) and checks the test predictions"""
import numpy as np, pandas as pd, os, json, sys, shutil, warnings, platform, glob
warnings.filterwarnings('ignore')
from split_cfg import FOLDS, TAG, LABEL
from wr_features import all_features, GRADES
B = os.path.dirname(os.path.abspath(__file__)) + '/'; D = B + 'data/'
OUT = B + '../outputs/ASD_2025-26_70-30_models/'; os.makedirs(OUT + 'ml', exist_ok=True); os.makedirs(OUT + 'dl', exist_ok=True)
M = pd.read_csv(D + 'meta.csv'); S0 = json.load(open(D + 'fold_selection.json'))[str(FOLDS[0])]; SPL = json.load(open(D + 'split.json'))
tr = (M.fold != FOLDS[0]).values; te = ~tr
SEL = dict(ndsi=S0['ndsi'], rsi=S0['rsi'], wri={k: S0['wri'][k] for k in ('l1', 'l2', 'w', 'l3')})
X0 = np.load(D + 'X_leaf.npy').astype(float); wl0 = np.load(D + 'wl.npy')
ALL = all_features(X0, wl0, SEL)
# check: the features computed from raw spectra are identical to the tables used for training and testing
P = np.load(D + 'prep.npz'); Ff = pd.read_csv(D + 'fold%d_indices.csv' % FOLDS[0])
assert np.allclose(ALL[['R%d' % w for w in P['w5']]].values, P['R5'], atol=1e-5) and np.allclose(ALL[Ff.columns].values, Ff.values, rtol=1e-4, atol=1e-6), 'feature mismatch'
SEL.update(OW=S0['OW'], VI=S0['VI'], DSF=S0['DSF'], split=dict(label=LABEL, test_plots=SPL['test_plots'], n_train_leaves=SPL['n_train_leaves'], n_test_leaves=SPL['n_test_leaves']))
json.dump(SEL, open(OUT + 'feature_selection.json', 'w'), indent=1)
enc = {g: i for i, g in enumerate(GRADES)}
def target(task):
    if task == 'A': return M.diseased.values
    if task == 'B': return M.grade.map(enc).values
    return M.grade.values.astype(float)
TASKN = {'A': 'detection (0 = healthy, 1 = diseased)', 'B': 'six severity grades (class index 0-5 = grade 0, 1, 3, 5, 7, 9)', 'C': 'severity score (0-9, regression)'}
FN = {'A': 'A_detection', 'B': 'B_six_grades', 'C': 'C_severity_score'}
MT = pd.read_csv(D + 'metrics_all.csv') if os.path.exists(D + 'metrics_all.csv') else None
def perf(t, m):
    if MT is None: return ''
    r = MT[(MT.task == t) & (MT.model == m)]
    if not len(r): return ''
    r = r.iloc[0]; return ('macro-F1 %.3f' % r.macro_F1 + (', AUC %.3f' % r.AUC if t == 'A' else ', QWK %.3f' % r.QWK)) if t in 'AB' else 'R2 %.3f, RMSE %.2f' % (r.R2, r.RMSE)
TRAINED = '%d leaves of the %d training plots of the %s grouped hold-out split (test plots %s held out), L3/L5/LL, 4 dates (11 Feb - 13 Mar 2026), IARI 2025-26, natural infection' % (
    SPL['n_train_leaves'], SPL['n_train_plots'], LABEL, ', '.join(str(p) for p in SPL['test_plots']))
part = sys.argv[1] if len(sys.argv) > 1 else 'ml'

if part == 'ml':
    import joblib, sklearn, xgboost
    PR = pd.read_csv(D + 'ml_predictions.csv'); rec = []
    for task in 'ABC':
        for fpath in sorted(glob.glob(D + 'ml_models/%s_*.joblib' % task)):
            b = joblib.load(fpath); name = b['model_name']; cols = b['candidate_features']; idx = b['idx']
            Xs = (ALL[cols].values - b['scaler_mean']) / b['scaler_sd']; yp = b['model'].predict(Xs[te][:, idx])
            ref = PR[(PR.task == task) & (PR.model == name)].sort_values('leaf').pred.values
            diff = float(np.mean(np.asarray(yp, float) != ref)) if task in 'AB' else float(np.max(np.abs(np.asarray(yp, float) - ref)))   # share of changed classes / max difference
            assert diff <= (0.002 if task in 'AB' else 1e-3), (task, name, diff)
            fn = '%s_%s.joblib' % (FN[task], name.replace(' ', '_'))
            bundle = dict(model=b['model'], task=task, task_description=TASKN[task], model_name=name, features=b['features'], candidate_features=cols, idx=idx,
                          scaler_mean=b['scaler_mean'], scaler_sd=b['scaler_sd'], grades=GRADES, params=b['params'], inner_cv_score=b['inner_cv_score'], scoring=b['scoring'],
                          trained_on=TRAINED, test_performance='%s test plots: %s' % (LABEL, perf(task, name)),
                          versions=dict(sklearn=sklearn.__version__, xgboost=xgboost.__version__, python=platform.python_version()))
            joblib.dump(bundle, OUT + 'ml/' + fn, compress=3)
            rec.append(dict(file='ml/' + fn, task=task, model=name, n_features=len(idx), features=', '.join(b['features']), params=json.dumps(b['params'], default=str),
                            inner_cv_score=round(float(b['inner_cv_score']), 4), scoring=b['scoring'], test_performance=perf(task, name), check_max_diff=diff))
            print(task, name, len(idx), 'features; reproduces the test predictions (max diff %.1e)' % diff, flush=True)
    pd.DataFrame(rec).to_csv(OUT + 'ml_models_index.csv', index=False); print('ML models saved', len(rec))

if part == 'dl':
    import torch
    import wr_networks as NW
    R = {(r['net'], r['task']): r for r in json.load(open(D + 'dl_main.json'))}; rec = []
    for task in 'ABC':
        for net in ['DNN-F1', 'DT-EDNet', 'EfficientNet-B0', 'ResNet18', 'ConvNeXt V2-Atto']:
            fpath = D + 'dl_models/%s_%s.pt' % (task, net.replace(' ', '_'))
            if not os.path.exists(fpath): print('missing', fpath); continue
            b = torch.load(fpath, map_location='cpu', weights_only=False); cols = b['features']
            X = ((ALL[cols].values.astype(np.float32) - b['scaler_mean']) / b['scaler_sd']).astype(np.float32)
            Xi = X.reshape(-1, 1, 1, X.shape[1]) if net == 'DNN-F1' else NW.pseudo(X)[0]
            model = NW.build(net, b['k'], len(cols), b['n_out'], 0.03); model.load_state_dict(b['state_dict']); model.eval()
            with torch.no_grad(): o = model(torch.tensor(Xi[te])).numpy()
            yp = o.argmax(1) if b['n_out'] > 1 else o.ravel(); ref = np.array(R[(net, task)]['pred'])
            diff = float(np.mean(yp != ref)) if task in 'AB' else float(np.max(np.abs(yp - ref))); assert diff <= (0.002 if task in 'AB' else 1e-3), (task, net, diff)
            fn = '%s_%s.pt' % (FN[task], net.replace(' ', '_'))
            torch.save(dict(state_dict=b['state_dict'], net=net, task=task, task_description=TASKN[task], features=cols, scaler_mean=b['scaler_mean'], scaler_sd=b['scaler_sd'], k=b['k'],
                            n_out=b['n_out'], epochs=b['best_epoch'], epochs_trained=b['epochs_trained'], lr=b['lr'], grades=GRADES, trained_on=TRAINED, early_stopping_plots=b['val_plots'],
                            test_performance='%s test plots: %s' % (LABEL, perf(task, net)),
                            input='pseudo-image k x k (features in order, zero padded)' if net != 'DNN-F1' else 'feature vector', torch=torch.__version__), OUT + 'dl/' + fn)
            rec.append(dict(file='dl/' + fn, task=task, model=net, n_features=len(cols), features=', '.join(cols), epochs=b['best_epoch'], lr=b['lr'], pseudo_image_k=b['k'],
                            n_parameters=sum(p.numel() for p in model.parameters()), test_performance=perf(task, net), check_max_diff=diff))
            print(task, net, 'best epoch', b['best_epoch'], 'reproduces the test predictions (max diff %.1e)' % diff, flush=True)
    pd.DataFrame(rec).to_csv(OUT + 'dl_models_index_all.csv', index=False); print('DL models saved', len(rec))
for f in ('wr_features.py', 'wr_networks.py'):
    if os.path.exists(B + f): shutil.copy(B + f, OUT + f)
