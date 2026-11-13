import matplotlib; matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, Rectangle
import numpy as np, json
from scipy.interpolate import PchipInterpolator
from scipy import stats
import os
D = os.path.dirname(os.path.abspath(__file__)) + '/'
F = D + 'fig/'
plt.rcParams['font.family'] = 'DejaVu Sans'
rng = np.random.default_rng(7)
CL = ['Healthy', 'Low', 'Moderate', 'High']
CC = ['#2E7D32', '#F9A825', '#EF6C00', '#C62828']
COL = {'RGB': '#2E7D32', 'MS': '#1565C0', 'HS': '#00838F', 'TIR': '#C62828'}
OUT = {}

def box(ax, x, y, w, h, title, lines, fc, ec, tfs=10, lfs=8.4):
    ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle='round,pad=0.02,rounding_size=0.1', fc=fc, ec=ec, lw=1.5))
    ax.text(x + 0.12, y + h - 0.16, title, fontsize=tfs, fontweight='bold', va='top', color='#1E3A1F')
    if lines: ax.text(x + 0.12, y + h - 0.52, '\n'.join(lines), fontsize=lfs, va='top', color='#222', linespacing=1.32)
def head(ax, x, y, w, h, t, c, fs=9.5):
    ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle='round,pad=0.02,rounding_size=0.08', fc=c, ec='none'))
    ax.text(x + w / 2, y + h / 2, t, ha='center', va='center', color='white', fontsize=fs, fontweight='bold')
def arrow(ax, x1, y1, x2, y2):
    ax.annotate('', xy=(x2, y2), xytext=(x1, y1), arrowprops=dict(arrowstyle='-|>', color='#555', lw=1.3))

# ---------------- dummy dataset ----------------
n = 432  # e.g. 6 post-symptomatic dates x 72 plots
cls = rng.choice(4, n, p=[0.30, 0.35, 0.20, 0.15])
DI = np.where(cls == 0, 0, np.where(cls == 1, rng.uniform(0.5, 25, n), np.where(cls == 2, rng.uniform(25.1, 50, n), rng.uniform(50.1, 90, n))))
z = DI / 100
feat = {
 'PSSRa (HS)': 9.5 - 5.5 * z + rng.normal(0, 0.9, n),
 'REP (HS, nm)': 722 - 14 * z + rng.normal(0, 2.2, n),
 'WRI (HS)': 0.05 + 0.45 * z + rng.normal(0, 0.06, n),
 'DWSI-1 (HS)': 2.6 - 0.9 * z + rng.normal(0, 0.18, n),
 'NDRE (MS)': 0.42 - 0.22 * z + rng.normal(0, 0.04, n),
 'PSRI_MS (MS)': 0.02 + 0.10 * z + rng.normal(0, 0.025, n),
 'CTD (TIR, °C)': -3.0 + 3.2 * z + rng.normal(0, 0.8, n),
 'NRCT (TIR)': 0.35 + 0.35 * z + rng.normal(0, 0.1, n),
 'Contrast (RGB)': 8 + 14 * z + rng.normal(0, 3.0, n),
 'Hue (RGB)': 95 - 25 * z + rng.normal(0, 6, n),
}
FN = list(feat)

# ---------------- m0 master flow ----------------
fig, ax = plt.subplots(figsize=(11, 13.6)); ax.set_xlim(0, 11); ax.set_ylim(0, 13.6); ax.axis('off')
for x, k, t in zip([0.25, 2.95, 5.65, 8.35], ['RGB', 'MS', 'HS', 'TIR'], ['RGB', 'Multispectral (MS)', 'Hyperspectral (HS)', 'Thermal (TIR)']):
    head(ax, x, 12.95, 2.4, 0.5, t, COL[k]); arrow(ax, x + 1.2, 12.95, x + 1.2, 12.68)
