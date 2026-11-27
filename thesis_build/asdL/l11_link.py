"""STEP L9: leaf-canopy link with the UAV hyperspectral plot spectra of 24 Feb 2026 (the only UAV date of 2025-26).
(1) Leaf vs canopy OW/VI overlap: not possible (no canopy selection chain for 2025-26) -> reported as not applicable.
(2) Plot-mean leaf spectrum (all leaves of the plot on 24 Feb) resampled to the UAV band centres (Gaussian response, FWHM = local band spacing);
    per-band Pearson r between leaf and UAV reflectance over the 48 plots; mean spectra.
(3) Leaf WRI and leaf VI computed from the UAV plot spectra; r with plot disease index (DI, %) and detection (DI > 0) with a threshold set on the
    33 training plots (Youden) and balanced accuracy on the 15 test plots."""
import os, json, numpy as np, pandas as pd
from scipy.signal import savgol_filter
import configL as C
O = C.OUT; M = pd.read_csv(os.path.join(O, 'L2_meta.csv')); S = np.load(os.path.join(O, 'L3_spectra.npz')); SEL = json.load(open(os.path.join(O, 'L5_selection.json')))
w1, R1 = S['w1'], S['R1'].astype(float)
L = open(C.UAV_PLOT).read().splitlines(); nc = sum(l.startswith('Column') for l in L); A = np.array([[float(x) for x in l.split()] for l in L[nc + 1:] if l.strip()])
wu, U = A[:, 0], A[:, 1:].T; assert U.shape[0] == 48                                              # ROI #p = plot p
d24 = (M.date == '2026-02-24').values; plots = np.arange(1, 49)
LEAF = np.stack([R1[d24 & (M['plot'].values == p)].mean(0) for p in plots]); nleaf = np.array([(d24 & (M['plot'].values == p)).sum() for p in plots])
DI = np.array([M.loc[d24 & (M['plot'].values == p), 'grade'].sum() / (9 * nleaf[i]) * 100 for i, p in enumerate(plots)])
# (2) resample leaf spectra to the UAV band centres
inr = (wu >= C.WMIN + 10) & (wu <= C.WMAX - 10); wb = wu[inr]; sp = np.gradient(wu)[inr]
fw = np.where(sp > 8, np.median(sp), sp)                                                           # bands next to a gap keep the median spacing
W = np.exp(-4 * np.log(2) * ((w1[None, :] - wb[:, None]) / fw[:, None]) ** 2); W /= W.sum(1, keepdims=True)
LR = LEAF @ W.T; UR = U[:, inr]
rb = np.array([np.corrcoef(LR[:, j], UR[:, j])[0, 1] for j in range(len(wb))])
rL = np.array([np.corrcoef(LR[:, j], DI)[0, 1] for j in range(len(wb))]); rU = np.array([np.corrcoef(UR[:, j], DI)[0, 1] for j in range(len(wb))])
healthy = plots <= 12
band = pd.DataFrame(dict(wavelength=wb, FWHM=fw, r_leaf_vs_UAV=rb, r_leaf_vs_DI=rL, r_UAV_vs_DI=rU, leaf_mean_healthy=LR[healthy].mean(0), leaf_mean_diseased=LR[~healthy].mean(0),
                         UAV_mean_healthy=UR[healthy].mean(0), UAV_mean_diseased=UR[~healthy].mean(0), ratio_UAV_to_leaf=UR.mean(0) / LR.mean(0)))
