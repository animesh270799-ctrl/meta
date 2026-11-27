"""Objective 1 on the pooled leaf data (descriptive, all 2339 leaves): response curves, correlation curves, NDSI/RSI maps,
effective ranges, SHAP-CARS optimal wavelengths, best NDSI/RSI, White Rust Index, index filter + ReliefF/RReliefF, VIF, PCA."""
import numpy as np, pandas as pd, os, json, time
from alib import *
from sklearn.decomposition import PCA
D = os.path.dirname(os.path.abspath(__file__)) + '/data/'
P = np.load(D + 'prep.npz'); wl, w5, R1, FD1, R5, FD5 = P['wl'], P['w5'], P['R1'], P['FD1'], P['R5'], P['FD5']
M = pd.read_csv(D + 'meta.csv'); F = pd.read_csv(D + 'indices.csv'); y = M.grade.values.astype(float); grades = [0, 1, 3, 5, 7, 9]
out = {}; t0 = time.time()
# 1.1.1 mean spectra and first derivative by grade
ms = pd.DataFrame({'wl': w5}); fs = pd.DataFrame({'wl': w5})
for g in grades:
    m = M.grade.values == g
    ms['mean_%d' % g] = R5[m].mean(0); ms['sd_%d' % g] = R5[m].std(0); fs['mean_%d' % g] = FD5[m].mean(0) * 1000
ms.to_csv(D + 'o1_mean_spectra.csv', index=False); fs.to_csv(D + 'o1_mean_fd.csv', index=False)
# 1.1.2 correlation curves (Pearson r with the leaf score) for reflectance and first derivative (5 nm)
rc = lambda A: np.array([np.corrcoef(A[:, j], y)[0, 1] for j in range(A.shape[1])])
cc = pd.DataFrame({'wl': w5, 'r_R': rc(R5), 'r_FD': rc(FD5)}); cc.to_csv(D + 'o1_corr_curves.csv', index=False)
out['corr_R_max'] = cc.loc[cc.r_R.abs().idxmax(), ['wl', 'r_R']].tolist(); out['corr_FD_max'] = cc.loc[cc.r_FD.abs().idxmax(), ['wl', 'r_FD']].tolist()
# 1.1.3 response by stage, variety, leaf position and date (mean score and NDVI/ARI/PSRI as examples) -> table
grp = []
for col in ['stage', 'variety', 'leaf', 'date', 'timing', 'block']:
    for k, d in M.groupby(col):
        grp.append(dict(factor=col, level=k, n=len(d), mean_score=d.grade.mean(), pct_diseased=100 * d.diseased.mean()))
pd.DataFrame(grp).to_csv(D + 'o1_strata.csv', index=False)
print('1.1 done %.0fs' % (time.time() - t0))
# 1.2.1 NDSI / RSI R² maps on 5-nm reflectance (all 80 200 pairs), effective ranges
Nm, Sm = r2_maps(R5, y); np.save(D + 'o1_ndsi_r2.npy', Nm.astype(np.float32)); np.save(D + 'o1_rsi_r2.npy', Sm.astype(np.float32))
used, thr = effective_ranges(Nm, Sm, w5)
out['eff_thr'] = float(thr); out['eff_nbands'] = int(used.sum())
# contiguous ranges for reporting
rng = []; s = None
for i, u in enumerate(used):
    if u and s is None: s = i
    if (not u or i == len(used) - 1) and s is not None: e = i if u else i - 1; rng.append((int(w5[s]), int(w5[e]))); s = None
