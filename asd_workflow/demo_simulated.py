"""Runs every step of asd_pipeline.py on SIMULATED ASD spectra, including plant-grouped nested CV.
The numbers it prints describe the simulation only, not white rust.

Run:  python demo_simulated.py
"""
import numpy as np
import pandas as pd
from sklearn.ensemble import IsolationForest, RandomForestClassifier
from sklearn.model_selection import StratifiedGroupKFold, GroupKFold, GridSearchCV
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.svm import SVC
from sklearn.metrics import f1_score, cohen_kappa_score
import asd_pipeline as A

rng = np.random.default_rng(1)
wl = np.arange(350, 2501, dtype=float)


def leaf_spectrum(sev):
    """Crude vegetation spectrum; sev 0-1 lowers chlorophyll absorption depth and NIR, raises SWIR."""
    chl = (1 - 0.6 * sev) * (0.9 * np.exp(-((wl - 670) / 35) ** 2) + 0.5 * np.exp(-((wl - 450) / 40) ** 2))
    base = 0.06 + 0.42 / (1 + np.exp(-(wl - (718 - 8 * sev)) / 12)) * (1 - 0.25 * sev)
    water = (0.9 - 0.5 * sev) * (0.12 * np.exp(-((wl - 1450) / 60) ** 2) + 0.2 * np.exp(-((wl - 1940) / 70) ** 2)
                                 + 0.03 * np.exp(-((wl - 970) / 30) ** 2) + 0.04 * np.exp(-((wl - 1200) / 40) ** 2))
    swir = -0.12 * np.log1p(np.exp((wl - 1300) / 40)) * 40 / 1200        # smooth decline beyond 1300 nm
    dry = 0.05 * sev / (1 + np.exp(-(wl - 1350) / 40))                    # drier tissue reflects more SWIR
    return np.clip(base * (1 - 0.8 * chl) - water * (wl > 900) + swir + dry, 0.01, 0.9)


# ---- simulated glasshouse data: 60 plants (pots), 4 leaves each, 3 readings per leaf
rows, spectra = [], []
for plant in range(60):
    inoculated = plant >= 15
    for leaf in range(4):
        grade = 0 if not inoculated else int(rng.integers(0, 6))
        s = leaf_spectrum(grade / 5 * rng.uniform(0.7, 1.1))
        for rep in range(3):
            x = s * rng.normal(1, 0.03) + rng.normal(0, 0.003, wl.size)
            x[: 651] += rng.normal(0, 0.01)                     # VNIR detector offset -> splice step
            spectra.append(x)
            rows.append(dict(plant_id=f"P{plant:02d}", leaf_id=f"P{plant:02d}L{leaf}", rep=rep, grade=grade))
R, meta = np.array(spectra), pd.DataFrame(rows)

# ---- Step 4: QC
R = A.splice_correct(R, wl)
R, meta = A.average_replicates(R, meta, "leaf_id")
print("leaves:", len(meta), "| physical flags:", A.physical_checks(R, wl).sum().to_dict())
keep = A.band_mask(wl)

# ---- Step 5: pre-processing
Rs = A.sg(R, 11, 2)
X_snv = A.snv(Rs[:, keep])
y = meta.grade.to_numpy()
groups = meta.plant_id.to_numpy()

# ---- Step 6-7: exploration (all data is acceptable for description, not for selection)
rho = A.correlation_spectrum(Rs[:, keep][:, ::5], y)
H, q = A.kruskal_spectrum(Rs[:, keep][:, ::5], y)
lag = A.lagged_correlation(Rs[:, keep])
print("max |rho| =", np.nanmax(np.abs(rho)).round(2), "| bands with q<0.05:", int((q < 0.05).sum()),
      "| lag where mean r < 0.2:", int(np.argmax(lag < 0.2) + 1) if (lag < 0.2).any() else ">60")
print("persistence of |rho|>=0.6 (max run, bands):", A.persistence(rho, 0.6).max())

# ---- Step 8: features
F = pd.concat([A.red_edge(Rs, wl), A.indices(Rs, wl)], axis=1)
print(F.groupby(y).mean()[["REP", "REV", "SDr670_780", "NDVI", "RBI"]].round(4))
wc, CR = A.continuum_removed(Rs, wl, 550, 750)
print("continuum-removed band depth at 670 nm, healthy vs grade 5:",
      (1 - CR[y == 0, np.argmin(abs(wc - 670))]).mean().round(3), (1 - CR[y == 5, np.argmin(abs(wc - 670))]).mean().round(3))
print("MicaSense simulated:", A.simulate_bands(Rs, wl, A.MICASENSE_MX).iloc[0].round(3).to_dict())

# ---- Steps 9-10: nested, plant-grouped CV with the index search INSIDE the training folds
outer = StratifiedGroupKFold(n_splits=4, shuffle=True, random_state=0)
pred = np.empty_like(y)
for k, (tr, te) in enumerate(outer.split(Rs, y, groups)):
    iso = IsolationForest(contamination=0.02, random_state=0).fit(X_snv[tr])
    tr = tr[iso.predict(X_snv[tr]) == 1]                                  # drop training outliers only
    top = A.ndsi_search(Rs[tr], wl, y[tr], step=20, keep=keep).head(3)    # search on training leaves
    feats = lambda idx: np.column_stack([F.iloc[idx][["REP", "REV", "SDr670_780", "NDVI", "PRI"]].to_numpy()]
                                        + [A.ndsi(Rs[idx], wl, r.b1, r.b2) for r in top.itertuples()])
    pipe = Pipeline([("sc", StandardScaler()), ("clf", SVC())])
    grid = GridSearchCV(pipe, {"clf__C": [1, 10, 100], "clf__gamma": ["scale", 0.1]}, cv=GroupKFold(3), scoring="f1_macro")
    grid.fit(feats(tr), y[tr], groups=groups[tr])
    pred[te] = grid.predict(feats(te))
    print(f"fold {k}: best NDSI on training = ({top.b1[0]:.0f}, {top.b2[0]:.0f}) |rho|={top.abs_rho[0]:.2f}")
print("outer-CV macro-F1 =", round(f1_score(y, pred, average="macro"), 2),
      "| quadratic-weighted kappa =", round(cohen_kappa_score(y, pred, weights="quadratic"), 2))
