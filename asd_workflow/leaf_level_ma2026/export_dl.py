"""Export pooled DT-EDNet / CNN results + pooled feature-engineering outputs to JSON and a pickle for figures/builders.
Usage: python export_dl.py leaf_clean.pkl results_dl.pkl results_dl.json pooled_extra.pkl"""
import os, sys, json, pickle, warnings
import numpy as np, pandas as pd
from sklearn.metrics import confusion_matrix
warnings.filterwarnings("ignore")
src = open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "analysis.py")).read()
head = src[:src.index("MODELS = [")].replace('d = pickle.load(open(sys.argv[1], "rb"))', 'd = pickle.load(open(LEAF_PKL, "rb"))')
g = {"LEAF_PKL": sys.argv[1], "__name__": "featlib"}; exec(compile(head, "analysis_head", "exec"), g)
R = pickle.load(open(sys.argv[2], "rb"))
meta = R["meta"]; tr, va, te = R["split"]["tr"], R["split"]["va"], R["split"]["te"]; f = R["feats"]; bins = R["bins"]
VI = g["VI"]; y = meta.level.values; LN = g["LEVEL_NAMES"]
MN, MR = g["r2_maps"](tr); gw = g["gw"]
NDSI = pd.DataFrame(MN, index=gw, columns=gw); RSI = pd.DataFrame(MR, index=gw, columns=gw)
VI_r = pd.Series({c: np.corrcoef(VI[c].values[tr], meta.score.values[tr])[0, 1] for c in VI.columns}); VI_corr = VI.iloc[tr].corr()
extra = dict(NDSI_R2=NDSI, RSI_R2=RSI, VI_r=VI_r, VI_corrmat=VI_corr, mean_by_level=g["OUT"]["mean_by_level"], sd_by_level=g["OUT"]["sd_by_level"],
             mean_by_date=g["OUT"]["mean_by_date"], VI=VI, VI_formulas=g["OUT"]["VI_formulas"], B=g["B"], qc=g["OUT"]["qc"], splice=g["OUT"]["splice"], r2_threshold=g["R2_EFFECTIVE"])
pickle.dump(extra, open(sys.argv[4], "wb"))

SETS = R["X_names"]; DL = ["DT-EDNet", "EfficientNet", "ResNet18", "ConvNeXt V2"]; ABL = ["DT-EDNet", "DT-EDNet-SE", "DT-EDNet-DTG", "DT-EDNet-SE-DTG"]; CL = ["RF", "SVM", "PLS-DA", "MLP"]
res = R["results"]
def r(x, n=4): return [None if (v is None or (isinstance(v, float) and np.isnan(v))) else round(float(v), n) for v in x]
def ranges(idx):
    w = sorted(int(bins[i]) for i in idx); out = []; s = p = w[0]
    for v in w[1:]:
        if v - p > 10: out.append((s, p)); s = v
        p = v
    out.append((s, p)); return [f"{a - 5}–{b + 5}" for a, b in out]
def block(models, fam):
    d = res[res.model.isin(models) & (res.family.isin(fam))]
    out = {k: {m: r(d[d.model == m].set_index("input").reindex(SETS)[k], 2) for m in models} for k in ("OA", "F1", "Kappa", "QWK")}
    b = d.loc[d.OA.idxmax()]; out["best"] = {k: (b[k] if isinstance(b[k], str) else round(float(b[k]), 2)) for k in b.index if k != "family"}
    out["table"] = [[row.input, row.model, *[round(float(getattr(row, c)), 1) for c in ("F1_L0", "F1_L1", "F1_L2", "F1_L3", "F1_L4", "OA", "Kappa", "QWK", "F1")]] for row in d.itertuples()]
    return out
DATES = ["110226", "240226", "030326", "130326"]; DN = ["11 Feb", "24 Feb", "03 Mar", "13 Mar"]
J = {"level_names": LN, "sets": SETS, "dl_models": DL, "cl_models": CL, "r2_threshold": g["R2_EFFECTIVE"]}
cnt = pd.crosstab(meta.date, meta.level).reindex(DATES)
J["counts"] = {"dates": DN, "levels": [[int(v) for v in cnt[l].values] for l in range(5)]}
J["inventory"] = [[DN[i], int((meta.date == d).sum()), int(meta[meta.date == d]["plot"].nunique()), ", ".join(sorted(meta[meta.date == d].stage.unique()))] for i, d in enumerate(DATES)]
J["split"] = {"names": ["Training", "Validation", "Test"], "leaves": [len(tr), len(va), len(te)], "plots": [len(set(meta["plot"].values[i].tolist())) for i in (tr, va, te)],
              "by_level": [[int((y[i] == l).sum()) for i in (tr, va, te)] for l in range(5)],
              "healthy_plots": [int(len(set(meta["plot"].values[i][meta.treatment.values[i] == "Healthy"]))) for i in (tr, va, te)]}
