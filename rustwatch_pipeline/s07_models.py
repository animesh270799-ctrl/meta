"""Step 7 - Phases 2 and 3: redundancy removal, SFFS, classifiers and nested grouped CV.

7.1 relevance-guided VIF (< 10)          (per sensor in Phase 2, pooled in Phase 3)
7.2 SPA for raw hyperspectral bands      (bands are p >> n, so VIF cannot be used)
7.3 SFFS per classifier (mlxtend, floating=True), inner CV grouped by plot,
    subset size by the one-standard-error rule -> OFC
7.4 hyperparameter tuning on the OFC (GridSearchCV, inner grouped CV)
7.5 nested, plot-grouped, repeated outer CV; Phase 1 is re-run inside every outer
    training fold so no label information leaks into the test fold
7.6 metrics: OA, macro-F1, kappa, per-class precision / recall / specificity
"""
import os
import warnings
import numpy as np
import pandas as pd
from sklearn.base import clone
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestClassifier
from sklearn.svm import SVC
from sklearn.neighbors import KNeighborsClassifier
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis
from sklearn.model_selection import GroupKFold, StratifiedGroupKFold, GridSearchCV, cross_val_score
from sklearn.metrics import accuracy_score, f1_score, cohen_kappa_score, confusion_matrix
from mlxtend.feature_selection import SequentialFeatureSelector as SFS
import config as C
from s06_dsf import select_dsf, is_hs_band, TARGET

warnings.filterwarnings("ignore")
FAST = os.environ.get("RW_FAST") == "1"     # quick settings for testing the code


def pipe(clf):
    return Pipeline([("imp", SimpleImputer(strategy="median")), ("sc", StandardScaler()), ("clf", clf)])


def classifiers():
    rs = C.RANDOM_STATE
    n_trees = 60 if FAST else 300
    return {
        "RF": (pipe(RandomForestClassifier(n_trees, class_weight="balanced", random_state=rs, n_jobs=-1)),
               {"clf__max_features": ["sqrt", 0.5], "clf__min_samples_leaf": [1, 3]}),
        "SVM": (pipe(SVC(kernel="rbf", class_weight="balanced", random_state=rs)),
                {"clf__C": 2.0 ** np.arange(-3, 12, 2), "clf__gamma": 2.0 ** np.arange(-11, 2, 2)}),
        "KNN": (pipe(KNeighborsClassifier()),
                {"clf__n_neighbors": [3, 5, 7, 9, 11, 15], "clf__weights": ["uniform", "distance"]}),
    }


def inner_cv(groups, n=None):
    return GroupKFold(n_splits=n or C.INNER_FOLDS)


# ------------------------------------------------------------------ 7.1 VIF
def vif_values(X):
    R = np.corrcoef(np.asarray(X, float), rowvar=False)
    return np.diag(np.linalg.pinv(R))              # VIF_j = (R^-1)_jj


def vif_filter(X, rank, thresh=C.VIF_MAX):
    """Iteratively drop, among features with VIF >= thresh, the one with the WORST Phase 1 rank."""
    feats = list(X.columns)
    removed = []
    while len(feats) > 1:
        v = vif_values(X[feats].fillna(X[feats].median()))
        if np.nanmax(v) < thresh:
            break
        high = [f for f, vi in zip(feats, v) if vi >= thresh]
        drop = max(high, key=lambda f: rank.get(f, np.inf))
        feats.remove(drop)
        removed.append(drop)
    return feats, removed


# ------------------------------------------------------------------ 7.2 SPA
def spa_chains(X, max_vars):
    """Successive Projections Algorithm (Araujo et al., 2001): one chain per starting band."""
    Xc = X - X.mean(0)
    p = Xc.shape[1]
    starts = range(p) if p <= 60 else np.linspace(0, p - 1, 60).astype(int)
    chains = []
    for k0 in starts:
        sel, Xp = [int(k0)], Xc.copy()
        for _ in range(min(max_vars, p) - 1):
            xk = Xp[:, sel[-1]].copy()
            Xp = Xp - np.outer(xk, xk @ Xp) / (xk @ xk + 1e-12)
            norms = np.linalg.norm(Xp, axis=0)
            norms[sel] = -1
            sel.append(int(np.argmax(norms)))
        chains.append(sel)
    return chains


def spa_select(Xdf, y, groups, max_vars=10):
    """Pick the chain prefix with the best grouped-CV accuracy of LDA (SPA-LDA, Pontes et al., 2005)."""
    X = Xdf.fillna(Xdf.median()).values
    cv = list(inner_cv(groups).split(X, y, groups))
    best, best_set = -np.inf, None
    for chain in spa_chains(X, max_vars):
        for m in range(2, len(chain) + 1):
            s = cross_val_score(LinearDiscriminantAnalysis(), X[:, chain[:m]], y, cv=cv, scoring="f1_macro").mean()
            if s > best:
                best, best_set = s, chain[:m]
    return [Xdf.columns[i] for i in best_set]


# ------------------------------------------------------------------ 7.3 SFFS
def sffs(estimator, X, y, groups, max_k=C.SFFS_MAX_FEATURES):
    cv = list(inner_cv(groups).split(X, y, groups))
    k_hi = min(max_k if not FAST else 6, X.shape[1])
    sfs = SFS(clone(estimator), k_features=(1, k_hi), forward=True, floating=True,
              scoring="f1_macro", cv=cv, n_jobs=-1)
    sfs.fit(X, y)
    res = sfs.subsets_
    best_k = max(res, key=lambda k: res[k]["avg_score"])
    se = np.std(res[best_k]["cv_scores"], ddof=1) / np.sqrt(len(cv))
    k_sel = min(k for k in res if res[k]["avg_score"] >= res[best_k]["avg_score"] - se)   # one-SE rule
    return list(res[k_sel]["feature_names"]), pd.DataFrame(
        [(k, v["avg_score"], ";".join(v["feature_names"])) for k, v in res.items()], columns=["k", "macro_F1", "features"])


