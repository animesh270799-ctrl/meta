"""Figures for the leaf-level ASD analysis (used in the Word report and the PPT)."""
import numpy as np, pandas as pd, json, os, sys, re
import matplotlib; matplotlib.use('Agg')
import matplotlib.pyplot as plt
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)) + '/../obj1')
from o1_flow import chart, COL, FILL
B = os.path.dirname(os.path.abspath(__file__)) + '/'; D = B + 'data/'; FG = B + 'fig/'
plt.rcParams.update({'font.family': 'DejaVu Sans', 'font.size': 9})
GL = ['0', '1', '3', '5', '7', '9']; GC = ['#2E7D32', '#9CCC65', '#FDD835', '#FB8C00', '#E53935', '#7B1FA2']; G6 = [0, 1, 3, 5, 7, 9]
Z = np.load(D + 'prep.npz'); M = pd.read_csv(D + 'meta_leaf2.csv'); P = pd.read_csv(D + 'plot_table.csv')
F = pd.read_csv(D + 'feat_leaf_wri.csv'); Fp = pd.read_csv(D + 'feat_plot_wri.csv')
R1 = json.load(open(D + 'res1.json')); RS = R1['RES']; y = M.grade.values; wl = Z['b5']
R2 = json.load(open(D + 'res2.json')) if os.path.exists(D + 'res2.json') else None
save = lambda n: (plt.tight_layout(), plt.savefig(FG + n, dpi=200), plt.close())

# ---------- flow chart ----------
COL['L'] = '#00695C'; FILL['L'] = '#E0F2F1'
chart('L', 'Leaf-level ASD analysis: methodology applied to the four sampling dates', [
 ('Tier 0  Data and labels', ['2339 leaf spectra (ASD, 350–2500 nm), 48 plots, 4 dates (11 Feb – 13 Mar 2026)', 'Leaf grade 0, 1, 3, 5, 7, 9 (classification); plot PDI = Σ score/(9n) × 100 (regression)', 'Leave-one-replication-out folds (R1, R2, R3; controls split by variety)'], 'Conn 1990', ['2339 leaves, 192 plot-dates', '3 LORO folds']),
 ('Pre-processing', ['Splice correction at 1000 nm; 400–2400 nm kept; 1350–1450 and 1800–1950 nm removed', 'Savitzky–Golay smoothing (11 nm, 2nd order); FD and SD; 5 nm bands (349)'], 'Savitzky 1964; Hueni 2017', ['349 bands × R, FD, SD']),
 ('Tier 1  Features', ['1047 band features; REP, Dr, SDr; 39 base + 9 SWIR indices', 'Leaf features from leaf spectra; plot features from plot-mean spectra'], 'Guo 2021; Apan 2004', ['1047 band + 51 features']),
 ('Tier 2  Scalogram + ReliefF', ['Scalogram: r of R/FD/SD with plot PDI (p < 0.01, top 5%)', 'ReliefF: six leaf grades, k = 10, same-plot neighbours excluded (top 5%)', 'One band per correlated region (r ≥ 0.95); common → robust'], 'Shukla 2024; Robnik-Šikonja 2003', ['Robust, regression and', 'classification band lists']),
 ('Tier 3  White Rust Index', ['VNIR 450–950 nm and SWIR 1000–2400 nm at 6 nm; ND + w·R', 'ReliefF top 25%; 8-fold plot-grouped CV; balanced accuracy'], 'Mahlein 2013', ['WRI formula and accuracy']),
 ('Tier 4  Univariate response', ['One-way ANOVA + Tukey HSD across six grades (leaves)', 'Pearson r with PDI (plots)'], 'Mahlein 2019', ['Responding features']),
 ('Tier 5  VIF + stepwise CDA', ['VIF < 10; step 1 bands, step 2 indices + red edge + WRI', 'Wilks lambda, canonical r, LORO accuracy'], 'Bhattacharya 2013', ['Separability of grades']),
 ('Tier 6  Boruta', ['Classification (leaves) and regression (plots)'], 'Kursa 2010', ['Two DSF pools']),
 ('Objective 2  Models (nested LORO)', ['Inside each training fold: Tier 2 → Boruta → VIF → ML-SFFS → tuning', 'SVM, RF, k-NN, MLP; SVR, RFR, k-NN, PLSR, MLP; baselines: PLS-DA/PLSR, RF all'], 'Tian 2021; Mustafa 2023', ['Accuracy of grades', 'and PDI']),
], 'l_flow.png', foot='Outputs: white-rust bands, WRI, responding indices, DSF pools, six-grade classifier and PDI model')
import shutil; shutil.move(B + '../obj1/fig/l_flow.png', FG + 'l_flow.png')