mb = extra["mean_by_level"]; sub = mb.loc[[w for w in mb.index if w % 10 == 0]]
J["mean_spectra"] = {"wl": [int(w) for w in sub.index], "series": {c: r(sub[c]) for c in sub.columns}}
z = mb.loc[450:1000]; J["mean_zoom"] = {"wl": [int(w) for w in z.index], "series": {c: r(z[c]) for c in z.columns}}
def best_pair(M):
    v = M.values.copy(); i, j = np.unravel_index(np.nanargmax(v), v.shape); return [int(M.index[i]), int(M.columns[j]), round(float(v[i, j]), 3)]
J["ndsi_best"] = best_pair(NDSI); J["rsi_best"] = best_pair(RSI)
J["effective"] = {"n": len(f["effective"]), "ranges": ranges(f["effective"])}
J["bands"] = {k: [int(bins[i]) for i in sorted(f[k])] for k in ("rfe", "sand", "cars")}
J["sand_w"] = {"wl": [int(v) for v in f["sand_w"].index], "w": r(f["sand_w"].values, 3)}
ci = f["cars_info"]; J["cars_curve"] = {"run": list(range(1, len(ci["rmsecv"]) + 1)), "rmsecv": r(ci["rmsecv"]), "nvars": [int(v) for v in ci["n_vars"]], "best": int(ci["best_run"])}
names = list(VI.columns); W = f["relief_w"]
J["vi"] = [[n, extra["VI_formulas"][n], round(float(VI_r[n]), 3), round(float(W[i]), 4), "Yes" if i in f["vi_top"] else ""] for i, n in enumerate(names)]
J["vi_corr"] = {"names": names, "m": [r(row, 2) for row in VI_corr.values]}
J["dl"] = block(DL, ["Deep (paper)"]); J["classical"] = block(CL, ["Classical"])
abl = res[(res.input == "Full wavelength (350-2500 nm)") & res.model.isin(ABL)].set_index("model").reindex(ABL)
J["ablation"] = [[m, *[round(float(abl.loc[m, k]), 2) for k in ("F1", "OA", "Kappa", "Recall")]] for m in ABL]
pdd = R["per_date"]; bd = J["dl"]["best"]
J["per_date"] = {"dates": DN, "models": DL, "set": bd["input"], "OA": {m: [round(float(pdd[(pdd.model == m) & (pdd.input == bd["input"]) & (pdd.date == d)].OA.iloc[0]), 1) for d in DATES] for m in DL},
                 "n_test": [int((meta.date.values[te] == d).sum()) for d in DATES]}
key = (bd["input"], bd["model"]); J["cm_key"] = list(key)
J["cm"] = confusion_matrix(y[te], R["preds"][key], labels=range(5)).tolist()
dt_key = (bd["input"], "DT-EDNet"); J["cm_dt_key"] = list(dt_key); J["cm_dt"] = confusion_matrix(y[te], R["preds"][dt_key], labels=range(5)).tolist()
J["train_info"] = [[s, m, R["infos"][(s, m)]["n_params"], R["infos"][(s, m)]["epochs_run"], round(R["infos"][(s, m)]["best_val_oa"] * 100, 1), R["infos"][(s, m)]["seconds"]]
                   for s in SETS for m in DL + ABL[1:] if (s, m) in R["infos"]]
vc = R["infos"][dt_key]["val_curve"]; J["dt_val_curve"] = {"epoch": list(range(1, len(vc) + 1)), "val_oa": [round(v * 100, 1) for v in vc]}
J["qc"] = {k: int(v.sum()) for k, v in extra["qc"].items()}; J["n_bins"] = int(len(bins))
json.dump(J, open(sys.argv[3], "w"), indent=1); print("json saved")
