"""Step 5 - Plot-wise feature extraction.

For every sensor, date and plot (polygon shrunk inward by PLOT_INSET_M) the vegetation
pixels are summarised into one row of features:
  MS  : band reflectance, 12 vegetation indices, canopy cover
  HS  : mean spectrum (every retained band), first-derivative edge features, red-edge
        position, continuum-removed absorption features, narrow-band indices,
        endmember abundances
  RGB : colour indices and GLCM texture (8 metrics x 3 bands)
  TIR : canopy temperature statistics, CTD, CTR, NRCT and GLCM texture
Output: FEAT/features_<sensor>.csv  (one row per plot_id x date)
"""
import numpy as np
import pandas as pd
import geopandas as gpd
import rasterio
from rasterio.features import geometry_mask
from rasterio.windows import from_bounds
from skimage.feature import graycomatrix
import config as C
from common import read_hs_wavelengths, band_index, safe_div


# ------------------------------------------------------------------ helpers
def plot_pixels(src, geom, extra_mask_src=None):
    """Read the window around one plot; return (array[bands,r,c], plot_mask, veg_mask)."""
    win = from_bounds(*geom.bounds, transform=src.transform).round_offsets().round_lengths()
    arr = src.read(window=win).astype("float32")
    tr = src.window_transform(win)
    inside = ~geometry_mask([geom], out_shape=arr.shape[1:], transform=tr)
    veg = inside.copy()
    if extra_mask_src is not None:
        veg &= extra_mask_src.read(1, window=win, boundless=True, fill_value=0) == 1
    if src.nodata is not None and not np.isnan(src.nodata):
        arr[arr == src.nodata] = np.nan
    return arr, inside, veg


def glcm_features(img, mask, levels=32, prefix=""):
    """Eight Haralick metrics averaged over 0, 45, 90, 135 degrees, using only masked pixels."""
    names = ["mean", "variance", "homogeneity", "contrast", "dissimilarity", "entropy", "asm", "correlation"]
    vals = img[mask & np.isfinite(img)]
    if vals.size < 50:
        return {f"{prefix}glcm_{n}": np.nan for n in names}
    lo, hi = np.percentile(vals, [1, 99])
    q = np.clip(((img - lo) / (hi - lo + 1e-9) * (levels - 2)), 0, levels - 2)
    q = np.nan_to_num(q).astype(np.uint8) + 1          # 1..levels-1 for vegetation
    q[~mask] = 0                                       # 0 = excluded (soil, outside plot)
    P = graycomatrix(q, [1], [0, np.pi / 4, np.pi / 2, 3 * np.pi / 4], levels=levels, symmetric=True)
    P = P[1:, 1:, 0, :].astype(float)                  # drop pairs touching excluded pixels
    i, j = np.indices(P.shape[:2])
    acc = {n: [] for n in names}
    for a in range(P.shape[2]):
        p = P[:, :, a]
        if p.sum() == 0:
            continue
        p = p / p.sum()
        mi, mj = (i * p).sum(), (j * p).sum()
        vi, vj = ((i - mi) ** 2 * p).sum(), ((j - mj) ** 2 * p).sum()
        nz = p[p > 0]
        acc["mean"].append(mi); acc["variance"].append(vi)
        acc["homogeneity"].append((p / (1 + (i - j) ** 2)).sum())
        acc["contrast"].append(((i - j) ** 2 * p).sum())
        acc["dissimilarity"].append((np.abs(i - j) * p).sum())
        acc["entropy"].append(-(nz * np.log(nz)).sum())
        acc["asm"].append((p ** 2).sum())
        acc["correlation"].append(((i - mi) * (j - mj) * p).sum() / np.sqrt(vi * vj + 1e-12))
    return {f"{prefix}glcm_{n}": float(np.mean(v)) if v else np.nan for n, v in acc.items()}


def stats(x, prefix):
    x = x[np.isfinite(x)]
    if x.size == 0:
        return {f"{prefix}_{k}": np.nan for k in ["mean", "std", "p10", "p90"]}
    return {f"{prefix}_mean": x.mean(), f"{prefix}_std": x.std(),
            f"{prefix}_p10": np.percentile(x, 10), f"{prefix}_p90": np.percentile(x, 90)}


