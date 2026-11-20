"""Matplotlib figures (Word paper; image-only slides) from results.pkl - paper-faithful version (no texture)."""
import pickle, sys, os
import numpy as np, pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from sklearn.metrics import confusion_matrix

O = pickle.load(open(sys.argv[1], "rb")); out = sys.argv[2]; os.makedirs(out, exist_ok=True)
meta = O["meta"]; LN = O["level_names"]; bins = O["bins"]; ff = O["final_feats"]
C5 = ["#2E7D32", "#9E9E9E", "#E0B000", "#1F5FD1", "#D62728"]
plt.rcParams.update({"font.size": 9, "axes.spines.top": False, "axes.spines.right": False})
SETS = ["RFE-RF", "SAND", "CARS-PLS", "VIs (Relief top 5)", "Full wavelength (350-2500 nm)", "OWs+VIs"]
MODELS = ["RF", "SVM", "PLS-DA", "MLP"]; MC = ["#1F6F78", "#B7791F", "#6B4C8A", "#B24A3F"]
def save(fig, name): fig.savefig(f"{out}/{name}.png", dpi=220, bbox_inches="tight"); plt.close(fig)

cnt = pd.crosstab(meta.date, meta.level).reindex(["110226", "240226", "030326", "130326"])
fig, ax = plt.subplots(figsize=(6, 3.2)); bottom = np.zeros(4)
for l in range(5): ax.bar(["11 Feb", "24 Feb", "03 Mar", "13 Mar"], cnt[l], bottom=bottom, color=C5[l], label=LN[l]); bottom += cnt[l].values
ax.set_ylabel("Leaves"); ax.legend(fontsize=7, frameon=False, bbox_to_anchor=(1, 1)); ax.set_title("Leaves per severity level and date"); save(fig, "fig_counts")

mb, sd = O["mean_by_level"], O["sd_by_level"]
fig, ax = plt.subplots(1, 2, figsize=(10, 3.6), gridspec_kw={"width_ratios": [1.6, 1]})
for k, c in enumerate(mb.columns):
    ax[0].plot(mb.index, mb[c], color=C5[k], lw=1.3, label=c)
    z = mb[c].loc[450:1000]; s = sd[c].loc[450:1000]
    ax[1].plot(z.index, z, color=C5[k], lw=1.4); ax[1].fill_between(z.index, z - s, z + s, color=C5[k], alpha=0.08)
for a in (1450, 1940): ax[0].axvline(a, color="#BBBBBB", lw=0.6, ls=":")
ax[0].text(1450, 0.03, "1450 nm\nwater", fontsize=7, ha="center", color="#777"); ax[0].text(1940, 0.03, "1940 nm\nwater", fontsize=7, ha="center", color="#777")
ax[0].set_xlabel("Wavelength (nm)"); ax[0].set_ylabel("Reflectance"); ax[0].legend(fontsize=7.5, frameon=False); ax[0].set_title("(a) Whole range 350–2500 nm")
ax[1].set_xlabel("Wavelength (nm)"); ax[1].set_title("(b) 450–1000 nm, mean ± SD"); save(fig, "fig_mean_spectra")

thr = O["r2_threshold"]
fig, ax = plt.subplots(1, 2, figsize=(10, 4.3))
vmax = np.nanmax([np.nanmax(O["NDSI_R2"].values), np.nanmax(O["RSI_R2"].values)])
for a_, key, lab in zip(ax, ("NDSI_R2", "RSI_R2"), ("a", "b")):
    M = O[key]; v = M.values.copy()
    if key == "NDSI_R2": v = np.where(np.triu(np.ones_like(v, bool), 1), v, np.nan)
    im = a_.imshow(v, origin="lower", cmap="jet", vmin=0, vmax=vmax, extent=(M.columns[0], M.columns[-1], M.index[0], M.index[-1]), aspect="auto")
    a_.contour(M.columns, M.index, np.nan_to_num(v), levels=[thr], colors="white", linewidths=0.8)
    i, j = np.unravel_index(np.nanargmax(v), v.shape); a_.plot(M.columns[j], M.index[i], "w*", ms=10, mec="k")
    a_.set_title(f"({lab}) {key.split('_')[0]}: max R² = {v[i, j]:.2f} at ({M.index[i]}, {M.columns[j]}) nm", fontsize=8.5)
    a_.set_xlabel("Band j (nm)"); a_.set_ylabel("Band i (nm)")
fig.colorbar(im, ax=ax, label=f"R² with leaf score (white contour = {thr})", shrink=0.85); save(fig, "fig_ndsi_rsi")

fig = plt.figure(figsize=(11, 6.4)); gs = fig.add_gridspec(2, 2)
ax0 = fig.add_subplot(gs[0, :]); m0 = O["mean_by_level"].iloc[:, 0]
ax0.plot(m0.index, m0.values, color="#555", lw=1, label="Mean L0 spectrum")
for i in ff["effective"]: ax0.axvspan(bins[i] - 5, bins[i] + 5, color="#FFE7B0", lw=0)
for k, (key, nm, yy) in enumerate((("rfe", "RFE-RF", 0.72), ("sand", "SAND", 0.77), ("cars", "CARS-PLS", 0.82))):
    ax0.scatter(bins[ff[key]], np.full(len(ff[key]), yy), marker="|", s=130, color=MC[k], label=f"{nm} ({len(ff[key])})")
