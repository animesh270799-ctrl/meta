"""RustWatch: UAV multimodal sensing of white rust in mustard - complete pipeline in one file.

Usage
  python rustwatch_pipeline.py synthetic        # create test data with the 48-plot layout
  python rustwatch_pipeline.py all              # run steps 1-8
  python rustwatch_pipeline.py 2 3 5            # run selected steps
  python rustwatch_pipeline.py 7 --fast         # quick test of the modelling (fewer trees, 1 repeat)
Edit STEP 0 (configuration) before running with real data.
"""
import sys


# ================================================================================================
# STEP 0 - CONFIGURATION (edit this section only)
# ================================================================================================
# Step 0 - Project configuration. Edit this file only; every other module reads from it.
from pathlib import Path

# ---------------------------------------------------------------- folders
ROOT = Path(__file__).resolve().parent / "project"
RAW = ROOT / "01_orthomosaics"        # input: one orthomosaic per sensor per date
PRE = ROOT / "02_preprocessed"        # calibrated, co-registered rasters
MASK = ROOT / "03_masks"              # vegetation masks
UNMIX = ROOT / "04_unmixing"          # endmembers and abundance maps
FEAT = ROOT / "05_features"           # plot-wise feature tables
DSF = ROOT / "06_dsf"                 # Phase 1 outputs
MODELS = ROOT / "07_models"           # Phase 2 and 3 outputs
MAPS = ROOT / "08_maps"               # severity and spray maps

PLOTS_FILE = ROOT / "plots.gpkg"            # plot polygons (Step 1)
LAYOUT_CSV = ROOT / "field_layout.csv"      # plot_id, row, col, treatment, rep
GROUND_TRUTH_CSV = ROOT / "ground_truth.csv"  # plot_id, date, DI
WEATHER_CSV = ROOT / "weather.csv"            # date, air_temp_C at flight time

# ---------------------------------------------------------------- campaign
SENSORS = ["MS", "HS", "RGB", "TIR"]
DATES = ["2026-01-20", "2026-01-25", "2026-01-30", "2026-02-04"]  # replace with your 4 flight dates
CRS = "EPSG:32643"   # WGS 84 / UTM zone 43N (Delhi)

# File naming convention: RAW/<sensor>/<sensor>_<date>.tif  (HS may also be ENVI .hdr/.dat)
def raw_path(sensor, date):
    return RAW / sensor / f"{sensor}_{date}.tif"

# ---------------------------------------------------------------- sensors
# MicaSense RedEdge-MX band order and centre wavelengths (nm)
MS_BANDS = {"B": 475, "G": 560, "R": 668, "RE": 717, "NIR": 840}
RGB_BANDS = ["R", "G", "B"]
# Hyperspectral: wavelengths are read from the ENVI header if present,
# otherwise from this file (one wavelength in nm per line).
HS_WAVELENGTH_FILE = ROOT / "hs_wavelengths.txt"
HS_BAD_RANGES = [(0, 400), (1340, 1460), (1790, 1960), (2450, 3000)]  # nm removed
SG_WINDOW, SG_POLY = 11, 2               # Savitzky-Golay smoothing

REFERENCE_SENSOR = "MS"   # all sensors are resampled onto this sensor's grid for masking

# ---------------------------------------------------------------- field layout
PLOT_LENGTH_M = 5.0       # along the field's 24 m side
PLOT_WIDTH_M = 3.5        # along the field's 48 m side
N_COLS, N_ROWS = 12, 4
FIELD_WIDTH_M, FIELD_LENGTH_M = 48.0, 24.0
CHANNEL_M = 2.0           # irrigation channels after plot rows 1 and 3
PLOT_INSET_M = 0.4        # inward buffer to avoid edge effects

# Field corner of the top-left plot (row 1, column 1) and field orientation.
# Measure with RTK GNSS; rotation is degrees anticlockwise from east.
FIELD_ORIGIN_E = 712000.0
FIELD_ORIGIN_N = 3170024.0
FIELD_ROTATION_DEG = 0.0

# ---------------------------------------------------------------- labels
# DI (%) -> severity class, as in the ORW (0 healthy ... 5 very high)
DI_CLASS_BINS = [-0.01, 0.0, 5, 10, 25, 50, 100]
CLASS_NAMES = ["Healthy", "Very low", "Low", "Moderate", "High", "Very high"]

# ---------------------------------------------------------------- masking
NDVI_MIN = None           # None = automatic Otsu threshold
SHADOW_NIR_PERCENTILE = 5 # darkest NIR pixels treated as shadow
RGB_EXG_MIN = None        # None = Otsu on ExG

# ---------------------------------------------------------------- unmixing
N_ENDMEMBERS = 4          # soil, healthy canopy, diseased canopy, shadow
UNMIX_SAMPLE = 20000      # pixels sampled for endmember extraction

# ---------------------------------------------------------------- feature selection
FDR_Q = 0.05
MIN_DATES_SIGNIFICANT = 2     # of the 4 dates
JM_MIN_DERIVED = 1.0
JM_MIN_HS_BAND = 1.94
RELIEF_K = 10
BOOTSTRAP_N = 50
STABILITY_MIN = 0.6
VIF_MAX = 10.0
SFFS_MAX_FEATURES = 10
OUTER_FOLDS, INNER_FOLDS = 4, 4
N_REPEATS = 3
RANDOM_STATE = 2026

C = sys.modules[__name__]     # lets every step write C.SETTING


# ================================================================================================
# SHARED HELPERS
# ================================================================================================
# Shared helpers: raster input/output, wavelengths, band lookup.
import re
import numpy as np
import rasterio


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


# ================================================================================================
# STEP 1 - FIELD LAYOUT, PLOT POLYGONS, GROUND TRUTH
# ================================================================================================
# Step 1 - Field layout, plot polygons and ground-truth labels.
import numpy as np
import pandas as pd
import geopandas as gpd
from shapely.geometry import Polygon
from shapely import affinity

# Plot numbers and treatments exactly as in the field-layout slide (row 1 = top/north row).
PLOT_IDS = [
    [48, 41, 40, 33, 32, 25, 24, 17, 16, 9, 8, 1],
    [47, 42, 39, 34, 31, 26, 23, 18, 15, 10, 7, 2],
    [46, 43, 38, 35, 30, 27, 22, 19, 14, 11, 6, 3],
    [45, 44, 37, 36, 29, 28, 21, 20, 13, 12, 5, 4],
]
TREATMENTS = [
    ["D3V3", "D1V1", "D2V2", "D4V3", "D3V2", "D1V3", "D1V1", "D3V2", "D2V3", "D2V1", "D2V3", "D4V2"],
    ["D4V1", "D1V2", "D2V3", "D1V1", "D4V2", "D2V1", "D1V3", "D4V2", "D3V1", "D3V3", "D1V1", "D2V2"],
    ["D4V3", "D4V1", "D1V3", "D2V2", "D1V2", "D2V3", "D2V1", "D2V2", "D4V1", "D3V2", "D4V3", "D1V3"],
    ["D2V2", "D3V2", "D3V1", "D3V1", "D3V3", "D4V1", "D3V3", "D4V3", "D1V2", "D4V1", "D1V2", "D3V1"],
]
BLOCKS = ["R1"] * 3 + ["R2"] * 3 + ["R3"] * 3 + ["CONTROL"] * 3   # by column


