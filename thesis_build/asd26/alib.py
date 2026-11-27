"""Shared methods for the ASD analysis: NDSI/RSI maps, SHAP-CARS, WRI search, redundancy filter, ReliefF/RReliefF, VIF."""
import numpy as np, pandas as pd
from sklearn.cross_decomposition import PLSRegression
from sklearn.model_selection import KFold

def r2_maps(R, y, chunk=40):
    """R² of NDSI and RSI with y for all band pairs (i < j)."""
    n, p = R.shape; yc = (y - y.mean()) / y.std()
    N = np.full((p, p), np.nan); S = np.full((p, p), np.nan)
    for a in range(0, p, chunk):
        A = R[:, a:a + chunk][:, :, None]; Bm = R[:, None, :]
        nd = (A - Bm) / (A + Bm); rs = A / Bm
        for M, out in ((nd, N), (rs, S)):
            Mc = (M - M.mean(0)) / (M.std(0) + 1e-12)
            rr = np.einsum('n,nij->ij', yc, Mc) / n
            out[a:a + chunk, :] = rr ** 2
    iu = np.tril_indices(p)
    N[iu] = np.nan; S[iu] = np.nan
    return N, S

def effective_ranges(Nmap, Smap, w, thr=0.5, top=0.05):
    """Bands taking part in pairs with R² >= thr in either map; fallback: top 5% of pairs."""
    both = np.fmax(Nmap, Smap)
    vals = both[np.isfinite(both)]
    t = thr if (vals >= thr).any() else np.quantile(vals, 1 - top)
    m = np.nan_to_num(both) >= t
    used = m.any(0) | m.any(1)
    return used, t

def best_pair(Mp, w, min_sep=10):
    A = Mp.copy(); i, j = np.indices(A.shape); A[np.abs(w[i] - w[j]) < min_sep] = np.nan
    k = np.nanargmax(A); a, b = np.unravel_index(k, A.shape); return int(w[a]), int(w[b]), float(A[a, b])

def pls_rmsecv(X, y, ncomp, folds=5, seed=0):
    kf = KFold(folds, shuffle=True, random_state=seed); e = []
    for tr, te in kf.split(X):
        m = PLSRegression(min(ncomp, X.shape[1], len(tr) - 1), scale=False).fit(X[tr], y[tr]); e.append(((m.predict(X[te]).ravel() - y[te]) ** 2).mean())
    return float(np.sqrt(np.mean(e)))

def mccv_ncomp(X, y, maxc=15, splits=50, seed=0):
    rng = np.random.default_rng(seed); n = len(y); maxc = min(maxc, X.shape[1]); err = np.zeros(maxc)
    for s in range(splits):
        idx = rng.permutation(n); tr, te = idx[:int(0.8 * n)], idx[int(0.8 * n):]
        m = PLSRegression(maxc, scale=False).fit(X[tr], y[tr])
        for c in range(1, maxc + 1):
            # predictions with c components from the fitted model
            Xc = (X[te] - m._x_mean) / m._x_std
            T = Xc @ m.x_rotations_[:, :c]; yp = T @ m.y_loadings_[:, :c].T * m._y_std + m._y_mean
            err[c - 1] += ((yp.ravel() - y[te]) ** 2).mean()
    return int(np.argmin(err) + 1), np.sqrt(err / splits)

def cars(X, y, ncomp, n_iter=50, seed=0):
    """Competitive adaptive reweighted sampling (Li et al., 2009). X standardised."""
    rng = np.random.default_rng(seed); n, p = X.shape
    a = (p / 2) ** (1 / (n_iter - 1)); k = np.log(p / 2) / (n_iter - 1)
    keep = np.arange(p); hist = []
    for i in range(1, n_iter + 1):
        sel = rng.choice(n, int(0.8 * n), replace=False)
        m = PLSRegression(min(ncomp, len(keep)), scale=False).fit(X[np.ix_(sel, keep)], y[sel])
        wgt = np.abs(m.coef_.ravel()); wgt = wgt / wgt.sum()
        ratio = a * np.exp(-k * i); nk = max(2, int(round(ratio * p)))
        order = np.argsort(-wgt)[:nk]; cand = keep[order]; wc = wgt[order] / wgt[order].sum()
        drawn = np.unique(rng.choice(len(cand), nk, replace=True, p=wc)); keep = cand[drawn]
        rm = pls_rmsecv(X[:, keep], y, min(ncomp, len(keep)), seed=seed)
        hist.append((i, len(keep), rm, keep.copy()))
    best = min(hist, key=lambda h: h[2])
    return best[3], hist

def shap_prescreen(X, y, frac=0.4, seed=42):
    import xgboost as xgb, shap
    m = xgb.XGBRegressor(n_estimators=300, max_depth=4, learning_rate=0.05, subsample=0.8, colsample_bytree=0.8, random_state=seed, n_jobs=4).fit(X, y)
    sv = shap.TreeExplainer(m).shap_values(X); imp = np.abs(sv).mean(0)
    k = max(10, int(round(frac * X.shape[1]))); return np.argsort(-imp)[:k], imp

