"""Step 8 - Single-sensor vs multi-sensor comparison, final model, SHAP, maps, regression.

8.1 nested CV for the 4 single sensors (Phase 2) and the 4 fusion scenarios (Phase 3)
8.2 fusion gain = best fused macro-F1 - best single-sensor macro-F1; McNemar test
8.3 final model on all data for the best configuration; robust cross-classifier features
8.4 SHAP explanation and sensor contributions
8.5 severity map and three-zone spray map for every flight date
8.6 regression of the continuous Disease Index (R2, RMSE, RE) with grouped CV
"""
import numpy as np
import pandas as pd
import geopandas as gpd
import shap
from collections import Counter
from statsmodels.stats.contingency_tables import mcnemar
from sklearn.ensemble import RandomForestRegressor
from sklearn.calibration import CalibratedClassifierCV
from sklearn.base import clone
from sklearn.model_selection import GroupKFold
from sklearn.metrics import r2_score, mean_squared_error
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Patch
import config as C
from s06_dsf import load_table, TARGET
from s07_models import (run_nested, summarize, class_report, dsf_for_sensor, build_model, sensor_of, FAST)

SINGLE = {s: [s] for s in C.SENSORS}
FUSION = {"F1_RGB+TIR": ["RGB", "TIR"], "F2_MS+TIR": ["MS", "TIR"],
          "F3_HS+TIR": ["HS", "TIR"], "F4_ALL": ["RGB", "MS", "HS", "TIR"]}
ZONE = {0: "Green", 1: "Green", 2: "Amber", 3: "Amber", 4: "Red", 5: "Red"}   # agree with pathologists
ZONE_COLOUR = {"Green": "#3E7B4F", "Amber": "#E0A526", "Red": "#A63A2A"}
CLASS_COLOUR = ["#2E7D32", "#9CCC65", "#FFEE58", "#FFA726", "#EF5350", "#8E0000"]


# ------------------------------------------------------------------ 8.2 fusion gain + McNemar
def mcnemar_test(preds, a, b, repeat=0):
    """a, b = (config, clf). Paired on the same rows of the same outer-CV repeat."""
    pa = preds[(preds.config == a[0]) & (preds.clf == a[1]) & (preds.repeat == repeat)].set_index("row")
    pb = preds[(preds.config == b[0]) & (preds.clf == b[1]) & (preds.repeat == repeat)].set_index("row")
    ca, cb = (pa.y_true == pa.y_pred), (pb.y_true == pb.y_pred).reindex(pa.index)
    table = [[(ca & cb).sum(), (ca & ~cb).sum()], [(~ca & cb).sum(), (~ca & ~cb).sum()]]
    return mcnemar(table, exact=True).pvalue


def fusion_gain(summary, preds):
    single = summary[summary.config.isin(SINGLE)]
    fused = summary[summary.config.isin(FUSION)]
    rows = []
    for clf in summary.clf.unique():
        bs = single[single.clf == clf].iloc[0]
        for _, f in fused[fused.clf == clf].iterrows():
            rows.append(dict(clf=clf, fusion=f.config, best_single=bs.config,
                             gain_macro_F1=f.macro_F1_mean - bs.macro_F1_mean, gain_OA=f.OA_mean - bs.OA_mean,
                             mcnemar_p=mcnemar_test(preds, (f.config, clf), (bs.config, clf))))
    return pd.DataFrame(rows)


# ------------------------------------------------------------------ 8.3 final model
def final_model(df, cols, sensors, clf):
    dsf, rank = {}, {}
    for s in sensors:
        dsf[s], rank[s] = dsf_for_sensor(df, [c for c in cols if sensor_of(c) == s], s, fast=False)
    return build_model(df, dsf, rank, sensors, clf)


