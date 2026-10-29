"""Step 2 - Image pre-processing.

Assumes each orthomosaic was already stitched (Pix4D / Agisoft / Headwall SpectralView)
and georeferenced with the 12 RTK ground-control points. This step then:
  2a  converts to physical units (reflectance 0-1, temperature in deg C),
  2b  applies the empirical-line correction if calibration-panel values are supplied,
  2c  removes noisy hyperspectral bands and smooths spectra (Savitzky-Golay),
  2d  co-registers every sensor to the reference sensor (sub-pixel shift),
  2e  writes analysis-ready GeoTIFFs.
"""
import numpy as np
import pandas as pd
import rasterio
from rasterio.warp import reproject, Resampling
from rasterio.transform import Affine
from scipy.signal import savgol_filter
from skimage.registration import phase_cross_correlation
from skimage.filters import sobel
import config as C
from common import read_raster, write_raster, read_hs_wavelengths, band_index, ms_band

PANEL_CSV = C.ROOT / "calibration_panels.csv"   # optional: sensor,date,band,dn_dark,dn_bright,refl_dark,refl_bright


# ------------------------------------------------------------------ 2a units
def to_reflectance(arr, sensor):
    """Scale digital numbers to 0-1 reflectance if the orthomosaic is stored as integers."""
    p99 = np.nanpercentile(arr, 99)
    if p99 > 1.5:
        scale = 255.0 if p99 <= 255 else (65535.0 if p99 > 20000 else 10000.0)
        print(f"  {sensor}: values look scaled (p99={p99:.0f}); dividing by {scale:.0f}")
        arr = arr / scale
    return np.clip(arr, 0, 1.5)


def to_celsius(arr, counts_to_kelvin=0.04):
    """Thermal: accept deg C, Kelvin, or FLIR radiometric counts (TLinear, 0.04 K per count)."""
    med = np.nanmedian(arr)
    if med > 1000:
        print("  TIR: radiometric counts -> deg C (check the scale factor in FLIR Tools)")
        return arr * counts_to_kelvin - 273.15
    if med > 200:
        print("  TIR: Kelvin -> deg C")
        return arr - 273.15
    return arr


# ------------------------------------------------------------------ 2b empirical line
def empirical_line(arr, sensor, date):
    """Two-panel empirical line per band: refl = gain * DN + offset."""
    if not PANEL_CSV.exists():
        return arr
    cal = pd.read_csv(PANEL_CSV, dtype={"date": str})
    cal = cal[(cal.sensor == sensor) & (cal.date == date)]
    for _, r in cal.iterrows():
        b = int(r.band)
        gain = (r.refl_bright - r.refl_dark) / (r.dn_bright - r.dn_dark)
        arr[b] = gain * arr[b] + (r.refl_dark - gain * r.dn_dark)
    if len(cal):
        print(f"  {sensor} {date}: empirical-line correction applied to {len(cal)} bands")
    return arr


# ------------------------------------------------------------------ 2c hyperspectral cleaning
def clean_hyperspectral(cube, wavelengths):
    keep = np.ones(len(wavelengths), bool)
    for lo, hi in C.HS_BAD_RANGES:
        keep &= ~((wavelengths >= lo) & (wavelengths <= hi))
    cube, wavelengths = cube[keep], wavelengths[keep]
    win = min(C.SG_WINDOW, len(wavelengths) - (1 - len(wavelengths) % 2))
    if win > C.SG_POLY + 1:
        # smooth each contiguous spectral segment separately so gaps are not bridged
        breaks = np.where(np.diff(wavelengths) > 3 * np.median(np.diff(wavelengths)))[0] + 1
        for seg in np.split(np.arange(len(wavelengths)), breaks):
            w = min(win, len(seg) if len(seg) % 2 else len(seg) - 1)
            if w > C.SG_POLY + 1:
                block = cube[seg]
                nan = np.isnan(block)
                block = savgol_filter(np.nan_to_num(block), w, C.SG_POLY, axis=0)
                block[nan] = np.nan
                cube[seg] = block
    return cube, wavelengths


