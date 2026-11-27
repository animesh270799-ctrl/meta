"""Feature selection of Objective 1 and Step E2 (methodology Part D). select_chain() runs the whole chain on the leaves given by `rows`:
on ALL leaves it is the Objective 1 description (Step D); on the training plots it gives the model inputs (Step E2)."""
import numpy as np, pandas as pd
from scipy.spatial.distance import cdist
from sklearn.cross_decomposition import PLSRegression
from sklearn.model_selection import GroupKFold, KFold
import config as C
from lib_spec import join_mask


# ------------------------------------------------------------------ D4 band-pair maps and effective ranges
def r2_maps(R, y, chunk=40):
    """R² of NDSI and RSI with y for all band pairs (i < j)."""
    n, p = R.shape; yc = (y - y.mean()) / y.std(); N = np.zeros((p, p)); S = np.zeros((p, p))
    for a in range(0, p, chunk):
        A = R[:, a:a + chunk]
        nd = (A[:, :, None] - R[:, None, :]) / (A[:, :, None] + R[:, None, :]); rs = A[:, :, None] / R[:, None, :]
        for M, out in ((nd, N), (rs, S)):
            Mc = (M - M.mean(0)) / (M.std(0) + 1e-12); r = np.einsum('i,ijk->jk', yc, Mc) / n; out[a:a + chunk] = r ** 2
    iu = np.tril_indices(p); N[iu] = np.nan; S[iu] = np.nan
    return N, S


def effective_ranges(N, S, w):
    """bands taking part in pairs with R² >= R2_THR in either map; if none, pairs in the top TOP_FRAC (Ma et al., 2026; Tian et al., 2021)."""
    ok = join_mask(w); okm = ok[:, None] & ok[None, :]
    allr2 = np.concatenate([N[okm & ~np.isnan(N)], S[okm & ~np.isnan(S)]])
    thr = C.R2_THR if (allr2 >= C.R2_THR).any() else float(np.quantile(allr2, 1 - C.TOP_FRAC))
    used = np.zeros(len(w), bool)
    for M in (N, S):
        hit = (np.nan_to_num(M) >= thr) & okm; used |= hit.any(0) | hit.any(1)
    return used, thr


def best_pair(M, w, min_sep=C.PAIR_MIN_SEP):
    A = M.copy(); i, j = np.indices(A.shape); A[np.abs(w[i] - w[j]) < min_sep] = np.nan
    ok = join_mask(w); A[~(ok[:, None] & ok[None, :])] = np.nan
    k = np.nanargmax(A); a, b = np.unravel_index(k, A.shape); return int(w[a]), int(w[b]), float(A[a, b])


# ------------------------------------------------------------------ D5 SHAP-CARS (Ma et al., 2026; Li et al., 2009)
def _splits(n, groups, k, seed):
    return list(GroupKFold(k).split(np.zeros(n), groups=groups)) if groups is not None else list(KFold(k, shuffle=True, random_state=seed).split(np.zeros(n)))


def pls_rmsecv(X, y, ncomp, groups=None, seed=0):
    e = []
    for tr, te in _splits(len(y), groups, 5, seed):
        m = PLSRegression(min(ncomp, X.shape[1], len(tr) - 1), scale=False).fit(X[tr], y[tr]); e.append(((m.predict(X[te]).ravel() - y[te]) ** 2).mean())
    return float(np.sqrt(np.mean(e)))


def mccv_ncomp(X, y, groups=None, seed=0):
    """Monte Carlo cross-validation (random 80/20 divisions of the plots) for the number of PLS components."""
    rng = np.random.default_rng(seed); maxc = min(C.MAX_PLS, X.shape[1]); err = np.zeros(maxc)
    ug = np.unique(groups) if groups is not None else None
    for s in range(C.MCCV_SPLITS):
        if groups is not None:
            tg = rng.choice(ug, int(0.8 * len(ug)), replace=False); trm = np.isin(groups, tg); tr, te = np.where(trm)[0], np.where(~trm)[0]
        else:
            idx = rng.permutation(len(y)); tr, te = idx[:int(0.8 * len(y))], idx[int(0.8 * len(y)):]
        m = PLSRegression(maxc, scale=False).fit(X[tr], y[tr]); Xc = (X[te] - m._x_mean) / m._x_std
        for c in range(1, maxc + 1):
            yp = (Xc @ m.x_rotations_[:, :c]) @ m.y_loadings_[:, :c].T * m._y_std + m._y_mean; err[c - 1] += ((yp.ravel() - y[te]) ** 2).mean()
    return int(np.argmin(err) + 1)


