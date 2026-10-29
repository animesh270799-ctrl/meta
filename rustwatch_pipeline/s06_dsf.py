"""Step 6 - Phase 1: Disease-Specific Feature (DSF) selection, run separately for each sensor.

6.1 quality control (missing values, near-zero variance, outlier flags)
6.2 Kruskal-Wallis across severity classes on each date + Benjamini-Hochberg FDR
    (+ Welch t-test healthy vs diseased, reported)
6.3 Jeffries-Matusita distance healthy vs each severity class; HS separability scalogram
6.4 ReliefF (multivariate filter)
6.5 Random-forest permutation importance (grouped CV) and Boruta (all-relevant)
6.6 consensus rule + stability over random half-samples of plots -> candidate DSFs
6.7 Spearman correlation with DI and correlation clustering (interpretation only)
Collinear features are NOT removed in this phase.
"""
import warnings
import numpy as np
import pandas as pd
from scipy.stats import kruskal, ttest_ind, spearmanr, binom
from scipy.spatial.distance import cdist, squareform
from scipy.cluster.hierarchy import linkage, fcluster
from statsmodels.stats.multitest import multipletests
from sklearn.ensemble import RandomForestClassifier
from sklearn.inspection import permutation_importance
from sklearn.model_selection import GroupKFold
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import config as C
from s01_layout import build_layout_table, load_ground_truth

warnings.filterwarnings("ignore", category=RuntimeWarning)
TARGET = "severity_class"
ID_COLS = ["plot_id", "date"]


# ------------------------------------------------------------------ data
def load_table(sensors):
    """Ground truth merged with the feature tables of the given sensors (one row per plot x date)."""
    df = load_ground_truth(build_layout_table())
    cols = []
    for s in sensors:
        f = pd.read_csv(C.FEAT / f"features_{s}.csv", dtype={"date": str})
        cols += [c for c in f.columns if c not in ID_COLS]
        df = df.merge(f, on=ID_COLS, how="inner")
    return df.reset_index(drop=True), cols


# ------------------------------------------------------------------ 6.1 quality control
def quality_control(df, cols, max_missing=0.05):
    keep, report = [], []
    for c in cols:
        x = df[c]
        if x.isna().mean() > max_missing:
            report.append((c, "missing")); continue
        vc = x.round(10).value_counts()
        freq_ratio = vc.iloc[0] / vc.iloc[1] if len(vc) > 1 else np.inf
        if freq_ratio > 19 and 100 * len(vc) / len(x) < 10:
            report.append((c, "near-zero variance")); continue
        keep.append(c)
    df = df.copy()
    df[keep] = df.groupby("date")[keep].transform(lambda s: s.fillna(s.median()))
    med = df.groupby("date")[keep].transform("median")
    mad = df.groupby("date")[keep].transform(lambda s: (s - s.median()).abs().median())
    mz = 0.6745 * (df[keep] - med) / mad.replace(0, np.nan)
    n_out = int((mz.abs() > 3.5).any(axis=1).sum())
    return df, keep, pd.DataFrame(report, columns=["feature", "reason"]), n_out


# ------------------------------------------------------------------ 6.2 statistics + FDR
def kruskal_p(df, c, target=TARGET):
    groups = [g[c].values for _, g in df.groupby(target) if len(g) >= 2]
    if len(groups) < 2:
        return np.nan, np.nan
    try:
        h, p = kruskal(*groups)
    except ValueError:            # all values identical
        return 0.0, 1.0
    return h, p


def stat_screen(df, cols, target=TARGET):
    res = pd.DataFrame(index=cols)
    sig_counts = pd.Series(0, index=cols)
    for date, g in df.groupby("date"):
        hp = np.array([kruskal_p(g, c, target) for c in cols])
        p = np.nan_to_num(hp[:, 1], nan=1.0)
        q = multipletests(p, method="fdr_bh")[1]
        res[f"q_{date}"] = q
        sig_counts += (q < C.FDR_Q).astype(int)
        hd = g[target] > 0
        res[f"t_p_{date}"] = [ttest_ind(g.loc[hd, c], g.loc[~hd, c], equal_var=False).pvalue
                              if hd.sum() > 1 and (~hd).sum() > 1 else np.nan for c in cols]
    hp_all = np.array([kruskal_p(df, c, target) for c in cols])
    res["H_pooled"] = hp_all[:, 0]
    res["q_pooled"] = multipletests(np.nan_to_num(hp_all[:, 1], nan=1.0), method="fdr_bh")[1]
    res["epsilon2"] = res["H_pooled"] / (len(df) - 1)
    res["n_dates_sig"] = sig_counts
    return res


