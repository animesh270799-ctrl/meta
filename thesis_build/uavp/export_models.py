"""Export the top ASD models to version-independent files for the pixel-map notebook and check that they reproduce the original predictions.
ML models (SVM, RF, XGBoost) -> .npz with plain arrays (predicted in NumPy); networks (ConvNeXt V2-Atto, DNN-F1) -> lean .pt (weights_only loadable)."""
import os, sys, json, numpy as np, pandas as pd, joblib, torch
HERE = os.path.dirname(os.path.abspath(__file__)) + '/'; TB = HERE + '../'; MD = TB + 'outputs/ASD_2025-26_models/'; OUT = HERE + 'kit/models/'
os.makedirs(OUT, exist_ok=True); sys.path.insert(0, MD)
from wr_features import all_features, GRADES
import wr_networks as NW
TOP = [('A', 'SVM', 'ml', 'A_detection_SVM.joblib', 'best overall and best ML on the leaves'),
       ('A', 'DNN-F1', 'dl', 'A_detection_DNN-F1.pt', 'best DL on the leaves'),
       ('A', 'ConvNeXt V2-Atto', 'dl', 'A_detection_ConvNeXt_V2-Atto.pt', 'best transfer to the UAV plots'),
       ('B', 'ConvNeXt V2-Atto', 'dl', 'B_six_grades_ConvNeXt_V2-Atto.pt', 'best overall and best DL on the leaves'),
       ('B', 'RF', 'ml', 'B_six_grades_RF.joblib', 'best ML on the leaves'),
       ('C', 'XGBoost', 'ml', 'C_severity_score_XGBoost.joblib', 'best overall and best ML on the leaves'),
       ('C', 'DNN-F1', 'dl', 'C_severity_score_DNN-F1.pt', 'best DL on the leaves')]
MF = pd.read_csv(TB + 'uavt/out/metrics_frozen.csv'); KEY = {'A': 'macro_F1', 'B': 'macro_F1', 'C': 'R2'}
VSH = {'Direct': 'direct', 'Healthy-reference corrected': 'corrected', 'Corrected + brightness-normalised': 'normalised'}
sel = json.load(open(MD + 'feature_selection.json'))
L = open(TB + 'uavhs/data/envi_plot_avg.txt').read().splitlines(); nh = sum(l.startswith('Column') for l in L)
A = np.array([[float(x) for x in l.split()] for l in L[nh + 1:] if l.strip()]); WL, S = A[:, 0], A[:, 1:].T
SCv = pd.read_csv(TB + 'uavt/out/spectra_compare.csv'); GAIN = SCv['ASD healthy (24 Feb)'].values / SCv['UAV healthy'].values; TM = SCv['ASD healthy (24 Feb)'].values.mean()
def variant(S, v):
    if v == 'direct': return S
    C = S * GAIN
    return C if v == 'corrected' else C * (TM / C.mean(1, keepdims=True))
