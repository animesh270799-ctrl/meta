"""Step A–E for the 2025-26 ASD leaf data: treatments from the field layout, labels, folds, smoothing, derivatives, 5-nm bands,
red-edge parameters and vegetation indices. Leaf level, all dates, stages, varieties and leaf positions pooled."""
import numpy as np, pandas as pd, os, json
from scipy.signal import savgol_filter
D = os.path.dirname(os.path.abspath(__file__)) + '/data/'
wl0 = np.load(D + 'wl.npy'); X0 = np.load(D + 'X_leaf.npy').astype(float); M = pd.read_csv(D + 'meta_raw.csv')

# ---- treatments (plot plan of the field layout: healthy block 1-12, R3 13-24, R2 25-36, R1 37-48) ----
LAY = {4: 'D3V1', 5: 'D1V2', 12: 'D4V1', 3: 'D1V3', 6: 'D4V3', 11: 'D3V2', 2: 'D2V2', 7: 'D1V1', 10: 'D3V3', 1: 'D4V2', 8: 'D2V3', 9: 'D2V1',
       13: 'D1V2', 20: 'D4V3', 21: 'D3V3', 14: 'D4V1', 19: 'D2V2', 22: 'D2V1', 15: 'D3V1', 18: 'D4V2', 23: 'D1V3', 16: 'D2V3', 17: 'D3V2', 24: 'D1V1',
       28: 'D4V1', 29: 'D3V3', 36: 'D3V1', 27: 'D2V3', 30: 'D1V2', 35: 'D2V2', 26: 'D4V2', 31: 'D2V1', 34: 'D1V1', 25: 'D1V3', 32: 'D3V2', 33: 'D4V3',
       37: 'D3V1', 44: 'D3V2', 45: 'D4V2', 38: 'D1V3', 43: 'D2V1', 46: 'D4V3', 39: 'D2V2', 42: 'D1V2', 47: 'D4V1', 40: 'D2V3', 41: 'D1V1', 48: 'D3V3'}
blk = lambda p: 'C' if p <= 12 else ('R3' if p <= 24 else ('R2' if p <= 36 else 'R1'))
M['block'] = M['plot'].map(blk); M['timing'] = M['plot'].map(lambda p: LAY[p][:2]); M['lay_var'] = M['plot'].map(lambda p: LAY[p][2:])
assert (M.lay_var == M.variety).all(), 'variety mismatch with layout'
M['unsprayed'] = (M.block != 'C').astype(int)          # natural infection: R1-R3 unsprayed, block C fungicide-sprayed (healthy)
M['grade'] = M.score.astype(int); M['diseased'] = (M.grade > 0).astype(int)
SOW = {'D1': '2025-12-09', 'D2': '2025-12-18', 'D3': '2025-12-27', 'D4': '2026-01-09'}   # D1-D4 = 50, 40, 30, 20 DAS treatments (user)
M['sowing'] = M.timing.map(SOW); M['DAS'] = (pd.to_datetime(M.date) - pd.to_datetime(M.sowing)).dt.days   # crop age at sampling
M['stage_code'] = M.stage.map({'Vegetative': 1, 'Flowering': 2, 'Pod formation': 3})
# ---- outer split: grouped, stratified hold-out of whole plots (split_lib.py; fold 0 = test plots, fold 1 = training plots) ----
import split_cfg as SC, split_lib as SL
TEST, sinfo = SL.best_split(M, SC.TEST_FRAC, seed=SC.SEED)
M['fold'] = np.where(M['plot'].isin(TEST), 0, 1)
SP, sdesc = SL.describe(M, TEST); SP.to_csv(D + 'split_plots.csv', index=False)
json.dump(dict(tag=SC.TAG, label=SC.LABEL, test_fraction_target=SC.TEST_FRAC, seed=SC.SEED, **sdesc, **sinfo,
               test_healthy_plots=[int(p) for p in TEST if p <= 12], test_unsprayed_plots=[int(p) for p in TEST if p > 12]), open(D + 'split.json', 'w'), indent=1)
print('split', SC.LABEL, sdesc)

