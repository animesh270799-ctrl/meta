"""Shared helpers: raster input/output, wavelengths, band lookup."""
import re
import numpy as np
import rasterio
import config as C


def read_raster(path):
    """Return (array[bands, rows, cols] as float32, rasterio profile)."""
    with rasterio.open(path) as src:
        arr = src.read().astype("float32")
        prof = src.profile.copy()
        if src.nodata is not None:
            arr[arr == src.nodata] = np.nan
    return arr, prof


def write_raster(path, arr, prof, dtype="float32", nodata=np.nan):
    path.parent.mkdir(parents=True, exist_ok=True)
    arr = np.asarray(arr)
    if arr.ndim == 2:
        arr = arr[None]
    p = prof.copy()
    p.update(driver="GTiff", count=arr.shape[0], dtype=dtype, nodata=nodata,
             compress="deflate", tiled=True, blockxsize=256, blockysize=256, BIGTIFF="IF_SAFER")
    p.pop("interleave", None)
    with rasterio.open(path, "w", **p) as dst:
        dst.write(arr.astype(dtype))


def read_hs_wavelengths(path):
    """Wavelengths (nm) from an ENVI header next to the cube, else from config.HS_WAVELENGTH_FILE."""
    hdr = path.with_suffix(".hdr")
    if hdr.exists():
        txt = hdr.read_text()
        m = re.search(r"wavelength\s*=\s*\{([^}]*)\}", txt, re.IGNORECASE)
        if m:
            wl = np.array([float(v) for v in m.group(1).replace("\n", " ").split(",") if v.strip()])
            return wl * 1000 if wl.max() < 10 else wl     # micrometres -> nm
    return np.loadtxt(C.HS_WAVELENGTH_FILE)


def band_index(wavelengths, target_nm, tol=15):
    """Index of the band nearest to target_nm, or None if none within tol nm."""
    wavelengths = np.asarray(wavelengths)
    i = int(np.argmin(np.abs(wavelengths - target_nm)))
    return i if abs(wavelengths[i] - target_nm) <= tol else None


def ms_band(arr, name):
    return arr[list(C.MS_BANDS).index(name)]


def safe_div(a, b):
    """Element-wise a / b with inf and NaN results set to NaN (works for arrays and scalars)."""
    with np.errstate(divide="ignore", invalid="ignore"):
        out = np.true_divide(a, b)
    out = np.where(np.isfinite(out), out, np.nan)
    return out if np.ndim(out) else float(out)