def cars(X, y, ncomp, groups=None, seed=0):
    rng = np.random.default_rng(seed); n, p = X.shape; it = C.CARS_ITER
    a = (p / 2) ** (1 / (it - 1)); k = np.log(p / 2) / (it - 1); keep = np.arange(p); hist = []
    for i in range(1, it + 1):
        sel = rng.choice(n, int(0.8 * n), replace=False)
        m = PLSRegression(min(ncomp, len(keep)), scale=False).fit(X[np.ix_(sel, keep)], y[sel])
        wgt = np.abs(m.coef_.ravel()); wgt = wgt / wgt.sum(); nk = max(2, int(round(a * np.exp(-k * i) * p)))
        order = np.argsort(-wgt)[:nk]; cand = keep[order]; wc = wgt[order] / wgt[order].sum()
        keep = cand[np.unique(rng.choice(len(cand), nk, replace=True, p=wc))]
        hist.append((pls_rmsecv(X[:, keep], y, min(ncomp, len(keep)), groups, seed), keep.copy()))
    return min(hist, key=lambda h: h[0])[1]


def shap_cars(Xc, y, names, groups=None, seed=C.SEED):
    import xgboost as xgb, shap
    m = xgb.XGBRegressor(random_state=seed, n_jobs=4, **C.XGB_SHAP).fit(Xc, y)
    imp = np.abs(shap.TreeExplainer(m).shap_values(Xc)).mean(0)
    top = np.argsort(-imp)[:max(10, int(round(C.SHAP_FRAC * Xc.shape[1])))]                    # SHAP pre-screen: top 40 %
    Xs = Xc[:, top]; Xs = (Xs - Xs.mean(0)) / (Xs.std(0) + 1e-12)
    nc = mccv_ncomp(Xs, y, groups, seed); cnt = np.zeros(len(top))
    for r in range(C.CARS_RUNS): cnt[cars(Xs, y, nc, groups, seed + r)] += 1
    freq = cnt / C.CARS_RUNS; st = np.where(freq >= C.CARS_KEEP)[0]
    if len(st) > C.MAX_OW: st = st[np.argsort(-freq[st])[:C.MAX_OW]]
    if len(st) < 3: st = np.argsort(-freq)[:3]
    return dict(names=[names[top[i]] for i in st], ncomp=nc, freq={names[top[i]]: float(freq[i]) for i in range(len(top)) if freq[i] > 0})


