"""Stage 2: Objective 1 tiers on leaf ASD data (Tier 2 band selection, Tier 3 WRI, Tier 4 ANOVA, Tier 5 VIF + CDA, Tier 6 Boruta)."""
import numpy as np, pandas as pd, json, os, time
from scipy import stats
from sklearn.model_selection import StratifiedGroupKFold
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis as LDA
from sklearn.metrics import accuracy_score, f1_score
import lib
D = os.path.dirname(os.path.abspath(__file__)) + '/data/'
Z = np.load(D + 'prep.npz'); M = pd.read_csv(D + 'meta_leaf2.csv'); P = pd.read_csv(D + 'plot_table.csv')
F = pd.read_csv(D + 'feat_leaf.csv'); Fp = pd.read_csv(D + 'feat_plot.csv')
wl = Z['b5']; Bl = {t: Z[t] for t in ('R', 'FD', 'SD')}; Bp = {t: Z[t + 'p'] for t in ('R', 'FD', 'SD')}
y = M.grade.values; grp = M['plot'].values; pdi = P.PDI.values
R1 = Z['R1nm'].astype(float); Rp1 = Z['Rp1nm'].astype(float); idx = lambda w: int(round(w - 350))
RES = {}; T = {}
t0 = time.time()

# ================= Tier 2: correlation scalogram + ReliefF =================
S = lib.select_bands(Bl, Bp, wl, y, grp, pdi)
print('Tier 2 done %.0fs' % (time.time() - t0), 'robust', S['robust'], 'reg-only', S['regonly'], 'cls-only', S['clsonly'])
sc = S['sc']; W = S['W']; nb = len(wl)
T['scalogram'] = pd.DataFrame({'wavelength_nm': wl, 'r_R': sc['R'][0], 'p_R': sc['R'][1], 'r_FD': sc['FD'][0], 'p_FD': sc['FD'][1], 'r_SD': sc['SD'][0], 'p_SD': sc['SD'][1]})
T['relieff'] = pd.DataFrame({'wavelength_nm': wl, 'W_R': W[:nb], 'W_FD': W[nb:2 * nb], 'W_SD': W[2 * nb:]})
T['regions_R'] = pd.DataFrame({'wavelength_nm': wl, 'region_R': S['reg']['R'], 'region_FD': S['reg']['FD'], 'region_SD': S['reg']['SD']})
rows = []
for lab, L in (('Scalogram (PDI)', S['S1']), ('ReliefF (grades)', S['R1'])):
    for t, j, s in L: rows.append([lab, t, int(wl[j]), S['reg'][t][j], round(float(s), 4)])
T['band_candidates'] = pd.DataFrame(rows, columns=['List', 'Spectrum', 'Wavelength_nm', 'Region_id', 'Score (|r| or ReliefF weight)'])
fl = lambda L: ['%s%d' % (t, w) for t, w in L]
RES['tier2'] = dict(n_regions={t: int(S['reg'][t].max() + 1) for t in S['reg']}, n_scal_cand=len(S['scand']), n_rel_cand=len(S['rcand']),
                   n_scal_reg=len(S['S1']), n_rel_reg=len(S['R1']), robust=fl(S['robust']), regonly=fl(S['regonly']), clsonly=fl(S['clsonly']),
                   max_r={t: [float(np.abs(sc[t][0]).max()), int(wl[np.abs(sc[t][0]).argmax()])] for t in sc},
                   top_relief=[['%s%d' % S['feat'][q], float(W[q])] for q in np.argsort(W)[::-1][:10]])
C = np.corrcoef(Bl['R'].T); RES['tier2']['median_adjacent_r'] = float(np.median(np.diag(C, 1)))
def bandval(B, L):
    return pd.DataFrame({'%s%d' % (t, w): B[t][:, list(wl).index(w)] for t, w in L})
cls_bands = S['robust'] + S['clsonly']; reg_bands = S['robust'] + S['regonly']

# ================= Tier 3: White Rust Index search (Mahlein et al., 2013) =================
yb = M.diseased.values
def ba_screen(V, yb):
    """in-sample best balanced accuracy over all thresholds for each row of V (both directions)"""
    o = np.argsort(V, axis=1); ys = yb[o]; P1 = yb.sum(); N0 = len(yb) - P1
    tp_below = np.cumsum(ys, 1); fn = tp_below; tn = np.cumsum(1 - ys, 1)
    ba = 0.5 * ((P1 - fn) / P1 + tn / N0)             # rule: diseased if value > threshold
    return np.maximum(ba, 1 - ba).max(1)
