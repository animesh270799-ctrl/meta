"""Objective 2, Step 2.1.2: feature selection repeated inside the training part of every leave-one-replication-out fold
(effective ranges -> SHAP-CARS; best NDSI/RSI and WRI; redundancy filter -> ReliefF / RReliefF; VIF)."""
import numpy as np, pandas as pd, os, json, time, sys
from split_cfg import FOLDS, TAG, LABEL
from alib import *
D = os.path.dirname(os.path.abspath(__file__)) + '/data/'
P = np.load(D + 'prep.npz'); wl, w5, R1, FD1, R5, FD5 = P['wl'], P['w5'], P['R1'], P['FD1'], P['R5'], P['FD5']
M = pd.read_csv(D + 'meta.csv'); F0 = pd.read_csv(D + 'indices.csv')
BANDS = pd.DataFrame(np.hstack([R5, FD5]), columns=['R%d' % w for w in w5] + ['FD%d' % w for w in w5])
g = lambda lam: R1[:, int(round(lam - 400))]
res = {}
for f in FOLDS:
    t0 = time.time(); tr = (M.fold != f).values; y = M.grade.values.astype(float)
    Nm, Sm = r2_maps(R5[tr], y[tr]); used, thr = effective_ranges(Nm, Sm, w5)
    re = (w5 >= 680) & (w5 <= 760); candR = np.where(used)[0]; candF = np.where(used | re)[0]
    Xc = np.hstack([R5[tr][:, candR], FD5[tr][:, candF]]); names = ['R%d' % w5[i] for i in candR] + ['FD%d' % w5[i] for i in candF]
    sc = shap_cars(Xc, y[tr], names, runs=20, n_iter=50, seed=42 + f)
    a, b, _ = best_pair(Nm, w5); c, d, _ = best_pair(Sm, w5); wr = wri_search(R5[tr], w5, y[tr], Nm)[0]
    F = F0.copy(); F['NDSI_best'] = (g(a) - g(b)) / (g(a) + g(b)); F['RSI_best'] = g(c) / g(d); F['WRI'] = wri_values(R1, wl, wr[2], wr[3], wr[4], wr[5])
    kept = corr_filter(F[tr].reset_index(drop=True), y[tr], 0.95)
    grp = M['plot'].values[tr]
    W6 = relieff(F[kept].values[tr], M.grade.values[tr], grp); W2 = relieff(F[kept].values[tr], M.diseased.values[tr], grp); WR = relieff(F[kept].values[tr], y[tr], grp, regression=True)
    top = lambda W: [kept[i] for i in np.argsort(-W)[:5]]
    VI = {'A': top(W2), 'B': top(W6), 'C': top(WR)}
    DSF = {}
    for t in 'ABC':
        pool = pd.concat([BANDS[sc['names']], F[VI[t]]], axis=1)[tr]
        DSF[t] = vif_filter(pool, 10.0)[0]
    F.to_csv(D + 'fold%d_indices.csv' % f, index=False)
    res[f] = dict(eff_thr=float(thr), eff_n=int(used.sum()), OW=sc['names'], cars_freq={names[sc['top'][i]]: float(sc['freq'][i]) for i in range(len(sc['top'])) if sc['freq'][i] > 0},
                  ndsi=[a, b], rsi=[c, d], wri=dict(l1=wr[2], l2=wr[3], w=wr[4], l3=wr[5], r=float(wr[1])), kept=kept, VI=VI, DSF=DSF)
    print('fold', f, 'done %.0fs' % (time.time() - t0), sc['names'], VI, DSF, flush=True)
json.dump(res, open(D + 'fold_selection.json', 'w'), indent=1, default=float)