# ---------- spectra ----------
R1nm = Z['R1nm']; w1 = np.arange(350, 2501); keep = (w1 >= 400) & (w1 <= 2400) & ~((w1 >= 1350) & (w1 <= 1450)) & ~((w1 >= 1800) & (w1 <= 1950))
fig, ax = plt.subplots(1, 2, figsize=(12, 4))
for k, g in enumerate(G6):
    m = R1nm[y == g].mean(0).astype(float); m[~keep] = np.nan; ax[0].plot(w1, m, color=GC[k], lw=1.4, label='grade %d (n=%d)' % (g, (y == g).sum()))
    fd = np.gradient(R1nm[y == g].mean(0).astype(float)) * 1000; ax[1].plot(w1[(w1 >= 450) & (w1 <= 1000)], fd[(w1 >= 450) & (w1 <= 1000)], color=GC[k], lw=1.4, label='grade %d' % g)
ax[0].set_xlabel('Wavelength (nm)'); ax[0].set_ylabel('Reflectance'); ax[0].set_title('(a) Mean leaf reflectance by grade (water bands removed)'); ax[0].legend(fontsize=7, frameon=False)
ax[1].set_xlabel('Wavelength (nm)'); ax[1].set_ylabel('FD (×10⁻³ nm⁻¹)'); ax[1].set_title('(b) Mean first derivative, 450–1000 nm'); ax[1].legend(fontsize=7, frameon=False)
save('l_spectra.png')

# ---------- scalogram + ReliefF ----------
S = pd.read_csv(D + 't_scalogram.csv'); W = pd.read_csv(D + 't_relieff.csv'); cand = pd.read_csv(D + 't_band_candidates.csv')
fig, ax = plt.subplots(4, 1, figsize=(11, 10), sharex=True)
for a, t in zip(ax[:3], ('R', 'FD', 'SD')):
    r = S['r_' + t].values.copy(); w5 = S.wavelength_nm.values
    gaps = np.where(np.diff(w5) > 5)[0]
    for seg in np.split(np.arange(len(w5)), gaps + 1): a.plot(w5[seg], r[seg], color='#00695C', lw=1)
    c = cand[(cand.List.str.startswith('Scal')) & (cand.Spectrum == t)]
    a.scatter(c.Wavelength_nm, [r[list(w5).index(v)] for v in c.Wavelength_nm], color='#C62828', s=22, zorder=3, label='selected (one per region)')
    a.axhline(0, color='grey', lw=0.6); a.set_ylabel('r with PDI'); a.set_title('Correlation scalogram: %s vs plot PDI (n = 192)' % t, fontsize=9); a.legend(fontsize=7, frameon=False, loc='lower right')
for t, c in (('R', '#2E7D32'), ('FD', '#1565C0'), ('SD', '#AD1457')):
    v = W['W_' + t].values; w5 = W.wavelength_nm.values; gaps = np.where(np.diff(w5) > 5)[0]
    for i, seg in enumerate(np.split(np.arange(len(w5)), gaps + 1)): ax[3].plot(w5[seg], v[seg], color=c, lw=1, label=t if i == 0 else None)
cr = cand[cand.List.str.startswith('Relief')]
ax[3].scatter(cr.Wavelength_nm, cr['Score (|r| or ReliefF weight)'], color='#C62828', s=22, zorder=3, label='selected')
ax[3].set_ylabel('ReliefF weight'); ax[3].set_xlabel('Wavelength (nm)'); ax[3].set_title('ReliefF weights for six leaf grades (n = 2339; k = 10; same-plot neighbours excluded)', fontsize=9); ax[3].legend(fontsize=7, frameon=False, ncol=4)
save('l_scal_relief.png')