box(ax, 0.25, 10.75, 10.5, 1.9, 'COMMON STEPS  A1–A4', ['A1 Experiment: 72 plots (4 inoculation timings × 3 varieties × 2 doses × 3 replications)', 'A2 Ground truth: DI (%) → classes Healthy (0), Low (0–25], Moderate (25–50], High (> 50); tasks C (4 classes) and R (DI)', 'A3 Pre-processing: orthomosaics, reflectance / temperature calibration, canopy mask, plot-mean features', 'A4 Pooled plot-date table; leave-one-replication-out validation (all dates of a plot kept together)'], '#EEF3E8', '#2C5F2D', 10.5, 8.6)
arrow(ax, 5.5, 10.75, 5.5, 10.45)
box(ax, 0.25, 7.55, 10.5, 2.85, 'OBJECTIVE 1  Characterise white rust (each sensor)', ['1.1 Feature extraction: HS 481 bands + FD + 39 indices + red edge; MS bands + 12 indices + texture;', '      RGB texture, colour, cover; TIR CT, CTD, CTR, NRCT, MTD, texture', '1.2 Univariate response: one-way ANOVA + Tukey HSD across 4 classes; Pearson r with DI; physiology', '1.3 HS band level: correlation scalogram (R, FD, SD vs DI) + ReliefF (4 classes); one band per correlated region', '1.4 White Rust Index (ReliefF + exhaustive search, Mahlein 2013)', '1.5 Class discrimination: two-step stepwise canonical discriminant analysis, CDA (Bhattacharya 2013)', '1.6 Disease-specific features (DSF): Boruta for C and R → 8 DSF pools; cross-sensor correlation'], '#E3F2FD', '#1565C0', 10.5, 8.5)
arrow(ax, 5.5, 7.55, 5.5, 7.25)
box(ax, 0.25, 4.4, 10.5, 2.8, 'OBJECTIVE 2  Classify and estimate severity by multimodal fusion', ['2.1 Optimum features: VIF < 10 → ML-SFFS (criterion macro-F1 for C, RMSE for R)', '2.2 Six models: SVM/SVR, RF/RFR, k-NN, PLSR (R only), DNN-F1, DNN-F2', '2.3 Single sensors S1–S4 vs combinations S5 RGB+TIR, S6 MS+TIR, S7 HS+TIR, S8 all four', '      Fusion: ML-SFFS feature-level fusion and DNN-F1 / DNN-F2', '2.4 Evaluation: OA, kappa, macro-F1, confusion matrix | R², RMSE, NRMSE', '2.5 Maps of class and DI      2.6 Independent validation (Bharatpur, farmers\' fields)'], '#FCE4EC', '#AD1457', 10.5, 8.5)
arrow(ax, 5.5, 4.4, 5.5, 4.1)
box(ax, 0.25, 2.0, 10.5, 2.05, 'OBJECTIVE 3  Pre-symptomatic prediction', ['3.1 Labels: control = healthy; inoculated plot = infected only if symptoms appear later (Tian 2021)', '3.2 Early features: t-test + % difference from healthy; Boruta', '3.3 VIF → ML-SFFS → SVM, RF, k-NN for S1–S8 (sensitivity, specificity)      3.4 Risk maps'], '#F3E5F5', '#6A1B9A', 10.5, 8.5)
ax.add_patch(FancyBboxPatch((0.25, 0.3), 10.5, 1.3, boxstyle='round,pad=0.02,rounding_size=0.1', fc='white', ec='#999', lw=1.2, ls='--'))
ax.text(5.5, 1.12, 'Outputs: DSF pools + White Rust Index (O1) | best sensors, fusion and model + maps (O2) | early-warning model + risk maps (O3)', ha='center', fontsize=7.7, fontweight='bold', color='#333')
ax.text(5.5, 0.66, 'All selection and tuning inside training replications; final test at Bharatpur and in farmers\' fields', ha='center', fontsize=8.6, color='#555', style='italic')
plt.savefig(F + 'm0_master.png', dpi=200, bbox_inches='tight'); plt.close()

# ---------------- m1 layout (dummy) ----------------
fig, axs = plt.subplots(1, 3, figsize=(12, 4.3))
trt = [(g, v, d) for g in range(4) for v in range(3) for d in range(2)]
vcol = ['#C62828', '#EF6C00', '#2E7D32']
for r, ax in enumerate(axs):
    order = rng.permutation(24)
    for k, t in enumerate(order):
        g, v, d = trt[t]; x, y = k % 6, k // 6
        ax.add_patch(Rectangle((x, y), 0.92, 0.92, fc=vcol[v], ec='black' if d else 'none', lw=1.6, alpha=0.35 + 0.15 * g))
        ax.text(x + 0.46, y + 0.46, 'G%dV%d\n%s' % (g + 1, v + 1, 'D2' if d else 'D1'), ha='center', va='center', fontsize=6.6)
    ax.set_xlim(-0.1, 6); ax.set_ylim(-0.1, 4); ax.set_aspect('equal'); ax.axis('off'); ax.set_title('Replication R%d (24 plots, 3 m × 3 m)' % (r + 1), fontsize=10)
fig.text(0.5, 0.02, 'Dummy randomisation. Colour: V1 Varuna (red), V2 Pusa Vijay (orange), V3 PM 38 (green); shade: inoculation timing G1–G4; black border: inoculated (D2).', ha='center', fontsize=8.5, style='italic')
plt.savefig(F + 'm1_layout.png', dpi=200, bbox_inches='tight'); plt.close()

# ---------------- m2 DI histogram ----------------
fig, axs = plt.subplots(1, 2, figsize=(11, 3.9), gridspec_kw=dict(width_ratios=[1.6, 1]))
ax = axs[0]
ax.hist(DI[DI > 0], bins=np.arange(0, 95, 2.5), color='#90A4AE', edgecolor='white')
ax.bar(-1.25, (DI == 0).sum() / 4, width=2.4, color=CC[0]); ax.text(-1.25, (DI == 0).sum() / 4 + 2, 'DI = 0\n(n=%d, ÷4)' % (DI == 0).sum(), ha='center', fontsize=7.5)
for xl in (25, 50): ax.axvline(xl, color='k', ls='--', lw=1)
for xm, t, c in ((12.5, 'Low\n0 < DI ≤ 25', CC[1]), (37.5, 'Moderate\n25 < DI ≤ 50', CC[2]), (70, 'High\nDI > 50', CC[3])):
    ax.text(xm, ax.get_ylim()[1] * 0.85, t, ha='center', fontsize=8.5, color=c, fontweight='bold')
ax.set_xlabel('Disease index DI (%)'); ax.set_ylabel('Plot-dates'); ax.set_title('(a) Dummy DI distribution (432 post-symptomatic plot-dates)', fontsize=10)
ax = axs[1]; counts = [(cls == k).sum() for k in range(4)]
ax.bar(CL, counts, color=CC); [ax.text(i, c + 4, str(c), ha='center', fontsize=9) for i, c in enumerate(counts)]
ax.set_title('(b) Dummy class sizes (unequal)', fontsize=10); ax.set_ylabel('Plot-dates')
plt.tight_layout(); plt.savefig(F + 'm2_di.png', dpi=200); plt.close()
OUT['counts'] = counts