def build_layout_table():
    rows = []
    for r in range(C.N_ROWS):
        for c in range(C.N_COLS):
            t = TREATMENTS[r][c]
            rows.append(dict(plot_id=PLOT_IDS[r][c], row=r + 1, col=c + 1, treatment=t,
                             inoc_age=t[:2], variety=t[2:], block=BLOCKS[c],
                             inoculated=BLOCKS[c] != "CONTROL"))
    return pd.DataFrame(rows).sort_values("plot_id").reset_index(drop=True)


def check_layout(layout):
    """Every replication block should contain each of the 12 treatments exactly once."""
    problems = []
    for block, g in layout.groupby("block"):
        counts = g["treatment"].value_counts()
        dup = counts[counts > 1].index.tolist()
        missing = sorted({f"D{d}V{v}" for d in range(1, 5) for v in range(1, 4)} - set(g["treatment"]))
        if dup or missing:
            problems.append(f"{block}: repeated {dup}, missing {missing}")
    return problems


def row_top_offset(r):
    """Distance (m) from the field's north edge to the top of plot row r (1-based)."""
    channels_above = (1 if r >= 2 else 0) + (1 if r >= 4 else 0)
    return (r - 1) * C.PLOT_LENGTH_M + channels_above * C.CHANNEL_M


def build_plot_polygons(layout):
    gap = (C.FIELD_WIDTH_M - C.N_COLS * C.PLOT_WIDTH_M) / (C.N_COLS - 1)
    geoms = []
    for _, p in layout.iterrows():
        x0 = (p.col - 1) * (C.PLOT_WIDTH_M + gap)
        y0 = -row_top_offset(p.row)
        poly = Polygon([(x0, y0), (x0 + C.PLOT_WIDTH_M, y0),
                        (x0 + C.PLOT_WIDTH_M, y0 - C.PLOT_LENGTH_M), (x0, y0 - C.PLOT_LENGTH_M)])
        poly = affinity.rotate(poly, C.FIELD_ROTATION_DEG, origin=(0, 0))
        geoms.append(affinity.translate(poly, C.FIELD_ORIGIN_E, C.FIELD_ORIGIN_N))
    gdf = gpd.GeoDataFrame(layout.copy(), geometry=geoms, crs=C.CRS)
    gdf["geometry_inner"] = gdf.geometry.buffer(-C.PLOT_INSET_M, join_style="mitre")
    return gdf


def di_to_class(di):
    return pd.cut(di, bins=C.DI_CLASS_BINS, labels=range(len(C.CLASS_NAMES))).astype(int)


def load_ground_truth(layout):
    gt = pd.read_csv(C.GROUND_TRUTH_CSV, dtype={"date": str})
    gt["severity_class"] = di_to_class(gt["DI"])
    gt["diseased"] = (gt["severity_class"] > 0).astype(int)
    gt = gt.merge(layout[["plot_id", "block", "treatment", "inoc_age", "variety", "inoculated"]],
                  on="plot_id", how="left")
    bad = gt[(~gt["inoculated"]) & (gt["DI"] > 0)]
    if len(bad):
        print(f"WARNING: {len(bad)} control plot-dates have DI > 0 (natural infection?)")
    return gt


# ================================================================================================
# STEP 2 - PRE-PROCESSING AND CO-REGISTRATION
# ================================================================================================
# Step 2 - Image pre-processing.
#
# Assumes each orthomosaic was already stitched (Pix4D / Agisoft / Headwall SpectralView)
# and georeferenced with the 12 RTK ground-control points. This step then:
#   2a  converts to physical units (reflectance 0-1, temperature in deg C),
#   2b  applies the empirical-line correction if calibration-panel values are supplied,
#   2c  removes noisy hyperspectral bands and smooths spectra (Savitzky-Golay),
#   2d  co-registers every sensor to the reference sensor (sub-pixel shift),
#   2e  writes analysis-ready GeoTIFFs.
import numpy as np
import pandas as pd
import rasterio
from rasterio.warp import reproject, Resampling
from rasterio.transform import Affine
from scipy.signal import savgol_filter
from skimage.registration import phase_cross_correlation
from skimage.filters import sobel

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


# ================================================================================================
# STEP 3 - VEGETATION MASKING, SOIL AND SHADOW REMOVAL
# ================================================================================================
# Step 3 - Vegetation masking, soil removal and shadow removal.
#
# MS and HS : NDVI > Otsu threshold, minus the darkest NIR pixels (shadow).
# RGB       : Excess Green (ExG) > Otsu threshold, minus very dark pixels.
# TIR       : no spectral information, so the MS vegetation mask of the same date is
#             resampled onto the thermal grid, then pixels warmer than the
#             canopy/soil Otsu split are removed (mixed soil pixels).
# Optional  : K-means clustering instead of a threshold (method="kmeans").
import numpy as np
from skimage.filters import threshold_otsu
from skimage.morphology import binary_opening, disk
from sklearn.cluster import KMeans
from rasterio.warp import Resampling


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


# ================================================================================================
# STEP 4 - ENDMEMBER EXTRACTION (VCA) AND UNMIXING (FCLS)
# ================================================================================================
# Step 4 - Endmember extraction (VCA) and spectral unmixing (FCLS).
#
# 4a  sample pixels from all dates inside the plots (one endmember set for all dates,
#     so abundances are comparable over time),
# 4b  extract p endmembers with Vertex Component Analysis (Nascimento & Bioucas-Dias, 2005),
# 4c  name the endmembers (soil, healthy canopy, diseased canopy, shadow) by spectral
#     angle to reference spectra taken from the data (control plots = healthy,
#     most severe plots = diseased, bright non-vegetation = soil, darkest pixels = shadow),
# 4d  unmix every plot pixel with Fully Constrained Least Squares (abundances >= 0, sum = 1),
# 4e  write abundance rasters; plot means become features in Step 5.
# Works for HS (default) and, with <= 5 endmembers, for MS.
import numpy as np
import pandas as pd
import geopandas as gpd
from rasterio.features import rasterize
from scipy.optimize import nnls, linear_sum_assignment
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

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


# ================================================================================================
# STEP 5 - PLOT-WISE FEATURE EXTRACTION
# ================================================================================================
# Step 5 - Plot-wise feature extraction.
#
# For every sensor, date and plot (polygon shrunk inward by PLOT_INSET_M) the vegetation
# pixels are summarised into one row of features:
#   MS  : band reflectance, 12 vegetation indices, canopy cover
#   HS  : mean spectrum (every retained band), first-derivative edge features, red-edge
#         position, continuum-removed absorption features, narrow-band indices,
#         endmember abundances
#   RGB : colour indices and GLCM texture (8 metrics x 3 bands)
#   TIR : canopy temperature statistics, CTD, CTR, NRCT and GLCM texture
# Output: FEAT/features_<sensor>.csv  (one row per plot_id x date)
import numpy as np
import pandas as pd
import geopandas as gpd
import rasterio
from rasterio.features import geometry_mask
from rasterio.windows import from_bounds
from skimage.feature import graycomatrix


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