# ---------- band correlation (regions) ----------
C = np.corrcoef(Z['R'].T); reg = pd.read_csv(D + 't_regions_R.csv').region_R.values
fig, ax = plt.subplots(figsize=(6.2, 5.4)); im = ax.imshow(C, cmap='RdBu_r', vmin=-1, vmax=1)
for b in np.where(np.diff(reg) != 0)[0]: ax.axhline(b + 0.5, color='k', lw=0.4); ax.axvline(b + 0.5, color='k', lw=0.4)
tk = [i for i, w in enumerate(wl) if w in (400, 700, 1000, 1300, 1600, 2000, 2400)]
ax.set_xticks(tk, wl[tk]); ax.set_yticks(tk, wl[tk]); plt.colorbar(im, label='Pearson r')
ax.set_title('Band-to-band correlation of leaf reflectance (349 bands)\nlines: %d correlated regions (r ≥ 0.95)' % RS['tier2']['n_regions']['R'], fontsize=9)
save('l_regions.png')

# ---------- WRI ----------
wv = R1['wri']; ch = RS['tier3']['chosen']
fig, ax = plt.subplots(1, 3, figsize=(13, 3.8))
rv = pd.read_csv(D + 't_wri_relief_vnir.csv'); ax[0].plot(rv.wavelength_nm, rv.ReliefF_weight, color='#00695C'); ax[0].set_xlabel('Wavelength (nm)'); ax[0].set_ylabel('ReliefF weight'); ax[0].set_title('(a) ReliefF weights, healthy vs diseased (6 nm bands)', fontsize=9)
for a, col, lab in ((ax[1], 'WRI_VNIR', 'VNIR WRI: ' + RS['tier3']['vnir']['formula']), (ax[2], 'WRI_SWIR', 'SWIR WRI: ' + RS['tier3']['swir']['formula'])):
    bp = a.boxplot([F[col][y == g] for g in G6], tick_labels=GL, patch_artist=True, showfliers=False, medianprops=dict(color='k'))
    for b_, c in zip(bp['boxes'], GC): b_.set_facecolor(c)
    a.set_xlabel('Leaf grade'); a.set_title(lab, fontsize=8.5)
ax[1].set_ylabel('Index value'); save('l_wri.png')

# ---------- ANOVA boxplots ----------
A = pd.read_csv(D + 't_anova.csv'); key = list(RS['tier4']['letters'])[:6]
fig, ax = plt.subplots(2, 3, figsize=(12, 6.4))
Fr = F.copy()
for nm in key:
    if nm not in Fr: t_, w_ = re.match(r'^(R|FD|SD)(\d+)$', nm).groups(); Fr[nm] = Z[t_][:, list(wl).index(int(w_))]
for a, nm in zip(ax.flat, key):
    bp = a.boxplot([Fr[nm][y == g] for g in G6], tick_labels=GL, patch_artist=True, showfliers=False, medianprops=dict(color='k'))
    for b_, c in zip(bp['boxes'], GC): b_.set_facecolor(c)
    lt = RS['tier4']['letters'][nm]; top = max(np.percentile(Fr[nm][y == g], 75) + 1.5 * (np.percentile(Fr[nm][y == g], 75) - np.percentile(Fr[nm][y == g], 25)) for g in G6)
    lo, hi = a.get_ylim(); a.set_ylim(lo, hi + 0.12 * (hi - lo))
    for i, g in enumerate(GL): a.text(i + 1, hi + 0.04 * (hi - lo), lt[g], ha='center', fontsize=8, fontweight='bold')
    row = A[A.Feature == nm].iloc[0]; a.set_title('%s  (F = %.0f, η² = %.2f, r_PDI = %.2f)' % (nm, row.F, row.eta2, row.r_PDI_plot), fontsize=8.5); a.set_xlabel('Leaf grade')