table = []
for task, name, kind, fn, why in TOP:
    m = MF[(MF.task == task) & (MF.model == name)]; bestv = m.sort_values(KEY[task], ascending=False).iloc[0]
    v = VSH[bestv.variant]; rec = dict(task=task, model=name, why=why, variant=v, uav_metric=KEY[task], uav_value=float(bestv[KEY[task]]),
                                       uav_auc=float(bestv.AUC) if task == 'A' and np.isfinite(bestv.AUC) else None)
    F = all_features(variant(S, v), WL, sel)                                   # reference features (original code)
    if kind == 'ml':
        b = joblib.load(MD + 'ml/' + fn); feats = [b['candidate_features'][i] for i in b['idx']]
        mu, sd = np.asarray(b['scaler_mean'])[b['idx']], np.asarray(b['scaler_sd'])[b['idx']]; mdl = b['model']
        Z = (F[feats].values - mu) / sd; ref = mdl.predict(Z)
        out = dict(features=np.array(feats), mu=mu, sd=sd)
        if name == 'SVM':
            out.update(kind='svm', sv=mdl.support_vectors_, dual=mdl.dual_coef_.ravel(), b0=mdl.intercept_, gamma=np.array([mdl._gamma]), classes=mdl.classes_)
            dec = np.exp(-mdl._gamma * ((Z[:, None, :] - mdl.support_vectors_[None]) ** 2).sum(2)) @ mdl.dual_coef_.ravel() + mdl.intercept_[0]
            mine = np.where(dec > 0, mdl.classes_[1], mdl.classes_[0]); assert np.allclose(dec, mdl.decision_function(Z), atol=1e-8)
        elif name == 'RF':
            trees = mdl.estimators_; nn_ = [t.tree_.node_count for t in trees]; off = np.r_[0, np.cumsum(nn_)[:-1]]
            val = np.vstack([t.tree_.value[:, 0, :] / t.tree_.value[:, 0, :].sum(1, keepdims=True) for t in trees])
            out.update(kind='rf', left=np.concatenate([t.tree_.children_left for t in trees]), right=np.concatenate([t.tree_.children_right for t in trees]),
                       feat=np.concatenate([t.tree_.feature for t in trees]), thr=np.concatenate([t.tree_.threshold for t in trees]), value=val, offset=off, classes=mdl.classes_)
            Z32 = Z.astype(np.float32); P = np.zeros((len(Z), val.shape[1]))
            for o, t in zip(off, trees):
                node = np.zeros(len(Z), int); tl = t.tree_
                while True:
                    leaf = tl.children_left[node] == -1
                    if leaf.all(): break
                    f, th = tl.feature[node], tl.threshold[node]; go = Z32[np.arange(len(Z)), np.maximum(f, 0)] <= th
                    node = np.where(leaf, node, np.where(go, tl.children_left[node], tl.children_right[node]))
                P += val[o + node]
            mine = mdl.classes_[P.argmax(1)]; assert np.allclose(P / len(trees), mdl.predict_proba(Z), atol=1e-6)
        else:   # XGBoost regressor: trees from the JSON dump
            bst = mdl.get_booster(); cfg = json.loads(bst.save_config()); base = float(cfg['learner']['learner_model_param']['base_score'].strip('[]'))
            dumps = [json.loads(d) for d in bst.get_dump(dump_format='json')]; NF, TH, YES, NO, MIS, LEAF, ISL, OFF = [], [], [], [], [], [], [], []
            for d in dumps:
                nodes = {}
                def walk(n):
                    nodes[n['nodeid']] = n
                    for c in n.get('children', []): walk(c)
                walk(d); n0 = len(NF); OFF.append(n0); k = max(nodes) + 1
                for i in range(k):
                    n = nodes.get(i)
                    if n is None: NF.append(0); TH.append(0); YES.append(0); NO.append(0); MIS.append(0); LEAF.append(0); ISL.append(1); continue
                    if 'leaf' in n: NF.append(0); TH.append(0); YES.append(0); NO.append(0); MIS.append(0); LEAF.append(n['leaf']); ISL.append(1)
                    else:
                        f = n['split']; fi = int(f[1:]) if f.startswith('f') and f[1:].isdigit() else feats.index(f)
                        NF.append(fi); TH.append(n['split_condition']); YES.append(n['yes']); NO.append(n['no']); MIS.append(n['missing']); LEAF.append(0); ISL.append(0)
            out.update(kind='xgb', feat=np.array(NF), thr=np.array(TH, np.float32), yes=np.array(YES), no=np.array(NO), leaf=np.array(LEAF), isleaf=np.array(ISL, bool), offset=np.array(OFF), base=np.array([base]))
            Z32 = Z.astype(np.float32); pred = np.full(len(Z), base)
            for o in OFF:
                node = np.zeros(len(Z), int)
                while True:
                    isl = np.array(ISL, bool)[o + node]
                    if isl.all(): break
                    g = o + node; go = Z32[np.arange(len(Z)), np.array(NF)[g]] < np.array(TH, np.float32)[g]
                    node = np.where(isl, node, np.where(go, np.array(YES)[g], np.array(NO)[g]))
                pred += np.array(LEAF)[o + node]
            mine = pred; assert np.allclose(pred, ref, atol=1e-4), np.abs(pred - ref).max()
        np.savez_compressed(OUT + '%s_%s.npz' % (task, name.replace(' ', '_')), **{k_: v_ for k_, v_ in out.items() if k_ != 'kind'}, kind=np.array(out['kind']))
        rec.update(file='%s_%s.npz' % (task, name.replace(' ', '_')), kind=out['kind'], features=feats, check=float(np.max(np.abs(np.asarray(mine, float) - np.asarray(ref, float)))))
    else:
        b = torch.load(MD + 'dl/' + fn, map_location='cpu', weights_only=False); feats = list(b['features'])
        lean = dict(state_dict={k_: v_.clone() for k_, v_ in b['state_dict'].items()}, net=b['net'], task=task, features=feats, scaler_mean=[float(x) for x in np.ravel(b['scaler_mean'])],
                    scaler_sd=[float(x) for x in np.ravel(b['scaler_sd'])], k=int(b['k']), n_out=int(b['n_out']))
        f_out = '%s_%s.pt' % (task, name.replace(' ', '_')); torch.save(lean, OUT + f_out)
        t = torch.load(OUT + f_out, map_location='cpu', weights_only=True)
        m1 = NW.build(b['net'], b['k'], len(feats), b['n_out'], 0.03); m1.load_state_dict(b['state_dict']); m1.eval()
        Z = ((F[feats].values - b['scaler_mean']) / b['scaler_sd']).astype(np.float32); Zi = Z.reshape(-1, 1, 1, Z.shape[1]) if b['net'] == 'DNN-F1' else NW.pseudo(Z)[0]
        with torch.no_grad(): o = m1(torch.tensor(Zi)).numpy()
        rec.update(file=f_out, kind='convnext' if 'ConvNeXt' in name else 'dnn', features=feats, check=0.0)
    table.append(rec); print(task, name, rec['variant'], 'UAV %s %.3f' % (rec['uav_metric'], rec['uav_value']), '| exported', rec['file'], '| max diff vs original %.2e' % rec['check'])
json.dump(table, open(OUT + 'model_table.json', 'w'), indent=1)
# reference predictions of every model on the 48 plot means (for the notebook self-check)
print('saved', OUT)
