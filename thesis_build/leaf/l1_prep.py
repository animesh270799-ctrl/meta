"""Stage 1: pre-processing, Tier 1 features (bands, derivatives, red-edge, 48 indices), plot aggregation and LORO folds."""
import numpy as np, pandas as pd, os, json
from scipy.signal import savgol_filter
D = os.path.dirname(os.path.abspath(__file__)) + '/data/'
wl = np.load(D + 'wl.npy'); X = np.load(D + 'X_leaf.npy'); M = pd.read_csv(D + 'meta_leaf.csv')
idx = lambda w: int(round(w - 350))

# ---- 1. splice correction at the VNIR/SWIR1 detector join (1000/1001 nm) ----
i0 = idx(1000); step = X[:, i0 + 1] - (2 * X[:, i0] - X[:, i0 - 1])
Xc = X.copy(); Xc[:, i0 + 1:idx(1800) + 1] -= step[:, None]
# ---- 2. Savitzky-Golay smoothing and derivatives (window 11 nm, 2nd order) ----
R = savgol_filter(Xc, 11, 2, axis=1); FD = savgol_filter(Xc, 11, 2, deriv=1, axis=1); SD = savgol_filter(Xc, 11, 2, deriv=2, axis=1)
# ---- 3. retained 5 nm bands: 400-2400 nm without 1350-1450 and 1800-1950 nm ----
b5 = np.array([w for w in range(400, 2401, 5) if not (1350 <= w <= 1450 or 1800 <= w <= 1950)])
cols = [idx(w) for w in b5]
B = {'R': R[:, cols], 'FD': FD[:, cols] * 1000, 'SD': SD[:, cols] * 1e5}      # FD per 1000 nm, SD per 1e5 nm^2 (scaled for readability)
print('bands kept', len(b5), '-> band features', 3 * len(b5))

# ---- 4-5. red-edge parameters and vegetation indices (39 base + 9 SWIR) from smoothed 1 nm reflectance ----
re = slice(idx(680), idx(750) + 1)
def features(Rm, FDm):
    r = lambda w: Rm[:, idx(w)]
    nd = lambda a, b: (r(a) - r(b)) / (r(a) + r(b))
    I = {}
    I['NDVI780'] = nd(780, 670); I['NDVI850'] = nd(850, 650); I['NDVI761'] = nd(761, 651)
    I['SR900'] = r(900) / r(680); I['SR850'] = r(850) / r(680); I['SR761'] = r(761) / r(651)
    I['GNDVI'] = nd(850, 550); I['RDVI'] = (r(800) - r(670)) / np.sqrt(r(800) + r(670))
    I['MSR'] = (r(800) / r(670) - 1) / np.sqrt(r(800) / r(670) + 1)
    I['TVI'] = 0.5 * (120 * (r(750) - r(550)) - 200 * (r(670) - r(550)))
    I['MTVI1'] = 1.2 * (1.2 * (r(800) - r(550)) - 2.5 * (r(670) - r(550)))
    I['MTVI2'] = 1.5 * (1.2 * (r(800) - r(550)) - 2.5 * (r(670) - r(550))) / np.sqrt((2 * r(800) + 1) ** 2 - (6 * r(800) - 5 * np.sqrt(r(670))) - 0.5)
    I['MCARI1'] = 1.2 * (2.5 * (r(800) - r(670)) - 1.3 * (r(800) - r(550)))
    I['TCARI'] = 3 * ((r(700) - r(670)) - 0.2 * (r(700) - r(550)) * (r(700) / r(670)))
    I['VIgreen'] = nd(550, 670); I['GI'] = r(554) / r(677); I['RR'] = 1 / r(700)
    I['PSSRa'] = r(800) / r(680); I['PSSRb'] = r(800) / r(635); I['PSSRc'] = r(800) / r(470)
    I['RARSa'] = r(675) / r(700); I['RARSb'] = r(675) / (r(700) * r(650)); I['RARSc'] = r(760) / r(500)
    I['SIPI'] = (r(800) - r(445)) / (r(800) - r(680)); I['NPCI'] = nd(680, 430); I['PSRI'] = (r(680) - r(500)) / r(750)
    I['ARI'] = 1 / r(550) - 1 / r(700); I['PPR'] = nd(550, 450); I['NRI'] = nd(570, 670)
    I['PRI'] = nd(531, 570); I['NPQI'] = nd(415, 435); I['RVSI'] = (r(712) + r(752)) / 2 - r(732)
    I['HI'] = nd(534, 698) - 0.5 * r(704)
    I['WI'] = r(900) / r(970); I['WI/NDVI'] = I['WI'] / I['NDVI780']; I['NWI-2'] = nd(970, 850)
    I['DWSI-1'] = r(800) / r(1660); I['DWSI-4'] = r(550) / r(680); I['ROTI'] = r(1175) / (r(1982) + r(691))
    I['DWSI-2'] = r(1660) / r(550); I['DWSI-3'] = r(1660) / r(680); I['DWSI-5'] = (r(800) + r(550)) / (r(1660) + r(680))
    I['NDWI'] = nd(860, 1240); I['MSI'] = r(1600) / r(820); I['NDII'] = nd(819, 1649)
    I['RBI_M'] = r(1148) / r(1301); I['NDBI'] = nd(1148, 1301); I['RBI_R'] = nd(1068, 1560)
    Fm = pd.DataFrame(I); fdre = FDm[:, re]
    Fm['REP'] = 680 + fdre.argmax(1).astype(float); Fm['Dr'] = fdre.max(1) * 1000; Fm['SDr'] = fdre.sum(1)
    return Fm