save('l_anova.png')

# ---------- r with PDI (plot level) ----------
top_r = A[A.Group != 'Band'].assign(ar=lambda d: d.r_PDI_plot.abs()).sort_values('ar', ascending=False).Feature.tolist()[:4]
fig, ax = plt.subplots(1, 4, figsize=(13, 3.3))
for a, nm in zip(ax, top_r):
    a.scatter(Fp[nm], P.PDI, c=[{'2026-02-11': '#9CCC65', '2026-02-24': '#FDD835', '2026-03-03': '#FB8C00', '2026-03-13': '#C62828'}[d] for d in P.date], s=12)
    a.set_xlabel(nm); a.set_ylabel('PDI (%)'); a.set_title('r = %.2f' % np.corrcoef(Fp[nm], P.PDI)[0, 1], fontsize=9)
save('l_r_pdi.png')

# ---------- CDA score plots ----------
sc = np.load(D + 'cda_scores.npz')
fig, ax = plt.subplots(1, 2, figsize=(12, 4.6))
for a, s, st, lab in ((ax[0], sc['s1'], RS['tier5']['step1'], 'Step 1: bands'), (ax[1], sc['s2'], RS['tier5']['step2'], 'Step 2: indices + red edge + WRI')):
    for k, g in enumerate(G6): a.scatter(s[y == g, 0], s[y == g, 1], s=5, color=GC[k], alpha=0.45, label='grade %d' % g)
    for k, g in enumerate(G6): a.scatter(*s[y == g].mean(0), marker='X', s=120, color=GC[k], edgecolor='k', zorder=4)
    a.set_xlabel('Function 1 (%.0f%%)' % (100 * st['share'][0])); a.set_ylabel('Function 2 (%.0f%%)' % (100 * st['share'][1]))
    a.set_title('%s — %d variables; r₁ = %.2f; Wilks Λ = %.3f; LORO acc. = %.2f' % (lab, len(st['selected']), st['cancor'][0], st['wilks'], st['acc']), fontsize=8.5)
ax[0].legend(fontsize=7, frameon=False, markerscale=2); save('l_cda.png')

# ---------- Boruta ----------
fig, ax = plt.subplots(1, 2, figsize=(12, 6))
for a, nm, lab in ((ax[0], 'boruta_cls', 'Classification (six grades, leaves)'), (ax[1], 'boruta_reg', 'Regression (PDI, plots)')):
    T = pd.read_csv(D + 't_%s.csv' % nm).head(25)[::-1]
    a.barh(T.Feature, T.Importance, color=[{'Confirmed': '#2E7D32', 'Tentative': '#FBC02D', 'Rejected': '#C62828'}[d] for d in T.Decision])
    a.set_title('Boruta: %s\n(green confirmed, yellow tentative, red rejected; top 25 by RF importance)' % lab, fontsize=8.5); a.set_xlabel('RF importance'); a.tick_params(axis='y', labelsize=7)
save('l_boruta.png')

