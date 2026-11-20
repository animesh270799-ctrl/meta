"""Step 4 - Endmember extraction (VCA) and spectral unmixing (FCLS).

4a  sample pixels from all dates inside the plots (one endmember set for all dates,
    so abundances are comparable over time),
4b  extract p endmembers with Vertex Component Analysis (Nascimento & Bioucas-Dias, 2005),
4c  name the endmembers (soil, healthy canopy, diseased canopy, shadow) by spectral
    angle to reference spectra taken from the data (control plots = healthy,
    most severe plots = diseased, bright non-vegetation = soil, darkest pixels = shadow),
4d  unmix every plot pixel with Fully Constrained Least Squares (abundances >= 0, sum = 1),
4e  write abundance rasters; plot means become features in Step 5.
Works for HS (default) and, with <= 5 endmembers, for MS.
"""
import numpy as np
import pandas as pd
import geopandas as gpd
from rasterio.features import rasterize
from scipy.optimize import nnls, linear_sum_assignment
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import config as C
from common import read_raster, write_raster

NAMES = ["soil", "healthy", "diseased", "shadow"]


def plot_id_raster(plots, prof):
    shapes = [(g, int(pid)) for g, pid in zip(plots.geometry, plots.plot_id)]
    return rasterize(shapes, out_shape=(prof["height"], prof["width"]), transform=prof["transform"], fill=0, dtype="int32")


def vca(Y, p, seed=0):
    """Vertex Component Analysis. Y: (bands, pixels). Returns endmembers (bands, p) and pixel indices."""
    rng = np.random.default_rng(seed)
    L, N = Y.shape
    U, _, _ = np.linalg.svd(Y @ Y.T / N)
    X = U[:, :p].T @ Y                                   # project onto signal subspace
    u = X.mean(1, keepdims=True)
    Yp = X / (u.T @ X)                                   # projective projection
    A = np.zeros((p, p)); A[-1, 0] = 1
    idx = []
    for i in range(p):
        w = rng.standard_normal((p, 1))
        f = w - A @ np.linalg.pinv(A) @ w
        f /= np.linalg.norm(f)
        k = int(np.argmax(np.abs(f.T @ Yp)))
        A[:, i] = Yp[:, k]
        idx.append(k)
    return Y[:, idx], np.array(idx)


def simplex_volume(E):
    Z = E - E.mean(1, keepdims=True)
    U, _, _ = np.linalg.svd(Z, full_matrices=False)
    P = U[:, :E.shape[1] - 1].T @ E
    return abs(np.linalg.det(P[:, 1:] - P[:, [0]]))


def best_vca(Y, p, runs=10):
    """VCA is randomised; keep the run whose endmembers span the largest simplex."""
    return max((vca(Y, p, s) for s in range(runs)), key=lambda r: simplex_volume(r[0]))


def spectral_angle(a, b):
    return np.arccos(np.clip(a @ b / (np.linalg.norm(a) * np.linalg.norm(b) + 1e-12), -1, 1))


def name_endmembers(E, refs):
    names = list(refs)
    cost = np.array([[spectral_angle(E[:, i], refs[n]) for n in names] for i in range(E.shape[1])])
    rows, cols = linear_sum_assignment(cost)
    labels = [f"em{i}" for i in range(E.shape[1])]
    for r, c in zip(rows, cols):
        labels[r] = names[c]
    return labels


def fcls(E, Y, delta=None):
    """Fully constrained least squares via NNLS with an appended sum-to-one row."""
    delta = delta or 10 * np.nanmax(E)
    Ea = np.vstack([np.full((1, E.shape[1]), delta), E])
    out = np.zeros((E.shape[1], Y.shape[1]), "float32")
    for j in range(Y.shape[1]):
        out[:, j] = nnls(Ea, np.concatenate([[delta], Y[:, j]]))[0]
    return out


def reference_spectra(cube, veg, pid, gt_date):
    healthy_ids = gt_date.loc[gt_date.DI == 0, "plot_id"].values
    severe_ids = gt_date.loc[gt_date.DI >= gt_date.DI.quantile(0.9), "plot_id"].values
    bright = np.nanmean(cube, 0)
    inside = pid > 0
    sel = {
        "healthy": veg & np.isin(pid, healthy_ids),
        "diseased": veg & np.isin(pid, severe_ids),
        "soil": inside & ~veg & (bright > np.nanpercentile(bright[inside], 50)),
        "shadow": inside & (bright < np.nanpercentile(bright[inside], 2)),
    }
    return {k: np.nanmean(cube[:, m], 1) for k, m in sel.items() if m.sum() > 10}


def run_unmixing(sensor="HS", p=C.N_ENDMEMBERS):
    plots = gpd.read_file(C.PLOTS_FILE)
    gt = pd.read_csv(C.GROUND_TRUTH_CSV, dtype={"date": str})
    rng = np.random.default_rng(C.RANDOM_STATE)
    samples, refs_all, cache = [], [], {}
    for date in C.DATES:
        cube, prof = read_raster(C.PRE / sensor / f"{sensor}_{date}.tif")
        veg = read_raster(C.MASK / sensor / f"{sensor}_{date}_veg.tif")[0][0] == 1
        pid = plot_id_raster(plots, prof)
        cache[date] = (prof, pid)
        Y = cube[:, pid > 0]
        Y = Y[:, np.all(np.isfinite(Y), 0)]
        samples.append(Y[:, rng.choice(Y.shape[1], min(C.UNMIX_SAMPLE // len(C.DATES), Y.shape[1]), replace=False)])
        refs_all.append(reference_spectra(cube, veg, pid, gt[gt.date == date]))
    Ysamp = np.hstack(samples)
    E, _ = best_vca(Ysamp, p)
    refs = {k: np.nanmean([r[k] for r in refs_all if k in r], 0) for k in NAMES if any(k in r for r in refs_all)}
    labels = name_endmembers(E, refs)
    C.UNMIX.mkdir(parents=True, exist_ok=True)
    pd.DataFrame(E, columns=labels).to_csv(C.UNMIX / f"{sensor}_endmembers.csv", index=False)
    fig, ax = plt.subplots(figsize=(7, 4))
    wl = np.loadtxt(C.PRE / "HS" / "wavelengths.txt") if sensor == "HS" else np.array(list(C.MS_BANDS.values()))
    for i, n in enumerate(labels):
        ax.plot(wl, E[:, i], label=n)
    ax.set_xlabel("Wavelength (nm)"); ax.set_ylabel("Reflectance"); ax.legend(); fig.tight_layout()
    fig.savefig(C.UNMIX / f"{sensor}_endmembers.png", dpi=150); plt.close(fig)
    print(f"{sensor} endmembers: {labels}")

    for date in C.DATES:
        cube = read_raster(C.PRE / sensor / f"{sensor}_{date}.tif")[0]
        prof, pid = cache[date]
        inside = (pid > 0) & np.all(np.isfinite(cube), 0)
        ab = np.full((p, *pid.shape), np.nan, "float32")
        ab[:, inside] = fcls(E, cube[:, inside])
        p2 = prof.copy()
        write_raster(C.UNMIX / f"{sensor}_{date}_abundance.tif", ab, p2)
        print(f"{sensor} {date}: unmixed {inside.sum()} pixels")
    return labels


if __name__ == "__main__":
    run_unmixing("HS")
