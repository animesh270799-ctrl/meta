"""Worked example of Phases 1-3 on a small, simulated test data set.

48 plots (P01-P12 healthy controls, P13-P48 inoculated) x 4 flight dates = 192 rows,
21 features from 4 sensors. Every number in worked_example/ is produced by the
pipeline's own functions (s06_dsf, s07_models), so the example follows the real code.

Run:  RW_FAST=1 python worked_example.py
"""
import os
import sys
from pathlib import Path

os.environ.setdefault("RW_FAST", "1")
sys.path.insert(0, str(Path(__file__).resolve().parent))

import numpy as np
import pandas as pd
from scipy.stats import chi2
from sklearn.model_selection import StratifiedGroupKFold
from sklearn.metrics import accuracy_score, f1_score, cohen_kappa_score, confusion_matrix

import config as C
from s06_dsf import select_dsf, TARGET
from s07_models import vif_values, vif_filter, sffs, classifiers, build_model, run_nested, summarize, sensor_of

OUT = Path(__file__).resolve().parent / "worked_example"
OUT.mkdir(exist_ok=True)
pd.set_option("display.width", 200, "display.max_columns", 30, "display.precision", 3)
LOG = open(OUT / "worked_example_log.txt", "w")


def say(*a):
    print(*a)
    print(*a, file=LOG)


# ------------------------------------------------------------------ 1. simulated test data set
def make_data(seed=7):
    """48 plots x 4 dates, like the IARI trial. Each sensor sees the disease through its own,
    partly independent response (chlorophyll, transpiration, visible symptoms)."""
    rng = np.random.default_rng(seed)
    plots = [f"P{i:02d}" for i in range(1, 49)]
    dates = ["D1", "D2", "D3", "D4"]
    frac = [0.15, 0.35, 0.65, 1.0]                          # epidemic progress at each flight
    final = rng.permutation(np.linspace(6, 85, 36))         # final DI of the 36 inoculated plots
    air = {"D1": 22.0, "D2": 24.0, "D3": 27.0, "D4": 29.0}  # air temperature at flight time
    pe = {p: rng.normal(0, 1, 30) for p in plots}           # plot-to-plot differences (soil, density)
    rows = []
    for i, p in enumerate(plots):
        for t, date in enumerate(dates):
            di = 0.0 if i < 12 else float(np.clip(final[i - 12] * frac[t] - 1.5, 0, 100).round(1))
            d = di / 100
            dc, dt, dv = (d * np.exp(rng.normal(0, s)) for s in (0.25, 0.35, 0.30))  # sensor-specific response
            e, N = pe[p], lambda s: rng.normal(0, s)
            ndre = 0.42 - 0.25 * (1 - np.exp(-dc / 0.12)) + 0.012 * e[0] + N(0.010)
            ndvi = 0.80 + 0.02 * t - 0.35 * dc + 0.02 * e[1] + N(0.02)
            ctd = -2.0 + 3.5 * (1 - np.exp(-dt / 0.2)) + 0.2 * e[2] + N(0.3)
            contrast = 0.4 + 3.0 * max(0, dv - 0.08) + 0.08 * e[3] + N(0.1)
            rows.append(dict(
                plot_id=p, date=date, DI=di,
                MS_NDRE=ndre, MS_CIre=(1 + ndre) / (1 - ndre) - 1 + N(0.01),
                MS_NDVI=ndvi, MS_OSAVI=0.9 * ndvi - 0.02 + N(0.004),
                MS_PSRI=0.01 + 0.08 * dc + 0.006 * e[4] + N(0.008), MS_B475=0.035 + N(0.004),
                HS_REP=727 - 9 * (1 - np.exp(-dc / 0.15)) + 0.5 * e[5] + N(0.5),
                HS_CR670=0.82 - 0.15 * (1 - np.exp(-dc / 0.15)) + 0.01 * e[6] + N(0.012),
                HS_PRI=0.02 - 0.03 * dc + N(0.012), HS_NDWI=0.05 - 0.05 * dt + N(0.015),
                HS_R550=0.085 + 0.03 * dc + N(0.008), HS_R1650=0.28 + N(0.02),
                RGB_contrast=contrast, RGB_homog=0.85 - 0.15 * (contrast - 0.4) + N(0.02),
                RGB_ExG=0.26 - 0.25 * dv + 0.02 * e[7] + N(0.025), RGB_VARI=0.12 - 0.05 * dv + N(0.03),
                RGB_entropy=4.0 + 1.5 * dv + N(0.25),
                TIR_CTD=ctd, TIR_CT=air[date] + ctd, TIR_Tstd=0.6 + 0.8 * dt + N(0.15)))
    df = pd.DataFrame(rows)
    for date, g in df.groupby("date"):                      # NRCT is scaled within each flight
        ct = g["TIR_CT"]
        df.loc[g.index, "TIR_NRCT"] = (ct - ct.min()) / (ct.max() - ct.min())
    df[TARGET] = pd.cut(df.DI, C.DI_CLASS_BINS, labels=False).astype(int)
    return df