if R2:
    # ---------- model comparison ----------
    rc = R2['cls']; rr = R2['reg']
    fig, ax = plt.subplots(1, 2, figsize=(12.5, 4.2))
    ks = list(rc); v = [rc[k]['macro_f1'] for k in ks]; a2 = [rc[k]['adj'] for k in ks]
    xs = np.arange(len(ks)); ax[0].bar(xs - 0.2, v, 0.4, color='#00695C', label='macro-F1'); ax[0].bar(xs + 0.2, [rc[k]['oa'] for k in ks], 0.4, color='#80CBC4', label='overall accuracy')
    for i, q in enumerate(v): ax[0].text(i - 0.2, q + 0.01, '%.2f' % q, ha='center', fontsize=7)
    ax[0].set_xticks(xs, ks, rotation=25, ha='right', fontsize=7.5); ax[0].set_ylim(0, 1); ax[0].legend(frameon=False, fontsize=7.5); ax[0].set_title('(a) Six-grade leaf classification (nested LORO)', fontsize=9)
    ks = list(rr); v = [max(rr[k]['r2'], 0) for k in ks]
    ax[1].bar(range(len(ks)), v, color='#AD1457')
    for i, q in enumerate(v): ax[1].text(i, q + 0.01, '%.2f' % q, ha='center', fontsize=7)
    ax[1].set_xticks(range(len(ks)), ks, rotation=25, ha='right', fontsize=7.5); ax[1].set_ylim(0, 1); ax[1].set_ylabel('R²'); ax[1].set_title('(b) Plot PDI regression (nested LORO)', fontsize=9)
    save('l_models.png')
    # ---------- confusion matrix + obs/pred ----------
    bc, br = R2['best']['cls'], R2['best']['reg']; cm = np.array(rc[bc]['cm']); pr = pd.read_csv(D + 'pred_reg.csv')
    fig, ax = plt.subplots(1, 2, figsize=(12, 4.8))
    ax[0].imshow(cm, cmap='Greens')
    for i in range(6):
        for j in range(6): ax[0].text(j, i, cm[i, j], ha='center', va='center', color='white' if cm[i, j] > cm.max() / 2 else 'k', fontsize=9)
    ax[0].set_xticks(range(6), GL); ax[0].set_yticks(range(6), GL); ax[0].set_xlabel('Predicted grade'); ax[0].set_ylabel('Observed grade')
    ax[0].set_title('(a) %s: OA %.2f, kappa %.2f, macro-F1 %.2f, ±1 grade %.2f' % (bc, rc[bc]['oa'], rc[bc]['kappa'], rc[bc]['macro_f1'], rc[bc]['adj']), fontsize=8.5)
    bu = [k for k in rr if k.startswith('Bottom-up')][0]
    ax[1].scatter(pr.observed_PDI, pr['pred_' + br], s=14, color='#AD1457', label='%s (R² %.2f, RMSE %.1f)' % (br, rr[br]['r2'], rr[br]['rmse']))
    ax[1].scatter(pr.observed_PDI, pr['pred_' + bu], s=14, color='#00695C', marker='^', alpha=0.6, label='bottom-up from leaf grades (R² %.2f)' % rr[bu]['r2'])
    ax[1].plot([0, 80], [0, 80], 'k--', lw=0.8); ax[1].set_xlabel('Observed PDI (%)'); ax[1].set_ylabel('Predicted PDI (%)'); ax[1].legend(fontsize=7.5, frameon=False); ax[1].set_title('(b) Plot PDI: observed vs predicted (held-out replications)', fontsize=8.5)
    save('l_eval.png')
    # ---------- SFFS curves (fold 1) ----------
    fig, ax = plt.subplots(1, 2, figsize=(11, 3.8))
    for name, c in zip(['SVM', 'RF', 'k-NN'], ['#00695C', '#2E7D32', '#C98A00']):
        cu = R2['folds'][0]['ofc'][name]['curve']; ks_ = sorted(int(k) for k in cu); ax[0].plot(ks_, [cu[str(k)] for k in ks_], '-o', ms=3, color=c, label=name)
    for name, c in zip(['SVR', 'RFR', 'k-NN', 'PLSR'], ['#00695C', '#2E7D32', '#C98A00', '#6A1B9A']):
        cu = R2['folds'][0]['ofc']['R_' + name]['curve']; ks_ = sorted(int(k) for k in cu); ax[1].plot(ks_, [-cu[str(k)] for k in ks_], '-o', ms=3, color=c, label=name)
    ax[0].set_xlabel('Number of features'); ax[0].set_ylabel('Inner-CV macro-F1'); ax[0].set_title('(a) ML-SFFS, classification (fold 1 training data)', fontsize=9); ax[0].legend(frameon=False, fontsize=7.5)
    ax[1].set_xlabel('Number of features'); ax[1].set_ylabel('Inner-CV RMSE (PDI %)'); ax[1].set_title('(b) ML-SFFS, regression (fold 1 training data)', fontsize=9); ax[1].legend(frameon=False, fontsize=7.5)
    save('l_sffs.png')
print('figures ok')
