"""STEP 5 (D1-D12): Objective 1 on ALL leaves = description of the disease signal. Its feature lists are NOT given to the models (Step 6 repeats the chain on TRAIN)."""
import os, json, numpy as np, pandas as pd
import matplotlib; matplotlib.use('Agg'); import matplotlib.pyplot as plt
from sklearn.decomposition import PCA
import config as C
from lib_select import select_chain, r2_maps, feature_table, jm_distance
O = C.OUT; M = pd.read_csv(os.path.join(O, '03_meta_split.csv')); Z = np.load(os.path.join(O, '04_spectra.npz')); S = {k: Z[k] for k in Z.files}
F44 = pd.read_csv(os.path.join(O, '04_indices.csv')); CR = pd.read_csv(os.path.join(O, '04_continuum.csv')); W = np.load(os.path.join(O, '04_cwt.npy'))
y = M.grade.values.astype(float); w5 = S['w5']; log = open(os.path.join(O, '05_obj1_log.txt'), 'w')
def L(*a): print(*a); print(*a, file=log)
# D1 mean +- SD spectra and difference from grade 0; D2 correlation curves
rows = []
for g in C.GRADES:
    m = M.grade.values == g; rows.append(pd.DataFrame({'wl': w5, 'grade': g, 'R_mean': S['R5'][m].mean(0), 'R_sd': S['R5'][m].std(0), 'FD_mean': S['FD5'][m].mean(0),
                                                       'R_minus_healthy': S['R5'][m].mean(0) - S['R5'][M.grade.values == 0].mean(0)}))
pd.concat(rows).to_csv(os.path.join(O, '05_D1_mean_spectra.csv'), index=False)
rc = lambda A: np.array([np.corrcoef(A[:, j], y)[0, 1] for j in range(A.shape[1])])
cc = pd.DataFrame({'wl': w5, 'r_R': rc(S['R5']), 'r_FD': rc(S['FD5'])}); cc.to_csv(os.path.join(O, '05_D2_correlation.csv'), index=False)
# D3 strata
st = [dict(factor=f, level=k, n=len(d), mean_grade=d.grade.mean(), pct_diseased=100 * d.diseased.mean()) for f in ('stage', 'variety', 'leaf', 'date', 'timing') for k, d in M.groupby(f)]
pd.DataFrame(st).to_csv(os.path.join(O, '05_D3_strata.csv'), index=False)
# D4-D10 the selection chain on ALL leaves
sel = select_chain(np.ones(len(M), bool), S, F44, CR, W, M, log=L)
# D11 JM distance between grades on the task-B DSF; D12 PCA
T = feature_table(sel, S, F44, CR, W); Xb = T[sel['DSF']['B']].values; Xb = (Xb - Xb.mean(0)) / Xb.std(0)
sel['JM'] = jm_distance(Xb, M.grade.values); L('D11 JM distances:', {k: round(v, 3) for k, v in sel['JM'].items()})
Rz = (S['R5'] - S['R5'].mean(0)) / S['R5'].std(0); pca = PCA(5).fit(Rz); sel['PCA_var'] = pca.explained_variance_ratio_.tolist()
pd.DataFrame(pca.transform(Rz)[:, :3], columns=['PC1', 'PC2', 'PC3']).assign(grade=M.grade).to_csv(os.path.join(O, '05_D12_pca_scores.csv'), index=False)
json.dump(sel, open(os.path.join(O, '05_obj1_selection.json'), 'w'), indent=1, default=float)
# figures
fig, ax = plt.subplots(1, 2, figsize=(12, 4)); D1 = pd.concat(rows)
for g in C.GRADES:
    d = D1[D1.grade == g]; ax[0].plot(d.wl, d.R_mean, label='grade %d' % g); ax[1].plot(d.wl, d.FD_mean * 1000)
ax[0].set_xlabel('nm'); ax[0].set_ylabel('reflectance'); ax[0].legend(); ax[1].set_xlim(500, 800); ax[1].set_xlabel('nm'); ax[1].set_ylabel('first derivative (x1000)')
fig.tight_layout(); fig.savefig(os.path.join(O, '05_D1_mean_spectra.png'), dpi=150); plt.close(fig)
fig, ax = plt.subplots(figsize=(8, 3.5)); ax.plot(w5, cc.r_R, label='reflectance'); ax.plot(w5, cc.r_FD, label='first derivative'); ax.axhline(0, color='k', lw=0.5)
ax.set_xlabel('nm'); ax.set_ylabel('r with grade'); ax.legend(); fig.tight_layout(); fig.savefig(os.path.join(O, '05_D2_correlation.png'), dpi=150); plt.close(fig)
N, Sm = r2_maps(S['R5'], y); fig, ax = plt.subplots(1, 2, figsize=(12, 5))
for a, Mp, t in ((ax[0], N, 'NDSI'), (ax[1], Sm, 'RSI')):
    im = a.imshow(np.nan_to_num(Mp.T, nan=0), origin='lower', extent=[w5[0], w5[-1], w5[0], w5[-1]], cmap='viridis'); a.set_title('R² of %s with grade' % t); plt.colorbar(im, ax=a)
fig.tight_layout(); fig.savefig(os.path.join(O, '05_D4_maps.png'), dpi=150); plt.close(fig)
print('CHECK: outputs 05_*.csv, 05_*.png and 05_obj1_selection.json written; DSF sizes', {t: len(sel['DSF'][t]) for t in 'ABC'})