# ------------------------------------------------------------------ D6 White Rust Index (Mahlein et al., 2013)
def wri_search(R, w, y, N):
    A = N.copy(); i, j = np.indices(A.shape); A[np.abs(w[i] - w[j]) < C.WRI_MIN_SEP] = np.nan
    ok = join_mask(w); A[~(ok[:, None] & ok[None, :])] = np.nan
    flat = np.argsort(np.nan_to_num(A, nan=-1).ravel())[::-1][:C.WRI_TOP_PAIRS]; l3 = np.arange(0, len(w), C.WRI_STEP // C.BAND_STEP)
    yc = (y - y.mean()) / y.std(); best = None
    for f in flat:
        a, b = np.unravel_index(f, A.shape); ndv = (R[:, a] - R[:, b]) / (R[:, a] + R[:, b])
        for wt in C.WRI_WEIGHTS:
            V = ndv[:, None] + wt * R[:, l3]; Vc = (V - V.mean(0)) / (V.std(0) + 1e-12); rr = yc @ Vc / len(y); kb = int(np.argmax(np.abs(rr)))
            if best is None or abs(rr[kb]) > best[0]: best = (abs(rr[kb]), float(rr[kb]), int(w[a]), int(w[b]), wt, int(w[l3[kb]]))
    return dict(l1=best[2], l2=best[3], w=best[4], l3=best[5], r=best[1])


def add_data_indices(F, R1, w1, sel):
    """NDSI_best, RSI_best and WRI for every leaf from the wavelengths chosen in `sel` (1-nm reflectance)."""
    g = lambda lam: R1[:, int(np.argmin(np.abs(w1 - lam)))]; F = F.copy(); a, b = sel['ndsi']; c, d = sel['rsi']; W = sel['wri']
    F['NDSI_best'] = (g(a) - g(b)) / (g(a) + g(b)); F['RSI_best'] = g(c) / g(d)
    F['WRI'] = (g(W['l1']) - g(W['l2'])) / (g(W['l1']) + g(W['l2'])) + W['w'] * g(W['l3']); return F


# ------------------------------------------------------------------ D7-D10 redundancy, ReliefF, wavelets, VIF
def corr_filter(F, y):
    cols = [c for c in F.columns if F[c].std() > 1e-12]
    ry = F[cols].corrwith(pd.Series(y, index=F.index)).abs().sort_values(ascending=False); Cm = F[cols].corr().abs(); kept = []
    for c in ry.index:
        if all(Cm.loc[c, k] < C.CORR_THR for k in kept): kept.append(c)
    return kept


def relieff(X, y, groups, regression=False, k=C.RELIEF_K):
    """ReliefF (classes) / RReliefF (continuous) with neighbours from the same plot excluded (Robnik-Sikonja and Kononenko, 2003)."""
    X = (X - X.min(0)) / (X.max(0) - X.min(0) + 1e-12); n, p = X.shape
    D = cdist(X, X, 'cityblock'); D[groups[:, None] == groups[None, :]] = np.inf
    if regression:
        nn = np.argsort(D, axis=1)[:, :k]; yr = (y - y.min()) / (y.max() - y.min() + 1e-12); NdC = 0.0; NdA = np.zeros(p); NdCdA = np.zeros(p)
        for i in range(n):
            dy = np.abs(yr[i] - yr[nn[i]]); dA = np.abs(X[i] - X[nn[i]]); NdC += dy.sum() / k; NdA += dA.sum(0) / k; NdCdA += (dy[:, None] * dA).sum(0) / k
        return NdCdA / NdC - (NdA - NdCdA) / (n - NdC)
    cl, cnt = np.unique(y, return_counts=True); P = dict(zip(cl, cnt / n)); W = np.zeros(p)
    for i in range(n):
        di = D[i]
        for c in cl:
            idx = np.where((y == c) & np.isfinite(di))[0]
            if len(idx) == 0: continue
            nb = idx[np.argsort(di[idx])[:k]]; diff = np.abs(X[i] - X[nb]).mean(0)
            W += (-diff if c == y[i] else P[c] / (1 - P[y[i]]) * diff) / n
    return W


def wavelet_screen(Wc, task, y_task, grade, groups, w1):
    """Step D9: separability of every wavelet coefficient (A: best balanced accuracy of one threshold, Tian et al., 2021; B, C: |r| with the grade),
    top 5 %, regions of the same scale < 10 nm apart -> representative, then ReliefF/RReliefF -> top N_TOP."""
    n, S, L = Wc.shape; X = Wc.reshape(n, S * L)
    ok = np.concatenate([np.array([all(lam + 2 * sc < a or lam - 2 * sc > b for a, b in C.JOIN_ZONES) for lam in w1]) for sc in C.CWT_SCALES])   # window +-2 x scale clear of the joins
    if task == 'A':
        y = y_task.astype(bool); m0, m1 = X[~y].mean(0), X[y].mean(0); sign = np.where(m1 >= m0, 1, -1); best = np.zeros(S * L)
        for q in np.linspace(0.01, 0.99, 99):
            t = m0 + q * (m1 - m0); pos = (X * sign) > (t * sign)
            ba = 0.5 * (pos[y].mean(0) + (~pos[~y]).mean(0)); best = np.maximum(best, ba)
        sep = best
    else:
        g = (grade - grade.mean()) / grade.std(); Xc = (X - X.mean(0)) / (X.std(0) + 1e-12); sep = np.abs(g @ Xc / n)
    sep[~ok] = -1; top = np.where(sep >= np.quantile(sep[ok], 1 - C.WAVELET_TOP))[0]
    reps = []
    for s in range(S):
        idx = sorted(i for i in top if i // L == s); grp = []
        for i in idx:
            if grp and w1[i % L] - w1[grp[-1] % L] >= C.REGION_GAP: reps.append(max(grp, key=lambda j: sep[j])); grp = []
            grp.append(i)
        if grp: reps.append(max(grp, key=lambda j: sep[j]))
    names = ['W%d_s%d' % (w1[i % L], C.CWT_SCALES[i // L]) for i in reps]
    Wt = relieff(X[:, reps], y_task, groups, regression=(task == 'C'))
    order = np.argsort(-Wt)[:C.N_TOP]
    return [names[i] for i in order], {names[i]: float(sep[reps[i]]) for i in range(len(reps))}


def wavelet_columns(Wc, w1, names):
    """values of the named wavelet features (W<nm>_s<scale>) for all leaves"""
    out = {}
    for nm in names:
        wl, s = nm[1:].split('_s'); out[nm] = Wc[:, C.CWT_SCALES.index(int(s)), int(np.argmin(np.abs(w1 - int(wl))))]
    return pd.DataFrame(out)


def vif_filter(F):
    cols = list(F.columns); Z = (F - F.mean()) / (F.std() + 1e-12); removed = []
    while len(cols) > 1:
        v = np.diag(np.linalg.pinv(np.corrcoef(Z[cols].values, rowvar=False))); j = int(np.argmax(v))
        if v[j] < C.VIF_THR: break
        removed.append((cols[j], float(v[j]))); cols.pop(j)
    return cols, removed


def jm_distance(X, y):
    """Step D11: Jeffries-Matusita distance 2(1 - exp(-B)) for every pair of classes, Gaussian classes (Richards, 2013)."""
    out = {}; cl = np.unique(y)
    for i, a in enumerate(cl):
        for b in cl[i + 1:]:
            A, B_ = X[y == a], X[y == b]; m = A.mean(0) - B_.mean(0); Sa, Sb = np.cov(A, rowvar=False), np.cov(B_, rowvar=False); S = (Sa + Sb) / 2
            Bd = m @ np.linalg.pinv(S) @ m / 8 + 0.5 * np.log(np.linalg.det(S) / np.sqrt(np.linalg.det(Sa) * np.linalg.det(Sb)) + 1e-300)
            out['%s-%s' % (a, b)] = float(2 * (1 - np.exp(-Bd)))
    return out


# ------------------------------------------------------------------ the whole chain
def select_chain(rows, S, F44, CR, Wc, M, log=print):
    """rows: boolean mask of the leaves to use. S: dict of spectra (w1, R1, FD1, w5, R5, FD5). F44: published indices + REP, Dr, REarea.
    CR: continuum-removal features. Wc: wavelet coefficients. M: leaf table with grade, diseased, plot. Returns the selection dictionary."""
    w5, R5, FD5, w1, R1 = S['w5'], S['R5'], S['FD5'], S['w1'], S['R1']
    y = M.grade.values.astype(float); grp = M['plot'].values; Y = {'A': M.diseased.values, 'B': M.grade.map({g: i for i, g in enumerate(C.GRADES)}).values, 'C': y}
    N, Sm = r2_maps(R5[rows], y[rows]); used, thr = effective_ranges(N, Sm, w5); log('D4 effective ranges: threshold R2 %.3f, %d bands' % (thr, used.sum()))
    re = (w5 >= C.REDEDGE_FD[0]) & (w5 <= C.REDEDGE_FD[1]) & join_mask(w5); cR, cF = np.where(used)[0], np.where(used | re)[0]
    Xc = np.hstack([R5[rows][:, cR], FD5[rows][:, cF]]); names = ['R%d' % w5[i] for i in cR] + ['FD%d' % w5[i] for i in cF]
    sc = shap_cars(Xc, y[rows], names, grp[rows]); log('D5 optimal wavelengths:', sc['names'])
    a, b, r2n = best_pair(N, w5); c, d, r2r = best_pair(Sm, w5); wri = wri_search(R5[rows], w5, y[rows], N)
    sel = dict(eff_thr=thr, eff_bands=[int(x) for x in w5[used]], OW=sc['names'], cars_ncomp=sc['ncomp'], cars_freq=sc['freq'], ndsi=[a, b], ndsi_r2=r2n, rsi=[c, d], rsi_r2=r2r, wri=wri)
    log('D6 best NDSI', (a, b), 'RSI', (c, d), 'WRI', wri)
    F2 = pd.concat([add_data_indices(F44, R1, w1, sel), CR], axis=1)
    kept = corr_filter(F2[rows].reset_index(drop=True), y[rows]); sel['family2_kept'] = kept; log('D7 index features kept after |r| filter:', len(kept))
    BANDS = pd.DataFrame(np.hstack([R5, FD5]), columns=['R%d' % w for w in w5] + ['FD%d' % w for w in w5])
    sel['VI'], sel['WF'], sel['DSF'], sel['VIF_removed'], sel['wavelet_sep'] = {}, {}, {}, {}, {}
    for t in 'ABC':
        Wt = relieff(F2[kept].values[rows], Y[t][rows], grp[rows], regression=(t == 'C')); sel['VI'][t] = [kept[i] for i in np.argsort(-Wt)[:C.N_TOP]]
        sel['WF'][t], sep = wavelet_screen(Wc[rows], t, Y[t][rows], y[rows], grp[rows], w1); sel['wavelet_sep'][t] = sep
        pool = pd.concat([BANDS[sc['names']], F2[sel['VI'][t]], wavelet_columns(Wc, w1, sel['WF'][t])], axis=1)[rows]
        sel['DSF'][t], sel['VIF_removed'][t] = vif_filter(pool)
        log('D8-D10 task %s: VI %s | WF %s | DSF (%d) %s' % (t, sel['VI'][t], sel['WF'][t], len(sel['DSF'][t]), sel['DSF'][t]))
    return sel


def feature_table(sel, S, F44, CR, Wc):
    """all candidate model inputs (bands, family 2 with the selected data-driven indices, selected wavelet features) for ALL leaves"""
    w5, w1 = S['w5'], S['w1']
    BANDS = pd.DataFrame(np.hstack([S['R5'], S['FD5']]), columns=['R%d' % w for w in w5] + ['FD%d' % w for w in w5])
    wf = sorted(set(x for t in 'ABC' for x in sel['WF'][t]))
    return pd.concat([BANDS, add_data_indices(F44, S['R1'], w1, sel), CR, wavelet_columns(Wc, w1, wf)], axis=1)
