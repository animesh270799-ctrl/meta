"""Pooled analysis (all 4 dates together) with the models of Ma et al. (2026): DT-EDNet vs EfficientNet, ResNet18, ConvNeXt V2.
Split (as the paper: 7:3 train/test, 10% of training for validation) done BY PLOT, stratified by treatment, so that no plot
contributes leaves to both training and test. All feature steps (NDSI/RSI effective ranges, RFE-RF, SAND, CARS-PLS, Relief)
fitted on training leaves only. Inputs: RFE-RF, SAND, CARS-PLS, VIs (Relief top 5), full wavelength (350-2500 nm, 20-nm bands),
OWs+VIs. Ablation (paper Table X) on the full-wavelength input. Classical models (RF, SVM, PLS-DA, MLP) on the same split for reference.
Usage: python dl_run.py leaf_clean.pkl results_dl.pkl
"""
import os, sys, time, pickle, warnings
os.environ["OMP_NUM_THREADS"] = "1"
import numpy as np, pandas as pd
from multiprocessing import get_context
warnings.filterwarnings("ignore")
src = open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "analysis.py")).read()
# reuse pre-processing, VIs and selectors from analysis.py (everything before the CV loop), without running the CV
head = src[:src.index("MODELS = [")]
head = head.replace("d = pickle.load(open(sys.argv[1], \"rb\"))", "d = pickle.load(open(LEAF_PKL, \"rb\"))")
LEAF_PKL = sys.argv[1]
g = {"LEAF_PKL": LEAF_PKL, "__name__": "featlib"}
exec(compile(head, "analysis_head", "exec"), g)
meta, B, bw, VI = g["meta"], g["B"], g["bw"], g["VI"]
from sklearn.model_selection import StratifiedGroupKFold
from sklearn.metrics import accuracy_score, cohen_kappa_score, f1_score, recall_score, confusion_matrix

y = meta.level.values; plots = meta["plot"].values; trt = meta.treatment.values
# ---- plot-grouped 7:3 split, then 10% of training (by plot) for validation
sgk = StratifiedGroupKFold(n_splits=10, shuffle=True, random_state=42)
fold_of = np.empty(len(y), int)
for k, (_, te) in enumerate(sgk.split(np.zeros(len(y)), trt, plots)): fold_of[te] = k
te_mask = np.isin(fold_of, [0, 1, 2]); va_mask = fold_of == 3; tr_mask = ~(te_mask | va_mask)
tr, va, te = np.where(tr_mask)[0], np.where(va_mask)[0], np.where(te_mask)[0]
print("split leaves train/val/test", len(tr), len(va), len(te), "plots", len(set(plots[tr])), len(set(plots[va])), len(set(plots[te])), flush=True)

# ---- feature engineering on training leaves (train part only)
t0 = time.time()
mn, mr = g["r2_maps"](tr); eff = g["effective_bins"](mn, mr)
f = {"effective": eff}
f["rfe"] = eff[g["sel_rfe"](B[tr][:, eff], y[tr])]
s_idx, s_w = g["sel_sand"](B[tr][:, eff], y[tr]); f["sand"] = eff[s_idx]; f["sand_w"] = pd.Series(s_w, index=bw[eff])
c_idx, c_info = g["sel_cars"](B[tr][:, eff], y[tr].astype(float), plots[tr]); f["cars"] = eff[c_idx]; f["cars_info"] = c_info
W = g["relief"](VI.values[tr], y[tr]); f["relief_w"] = W; f["vi_top"] = list(np.argsort(-W)[:5])
B20 = np.column_stack([B[:, i:i + 2].mean(1) for i in range(0, B.shape[1] - 1, 2)]); bw20 = np.array([bw[i:i + 2].mean() for i in range(0, B.shape[1] - 1, 2)])
X = {"RFE-RF": B[:, f["rfe"]], "SAND": B[:, f["sand"]], "CARS-PLS": B[:, f["cars"]], "VIs (Relief top 5)": VI.values[:, f["vi_top"]],
     "Full wavelength (350-2500 nm)": B20, "OWs+VIs": np.hstack([B[:, f["cars"]], VI.values[:, f["vi_top"]]])}
