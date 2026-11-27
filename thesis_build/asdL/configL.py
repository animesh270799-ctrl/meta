"""Settings of the Part L analysis (methodology 2026-27, Steps L1-L10) applied to the 2025-26 ASD leaf data, pooled over dates, growth stages,
varieties and leaf positions. Every value below is taken from the methodology document; deviations are marked DEV and explained in the report."""
import os
BASE = os.path.dirname(os.path.abspath(__file__)); OUT = os.path.join(BASE, 'out'); os.makedirs(OUT, exist_ok=True)
UP = '/root/.claude/uploads/c5704ca0-f1ca-5695-b9e0-a810fbe166a9/'
RAW_FILES = {'2026-02-11': 'eeec9a7f-asd__data_complete_labelled_110226_scored.xlsx', '2026-02-24': 'c6bc9195-asd__data_complete_labelled_240226_scored.xlsx',
             '2026-03-03': '3ecb31e0-asd__data_complete_labelled_030326_scored.xlsx', '2026-03-13': '6584ad8d-asd__data_complete_labelled_130326_scored.xlsx'}
WEATHER = '/home/user/meta/thesis_build/asd26/data/weather_season.csv'          # IARI observatory daily weather (from the user's weather file)
UAV_PLOT = '/home/user/meta/thesis_build/uavhs/data/envi_plot_avg.txt'           # UAV hyperspectral plot means, 24 Feb 2026 (Step L9)
LAYOUT = {4: 'D3V1', 5: 'D1V2', 12: 'D4V1', 3: 'D1V3', 6: 'D4V3', 11: 'D3V2', 2: 'D2V2', 7: 'D1V1', 10: 'D3V3', 1: 'D4V2', 8: 'D2V3', 9: 'D2V1',
          13: 'D1V2', 20: 'D4V3', 21: 'D3V3', 14: 'D4V1', 19: 'D2V2', 22: 'D2V1', 15: 'D3V1', 18: 'D4V2', 23: 'D1V3', 16: 'D2V3', 17: 'D3V2', 24: 'D1V1',
          28: 'D4V1', 29: 'D3V3', 36: 'D3V1', 27: 'D2V3', 30: 'D1V2', 35: 'D2V2', 26: 'D4V2', 31: 'D2V1', 34: 'D1V1', 25: 'D1V3', 32: 'D3V2', 33: 'D4V3',
          37: 'D3V1', 44: 'D3V2', 45: 'D4V2', 38: 'D1V3', 43: 'D2V1', 46: 'D4V3', 39: 'D2V2', 42: 'D1V2', 47: 'D4V1', 40: 'D2V3', 41: 'D1V1', 48: 'D3V3'}
BLOCK = lambda p: 'C' if p <= 12 else ('R3' if p <= 24 else ('R2' if p <= 36 else 'R1'))
SOWING = {'D1': '2025-12-09', 'D2': '2025-12-18', 'D3': '2025-12-27', 'D4': '2026-01-09'}
STAGE_CODE = {'Vegetative': 1, 'Flowering': 2, 'Pod formation': 3}
GRADES = [0, 1, 3, 5, 7, 9]; LEAVES = ['L3', 'L5', 'LL']
# L2 split (methodology Step D1/D2): same test plots and network validation plots as the 2026-27 plan (same plot plan)
TEST_PLOTS = [1, 4, 5, 8, 13, 14, 18, 25, 27, 31, 35, 37, 44, 46, 48]
VAL_PLOTS = [6, 7, 11, 19, 24, 26, 28, 30, 36, 39, 41]
SEED = 42; INNER = 3
# L1 outlier screening
IF_CONTAM = 'auto'
SPLICE_JOIN = 1000; SPLICE_GUARD = (995, 1005)          # DEV-1: first-derivative bands at the residual 1000-nm detector join excluded from band selection
# L3
SG_W, SG_O, WMIN, WMAX, STEP = 11, 2, 400, 2400, 5
# L5
R2_THR, TOP_FRAC, SHAP_FRAC, MCCV, MAX_PLS, CARS_IT = 0.5, 0.05, 0.40, 50, 15, 50
PAIR_SEP, WRI_SEP, WRI_PAIRS, WRI_STEP, WRI_W = 10, 50, 200, 10, (-1, -0.5, 0, 0.5, 1)
CORR_THR, RELIEF_K, N_TOP, VIF_THR = 0.95, 10, 5, 10.0
# L6
SFFS_MAX = 15
DL = dict(lr=6e-4, wd=1e-5, lr_min=1e-6, epochs=300, patience=60, min_delta=5e-5, batch=32, smooth=0.01, clip=1.2, drop=0.03)