def wri_search(bands, label):
    Rb = R1[:, [idx(w) for w in bands]]
    pairs = [(a, b) for a in range(len(bands)) for b in range(a + 1, len(bands)) if bands[b] - bands[a] >= 50]
    NDm = np.column_stack([(Rb[:, a] - Rb[:, b]) / (Rb[:, a] + Rb[:, b]) for a, b in pairs])
    # ReliefF (healthy vs diseased): neighbours in band space, weights for bands and for normalised differences
    Wb = lib.relieff(Rb, yb, grp, k=10); Wnd = lib.relieff(Rb, yb, grp, k=10, Xdist=Rb, Xupd=NDm)
    nb_top = np.argsort(Wb)[::-1][:int(round(0.25 * len(bands)))]; nd_top = np.argsort(Wnd)[::-1][:int(round(0.25 * len(pairs)))]
    cands = [(q, None, 0.0) for q in nd_top] + [(q, c, w) for q in nd_top for c in nb_top for w in (-1, -0.5, 0.5, 1)]
    best = np.zeros(len(cands))
    for s in range(0, len(cands), 2000):
        ch = cands[s:s + 2000]
        V = np.vstack([NDm[:, q] + (w * Rb[:, c] if c is not None else 0) for q, c, w in ch])
        best[s:s + len(ch)] = ba_screen(V, yb)
    top = np.argsort(best)[::-1][:30]
    cv = StratifiedGroupKFold(8, shuffle=True, random_state=1); out = []
    for k in top:
        q, c, w = cands[k]; v = NDm[:, q] + (w * Rb[:, c] if c is not None else 0); bas = []
        for tr, te in cv.split(v, yb, grp):
            # threshold and direction from training data
            o = np.argsort(v[tr]); vs, ys = v[tr][o], yb[tr][o]; P1 = ys.sum(); N0 = len(ys) - P1
            ba = 0.5 * ((P1 - np.cumsum(ys)) / P1 + np.cumsum(1 - ys) / N0); j1, j2 = ba.argmax(), (1 - ba).argmax()
            if ba[j1] >= 1 - ba[j2]: th, sgn = vs[j1], 1
            else: th, sgn = vs[j2], -1
            pred = (sgn * (v[te] - th) > 0).astype(int)
            bas.append(0.5 * (((pred == 1) & (yb[te] == 1)).sum() / max((yb[te] == 1).sum(), 1) + ((pred == 0) & (yb[te] == 0)).sum() / max((yb[te] == 0).sum(), 1)))
        a, b = pairs[q]
        out.append(dict(l1=int(bands[a]), l2=int(bands[b]), l3=(int(bands[c]) if c is not None else None), w=w, ba_screen=float(best[k]), ba_cv=float(np.mean(bas)), ba_cv_sd=float(np.std(bas))))
    out = sorted(out, key=lambda d: -d['ba_cv'])
    print(label, 'pairs', len(pairs), 'candidates', len(cands), 'best', out[0])
    return dict(n_bands=len(bands), n_pairs=len(pairs), n_cand=len(cands), top=out, Wb=Wb, bands=bands, nb_top=[int(bands[q]) for q in nb_top])
vn = list(range(450, 951, 6)); sw = [w for w in range(1000, 2401, 6) if not (1350 <= w <= 1450 or 1800 <= w <= 1950)]
WV = wri_search(vn, 'VNIR'); WS = wri_search(sw, 'SWIR')
print('Tier 3 done %.0fs' % (time.time() - t0))
def wri_val(Rm, d):
    r = lambda w: Rm[:, idx(w)]; v = (r(d['l1']) - r(d['l2'])) / (r(d['l1']) + r(d['l2']))
    return v + (d['w'] * r(d['l3']) if d['l3'] else 0)
