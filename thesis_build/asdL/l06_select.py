"""STEPS L5.2-L5.6 on the 1571 TRAINING leaves only (selection): NDSI/RSI R2 maps -> effective ranges -> SHAP-CARS optimal wavelengths;
best NDSI, RSI and White Rust Index; redundancy filter + ReliefF/RReliefF top 5 per task; VIF < 10 -> leaf DSF per task; JM distance between grades."""
import os, json, time, numpy as np, pandas as pd
from scipy.spatial.distance import cdist
from sklearn.ensemble import RandomForestRegressor
from sklearn.cross_decomposition import PLSRegression
import shap
import configL as C
t0 = time.time(); M = pd.read_csv(os.path.join(C.OUT, 'L2_meta.csv')); S = np.load(os.path.join(C.OUT, 'L3_spectra.npz')); F = pd.read_csv(os.path.join(C.OUT, 'L4_indices.csv'))
w5, R5, FD5, w1, R1 = S['w5'], S['R5'], S['FD5'], S['w1'], S['R1']; tr = (M.split == 'TRAIN').values; y = M.grade.values.astype(float); grp = M['plot'].values
Y = {'A': M.diseased.values, 'B': M.grade.map({g: i for i, g in enumerate(C.GRADES)}).values, 'C': y}
folds = M.inner_fold.values
def inner_splits(rows):
    f = folds[rows]; return [(np.where(f != k)[0], np.where(f == k)[0]) for k in (1, 2, 3)]
# ---------------- L5.2 maps
Rt, yt = R5[tr], y[tr]; n, p = Rt.shape; yc = (yt - yt.mean()) / yt.std(); N = np.full((p, p), np.nan); Sm = np.full((p, p), np.nan)
for a in range(p):
    A = Rt[:, a:a + 1]; nd = (A - Rt) / (A + Rt); rs = A / Rt
    for Mx, out in ((nd, N), (rs, Sm)):
        Mc = (Mx - Mx.mean(0)) / (Mx.std(0) + 1e-15); out[a] = (yc @ Mc / n) ** 2
iu = np.tril_indices(p); N[iu] = np.nan; Sm[iu] = np.nan
np.save(os.path.join(C.OUT, 'L5_2_NDSI_R2.npy'), N); np.save(os.path.join(C.OUT, 'L5_2_RSI_R2.npy'), Sm)
def hits(Mx):
    v = Mx[~np.isnan(Mx)]; thr = C.R2_THR if v.max() >= C.R2_THR else float(np.quantile(v, 1 - C.TOP_FRAC)); h = np.nan_to_num(Mx) >= thr; return h.any(0) | h.any(1), thr
bN, thN = hits(N); bS, thS = hits(Sm); eff = bN & bS
print('L5.2 maps done %.0fs | max R2 NDSI %.3f RSI %.3f | thresholds %.3f / %.3f | effective bands %d' % (time.time() - t0, np.nanmax(N), np.nanmax(Sm), thN, thS, eff.sum()))
guard = (w5 >= C.SPLICE_GUARD[0]) & (w5 <= C.SPLICE_GUARD[1])
cR, cF = np.where(eff)[0], np.where(eff & ~guard)[0]
Xc = np.hstack([R5[:, cR], FD5[:, cF]]); names = ['R%d' % w5[i] for i in cR] + ['FD%d' % w5[i] for i in cF]
rf = RandomForestRegressor(500, random_state=C.SEED, n_jobs=-1, min_samples_leaf=1).fit(Xc[tr], yt)
t1 = time.time(); sv = shap.TreeExplainer(rf).shap_values(Xc[tr], check_additivity=False); imp = np.abs(sv).mean(0); print('SHAP %.0fs' % (time.time() - t1))
ntop = max(10, int(round(C.SHAP_FRAC * len(names)))); top = np.argsort(-imp)[:ntop]
pd.DataFrame({'feature': names, 'mean_abs_SHAP': imp, 'kept_top40': np.isin(np.arange(len(names)), top)}).sort_values('mean_abs_SHAP', ascending=False).to_csv(os.path.join(C.OUT, 'L5_2_shap.csv'), index=False)
Xs = Xc[tr][:, top]; mu, sd = Xs.mean(0), Xs.std(0) + 1e-15; Xs = (Xs - mu) / sd; tn = [names[i] for i in top]
rng = np.random.default_rng(C.SEED); ug = np.unique(grp[tr]); maxc = min(C.MAX_PLS, Xs.shape[1]); err = np.zeros(maxc)
for s_ in range(C.MCCV):
    tg = rng.choice(ug, int(0.8 * len(ug)), replace=False); trm = np.isin(grp[tr], tg)
    for c in range(1, maxc + 1):
        m = PLSRegression(c, scale=False).fit(Xs[trm], yt[trm]); err[c - 1] += ((m.predict(Xs[~trm]).ravel() - yt[~trm]) ** 2).mean()