ax0.set_ylim(0, 0.88); ax0.set_xlim(350, 2500); ax0.set_xlabel("Wavelength (nm)"); ax0.set_ylabel("Reflectance")
ax0.legend(fontsize=7.5, frameon=False, loc="center right"); ax0.set_title("(a) Selected wavelengths (shaded = effective ranges from NDSI/RSI)")
ax1 = fig.add_subplot(gs[1, 0]); sw = ff["sand_w"]
ax1.bar(sw.index, sw.values, width=8, color=["#B7791F" if v > 0.524 else "#CCCCCC" for v in sw.values]); ax1.axhline(0.524, color="#B24A3F", ls="--", lw=0.9)
ax1.set_xlabel("Wavelength (nm)"); ax1.set_ylabel("SAND weight"); ax1.set_title("(b) SAND feature weights (threshold 0.524)")
ax2 = fig.add_subplot(gs[1, 1]); ci = ff["cars_info"]; x = range(1, len(ci["rmsecv"]) + 1)
ax2.plot(x, ci["rmsecv"], color="#1F6F78"); ax2.axvline(ci["best_run"], color="#B24A3F", ls="--"); ax2.set_xlabel("CARS sampling run"); ax2.set_ylabel("RMSECV")
ax3 = ax2.twinx(); ax3.plot(x, ci["n_vars"], color="#B7791F", lw=0.9); ax3.set_ylabel("Variables kept", color="#B7791F"); ax2.set_title("(c) CARS-PLS")
fig.tight_layout(); save(fig, "fig_band_selection")

names = list(O["VI"].columns); W = ff["relief_w"]; r = O["VI_r"][names].values
fig, ax = plt.subplots(1, 3, figsize=(12, 3.9), gridspec_kw={"width_ratios": [1, 1, 1.25]})
o = np.argsort(np.abs(r)); ax[0].barh(np.array(names)[o], r[o], color=["#1F6F78" if v > 0 else "#B24A3F" for v in r[o]]); ax[0].set_xlabel("Pearson r with leaf score"); ax[0].set_title("(a) Correlation (Table VIII)")
o = np.argsort(W); ax[1].barh(np.array(names)[o], W[o], color=["#B7791F" if i in ff["vi_top"] else "#BBBBBB" for i in o]); ax[1].set_xlabel("Relief weight"); ax[1].set_title("(b) Relief (top 5 coloured)")
cm = O["VI_corrmat"]; im = ax[2].imshow(cm.values, cmap="RdBu_r", vmin=-1, vmax=1)
ax[2].set_xticks(range(len(names))); ax[2].set_xticklabels(names, rotation=90, fontsize=6.5); ax[2].set_yticks(range(len(names))); ax[2].set_yticklabels(names, fontsize=6.5)
ax[2].set_title("(c) Correlation among indices"); fig.colorbar(im, ax=ax[2], shrink=0.8); fig.tight_layout(); save(fig, "fig_vegetation_indices")

for key, nm, title in (("internal", "fig_models_internal", "Internal 5-fold CV grouped by plot (11 Feb, 24 Feb, 3 Mar)"),
                       ("external", "fig_models_external", "Independent date: trained on 3 dates, tested on 13 Mar 2026")):
    d = O[key]; piv = d.pivot(index="input", columns="model", values="OA").reindex(SETS)[MODELS]
    fig, ax = plt.subplots(figsize=(9.5, 3.7)); xs = np.arange(len(SETS)); w = 0.2
    for k, m in enumerate(MODELS): ax.bar(xs + (k - 1.5) * w, piv[m], w, color=MC[k], label=m)
    ax.set_xticks(xs); ax.set_xticklabels(SETS, rotation=15, ha="right", fontsize=8.5); ax.set_ylabel("Overall accuracy (%)"); ax.set_ylim(0, 100)
    ax.axhline(20, color="#999", ls=":", lw=0.8); ax.text(5.45, 21.5, "chance (5 levels)", fontsize=7, color="#777", ha="right")
    ax.legend(ncol=4, frameon=False, fontsize=8); ax.set_title(title); save(fig, nm)

d = O["internal"]; best = d.loc[d.OA.idxmax()]; key = (best["input"], best["model"]); y = meta.level.values
fig, ax = plt.subplots(1, 2, figsize=(9, 3.8))
for a_, (P, idx, tt) in zip(ax, ((O["internal_preds"][key][O["tr_idx"]], O["tr_idx"], "Internal CV"), (O["external_preds"][key], O["te_idx"], "Independent date (13 Mar)"))):
    cm_ = confusion_matrix(y[idx], P, labels=range(5)); cmn = cm_ / np.maximum(cm_.sum(1, keepdims=True), 1)
    a_.imshow(cmn, cmap="Blues", vmin=0, vmax=1)
    for i in range(5):
        for j in range(5): a_.text(j, i, f"{cm_[i, j]}\n{cmn[i, j]*100:.0f}%", ha="center", va="center", fontsize=7, color="white" if cmn[i, j] > 0.5 else "black")
    a_.set_xticks(range(5)); a_.set_yticks(range(5)); a_.set_xticklabels([f"L{k}" for k in range(5)]); a_.set_yticklabels([f"L{k}" for k in range(5)])
    a_.set_xlabel("Predicted level"); a_.set_ylabel("Observed level"); a_.set_title(f"{tt}: {key[0]} + {key[1]}", fontsize=8.5)
fig.tight_layout(); save(fig, "fig_confusion")
print("figures saved")