# ------------------------------------------------------------------ 7.4 per-fold model building
def sensor_of(col):
    return col.split("_")[0]


def dsf_for_sensor(train, sensor_cols, sensor, fast=True):
    dsf, _, rank = select_dsf(train, sensor_cols, fast=fast)
    if sensor == "HS":
        bands = [f for f in dsf if is_hs_band(f)]
        if len(bands) > 10:
            bands = spa_select(train[bands], train[TARGET].values, train.plot_id.values)
        dsf = bands + [f for f in dsf if not is_hs_band(f)]
    return dsf, rank


def build_model(train, dsf_by_sensor, rank_by_sensor, sensors, clf_name):
    feats = [f for s in sensors for f in dsf_by_sensor[s]]
    rank = pd.concat([rank_by_sensor[s] for s in sensors])
    feats, _ = vif_filter(train[feats], rank)
    est, grid = classifiers()[clf_name]
    y, g = train[TARGET].values, train.plot_id.values
    ofc, _ = sffs(est, train[feats], y, g)
    gs = GridSearchCV(clone(est), grid, scoring="f1_macro", cv=list(inner_cv(g).split(train, y, g)), n_jobs=-1)
    gs.fit(train[ofc], y)
    return dict(model=gs.best_estimator_, ofc=ofc, after_vif=feats, params=gs.best_params_)


# ------------------------------------------------------------------ 7.5 nested CV
def run_nested(df, feature_cols, configs, clf_names=("RF", "SVM", "KNN"), n_repeats=None, outer_folds=None):
    """configs: dict name -> list of sensors, e.g. {"MS": ["MS"], "F2_MS+TIR": ["MS", "TIR"]}.
    Phase 1 runs once per sensor per outer fold and is shared by all configurations."""
    y, g = df[TARGET].values, df.plot_id.values
    preds, picks = [], []
    sensors_needed = sorted({s for v in configs.values() for s in v})
    for rep in range(n_repeats or (1 if FAST else C.N_REPEATS)):
        outer = StratifiedGroupKFold(n_splits=outer_folds or C.OUTER_FOLDS, shuffle=True, random_state=C.RANDOM_STATE + rep)
        for fold, (tr, te) in enumerate(outer.split(df, y, g)):
            train, test = df.iloc[tr], df.iloc[te]
            dsf, rank = {}, {}
            for s in sensors_needed:
                dsf[s], rank[s] = dsf_for_sensor(train, [c for c in feature_cols if sensor_of(c) == s], s)
            for name, sensors in configs.items():
                for clf in clf_names:
                    m = build_model(train, dsf, rank, sensors, clf)
                    yp = m["model"].predict(test[m["ofc"]])
                    preds.append(pd.DataFrame(dict(config=name, clf=clf, repeat=rep, fold=fold, row=test.index,
                                                   plot_id=test.plot_id.values, date=test.date.values,
                                                   y_true=test[TARGET].values, y_pred=yp)))
                    picks.append(dict(config=name, clf=clf, repeat=rep, fold=fold, n_after_vif=len(m["after_vif"]),
                                      ofc=";".join(m["ofc"]), params=str(m["params"])))
                    print(f"rep {rep} fold {fold} {name:<14} {clf:<4} OFC={len(m['ofc'])} "
                          f"F1={f1_score(test[TARGET], yp, average='macro', zero_division=0):.2f}")
    return pd.concat(preds, ignore_index=True), pd.DataFrame(picks)


# ------------------------------------------------------------------ 7.6 metrics
def specificity_per_class(cm):
    out = []
    for k in range(cm.shape[0]):
        tn = cm.sum() - cm[k].sum() - cm[:, k].sum() + cm[k, k]
        fp = cm[:, k].sum() - cm[k, k]
        out.append(tn / (tn + fp) if tn + fp else np.nan)
    return out


def summarize(preds):
    rows = []
    for (cfg, clf), d in preds.groupby(["config", "clf"]):
        per_rep = d.groupby("repeat").apply(lambda r: pd.Series(dict(
            OA=accuracy_score(r.y_true, r.y_pred),
            macro_F1=f1_score(r.y_true, r.y_pred, average="macro", zero_division=0),
            kappa=cohen_kappa_score(r.y_true, r.y_pred))), include_groups=False)
        rows.append(dict(config=cfg, clf=clf, **{f"{m}_mean": per_rep[m].mean() for m in per_rep},
                         **{f"{m}_sd": per_rep[m].std(ddof=1) for m in per_rep}))
    return pd.DataFrame(rows).sort_values("macro_F1_mean", ascending=False)


def class_report(preds, cfg, clf):
    d = preds[(preds.config == cfg) & (preds.clf == clf)]
    labels = sorted(set(d.y_true) | set(d.y_pred))
    cm = confusion_matrix(d.y_true, d.y_pred, labels=labels)
    rec = np.diag(cm) / cm.sum(1).clip(min=1)
    prec = np.diag(cm) / cm.sum(0).clip(min=1)
    return cm, pd.DataFrame(dict(cls=labels, precision=prec, recall=rec, specificity=specificity_per_class(cm)))
