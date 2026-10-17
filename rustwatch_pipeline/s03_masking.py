"""Step 3 - Vegetation masking, soil removal and shadow removal.

MS and HS : NDVI > Otsu threshold, minus the darkest NIR pixels (shadow).
RGB       : Excess Green (ExG) > Otsu threshold, minus very dark pixels.
TIR       : no spectral information, so the MS vegetation mask of the same date is
            resampled onto the thermal grid, then pixels warmer than the
            canopy/soil Otsu split are removed (mixed soil pixels).
Optional  : K-means clustering instead of a threshold (method="kmeans").
"""
import numpy as np
from skimage.filters import threshold_otsu
from skimage.morphology import binary_opening, disk
from sklearn.cluster import KMeans
from rasterio.warp import Resampling
import config as C
from common import read_raster, write_raster, band_index, ms_band, safe_div
from s02_preprocess import resample_to


def ndvi_ms(arr):
    return safe_div(ms_band(arr, "NIR") - ms_band(arr, "R"), ms_band(arr, "NIR") + ms_band(arr, "R"))


def ndvi_hs(arr, wl):
    r, n = arr[band_index(wl, 670)], arr[band_index(wl, 800, tol=40)]
    return safe_div(n - r, n + r)


def excess_green(rgb):
    s = np.nansum(rgb, axis=0) + 1e-9
    r, g, b = rgb[0] / s, rgb[1] / s, rgb[2] / s
    return 2 * g - r - b


def otsu_mask(index, fixed=None):
    v = index[np.isfinite(index)]
    t = fixed if fixed is not None else threshold_otsu(v)
    return np.nan_to_num(index, nan=-9) > t, t


def kmeans_mask(features, veg_feature=0, k=3, seed=C.RANDOM_STATE):
    """features: list of 2-D arrays. Cluster with the highest mean of features[veg_feature] = vegetation."""
    X = np.stack([f.ravel() for f in features], 1)
    ok = np.all(np.isfinite(X), 1)
    sample = np.random.default_rng(seed).choice(np.where(ok)[0], min(50000, ok.sum()), replace=False)
    km = KMeans(k, n_init=10, random_state=seed).fit(X[sample])
    lab = np.full(len(X), -1)
    lab[ok] = km.predict(X[ok])
    veg = int(np.argmax(km.cluster_centers_[:, veg_feature]))
    return (lab == veg).reshape(features[0].shape)


def shadow_mask(nir):
    return nir < np.nanpercentile(nir, C.SHADOW_NIR_PERCENTILE)


def clean(mask, radius=1):
    return binary_opening(mask, disk(radius)) if radius else mask


def mask_date(date, method="otsu"):
    out = {}
    ms, ms_prof = read_raster(C.PRE / "MS" / f"MS_{date}.tif")
    ndvi = ndvi_ms(ms)
    if method == "kmeans":
        veg = kmeans_mask([ndvi, ms_band(ms, "NIR")])
        t = np.nan
    else:
        veg, t = otsu_mask(ndvi, C.NDVI_MIN)
    veg = clean(veg & ~shadow_mask(ms_band(ms, "NIR")))
    out["MS"] = (veg, ms_prof, t)

    hs_path = C.PRE / "HS" / f"HS_{date}.tif"
    if hs_path.exists():
        hs, hs_prof = read_raster(hs_path)
        wl = np.loadtxt(C.PRE / "HS" / "wavelengths.txt")
        veg_h, t_h = otsu_mask(ndvi_hs(hs, wl), C.NDVI_MIN)
        nir = hs[band_index(wl, 800, tol=40)]
        out["HS"] = (clean(veg_h & ~shadow_mask(nir)), hs_prof, t_h)

    rgb_path = C.PRE / "RGB" / f"RGB_{date}.tif"
    if rgb_path.exists():
        rgb, rgb_prof = read_raster(rgb_path)
        veg_r, t_r = otsu_mask(excess_green(rgb), C.RGB_EXG_MIN)
        bright = np.nansum(rgb, 0)
        dark = bright < np.nanpercentile(bright, C.SHADOW_NIR_PERCENTILE)
        out["RGB"] = (clean(veg_r & ~dark, radius=2), rgb_prof, t_r)

    tir_path = C.PRE / "TIR" / f"TIR_{date}.tif"
    if tir_path.exists():
        tir, tir_prof = read_raster(tir_path)
        ms_on_tir = resample_to(out["MS"][0][None].astype("float32"), ms_prof, tir_prof, Resampling.average)[0]
        veg_t = np.nan_to_num(ms_on_tir) > 0.8                      # mostly-canopy thermal pixels
        warm, t_t = otsu_mask(tir[0])                               # soil is warmer than canopy
        out["TIR"] = (veg_t & ~warm, tir_prof, t_t)

    for sensor, (m, prof, t) in out.items():
        write_raster(C.MASK / sensor / f"{sensor}_{date}_veg.tif", m.astype("uint8"), prof, dtype="uint8", nodata=255)
        print(f"{sensor} {date}: threshold={t:.3f}  vegetation fraction={m.mean():.2f}")
    return out


if __name__ == "__main__":
    for d in C.DATES:
        mask_date(d)