# ================================================================================================
# STEP 6 - PHASE 1: DISEASE-SPECIFIC FEATURE SELECTION
# ================================================================================================
# Step 6 - Phase 1: Disease-Specific Feature (DSF) selection, run separately for each sensor.
#
# 6.1 quality control (missing values, near-zero variance, outlier flags)
# 6.2 Kruskal-Wallis across severity classes on each date + Benjamini-Hochberg FDR
#     (+ Welch t-test healthy vs diseased, reported)
# 6.3 Jeffries-Matusita distance healthy vs each severity class; HS separability scalogram
# 6.4 ReliefF (multivariate filter)
# 6.5 Random-forest permutation importance (grouped CV) and Boruta (all-relevant)
# 6.6 consensus rule + stability over random half-samples of plots -> candidate DSFs
# 6.7 Spearman correlation with DI and correlation clustering (interpretation only)
# Collinear features are NOT removed in this phase.
import warnings
import numpy as np
import pandas as pd
from scipy.stats import kruskal, ttest_ind, spearmanr, binom
from scipy.spatial.distance import cdist, squareform
from scipy.cluster.hierarchy import linkage, fcluster
from statsmodels.stats.multitest import multipletests
from sklearn.ensemble import RandomForestClassifier
from sklearn.inspection import permutation_importance
from sklearn.model_selection import GroupKFold
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

warnings.filterwarnings("ignore", category=RuntimeWarning)
TARGET = "severity_class"
ID_COLS = ["plot_id", "date"]


# ------------------------------------------------------------------ data
def load_table(sensors):
    """Ground truth merged with the feature tables of the given sensors (one row per plot x date)."""
    df = load_ground_truth(build_layout_table())
    cols = []
    for s in sensors:
        f = pd.read_csv(C.FEAT / f"features_{s}.csv", dtype={"date": str})
        cols += [c for c in f.columns if c not in ID_COLS]
        df = df.merge(f, on=ID_COLS, how="inner")
    return df.reset_index(drop=True), cols


# ------------------------------------------------------------------ 6.1 quality control
def quality_control(df, cols, max_missing=0.05):
    keep, report = [], []
    for c in cols:
        x = df[c]
        if x.isna().mean() > max_missing:
            report.append((c, "missing")); continue
        vc = x.round(10).value_counts()
        freq_ratio = vc.iloc[0] / vc.iloc[1] if len(vc) > 1 else np.inf
        if freq_ratio > 19 and 100 * len(vc) / len(x) < 10:
            report.append((c, "near-zero variance")); continue
        keep.append(c)
    df = df.copy()
    df[keep] = df.groupby("date")[keep].transform(lambda s: s.fillna(s.median()))
    med = df.groupby("date")[keep].transform("median")
    mad = df.groupby("date")[keep].transform(lambda s: (s - s.median()).abs().median())
    mz = 0.6745 * (df[keep] - med) / mad.replace(0, np.nan)
    n_out = int((mz.abs() > 3.5).any(axis=1).sum())
    return df, keep, pd.DataFrame(report, columns=["feature", "reason"]), n_out


# ------------------------------------------------------------------ 6.2 statistics + FDR
def kruskal_p(df, c, target=TARGET):
    groups = [g[c].values for _, g in df.groupby(target) if len(g) >= 2]
    if len(groups) < 2:
        return np.nan, np.nan
    try:
        h, p = kruskal(*groups)
    except ValueError:            # all values identical
        return 0.0, 1.0
    return h, p


def stat_screen(df, cols, target=TARGET):
    res = pd.DataFrame(index=cols)
    sig_counts = pd.Series(0, index=cols)
    for date, g in df.groupby("date"):
        hp = np.array([kruskal_p(g, c, target) for c in cols])
        p = np.nan_to_num(hp[:, 1], nan=1.0)
        q = multipletests(p, method="fdr_bh")[1]
        res[f"q_{date}"] = q
        sig_counts += (q < C.FDR_Q).astype(int)
        hd = g[target] > 0
        res[f"t_p_{date}"] = [ttest_ind(g.loc[hd, c], g.loc[~hd, c], equal_var=False).pvalue
                              if hd.sum() > 1 and (~hd).sum() > 1 else np.nan for c in cols]
    hp_all = np.array([kruskal_p(df, c, target) for c in cols])
    res["H_pooled"] = hp_all[:, 0]
    res["q_pooled"] = multipletests(np.nan_to_num(hp_all[:, 1], nan=1.0), method="fdr_bh")[1]
    res["epsilon2"] = res["H_pooled"] / (len(df) - 1)
    res["n_dates_sig"] = sig_counts
    return res


# ------------------------------------------------------------------ 6.3 Jeffries-Matusita
def jm_1d(x1, x2):
    m1, m2 = np.mean(x1), np.mean(x2)
    v1, v2 = np.var(x1, ddof=1) + 1e-12, np.var(x2, ddof=1) + 1e-12
    b = (m1 - m2) ** 2 / (4 * (v1 + v2)) + 0.5 * np.log((v1 + v2) / (2 * np.sqrt(v1 * v2)))
    return 2 * (1 - np.exp(-b))


def jm_table(df, cols, target=TARGET):
    healthy = df[df[target] == 0]
    out = pd.DataFrame(index=cols)
    for k in sorted(df[target].unique()):
        if k == 0:
            continue
        d = df[df[target] == k]
        if len(d) >= 3 and len(healthy) >= 3:
            out[f"JM_0v{k}"] = [jm_1d(healthy[c].values, d[c].values) for c in cols]
    out["JM_max"] = out.max(axis=1) if out.shape[1] else np.nan
    return out


def is_hs_band(c):
    return c.startswith("HS_R") and c[4:].replace(".", "").isdigit()


def plot_scalogram(table, path):
    bands = [c for c in table.index if is_hs_band(c)]
    if not bands:
        return
    wl = np.array([float(c[4:]) for c in bands])
    o = np.argsort(wl)
    fig, ax = plt.subplots(figsize=(8, 3.5))
    for col in [c for c in table.columns if c.startswith("JM_0v")]:
        ax.plot(wl[o], table.loc[bands, col].values[o], lw=1, label=col.replace("JM_0v", "healthy vs class "))
    ax.axhline(C.JM_MIN_HS_BAND, color="k", ls="--", lw=1, label=f"JM = {C.JM_MIN_HS_BAND}")
    ax.set_xlabel("Wavelength (nm)"); ax.set_ylabel("JM distance"); ax.set_ylim(0, 2.05)
    ax.legend(fontsize=7, ncol=3); fig.tight_layout(); fig.savefig(path, dpi=150); plt.close(fig)


# ------------------------------------------------------------------ 6.4 ReliefF
def relieff(X, y, k=C.RELIEF_K):
    X = np.asarray(X, float)
    rng_ = X.max(0) - X.min(0)
    X = (X - X.min(0)) / np.where(rng_ == 0, 1, rng_)
    n, p = X.shape
    classes, counts = np.unique(y, return_counts=True)
    prior = dict(zip(classes, counts / n))
    D = cdist(X, X, "cityblock")
    np.fill_diagonal(D, np.inf)
    W = np.zeros(p)
    for i in range(n):
        same = np.where(y == y[i])[0]
        same = same[same != i]
        if len(same):
            h = same[np.argsort(D[i, same])[:k]]
            W -= np.abs(X[h] - X[i]).sum(0) / (n * len(h))
        for c in classes:
            if c == y[i]:
                continue
            other = np.where(y == c)[0]
            m = other[np.argsort(D[i, other])[:k]]
            W += prior[c] / (1 - prior[y[i]]) * np.abs(X[m] - X[i]).sum(0) / (n * len(m))
    return W


