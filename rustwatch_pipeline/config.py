"""Step 0 - Project configuration. Edit this file only; every other module reads from it."""
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