wbest = WV['top'][0] if WV['top'][0]['ba_cv'] >= WS['top'][0]['ba_cv'] else WS['top'][0]
F['WRI'] = wri_val(R1, wbest); Fp['WRI'] = wri_val(Rp1, wbest)
F['WRI_VNIR'] = wri_val(R1, WV['top'][0]); F['WRI_SWIR'] = wri_val(R1, WS['top'][0])
Fp['WRI_VNIR'] = wri_val(Rp1, WV['top'][0]); Fp['WRI_SWIR'] = wri_val(Rp1, WS['top'][0])
wform = lambda d: 'ND(%d, %d)%s' % (d['l1'], d['l2'], (' %+g R%d' % (d['w'], d['l3'])) if d['l3'] else '')
RES['tier3'] = dict(vnir=dict(n_bands=WV['n_bands'], n_pairs=WV['n_pairs'], n_cand=WV['n_cand'], best=WV['top'][0], formula=wform(WV['top'][0]), top_bands=WV['nb_top']),
                    swir=dict(n_bands=WS['n_bands'], n_pairs=WS['n_pairs'], n_cand=WS['n_cand'], best=WS['top'][0], formula=wform(WS['top'][0]), top_bands=WS['nb_top']),
                    chosen='VNIR' if wbest is WV['top'][0] else 'SWIR', formula=wform(wbest),
                    r_pdi=float(stats.pearsonr(Fp.WRI, pdi)[0]), grade_means={int(g): float(F.WRI[y == g].mean()) for g in np.unique(y)})
for nm, W_ in (('wri_vnir_top', WV), ('wri_swir_top', WS)):
    T[nm] = pd.DataFrame([[wform(d), d['ba_screen'], d['ba_cv'], d['ba_cv_sd']] for d in W_['top'][:15]], columns=['Candidate index', 'Balanced accuracy (all data)', 'Balanced accuracy (8-fold CV)', 'CV SD'])
T['wri_relief_vnir'] = pd.DataFrame({'wavelength_nm': WV['bands'], 'ReliefF_weight': WV['Wb']})

# ================= Tier 4: univariate response (ANOVA + Tukey; Pearson r with PDI) =================
featnames = list(F.columns[:51]) + ['WRI_VNIR', 'WRI_SWIR']
Fr = pd.concat([F[featnames], bandval(Bl, S['robust'])], axis=1); Frp = pd.concat([Fp[featnames], bandval(Bp, S['robust'])], axis=1)
rows = []
for c in Fr.columns:
    groups = [Fr[c].values[y == g] for g in np.unique(y)]; Fv, pv = stats.f_oneway(*groups)
    ss_b = sum(len(gq) * (gq.mean() - Fr[c].mean()) ** 2 for gq in groups); ss_t = ((Fr[c] - Fr[c].mean()) ** 2).sum()
    rp, pp = stats.pearsonr(Frp[c], pdi); rl = stats.spearmanr(Fr[c], y)[0]
    rows.append([c, Fv, pv, ss_b / ss_t, rp, pp, rl] + [Fr[c].values[y == g].mean() for g in np.unique(y)])
A = pd.DataFrame(rows, columns=['Feature', 'F', 'p', 'eta2', 'r_PDI_plot', 'p_r', 'rho_score_leaf'] + ['mean_g%d' % g for g in np.unique(y)]).sort_values('F', ascending=False)
import re as _re
SW9 = json.load(open(D + 'prep_info.json'))['swir9']
A['Group'] = A.Feature.map(lambda c: 'Band' if _re.match(r'^(R|FD|SD)\d+$', c) else ('SWIR index' if c in SW9 else ('WRI' if c.startswith('WRI') else ('Red edge' if c in ('REP', 'Dr', 'SDr') else 'Index'))))
T['anova'] = A
key = list(A.Feature[:8]); dfl = Fr.assign(grade=y.astype(str))
RES['tier4'] = dict(n_sig=int((A.p < 0.001).sum()), n_feat=len(A), top=A.head(12)[['Feature', 'F', 'eta2', 'r_PDI_plot']].round(3).values.tolist(),
                    letters={c: lib.tukey_letters(dfl, c, 'grade', [str(g) for g in np.unique(y)]) for c in key},
                    swir=A[A.Group == 'SWIR index'][['Feature', 'F', 'r_PDI_plot']].round(3).values.tolist())
print('Tier 4 done %.0fs' % (time.time() - t0))