out['eff_ranges'] = rng
out['best_ndsi'] = best_pair(Nm, w5); out['best_rsi'] = best_pair(Sm, w5)
print('1.2.1 done %.0fs' % (time.time() - t0), out['eff_thr'], out['eff_nbands'], out['best_ndsi'], out['best_rsi'])
# 1.2.2-1.2.4 SHAP-CARS on reflectance + first derivative inside the effective ranges + red-edge FD (680-760 nm)
re = (w5 >= 680) & (w5 <= 760)
candR = np.where(used)[0]; candF = np.where(used | re)[0]
Xc = np.hstack([R5[:, candR], FD5[:, candF]]); names = ['R%d' % w5[i] for i in candR] + ['FD%d' % w5[i] for i in candF]
sc = shap_cars(Xc, y, names, runs=20, n_iter=50, seed=42)
OW = sc['names']; out['OW'] = OW; out['OW_n_R'] = sum(n.startswith('R') for n in OW); out['OW_n_FD'] = sum(n.startswith('FD') for n in OW); out['cars_ncomp'] = sc['ncomp']
pd.DataFrame({'feature': [names[t] for t in sc['top']], 'mean_abs_shap': sc['imp'][sc['top']], 'cars_freq': sc['freq']}).to_csv(D + 'o1_shapcars.csv', index=False)
pd.DataFrame({'feature': names, 'mean_abs_shap': sc['imp']}).to_csv(D + 'o1_shap_all.csv', index=False)
pd.DataFrame([(h[0], h[1], h[2]) for h in sc['hist']], columns=['iteration', 'n_vars', 'rmsecv']).to_csv(D + 'o1_cars_hist.csv', index=False)
pd.DataFrame({'ncomp': np.arange(1, len(sc['mccv']) + 1), 'rmse': sc['mccv']}).to_csv(D + 'o1_mccv.csv', index=False)
OWX = pd.DataFrame(np.hstack([R5, FD5]), columns=['R%d' % w for w in w5] + ['FD%d' % w for w in w5])[OW]
print('1.2 SHAP-CARS done %.0fs' % (time.time() - t0), OW)
# 1.3 best NDSI, RSI and the White Rust Index
a, b, _ = out['best_ndsi']; c, d, _ = out['best_rsi']
g = lambda lam: R1[:, int(round(lam - 400))]
F['NDSI_best'] = (g(a) - g(b)) / (g(a) + g(b)); F['RSI_best'] = g(c) / g(d)
cand = wri_search(R5, w5, y, Nm)
wbest = cand[0]; out['WRI'] = dict(l1=wbest[2], l2=wbest[3], w=wbest[4], l3=wbest[5], r=float(wbest[1]))
F['WRI'] = wri_values(R1, wl, wbest[2], wbest[3], wbest[4], wbest[5])
pd.DataFrame(cand[:30], columns=['abs_r', 'r', 'l1', 'l2', 'w', 'l3']).to_csv(D + 'o1_wri_top.csv', index=False)
print('1.3 done', out['WRI'])
# 1.4 index group: redundancy filter |r| >= 0.95 -> ReliefF (6 classes), ReliefF (binary), RReliefF (score)
kept = corr_filter(F, y, 0.95); out['idx_kept'] = kept
grpid = M['plot'].values
W6 = relieff(F[kept].values, M.grade.values, grpid, k=10); W2 = relieff(F[kept].values, M.diseased.values, grpid, k=10); WR = relieff(F[kept].values, y, grpid, k=10, regression=True)
rel = pd.DataFrame({'index': kept, 'ReliefF_classes': W6, 'ReliefF_binary': W2, 'RReliefF_score': WR, 'r_score': [np.corrcoef(F[k], y)[0, 1] for k in kept]})
rel.to_csv(D + 'o1_relief.csv', index=False)
VI6 = list(rel.sort_values('ReliefF_classes', ascending=False)['index'][:5]); VI2 = list(rel.sort_values('ReliefF_binary', ascending=False)['index'][:5]); VIR = list(rel.sort_values('RReliefF_score', ascending=False)['index'][:5])
out['VI_classes'] = VI6; out['VI_binary'] = VI2; out['VI_score'] = VIR
print('1.4 done', VI6, VIR)
# index correlation matrix (for the heat map)
F[kept].corr().to_csv(D + 'o1_index_corr.csv')
# 1.6 VIF across groups (OW + indices selected for classes) -> disease-specific feature set
pool = pd.concat([OWX, F[sorted(set(VI6) | set(VIR))]], axis=1)
dsf, vif_final, vif_hist = vif_filter(pool, 10.0); out['DSF'] = dsf; out['VIF_final'] = vif_final; out['VIF_removed'] = vif_hist
print('1.6 done', dsf)
# PCA score plot data
Z = (R5 - R5.mean(0)) / R5.std(0); pca = PCA(5).fit(Z); S = pca.transform(Z)
pd.DataFrame({'PC1': S[:, 0], 'PC2': S[:, 1], 'grade': M.grade}).to_csv(D + 'o1_pca.csv', index=False); out['pca_var'] = pca.explained_variance_ratio_.tolist()
F.to_csv(D + 'indices_full.csv', index=False)
json.dump(out, open(D + 'o1_results.json', 'w'), indent=1, default=float)
print('Objective 1 finished %.0fs' % (time.time() - t0))