df = make_data()
FEATS = [c for c in df.columns if c.split("_")[0] in C.SENSORS]
SENS = {s: [c for c in FEATS if sensor_of(c) == s] for s in ["MS", "HS", "RGB", "TIR"]}
df.round(4).to_csv(OUT / "test_dataset.csv", index=False)
say("=== TEST DATA SET ===")
say(f"{len(df)} rows = {df.plot_id.nunique()} plots x {df.date.nunique()} dates, {len(FEATS)} features")
say("rows per class:", df[TARGET].value_counts().sort_index().to_dict())
say(df[["plot_id", "date", "DI", TARGET] + FEATS[:4] + ["TIR_CTD", "RGB_contrast"]].head(8).round(3).to_string(index=False))
say("\nclass means of key features:")
say(df.groupby(TARGET)[["MS_NDRE", "MS_NDVI", "HS_REP", "RGB_contrast", "TIR_CTD", "MS_B475"]].mean().round(3).to_string())

# ------------------------------------------------------------------ 2. one outer fold, step by step
outer = StratifiedGroupKFold(n_splits=4, shuffle=True, random_state=C.RANDOM_STATE)
tr, te = next(outer.split(df, df[TARGET], df.plot_id))
train, test = df.iloc[tr], df.iloc[te]
say("\n=== OUTER FOLD 1 ===")
say("TEST plots (locked away):", sorted(test.plot_id.unique()))
say("TRAIN plots:", sorted(train.plot_id.unique()))
say(f"train rows {len(train)}, test rows {len(test)}; test classes {test[TARGET].value_counts().sort_index().to_dict()}")

# ---------------- Phase 1 per sensor, on TRAIN only
say("\n=== PHASE 1 (training plots only) ===")
dsf, rank = {}, {}
show = ["n_dates_sig", "JM_max", "relief", "rf_perm", "boruta_hits", "votes", "stability", "DSF"]
for s, cols in SENS.items():
    dsf[s], t, rank[s] = select_dsf(train, cols, fast=False)
    say(f"\n-- {s}: DSF = {dsf[s]}")
    say(t[show].round(3).to_string())

# ---------------- Phase 2 per sensor
say("\n=== PHASE 2 (per sensor, training plots only; inner CV = 4 folds grouped by plot) ===")
y, g = train[TARGET].values, train.plot_id.values
est = {k: v[0] for k, v in classifiers().items()}
phase2 = {}
for s in SENS:
    feats = dsf[s]
    v = pd.Series(vif_values(train[feats]), index=feats)
    kept, removed = vif_filter(train[feats], rank[s])
    say(f"\n-- {s}: VIF before = {v.round(1).to_dict()}")
    say(f"   VIF removed {removed} -> kept {kept}")
    ofc, steps = sffs(est["RF"], train[kept], y, g)
    say("   SFFS (RF) best subset for each size k, inner-CV macro-F1:")
    say(steps.round(3).to_string(index=False))
    say(f"   one-SE rule -> OFC = {ofc}")
    for clf in ["RF", "SVM", "KNN"]:
        m = build_model(train, dsf, rank, [s], clf)
        yp = m["model"].predict(test[m["ofc"]])
        phase2[(s, clf)] = yp
        say(f"   {clf:<3} OFC={m['ofc']}  params={m['params']}  TEST OA={accuracy_score(test[TARGET], yp):.2f} "
            f"macro-F1={f1_score(test[TARGET], yp, average='macro', zero_division=0):.2f}")