# ================= Tier 5: VIF + two-step stepwise CDA (Bhattacharya and Chattopadhyay, 2013) =================
def cda_step(Xdf, label):
    log = []; keep = lib.vif_filter(Xdf, 10, log); sel, steps = lib.stepwise_cda(Xdf[keep], y)
    can = lib.canonical(Xdf[sel], y)
    accs = []; pred = np.zeros(len(y), int)
    for f in range(3):
        tr, te = M.fold.values != f, M.fold.values == f
        m = LDA(priors=np.ones(6) / 6).fit(Xdf[sel].values[tr], y[tr]); pred[te] = m.predict(Xdf[sel].values[te])
    acc = accuracy_score(y, pred); mf1 = f1_score(y, pred, average='macro'); adj = np.mean(np.abs(np.searchsorted([0, 1, 3, 5, 7, 9], pred) - np.searchsorted([0, 1, 3, 5, 7, 9], y)) <= 1)
    print(label, 'VIF kept', len(keep), 'of', Xdf.shape[1], 'selected', sel, 'cancor', can['cancor'][:3].round(3), 'acc %.2f' % acc)
    return dict(n_in=Xdf.shape[1], n_vif=len(keep), vif_removed=[l[1] for l in log if l[2] >= 10], selected=sel, steps=steps, cancor=can['cancor'].tolist(), share=can['share'].tolist(),
                wilks=float(can['wilks']), std_coef=can['std_coef'][:, :2].tolist(), struct=can['struct'][:, :2].tolist(), centroids=can['centroids'][:, :2].tolist(),
                acc=float(acc), macro_f1=float(mf1), adj=float(adj)), can['scores'][:, :2]
cda1, sc1 = cda_step(bandval(Bl, cls_bands), 'CDA step 1 (bands)')
cda2, sc2 = cda_step(F[list(F.columns[:51]) + ['WRI_VNIR', 'WRI_SWIR']], 'CDA step 2 (indices + red edge + WRI)')
RES['tier5'] = dict(step1=cda1, step2=cda2)
np.savez(D + 'cda_scores.npz', s1=sc1, s2=sc2)
print('Tier 5 done %.0fs' % (time.time() - t0))

# ================= Tier 6: Boruta (Kursa and Rudnicki, 2010) =================
Xc = pd.concat([bandval(Bl, cls_bands), F[featnames]], axis=1); Xr = pd.concat([bandval(Bp, reg_bands), Fp[featnames]], axis=1)
bc = lib.boruta(Xc.values, y, 'c'); br = lib.boruta(Xr.values, pdi, 'r')
dec = lambda b, cols: pd.DataFrame({'Feature': cols, 'Decision': np.where(b.support_, 'Confirmed', np.where(b.support_weak_, 'Tentative', 'Rejected')), 'Rank': b.ranking_})
Tc, Tr = dec(bc, list(Xc.columns)), dec(br, list(Xr.columns))
# RF importance (mean decrease in impurity) on the full set, for plotting
from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor
Tc['Importance'] = RandomForestClassifier(500, n_jobs=-1, class_weight='balanced', random_state=0, max_depth=7).fit(Xc, y).feature_importances_
Tr['Importance'] = RandomForestRegressor(500, n_jobs=-1, random_state=0, max_depth=7).fit(Xr, pdi).feature_importances_
T['boruta_cls'] = Tc.sort_values('Importance', ascending=False); T['boruta_reg'] = Tr.sort_values('Importance', ascending=False)
RES['tier6'] = dict(cls=dict(n_in=len(Tc), confirmed=Tc[Tc.Decision == 'Confirmed'].sort_values('Importance', ascending=False).Feature.tolist(), tentative=Tc[Tc.Decision == 'Tentative'].Feature.tolist()),
                    reg=dict(n_in=len(Tr), confirmed=Tr[Tr.Decision == 'Confirmed'].sort_values('Importance', ascending=False).Feature.tolist(), tentative=Tr[Tr.Decision == 'Tentative'].Feature.tolist()))
print('Tier 6 done %.0fs' % (time.time() - t0), {k: len(v['confirmed']) for k, v in RES['tier6'].items()})

# ---- save ----
F.to_csv(D + 'feat_leaf_wri.csv', index=False); Fp.to_csv(D + 'feat_plot_wri.csv', index=False)
for k, v in T.items(): v.to_csv(D + 't_%s.csv' % k, index=False)
json.dump(dict(RES=RES, wri=dict(vnir=WV['top'][0], swir=WS['top'][0], chosen=wbest), cls_bands=cls_bands, reg_bands=reg_bands), open(D + 'res1.json', 'w'), indent=1, default=float)
print('saved; total %.0fs' % (time.time() - t0))