# ------------------------------------------------------------------ MS
def ms_indices(b):
    B, G, R, RE, N = b["B"], b["G"], b["R"], b["RE"], b["NIR"]
    return {
        "NDVI": safe_div(N - R, N + R), "GNDVI": safe_div(N - G, N + G), "NDRE": safe_div(N - RE, N + RE),
        "CIre": safe_div(N, RE) - 1, "CIg": safe_div(N, G) - 1, "MTCI": safe_div(N - RE, RE - R),
        "TCARI": 3 * ((RE - R) - 0.2 * (RE - G) * safe_div(RE, R)),
        "SAVI": 1.5 * safe_div(N - R, N + R + 0.5), "OSAVI": safe_div(N - R, N + R + 0.16),
        "MSR": safe_div(safe_div(N, R) - 1, np.sqrt(np.clip(safe_div(N, R), 0, None)) + 1),
        "SR": safe_div(N, R), "PSRI": safe_div(R - B, N),
    }


def ms_features(arr, inside, veg):
    b = {name: arr[i] for i, name in enumerate(C.MS_BANDS)}
    f = {f"MS_{k}": np.nanmean(v[veg]) for k, v in b.items()}
    for k, v in ms_indices(b).items():
        f[f"MS_{k}"] = np.nanmean(v[veg])
    f["MS_NDVI_std"] = np.nanstd(ms_indices(b)["NDVI"][veg])
    return f


# ------------------------------------------------------------------ HS
HS_VIS = {
    "PRI": lambda r: safe_div(r(531) - r(570), r(531) + r(570)),
    "MCARI": lambda r: ((r(700) - r(670)) - 0.2 * (r(700) - r(550))) * safe_div(r(700), r(670)),
    "TCARI": lambda r: 3 * ((r(700) - r(670)) - 0.2 * (r(700) - r(550)) * safe_div(r(700), r(670))),
    "PSRI": lambda r: safe_div(r(680) - r(500), r(750)),
    "SIPI": lambda r: safe_div(r(800) - r(445), r(800) - r(680)),
    "ARI": lambda r: safe_div(1.0, r(550)) - safe_div(1.0, r(700)),
    "NDWI": lambda r: safe_div(r(860) - r(1240), r(860) + r(1240)),
    "WI": lambda r: safe_div(r(900), r(970)),
    "NDVI705": lambda r: safe_div(r(750) - r(705), r(750) + r(705)),
    "HI": lambda r: safe_div(r(534) - r(698), r(534) + r(698)) - 0.5 * r(704),
}


def continuum_removed(wl, s, lo, hi):
    """Band depth and area of an absorption feature after convex-hull continuum removal."""
    m = (wl >= lo) & (wl <= hi)
    x, y = wl[m], s[m]
    if x.size < 5:
        return np.nan, np.nan
    hull = [0]
    for k in range(1, len(x)):                      # upper convex hull (monotone chain)
        while len(hull) >= 2:
            a, b = hull[-2], hull[-1]
            if (y[b] - y[a]) * (x[k] - x[a]) <= (y[k] - y[a]) * (x[b] - x[a]):
                hull.pop()
            else:
                break
        hull.append(k)
    cont = np.interp(x, x[hull], y[hull])
    cr = y / cont
    return float(1 - cr.min()), float(np.trapezoid(1 - cr, x))


def hs_features(arr, inside, veg, wl):
    spec = np.nanmean(arr[:, veg], axis=1) if veg.any() else np.full(len(wl), np.nan)
    f = {f"HS_R{w:.0f}": v for w, v in zip(wl, spec)}
    r = lambda nm: spec[band_index(wl, nm, tol=10)] if band_index(wl, nm, tol=10) is not None else np.nan
    for k, fn in HS_VIS.items():
        f[f"HS_{k}"] = float(fn(r))
    d1 = np.gradient(spec, wl)
    for edge, (lo, hi) in {"b": (490, 530), "y": (550, 582), "r": (680, 760)}.items():
        m = (wl >= lo) & (wl <= hi)
        if m.sum() >= 2:
            k = np.argmax(d1[m])
            f[f"HS_D{edge}"] = d1[m][k]; f[f"HS_lambda_{edge}"] = wl[m][k]
            f[f"HS_SD{edge}"] = np.trapezoid(d1[m], wl[m])
    if {"HS_SDr", "HS_SDb", "HS_SDy"} <= f.keys():
        f["HS_SDr_SDb"] = safe_div(f["HS_SDr"], f["HS_SDb"])
        f["HS_SDr_SDy"] = safe_div(f["HS_SDr"], f["HS_SDy"])
    f["HS_REP"] = 700 + 40 * safe_div((r(670) + r(780)) / 2 - r(700), r(740) - r(700))
    for name, (lo, hi) in {"670": (540, 760), "970": (920, 1080), "1200": (1100, 1280)}.items():
        f[f"HS_CR{name}_depth"], f[f"HS_CR{name}_area"] = continuum_removed(wl, spec, lo, hi)
    return f