# ------------------------------------------------------------------ 6.3 Jeffries-Matusita
def jm_1d(x1, x2):
    m1, m2 = np.mean(x1), np.mean(x2)
    v1, v2 = np.var(x1, ddof=1) + 1e-12, np.var(x2, ddof=1) + 1e-12
    b = (m1 - m2) ** 2 / (4 * (v1 + v2)) + 0.5 * np.log((v1 + v2) / (2 * np.sqrt(v1 * v2)))
    return 2 * (1 - np.exp(-b))


def jm_table(df, cols, target=TARGET):
    healthy = df[df[target] == 0]
    out = pd.DataFrame(index=cols)
    for k in sorted(df[target].unique()):
        if k == 0:
            continue
        d = df[df[target] == k]
        if len(d) >= 3 and len(healthy) >= 3:
            out[f"JM_0v{k}"] = [jm_1d(healthy[c].values, d[c].values) for c in cols]
    out["JM_max"] = out.max(axis=1) if out.shape[1] else np.nan
    return out


def is_hs_band(c):
    return c.startswith("HS_R") and c[4:].replace(".", "").isdigit()


def plot_scalogram(table, path):
    bands = [c for c in table.index if is_hs_band(c)]
    if not bands:
        return
    wl = np.array([float(c[4:]) for c in bands])
    o = np.argsort(wl)
    fig, ax = plt.subplots(figsize=(8, 3.5))
    for col in [c for c in table.columns if c.startswith("JM_0v")]:
        ax.plot(wl[o], table.loc[bands, col].values[o], lw=1, label=col.replace("JM_0v", "healthy vs class "))
    ax.axhline(C.JM_MIN_HS_BAND, color="k", ls="--", lw=1, label=f"JM = {C.JM_MIN_HS_BAND}")
    ax.set_xlabel("Wavelength (nm)"); ax.set_ylabel("JM distance"); ax.set_ylim(0, 2.05)
    ax.legend(fontsize=7, ncol=3); fig.tight_layout(); fig.savefig(path, dpi=150); plt.close(fig)


# ------------------------------------------------------------------ 6.4 ReliefF
def relieff(X, y, k=C.RELIEF_K):
    X = np.asarray(X, float)
    rng_ = X.max(0) - X.min(0)
    X = (X - X.min(0)) / np.where(rng_ == 0, 1, rng_)
    n, p = X.shape
    classes, counts = np.unique(y, return_counts=True)
    prior = dict(zip(classes, counts / n))
    D = cdist(X, X, "cityblock")
    np.fill_diagonal(D, np.inf)
    W = np.zeros(p)
    for i in range(n):
        same = np.where(y == y[i])[0]
        same = same[same != i]
        if len(same):
            h = same[np.argsort(D[i, same])[:k]]
            W -= np.abs(X[h] - X[i]).sum(0) / (n * len(h))
        for c in classes:
            if c == y[i]:
                continue
            other = np.where(y == c)[0]
            m = other[np.argsort(D[i, other])[:k]]
            W += prior[c] / (1 - prior[y[i]]) * np.abs(X[m] - X[i]).sum(0) / (n * len(m))
    return W


# ------------------------------------------------------------------ 6.5 RF importance + Boruta
def rf_permutation_importance(X, y, groups, n_trees=300, seed=C.RANDOM_STATE):
    imps = []
    for tr, te in GroupKFold(n_splits=C.INNER_FOLDS).split(X, y, groups):
        rf = RandomForestClassifier(n_trees, class_weight="balanced", random_state=seed, n_jobs=-1).fit(X[tr], y[tr])
        r = permutation_importance(rf, X[te], y[te], n_repeats=5, random_state=seed, scoring="f1_macro", n_jobs=-1)
        imps.append(r.importances_mean)
    return np.mean(imps, 0)


def boruta(X, y, n_iter=60, n_trees=200, alpha=0.01, seed=C.RANDOM_STATE):
    """Shadow-feature test (Kursa & Rudnicki, 2010). Returns 'confirmed' / 'tentative' / 'rejected'."""
    rng = np.random.default_rng(seed)
    n, p = X.shape
    hits = np.zeros(p)
    for it in range(n_iter):
        shadow = rng.permuted(X, axis=0)
        rf = RandomForestClassifier(n_trees, class_weight="balanced", random_state=seed + it, n_jobs=-1)
        rf.fit(np.hstack([X, shadow]), y)
        imp = rf.feature_importances_
        hits += imp[:p] > imp[p:].max()
    a = alpha / p                                           # Bonferroni
    confirmed = binom.sf(hits - 1, n_iter, 0.5) < a
    rejected = binom.cdf(hits, n_iter, 0.5) < a
    return np.where(confirmed, "confirmed", np.where(rejected, "rejected", "tentative")), hits / n_iter


