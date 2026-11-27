"""STEP L6 check (as Step 2.3): stability of the SFFS selection for the best ML model of each task (Tian et al., 2021).
SFFS (same settings as L6) is repeated over N random GroupKFold(3) divisions of the 33 training plots; the selection frequency of every DSF feature
and the distribution of the number of features are reported. N = 100 (methodology); see the log for the run time."""
import os, sys, glob, json, time, warnings, numpy as np, pandas as pd
warnings.filterwarnings('ignore')
from mlxtend.feature_selection import SequentialFeatureSelector as SFS
import configL as C
from lmods import base
O = C.OUT; M = pd.read_csv(os.path.join(O, 'L2_meta.csv')); ALL = pd.read_csv(os.path.join(O, 'L5_all_features.csv')); SEL = json.load(open(os.path.join(O, 'L5_selection.json')))
BM = json.load(open(os.path.join(O, 'L7_best.json')))['best_ml']; N = int(sys.argv[1]) if len(sys.argv) > 1 else 50; N_RF = int(sys.argv[2]) if len(sys.argv) > 2 else 20   # run time (DEV-6): 50 divisions for SVM/k-NN/PLS, 20 with 100 trees for RF (methodology: 100)
tr = (M.split == 'TRAIN').values; pl = M['plot'].values[tr]; up = np.unique(pl)
Y = {'A': M.diseased.values.astype(int), 'B': M.grade.map({g: i for i, g in enumerate(C.GRADES)}).values.astype(int), 'C': M.grade.values.astype(float)}
SC = {'A': 'f1_macro', 'B': 'f1_macro', 'C': 'neg_root_mean_squared_error'}; rows, freq = [], []
CK = os.path.join(O, 'L6_stability_ckpt.csv'); done = pd.read_csv(CK).to_dict('records') if os.path.isfile(CK) else []
for task in 'ABC':
    model = BM[task]; cols = SEL['DSF'][task]; X = ALL[cols].values[tr]; y = Y[task][tr]; rng = np.random.default_rng(C.SEED + 1); t0 = time.time()
    est = base(model, task)
    if model == 'RF': est.set_params(n_estimators=100)          # cost reduction for the repeated runs only (documented)
    NN = N_RF if model == 'RF' else N
    for rep in range(NN):
        g = rng.permutation(up)
        prev = [d for d in done if d['task'] == task and d['repeat'] == rep + 1]
        if prev: rows.append(prev[0]); continue
        fold = {q: i % 3 for i, q in enumerate(g)}; f = np.array([fold[q] for q in pl]); spl = [(np.where(f != k)[0], np.where(f == k)[0]) for k in range(3)]
        s = SFS(est, k_features=(1, min(C.SFFS_MAX, len(cols))), forward=True, floating=True, scoring=SC[task], cv=spl, n_jobs=(1 if model == 'RF' else 4)).fit(X, y)
        rows.append(dict(task=task, model=model, repeat=rep + 1, n_features=len(s.k_feature_idx_), cv_score=float(s.k_score_), features=' '.join(cols[i] for i in s.k_feature_idx_)))
        pd.DataFrame(rows).to_csv(CK, index=False)
    D = pd.DataFrame([r for r in rows if r['task'] == task]); MS = pd.concat([pd.read_csv(f) for f in glob.glob(os.path.join(O, 'L6_ml_summary_*.csv'))]); main = set(MS[(MS.task == task) & (MS.model == model)].sffs_features.iloc[0].split())
    for c in cols: freq.append(dict(task=task, model=model, feature=c, frequency=float(D.features.str.split().apply(lambda z: c in z).mean()), in_main_SFFS=c in main))
    print('task %s %s: %d repeats, median %d features, %.0fs' % (task, model, NN, D.n_features.median(), time.time() - t0), flush=True)
pd.DataFrame(rows).to_csv(os.path.join(O, 'L6_stability_runs.csv'), index=False); pd.DataFrame(freq).to_csv(os.path.join(O, 'L6_stability_frequency.csv'), index=False)
print(pd.DataFrame(freq).sort_values(['task', 'frequency'], ascending=[True, False]).round(2).to_string(index=False))
