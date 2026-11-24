"""Grouped, stratified hold-out split of the 48 field plots (used by the 70:30 and 80:20 pipelines and by the comparison script).

Rules (whole plots go to one side only, so leaves of one plot are never in both training and test):
  * healthy (fungicide-sprayed) block C and the unsprayed blocks R1-R3 are split separately (stratified by block type);
  * number of test plots = round(test fraction x plots) in each block type (70:30 -> 4 healthy + 11 unsprayed; 80:20 -> 2 + 7);
  * unsprayed test plots come from different treatments (sowing timing x variety) and are spread evenly over the
    replications, varieties and timings; healthy test plots have different varieties and timings where possible;
  * among many random candidates that meet these rules, the 'best' split is the one whose test set is closest to the
    target leaf fraction and to the overall distribution of grades and dates (fixed seed -> reproducible).
References: grouped / blocked validation (Roberts et al., 2017); stratified random hold-out (Kuhn and Johnson, 2013);
StratifiedGroupKFold idea in scikit-learn (Pedregosa et al., 2011); 70:30 and 80:20 ratios (Gholamy et al., 2018; Joseph, 2022)."""
import numpy as np, pandas as pd

BLK = lambda p: 'C' if p <= 12 else ('R3' if p <= 24 else ('R2' if p <= 36 else 'R1'))


def plot_table(M):
    """one row per plot: block, timing, variety, number of leaves"""
    g = M.groupby('plot').agg(block=('block', 'first'), timing=('timing', 'first'), variety=('variety', 'first'), n=('grade', 'size')).reset_index()
    return g


def _even(counts, k):
    """True if the counts of the k picked items are as even as possible over the levels"""
    lo = k // len(counts); return all(c in (lo, lo + 1) for c in counts)


def candidates(M, frac, n_cand=5000, seed=2026):
    P = plot_table(M); H = P[P.block == 'C'].reset_index(drop=True); U = P[P.block != 'C'].reset_index(drop=True)
    nh, nu = int(round(len(H) * frac)), int(round(len(U) * frac)); rng = np.random.default_rng(seed); out = set()
    V, T = ['V1', 'V2', 'V3'], ['D1', 'D2', 'D3', 'D4']; TR = [(t, v) for t in T for v in V]
    uplot = {(r.block, r.timing, r.variety): int(r['plot']) for _, r in U.iterrows()}
    hv, ht, hp = H.variety.values, H.timing.values, H['plot'].values
    even = lambda labels, levels, k: _even([sum(x == l for x in labels) for l in levels], k)
    tries = 0
    while len(out) < n_cand and tries < n_cand * 200:
        tries += 1
        it = rng.choice(len(TR), nu, replace=False); tv = [TR[i] for i in it]                 # nu different treatments
        if not (even([x[1] for x in tv], V, nu) and even([x[0] for x in tv], T, nu)): continue
        base = ['R1', 'R2', 'R3'] * (nu // 3); extra = list(rng.choice(['R1', 'R2', 'R3'], nu % 3, replace=False)); reps = base + extra; rng.shuffle(reps)
        ih = rng.choice(len(H), nh, replace=False)
        if not (even(hv[ih], V, nh) and even(ht[ih], T, nh)): continue
        out.add(tuple(sorted([int(x) for x in hp[ih]] + [uplot[(r, t, v)] for r, (t, v) in zip(reps, tv)])))
    return sorted(out)


class _Scorer:
    def __init__(self, M, frac):
        self.frac = frac; pl = M['plot'].values; self.plots = np.unique(pl); ix = {p: i for i, p in enumerate(self.plots)}
        gl = sorted(M.grade.unique()); dl = sorted(M.date.unique())
        self.G = np.zeros((len(self.plots), len(gl))); self.Dm = np.zeros((len(self.plots), len(dl)))
        np.add.at(self.G, ([ix[p] for p in pl], [gl.index(g) for g in M.grade]), 1); np.add.at(self.Dm, ([ix[p] for p in pl], [dl.index(d) for d in M.date]), 1)
        self.ix = ix; self.N = len(M); self.g0 = self.G.sum(0) / self.N; self.d0 = self.Dm.sum(0) / self.N
    def __call__(self, test_plots):
        i = [self.ix[p] for p in test_plots]; g = self.G[i].sum(0); d = self.Dm[i].sum(0); n = g.sum()
        return abs(n / self.N - self.frac) + 0.5 * (0.5 * np.abs(g / n - self.g0).sum() + 0.5 * np.abs(d / n - self.d0).sum())


def score(M, test_plots, frac):
    """distance of a candidate test set from the target: |leaf fraction - target| + half of the total-variation distances
    of the grade and date distributions (test vs all leaves)"""
    return _Scorer(M, frac)(test_plots)


def best_split(M, frac, seed=2026, n_cand=5000):
    C = candidates(M, frac, n_cand, seed); sc = _Scorer(M, frac); s = np.array([sc(c) for c in C]); i = int(np.argmin(s))
    return list(C[i]), dict(n_candidates=len(C), score=float(s[i]), score_median=float(np.median(s)))


def random_splits(M, frac, n, seed=7, n_cand=3000, tol=None):
    """n different rule-conforming splits drawn at random (for the split-to-split variability analysis); tol = keep only
    candidates whose score is below this value (None = the median score of all candidates)"""
    C = candidates(M, frac, n_cand, seed); sc = _Scorer(M, frac); s = np.array([sc(c) for c in C]); tol = np.median(s) if tol is None else tol
    ok = [c for c, v in zip(C, s) if v <= tol]; rng = np.random.default_rng(seed + 1); pick = rng.choice(len(ok), n, replace=False)
    return [list(ok[i]) for i in pick]


def describe(M, test_plots):
    te = M['plot'].isin(test_plots).values; P = plot_table(M); P['set'] = np.where(P['plot'].isin(test_plots), 'test', 'train')
    return P, dict(test_plots=sorted(int(p) for p in test_plots), n_test_plots=len(test_plots), n_train_plots=int(48 - len(test_plots)),
                   n_test_leaves=int(te.sum()), n_train_leaves=int((~te).sum()), test_leaf_fraction=float(te.mean()))
