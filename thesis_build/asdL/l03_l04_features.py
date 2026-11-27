"""STEP L3 - pre-processing: Savitzky-Golay (11, 2) on 350-2500 nm, trim to 400-2400 nm (water bands kept), first derivative (same filter),
5-nm band means for the band searches.  STEP L4 - the 48 published indices (39 base + 9 SWIR) and REP, Dr, SDr at 1 nm."""
import os, numpy as np, pandas as pd
from scipy.signal import savgol_filter
import configL as C
X = np.load(os.path.join(C.OUT, 'L1_X.npy')); wl = np.load(os.path.join(C.OUT, 'L1_wl.npy'))
R = savgol_filter(X, C.SG_W, C.SG_O, axis=1); FD = savgol_filter(X, C.SG_W, C.SG_O, deriv=1, axis=1)
keep = (wl >= C.WMIN) & (wl <= C.WMAX); w1 = wl[keep]; R1, FD1 = R[:, keep], FD[:, keep]
w5 = np.arange(C.WMIN, C.WMAX + 1, C.STEP); idx = [np.where((w1 >= w - 2) & (w1 <= w + 2))[0] for w in w5]
R5 = np.stack([R1[:, i].mean(1) for i in idx], 1); FD5 = np.stack([FD1[:, i].mean(1) for i in idx], 1)
np.savez_compressed(os.path.join(C.OUT, 'L3_spectra.npz'), w1=w1, R1=R1.astype(np.float32), FD1=FD1.astype(np.float32), w5=w5, R5=R5, FD5=FD5)
res = X[:, keep] - R1; print('L3: SG residual SD %.5f; 1-nm bands %d; 5-nm bands %d' % (res.std(), len(w1), len(w5)))
pd.DataFrame([dict(item='raw bands', value='%d (350-2500 nm)' % X.shape[1]), dict(item='after trimming', value='%d (400-2400 nm, water bands kept)' % len(w1)),
              dict(item='5-nm bands', value='%d reflectance + %d first-derivative' % (len(w5), len(w5))), dict(item='Savitzky-Golay', value='window 11 nm, order 2; derivative with the same filter'),
              dict(item='residual SD (raw - smoothed)', value='%.5f reflectance' % res.std())]).to_csv(os.path.join(C.OUT, 'L3_summary.csv'), index=False)
r = lambda w: R1[:, int(round(w - 400))]; nd = lambda a, b: (r(a) - r(b)) / (r(a) + r(b)); I = {}
I['NDVI780'] = nd(780, 670); I['NDVI850'] = nd(850, 650); I['NDVI761'] = nd(761, 651); I['SR900'] = r(900) / r(680); I['SR850'] = r(850) / r(680); I['SR761'] = r(761) / r(651)
I['GNDVI'] = nd(850, 550); I['RDVI'] = (r(800) - r(670)) / np.sqrt(r(800) + r(670)); I['MSR'] = (r(800) / r(670) - 1) / np.sqrt(r(800) / r(670) + 1)
I['TVI'] = 0.5 * (120 * (r(750) - r(550)) - 200 * (r(670) - r(550))); I['MTVI1'] = 1.2 * (1.2 * (r(800) - r(550)) - 2.5 * (r(670) - r(550)))
I['MTVI2'] = 1.5 * (1.2 * (r(800) - r(550)) - 2.5 * (r(670) - r(550))) / np.sqrt((2 * r(800) + 1) ** 2 - (6 * r(800) - 5 * np.sqrt(r(670))) - 0.5)
I['MCARI1'] = 1.2 * (2.5 * (r(800) - r(670)) - 1.3 * (r(800) - r(550))); I['TCARI'] = 3 * ((r(700) - r(670)) - 0.2 * (r(700) - r(550)) * (r(700) / r(670)))
I['VIgreen'] = nd(550, 670); I['GI'] = r(554) / r(677); I['RR'] = 1 / r(700)
I['PSSRa'] = r(800) / r(680); I['PSSRb'] = r(800) / r(635); I['PSSRc'] = r(800) / r(470); I['RARSa'] = r(675) / r(700); I['RARSb'] = r(675) / (r(700) * r(650)); I['RARSc'] = r(760) / r(500)
I['SIPI'] = (r(800) - r(445)) / (r(800) - r(680)); I['NPCI'] = nd(680, 430); I['PSRI'] = (r(680) - r(500)) / r(750); I['ARI'] = 1 / r(550) - 1 / r(700); I['PPR'] = nd(550, 450); I['NRI'] = nd(570, 670)
I['PRI'] = nd(531, 570); I['NPQI'] = nd(415, 435); I['RVSI'] = (r(712) + r(752)) / 2 - r(732); I['HI'] = nd(534, 698) - 0.5 * r(704)
I['WI'] = r(900) / r(970); I['WI/NDVI'] = (r(900) / r(970)) / nd(900, 680); I['NWI-2'] = nd(970, 850)
I['DWSI-1'] = r(800) / r(1660); I['DWSI-4'] = r(550) / r(680); I['ROTI'] = r(1175) / (r(1982) + r(691))
I['DWSI-2'] = r(1660) / r(550); I['DWSI-3'] = r(1660) / r(680); I['DWSI-5'] = (r(800) + r(550)) / (r(1660) + r(680)); I['NDWI'] = nd(860, 1240); I['MSI'] = r(1600) / r(820)
I['NDII'] = nd(819, 1649); I['RBI_M'] = r(1148) / r(1301); I['NDBI'] = nd(1148, 1301); I['RBI_R'] = nd(1068, 1560)
F = pd.DataFrame(I); fdre = FD1[:, int(680 - 400):int(760 - 400) + 1]
F['REP'] = 680 + fdre.argmax(1).astype(float); F['Dr'] = fdre.max(1); F['SDr'] = fdre.sum(1)
assert F.shape[1] == 51 and np.isfinite(F.values).all(), (F.shape, F.columns[~np.isfinite(F.values).all(0)])
F.to_csv(os.path.join(C.OUT, 'L4_indices.csv'), index=False); print('L4: %d features (48 indices + REP, Dr, SDr); all finite' % F.shape[1])