def shap_cars(Xc, y, names, runs=20, n_iter=50, maxsel=15, seed=42):
    """SHAP pre-screening (top 40%) -> standardisation -> MCCV for PLS components -> CARS repeated `runs` times -> stability >= 50%."""
    top, imp = shap_prescreen(Xc, y, seed=seed)
    Xs = Xc[:, top]; Xs = (Xs - Xs.mean(0)) / (Xs.std(0) + 1e-12)
    nc, mc_err = mccv_ncomp(Xs, y, seed=seed)
    counts = np.zeros(len(top)); hists = []
    for rr in range(runs):
        sel, hist = cars(Xs, y, nc, n_iter=n_iter, seed=seed + rr); counts[sel] += 1; hists.append(hist)
    freq = counts / runs; stable = np.where(freq >= 0.5)[0]
    if len(stable) > maxsel: stable = stable[np.argsort(-freq[stable])[:maxsel]]
    if len(stable) < 3: stable = np.argsort(-freq)[:max(3, min(maxsel, int((freq > 0).sum())))]
    chosen = top[stable]
    return dict(chosen=chosen, names=[names[c] for c in chosen], freq=freq, top=top, imp=imp, ncomp=nc, mccv=mc_err, hist=hists[0])

def wri_search(R, w, y, Nmap, top_pairs=200, step=10, weights=(-1, -0.5, 0, 0.5, 1), min_sep=50):
    """WRI = NDSI(l1, l2) + w R(l3); l1, l2 from the top NDSI pairs (>= 50 nm apart), l3 every `step` nm; score |r| with y."""
    A = Nmap.copy(); i, j = np.indices(A.shape); A[np.abs(w[i] - w[j]) < min_sep] = np.nan
    flat = np.argsort(np.nan_to_num(A, nan=-1).ravel())[::-1][:top_pairs]
    pairs = [np.unravel_index(f, A.shape) for f in flat]
    l3 = np.arange(0, len(w), step // int(w[1] - w[0]))
    yc = (y - y.mean()) / y.std(); out = []
    for a, b in pairs:
        ndv = (R[:, a] - R[:, b]) / (R[:, a] + R[:, b])
        for wt in weights:
            V = ndv[:, None] + wt * R[:, l3]
            Vc = (V - V.mean(0)) / (V.std(0) + 1e-12); rr = yc @ Vc / len(y)
            kbest = np.argmax(np.abs(rr)); out.append((abs(rr[kbest]), rr[kbest], int(w[a]), int(w[b]), wt, int(w[l3[kbest]])))
    out.sort(key=lambda t: -t[0]); return out

def wri_values(R, w, l1, l2, wt, l3):
    g = lambda lam: R[:, int(np.argmin(np.abs(w - lam)))]
    return (g(l1) - g(l2)) / (g(l1) + g(l2)) + wt * g(l3)

def corr_filter(F, y, thr=0.95):
    """Keep one feature per cluster with |r| >= thr (the one most correlated with y)."""
    cols = [c for c in F.columns if F[c].std() > 1e-12]
    ry = F[cols].corrwith(pd.Series(y, index=F.index)).abs().sort_values(ascending=False)
    C = F[cols].corr().abs(); kept = []
    for c in ry.index:
        if all(C.loc[c, k] < thr for k in kept): kept.append(c)
    return kept

def relieff(X, y, groups, k=10, regression=False, seed=0):
    """ReliefF (classes) / RReliefF (continuous) with neighbours from the same plot excluded (Robnik-Šikonja and Kononenko, 2003)."""
    X = (X - X.min(0)) / (X.max(0) - X.min(0) + 1e-12); n, p = X.shape
    D = np.abs(X[:, None, :] - X[None, :, :]).sum(2)
    same = groups[:, None] == groups[None, :]; D[same] = np.inf
    nn = np.argsort(D, axis=1)[:, :k]
    if regression:
        yr = (y - y.min()) / (y.max() - y.min() + 1e-12)
        NdC = NdA = 0.0; NdCdA = np.zeros(p); NdAv = np.zeros(p)
        for i in range(n):
            for jn in nn[i]:
                dy = abs(yr[i] - yr[jn]); dA = np.abs(X[i] - X[jn])
                NdC += dy / k; NdAv += dA / k; NdCdA += dy * dA / k
        return NdCdA / NdC - (NdAv - NdCdA) / (n - NdC)
    classes, cnt = np.unique(y, return_counts=True); P = dict(zip(classes, cnt / n)); W = np.zeros(p)
    Dc = D.copy()
    for i in range(n):
        di = Dc[i]
        hit_idx = np.where(y == y[i])[0]; hit_idx = hit_idx[np.isfinite(di[hit_idx])]
        hits = hit_idx[np.argsort(di[hit_idx])[:k]]
        W -= np.abs(X[i] - X[hits]).mean(0) / n
        for c in classes:
            if c == y[i]: continue
            mi = np.where(y == c)[0]; mi = mi[np.isfinite(di[mi])]
            if len(mi) == 0: continue
            miss = mi[np.argsort(di[mi])[:k]]
            W += P[c] / (1 - P[y[i]]) * np.abs(X[i] - X[miss]).mean(0) / n
    return W

def vif_filter(F, thr=10.0):
    cols = list(F.columns); Z = (F - F.mean()) / (F.std() + 1e-12); hist = []
    while len(cols) > 1:
        Cm = np.corrcoef(Z[cols].values, rowvar=False)
        try: inv = np.linalg.inv(Cm)
        except np.linalg.LinAlgError: inv = np.linalg.pinv(Cm)
        v = np.diag(inv); j = int(np.argmax(v))
        if v[j] < thr: break
        hist.append((cols[j], float(v[j]))); cols.pop(j)
    Cm = np.corrcoef(Z[cols].values, rowvar=False) if len(cols) > 1 else np.ones((1, 1))
    final = dict(zip(cols, np.diag(np.linalg.pinv(Cm)).round(2) if len(cols) > 1 else [1.0]))
    return cols, final, hist