print("features done", round(time.time() - t0), "s | eff", len(eff), "rfe", len(f["rfe"]), "sand", len(f["sand"]), "cars", len(f["cars"]), flush=True)
SETS = list(X); DL = ["DT-EDNet", "EfficientNet", "ResNet18", "ConvNeXt V2"]; ABL = ["DT-EDNet-SE", "DT-EDNet-DTG", "DT-EDNet-SE-DTG"]


def job(args):
    import torch; torch.set_num_threads(1)
    from dtednet import train_eval
    s, m = args; t = time.time(); Xs = X[s].astype(np.float32)
    p, info = train_eval(m, Xs[tr], y[tr], Xs[va], y[va], Xs[te], epochs=int(os.environ.get('DL_EPOCHS', 300)), patience=int(os.environ.get('DL_PATIENCE', 60)))
    info["seconds"] = round(time.time() - t); print(f"  {m:16s} | {s:30s} | {info['epochs_run']:3d} ep | {info['seconds']:5d} s | test OA {np.mean(p == y[te]) * 100:5.1f}", flush=True)
    return (s, m), p, info


def metrics(yt, p):
    f1 = f1_score(yt, p, average=None, labels=range(5), zero_division=0)
    return dict(OA=accuracy_score(yt, p) * 100, Kappa=cohen_kappa_score(yt, p) * 100, QWK=cohen_kappa_score(yt, p, weights="quadratic") * 100,
                Recall=recall_score(yt, p, average="macro", labels=range(5), zero_division=0) * 100,
                F1=f1_score(yt, p, average="macro", labels=range(5), zero_division=0) * 100, **{f"F1_L{l}": f1[l] * 100 for l in range(5)})


if __name__ == "__main__":
    jobs = [("Full wavelength (350-2500 nm)", "DT-EDNet")] + [(s, m) for s in SETS for m in DL if not (s.startswith("Full") and m == "DT-EDNet")] + \
           [("Full wavelength (350-2500 nm)", a) for a in ABL]
    # longest jobs first
    order = {"Full wavelength (350-2500 nm)": 0}
    jobs = sorted(jobs, key=lambda j: (0 if j[0].startswith("Full") and j[1] in ("DT-EDNet", "DT-EDNet-SE") else 1, j[1] != "EfficientNet"))
    if os.environ.get('DL_SMOKE'): jobs = jobs[:2] + [j for j in jobs if j[1] in ('ResNet18', 'ConvNeXt V2', 'DT-EDNet-DTG')][:3]
    with get_context("fork").Pool(4) as pool: out = pool.map(job, jobs, chunksize=1)
    preds = {k: p for k, p, _ in out}; infos = {k: i for k, _, i in out}
    # classical baselines on the same split (train + val used for fitting)
    trv = np.concatenate([tr, va]); cls = {}
    for s in SETS:
        for m in ["RF", "SVM", "PLS-DA", "MLP"]:
            cls[(s, m)] = g["fit_predict"](m, X[s][trv], y[trv], X[s][te], plots[trv])
    rows = [dict(input=s, model=m, family="Deep (paper)" if m in DL else ("Ablation" if m in ABL else "Classical"), **metrics(y[te], p)) for (s, m), p in {**preds, **cls}.items()]
    res = pd.DataFrame(rows)
    per_date = [dict(input=s, model=m, date=dt, OA=accuracy_score(y[te][meta.date.values[te] == dt], p[meta.date.values[te] == dt]) * 100)
                for (s, m), p in preds.items() for dt in ["110226", "240226", "030326", "130326"]]
    OUT = dict(meta=meta, split=dict(tr=tr, va=va, te=te), feats=f, X_names=SETS, results=res, preds={**preds, **cls}, infos=infos,
               per_date=pd.DataFrame(per_date), B20_wl=bw20, bins=bw)
    with open(sys.argv[2], "wb") as fh: pickle.dump(OUT, fh)
    print(res[res.family != "Classical"].sort_values("OA", ascending=False).head(8)[["input", "model", "OA", "Kappa", "F1"]].round(1).to_string())
    print("ALL DONE")