# ---------------- m3 preprocessing chains ----------------
fig, ax = plt.subplots(figsize=(11, 6.6)); ax.set_xlim(0, 11); ax.set_ylim(0, 6.6); ax.axis('off')
chains = {'RGB': ['Raw images (85%/80% overlap)', 'GCPs + structure-from-motion', 'Orthomosaic + surface model', 'HS canopy mask transferred\n(nearest neighbour, edge erosion)', 'Plot features: texture,\ncolour, VF, CH'],
          'MS': ['Raw 5-band images', 'Panels + irradiance sensor\n(empirical line)', 'Reflectance orthomosaic', 'HS canopy mask transferred\n(nearest neighbour, edge erosion)', 'Plot features: bands,\n12 indices, texture'],
          'HS': ['Raw VNIR + SWIR cubes', 'White reference; orthorectif.;\nremove 1350–1450, 1800–1950 nm', 'Canopy mask: NDVI > 0.6\nAND SAM < 0.3 rad', '30 endmembers per plot;\nkeep crop, average; SG', 'Plot features: 481 bands,\nFD, 39 indices, red edge'],
          'TIR': ['Raw thermal (camera\nwarm-up 15–20 min)', 'Radiometric conversion\n(emissivity, Ta, RH, height)', 'Check with ground targets', 'HS canopy mask transferred\n(edge erosion: no warm soil)', 'Plot features: CT, CTD,\nCTR, NRCT, MTD, texture']}
for i, (k, steps) in enumerate(chains.items()):
    x = 0.25 + i * 2.7; head(ax, x, 6.0, 2.4, 0.45, k, COL[k])
    for j, s in enumerate(steps):
        y = 5.0 - j * 1.12
        ax.add_patch(FancyBboxPatch((x, y), 2.4, 0.82, boxstyle='round,pad=0.02,rounding_size=0.06', fc='#F7F9F7' if j < 4 else '#E8F5E9', ec=COL[k], lw=1.2))
        ax.text(x + 1.2, y + 0.41, s, ha='center', va='center', fontsize=7.9)
        arrow(ax, x + 1.2, y + 0.82 + (0.3 if j == 0 else 0.3), x + 1.2, y + 0.84) if j == 0 else arrow(ax, x + 1.2, y + 1.12, x + 1.2, y + 0.84)
ax.text(5.5, 0.15, 'All products co-registered with the same GCPs; one HS canopy mask per flight applied to every sensor; plot features (0.5 m inner buffer) in native resolution.', ha='center', fontsize=8.4, style='italic', color='#444')
plt.savefig(F + 'm3_preproc.png', dpi=200, bbox_inches='tight'); plt.close()

# ---------------- m4 CV diagram ----------------
fig, ax = plt.subplots(figsize=(11, 4.4)); ax.set_xlim(0, 11); ax.set_ylim(0, 4.4); ax.axis('off')
for f in range(3):
    y = 3.4 - f * 1.15; ax.text(0.1, y + 0.3, 'Fold %d' % (f + 1), fontsize=9.5, fontweight='bold', va='center')
    for r in range(3):
        test = (r == f); x = 1.1 + r * 1.75
        ax.add_patch(FancyBboxPatch((x, y), 1.6, 0.6, boxstyle='round,pad=0.02,rounding_size=0.05', fc='#C62828' if test else '#2E7D32', ec='none'))
        ax.text(x + 0.8, y + 0.3, ('R%d test' if test else 'R%d train') % (r + 1), ha='center', va='center', color='white', fontsize=9, fontweight='bold')
box(ax, 6.7, 0.35, 4.1, 3.75, 'Inside each training set (2 replications)', ['Grouped 4-fold CV by plot (12 plots per fold):', ' • Boruta, ReliefF, scalogram band choice', ' • VIF and ML-SFFS', ' • hyperparameter tuning', 'Then: refit on both training replications', 'and predict the test replication once.', 'Report mean ± SD over the 3 folds;', 'final model refitted on all data and', 'tested at Bharatpur / farmers\' fields.'], '#FFF8E1', '#C98A00', 9.6, 8.4)
plt.savefig(F + 'm4_cv.png', dpi=200, bbox_inches='tight'); plt.close()

# ---------------- m5 class spectra (dummy) ----------------
pts_h = [(400,0.040),(450,0.045),(500,0.060),(550,0.120),(600,0.070),(650,0.045),(680,0.040),(700,0.090),(720,0.250),(750,0.420),(800,0.460),(900,0.470),(970,0.440),(1050,0.460),(1200,0.400),(1300,0.420),(1450,0.200),(1650,0.300),(1800,0.270),(1940,0.080),(2100,0.180),(2200,0.200),(2300,0.150),(2500,0.080)]
pts_d = [(400,0.060),(450,0.070),(500,0.090),(550,0.150),(600,0.110),(650,0.090),(680,0.085),(700,0.130),(720,0.240),(750,0.350),(800,0.380),(900,0.390),(970,0.370),(1050,0.390),(1200,0.360),(1300,0.380),(1450,0.240),(1650,0.330),(1800,0.300),(1940,0.120),(2100,0.220),(2200,0.240),(2300,0.190),(2500,0.110)]
wl = np.arange(400, 2501)
H = PchipInterpolator(*zip(*pts_h))(wl); Dd = PchipInterpolator(*zip(*pts_d))(wl)
fig, axs = plt.subplots(1, 2, figsize=(12, 4.2))
mask = ((wl >= 1350) & (wl <= 1450)) | ((wl >= 1800) & (wl <= 1950))
for k, a in enumerate([0, 0.35, 0.7, 1.0]):
    s = H + a * (Dd - H); s2 = s.copy(); s2[mask] = np.nan
    axs[0].plot(wl, s2, color=CC[k], lw=1.8, label=CL[k])
    fd = np.gradient(s, wl) * 1000; fd[mask] = np.nan
    axs[1].plot(wl[(wl <= 1000)], fd[(wl <= 1000)], color=CC[k], lw=1.8, label=CL[k])