# ------------------------------------------------------------------ 6.5 RF importance + Boruta
def rf_permutation_importance(X, y, groups, n_trees=300, seed=C.RANDOM_STATE):
    imps = []
    for tr, te in GroupKFold(n_splits=C.INNER_FOLDS).split(X, y, groups):
        rf = RandomForestClassifier(n_trees, class_weight="balanced", random_state=seed, n_jobs=-1).fit(X[tr], y[tr])
        r = permutation_importance(rf, X[te], y[te], n_repeats=5, random_state=seed, scoring="f1_macro", n_jobs=-1)
        imps.append(r.importances_mean)
    return np.mean(imps, 0)


def boruta(X, y, n_iter=60, n_trees=200, alpha=0.01, seed=C.RANDOM_STATE):
    """Shadow-feature test (Kursa & Rudnicki, 2010). Returns 'confirmed' / 'tentative' / 'rejected'."""
    rng = np.random.default_rng(seed)
    n, p = X.shape
    hits = np.zeros(p)
    for it in range(n_iter):
        shadow = rng.permuted(X, axis=0)
        rf = RandomForestClassifier(n_trees, class_weight="balanced", random_state=seed + it, n_jobs=-1)
        rf.fit(np.hstack([X, shadow]), y)
        imp = rf.feature_importances_
        hits += imp[:p] > imp[p:].max()
    a = alpha / p                                           # Bonferroni
    confirmed = binom.sf(hits - 1, n_iter, 0.5) < a
    rejected = binom.cdf(hits, n_iter, 0.5) < a
    return np.where(confirmed, "confirmed", np.where(rejected, "rejected", "tentative")), hits / n_iter


