"""Shared methods: ReliefF, correlated regions, scalogram, band combination, VIF, stepwise CDA, Boruta."""
import numpy as np, pandas as pd
from scipy import stats
from scipy.spatial.distance import cdist
from sklearn.linear_model import LinearRegression

def minmax(X):
    lo, hi = X.min(0), X.max(0); return (X - lo) / np.where(hi - lo > 0, hi - lo, 1)

def relieff(X, y, groups=None, k=10, Xdist=None, Xupd=None):
    """Multi-class ReliefF (Robnik-Sikonja and Kononenko, 2003). Neighbours from Xdist (default X), weights for Xupd (default X).
    Neighbours from the same group (plot) are excluded."""
    Xd = minmax(X if Xdist is None else Xdist); Xu = minmax(X if Xupd is None else Xupd)
    D = cdist(Xd, Xd, 'cityblock'); np.fill_diagonal(D, np.inf)
    if groups is not None: D[groups[:, None] == groups[None, :]] = np.inf
    cls, cnt = np.unique(y, return_counts=True); P = dict(zip(cls, cnt / len(y)))
    W = np.zeros(Xu.shape[1]); m = len(y)
    order = np.argsort(D, axis=1)
    for i in range(m):
        oi = order[i]; yi = y[oi]; fin = np.isfinite(D[i, oi])
        hits = oi[(yi == y[i]) & fin][:k]
        W -= np.abs(Xu[hits] - Xu[i]).sum(0) / (m * k)
        for c in cls:
            if c == y[i]: continue
            miss = oi[(yi == c) & fin][:k]
            W += P[c] / (1 - P[y[i]]) * np.abs(Xu[miss] - Xu[i]).sum(0) / (m * k)
    return W

def regions(X, wl, thr=0.95, gap=5):
    """Contiguous correlated regions: a region starts at a band and grows while r(start band, band) >= thr and bands are adjacent."""
    C = np.corrcoef(X.T); reg = np.zeros(len(wl), int); r_id = 0; s = 0
    for j in range(1, len(wl)):
        if wl[j] - wl[j - 1] > gap or C[s, j] < thr: r_id += 1; s = j
        reg[j] = r_id
    return reg

def scalogram(B, y):
    """Pearson r and p of every band feature with y."""
    out = {}
    for t, A in B.items():
        r = np.array([stats.pearsonr(A[:, j], y)[0] for j in range(A.shape[1])])
        n = len(y); tt = r * np.sqrt((n - 2) / (1 - r ** 2)); p = 2 * stats.t.sf(np.abs(tt), n - 2)
        out[t] = (r, p)
    return out

def select_bands(Bleaf, Bplot, wl, ycls, groups, ypdi, top=0.05, thr=0.95, k=10):
    """HS Tier 2: scalogram (plot level, PDI) + ReliefF (leaf level, grades); one band per correlated region; combine lists."""
    types = list(Bleaf)
    sc = scalogram(Bplot, ypdi)
    Xall = np.hstack([Bleaf[t] for t in types]); feat = [(t, w) for t in types for w in wl]
    W = relieff(Xall, ycls, groups, k=k)
    reg = {t: regions(Bleaf[t], wl, thr) for t in types}
    # scalogram candidates: p < 0.01 and top 5% |r| within each spectrum type
    scand = []
    for t in types:
        r, p = sc[t]; cut = np.quantile(np.abs(r), 1 - top)
        for j in np.where((p < 0.01) & (np.abs(r) >= cut))[0]: scand.append((t, j, abs(r[j])))
    cut = np.quantile(W, 1 - top); rcand = [(feat[q][0], wl.tolist().index(feat[q][1]), W[q]) for q in np.where(W >= cut)[0]]
    # derivative features within 10 nm of the detector splice (1000 nm) or a removed water band edge are artefact-prone: not eligible
    edge = lambda t, w: t in ('FD', 'SD') and any(abs(w - e) <= 10 for e in (1000, 1350, 1450, 1800, 1950))
    scand = [c for c in scand if not edge(c[0], wl[c[1]])]; rcand = [c for c in rcand if not edge(c[0], wl[c[1]])]
    def one_per_region(c):
        best = {}
        for t, j, s in c:
            key = (t, reg[t][j])
            if key not in best or s > best[key][2]: best[key] = (t, j, s)
        return sorted(best.values(), key=lambda x: -x[2])
    S1, R1 = one_per_region(scand), one_per_region(rcand)
    robust, regonly, clsonly = [], [], []
    used_r = set()
    for t, j, s in S1:
        match = [q for q in R1 if q[0] == t and (reg[t][q[1]] == reg[t][j] or abs(wl[q[1]] - wl[j]) <= 10)]
        if match: robust.append((t, int(wl[j]))); used_r |= {(q[0], q[1]) for q in match}
        else: regonly.append((t, int(wl[j])))
    clsonly = [(t, int(wl[j])) for t, j, s in R1 if (t, j) not in used_r]
    return dict(sc=sc, W=W, feat=feat, reg=reg, scand=scand, rcand=rcand, S1=S1, R1=R1, robust=robust, regonly=regonly, clsonly=clsonly)

def vif_filter(Xdf, thr=10.0, log=None):
    cols = list(Xdf.columns)
    while len(cols) > 1:
        X = Xdf[cols].values; X = (X - X.mean(0)) / X.std(0)
        v = []
        for j in range(len(cols)):
            o = np.delete(X, j, 1); r2 = LinearRegression().fit(o, X[:, j]).score(o, X[:, j]); v.append(1 / max(1 - r2, 1e-9))
        v = np.array(v); jm = v.argmax()
        if log is not None: log.append((len(cols), cols[jm], float(v[jm])))
        if v[jm] < thr: break
        cols.pop(jm)
    return cols