def robust_features(picks, config):
    """Features chosen in >= 2 of the 3 classifiers' OFCs, counted over all outer folds."""
    d = picks[picks.config == config]
    per_clf = {clf: Counter(f for o in g.ofc for f in o.split(";")) for clf, g in d.groupby("clf")}
    n_folds = d.groupby("clf").size().max()
    feats = set().union(*per_clf.values())
    rows = [dict(feature=f, **{f"{clf}_freq": per_clf[clf][f] / n_folds for clf in per_clf}) for f in feats]
    t = pd.DataFrame(rows)
    t["n_classifiers"] = (t.filter(like="_freq") >= 0.5).sum(1)
    return t.sort_values("n_classifiers", ascending=False)


# ------------------------------------------------------------------ 8.4 SHAP
def probability_function(clf, Xs, y):
    """Class probabilities for Kernel SHAP. SVC has no predict_proba unless calibrated."""
    try:
        clf.predict_proba(Xs[:1])
        return clf.predict_proba
    except AttributeError:
        pass
    n_min = int(pd.Series(y).value_counts().min())
    if n_min >= 2:
        cal = CalibratedClassifierCV(clone(clf), cv=min(3, n_min)).fit(Xs, y)
        return cal.predict_proba
    classes = np.unique(y)                              # last resort: explain the predicted label
    return lambda X: (clf.predict(X)[:, None] == classes[None]).astype(float)


def shap_importance(model, X, y):
    pre = model[:-1]
    clf = model.named_steps["clf"]
    Xs = pre.transform(X)
    if clf.__class__.__name__ == "RandomForestClassifier":
        sv = np.array(shap.TreeExplainer(clf).shap_values(Xs))
    else:
        bg = shap.kmeans(Xs, min(10, len(Xs)))
        sv = np.array(shap.KernelExplainer(probability_function(clf, Xs, y), bg).shap_values(Xs, nsamples=100, silent=True))
    n, p = X.shape
    if sv.ndim == 2:
        imp = np.abs(sv).mean(0)
    elif sv.shape[0] == n and sv.shape[1] == p:      # (samples, features, classes)
        imp = np.abs(sv).mean((0, 2))
    else:                                           # (classes, samples, features)
        imp = np.abs(sv).mean((0, 1))
    s = pd.Series(imp, index=X.columns).sort_values(ascending=False)
    contrib = s.groupby(lambda c: sensor_of(c)).sum()
    return s, contrib / contrib.sum()


# ------------------------------------------------------------------ 8.5 maps
def make_maps(df, fm, tag):
    plots = gpd.read_file(C.PLOTS_FILE)
    C.MAPS.mkdir(parents=True, exist_ok=True)
    out = []
    for date, d in df.groupby("date"):
        pred = pd.DataFrame(dict(plot_id=d.plot_id.values, pred_class=fm["model"].predict(d[fm["ofc"]]),
                                 true_class=d[TARGET].values))
        pred["zone"] = pred.pred_class.map(ZONE)
        g = plots.merge(pred, on="plot_id")
        g["date"] = date
        out.append(g)
        fig, axes = plt.subplots(1, 2, figsize=(13, 4.5))
        g.plot(ax=axes[0], color=[CLASS_COLOUR[c] for c in g.pred_class], edgecolor="k", lw=0.5)
        axes[0].legend(handles=[Patch(color=CLASS_COLOUR[k], label=f"{k} {n}") for k, n in enumerate(C.CLASS_NAMES)],
                       fontsize=7, loc="upper left", bbox_to_anchor=(1, 1))
        axes[0].set_title(f"Predicted severity class, {date}")
        g.plot(ax=axes[1], color=[ZONE_COLOUR[z] for z in g.zone], edgecolor="k", lw=0.5)
        axes[1].legend(handles=[Patch(color=c, label=z) for z, c in ZONE_COLOUR.items()],
                       fontsize=8, loc="upper left", bbox_to_anchor=(1, 1))
        axes[1].set_title("Spray decision: Green skip / Amber spray / Red too late")
        for ax in axes:
            for _, r in g.iterrows():
                ax.annotate(str(r.plot_id), r.geometry.centroid.coords[0], ha="center", va="center", fontsize=6)
            ax.set_axis_off()
        fig.tight_layout(); fig.savefig(C.MAPS / f"{tag}_{date}_maps.png", dpi=150); plt.close(fig)
    allg = pd.concat(out)
    gpd.GeoDataFrame(allg, crs=plots.crs).to_file(C.MAPS / f"{tag}_predictions.gpkg", layer="predictions")
    return allg


