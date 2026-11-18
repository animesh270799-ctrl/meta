"""Full-range White Rust Index (400-2400 nm, water bands kept: contact-probe spectra) and comparison with the VNIR and SWIR WRIs.
Same search rules as Tier 3 (Mahlein et al., 2013): ND(l1, l2) + w * R(l3), 6 nm bands, ND bands >= 50 nm apart,
ReliefF top 25% bands and NDs (healthy vs diseased), threshold from training data, 8-fold plot-grouped CV.
Added: nested leave-one-replication-out (LORO) search, so the index formula itself is chosen without the test replication."""
import numpy as np, pandas as pd, json, os, time, sys
from scipy import stats
from scipy.signal import savgol_filter
from sklearn.model_selection import StratifiedGroupKFold
from sklearn.metrics import roc_auc_score
from joblib import Parallel, delayed
import lib
D = os.path.dirname(os.path.abspath(__file__)) + '/data/'
M = pd.read_csv(D + 'meta_leaf2.csv'); P = pd.read_csv(D + 'plot_table.csv'); X = np.load(D + 'X_leaf.npy')
idx = lambda w: int(round(w - 350)); G6 = [0, 1, 3, 5, 7, 9]
# ---- splice correction: shift the whole SWIR part (1001-2500 nm) by the 1000 nm step (Hueni and Bialek, 2017) ----
# raw data show no step at 1800 nm (mean 0.0000), so one shift of 1001-2500 nm keeps SWIR1 and SWIR2 continuous
i0 = idx(1000); step = X[:, i0 + 1] - (2 * X[:, i0] - X[:, i0 - 1]); Xc = X.copy(); Xc[:, i0 + 1:] -= step[:, None]
R1 = savgol_filter(Xc, 11, 2, axis=1).astype(np.float32)
gi = M.pd.map({k: i for i, k in enumerate(P.pd)}).values; Rp1 = np.vstack([R1[gi == i].mean(0) for i in range(len(P))])
y = M.grade.values; yb = M.diseased.values; grp = M['plot'].values; fold = M.fold.values; pdi = P.PDI.values; pfold = P.fold.values

RANGES = {'VNIR': list(range(450, 951, 6)),
          'SWIR': [w for w in range(1000, 2401, 6) if not (1350 <= w <= 1450 or 1800 <= w <= 1950)],
          'SWIR-W': list(range(1000, 2401, 6)),
          'FULL': list(range(400, 2401, 6))}

def ba_screen(V, yb):
    o = np.argsort(V, axis=1); ys = yb[o]; P1 = yb.sum(); N0 = len(yb) - P1
    ba = 0.5 * ((P1 - np.cumsum(ys, 1)) / P1 + np.cumsum(1 - ys, 1) / N0)
    return np.maximum(ba, 1 - ba).max(1)

def fit_thr(v, yt):
    """threshold and direction maximising balanced accuracy on training values"""
    o = np.argsort(v); vs, ys = v[o], yt[o]; P1 = ys.sum(); N0 = len(ys) - P1
    ba = 0.5 * ((P1 - np.cumsum(ys)) / P1 + np.cumsum(1 - ys) / N0); j1, j2 = ba.argmax(), (1 - ba).argmax()
    return (vs[j1], 1) if ba[j1] >= 1 - ba[j2] else (vs[j2], -1)

def bacc(pred, yt):
    return 0.5 * (((pred == 1) & (yt == 1)).sum() / max((yt == 1).sum(), 1) + ((pred == 0) & (yt == 0)).sum() / max((yt == 0).sum(), 1))

def value(Rm, d):
    r = lambda w: Rm[:, idx(w)].astype(float); v = (r(d['l1']) - r(d['l2'])) / (r(d['l1']) + r(d['l2']))
    return v + (d['w'] * r(d['l3']) if d['l3'] is not None else 0)