for a in axs: a.legend(fontsize=8, frameon=False)
axs[0].set_title('(a) Dummy class-mean reflectance (water bands removed)', fontsize=10); axs[0].set_xlabel('Wavelength (nm)'); axs[0].set_ylabel('Reflectance')
axs[1].set_title('(b) Dummy first derivative, 400–1000 nm (red-edge peak)', fontsize=10); axs[1].set_xlabel('Wavelength (nm)'); axs[1].set_ylabel('FD (×10^-3 per nm)')
plt.tight_layout(); plt.savefig(F + 'm5_spectra.png', dpi=200); plt.close()

# ---------------- m6 boxplots + KW ----------------
sel = ['PSSRa (HS)', 'NDRE (MS)', 'CTD (TIR, °C)', 'Contrast (RGB)']
fig, axs = plt.subplots(1, 4, figsize=(13, 3.8))
rows = []
for ax, f in zip(axs, sel):
    data = [feat[f][cls == k] for k in range(4)]
    bp = ax.boxplot(data, tick_labels=['H', 'L', 'M', 'Hi'], patch_artist=True, widths=0.6, showfliers=False)
    for p, c in zip(bp['boxes'], CC): p.set_facecolor(c); p.set_alpha(0.6)
    Hs, p = stats.f_oneway(*data); rho, pr = stats.pearsonr(feat[f], DI)
    from statsmodels.stats.multicomp import pairwise_tukeyhsd
    tk = pairwise_tukeyhsd(feat[f], cls); 
    ax.set_title('%s\nANOVA F = %.0f, p < 0.001; r = %.2f' % (f, Hs, rho), fontsize=8.8, pad=6)
    means = [d.mean() for d in data]; order = np.argsort(means)[::-1]; letters = ['']*4
    import string; L = iter(string.ascii_lowercase); cur = next(L); letters[order[0]] = cur
    rej = {(min(a,b2), max(a,b2)): r for a, b2, r in zip(tk._multicomp.pairindices[0], tk._multicomp.pairindices[1], tk.reject)}
    for k in range(1, 4):
        prev = order[k-1]; c = order[k]
        if rej[(min(prev,c), max(prev,c))]: cur = next(L)
        letters[c] = cur
    lo, hi = ax.get_ylim(); ax.set_ylim(lo, hi + 0.18 * (hi - lo))
    for i2 in range(4): ax.text(i2 + 1, hi + 0.05 * (hi - lo), letters[i2], ha='center', va='bottom', fontsize=10, fontweight='bold')
    rows.append([f, '%.2f ± %.2f' % (data[0].mean(), data[0].std()), '%.2f ± %.2f' % (data[1].mean(), data[1].std()), '%.2f ± %.2f' % (data[2].mean(), data[2].std()), '%.2f ± %.2f' % (data[3].mean(), data[3].std()), '%.0f' % Hs, '%.2f' % rho])
fig.text(0.5, -0.02, 'Dummy data. H = Healthy, L = Low, M = Moderate, Hi = High. Classes sharing a letter do not differ (Tukey HSD, p < 0.05).', ha='center', fontsize=8.5, style='italic')
plt.tight_layout(); plt.savefig(F + 'm6_box.png', dpi=200, bbox_inches='tight'); plt.close()
OUT['stats_rows'] = rows

# ---------------- m7 scalogram + ReliefF (dummy) ----------------
w5 = np.arange(400, 2401, 5); keep = ~(((w5 >= 1350) & (w5 <= 1450)) | ((w5 >= 1800) & (w5 <= 1950)))
rhoR = np.interp(w5, [400, 500, 550, 600, 680, 700, 730, 760, 900, 1100, 1300, 1500, 1650, 1750, 2000, 2200, 2400], [0.55, 0.45, 0.35, 0.6, 0.72, 0.4, -0.3, -0.62, -0.66, -0.55, -0.35, 0.55, 0.68, 0.6, 0.62, 0.7, 0.5]) + rng.normal(0, 0.03, len(w5))
rhoF = np.interp(w5, [400, 500, 520, 600, 690, 700, 715, 730, 760, 900, 1150, 1500, 1700, 2000, 2400], [0.1, 0.5, 0.3, -0.2, 0.2, -0.65, -0.8, -0.6, -0.1, 0.05, 0.4, 0.2, 0.45, 0.3, 0.1]) + rng.normal(0, 0.06, len(w5))
relief = np.clip(0.6 * np.abs(rhoR) * (1 + 0.4 * np.sin(w5 / 60)) + rng.normal(0, 0.03, len(w5)), 0, None)
for a in (rhoR, rhoF, relief): a[~keep] = np.nan
fig, axs = plt.subplots(3, 1, figsize=(11, 7.2), sharex=True)
for ax, y, t in ((axs[0], rhoR, 'Pearson r(λ): reflectance vs DI'), (axs[1], rhoF, 'Pearson r(λ): first derivative vs DI')):
    ax.plot(w5, y, color='#00838F', lw=1.4); ax.axhline(0, color='grey', lw=0.6)
    thr = np.nanpercentile(np.abs(y), 95); ax.axhline(thr, color='#C62828', ls='--', lw=0.8); ax.axhline(-thr, color='#C62828', ls='--', lw=0.8)
    top = np.abs(y) >= thr; ax.plot(w5[top], y[top], 'o', color='#C62828', ms=3)
    ax.set_ylabel('r'); ax.set_title(t + ' (red: top 5% of |r|)', fontsize=9.5); ax.set_ylim(-1, 1)
ax = axs[2]; ax.fill_between(w5, 0, relief, color='#1565C0', alpha=0.5); thr = np.nanpercentile(relief, 95); ax.axhline(thr, color='#C62828', ls='--', lw=0.8)
ax.set_ylabel('ReliefF weight'); ax.set_title('ReliefF weights for the four classes (red line: top 5%)', fontsize=9.5); ax.set_xlabel('Wavelength (nm)')
for ax in axs:
    for a, b in ((1350, 1450), (1800, 1950)): ax.axvspan(a, b, color='#EEEEEE')
