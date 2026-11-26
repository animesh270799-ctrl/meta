"""ALL settings of the analysis in one place (methodology Appendix B).
Edit only the PATHS block when the files are on another computer (for Windows use r'C:\\...' paths)."""
import os
# ------------------------------------------------------------------ PATHS (edit these)
BASE = os.path.dirname(os.path.abspath(__file__))
RAW_DIR = os.environ.get('WR_RAW', os.path.join(BASE, 'raw'))          # folder with the four ASD Excel files and the weather file
RAW_FILES = {'2026-02-11': 'asd__data_complete_labelled_110226_scored.xlsx', '2026-02-24': 'asd__data_complete_labelled_240226_scored.xlsx',
             '2026-03-03': 'asd__data_complete_labelled_030326_scored.xlsx', '2026-03-13': 'asd__data_complete_labelled_130326_scored.xlsx'}
WEATHER_FILE = 'IARI_daily_weather_2025-26.csv'                        # columns: date,Tmax,Tmin,rain,wind,...,RH1,RH2,BSS,evap
OUT = os.environ.get('WR_OUT', os.path.join(BASE, 'out'))              # every script writes here; files are numbered by step
os.makedirs(OUT, exist_ok=True)
FAST = os.environ.get('WR_FAST') == '1'                                # quick test run with small settings (never for the thesis)

# ------------------------------------------------------------------ A. experiment
LAYOUT = {4: 'D3V1', 5: 'D1V2', 12: 'D4V1', 3: 'D1V3', 6: 'D4V3', 11: 'D3V2', 2: 'D2V2', 7: 'D1V1', 10: 'D3V3', 1: 'D4V2', 8: 'D2V3', 9: 'D2V1',
          13: 'D1V2', 20: 'D4V3', 21: 'D3V3', 14: 'D4V1', 19: 'D2V2', 22: 'D2V1', 15: 'D3V1', 18: 'D4V2', 23: 'D1V3', 16: 'D2V3', 17: 'D3V2', 24: 'D1V1',
          28: 'D4V1', 29: 'D3V3', 36: 'D3V1', 27: 'D2V3', 30: 'D1V2', 35: 'D2V2', 26: 'D4V2', 31: 'D2V1', 34: 'D1V1', 25: 'D1V3', 32: 'D3V2', 33: 'D4V3',
          37: 'D3V1', 44: 'D3V2', 45: 'D4V2', 38: 'D1V3', 43: 'D2V1', 46: 'D4V3', 39: 'D2V2', 42: 'D1V2', 47: 'D4V1', 40: 'D2V3', 41: 'D1V1', 48: 'D3V3'}
BLOCK = lambda p: 'C' if p <= 12 else ('R3' if p <= 24 else ('R2' if p <= 36 else 'R1'))   # C = fungicide-sprayed healthy block
SOWING = {'D1': '2025-12-09', 'D2': '2025-12-18', 'D3': '2025-12-27', 'D4': '2026-01-09'}
STAGE_CODE = {'Vegetative': 1, 'Flowering': 2, 'Pod formation': 3}
GRADES = [0, 1, 3, 5, 7, 9]
LEAF_POSITIONS = ['L3', 'L5', 'LL']

# ------------------------------------------------------------------ A5. quality control
SPLICE_JOINS = [1000, 1800]            # ASD detector joins (Hueni and Bialek, 2017): last band of the lower detector
SPLICE_MIN_STEP = 5e-4                 # correct a join only if its median excess jump is larger than this (reflectance units)
JOIN_ZONES = [(990, 1010), (1790, 1835)]   # excluded from band and wavelet candidates (Step C1)

# ------------------------------------------------------------------ B. split (fixed once; keep for every analysis)
TEST_FRAC, SEED_SPLIT, N_CAND = 0.30, 2026, 5000
TEST_PLOTS = [1, 4, 5, 8, 13, 14, 18, 25, 27, 31, 35, 37, 44, 46, 48]
LORO_TEST = {1: list(range(37, 49)) + [7, 2, 10, 12], 2: list(range(25, 37)) + [5, 8, 4, 1], 3: list(range(13, 25)) + [3, 9, 11, 6]}   # check of the design (H3)
SEED = 42
INNER_FOLDS = 3

# ------------------------------------------------------------------ C. pre-processing and features
SG_WINDOW, SG_ORDER = 11, 2
WL_MIN, WL_MAX, BAND_STEP = 400, 2400, 5
CR_FEATURES = {'CR550': (530, 760), 'CR1200': (1080, 1280), 'CR1450': (1300, 1650), 'CR1940': (1840, 2150)}   # 970-nm feature not used: it spans the 1000-nm join
CWT_SCALES = [2, 4, 8, 16, 32, 64]

# ------------------------------------------------------------------ D / E2. feature selection
R2_THR, TOP_FRAC = 0.5, 0.05
REDEDGE_FD = (680, 760)
SHAP_FRAC, XGB_SHAP = 0.40, dict(n_estimators=300, max_depth=4, learning_rate=0.05, subsample=0.8, colsample_bytree=0.8)
MCCV_SPLITS, MAX_PLS = (5 if FAST else 50), 15
CARS_RUNS, CARS_ITER, CARS_KEEP, MAX_OW = (2 if FAST else 20), (10 if FAST else 50), 0.5, 15
PAIR_MIN_SEP, WRI_MIN_SEP, WRI_TOP_PAIRS, WRI_STEP, WRI_WEIGHTS = 10, 50, 200, 10, (-1, -0.5, 0, 0.5, 1)
CORR_THR, RELIEF_K, N_TOP = 0.95, 10, 5
WAVELET_TOP, REGION_GAP = 0.05, 10
VIF_THR = 10.0

# ------------------------------------------------------------------ E. models
SFFS_MAX, SFFS_TOL = (5 if FAST else 15), 0.01
DL = dict(lr=6e-4, weight_decay=1e-5, lr_min=1e-6, epochs=(2 if FAST else 100), patience=(2 if FAST else 20), min_delta=5e-5, batch=32,
          label_smoothing=0.01, clip=1.2, drop=0.03)
NETS = ['DNN-F1', 'DT-EDNet', 'EfficientNet-B0', 'ResNet18', 'ConvNeXt V2-Atto']

# ------------------------------------------------------------------ F, G, H. evaluation
N_BOOT, N_BOOT_GAIN = (50 if FAST else 1000), (100 if FAST else 2000)
N_REPEAT_SPLITS, N_LEAF_SPLITS = (2 if FAST else 20), (1 if FAST else 5)