def search(bands, rows, label):
    Rb = R1[np.ix_(rows, [idx(w) for w in bands])]; ybt = yb[rows]; gt = grp[rows]
    pairs = [(a, b) for a in range(len(bands)) for b in range(a + 1, len(bands)) if bands[b] - bands[a] >= 50]
    A = np.array([p[0] for p in pairs]); B = np.array([p[1] for p in pairs])
    NDm = ((Rb[:, A] - Rb[:, B]) / (Rb[:, A] + Rb[:, B])).astype(np.float32)
    Wb = lib.relieff(Rb, ybt, gt, k=10); Wnd = lib.relieff(Rb, ybt, gt, k=10, Xdist=Rb, Xupd=NDm)
    nb_top = np.argsort(Wb)[::-1][:int(round(0.25 * len(bands)))]; nd_top = np.argsort(Wnd)[::-1][:int(round(0.25 * len(pairs)))]
    cands = [(q, None, 0.0) for q in nd_top] + [(q, c, w) for q in nd_top for c in nb_top for w in (-1, -0.5, 0.5, 1)]
    best = np.zeros(len(cands), np.float32)
    for s in range(0, len(cands), 2000):
        ch = cands[s:s + 2000]
        V = np.vstack([NDm[:, q] + (w * Rb[:, c] if c is not None else 0) for q, c, w in ch])
        best[s:s + len(ch)] = ba_screen(V, ybt)
    nd_only = np.array([c[1] is None for c in cands])
    top = list(np.argsort(best)[::-1][:30]) + list(np.where(nd_only)[0][np.argsort(best[nd_only])[::-1][:10]])
    cv = StratifiedGroupKFold(8, shuffle=True, random_state=1); out = []
    for k in dict.fromkeys(top):
        q, c, w = cands[k]; a, b = pairs[q]
        d = dict(l1=int(bands[a]), l2=int(bands[b]), l3=(int(bands[c]) if c is not None else None), w=float(w), ba_screen=float(best[k]))
        v = value(R1[rows], d); bas = []
        for tr, te in cv.split(v, ybt, gt):
            th, sg = fit_thr(v[tr], ybt[tr]); bas.append(bacc((sg * (v[te] - th) > 0).astype(int), ybt[te]))
        d.update(ba_cv=float(np.mean(bas)), ba_cv_sd=float(np.std(bas))); out.append(d)
    out = sorted(out, key=lambda d: -d['ba_cv'])
    print(label, 'bands', len(bands), 'pairs', len(pairs), 'candidates', len(cands), 'best', out[0], flush=True)
    return dict(label=label, n_bands=len(bands), n_pairs=len(pairs), n_cand=len(cands), top=out,
                best_nd=[d for d in out if d['l3'] is None][0], Wb=Wb.tolist(), bands=bands, nb_top=[int(bands[q]) for q in nb_top])

def wform(d):
    s = 'ND(%d, %d)' % (d['l1'], d['l2'])
    if d['l3'] is not None: s += ' %s%g R%d' % ('+' if d['w'] > 0 else '−', abs(d['w']), d['l3'])
    return s