fig.suptitle('Dummy correlation scalograms and ReliefF weights; one band per correlated region is kept from each list', fontsize=10, y=1.0)
plt.tight_layout(); plt.savefig(F + 'm7_scalogram.png', dpi=200, bbox_inches='tight'); plt.close()

# ---------------- m8 WRI ----------------
fig, axs = plt.subplots(1, 2, figsize=(11.5, 4.3), gridspec_kw=dict(width_ratios=[1.15, 1]))
l = np.arange(450, 951, 6); L1, L2 = np.meshgrid(l, l)
BA = 0.55 + 0.33 * np.exp(-((L1 - 560) ** 2 / 900 + (L2 - 705) ** 2 / 500)) + 0.2 * np.exp(-((L1 - 705) ** 2 / 500 + (L2 - 560) ** 2 / 900)) + rng.normal(0, 0.01, L1.shape)
BA[np.abs(L1 - L2) < 50] = np.nan
im = axs[0].imshow(BA, origin='lower', extent=[450, 950, 450, 950], cmap='viridis', vmin=0.5, vmax=0.9)
plt.colorbar(im, ax=axs[0], label='Balanced accuracy'); axs[0].set_xlabel('λ1 (nm)'); axs[0].set_ylabel('λ2 (nm)')
axs[0].set_title('(a) Dummy balanced accuracy of ND(λ1, λ2)\n(grey diagonal: bands < 50 nm apart excluded)', fontsize=9.5)
i = np.nanargmax(BA); axs[0].plot(L1.flat[i], L2.flat[i], 'r*', ms=14)
data = [feat['WRI (HS)'][cls == k] for k in range(4)]
vp = axs[1].violinplot(data, showmedians=True)
for b, c in zip(vp['bodies'], CC): b.set_facecolor(c); b.set_alpha(0.6)
axs[1].axhline(0.12, color='k', ls='--', lw=1); axs[1].text(4.45, 0.13, 'threshold t', ha='right', fontsize=8)
axs[1].set_xticks([1, 2, 3, 4], CL); axs[1].set_ylabel('WRI'); axs[1].set_title('(b) Dummy WRI by class', fontsize=9.5)
plt.tight_layout(); plt.savefig(F + 'm8_wri.png', dpi=200); plt.close()
OUT['wri_best'] = [int(L1.flat[i]), int(L2.flat[i]), round(float(np.nanmax(BA)), 2)]

# ---------------- m9 CDA (real LDA on dummy features) ----------------
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis as LDA
from sklearn.preprocessing import StandardScaler
hsF = ['PSSRa (HS)', 'REP (HS, nm)', 'WRI (HS)', 'DWSI-1 (HS)']
Xh = StandardScaler().fit_transform(np.column_stack([feat[f] for f in hsF]))
lda = LDA(n_components=3).fit(Xh, cls); Zs = lda.transform(Xh)
ev = lda.explained_variance_ratio_
# eigenvalues and Wilks
Sw = sum(np.cov(Xh[cls == k].T) * ((cls == k).sum() - 1) for k in range(4)); St = np.cov(Xh.T) * (n - 1)
eig = np.sort(np.real(np.linalg.eigvals(np.linalg.solve(Sw, St - Sw))))[::-1][:3]
wilks = float(np.prod(1 / (1 + eig))); can = np.sqrt(eig / (1 + eig))
fig, ax0 = plt.subplots(figsize=(7.2, 4.6))
for k in range(4):
    ax0.scatter(Zs[cls == k, 0], Zs[cls == k, 1], s=8, color=CC[k], alpha=0.5, label=CL[k])
    ax0.plot(Zs[cls == k, 0].mean(), Zs[cls == k, 1].mean(), 'X', color='black', ms=9)
ax0.set_xlabel('Canonical function 1 (%.0f%% of separation)' % (100 * ev[0])); ax0.set_ylabel('Canonical function 2 (%.0f%%)' % (100 * ev[1]))
ax0.legend(fontsize=8, markerscale=2); ax0.set_title('Dummy CDA score plot (X = class centre)', fontsize=10)
def jm(a, b):
    m1, m2 = a.mean(0), b.mean(0); S1, S2 = np.cov(a.T), np.cov(b.T); S = (S1 + S2) / 2
    B = 0.125 * (m1 - m2) @ np.linalg.solve(S, m1 - m2) + 0.5 * np.log(np.linalg.det(S) / np.sqrt(np.linalg.det(S1) * np.linalg.det(S2)))
    return 2 * (1 - np.exp(-B))
J = np.array([[jm(Xh[cls == i], Xh[cls == j]) if i != j else np.nan for j in range(4)] for i in range(4)])
from sklearn.model_selection import cross_val_score
acc = cross_val_score(LDA(), Xh, cls, cv=4).mean()
plt.tight_layout(); plt.savefig(F + 'm9_cda.png', dpi=200); plt.close()
OUT['cda'] = {'acc': round(float(acc), 2), 'eig': [round(float(e), 2) for e in eig], 'can': [round(float(c), 2) for c in can], 'wilks': round(wilks, 3),
              'coef': [[f] + ['%.2f' % v for v in lda.scalings_[i, :2]] for i, f in enumerate(hsF)],
              'jm': [[CL[i], CL[j], '%.2f' % J[i, j]] for i in range(4) for j in range(i + 1, 4)]}