# ------------------------------------------------------------------ 2d co-registration
def registration_band(arr, sensor, wavelengths=None):
    """A band with clear canopy/soil contrast for each sensor."""
    if sensor == "MS":
        return ms_band(arr, "NIR")
    if sensor == "HS":
        return arr[band_index(wavelengths, 800, tol=60)]
    if sensor == "RGB":
        return arr[1]
    return -arr[0]          # thermal: canopy is cool, soil warm -> invert for similar contrast


def resample_to(src_arr, src_prof, dst_prof, method=Resampling.average):
    dst = np.full((src_arr.shape[0], dst_prof["height"], dst_prof["width"]), np.nan, "float32")
    for b in range(src_arr.shape[0]):
        reproject(src_arr[b], dst[b], src_transform=src_prof["transform"], src_crs=src_prof["crs"],
                  dst_transform=dst_prof["transform"], dst_crs=dst_prof["crs"],
                  src_nodata=np.nan, dst_nodata=np.nan, resampling=method)
    return dst


def estimate_shift(moving, reference):
    """Sub-pixel (row, col) shift that aligns `moving` to `reference`, using edge images."""
    def prep(x):
        x = np.nan_to_num((x - np.nanmean(x)) / (np.nanstd(x) + 1e-9))
        return sobel(x)
    shift, error, _ = phase_cross_correlation(prep(reference), prep(moving), upsample_factor=20)
    return shift, error


def apply_shift(prof, shift_rows, shift_cols, ref_prof):
    """Translate the geotransform by a shift measured in reference-grid pixels."""
    t, rt = prof["transform"], ref_prof["transform"]
    new = Affine(t.a, t.b, t.c + shift_cols * rt.a, t.d, t.e, t.f + shift_rows * rt.e)
    out = prof.copy()
    out["transform"] = new
    return out


# ------------------------------------------------------------------ main
def preprocess_all(max_shift_m=1.0):
    log = []
    for date in C.DATES:
        ref_arr, ref_prof = None, None
        for sensor in [C.REFERENCE_SENSOR] + [s for s in C.SENSORS if s != C.REFERENCE_SENSOR]:
            path = C.raw_path(sensor, date)
            if not path.exists():
                print(f"missing {path}")
                continue
            arr, prof = read_raster(path)
            wl = None
            if sensor == "TIR":
                arr = to_celsius(arr)
            else:
                arr = empirical_line(arr, sensor, date)
                arr = to_reflectance(arr, sensor)
            if sensor == "HS":
                wl = read_hs_wavelengths(path)
                arr, wl = clean_hyperspectral(arr, wl)
                (C.PRE / "HS").mkdir(parents=True, exist_ok=True)
                np.savetxt(C.PRE / "HS" / "wavelengths.txt", wl, fmt="%.2f")
            if sensor == C.REFERENCE_SENSOR:
                ref_arr, ref_prof = arr, prof
                shift = (0.0, 0.0)
            else:
                mov = resample_to(registration_band(arr, sensor, wl)[None], prof, ref_prof)[0]
                shift, err = estimate_shift(mov, registration_band(ref_arr, C.REFERENCE_SENSOR))
                shift_m = np.hypot(shift[0] * ref_prof["transform"].e, shift[1] * ref_prof["transform"].a)
                if shift_m > max_shift_m:
                    print(f"  WARNING {sensor} {date}: shift {shift_m:.2f} m exceeds {max_shift_m} m; not applied - check GCPs")
                    shift = (0.0, 0.0)
                else:
                    prof = apply_shift(prof, shift[0], shift[1], ref_prof)
            log.append(dict(sensor=sensor, date=date, shift_rows=shift[0], shift_cols=shift[1]))
            write_raster(C.PRE / sensor / f"{sensor}_{date}.tif", arr, prof)
            print(f"{sensor} {date}: {arr.shape} written; shift (ref px) = {np.round(shift, 2)}")
    pd.DataFrame(log).to_csv(C.PRE / "coregistration_log.csv", index=False)


if __name__ == "__main__":
    preprocess_all()
