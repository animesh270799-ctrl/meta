"""STEP L5.1 - leaf response on ALL leaves (description only): mean +- SD spectra and first derivatives of each grade, % difference from grade 0,
Pearson r of every 5-nm band and index with the grade, the same by leaf position, growth stage, variety and date.  STEP L5.7 - PCA of standardised 5-nm reflectance."""
import os, json, numpy as np, pandas as pd
from sklearn.decomposition import PCA
import configL as C
M = pd.read_csv(os.path.join(C.OUT, 'L2_meta.csv')); S = np.load(os.path.join(C.OUT, 'L3_spectra.npz')); F = pd.read_csv(os.path.join(C.OUT, 'L4_indices.csv'))
w5, R5, FD5 = S['w5'], S['R5'], S['FD5']; g = M.grade.values
def rcurve(A, y):
    Ac = (A - A.mean(0)) / (A.std(0) + 1e-15); yc = (y - y.mean()) / y.std(); return yc @ Ac / len(y)
D = pd.DataFrame({'wavelength': w5})
for G in C.GRADES:
    k = g == G; D['R_mean_g%d' % G] = R5[k].mean(0); D['R_sd_g%d' % G] = R5[k].std(0, ddof=1); D['FD_mean_g%d' % G] = FD5[k].mean(0)
for G in C.GRADES[1:]: D['diff_pct_g%d' % G] = (D['R_mean_g%d' % G] - D['R_mean_g0']) / D['R_mean_g0'] * 100
D['r_R'] = rcurve(R5, g.astype(float)); D['r_FD'] = rcurve(FD5, g.astype(float)); D.to_csv(os.path.join(C.OUT, 'L5_1_spectra_by_grade.csv'), index=False)
ri = F.corrwith(pd.Series(g, dtype=float)).rename('r_with_grade'); ri.to_frame().assign(abs_r=ri.abs()).sort_values('abs_r', ascending=False).to_csv(os.path.join(C.OUT, 'L5_1_index_r.csv'))
idx_g = F.groupby(g).mean().T; idx_g.columns = ['mean_g%d' % c for c in idx_g.columns]; idx_g.to_csv(os.path.join(C.OUT, 'L5_1_index_means_by_grade.csv'))
strata = {'leaf': 'Leaf position', 'stage': 'Growth stage', 'variety': 'Variety', 'date': 'Date'}; SR = pd.DataFrame({'wavelength': w5}); counts = []
for col, lab in strata.items():
    for v in sorted(M[col].unique()):
        k = (M[col] == v).values
        SR['r_R|%s=%s' % (col, v)] = rcurve(R5[k], g[k].astype(float)); SR['r_FD|%s=%s' % (col, v)] = rcurve(FD5[k], g[k].astype(float))
        c = dict(stratum=lab, level=v, leaves=int(k.sum()), mean_grade=float(g[k].mean())); c.update({'grade %d' % G: int((g[k] == G).sum()) for G in C.GRADES})
        c['max |r| R'] = float(np.abs(SR['r_R|%s=%s' % (col, v)]).max()); c['max |r| FD'] = float(np.abs(SR['r_FD|%s=%s' % (col, v)]).max()); c['REP grade0'] = float(F.REP[k & (g == 0)].mean()) if (k & (g == 0)).any() else np.nan
        c['REP grade>=5'] = float(F.REP[k & (g >= 5)].mean()) if (k & (g >= 5)).any() else np.nan; counts.append(c)
SR.to_csv(os.path.join(C.OUT, 'L5_1_r_by_stratum.csv'), index=False); pd.DataFrame(counts).to_csv(os.path.join(C.OUT, 'L5_1_strata.csv'), index=False)
# L5.7 PCA
Z = (R5 - R5.mean(0)) / R5.std(0); P = PCA(10).fit(Z); sc = P.transform(Z)
pd.DataFrame({'PC': ['PC%d' % (i + 1) for i in range(10)], 'explained_pct': P.explained_variance_ratio_ * 100, 'cumulative_pct': np.cumsum(P.explained_variance_ratio_) * 100}).to_csv(os.path.join(C.OUT, 'L5_7_pca_variance.csv'), index=False)
pd.DataFrame({'wavelength': w5, 'PC1': P.components_[0], 'PC2': P.components_[1], 'PC3': P.components_[2]}).to_csv(os.path.join(C.OUT, 'L5_7_pca_loadings.csv'), index=False)
pd.DataFrame({'leaf_id': np.arange(len(M)), 'grade': g, 'PC1': sc[:, 0], 'PC2': sc[:, 1], 'PC3': sc[:, 2]}).to_csv(os.path.join(C.OUT, 'L5_7_pca_scores.csv'), index=False)
ell = []
t = np.linspace(0, 2 * np.pi, 73)
for G in C.GRADES:
    for a, b in ((0, 1), (0, 2)):
        Q = sc[g == G][:, [a, b]]; mu = Q.mean(0); cov = np.cov(Q, rowvar=False); ev, V = np.linalg.eigh(cov); rad = np.sqrt(5.991 * ev)
        E = (V @ (rad[:, None] * np.vstack([np.cos(t), np.sin(t)]))).T + mu
        for i, (x, y) in enumerate(E): ell.append(dict(grade=G, pair='PC%d-PC%d' % (a + 1, b + 1), i=i, x=x, y=y))
pd.DataFrame(ell).to_csv(os.path.join(C.OUT, 'L5_7_pca_ellipses.csv'), index=False)
pcg = pd.DataFrame(sc[:, :3], columns=['PC1', 'PC2', 'PC3']).groupby(g).mean(); pcg.to_csv(os.path.join(C.OUT, 'L5_7_pca_grade_means.csv'))
best = D.iloc[np.argmax(np.abs(D.r_FD))]
summ = dict(max_abs_r_R=float(np.abs(D.r_R).max()), wl_max_r_R=int(D.wavelength[np.argmax(np.abs(D.r_R))]), max_abs_r_FD=float(np.abs(D.r_FD).max()), wl_max_r_FD=int(best.wavelength),
            REP_by_grade={int(G): float(F.REP[g == G].mean()) for G in C.GRADES}, top_index=ri.abs().idxmax(), top_index_r=float(ri[ri.abs().idxmax()]),
            pca_var=[float(v) for v in P.explained_variance_ratio_[:5] * 100])
json.dump(summ, open(os.path.join(C.OUT, 'L5_1_summary.json'), 'w'), indent=1); print(json.dumps(summ, indent=1))