# ---------------- m10 Boruta (dummy importance distributions) ----------------
names = ['NDRE', 'CI_rededge', 'PSRI_MS', 'MTCI', 'NDVI', 'RE band', 'NIR band', 'CON_RE', 'ENT_NIR', 'HOM_B', 'MEA_G', 'SAVI']
mu = [14, 12, 11, 10, 6.5, 9, 7, 5.6, 4.8, 2.2, 1.8, 4.4]
shadow = rng.normal(3.0, 0.9, (100, 3)).max(1)
imp = [rng.normal(m, 1.2, 100) for m in mu]
status = ['Confirmed' if m > 5.5 else ('Tentative' if m > 4 else 'Rejected') for m in mu]
scol = {'Confirmed': '#2E7D32', 'Tentative': '#F9A825', 'Rejected': '#C62828'}
order = np.argsort(mu)
fig, ax = plt.subplots(figsize=(11, 4.2))
data = [shadow] + [imp[i] for i in order]
bp = ax.boxplot(data, patch_artist=True, showfliers=False, widths=0.6)
bp['boxes'][0].set_facecolor('#90A4AE')
for p, i in zip(bp['boxes'][1:], order): p.set_facecolor(scol[status[i]])
ax.set_xticks(range(1, len(data) + 1), ['shadowMax'] + [names[i] for i in order], rotation=40, ha='right', fontsize=8.5)
ax.set_ylabel('Importance (Z-score)'); ax.set_title('Dummy Boruta result for the MS sensor, 4-class task (green confirmed, yellow tentative, red rejected, grey best shadow)', fontsize=9.5)
plt.tight_layout(); plt.savefig(F + 'm10_boruta.png', dpi=200); plt.close()

# ---------------- m11 cross-sensor correlation ----------------
Xall = np.column_stack([feat[f] for f in FN]); C = np.corrcoef(Xall.T)
fig, ax = plt.subplots(figsize=(7.6, 6.2)); im = ax.imshow(C, cmap='RdBu_r', vmin=-1, vmax=1)
for i in range(len(FN)):
    for j in range(len(FN)): ax.text(j, i, '%.1f' % C[i, j], ha='center', va='center', fontsize=7)
ax.set_xticks(range(len(FN)), FN, rotation=60, ha='right', fontsize=8); ax.set_yticks(range(len(FN)), FN, fontsize=8)
plt.colorbar(im, label='Pearson r'); ax.set_title('Dummy correlation matrix of DSFs from the four sensors', fontsize=10)
plt.tight_layout(); plt.savefig(F + 'm11_xcorr.png', dpi=200); plt.close()

# ---------------- VIF table (real computation on dummy) ----------------
vf = {'NDVI780': 0.70 - 0.3 * z + rng.normal(0, 0.03, n)}
vf['NDVI850'] = vf['NDVI780'] + rng.normal(0, 0.008, n)
vf['SR850'] = 6 - 3 * z + 8 * (vf['NDVI780'] - 0.7) + rng.normal(0, 0.15, n)
vf['PSSRa'] = feat['PSSRa (HS)']; vf['REP'] = feat['REP (HS, nm)']; vf['WRI'] = feat['WRI (HS)']; vf['DWSI-1'] = feat['DWSI-1 (HS)']; vf['PRI'] = -0.02 - 0.04 * z + rng.normal(0, 0.012, n)
def vifs(M):
    out = []
    for j in range(M.shape[1]):
        y = M[:, j]; X = np.column_stack([np.ones(len(y)), np.delete(M, j, 1)]); b = np.linalg.lstsq(X, y, rcond=None)[0]
        r2 = 1 - ((y - X @ b) ** 2).sum() / ((y - y.mean()) ** 2).sum(); out.append(1 / (1 - r2))
    return np.array(out)
names_v = list(vf); M = np.column_stack([vf[k] for k in names_v]); it = []
while True:
    v = vifs(M); it.append([', '.join('%s %.0f' % (nm, x) if x >= 10 else '%s %.1f' % (nm, x) for nm, x in zip(names_v, v))])
    if v.max() < 10: break
    j = int(np.argmax(v)); it[-1].append('remove ' + names_v[j]); names_v.pop(j); M = np.delete(M, j, 1)
it[-1].append('all VIF < 10: stop')
OUT['vif'] = it

# ---------------- m12 SFFS (real mlxtend on dummy) ----------------
from mlxtend.feature_selection import SequentialFeatureSelector as SFS
from sklearn.svm import SVC
from sklearn.neighbors import KNeighborsClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.pipeline import make_pipeline
pool = ['PSSRa (HS)', 'REP (HS, nm)', 'WRI (HS)', 'DWSI-1 (HS)', 'NDRE (MS)', 'PSRI_MS (MS)', 'CTD (TIR, °C)', 'NRCT (TIR)', 'Contrast (RGB)', 'Hue (RGB)']
Xp = np.column_stack([feat[f] for f in pool]); Xp = np.column_stack([Xp, rng.normal(0, 1, (n, 4))]); pn = pool + ['noise1', 'noise2', 'noise3', 'noise4']
res = {}
for nm, est in (('SVM', make_pipeline(StandardScaler(), SVC(C=4, gamma='scale', class_weight='balanced'))), ('k-NN', make_pipeline(StandardScaler(), KNeighborsClassifier(7))), ('RF', RandomForestClassifier(150, random_state=0, class_weight='balanced'))):
    s = SFS(est, k_features=(1, 10), forward=True, floating=True, scoring='f1_macro', cv=4, n_jobs=-1).fit(Xp, cls)
    sub = s.get_metric_dict(); ks = sorted(sub); sc = [sub[k]['avg_score'] for k in ks]
    kb = ks[int(np.argmax(sc))]; thr = sub[kb]['avg_score'] - 0.01
    k1 = min(k for k in ks if sub[k]['avg_score'] >= thr)
    res[nm] = (ks, sc, [pn[i] for i in sub[k1]['feature_idx']], sub[k1]['avg_score'], thr)