F = features(R, FD)
base39 = list(F.columns[:39]); swir9 = list(F.columns[39:48])
assert np.isfinite(F.values).all() and F.shape[1] == 51

# ---- 6. folds: leave-one-replication-out; the 12 control plots are split by variety (V1->R1, V2->R2, V3->R3) ----
fold = M.rep.map({'R1': 0, 'R2': 1, 'R3': 2}).astype('float')
cmask = M.rep == 'C'; fold[cmask] = M.loc[cmask, 'variety'].map({'V1': 0, 'V2': 1, 'V3': 2})
M['fold'] = fold.astype(int); M['grade'] = M.score.astype(int); M['diseased'] = (M.grade > 0).astype(int)
M['pd'] = M.date + '_' + M['plot'].astype(str)

# ---- 7. plot-level table: mean spectrum of the leaves of each plot-date, PDI = sum(score)/(9 n) x 100 ----
g = M.groupby('pd', sort=False)
P = g.agg(date=('date', 'first'), plot=('plot', 'first'), variety=('variety', 'first'), rep=('rep', 'first'), inoc=('inoc', 'first'), stage=('stage', lambda s: s.mode()[0]),
          fold=('fold', 'first'), n_leaves=('grade', 'size'), sum_score=('grade', 'sum')).reset_index()
P['PDI'] = P.sum_score / (9 * P.n_leaves) * 100
order = {k: i for i, k in enumerate(P.pd)}; gi = M.pd.map(order).values
def pmean(A): return np.vstack([A[gi == i].mean(0) for i in range(len(P))])
Rp = pmean(R)                                        # plot-mean reflectance (1 nm)
# recompute derivatives, red edge and indices on the plot-mean reflectance (features of the plot spectrum)
FDp = savgol_filter(Rp, 11, 2, deriv=1, axis=1); SDp = savgol_filter(Rp, 11, 2, deriv=2, axis=1)
Bp = {'R': Rp[:, cols], 'FD': FDp[:, cols] * 1000, 'SD': SDp[:, cols] * 1e5}
Fp = features(Rp, FDp)

np.savez_compressed(D + 'prep.npz', b5=b5, R=B['R'], FD=B['FD'], SD=B['SD'], Rp=Bp['R'], FDp=Bp['FD'], SDp=Bp['SD'],
                    R1nm=R.astype(np.float32), Rp1nm=Rp.astype(np.float32), splice=step)
M.to_csv(D + 'meta_leaf2.csv', index=False); P.to_csv(D + 'plot_table.csv', index=False)
F.to_csv(D + 'feat_leaf.csv', index=False); Fp.to_csv(D + 'feat_plot.csv', index=False)
json.dump({'base39': base39, 'swir9': swir9, 'n_bands': len(b5), 'splice_mean': float(step.mean()), 'splice_sd': float(step.std())}, open(D + 'prep_info.json', 'w'))
print('leaves', len(M), 'plot-dates', len(P), 'PDI range %.1f-%.1f' % (P.PDI.min(), P.PDI.max()))
print(pd.crosstab(M.fold, M.grade)); print(P.groupby('fold').PDI.describe().round(1))
print('splice step mean %.4f sd %.4f' % (step.mean(), step.std()))