def _wilks(X, y, cols):
    Xs = X[:, cols]; T = np.cov(Xs.T, bias=True) * len(y)
    W = sum(np.cov(Xs[y == c].T, bias=True) * (y == c).sum() for c in np.unique(y))
    T = np.atleast_2d(T); W = np.atleast_2d(W)
    return np.linalg.det(W) / np.linalg.det(T)

def stepwise_cda(Xdf, y, p_in=0.001, p_out=0.01, max_vars=10):
    """Forward stepwise discriminant selection with Wilks' lambda and partial F (Klecka, 1980; Bhattacharya and Chattopadhyay, 2013)."""
    X = Xdf.values.astype(float); X = (X - X.mean(0)) / X.std(0); names = list(Xdf.columns)
    n, g = len(y), len(np.unique(y)); sel = []; steps = []
    while len(sel) < max_vars:
        lam0 = _wilks(X, y, sel) if sel else 1.0; p = len(sel); best = None
        for j in range(X.shape[1]):
            if j in sel: continue
            lam1 = _wilks(X, y, sel + [j]); F = (n - g - p) / (g - 1) * (lam0 / lam1 - 1); pv = stats.f.sf(F, g - 1, n - g - p)
            if best is None or lam1 < best[1]: best = (j, lam1, F, pv)
        if best is None or best[3] > p_in: break
        sel.append(best[0]); steps.append(dict(step=len(sel), entered=names[best[0]], wilks=best[1], F=best[2], p=best[3]))
        # removal check
        if len(sel) > 2:
            lam = _wilks(X, y, sel); p = len(sel)
            for j in list(sel[:-1]):
                rest = [q for q in sel if q != j]; F = (n - g - p + 1) / (g - 1) * (_wilks(X, y, rest) / lam - 1)
                if stats.f.sf(F, g - 1, n - g - p + 1) > p_out: sel.remove(j); steps.append(dict(step=len(sel), entered='removed ' + names[j], wilks=_wilks(X, y, sel), F=F, p=np.nan))
    return [names[j] for j in sel], steps

def canonical(Xdf, y):
    """Canonical discriminant functions: eigenvalues of W^-1 B, canonical correlations, standardised coefficients, structure r, scores."""
    X = Xdf.values.astype(float); mu = X.mean(0); cls = np.unique(y)
    W = sum(np.cov(X[y == c].T, bias=True) * (y == c).sum() for c in cls)
    B = sum((y == c).sum() * np.outer(X[y == c].mean(0) - mu, X[y == c].mean(0) - mu) for c in cls)
    W, B = np.atleast_2d(W), np.atleast_2d(B)
    ev, V = np.linalg.eig(np.linalg.solve(W, B)); ev, V = np.real(ev), np.real(V)
    o = np.argsort(ev)[::-1]; q = min(len(cls) - 1, X.shape[1]); ev, V = ev[o][:q], V[:, o][:, :q]
    sw = np.sqrt(np.diag(W) / (len(y) - len(cls)))
    Vn = V / np.sqrt(np.diag(V.T @ (W / (len(y) - len(cls))) @ V))        # unit within-group variance of scores
    scores = (X - mu) @ Vn
    std_coef = Vn * sw[:, None]
    struct = np.array([[np.corrcoef(X[:, i], scores[:, f])[0, 1] for f in range(q)] for i in range(X.shape[1])])
    cancor = np.sqrt(ev / (1 + ev)); wilks = np.prod(1 / (1 + ev))
    cent = np.array([scores[y == c].mean(0) for c in cls])
    return dict(ev=ev, cancor=cancor, wilks=wilks, std_coef=std_coef, struct=struct, scores=scores, centroids=cent, share=ev / ev.sum())

def boruta(X, y, task, seed=0, max_iter=100):
    from boruta import BorutaPy
    from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor
    rf = (RandomForestClassifier(n_jobs=-1, class_weight='balanced', max_depth=7, random_state=seed) if task == 'c'
          else RandomForestRegressor(n_jobs=-1, max_depth=7, random_state=seed))
    b = BorutaPy(rf, n_estimators='auto', alpha=0.01, max_iter=max_iter, random_state=seed, verbose=0)
    b.fit(np.asarray(X, float), np.asarray(y))
    return b

def tukey_letters(df, val, grp, order):
    from statsmodels.stats.multicomp import pairwise_tukeyhsd
    t = pairwise_tukeyhsd(df[val], df[grp], alpha=0.05)
    res = pd.DataFrame(t._results_table.data[1:], columns=t._results_table.data[0])
    ns = {(str(a), str(b)) for a, b, rej in zip(res.group1, res.group2, res.reject) if not rej}
    ns |= {(b, a) for a, b in ns}
    means = df.groupby(grp)[val].mean()
    srt = sorted(order, key=lambda g: -means[g]); letters = {g: '' for g in order}; groups_ = []
    for g in srt:
        placed = False
        for li, members in enumerate(groups_):
            if all((str(g), str(m)) in ns for m in members): members.append(g); letters[g] += 'abcdefghij'[li]; placed = True
        if not placed: groups_.append([g]); letters[g] += 'abcdefghij'[len(groups_) - 1]
    # second pass: a group gets every letter whose members are all non-different from it
    for li, members in enumerate(groups_):
        for g in order:
            if 'abcdefghij'[li] not in letters[g] and all((str(g), str(m)) in ns for m in members): letters[g] += 'abcdefghij'[li]
    return {g: ''.join(sorted(letters[g])) for g in order}