fig, ax = plt.subplots(figsize=(9.5, 4))
for (nm, (ks, sc, best, bs, thr)), c in zip(res.items(), ['#1565C0', '#2E7D32', '#C62828']):
    ax.plot(ks, sc, 'o-', color=c, label='%s (OFC: %d features, macro-F1 %.2f)' % (nm, len(best), bs)); ax.plot(len(best), bs, '*', color=c, ms=15)
ax.set_xlabel('Number of features in subset'); ax.set_ylabel('Cross-validated macro-F1'); ax.legend(fontsize=8.5); ax.grid(alpha=0.3)
ax.set_title('ML-SFFS on a dummy pooled DSF set (10 informative + 4 noise features)\nstar = OFC: best score, or a smaller subset within 0.01 of it', fontsize=9.5)
plt.tight_layout(); plt.savefig(F + 'm12_sffs.png', dpi=200); plt.close()
OUT['sffs'] = {k: [', '.join(v[2]), '%.2f' % v[3]] for k, v in res.items()}

# ---------------- m13 fusion bars (dummy) ----------------
sets = ['S1 RGB', 'S2 MS', 'S3 HS', 'S4 TIR', 'S5 RGB+TIR', 'S6 MS+TIR', 'S7 HS+TIR', 'S8 All']
f1 = [0.58, 0.66, 0.72, 0.55, 0.66, 0.73, 0.79, 0.81]; r2 = [0.52, 0.64, 0.71, 0.48, 0.63, 0.72, 0.80, 0.83]
fig, axs = plt.subplots(1, 2, figsize=(12, 4))
for ax, v, t in ((axs[0], f1, 'Classification (4 classes): macro-F1'), (axs[1], r2, 'Regression (DI): R²')):
    b = ax.bar(sets, v, color=['#90A4AE'] * 4 + ['#1565C0'] * 4, yerr=[0.04] * 8, capsize=3)
    ax.set_ylim(0, 1); ax.set_title('Dummy best model per input set — ' + t, fontsize=9.5); ax.tick_params(axis='x', rotation=40, labelsize=8.5)
    for i, x in enumerate(v): ax.text(i, x + 0.05, '%.2f' % x, ha='center', fontsize=8)
plt.tight_layout(); plt.savefig(F + 'm13_fusion.png', dpi=200); plt.close()

# ---------------- m14 confusion + scatter ----------------
cm = np.array([[40, 3, 1, 0], [4, 41, 5, 1], [0, 5, 22, 3], [0, 0, 3, 16]])
P = cm.diagonal() / cm.sum(0); R = cm.diagonal() / cm.sum(1); F1 = 2 * P * R / (P + R); N = cm.sum(); oa = cm.trace() / N
pe = (cm.sum(0) * cm.sum(1)).sum() / N ** 2; kap = (oa - pe) / (1 - pe)
fig, axs = plt.subplots(1, 2, figsize=(11.5, 4.5))
axs[0].imshow(cm, cmap='Greens')
for i in range(4):
    for j in range(4): axs[0].text(j, i, cm[i, j], ha='center', va='center', fontsize=10, color='white' if cm[i, j] > 25 else 'black')
axs[0].set_xticks(range(4), CL); axs[0].set_yticks(range(4), CL); axs[0].set_xlabel('Predicted'); axs[0].set_ylabel('Observed')
axs[0].set_title('(a) Dummy confusion matrix (one test replication, 144 plot-dates)\nOA = %.2f, kappa = %.2f, macro-F1 = %.2f' % (oa, kap, F1.mean()), fontsize=9.5)
obs = DI[:144]; pred = np.clip(obs + rng.normal(0, 7, 144) - 0.08 * (obs - 30), 0, 100)
r2v = 1 - ((obs - pred) ** 2).sum() / ((obs - obs.mean()) ** 2).sum(); rmse = np.sqrt(((obs - pred) ** 2).mean())
axs[1].scatter(obs, pred, s=10, c=[CC[c] for c in cls[:144]], alpha=0.7); axs[1].plot([0, 100], [0, 100], 'k--', lw=1)
for xl in (25, 50): axs[1].axvline(xl, color='grey', lw=0.6, ls=':'); axs[1].axhline(xl, color='grey', lw=0.6, ls=':')
axs[1].set_xlabel('Observed DI (%)'); axs[1].set_ylabel('Predicted DI (%)'); axs[1].set_title('(b) Dummy DI regression: R² = %.2f, RMSE = %.1f, NRMSE = %.0f%%' % (r2v, rmse, 100 * rmse / obs.mean()), fontsize=9.5)
plt.tight_layout(); plt.savefig(F + 'm14_eval.png', dpi=200); plt.close()
OUT['cm'] = {'P': ['%.2f' % x for x in P], 'R': ['%.2f' % x for x in R], 'F1': ['%.2f' % x for x in F1], 'oa': '%.2f' % oa, 'kap': '%.2f' % kap, 'mf1': '%.2f' % F1.mean(), 'r2': '%.2f' % r2v, 'rmse': '%.1f' % rmse}

# ---------------- m15 maps ----------------
fig, axs = plt.subplots(1, 3, figsize=(12.5, 3.6))
obsc = rng.choice(4, (6, 12), p=[0.3, 0.35, 0.2, 0.15]); predc = obsc.copy(); flip = rng.random((6, 12)) < 0.18
predc[flip] = np.clip(predc[flip] + rng.choice([-1, 1], flip.sum()), 0, 3)
from matplotlib.colors import ListedColormap
cmap = ListedColormap(CC)
axs[0].imshow(obsc, cmap=cmap, vmin=0, vmax=3); axs[0].set_title('(a) Observed class', fontsize=9.5)
axs[1].imshow(predc, cmap=cmap, vmin=0, vmax=3); axs[1].set_title('(b) Predicted class', fontsize=9.5)
err = np.abs(rng.normal(0, 7, (6, 12))); im = axs[2].imshow(err, cmap='magma_r'); axs[2].set_title('(c) Absolute DI error (%)', fontsize=9.5); plt.colorbar(im, ax=axs[2], fraction=0.03)
for a in axs: a.set_xticks([]); a.set_yticks([])
from matplotlib.patches import Patch
fig.legend(handles=[Patch(color=c, label=l) for c, l in zip(CC, CL)], loc='lower center', ncol=4, fontsize=8.5, frameon=False)
fig.suptitle('Dummy plot-level maps of the 72-plot field for one flight', fontsize=10)
plt.tight_layout(rect=[0, 0.08, 1, 0.95]); plt.savefig(F + 'm15_maps.png', dpi=200); plt.close()