# ------------------------------------------------------------------ RGB
def rgb_features(arr, inside, veg):
    R, G, B = arr[0], arr[1], arr[2]
    s = R + G + B + 1e-9
    r, g, b = R / s, G / s, B / s
    idx = {"ExG": 2 * g - r - b, "ExR": 1.4 * r - g, "VARI": safe_div(G - R, G + R - B),
           "GLI": safe_div(2 * G - R - B, 2 * G + R + B), "NGRDI": safe_div(G - R, G + R)}
    f = {f"RGB_{k}": np.nanmean(v[veg]) for k, v in idx.items()}
    for i, band in enumerate(C.RGB_BANDS):
        f.update(glcm_features(arr[i], veg, prefix=f"RGB_{band}_"))
    return f


# ------------------------------------------------------------------ TIR
def tir_features(arr, inside, veg, air_temp, ct_min, ct_max):
    t = arr[0]
    ct = np.nanmean(t[veg]) if veg.any() else np.nan
    f = {"TIR_CT": ct, "TIR_CTD": ct - air_temp, "TIR_CTR": ct / air_temp,
         "TIR_NRCT": (ct - ct_min) / (ct_max - ct_min)}
    f.update(stats(t[veg], "TIR_T"))
    f.update(glcm_features(t, veg, prefix="TIR_"))
    return f


# ------------------------------------------------------------------ driver
MIN_VEG_PIXELS = 20


def extract(sensor):
    low_cover = []
    plots = gpd.read_file(C.PLOTS_FILE)
    plots["geometry"] = plots.geometry.buffer(-C.PLOT_INSET_M, join_style="mitre")
    weather = pd.read_csv(C.WEATHER_CSV, dtype={"date": str}).set_index("date") if C.WEATHER_CSV.exists() else None
    wl = np.loadtxt(C.PRE / "HS" / "wavelengths.txt") if sensor == "HS" else None
    rows = []
    for date in C.DATES:
        img_path = C.PRE / sensor / f"{sensor}_{date}.tif"
        if not img_path.exists():
            continue
        ab_path = C.UNMIX / f"{sensor}_{date}_abundance.tif"
        ab_names = pd.read_csv(C.UNMIX / f"{sensor}_endmembers.csv", nrows=0).columns.tolist() if ab_path.exists() else []
        with rasterio.open(img_path) as src, rasterio.open(C.MASK / sensor / f"{sensor}_{date}_veg.tif") as msk:
            if sensor == "TIR":     # field-wide canopy temperature range on this date (robust min/max)
                t_all = src.read(1); vm = msk.read(1) == 1
                ct_min, ct_max = np.nanpercentile(t_all[vm], [0.5, 99.5])
                air = weather.loc[date, "air_temp_C"] if weather is not None else np.nan
            ab_src = rasterio.open(ab_path) if ab_path.exists() else None
            for _, p in plots.iterrows():
                arr, inside, veg = plot_pixels(src, p.geometry, msk)
                row = {"plot_id": int(p.plot_id), "date": date,
                       f"{sensor}_cover": veg.sum() / max(inside.sum(), 1)}
                if veg.sum() < MIN_VEG_PIXELS:
                    # severe disease can push the whole canopy below the NDVI threshold;
                    # use all plot pixels rather than lose the most diseased plots
                    veg = inside.copy()
                    low_cover.append((sensor, date, int(p.plot_id)))
                if sensor == "MS":
                    row.update(ms_features(arr, inside, veg))
                elif sensor == "HS":
                    row.update(hs_features(arr, inside, veg, wl))
                elif sensor == "RGB":
                    row.update(rgb_features(arr, inside, veg))
                elif sensor == "TIR":
                    row.update(tir_features(arr, inside, veg, air, ct_min, ct_max))
                if ab_src is not None:
                    a, ins, _ = plot_pixels(ab_src, p.geometry)
                    means = {n: np.nanmean(a[k][ins]) for k, n in enumerate(ab_names)}
                    row.update({f"{sensor}_ab_{n}": v for n, v in means.items()})
                    if "healthy" in means and "diseased" in means:
                        row[f"{sensor}_ab_diseased_share"] = means["diseased"] / (means["diseased"] + means["healthy"] + 1e-9)
                rows.append(row)
            if ab_src is not None:
                ab_src.close()
        print(f"{sensor} {date}: features for {len(plots)} plots")
    df = pd.DataFrame(rows)
    if low_cover:
        print(f"  {sensor}: {len(low_cover)} plot-dates had < {MIN_VEG_PIXELS} vegetation pixels; "
              f"all plot pixels used instead: {low_cover}")
    C.FEAT.mkdir(parents=True, exist_ok=True)
    df.to_csv(C.FEAT / f"features_{sensor}.csv", index=False)
    return df


if __name__ == "__main__":
    for s in C.SENSORS:
        extract(s)