# ---------------- Phase 3 fusion
say("\n=== PHASE 3 (fusion of all four sensors' DSFs) ===")
pool = [f for s in SENS for f in dsf[s]]
allrank = pd.concat(rank.values())
kept, removed = vif_filter(train[pool], allrank)
say(f"pooled DSFs ({len(pool)}): {pool}")
say(f"VIF removed {removed} -> kept {kept}")
ofc, steps = sffs(est["RF"], train[kept], y, g)
say("SFFS (RF) on the fused pool:")
say(steps.round(3).to_string(index=False))
say(f"one-SE rule -> fused OFC = {ofc}")
for clf in ["RF", "SVM", "KNN"]:
    m = build_model(train, dsf, rank, list(SENS), clf)
    yp = m["model"].predict(test[m["ofc"]])
    say(f"{clf:<3} OFC={m['ofc']}  TEST OA={accuracy_score(test[TARGET], yp):.2f} "
        f"macro-F1={f1_score(test[TARGET], yp, average='macro', zero_division=0):.2f}")
    if clf == "RF":
        labels = list(range(6))
        say("confusion matrix, fused RF on the test rows (rows = true class 0-5, cols = predicted):")
        say(pd.DataFrame(confusion_matrix(test[TARGET], yp, labels=labels), index=labels, columns=labels).to_string())
        say(pd.DataFrame(dict(plot=test.plot_id.values, date=test.date.values, DI=test.DI.values,
                              true=test[TARGET].values, pred=yp)).to_string(index=False))

# ------------------------------------------------------------------ 3. full nested CV (all 4 outer folds)
say("\n=== FULL NESTED CV: 4 outer folds, every plot tested once ===")
configs = {"MS": ["MS"], "HS": ["HS"], "RGB": ["RGB"], "TIR": ["TIR"], "MS+TIR": ["MS", "TIR"], "ALL4": list(SENS)}
preds, picks = run_nested(df, FEATS, configs, n_repeats=1, outer_folds=4)
preds.to_csv(OUT / "nested_cv_predictions.csv", index=False)
picks.to_csv(OUT / "nested_cv_feature_picks.csv", index=False)
summ = summarize(preds)[["config", "clf", "OA_mean", "macro_F1_mean", "kappa_mean"]]
say(summ.round(3).to_string(index=False))

best_single = summ[summ.config.isin(["MS", "HS", "RGB", "TIR"])].iloc[0]
fused = summ[summ.config == "ALL4"].iloc[0]
a = preds[(preds.config == best_single.config) & (preds.clf == best_single.clf)].sort_values("row")
b = preds[(preds.config == "ALL4") & (preds.clf == fused.clf)].sort_values("row")
ra, rb = (a.y_true.values == a.y_pred.values), (b.y_true.values == b.y_pred.values)
n01, n10 = int((~ra & rb).sum()), int((ra & ~rb).sum())
stat = (abs(n01 - n10) - 1) ** 2 / (n01 + n10) if n01 + n10 else 0.0
say(f"\nMcNemar: best single = {best_single.config}/{best_single.clf}, fused = ALL4/{fused.clf}")
say(f"fused right & single wrong = {n01}, single right & fused wrong = {n10}, "
    f"chi2 = {stat:.2f}, p = {chi2.sf(stat, 1):.3f}")
LOG.close()