# ---- pre-processing: 400-2400 nm (detector-edge noise trimmed), water bands kept, Savitzky-Golay 11 nm / order 2 ----
keep = (wl0 >= 400) & (wl0 <= 2400); wl = wl0[keep]
R1 = savgol_filter(X0, 11, 2, axis=1)[:, keep]; FD1 = savgol_filter(X0, 11, 2, deriv=1, axis=1)[:, keep]
w5 = np.arange(400, 2401, 5); i5 = np.searchsorted(wl, w5)
R5 = R1[:, i5]; FD5 = FD1[:, i5]
ix = lambda w: int(round(w - 400))
r = lambda w: R1[:, ix(w)]
nd = lambda a, b: (r(a) - r(b)) / (r(a) + r(b))
I = {}
I['NDVI'] = nd(800, 670); I['NDVI850'] = nd(850, 650); I['SR'] = r(800) / r(680); I['RVI'] = r(800) / r(670); I['GNDVI'] = nd(850, 550)
I['RDVI'] = (r(800) - r(670)) / np.sqrt(r(800) + r(670)); I['MSR'] = (r(800) / r(670) - 1) / np.sqrt(r(800) / r(670) + 1)
I['OSAVI'] = 1.16 * (r(800) - r(670)) / (r(800) + r(670) + 0.16)
I['TVI'] = 0.5 * (120 * (r(750) - r(550)) - 200 * (r(670) - r(550))); I['MTVI2'] = 1.5 * (1.2 * (r(800) - r(550)) - 2.5 * (r(670) - r(550))) / np.sqrt((2 * r(800) + 1) ** 2 - (6 * r(800) - 5 * np.sqrt(r(670))) - 0.5)
I['MCARI'] = ((r(700) - r(670)) - 0.2 * (r(700) - r(550))) * (r(700) / r(670)); I['TCARI'] = 3 * ((r(700) - r(670)) - 0.2 * (r(700) - r(550)) * (r(700) / r(670)))
I['VIgreen'] = nd(550, 670); I['GI'] = r(554) / r(677)
I['CIrededge'] = r(790) / r(720) - 1; I['CIgreen'] = r(790) / r(550) - 1; I['NDRE'] = nd(790, 720); I['MTCI'] = (r(754) - r(709)) / (r(709) - r(681))
I['PSSRa'] = r(800) / r(680); I['PSSRb'] = r(800) / r(635); I['PSSRc'] = r(800) / r(470)
I['SIPI'] = (r(800) - r(445)) / (r(800) - r(680)); I['NPCI'] = nd(680, 430); I['PSRI'] = (r(680) - r(500)) / r(750)
I['ARI'] = 1 / r(550) - 1 / r(700); I['PRI'] = nd(531, 570); I['NPQI'] = nd(415, 435); I['RVSI'] = (r(712) + r(752)) / 2 - r(732)
I['HI'] = nd(534, 698) - 0.5 * r(704)
I['WI'] = r(900) / r(970); I['WBI'] = r(970) / r(900); I['NDWI'] = nd(860, 1240); I['MoistSI'] = r(1600) / r(820); I['NDII'] = nd(819, 1649)
I['DWSI-1'] = r(800) / r(1660); I['DWSI-2'] = r(1660) / r(550); I['DWSI-3'] = r(1660) / r(680); I['DWSI-4'] = r(550) / r(680); I['DWSI-5'] = (r(800) + r(550)) / (r(1660) + r(680))
I['RBI'] = r(1148) / r(1301); I['NDBI'] = nd(1148, 1301)
F = pd.DataFrame(I)
re = slice(ix(680), ix(760) + 1); fdre = FD1[:, re]
F['REP'] = 680 + fdre.argmax(1).astype(float); F['Dr'] = fdre.max(1) * 1000; F['REarea'] = fdre.sum(1)
assert np.isfinite(F.values).all()
REF = {'NDVI': 'Rouse et al. (1974)', 'NDVI850': 'Raun et al. (2001)', 'SR': 'Jordan (1969)', 'RVI': 'Jordan (1969)', 'GNDVI': 'Gitelson et al. (1996)', 'RDVI': 'Roujean and Bréon (1995)',
       'MSR': 'Chen (1996)', 'OSAVI': 'Rondeaux et al. (1996)', 'TVI': 'Broge and Leblanc (2001)', 'MTVI2': 'Haboudane et al. (2004)', 'MCARI': 'Daughtry et al. (2000)', 'TCARI': 'Haboudane et al. (2002)',
       'VIgreen': 'Gitelson et al. (2002)', 'GI': 'Guo et al. (2021)', 'CIrededge': 'Gitelson et al. (2003)', 'CIgreen': 'Gitelson et al. (2003)', 'NDRE': 'Gitelson and Merzlyak (1994)', 'MTCI': 'Dash and Curran (2004)',
       'PSSRa': 'Blackburn (1998)', 'PSSRb': 'Blackburn (1998)', 'PSSRc': 'Blackburn (1998)', 'SIPI': 'Peñuelas et al. (1995)', 'NPCI': 'Peñuelas et al. (1994)', 'PSRI': 'Merzlyak et al. (1999)',
       'ARI': 'Gitelson et al. (2001)', 'PRI': 'Gamon et al. (1992)', 'NPQI': 'Barnes et al. (1992)', 'RVSI': 'Merton and Huntington (1999)', 'HI': 'Mahlein et al. (2013)', 'WI': 'Peñuelas et al. (1997)',
       'WBI': 'Peñuelas et al. (1997)', 'NDWI': 'Gao (1996)', 'MoistSI': 'Hunt and Rock (1989)', 'NDII': 'Hardisky et al. (1983)', 'DWSI-1': 'Apan et al. (2004)', 'DWSI-2': 'Apan et al. (2004)',
       'DWSI-3': 'Apan et al. (2004)', 'DWSI-4': 'Apan et al. (2004)', 'DWSI-5': 'Apan et al. (2004)', 'RBI': 'Mandal et al. (2023)', 'NDBI': 'Mandal et al. (2023)',
       'REP': 'Filella and Peñuelas (1994)', 'Dr': 'Filella and Peñuelas (1994)', 'REarea': 'Filella and Peñuelas (1994)'}
np.savez_compressed(D + 'prep.npz', wl=wl, w5=w5, R1=R1.astype(np.float32), FD1=FD1.astype(np.float32), R5=R5, FD5=FD5)
M.to_csv(D + 'meta.csv', index=False); F.to_csv(D + 'indices.csv', index=False); json.dump(REF, open(D + 'index_refs.json', 'w'), indent=1)
print('leaves', len(M), 'bands 1 nm', R1.shape[1], '5 nm', len(w5), 'indices', F.shape[1])
print(pd.crosstab(M.fold, M.grade)); print(pd.crosstab(M.block, M.status)); print(pd.crosstab(M.unsprayed, M.grade)); print(M.DAS.value_counts().sort_index())
