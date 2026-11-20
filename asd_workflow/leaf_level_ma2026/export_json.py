import pickle, sys, json
import numpy as np, pandas as pd
from sklearn.metrics import confusion_matrix
O = pickle.load(open(sys.argv[1], "rb")); meta = O["meta"]; LN = O["level_names"]; bins = O["bins"]
SETS = ["RFE-RF", "SAND", "CARS-PLS", "VIs (Relief top 5)", "Full wavelength (350-2500 nm)", "OWs+VIs"]
MODELS = ["RF", "SVM", "PLS-DA", "MLP"]
DATES = ["110226", "240226", "030326", "130326"]; DN = ["11 Feb", "24 Feb", "03 Mar", "13 Mar"]
ff = O["final_feats"]
def r(x, n=4): return [None if (v is None or (isinstance(v, float) and np.isnan(v))) else round(float(v), n) for v in x]
def ranges(idx):
    w = sorted(int(bins[i]) for i in idx); out = []; s = p = w[0]
    for v in w[1:]:
        if v - p > 10: out.append((s, p)); s = v
        p = v
    out.append((s, p)); return [f"{a - 5}–{b + 5}" for a, b in out]
J = {"level_names": LN, "sets": SETS, "models": MODELS, "r2_threshold": O["r2_threshold"]}
cnt = pd.crosstab(meta.date, meta.level).reindex(DATES)
J["counts"] = {"dates": DN, "levels": [[int(v) for v in cnt[l].values] for l in range(5)]}
J["inventory"] = [[DN[i], int((meta.date == d).sum()), int(meta[meta.date == d]["plot"].nunique()), ", ".join(sorted(meta[meta.date == d].stage.unique())),
                   "Training" if d != "130326" else "Independent test"] for i, d in enumerate(DATES)]
mb = O["mean_by_level"]; sub = mb.loc[[w for w in mb.index if w % 10 == 0]]
J["mean_spectra"] = {"wl": [int(w) for w in sub.index], "series": {c: r(sub[c]) for c in sub.columns}}
z = mb.loc[450:1000]; J["mean_zoom"] = {"wl": [int(w) for w in z.index], "series": {c: r(z[c]) for c in z.columns}}
def best_pair(M):
    v = M.values.copy(); i, j = np.unravel_index(np.nanargmax(v), v.shape); return [int(M.index[i]), int(M.columns[j]), round(float(v[i, j]), 3)]
J["ndsi_best"] = best_pair(O["NDSI_R2"]); J["rsi_best"] = best_pair(O["RSI_R2"])
J["effective"] = {"n": len(ff["effective"]), "ranges": ranges(ff["effective"])}
J["bands"] = {k: [int(bins[i]) for i in sorted(ff[k])] for k in ("rfe", "sand", "cars")}
sw = ff["sand_w"]; J["sand_w"] = {"wl": [int(v) for v in sw.index], "w": r(sw.values, 3)}
ci = ff["cars_info"]; J["cars_curve"] = {"run": list(range(1, len(ci["rmsecv"]) + 1)), "rmsecv": r(ci["rmsecv"]), "nvars": [int(v) for v in ci["n_vars"]], "best": int(ci["best_run"])}
freq = {k: np.zeros(len(bins)) for k in ("rfe", "sand", "cars")}
for f in O["fold_feats"]:
    for k in freq: freq[k][f[k]] += 1
J["stability"] = [[int(bins[i]), int(freq["rfe"][i]), int(freq["sand"][i]), int(freq["cars"][i])] for i in range(len(bins)) if sum(freq[k][i] for k in freq) > 0]
J["fold_counts"] = [[len(f["effective"]), len(f["rfe"]), len(f["sand"]), len(f["cars"])] for f in O["fold_feats"]]
names = list(O["VI"].columns); W = ff["relief_w"]
J["vi"] = [[n, O["VI_formulas"][n], round(float(O["VI_r"][n]), 3), round(float(W[i]), 4), "Yes" if i in ff["vi_top"] else ""] for i, n in enumerate(names)]
J["vi_corr"] = {"names": names, "m": [r(row, 2) for row in O["VI_corrmat"].values]}
for key in ("internal", "external"):
    d = O[key]
    J[key] = {"OA": {m: r(d[d.model == m].set_index("input").reindex(SETS).OA, 2) for m in MODELS},
              "F1": {m: r(d[d.model == m].set_index("input").reindex(SETS).F1, 2) for m in MODELS},
              "Kappa": {m: r(d[d.model == m].set_index("input").reindex(SETS).Kappa, 2) for m in MODELS},
              "QWK": {m: r(d[d.model == m].set_index("input").reindex(SETS).QWK, 2) for m in MODELS}}
    b = d.loc[d.OA.idxmax()]; J[key]["best"] = {k: (b[k] if isinstance(b[k], str) else round(float(b[k]), 2)) for k in b.index}
    J[key]["table"] = [[row.input, row.model, *[round(float(getattr(row, c)), 1) for c in ("F1_L0", "F1_L1", "F1_L2", "F1_L3", "F1_L4", "OA", "Kappa", "QWK", "F1")]] for row in d.itertuples()]
fs = O["internal_folds"].groupby(["input", "model"]).OA.agg(["mean", "std"])
J["internal"]["fold_sd"] = {f"{a}|{b}": [round(float(v["mean"]), 2), round(float(v["std"]), 2)] for (a, b), v in fs.iterrows()}
bi = O["internal"].loc[O["internal"].OA.idxmax()]; key = (bi["input"], bi["model"]); y = meta.level.values
J["cm_internal"] = confusion_matrix(y[O["tr_idx"]], O["internal_preds"][key][O["tr_idx"]], labels=range(5)).tolist()
J["cm_external"] = confusion_matrix(y[O["te_idx"]], O["external_preds"][key], labels=range(5)).tolist()
J["cm_key"] = list(key)
J["ext_same_model"] = {k: round(float(v), 2) for k, v in O["external"].set_index(["input", "model"]).loc[key][["OA", "Kappa", "QWK", "Recall", "F1"]].items()}
J["qc"] = {k: int(v.sum()) for k, v in O["qc"].items()}
J["n_bins"] = int(len(bins))
json.dump(J, open(sys.argv[2], "w"), indent=1); print("json saved")