ncomp = int(np.argmin(err) + 1); pd.DataFrame({'components': np.arange(1, maxc + 1), 'MCCV_RMSE': np.sqrt(err / C.MCCV)}).to_csv(os.path.join(C.OUT, 'L5_2_mccv.csv'), index=False)
spl = inner_splits(tr)
def gkf_rmse(cols):
    e = []
    for a, b in spl:
        m = PLSRegression(min(ncomp, len(cols)), scale=False).fit(Xs[np.ix_(a, cols)], yt[a]); e.append(((m.predict(Xs[np.ix_(b, cols)]).ravel() - yt[b]) ** 2).mean())
    return float(np.sqrt(np.mean(e)))
P_ = Xs.shape[1]; it = C.CARS_IT; aa = (P_ / 2) ** (1 / (it - 1)); kk = np.log(P_ / 2) / (it - 1); keep = np.arange(P_); hist = []
for i in range(1, it + 1):
    sel = rng.choice(len(yt), int(0.8 * len(yt)), replace=False)
    m = PLSRegression(min(ncomp, len(keep)), scale=False).fit(Xs[np.ix_(sel, keep)], yt[sel]); wgt = np.abs(m.coef_.ravel()); wgt = wgt / wgt.sum()
    nk = max(2, int(round(aa * np.exp(-kk * i) * P_))); order = np.argsort(-wgt)[:nk]; cand = keep[order]; wc = wgt[order] / wgt[order].sum()
    keep = np.sort(cand[np.unique(rng.choice(len(cand), nk, replace=True, p=wc))]); hist.append(dict(iteration=i, n_bands=len(keep), GKF_RMSE=gkf_rmse(keep), bands=' '.join(tn[j] for j in keep)))
H = pd.DataFrame(hist); H.to_csv(os.path.join(C.OUT, 'L5_2_cars.csv'), index=False); best = H.loc[H.GKF_RMSE.idxmin()]; OW = best.bands.split()
print('L5.2 SHAP-CARS: candidates %d, SHAP kept %d, PLS comps %d, OW (%d) at iteration %d RMSE %.3f: %s' % (len(names), ntop, ncomp, len(OW), best.iteration, best.GKF_RMSE, OW))
# ---------------- L5.3 indices
def best_pair(Mx, sep):
    A = Mx.copy(); i, j = np.indices(A.shape); A[np.abs(w5[i] - w5[j]) < sep] = np.nan; k = np.nanargmax(A); a, b = np.unravel_index(k, A.shape); return int(w5[a]), int(w5[b]), float(A[a, b])