if __name__ == '__main__':
    t0 = time.time(); allrows = np.arange(len(M))
    if '--compare' in sys.argv:          # reuse saved searches, recompute the comparison only
        prev = json.load(open(D + 'wri_full.json')); S = prev['searches']; S['FULL all']['Wb'] = prev['wb_full']
    else:
        jobs = [(r, allrows, r + ' all') for r in RANGES] + [(r, np.where(fold != f)[0], '%s fold%d' % (r, f)) for r in RANGES for f in range(3)]
        res = Parallel(n_jobs=3, verbose=0)(delayed(search)(RANGES[r], rows, lab) for r, rows, lab in jobs)
        S = {lab: v for (r, rows, lab), v in zip(jobs, res)}
    print('searches done %.0fs' % (time.time() - t0), flush=True)
    # all indices re-derived on the same (corrected) spectra with the same rules
    IDX = {'WRI-VNIR (450–950 nm)': S['VNIR all']['top'][0], 'WRI-SWIR (1000–2400 nm, water bands removed)': S['SWIR all']['top'][0],
           'WRI-SWIR-W (1000–2400 nm, water bands kept)': S['SWIR-W all']['top'][0], 'WRI-FULL (400–2400 nm)': S['FULL all']['top'][0],
           'ND-FULL (best two-band, 400–2400 nm)': S['FULL all']['best_nd']}
    NDVI = lambda Rm: (Rm[:, idx(800)] - Rm[:, idx(670)]) / (Rm[:, idx(800)] + Rm[:, idx(670)])
    NDWI = lambda Rm: (Rm[:, idx(860)] - Rm[:, idx(1240)]) / (Rm[:, idx(860)] + Rm[:, idx(1240)])
    VAL = {k: (value(R1, d), value(Rp1, d)) for k, d in IDX.items()}
    VAL['NDVI (Rouse et al., 1974)'] = (NDVI(R1).astype(float), NDVI(Rp1)); VAL['NDWI (Gao, 1996)'] = (NDWI(R1).astype(float), NDWI(Rp1))
    cv = StratifiedGroupKFold(8, shuffle=True, random_state=1); rows = []; leafv = {}; plotv = {}; letters = {}
    for k, (v, vp) in VAL.items():
        bas = []
        for tr, te in cv.split(v, yb, grp):
            th, sg = fit_thr(v[tr], yb[tr]); bas.append(bacc((sg * (v[te] - th) > 0).astype(int), yb[te]))
        auc = roc_auc_score(yb, v); auc = max(auc, 1 - auc)
        m01 = np.isin(y, [0, 1]); a01 = roc_auc_score((y[m01] == 1).astype(int), v[m01]); a01 = max(a01, 1 - a01)
        F_, p_ = stats.f_oneway(*[v[y == g] for g in G6]); ss_b = sum((y == g).sum() * (v[y == g].mean() - v.mean()) ** 2 for g in G6)
        eta = ss_b / ((v - v.mean()) ** 2).sum()
        letters[k] = lib.tukey_letters(pd.DataFrame({'v': v, 'grade': y.astype(str)}), 'v', 'grade', [str(g) for g in G6])
        rows.append(dict(Index=k, Formula=(wform(IDX[k]) if k in IDX else ('ND(800, 670)' if 'NDVI' in k else 'ND(860, 1240)')),
                         BA_CV=np.mean(bas), BA_CV_SD=np.std(bas), AUC=auc, AUC_0v1=a01, F=F_, eta2=eta,
                         rho_grade=stats.spearmanr(v, y)[0], r_PDI=np.corrcoef(vp, pdi)[0, 1]))
        leafv[k] = v; plotv[k] = vp
    C = pd.DataFrame(rows)
    # nested LORO: formula chosen on two replications (+ their controls), threshold fitted there, tested on the third
    NL = []
    for r in RANGES:
        for f in range(3):
            d = S['%s fold%d' % (r, f)]['top'][0]; tr, te = np.where(fold != f)[0], np.where(fold == f)[0]
            v = value(R1, d); th, sg = fit_thr(v[tr], yb[tr]); vp = value(Rp1, d)
            NL.append(dict(Range=r, fold=f, test_rep='R%d' % (f + 1), formula=wform(d), ba_test=bacc((sg * (v[te] - th) > 0).astype(int), yb[te]),
                           r_PDI_test=np.corrcoef(vp[pfold == f], pdi[pfold == f])[0, 1]))
    NL = pd.DataFrame(NL)
    out = dict(searches={k: {kk: vv for kk, vv in v.items() if kk not in ('Wb',)} for k, v in S.items()},
               wb_full=S['FULL all']['Wb'], bands_full=S['FULL all']['bands'], indices={k: (wform(d), d) for k, d in IDX.items()},
               comparison=C.to_dict('records'), nested=NL.to_dict('records'),
               grade_means={k: [float(leafv[k][y == g].mean()) for g in G6] for k in leafv}, letters=letters, splice_mean=float(step.mean()))
    json.dump(out, open(D + 'wri_full.json', 'w'), indent=1, default=float)
    np.savez_compressed(D + 'wri_full_vals.npz', **{'leaf_%d' % i: leafv[k] for i, k in enumerate(leafv)}, **{'plot_%d' % i: plotv[k] for i, k in enumerate(plotv)})
    pd.set_option('display.width', 250); print(C.round(3).to_string()); print(NL.round(3).to_string())
    print('done %.0fs' % (time.time() - t0))