# ------------------------------------------------------------------ 6.6 consensus + stability
def stability(df, cols, n_sub=C.BOOTSTRAP_N, seed=C.RANDOM_STATE):
    """Fraction of random half-samples of plots in which a feature passes FDR and is in the ReliefF top half."""
    rng = np.random.default_rng(seed)
    plots = df.plot_id.unique()
    freq = np.zeros(len(cols))
    for _ in range(n_sub):
        sub = df[df.plot_id.isin(rng.choice(plots, len(plots) // 2, replace=False))]
        p = np.array([kruskal_p(sub, c)[1] for c in cols])
        q = multipletests(np.nan_to_num(p, nan=1.0), method="fdr_bh")[1]
        w = relieff(sub[cols].values, sub[TARGET].values)
        freq += (q < C.FDR_Q) & (w > 0) & (w >= np.median(w))
    return freq / n_sub


def select_dsf(df, cols, fast=False, out_prefix=None):
    """Phase 1 for one sensor. Returns (DSF list, full table, consensus rank Series)."""
    df, cols, qc_report, n_out = quality_control(df, cols)
    X, y, g = df[cols].values, df[TARGET].values, df.plot_id.values
    t = stat_screen(df, cols)
    t = t.join(jm_table(df, cols))
    t["relief"] = relieff(X, y)
    t["rf_perm"] = rf_permutation_importance(X, y, g, n_trees=100 if fast else 300)
    t["boruta"], t["boruta_hits"] = boruta(X, y, n_iter=20 if fast else 60, n_trees=100 if fast else 200)

    t["pass_stat"] = t["n_dates_sig"] >= C.MIN_DATES_SIGNIFICANT
    jm_thr = np.where([is_hs_band(c) for c in cols], C.JM_MIN_HS_BAND, C.JM_MIN_DERIVED)
    t["pass_sep"] = t["JM_max"].fillna(0).values >= jm_thr
    t["vote_relief"] = (t["relief"] > 0) & (t["relief"] >= t["relief"].median())
    t["vote_rf"] = t["rf_perm"] >= t["rf_perm"].median()
    t["vote_boruta"] = t["boruta"] == "confirmed"
    t["votes"] = t[["vote_relief", "vote_rf", "vote_boruta"]].sum(1)
    candidate = t["pass_stat"] & t["pass_sep"] & (t["votes"] >= 2)
    if not fast:
        t["stability"] = 0.0
        if candidate.any():
            t.loc[candidate, "stability"] = stability(df, list(t.index[candidate]))
        candidate &= t["stability"] >= C.STABILITY_MIN
    t["DSF"] = candidate

    ranks = pd.concat([t["q_pooled"].rank(), t["JM_max"].rank(ascending=False),
                       t["relief"].rank(ascending=False), t["rf_perm"].rank(ascending=False)], axis=1)
    t["consensus_rank"] = ranks.mean(1).rank()
    dsf = list(t.index[t["DSF"]])
    if len(dsf) < 3:          # never leave a sensor empty: fall back to the best-ranked features
        dsf = list(t.sort_values("consensus_rank").index[:5])
        t["DSF_fallback"] = t.index.isin(dsf)

    if out_prefix is not None:
        C.DSF.mkdir(parents=True, exist_ok=True)
        t["rho_DI"] = [spearmanr(df[c], df["DI"])[0] for c in cols]
        if len(dsf) > 2:
            rho = df[dsf].corr("spearman").abs().fillna(0).values
            dist = squareform(1 - rho, checks=False)
            t.loc[dsf, "cluster"] = fcluster(linkage(dist, "average"), t=0.3, criterion="distance")
        t.sort_values("consensus_rank").to_csv(C.DSF / f"{out_prefix}_feature_table.csv")
        qc_report.to_csv(C.DSF / f"{out_prefix}_qc_removed.csv", index=False)
        plot_scalogram(t, C.DSF / f"{out_prefix}_JM_scalogram.png")
        print(f"{out_prefix}: {len(cols)} features after QC, {n_out} plot-dates flagged as outliers, "
              f"{len(dsf)} DSFs")
    return dsf, t, t["consensus_rank"]


if __name__ == "__main__":
    for s in C.SENSORS:
        d, cols = load_table([s])
        dsf, _, _ = select_dsf(d, cols, out_prefix=s)
        print(s, "DSFs:", dsf[:15], "..." if len(dsf) > 15 else "")