# ------------------------------------------------------------------ 6.6 consensus + stability
def stability(df, cols, n_sub=C.BOOTSTRAP_N, seed=C.RANDOM_STATE):
    """Fraction of random half-samples of plots in which a feature passes FDR and is in the ReliefF top half."""
    rng = np.random.default_rng(seed)
    plots = df.plot_id.unique()
    freq = np.zeros(len(cols))
    for _ in range(n_sub):
        sub = df[df.plot_id.isin(rng.choice(plots, len(plots) // 2, replace=False))]
        p = np.array([kruskal_p(sub, c)[1] for c in cols])
        q = multipletests(np.nan_to_num(p, nan=1.0), method="fdr_bh")[1]
        w = relieff(sub[cols].values, sub[TARGET].values)
        freq += (q < C.FDR_Q) & (w > 0) & (w >= np.median(w))
    return freq / n_sub


def select_dsf(df, cols, fast=False, out_prefix=None):
    """Phase 1 for one sensor. Returns (DSF list, full table, consensus rank Series)."""
    df, cols, qc_report, n_out = quality_control(df, cols)
    X, y, g = df[cols].values, df[TARGET].values, df.plot_id.values
    t = stat_screen(df, cols)
    t = t.join(jm_table(df, cols))
    t["relief"] = relieff(X, y)
    t["rf_perm"] = rf_permutation_importance(X, y, g, n_trees=100 if fast else 300)
    t["boruta"], t["boruta_hits"] = boruta(X, y, n_iter=20 if fast else 60, n_trees=100 if fast else 200)

    t["pass_stat"] = t["n_dates_sig"] >= C.MIN_DATES_SIGNIFICANT
    jm_thr = np.where([is_hs_band(c) for c in cols], C.JM_MIN_HS_BAND, C.JM_MIN_DERIVED)
    t["pass_sep"] = t["JM_max"].fillna(0).values >= jm_thr
    t["vote_relief"] = (t["relief"] > 0) & (t["relief"] >= t["relief"].median())
    t["vote_rf"] = t["rf_perm"] >= t["rf_perm"].median()
    t["vote_boruta"] = t["boruta"] == "confirmed"
    t["votes"] = t[["vote_relief", "vote_rf", "vote_boruta"]].sum(1)
    candidate = t["pass_stat"] & t["pass_sep"] & (t["votes"] >= 2)
    if not fast:
        t["stability"] = 0.0
        if candidate.any():
            t.loc[candidate, "stability"] = stability(df, list(t.index[candidate]))
        candidate &= t["stability"] >= C.STABILITY_MIN
    t["DSF"] = candidate

    ranks = pd.concat([t["q_pooled"].rank(), t["JM_max"].rank(ascending=False),
                       t["relief"].rank(ascending=False), t["rf_perm"].rank(ascending=False)], axis=1)
    t["consensus_rank"] = ranks.mean(1).rank()
    dsf = list(t.index[t["DSF"]])
    if len(dsf) < 3:          # never leave a sensor empty: fall back to the best-ranked features
        dsf = list(t.sort_values("consensus_rank").index[:5])
        t["DSF_fallback"] = t.index.isin(dsf)

    if out_prefix is not None:
        C.DSF.mkdir(parents=True, exist_ok=True)
        t["rho_DI"] = [spearmanr(df[c], df["DI"])[0] for c in cols]
        if len(dsf) > 2:
            rho = df[dsf].corr("spearman").abs().fillna(0).values
            dist = squareform(1 - rho, checks=False)
            t.loc[dsf, "cluster"] = fcluster(linkage(dist, "average"), t=0.3, criterion="distance")
        t.sort_values("consensus_rank").to_csv(C.DSF / f"{out_prefix}_feature_table.csv")
        qc_report.to_csv(C.DSF / f"{out_prefix}_qc_removed.csv", index=False)
        plot_scalogram(t, C.DSF / f"{out_prefix}_JM_scalogram.png")
        print(f"{out_prefix}: {len(cols)} features after QC, {n_out} plot-dates flagged as outliers, "
              f"{len(dsf)} DSFs")
    return dsf, t, t["consensus_rank"]


# ================================================================================================
# STEP 7 - PHASES 2-3: VIF, SPA, SFFS, CLASSIFIERS, NESTED CV
# ================================================================================================
# Step 7 - Phases 2 and 3: redundancy removal, SFFS, classifiers and nested grouped CV.
#
# 7.1 relevance-guided VIF (< 10)          (per sensor in Phase 2, pooled in Phase 3)
# 7.2 SPA for raw hyperspectral bands      (bands are p >> n, so VIF cannot be used)
# 7.3 SFFS per classifier (mlxtend, floating=True), inner CV grouped by plot,
#     subset size by the one-standard-error rule -> OFC
# 7.4 hyperparameter tuning on the OFC (GridSearchCV, inner grouped CV)
# 7.5 nested, plot-grouped, repeated outer CV; Phase 1 is re-run inside every outer
#     training fold so no label information leaks into the test fold
# 7.6 metrics: OA, macro-F1, kappa, per-class precision / recall / specificity
import os
import warnings
import numpy as np
import pandas as pd
from sklearn.base import clone
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestClassifier
from sklearn.svm import SVC
from sklearn.neighbors import KNeighborsClassifier
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis
from sklearn.model_selection import GroupKFold, StratifiedGroupKFold, GridSearchCV, cross_val_score
from sklearn.metrics import accuracy_score, f1_score, cohen_kappa_score, confusion_matrix
from mlxtend.feature_selection import SequentialFeatureSelector as SFS

warnings.filterwarnings("ignore")
FAST = os.environ.get("RW_FAST") == "1"     # quick settings for testing the code


def pipe(clf):
    return Pipeline([("imp", SimpleImputer(strategy="median")), ("sc", StandardScaler()), ("clf", clf)])


def classifiers():
    rs = C.RANDOM_STATE
    n_trees = 60 if FAST else 300
    return {
        "RF": (pipe(RandomForestClassifier(n_trees, class_weight="balanced", random_state=rs, n_jobs=-1)),
               {"clf__max_features": ["sqrt", 0.5], "clf__min_samples_leaf": [1, 3]}),
        "SVM": (pipe(SVC(kernel="rbf", class_weight="balanced", random_state=rs)),
                {"clf__C": 2.0 ** np.arange(-3, 12, 2), "clf__gamma": 2.0 ** np.arange(-11, 2, 2)}),
        "KNN": (pipe(KNeighborsClassifier()),
                {"clf__n_neighbors": [3, 5, 7, 9, 11, 15], "clf__weights": ["uniform", "distance"]}),
    }


def inner_cv(groups, n=None):
    return GroupKFold(n_splits=n or C.INNER_FOLDS)


# ------------------------------------------------------------------ 7.1 VIF
def vif_values(X):
    R = np.corrcoef(np.asarray(X, float), rowvar=False)
    return np.diag(np.linalg.pinv(R))              # VIF_j = (R^-1)_jj


def vif_filter(X, rank, thresh=C.VIF_MAX):
    """Iteratively drop, among features with VIF >= thresh, the one with the WORST Phase 1 rank."""
    feats = list(X.columns)
    removed = []
    while len(feats) > 1:
        v = vif_values(X[feats].fillna(X[feats].median()))
        if np.nanmax(v) < thresh:
            break
        high = [f for f, vi in zip(feats, v) if vi >= thresh]
        drop = max(high, key=lambda f: rank.get(f, np.inf))
        feats.remove(drop)
        removed.append(drop)
    return feats, removed


# ------------------------------------------------------------------ 7.2 SPA
def spa_chains(X, max_vars):
    """Successive Projections Algorithm (Araujo et al., 2001): one chain per starting band."""
    Xc = X - X.mean(0)
    p = Xc.shape[1]
    starts = range(p) if p <= 60 else np.linspace(0, p - 1, 60).astype(int)
    chains = []
    for k0 in starts:
        sel, Xp = [int(k0)], Xc.copy()
        for _ in range(min(max_vars, p) - 1):
            xk = Xp[:, sel[-1]].copy()
            Xp = Xp - np.outer(xk, xk @ Xp) / (xk @ xk + 1e-12)
            norms = np.linalg.norm(Xp, axis=0)
            norms[sel] = -1
            sel.append(int(np.argmax(norms)))
        chains.append(sel)
    return chains


def spa_select(Xdf, y, groups, max_vars=10):
    """Pick the chain prefix with the best grouped-CV accuracy of LDA (SPA-LDA, Pontes et al., 2005)."""
    X = Xdf.fillna(Xdf.median()).values
    cv = list(inner_cv(groups).split(X, y, groups))
    best, best_set = -np.inf, None
    for chain in spa_chains(X, max_vars):
        for m in range(2, len(chain) + 1):
            s = cross_val_score(LinearDiscriminantAnalysis(), X[:, chain[:m]], y, cv=cv, scoring="f1_macro").mean()
            if s > best:
                best, best_set = s, chain[:m]
    return [Xdf.columns[i] for i in best_set]


# ------------------------------------------------------------------ 7.3 SFFS
def sffs(estimator, X, y, groups, max_k=C.SFFS_MAX_FEATURES):
    cv = list(inner_cv(groups).split(X, y, groups))
    k_hi = min(max_k if not FAST else 6, X.shape[1])
    sfs = SFS(clone(estimator), k_features=(1, k_hi), forward=True, floating=True,
              scoring="f1_macro", cv=cv, n_jobs=-1)
    sfs.fit(X, y)
    res = sfs.subsets_
    best_k = max(res, key=lambda k: res[k]["avg_score"])
    se = np.std(res[best_k]["cv_scores"], ddof=1) / np.sqrt(len(cv))
    k_sel = min(k for k in res if res[k]["avg_score"] >= res[best_k]["avg_score"] - se)   # one-SE rule
    return list(res[k_sel]["feature_names"]), pd.DataFrame(
        [(k, v["avg_score"], ";".join(v["feature_names"])) for k, v in res.items()], columns=["k", "macro_F1", "features"])


# ------------------------------------------------------------------ 7.4 per-fold model building
def sensor_of(col):
    return col.split("_")[0]


def dsf_for_sensor(train, sensor_cols, sensor, fast=True):
    dsf, _, rank = select_dsf(train, sensor_cols, fast=fast)
    if sensor == "HS":
        bands = [f for f in dsf if is_hs_band(f)]
        if len(bands) > 10:
            bands = spa_select(train[bands], train[TARGET].values, train.plot_id.values)
        dsf = bands + [f for f in dsf if not is_hs_band(f)]
    return dsf, rank


def build_model(train, dsf_by_sensor, rank_by_sensor, sensors, clf_name):
    feats = [f for s in sensors for f in dsf_by_sensor[s]]
    rank = pd.concat([rank_by_sensor[s] for s in sensors])
    feats, _ = vif_filter(train[feats], rank)
    est, grid = classifiers()[clf_name]
    y, g = train[TARGET].values, train.plot_id.values
    ofc, _ = sffs(est, train[feats], y, g)
    gs = GridSearchCV(clone(est), grid, scoring="f1_macro", cv=list(inner_cv(g).split(train, y, g)), n_jobs=-1)
    gs.fit(train[ofc], y)
    return dict(model=gs.best_estimator_, ofc=ofc, after_vif=feats, params=gs.best_params_)


# ------------------------------------------------------------------ 7.5 nested CV
def run_nested(df, feature_cols, configs, clf_names=("RF", "SVM", "KNN"), n_repeats=None, outer_folds=None):
    """configs: dict name -> list of sensors, e.g. {"MS": ["MS"], "F2_MS+TIR": ["MS", "TIR"]}.
    Phase 1 runs once per sensor per outer fold and is shared by all configurations."""
    y, g = df[TARGET].values, df.plot_id.values
    preds, picks = [], []
    sensors_needed = sorted({s for v in configs.values() for s in v})
    for rep in range(n_repeats or (1 if FAST else C.N_REPEATS)):
        outer = StratifiedGroupKFold(n_splits=outer_folds or C.OUTER_FOLDS, shuffle=True, random_state=C.RANDOM_STATE + rep)
        for fold, (tr, te) in enumerate(outer.split(df, y, g)):
            train, test = df.iloc[tr], df.iloc[te]
            dsf, rank = {}, {}
            for s in sensors_needed:
                dsf[s], rank[s] = dsf_for_sensor(train, [c for c in feature_cols if sensor_of(c) == s], s)
            for name, sensors in configs.items():
                for clf in clf_names:
                    m = build_model(train, dsf, rank, sensors, clf)
                    yp = m["model"].predict(test[m["ofc"]])
                    preds.append(pd.DataFrame(dict(config=name, clf=clf, repeat=rep, fold=fold, row=test.index,
                                                   plot_id=test.plot_id.values, date=test.date.values,
                                                   y_true=test[TARGET].values, y_pred=yp)))
                    picks.append(dict(config=name, clf=clf, repeat=rep, fold=fold, n_after_vif=len(m["after_vif"]),
                                      ofc=";".join(m["ofc"]), params=str(m["params"])))
                    print(f"rep {rep} fold {fold} {name:<14} {clf:<4} OFC={len(m['ofc'])} "
                          f"F1={f1_score(test[TARGET], yp, average='macro', zero_division=0):.2f}")
    return pd.concat(preds, ignore_index=True), pd.DataFrame(picks)


# ------------------------------------------------------------------ 7.6 metrics
def specificity_per_class(cm):
    out = []
    for k in range(cm.shape[0]):
        tn = cm.sum() - cm[k].sum() - cm[:, k].sum() + cm[k, k]
        fp = cm[:, k].sum() - cm[k, k]
        out.append(tn / (tn + fp) if tn + fp else np.nan)
    return out


def summarize(preds):
    rows = []
    for (cfg, clf), d in preds.groupby(["config", "clf"]):
        per_rep = d.groupby("repeat").apply(lambda r: pd.Series(dict(
            OA=accuracy_score(r.y_true, r.y_pred),
            macro_F1=f1_score(r.y_true, r.y_pred, average="macro", zero_division=0),
            kappa=cohen_kappa_score(r.y_true, r.y_pred))), include_groups=False)
        rows.append(dict(config=cfg, clf=clf, **{f"{m}_mean": per_rep[m].mean() for m in per_rep},
                         **{f"{m}_sd": per_rep[m].std(ddof=1) for m in per_rep}))
    return pd.DataFrame(rows).sort_values("macro_F1_mean", ascending=False)


def class_report(preds, cfg, clf):
    d = preds[(preds.config == cfg) & (preds.clf == clf)]
    labels = sorted(set(d.y_true) | set(d.y_pred))
    cm = confusion_matrix(d.y_true, d.y_pred, labels=labels)
    rec = np.diag(cm) / cm.sum(1).clip(min=1)
    prec = np.diag(cm) / cm.sum(0).clip(min=1)
    return cm, pd.DataFrame(dict(cls=labels, precision=prec, recall=rec, specificity=specificity_per_class(cm)))


# ================================================================================================
# STEP 8 - FUSION, FINAL MODEL, SHAP, MAPS, DI REGRESSION
# ================================================================================================
# Step 8 - Single-sensor vs multi-sensor comparison, final model, SHAP, maps, regression.
#
# 8.1 nested CV for the 4 single sensors (Phase 2) and the 4 fusion scenarios (Phase 3)
# 8.2 fusion gain = best fused macro-F1 - best single-sensor macro-F1; McNemar test
# 8.3 final model on all data for the best configuration; robust cross-classifier features
# 8.4 SHAP explanation and sensor contributions
# 8.5 severity map and three-zone spray map for every flight date
# 8.6 regression of the continuous Disease Index (R2, RMSE, RE) with grouped CV
import numpy as np
import pandas as pd
import geopandas as gpd
import shap
from collections import Counter
from statsmodels.stats.contingency_tables import mcnemar
from sklearn.ensemble import RandomForestRegressor
from sklearn.calibration import CalibratedClassifierCV
from sklearn.base import clone
from sklearn.model_selection import GroupKFold
from sklearn.metrics import r2_score, mean_squared_error
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Patch

SINGLE = {s: [s] for s in C.SENSORS}
FUSION = {"F1_RGB+TIR": ["RGB", "TIR"], "F2_MS+TIR": ["MS", "TIR"],
          "F3_HS+TIR": ["HS", "TIR"], "F4_ALL": ["RGB", "MS", "HS", "TIR"]}
ZONE = {0: "Green", 1: "Green", 2: "Amber", 3: "Amber", 4: "Red", 5: "Red"}   # agree with pathologists
ZONE_COLOUR = {"Green": "#3E7B4F", "Amber": "#E0A526", "Red": "#A63A2A"}
CLASS_COLOUR = ["#2E7D32", "#9CCC65", "#FFEE58", "#FFA726", "#EF5350", "#8E0000"]


# ------------------------------------------------------------------ 8.2 fusion gain + McNemar
def mcnemar_test(preds, a, b, repeat=0):
    """a, b = (config, clf). Paired on the same rows of the same outer-CV repeat."""
    pa = preds[(preds.config == a[0]) & (preds.clf == a[1]) & (preds.repeat == repeat)].set_index("row")
    pb = preds[(preds.config == b[0]) & (preds.clf == b[1]) & (preds.repeat == repeat)].set_index("row")
    ca, cb = (pa.y_true == pa.y_pred), (pb.y_true == pb.y_pred).reindex(pa.index)
    table = [[(ca & cb).sum(), (ca & ~cb).sum()], [(~ca & cb).sum(), (~ca & ~cb).sum()]]
    return mcnemar(table, exact=True).pvalue


def fusion_gain(summary, preds):
    single = summary[summary.config.isin(SINGLE)]
    fused = summary[summary.config.isin(FUSION)]
    rows = []
    for clf in summary.clf.unique():
        bs = single[single.clf == clf].iloc[0]
        for _, f in fused[fused.clf == clf].iterrows():
            rows.append(dict(clf=clf, fusion=f.config, best_single=bs.config,
                             gain_macro_F1=f.macro_F1_mean - bs.macro_F1_mean, gain_OA=f.OA_mean - bs.OA_mean,
                             mcnemar_p=mcnemar_test(preds, (f.config, clf), (bs.config, clf))))
    return pd.DataFrame(rows)


# ------------------------------------------------------------------ 8.3 final model
def final_model(df, cols, sensors, clf):
    dsf, rank = {}, {}
    for s in sensors:
        dsf[s], rank[s] = dsf_for_sensor(df, [c for c in cols if sensor_of(c) == s], s, fast=False)
    return build_model(df, dsf, rank, sensors, clf)


def robust_features(picks, config):
    """Features chosen in >= 2 of the 3 classifiers' OFCs, counted over all outer folds."""
    d = picks[picks.config == config]
    per_clf = {clf: Counter(f for o in g.ofc for f in o.split(";")) for clf, g in d.groupby("clf")}
    n_folds = d.groupby("clf").size().max()
    feats = set().union(*per_clf.values())
    rows = [dict(feature=f, **{f"{clf}_freq": per_clf[clf][f] / n_folds for clf in per_clf}) for f in feats]
    t = pd.DataFrame(rows)
    t["n_classifiers"] = (t.filter(like="_freq") >= 0.5).sum(1)
    return t.sort_values("n_classifiers", ascending=False)


# ------------------------------------------------------------------ 8.4 SHAP
def probability_function(clf, Xs, y):
    """Class probabilities for Kernel SHAP. SVC has no predict_proba unless calibrated."""
    try:
        clf.predict_proba(Xs[:1])
        return clf.predict_proba
    except AttributeError:
        pass
    n_min = int(pd.Series(y).value_counts().min())
    if n_min >= 2:
        cal = CalibratedClassifierCV(clone(clf), cv=min(3, n_min)).fit(Xs, y)
        return cal.predict_proba
    classes = np.unique(y)                              # last resort: explain the predicted label
    return lambda X: (clf.predict(X)[:, None] == classes[None]).astype(float)


def shap_importance(model, X, y):
    pre = model[:-1]
    clf = model.named_steps["clf"]
    Xs = pre.transform(X)
    if clf.__class__.__name__ == "RandomForestClassifier":
        sv = np.array(shap.TreeExplainer(clf).shap_values(Xs))
    else:
        bg = shap.kmeans(Xs, min(10, len(Xs)))
        sv = np.array(shap.KernelExplainer(probability_function(clf, Xs, y), bg).shap_values(Xs, nsamples=100, silent=True))
    n, p = X.shape
    if sv.ndim == 2:
        imp = np.abs(sv).mean(0)
    elif sv.shape[0] == n and sv.shape[1] == p:      # (samples, features, classes)
        imp = np.abs(sv).mean((0, 2))
    else:                                           # (classes, samples, features)
        imp = np.abs(sv).mean((0, 1))
    s = pd.Series(imp, index=X.columns).sort_values(ascending=False)
    contrib = s.groupby(lambda c: sensor_of(c)).sum()
    return s, contrib / contrib.sum()


# ------------------------------------------------------------------ 8.5 maps
def make_maps(df, fm, tag):
    plots = gpd.read_file(C.PLOTS_FILE)
    C.MAPS.mkdir(parents=True, exist_ok=True)
    out = []
    for date, d in df.groupby("date"):
        pred = pd.DataFrame(dict(plot_id=d.plot_id.values, pred_class=fm["model"].predict(d[fm["ofc"]]),
                                 true_class=d[TARGET].values))
        pred["zone"] = pred.pred_class.map(ZONE)
        g = plots.merge(pred, on="plot_id")
        g["date"] = date
        out.append(g)
        fig, axes = plt.subplots(1, 2, figsize=(13, 4.5))
        g.plot(ax=axes[0], color=[CLASS_COLOUR[c] for c in g.pred_class], edgecolor="k", lw=0.5)
        axes[0].legend(handles=[Patch(color=CLASS_COLOUR[k], label=f"{k} {n}") for k, n in enumerate(C.CLASS_NAMES)],
                       fontsize=7, loc="upper left", bbox_to_anchor=(1, 1))
        axes[0].set_title(f"Predicted severity class, {date}")
        g.plot(ax=axes[1], color=[ZONE_COLOUR[z] for z in g.zone], edgecolor="k", lw=0.5)
        axes[1].legend(handles=[Patch(color=c, label=z) for z, c in ZONE_COLOUR.items()],
                       fontsize=8, loc="upper left", bbox_to_anchor=(1, 1))
        axes[1].set_title("Spray decision: Green skip / Amber spray / Red too late")
        for ax in axes:
            for _, r in g.iterrows():
                ax.annotate(str(r.plot_id), r.geometry.centroid.coords[0], ha="center", va="center", fontsize=6)
            ax.set_axis_off()
        fig.tight_layout(); fig.savefig(C.MAPS / f"{tag}_{date}_maps.png", dpi=150); plt.close(fig)
    allg = pd.concat(out)
    gpd.GeoDataFrame(allg, crs=plots.crs).to_file(C.MAPS / f"{tag}_predictions.gpkg", layer="predictions")
    return allg


# ------------------------------------------------------------------ 8.6 regression of DI
def di_regression(df, cols, sensors, n_folds=None):
    preds = np.full(len(df), np.nan)
    g = df.plot_id.values
    for tr, te in GroupKFold(n_splits=n_folds or C.OUTER_FOLDS).split(df, df.DI, g):
        train = df.iloc[tr]
        feats = []
        for s in sensors:
            feats += dsf_for_sensor(train, [c for c in cols if sensor_of(c) == s], s)[0]
        rf = RandomForestRegressor(300, random_state=C.RANDOM_STATE, n_jobs=-1)
        rf.fit(train[feats].fillna(train[feats].median()), train.DI)
        preds[te] = rf.predict(df.iloc[te][feats].fillna(train[feats].median()))
    rmse = mean_squared_error(df.DI, preds) ** 0.5
    return dict(R2=float(r2_score(df.DI, preds)), RMSE=float(rmse), RE_pct=float(100 * rmse / df.DI.mean())), preds


# ------------------------------------------------------------------ driver
def run_modelling():
    C.MODELS.mkdir(parents=True, exist_ok=True)
    df, cols = load_table(C.SENSORS)
    print(f"{len(df)} plot-date observations, {df.plot_id.nunique()} plots, {len(cols)} features")
    configs = {**SINGLE, **FUSION}
    preds, picks = run_nested(df, cols, configs)
    preds.to_csv(C.MODELS / "outer_cv_predictions.csv", index=False)
    picks.to_csv(C.MODELS / "selected_features_per_fold.csv", index=False)
    summary = summarize(preds)
    summary.to_csv(C.MODELS / "performance_summary.csv", index=False)
    print(summary.round(3).to_string(index=False))

    gain = fusion_gain(summary, preds)
    gain.to_csv(C.MODELS / "fusion_gain.csv", index=False)
    print(gain.round(3).to_string(index=False))

    best = summary.iloc[0]
    cm, rep = class_report(preds, best.config, best.clf)
    pd.DataFrame(cm).to_csv(C.MODELS / "best_confusion_matrix.csv")
    rep.to_csv(C.MODELS / "best_class_report.csv", index=False)
    robust = robust_features(picks, best.config)
    robust.to_csv(C.MODELS / f"robust_features_{best.config}.csv", index=False)

    sensors = configs[best.config]
    fm = final_model(df, cols, sensors, best.clf)
    pd.Series(fm["ofc"]).to_csv(C.MODELS / "final_OFC.csv", index=False, header=["feature"])
    print(f"Final model: {best.config} / {best.clf}; OFC = {fm['ofc']}; params = {fm['params']}")
    imp, contrib = shap_importance(fm["model"], df[fm["ofc"]], df[TARGET].values)
    imp.to_csv(C.MODELS / "shap_feature_importance.csv", header=["mean_abs_shap"])
    contrib.to_csv(C.MODELS / "shap_sensor_contribution.csv", header=["share"])
    print("Sensor contribution (SHAP):", contrib.round(2).to_dict())

    make_maps(df, fm, f"{best.config}_{best.clf}")
    reg, _ = di_regression(df, cols, sensors)
    pd.Series(reg).to_csv(C.MODELS / "di_regression.csv", header=["value"])
    print("DI regression:", {k: round(v, 3) for k, v in reg.items()})


# ================================================================================================
# OPTIONAL - SYNTHETIC TEST DATA
# ================================================================================================
# Create a small synthetic dataset with the same structure as the real one
# (48 plots, 4 dates, MS / HS / RGB / TIR orthomosaics, ground truth, weather),
# so that every step of the pipeline can be tested before real data are ready.
# The spectra are simplified; results on these data say nothing about real accuracy.
import numpy as np
import pandas as pd
import geopandas as gpd
from rasterio.features import rasterize
from rasterio.transform import from_origin
from scipy.ndimage import gaussian_filter

SYN_RNG = np.random.default_rng(1)
FINE = 0.02                                   # m, base grid
MARGIN = 2.0
X0, Y0 = C.FIELD_ORIGIN_E - MARGIN, C.FIELD_ORIGIN_N + MARGIN
SYN_W, SYN_H = int((C.FIELD_WIDTH_M + 2 * MARGIN) / FINE), int((C.FIELD_LENGTH_M + 2 * MARGIN) / FINE)
FACTORS = {"RGB": 1, "MS": 2, "TIR": 4, "HS": 10}     # 2 cm, 4 cm, 8 cm, 20 cm
WL = np.arange(400, 2501, 15.0)
AIR = {d: t for d, t in zip(C.DATES, [20.0, 22.5, 19.0, 24.0])}


def spectra():
    wl = WL
    soil = 0.10 + 0.18 * (wl - 400) / 2100
    def veg(s):
        vis = 0.04 + 0.05 * np.exp(-((wl - 550) / 30) ** 2) - 0.015 * np.exp(-((wl - 670) / 25) ** 2)
        vis += s * (0.05 * np.exp(-((wl - 600) / 60) ** 2))                      # chlorosis
        edge = 1 / (1 + np.exp(-(wl - (715 - 12 * s)) / 12))
        nir = (0.48 * (1 - 0.3 * s)) * edge
        water = 1 - (0.06 * np.exp(-((wl - 970) / 25) ** 2) + 0.1 * np.exp(-((wl - 1200) / 40) ** 2)
                     + 0.6 * np.exp(-((wl - 1450) / 60) ** 2) + 0.7 * np.exp(-((wl - 1940) / 70) ** 2)) * (1 - 0.3 * s)
        swir = np.where(wl > 1300, (0.35 - 0.12 * (wl - 1300) / 1200) + 0.08 * s, 1)
        return (vis * (1 - edge) + nir * np.where(wl > 1300, swir / 0.48, 1)) * water
    return soil, veg(0.0), veg(1.0), np.full_like(wl, 0.55)


def block_mean(a, f):
    h, w = a.shape[0] // f * f, a.shape[1] // f * f
    return a[:h, :w].reshape(h // f, f, w // f, f).mean((1, 3))


def make_synthetic():
    for d in [C.ROOT]:
        d.mkdir(parents=True, exist_ok=True)
    layout = build_layout_table()
    layout.to_csv(C.LAYOUT_CSV, index=False)
    plots = build_plot_polygons(layout)
    plots.set_geometry("geometry").drop(columns="geometry_inner").to_file(C.PLOTS_FILE, layer="plots")

    sus = {"V1": 1.4, "V2": 1.0, "V3": 0.7}
    age = {"D1": 1.2, "D2": 1.0, "D3": 0.8, "D4": 0.6}
    tf = [0.25, 0.55, 0.85, 1.15]
    gt = []
    for _, p in layout.iterrows():
        base = SYN_RNG.lognormal(0, 0.35)
        for t, date in zip(tf, C.DATES):
            di = 0.0 if not p.inoculated else float(np.clip(32 * sus[p.variety] * age[p.inoc_age] * t * base, 0.5, 95))
            gt.append(dict(plot_id=p.plot_id, date=date, DI=round(di, 1)))
    gt = pd.DataFrame(gt)
    gt.to_csv(C.GROUND_TRUTH_CSV, index=False)
    pd.DataFrame(dict(date=C.DATES, air_temp_C=[AIR[d] for d in C.DATES])).to_csv(C.WEATHER_CSV, index=False)
    np.savetxt(C.HS_WAVELENGTH_FILE, WL, fmt="%.1f")

    tr = from_origin(X0, Y0, FINE, FINE)
    pid = rasterize([(g, int(i)) for g, i in zip(plots.geometry, plots.plot_id)], (SYN_H, SYN_W), transform=tr, dtype="int32")
    soil, healthy, diseased, white = spectra()
    for date in C.DATES:
        di_map = dict(zip(gt[gt.date == date].plot_id, gt[gt.date == date].DI))
        s_fine = np.vectorize(lambda i: min(di_map.get(i, 0) / 50, 1.0))(pid) * (pid > 0)
        noise = gaussian_filter(SYN_RNG.standard_normal((SYN_H, SYN_W)), 6)
        veg = (pid > 0) & (noise > np.quantile(noise, 0.2) + 0.25 * s_fine * noise.std())
        pust = veg & (SYN_RNG.random((SYN_H, SYN_W)) < 0.25 * s_fine)
        for sensor, f in FACTORS.items():
            fv, fp, s = block_mean(veg.astype(float), f), block_mean(pust.astype(float), f), block_mean(s_fine, f)
            h, w = fv.shape
            prof = dict(driver="GTiff", height=h, width=w, crs=C.CRS, transform=from_origin(X0, Y0, FINE * f, FINE * f))
            spec = ((fv - fp)[None] * healthy[:, None, None] + ((fv - fp) * s)[None] * (diseased - healthy)[:, None, None]
                    + fp[None] * white[:, None, None] + (1 - fv)[None] * soil[:, None, None])
            if sensor == "HS":
                cube = spec + SYN_RNG.normal(0, 0.004, spec.shape)
                write_raster(C.raw_path("HS", date), np.clip(cube, 0, 1) * 10000, prof, dtype="uint16", nodata=0)
            elif sensor == "MS":
                idx = [int(np.argmin(np.abs(WL - c))) for c in C.MS_BANDS.values()]
                write_raster(C.raw_path("MS", date), spec[idx] + SYN_RNG.normal(0, 0.005, (5, h, w)), prof)
            elif sensor == "RGB":
                idx = [int(np.argmin(np.abs(WL - c))) for c in (640, 550, 470)]
                rgb = np.clip(spec[idx] / 0.6 * 255 + SYN_RNG.normal(0, 4, (3, h, w)), 0, 255)
                write_raster(C.raw_path("RGB", date), rgb, prof, dtype="uint8", nodata=None)
            else:
                at = AIR[date]
                t_c = fv * (at - 3 + 4 * s) + (1 - fv) * (at + 9) + SYN_RNG.normal(0, 0.3, (h, w))
                shifted = prof.copy()
                shifted["transform"] = from_origin(X0 + 0.24, Y0, FINE * f, FINE * f)   # 24 cm registration error
                write_raster(C.raw_path("TIR", date), t_c + 273.15, shifted)
        print(f"synthetic {date}: written")


# ================================================================================================
# RUN
# ================================================================================================
def step1():
    layout = build_layout_table()
    for msg in check_layout(layout):
        print("LAYOUT CHECK:", msg)
    C.ROOT.mkdir(parents=True, exist_ok=True)
    layout.to_csv(C.LAYOUT_CSV, index=False)
    if not C.PLOTS_FILE.exists():
        build_plot_polygons(layout).drop(columns="geometry_inner").to_file(C.PLOTS_FILE, layer="plots")
    if C.GROUND_TRUTH_CSV.exists():
        print(load_ground_truth(layout).groupby(["date", "severity_class"]).size().unstack(fill_value=0))


STEPS = {
    1: ("Field layout and plot polygons", step1),
    2: ("Pre-processing and co-registration", preprocess_all),
    3: ("Vegetation masking", lambda: [mask_date(d) for d in C.DATES]),
    4: ("Endmember extraction and unmixing", lambda: run_unmixing("HS")),
    5: ("Plot-wise feature extraction", lambda: [extract(s) for s in C.SENSORS]),
    6: ("Phase 1 DSF selection (full data, for reporting)",
        lambda: [select_dsf(*load_table([s]), out_prefix=s) for s in C.SENSORS]),
    7: ("Phases 2-3: nested CV, fusion, final model, SHAP, maps, regression", run_modelling),
}


if __name__ == "__main__":
    args = sys.argv[1:]
    if "--fast" in args:
        FAST = True
        args.remove("--fast")
    if args == ["synthetic"]:
        make_synthetic()
    else:
        todo = list(STEPS) if args in ([], ["all"]) else [int(a) for a in args]
        for k in todo:
            name, fn = STEPS[k]
            print(f"\n===== Step {k}: {name} =====")
            fn()
