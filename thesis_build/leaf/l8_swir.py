"""SWIR-only Tier 2: scalogram + ReliefF restricted to 1000-2400 nm, robust regions and their stability across folds and dates."""
import numpy as np, pandas as pd, json
from scipy import stats
import lib
D = 'data/'; Z = np.load(D + 'prep.npz'); M = pd.read_csv(D + 'meta_leaf2.csv'); P = pd.read_csv(D + 'plot_table.csv')
wl = Z['b5']; sw = (wl >= 1000)
W5 = wl[sw]; Bl = {t: Z[t][:, sw] for t in ('R', 'FD', 'SD')}; Bp = {t: Z[t + 'p'][:, sw] for t in ('R', 'FD', 'SD')}
y = M.grade.values; grp = M['plot'].values; pdi = P.PDI.values
S = lib.select_bands(Bl, Bp, W5, y, grp, pdi)
print('SWIR regions R/FD/SD:', {t: int(S['reg'][t].max() + 1) for t in S['reg']})
print('robust:', S['robust']); print('regression-only:', S['regonly']); print('classification-only:', S['clsonly'])
# region summary for reflectance: mean r with PDI and mean ReliefF weight per contiguous region
sc = S['sc']; nb = len(W5); Wt = {'R': S['W'][:nb], 'FD': S['W'][nb:2 * nb], 'SD': S['W'][2 * nb:]}
rows = []
for t in ('R', 'FD', 'SD'):
    r, p = sc[t]
    for j in np.argsort(-np.abs(r))[:8]: rows.append([t, int(W5[j]), round(float(r[j]), 3), round(float(Wt[t][j]), 4)])
print(pd.DataFrame(rows, columns=['type', 'nm', 'r_PDI', 'ReliefF']).to_string(index=False))
# stability: repeat in each LORO training fold
cnt = {}
for f in range(3):
    tr = M.fold.values != f; ptr = P.fold.values != f
    Sf = lib.select_bands({t: Bl[t][tr] for t in Bl}, {t: Bp[t][ptr] for t in Bp}, W5, y[tr], grp[tr], pdi[ptr])
    for lab, L in (('robust', Sf['robust']), ('reg', Sf['regonly']), ('cls', Sf['clsonly'])):
        for t, w in L: cnt.setdefault((t, w // 50 * 50), []).append((f, lab, w))
print('\nper-fold selections grouped in 50 nm windows:')
for k in sorted(cnt): print(k, cnt[k])
# per-date correlation of reflectance with plot PDI in candidate windows
for lo, hi in ((1450, 1500), (1500, 1650), (1650, 1800), (1950, 2100), (2100, 2250), (2250, 2400), (1000, 1100), (1100, 1300)):
    m = (W5 >= lo) & (W5 < hi); rr = []
    for d in sorted(P.date.unique()):
        q = P.date.values == d
        rr.append(np.nanmean([stats.pearsonr(Bp['R'][q][:, j], pdi[q])[0] for j in np.where(m)[0]]) if pdi[q].std() > 0 else np.nan)
    print('R %d-%d nm: r by date' % (lo, hi), np.round(rr, 2), ' pooled %.2f' % np.mean([sc['R'][0][j] for j in np.where(m)[0]]))
json.dump(dict(robust=S['robust'], regonly=S['regonly'], clsonly=S['clsonly'], top=rows, folds={'%s%d' % k: v for k, v in cnt.items()}), open(D + 'swir_tier2.json', 'w'), default=int)