# ------------------------------------------------------------------ 8.6 regression of DI
def di_regression(df, cols, sensors, n_folds=None):
    preds = np.full(len(df), np.nan)
    g = df.plot_id.values
    for tr, te in GroupKFold(n_splits=n_folds or C.OUTER_FOLDS).split(df, df.DI, g):
        train = df.iloc[tr]
        feats = []
        for s in sensors:
            feats += dsf_for_sensor(train, [c for c in cols if sensor_of(c) == s], s)[0]
        rf = RandomForestRegressor(300, random_state=C.RANDOM_STATE, n_jobs=-1)
        rf.fit(train[feats].fillna(train[feats].median()), train.DI)
        preds[te] = rf.predict(df.iloc[te][feats].fillna(train[feats].median()))
    rmse = mean_squared_error(df.DI, preds) ** 0.5
    return dict(R2=float(r2_score(df.DI, preds)), RMSE=float(rmse), RE_pct=float(100 * rmse / df.DI.mean())), preds


# ------------------------------------------------------------------ driver
def main():
    C.MODELS.mkdir(parents=True, exist_ok=True)
    df, cols = load_table(C.SENSORS)
    print(f"{len(df)} plot-date observations, {df.plot_id.nunique()} plots, {len(cols)} features")
    configs = {**SINGLE, **FUSION}
    preds, picks = run_nested(df, cols, configs)
    preds.to_csv(C.MODELS / "outer_cv_predictions.csv", index=False)
    picks.to_csv(C.MODELS / "selected_features_per_fold.csv", index=False)
    summary = summarize(preds)
    summary.to_csv(C.MODELS / "performance_summary.csv", index=False)
    print(summary.round(3).to_string(index=False))

    gain = fusion_gain(summary, preds)
    gain.to_csv(C.MODELS / "fusion_gain.csv", index=False)
    print(gain.round(3).to_string(index=False))

    best = summary.iloc[0]
    cm, rep = class_report(preds, best.config, best.clf)
    pd.DataFrame(cm).to_csv(C.MODELS / "best_confusion_matrix.csv")
    rep.to_csv(C.MODELS / "best_class_report.csv", index=False)
    robust = robust_features(picks, best.config)
    robust.to_csv(C.MODELS / f"robust_features_{best.config}.csv", index=False)

    sensors = configs[best.config]
    fm = final_model(df, cols, sensors, best.clf)
    pd.Series(fm["ofc"]).to_csv(C.MODELS / "final_OFC.csv", index=False, header=["feature"])
    print(f"Final model: {best.config} / {best.clf}; OFC = {fm['ofc']}; params = {fm['params']}")
    imp, contrib = shap_importance(fm["model"], df[fm["ofc"]], df[TARGET].values)
    imp.to_csv(C.MODELS / "shap_feature_importance.csv", header=["mean_abs_shap"])
    contrib.to_csv(C.MODELS / "shap_sensor_contribution.csv", header=["share"])
    print("Sensor contribution (SHAP):", contrib.round(2).to_dict())

    make_maps(df, fm, f"{best.config}_{best.clf}")
    reg, _ = di_regression(df, cols, sensors)
    pd.Series(reg).to_csv(C.MODELS / "di_regression.csv", header=["value"])
    print("DI regression:", {k: round(v, 3) for k, v in reg.items()})


if __name__ == "__main__":
    main()