band.to_csv(os.path.join(O, 'L9_bandwise.csv'), index=False)
# (3) leaf indices on the UAV spectra: UAV spectrum -> 1 nm (linear) -> SG (11, 2) as in L3
w1u = np.arange(400, 2401); U1 = np.stack([np.interp(w1u, wu, u) for u in U]); Ru = savgol_filter(U1, C.SG_W, C.SG_O, axis=1); FDu = savgol_filter(U1, C.SG_W, C.SG_O, deriv=1, axis=1)
Rl = R1[d24]; FDl = S['FD1'].astype(float)[d24]
def idx(Rm, FDm):
    r = lambda w: Rm[:, int(round(w - 400))]; nd = lambda a, b: (r(a) - r(b)) / (r(a) + r(b)); n_, b_ = SEL['ndsi'][:2]; ra, rb_ = SEL['rsi'][:2]; wr = SEL['wri']
    fd = FDm[:, 280:361]
    return pd.DataFrame({'WRI': nd(wr['l1'], wr['l2']) + wr['w'] * r(wr['l3']), 'NDSI_best': nd(n_, b_), 'RSI_best': r(ra) / r(rb_), 'HI': nd(534, 698) - 0.5 * r(704), 'RR': 1 / r(700),
                         'REP': 680 + fd.argmax(1).astype(float), 'RVSI': (r(712) + r(752)) / 2 - r(732), 'GNDVI': nd(850, 550), 'RARSa': r(675) / r(700), 'DWSI-2': r(1660) / r(550)})
IU = idx(Ru, FDu); IL = idx(Rl, FDl); IL['plot'] = M.loc[d24, 'plot'].values; ILp = IL.groupby('plot').mean().reindex(plots)
test = np.isin(plots, C.TEST_PLOTS); y = (DI > 0).astype(int); rows = []
for f in IU.columns:
    v = IU[f].values; rr = np.corrcoef(v, DI)[0, 1]; rtr = np.corrcoef(v[~test], DI[~test])[0, 1]; sgn = 1 if np.corrcoef(v[~test], y[~test])[0, 1] > 0 else -1
    cand = np.unique(v[~test]); best = (-1, None)
    for t in cand:
        pr = (sgn * v[~test] >= sgn * t).astype(int); sens = pr[y[~test] == 1].mean(); spec = 1 - pr[y[~test] == 0].mean(); j = sens + spec - 1
        if j > best[0]: best = (j, t)
    pt = (sgn * v[test] >= sgn * best[1]).astype(int); sens = pt[y[test] == 1].mean(); spec = 1 - pt[y[test] == 0].mean()
    rows.append(dict(feature=f, r_UAV_vs_DI_all48=rr, r_UAV_vs_DI_test15=np.corrcoef(v[test], DI[test])[0, 1], r_leaf_vs_DI_all48=np.corrcoef(ILp[f].values, DI)[0, 1],
                     r_leaf_vs_UAV_index=np.corrcoef(ILp[f].values, v)[0, 1], direction=('higher = diseased' if sgn > 0 else 'lower = diseased'), threshold_train=best[1],
                     test_sensitivity=sens, test_specificity=spec, test_balanced_acc=(sens + spec) / 2, leaf_r_with_grade=np.corrcoef(IL[f].values, M.loc[d24, 'grade'].values)[0, 1]))
T = pd.DataFrame(rows); T.to_csv(os.path.join(O, 'L9_transfer.csv'), index=False)
pl = pd.DataFrame(dict(plot=plots, block=[C.BLOCK(p) for p in plots], split=np.where(test, 'TEST', 'TRAIN'), n_leaves=nleaf, DI=DI)); pl = pd.concat([pl, IU.add_prefix('UAV_'), ILp.reset_index(drop=True).add_prefix('leaf_')], axis=1)
pl.to_csv(os.path.join(O, 'L9_plots.csv'), index=False)
json.dump(dict(n_uav_bands=int(len(wu)), uav_range=[float(wu[0]), float(wu[-1])], bands_compared=int(len(wb)), median_r_leaf_vs_UAV=float(np.median(rb)), r_by_region={k: float(np.median(rb[(wb >= a) & (wb < b)])) for k, (a, b) in
           {'VIS 400-700': (400, 700), 'red edge 700-750': (700, 750), 'NIR 750-1300': (750, 1300), 'SWIR 1300-2400': (1300, 2400)}.items()}, healthy_plots=int(healthy.sum()), diseased_plots=int((DI > 0).sum())),
          open(os.path.join(O, 'L9_summary.json'), 'w'), indent=1)
pd.set_option('display.width', 250); print(T.round(3).to_string(index=False)); print(json.load(open(os.path.join(O, 'L9_summary.json'))))