# ---------------- m16 pre-symptomatic ----------------
fig, axs = plt.subplots(1, 2, figsize=(12, 4.3))
fe = ['CTD', 'NRCT', 'MTD', 'PRI', 'PSSRa', 'REP', 'WI', 'NDRE', 'PSRI_MS', 'Contrast', 'Hue']
sens = ['TIR', 'TIR', 'TIR', 'HS', 'HS', 'HS', 'HS', 'MS', 'MS', 'RGB', 'RGB']
d = [14, 12, 9, 10, 6, 7, 8, 5, 3, 2, 1.5]
o = np.argsort(d)
axs[0].barh([fe[i] for i in o], [d[i] for i in o], color=[COL[sens[i]] for i in o]); 
axs[0].set_xlabel('Difference from healthy plots (%)'); axs[0].set_title('(a) Dummy pre-symptomatic differences (colour = sensor)', fontsize=9.5)
fpr = np.linspace(0, 1, 100)
for nm, auc, c in (('S3 HS', 0.74, COL['HS']), ('S4 TIR', 0.71, COL['TIR']), ('S2 MS', 0.65, COL['MS']), ('S1 RGB', 0.57, COL['RGB']), ('S7 HS+TIR', 0.80, 'black')):
    a = auc / (1 - auc); tpr = 1 - (1 - fpr) ** a; axs[1].plot(fpr, tpr, color=c, lw=1.8 if nm != 'S7 HS+TIR' else 2.4, label='%s (AUC %.2f)' % (nm, auc))
axs[1].plot([0, 1], [0, 1], 'k:', lw=0.8); axs[1].set_xlabel('1 − specificity'); axs[1].set_ylabel('Sensitivity'); axs[1].legend(fontsize=8); axs[1].set_title('(b) Dummy ROC curves of pre-symptomatic models', fontsize=9.5)
plt.tight_layout(); plt.savefig(F + 'm16_presym.png', dpi=200); plt.close()

# ---------------- m17 risk map ----------------
fig, ax = plt.subplots(figsize=(7.5, 3.6))
risk = np.clip(rng.beta(2, 5, (6, 12)) + (rng.random((6, 12)) < 0.3) * 0.45, 0, 1)
im = ax.imshow(risk, cmap='RdYlGn_r', vmin=0, vmax=1); plt.colorbar(im, ax=ax, label='Probability of infection')
ax.set_xticks([]); ax.set_yticks([]); ax.set_title('Dummy pre-symptomatic risk map (72 plots, one flight)', fontsize=10)
plt.tight_layout(); plt.savefig(F + 'm17_risk.png', dpi=200); plt.close()

json.dump(OUT, open(D + 'dummy.json', 'w'), indent=1, ensure_ascii=False, default=lambda o: o.item())
print(json.dumps(OUT, ensure_ascii=False, default=lambda o: o.item())[:3000])

# ---------------- m18 class overlap ----------------
from scipy.stats import gaussian_kde
fig, axs = plt.subplots(1, 2, figsize=(11.5, 4), gridspec_kw=dict(width_ratios=[1.3, 1]))
xs = np.linspace(feat['PSSRa (HS)'].min() - 1, feat['PSSRa (HS)'].max() + 1, 300)
for k in range(4):
    kd = gaussian_kde(feat['PSSRa (HS)'][cls == k]); axs[0].fill_between(xs, kd(xs), color=CC[k], alpha=0.35, label=CL[k]); axs[0].plot(xs, kd(xs), color=CC[k])
axs[0].set_xlabel('PSSRa (dummy)'); axs[0].set_ylabel('Density'); axs[0].legend(fontsize=8)
axs[0].set_title('(a) One feature: neighbouring classes overlap (dummy data)', fontsize=9.5)
cmx = np.array([[40, 3, 1, 0], [4, 41, 5, 1], [0, 5, 22, 3], [0, 0, 3, 16]]); N = cmx.sum()
exact = np.trace(cmx) / N; adj = sum(cmx[i, j] for i in range(4) for j in range(4) if abs(i - j) <= 1) / N
vals = [exact, adj, exact - 0.03, adj - 0.005]
b = axs[1].bar(['Direct\nexact', 'Direct\n± 1 class', 'From DI\nexact', 'From DI\n± 1 class'], vals, color=['#1565C0', '#90CAF9', '#2E7D32', '#A5D6A7'])
for i, v in enumerate(vals): axs[1].text(i, v + 0.01, '%.2f' % v, ha='center', fontsize=9)
axs[1].set_ylim(0, 1.1); axs[1].set_ylabel('Accuracy'); axs[1].set_title('(b) Most errors are between adjacent classes (dummy)', fontsize=9.5)
plt.tight_layout(); plt.savefig(F + 'm18_overlap.png', dpi=200); plt.close()
OUT['overlap'] = ['%.2f' % exact, '%.2f' % adj]
json.dump(OUT, open(D + 'dummy.json', 'w'), indent=1, ensure_ascii=False, default=lambda o: o.item())