na, nb, nr2 = best_pair(N, C.PAIR_SEP); ra, rb, rr2 = best_pair(Sm, C.PAIR_SEP)
A = N.copy(); i, j = np.indices(A.shape); A[np.abs(w5[i] - w5[j]) < C.WRI_SEP] = np.nan
flat = np.argsort(np.nan_to_num(A, nan=-1).ravel())[::-1][:C.WRI_PAIRS]; l3 = np.arange(0, len(w5), C.WRI_STEP // C.STEP); wri_rows = []; bestW = None
for f in flat:
    a, b = np.unravel_index(f, A.shape); ndv = (Rt[:, a] - Rt[:, b]) / (Rt[:, a] + Rt[:, b])
    for wt in C.WRI_W:
        V = ndv[:, None] + wt * Rt[:, l3]; Vc = (V - V.mean(0)) / (V.std(0) + 1e-15); rr = yc @ Vc / n; kb = int(np.argmax(np.abs(rr)))
        cand = (abs(rr[kb]), float(rr[kb]), int(w5[a]), int(w5[b]), wt, int(w5[l3[kb]])); wri_rows.append(dict(l1=cand[2], l2=cand[3], w=wt, l3=cand[5], r=cand[1], abs_r=cand[0]))
        if bestW is None or cand[0] > bestW[0]: bestW = cand
pd.DataFrame(wri_rows).sort_values('abs_r', ascending=False).drop_duplicates(['l1', 'l2', 'w']).head(50).to_csv(os.path.join(C.OUT, 'L5_3_wri_top.csv'), index=False)
WRI = dict(l1=bestW[2], l2=bestW[3], w=bestW[4], l3=bestW[5], r=bestW[1])
gi = lambda lam: R1[:, int(np.argmin(np.abs(w1 - lam)))]
F2 = F.copy(); F2['NDSI_best'] = (gi(na) - gi(nb)) / (gi(na) + gi(nb)); F2['RSI_best'] = gi(ra) / gi(rb)
F2['WRI'] = (gi(WRI['l1']) - gi(WRI['l2'])) / (gi(WRI['l1']) + gi(WRI['l2'])) + WRI['w'] * gi(WRI['l3'])
print('L5.3 NDSI(%d,%d) R2 %.3f | RSI(%d,%d) R2 %.3f | WRI %s' % (na, nb, nr2, ra, rb, rr2, WRI))
# ---------------- L5.4 redundancy filter + ReliefF
Ft = F2[tr].reset_index(drop=True); ry = Ft.corrwith(pd.Series(yt)).abs().sort_values(ascending=False); Cm = Ft.corr().abs(); kept = []
for c in ry.index:
    if all(Cm.loc[c, k] < C.CORR_THR for k in kept): kept.append(c)
clusters = {k: [c for c in ry.index if Cm.loc[c, k] >= C.CORR_THR and c != k] for k in kept}
def relieff(X, yv, regression=False, k=C.RELIEF_K):
    X = (X - X.min(0)) / (X.max(0) - X.min(0) + 1e-15); nn_, p_ = X.shape; D = cdist(X, X, 'cityblock'); np.fill_diagonal(D, np.inf)
    if regression:
        nn = np.argsort(D, axis=1)[:, :k]; yr = (yv - yv.min()) / (yv.max() - yv.min()); NdC = 0.0; NdA = np.zeros(p_); NdCdA = np.zeros(p_)
        for i in range(nn_):
            dy = np.abs(yr[i] - yr[nn[i]]); dA = np.abs(X[i] - X[nn[i]]); NdC += dy.sum() / k; NdA += dA.sum(0) / k; NdCdA += (dy[:, None] * dA).sum(0) / k
        return NdCdA / NdC - (NdA - NdCdA) / (nn_ - NdC)
    cl, cnt = np.unique(yv, return_counts=True); Pc = dict(zip(cl, cnt / nn_)); W = np.zeros(p_)
    for i in range(nn_):
        for c in cl:
            idx = np.where(yv == c)[0]; idx = idx[idx != i]; nb_ = idx[np.argsort(D[i, idx])[:k]]; diff = np.abs(X[i] - X[nb_]).mean(0)
            W += (-diff if c == yv[i] else Pc[c] / (1 - Pc[yv[i]]) * diff) / nn_
    return W
RW = pd.DataFrame({'feature': kept}); VI = {}
for t in 'ABC':
    W = relieff(Ft[kept].values, Y[t][tr], regression=(t == 'C')); RW['weight_' + t] = W; VI[t] = [kept[i] for i in np.argsort(-W)[:C.N_TOP]]
RW['r_with_grade'] = [float(Ft[c].corr(pd.Series(yt))) for c in kept]; RW.to_csv(os.path.join(C.OUT, 'L5_4_relieff.csv'), index=False)
print('L5.4 kept after filter %d of %d; VI A %s | B %s | C %s' % (len(kept), F2.shape[1], VI['A'], VI['B'], VI['C']))
# ---------------- L5.5 VIF
BANDS = pd.DataFrame(np.hstack([R5, FD5]), columns=['R%d' % w for w in w5] + ['FD%d' % w for w in w5]); DSF = {}; VIFlog = []
def vif_filter(Fm):
    cols = list(Fm.columns); Z = (Fm - Fm.mean()) / (Fm.std() + 1e-15); out = []
    while len(cols) > 1:
        v = np.diag(np.linalg.pinv(np.corrcoef(Z[cols].values, rowvar=False))); j = int(np.argmax(v))
        out.append(dict(zip(cols, v)))
        if v[j] < C.VIF_THR: break
        cols.pop(j)
    return cols, out
for t in 'ABC':
    pool = pd.concat([BANDS[OW], F2[VI[t]]], axis=1)[tr]; pool = pool.loc[:, ~pool.columns.duplicated()]; cols, steps = vif_filter(pool); DSF[t] = cols
    for k_, st in enumerate(steps):
        for f_, v_ in st.items(): VIFlog.append(dict(task=t, round=k_ + 1, feature=f_, VIF=v_))
pd.DataFrame(VIFlog).to_csv(os.path.join(C.OUT, 'L5_5_vif_rounds.csv'), index=False)
print('L5.5 DSF A (%d) %s\n     B (%d) %s\n     C (%d) %s' % (len(DSF['A']), DSF['A'], len(DSF['B']), DSF['B'], len(DSF['C']), DSF['C']))
# ---------------- L5.6 JM distance (task B DSF, training leaves)
ALL = pd.concat([BANDS, F2], axis=1); ALL = ALL.loc[:, ~ALL.columns.duplicated()]
Xb = ALL[DSF['B']].values[tr]; Xb = (Xb - Xb.mean(0)) / Xb.std(0); gb = y[tr]; JM = []
for ii, a in enumerate(C.GRADES):
    for b in C.GRADES[ii + 1:]:
        Aa, Bb = Xb[gb == a], Xb[gb == b]; m = Aa.mean(0) - Bb.mean(0); Sa, Sb = np.cov(Aa, rowvar=False), np.cov(Bb, rowvar=False); Sx = (Sa + Sb) / 2
        sa, la = np.linalg.slogdet(Sa); sb, lb = np.linalg.slogdet(Sb); sx, lx = np.linalg.slogdet(Sx)
        Bd = m @ np.linalg.pinv(Sx) @ m / 8 + 0.5 * (lx - 0.5 * (la + lb)); JM.append(dict(grade_a=a, grade_b=b, JM=float(2 * (1 - np.exp(-Bd))), Bhattacharyya=float(Bd)))
pd.DataFrame(JM).to_csv(os.path.join(C.OUT, 'L5_6_jm.csv'), index=False)
ALL.to_csv(os.path.join(C.OUT, 'L5_all_features.csv'), index=False)
sel = dict(map_max_R2=dict(NDSI=float(np.nanmax(N)), RSI=float(np.nanmax(Sm))), thresholds=dict(NDSI=thN, RSI=thS), effective_bands=[int(x) for x in w5[eff]], n_candidates=len(names),
           n_shap_kept=ntop, pls_components=ncomp, OW=OW, cars_best_iteration=int(best.iteration), cars_best_rmse=float(best.GKF_RMSE), ndsi=[na, nb, nr2], rsi=[ra, rb, rr2], wri=WRI,
           kept_after_filter=kept, clusters=clusters, VI=VI, DSF=DSF, seconds=time.time() - t0)
json.dump(sel, open(os.path.join(C.OUT, 'L5_selection.json'), 'w'), indent=1); print('done %.0fs' % (time.time() - t0))
