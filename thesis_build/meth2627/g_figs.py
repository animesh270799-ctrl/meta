"""Demo figures of the 2026-27 methodology (no real results; all data in the demo figures are simulated)."""
import json, re, os
import numpy as np
import matplotlib; matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, Rectangle, Circle
plt.rcParams.update({'font.family': 'Liberation Sans', 'font.size': 10})
D = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'fig')
TEST = [1, 4, 5, 8, 13, 14, 18, 25, 27, 31, 35, 37, 44, 46, 48]; VAL = [6, 7, 11, 19, 24, 26, 28, 30, 36, 39, 41]
C_TR, C_VA, C_TE = '#CFE3C8', '#BBD5EE', '#F6C59C'
rng = np.random.default_rng(7)


def save(fig, n):
    fig.savefig(os.path.join(D, n), dpi=200, bbox_inches='tight'); plt.close(fig)


def boxes(ax, items, fs=9):
    for (x, y, w, h, t, c) in items:
        ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle='round,pad=0.25,rounding_size=0.8', fc=c, ec='#333', lw=0.8))
        ax.text(x + w / 2, y + h / 2, t, ha='center', va='center', fontsize=fs, wrap=True)


def arrow(ax, a, b, **k):
    ax.annotate('', xy=b, xytext=a, arrowprops=dict(arrowstyle='-|>', color='#333', lw=0.9, **k))


# 1 overall workflow ------------------------------------------------------------
fig, ax = plt.subplots(figsize=(11, 6.6)); ax.set_xlim(0, 100); ax.set_ylim(0, 100); ax.axis('off')
G, B_, O, P_, Y = '#E2EFDA', '#DDEBF7', '#FCE4D6', '#EDE2F6', '#FFF2CC'
boxes(ax, [(1, 80, 22, 15, 'Part A\nField experiment and\ndata collection (A1–A9)', G), (27, 80, 22, 15, 'Part B\nUAV image processing,\nsubplot ROI averages (B1–B6)', G),
           (53, 80, 22, 15, 'Part C\nFeatures of the four\ncameras (C1–C6)', G), (77, 80, 22, 15, 'Part D\n7:3 split by plots,\ninner validation, normalisation', Y),
           (1, 47, 30, 22, 'Objective 1\nCharacterisation\nresponses, optimal wavelengths,\nWRI, indices, texture, DSF,\nphysiology, pre-symptomatic stage', B_),
           (35, 47, 30, 22, 'Objective 2\nDetection and severity\n15 sensor sets; ML + DL;\ntest plots; covariate baseline;\nmaps; Bharatpur test', B_),
           (69, 47, 30, 22, 'Objective 3\nPre-symptomatic prediction\nlater-infected vs healthy;\nearliest detection day;\nrisk maps', B_),
           (1, 14, 62, 20, 'Part L – ASD leaf spectra (same survey points and leaves)\nL1 assembly and quality control → L2 same 7:3 split → L3 pre-processing → L4 indices →\nL5 Objective 1 (leaf) → L6 models (leaf) → L7 evaluation → L8 covariate baseline → L9 leaf–canopy link', P_),
           (69, 14, 30, 20, 'Outputs\nwavelengths and indices,\nbest sensor set, models,\nmaps, earliest detection day', O)], fs=9)
for x in (23.5, 49.5, 75.5): arrow(ax, (x, 87.5), (x + 3, 87.5))
arrow(ax, (88, 80), (84, 69.5)); arrow(ax, (88, 80), (50, 69.5)); arrow(ax, (88, 80), (16, 69.5))
arrow(ax, (31, 58), (34.5, 58)); arrow(ax, (65, 58), (68.5, 58)); arrow(ax, (12, 80), (12, 34.5)); arrow(ax, (63.5, 24), (68.5, 24)); arrow(ax, (84, 47), (84, 34.5))
ax.text(50, 3, 'Everything that learns (selection, tuning, early stopping, scaling) uses the 33 training plots only; the 15 test plots are used once.', ha='center', fontsize=9.5, style='italic')
save(fig, 'g01_workflow.png')

# 2 field layout -----------------------------------------------------------------
L = json.load(open('/home/user/meta/thesis_build/acm/layout.json'))['buffer10']
fig, ax = plt.subplots(figsize=(11, 4.6)); ax.axis('off')
xs, ys = [], []
for r in L:
    m = re.search(r'\((\d+)\)', r['t']);
    if not m: continue
    n = int(m.group(1)); trt = r['t'].split('\n')[0]
    c = C_TE if n in TEST else (C_VA if n in VAL else C_TR)
    ax.add_patch(Rectangle((r['x'], -r['y'] - r['h']), r['w'], r['h'], fc=c, ec='#555', lw=0.7))
    ax.text(r['x'] + r['w'] / 2, -r['y'] - r['h'] / 2, '%s\n%d' % (trt, n), ha='center', va='center', fontsize=6.6, fontweight='bold' if n in TEST + VAL else None)
    xs += [r['x'], r['x'] + r['w']]; ys += [-r['y'], -r['y'] - r['h']]
ax.set_xlim(min(xs) - 0.2, max(xs) + 0.2); ax.set_ylim(min(ys) - 0.9, max(ys) + 0.5); ax.set_aspect('equal')
for c, t in ((C_TR, 'training plots used to fit the networks (22)'), (C_VA, 'training plots used as network validation (11) = one third'), (C_TE, 'test plots (15) = 30% of the plots')):
    ax.add_patch(Rectangle((0, 0), 0, 0, fc=c, ec='#555', label=t))
ax.legend(loc='lower center', bbox_to_anchor=(0.5, -0.17), ncol=3, frameon=False, fontsize=9)
ax.text(min(xs), max(ys) + 0.25, 'Healthy block (plots 1–12, uninoculated)                       10 m buffer                       Inoculated block: R3 (13–24), R2 (25–36), R1 (37–48)', fontsize=8.5)
save(fig, 'g02_layout.png')

# 3 subplot and survey points ------------------------------------------------------
fig, (a1, a2) = plt.subplots(1, 2, figsize=(10.5, 4.4), gridspec_kw=dict(width_ratios=[1.5, 1]))
a1.set_xlim(-0.3, 5.3); a1.set_ylim(-0.5, 3.4); a1.set_aspect('equal'); a1.axis('off')
a1.add_patch(Rectangle((0, 0), 5, 3, fc='#EAF3E5', ec='#333', lw=1.2))
for x in (2.5,): a1.plot([x, x], [0, 3], 'k-', lw=1)
a1.plot([0, 5], [1.5, 1.5], 'k-', lw=1)
for i, (x0, y0) in enumerate([(0, 1.5), (2.5, 1.5), (0, 0), (2.5, 0)]):
    a1.add_patch(Rectangle((x0 + 0.25, y0 + 0.2), 2.0, 1.1, fill=False, ec='#888', ls='--', lw=0.8))
    a1.text(x0 + 1.25, y0 + 1.36, 'subplot %d' % (i + 1), ha='center', fontsize=8.5, fontweight='bold')
    for f in (0.25, 0.5, 0.75):
        px, py = x0 + 0.25 + 2.0 * f, y0 + 0.2 + 1.1 * f
        a1.add_patch(Circle((px, py), 0.09, fc='#C0392B', ec='k', lw=0.5))
a1.text(2.5, -0.35, 'Plot 5 m × 3 m → 4 subplots (2.5 m × 1.5 m); dashed line = inner buffer; red dots = 3 survey points on the diagonal\n(1/4, 1/2 and 3/4 of the diagonal), one tagged plant per point', ha='center', fontsize=8.3)
a2.set_xlim(0, 10); a2.set_ylim(0, 10); a2.axis('off')
a2.plot([5, 5], [0.5, 9.3], color='#5B8C3A', lw=3)
for y, s, lab in ((8.2, 1, 'L3 (3rd fully expanded leaf from top)'), (6.4, -1, 'L5 (5th fully expanded leaf)'), (1.8, 1, 'LL (lowest green leaf)')):
    a2.add_patch(matplotlib.patches.Ellipse((5 + s * 1.3, y), 2.4, 0.9, angle=s * 20, fc='#8BC34A', ec='#33691E'))
    a2.text(5 + s * 2.8, y + 0.7, lab, ha='left' if s > 0 else 'right', fontsize=8.3)
a2.text(5, 0.1, 'At each survey point: grade the three leaves 0–9,\nthen take 2 ASD contact-probe readings of the same leaves', ha='center', fontsize=8.3)
save(fig, 'g03_survey.png')

# 4 timeline -------------------------------------------------------------------------
import datetime as dt
d0 = dt.date(2026, 11, 15); day = lambda s: (dt.date(*s) - d0).days
fig, ax = plt.subplots(figsize=(11, 3.6)); ax.set_ylim(-1.4, 4.3); ax.set_xlim(0, day((2027, 3, 20))); ax.set_yticks([]); [s.set_visible(False) for s in ax.spines.values()]
ax.axhline(0, color='#333', lw=1)
for k, d in enumerate([(2026, 11, 19), (2026, 11, 26), (2026, 12, 3), (2026, 12, 10)]):
    ax.plot(day(d), 0, 'v', color='#6D4C41', ms=9); ax.text(day(d), -0.55, 'D%d\n%d %s' % (k + 1, d[2], 'Nov' if d[1] == 11 else 'Dec'), ha='center', fontsize=7.5)
ax.plot(day((2026, 12, 30)), 0, '*', color='#C0392B', ms=16); ax.text(day((2026, 12, 30)), -0.75, 'inoculation\n30 Dec', ha='center', fontsize=8, color='#C0392B')
pre = [(2027, 1, 1), (2027, 1, 4), (2027, 1, 7)]
post = [(2027, 1, 11), (2027, 1, 18), (2027, 1, 25), (2027, 2, 1), (2027, 2, 8), (2027, 2, 15), (2027, 2, 22), (2027, 3, 1), (2027, 3, 8), (2027, 3, 15)]
for d in pre + post:
    c = '#E67E22' if d in pre else '#2E75B6'; ax.plot([day(d)] * 2, [0.15, 1.15], color=c, lw=2.5)
    ax.text(day(d), 1.3, '%d/%d' % (d[2], d[1]), rotation=90, fontsize=7, ha='center', va='bottom')
for d in [(2027, 1, 7), (2027, 1, 18), (2027, 2, 8), (2027, 3, 1)]: ax.plot(day(d), 2.75, 's', color='#7B1FA2', ms=7)
ax.text(day((2027, 1, 1)) - 2, 3.5, 'flights of all four cameras + leaf scoring + ASD at 3 survey points per subplot (13 dates)', fontsize=8.5)
ax.text(day((2026, 11, 20)), 2.7, 'physiology and LAI (4 dates) ■', fontsize=8.5, color='#7B1FA2')
ax.text(day((2027, 1, 3)), -1.25, 'pre-symptomatic: 2, 5, 8 DAI (orange)          post-symptomatic: 12–75 DAI, weekly (blue)', fontsize=8.5)
save(fig, 'g04_timeline.png')

# 5 split ------------------------------------------------------------------------------
fig, ax = plt.subplots(figsize=(10, 3.2))
rows = [('Leaf dataset (ASD)\n22 464 leaves', 22 * 36 * 13, 11 * 36 * 13, 15 * 36 * 13), ('UAV pre-symptomatic\n576 subplot-dates', 22 * 4 * 3, 11 * 4 * 3, 15 * 4 * 3), ('UAV post-symptomatic\n1920 subplot-dates', 22 * 4 * 10, 11 * 4 * 10, 15 * 4 * 10)]
for i, (lab, tr, va, te) in enumerate(rows):
    tot = tr + va + te; l = 0
    for v, c, t in ((tr, C_TR, 'training: network fit'), (va, C_VA, 'training: network validation'), (te, C_TE, 'test')):
        ax.barh(i, v / tot * 100, left=l, color=c, ec='#555'); ax.text(l + v / tot * 50, i, '%s\n%d (%.1f%%)' % (t, v, v / tot * 100), ha='center', va='center', fontsize=7.6); l += v / tot * 100
ax.set_yticks(range(3)); ax.set_yticklabels([r[0] for r in rows], fontsize=8.5); ax.set_xlim(0, 100); ax.set_xlabel('% of samples')
ax.set_title('7:3 split by whole plots: 33 training plots (green + blue) and 15 test plots (orange).\nML models: GroupKFold(3) over the 33 training plots; networks: 22 plots fit, 11 plots (one third) validate.', fontsize=9.3)
save(fig, 'g05_split.png')

# 6 processing chain --------------------------------------------------------------------
fig, ax = plt.subplots(figsize=(11, 3.6)); ax.set_xlim(0, 100); ax.set_ylim(0, 40); ax.axis('off')
steps = ['B1 Radiometric\ncalibration', 'B2 Orthomosaic,\ngeoreferencing', 'B3 HS quality\ncontrol, smoothing', 'B4 Projection,\nco-registration', 'B5 Resampling\nto HS grid', 'B6 Subplot ROIs,\naverage spectra']
for i, t in enumerate(steps):
    x = 1 + i * 16.5; boxes(ax, [(x, 14, 14.4, 14, t, '#E2EFDA')], fs=8.3)
    if i: arrow(ax, (x - 1.7, 21), (x - 0.2, 21))
ax.text(50, 5, 'Inputs: raw HS cubes, MS / RGB / thermal frames, panels, GCPs → Output: one table per camera, one row per subplot and date', ha='center', fontsize=9)
save(fig, 'g06_processing.png')

# synthetic spectra -------------------------------------------------------------------------
wl = np.arange(400, 2401, 5.0)
def spec(sev, noise=0.0):
    re_ = 718 - 9 * sev
    vis = 0.05 + 0.045 * np.exp(-((wl - 550) / 35) ** 2) + 0.05 * sev * np.exp(-((wl - 660) / 40) ** 2)
    nir = (0.46 - 0.10 * sev) / (1 + np.exp(-(wl - re_) / 11))
    sw = np.where(wl > 1000, -0.00011 * (wl - 1000) * (1 - 0.25 * sev), 0)
    w = -0.12 * np.exp(-((wl - 1450) / 60) ** 2) - 0.18 * np.exp(-((wl - 1940) / 70) ** 2) - 0.05 * np.exp(-((wl - 1180) / 50) ** 2)
    r = vis + nir + sw + w * (1 - 0.2 * sev)
    return np.clip(r + noise * rng.normal(size=wl.size), 0.01, None)
cls = [0, 1, 3, 5, 7, 9]; sv = [0, 0.08, 0.2, 0.4, 0.65, 0.9]
fig, ax = plt.subplots(1, 3, figsize=(12.5, 3.8)); cm = plt.cm.RdYlGn_r(np.linspace(0.05, 0.95, 6))
for c, s, col in zip(cls, sv, cm):
    r = spec(s); ax[0].plot(wl, r, color=col, label='class %d' % c); ax[1].plot(wl, (r - spec(0)) / spec(0) * 100, color=col)
    fd = np.gradient(r, wl); m = (wl >= 650) & (wl <= 800); ax[2].plot(wl[m], fd[m] * 1000, color=col)
ax[0].set_title('a  Mean reflectance by DI class (demo)', fontsize=9.5); ax[0].legend(fontsize=7, ncol=2); ax[0].set_xlabel('nm')
ax[1].set_title('b  Difference from class 0 (%)', fontsize=9.5); ax[1].axhline(0, color='k', lw=0.6); ax[1].set_xlabel('nm')
ax[2].set_title('c  First derivative, red edge (×10⁻³ nm⁻¹)', fontsize=9.5); ax[2].set_xlabel('nm')
for a in ax: a.axvspan(1335, 1460, color='#EEE'); a.axvspan(1785, 1965, color='#EEE')
save(fig, 'g07_spectra_demo.png')

# 8 NDSI map ----------------------------------------------------------------------------------
w2 = np.arange(400, 1001, 10.0); n = w2.size
Ri, Rj = np.meshgrid(w2, w2)
R2 = 0.6 * np.exp(-((Ri - 700) / 60) ** 2 - ((Rj - 790) / 120) ** 2) + 0.35 * np.exp(-((Ri - 550) / 50) ** 2 - ((Rj - 680) / 40) ** 2) + 0.05 * rng.random((n, n))
R2 = np.where(Ri < Rj, R2, np.nan)
fig, ax = plt.subplots(figsize=(5.6, 4.6)); im = ax.pcolormesh(Rj, Ri, R2, cmap='viridis', vmin=0, vmax=0.7, shading='auto'); plt.colorbar(im, label='R² with DI (demo)')
ax.contour(Rj, Ri, np.nan_to_num(R2), levels=[0.5], colors='white', linewidths=1.2)
ax.set_xlabel('band j (nm)'); ax.set_ylabel('band i (nm)'); ax.set_title('NDSI(i, j) R² map; white line R² = 0.5 (demo)', fontsize=9.5)
save(fig, 'g08_ndsi_demo.png')

# 9 SHAP-CARS ---------------------------------------------------------------------------------
cand = np.arange(500, 1000, 5.0); shap = np.abs(0.6 * np.exp(-((cand - 715) / 25) ** 2) + 0.3 * np.exp(-((cand - 560) / 20) ** 2) + 0.08 * rng.random(cand.size))
keep = shap >= np.quantile(shap, 0.6)
fig, ax = plt.subplots(1, 2, figsize=(11.5, 3.6))
ax[0].bar(cand, shap, width=4, color=np.where(keep, '#2E75B6', '#BBBBBB')); ax[0].set_title('a  Mean |SHAP| of candidate bands; blue = top 40% (demo)', fontsize=9.5); ax[0].set_xlabel('nm')
k = cand[keep]; freq = np.clip(0.9 * np.exp(-((k - 715) / 15) ** 2) + 0.7 * np.exp(-((k - 560) / 10) ** 2) + 0.15 * rng.random(k.size), 0, 1)
ax[1].bar(k, freq * 100, width=4, color=np.where(freq >= 0.5, '#C0392B', '#F2B8B0')); ax[1].axhline(50, color='k', ls='--', lw=0.8)
ax[1].set_title('b  CARS selection frequency in 20 runs; red = optimal wavelengths (≥ 50%)', fontsize=9.5); ax[1].set_xlabel('nm'); ax[1].set_ylabel('% of runs')
save(fig, 'g09_shapcars_demo.png')

# 10 selection chain -----------------------------------------------------------------------------
fig, ax = plt.subplots(figsize=(11, 5.4)); ax.set_xlim(0, 100); ax.set_ylim(0, 100); ax.axis('off')
lanes = [('HS bands R + FD', 'NDSI/RSI R² maps →\neffective ranges', 'SHAP (top 40%) →\nCARS (20 runs)', 'OW (≤ 15)'),
         ('HS indices (48 + 3 RE\n+ NDSI, RSI, WRI)', '|r| ≥ 0.95\nredundancy filter', 'ReliefF / RReliefF\n(k = 10)', 'VI (top 5)'),
         ('HS texture (3 PCs ×\n8 GLCM measures)', '|r| ≥ 0.95\nredundancy filter', 'mRMR (top 6) →\nTTFI search', 'TF + TTFI'),
         ('MS, RGB, thermal\nfeatures', '|r| ≥ 0.95\nredundancy filter', 'ReliefF / RReliefF\n(thermal kept)', 'top 5 per camera')]
for i, (a, b, c, d) in enumerate(lanes):
    y = 80 - i * 20
    boxes(ax, [(1, y, 18, 14, a, '#E2EFDA'), (24, y, 18, 14, b, '#DDEBF7'), (47, y, 18, 14, c, '#DDEBF7'), (70, y, 11, 14, d, '#FFF2CC')], fs=8.2)
    for x in (19.5, 42.5, 65.5): arrow(ax, (x, y + 7), (x + 4, y + 7))
    arrow(ax, (81.5, y + 7), (86.5, 50))
boxes(ax, [(87, 40, 12, 20, 'VIF < 10\n→ DSF of\neach camera\nand task', '#FCE4D6')], fs=8.5)
ax.text(50, 3, 'Objective 1: chain run on all samples (description). Objectives 2–3: the same chain re-run on the training plots only (model inputs).', ha='center', fontsize=9, style='italic')
save(fig, 'g10_selection_chain.png')

# 11 models + pseudo-image --------------------------------------------------------------------------
fig, ax = plt.subplots(1, 2, figsize=(11.5, 4.2), gridspec_kw=dict(width_ratios=[1.6, 1]))
a = ax[0]; a.set_xlim(0, 100); a.set_ylim(0, 100); a.axis('off')
boxes(a, [(2, 70, 30, 24, 'Machine learning\nSVM/SVR, RF, XGBoost,\nk-NN, PLS-DA/PLSR\n(SFFS ≤ 15 features)', '#DDEBF7'),
          (36, 70, 30, 24, 'Feature-fusion network\nDNN-F1\n(input-level fusion,\nall three tasks)', '#EDE2F6'),
          (70, 70, 28, 24, 'Pseudo-image networks\nDT-EDNet, EfficientNet-B0,\nResNet18, ConvNeXt V2\n(Tasks A and B)', '#FCE4D6'),
          (2, 30, 96, 26, 'Same 33 training plots and same 15 test plots for every model and sensor set\nML: SFFS and grid search by GroupKFold(3) over the training plots → refit on all 33 training plots\nNetworks: fit on 22 training plots; early stopping on 11 training plots (one third)\nTest plots: predicted once → OA, kappa, macro-F1, per-class F1; R², RMSE, RPD', '#F2F2F2')], fs=8.6)
for x in (17, 51, 84): arrow(a, (x, 70), (x, 56.5))
b = ax[1]; k = 5; grid = np.full((k, k), np.nan); vals = np.r_[rng.random(12), rng.random(6) + 1, rng.random(4) + 2]
grid.flat[:vals.size] = np.floor(vals)
b.imshow(np.ma.masked_invalid(grid), cmap=matplotlib.colors.ListedColormap(['#2E75B6', '#E67E22', '#C0392B']), vmin=0, vmax=2)
for i in range(k):
    for j in range(k):
        v = grid[i, j]; b.text(j, i, '0' if np.isnan(v) else ('OW', 'VI', 'TF')[int(v)], ha='center', va='center', fontsize=8, color='w' if not np.isnan(v) else 'k')
b.set_xticks([]); b.set_yticks([]); b.set_title('Pseudo-image k × k (k = ⌈√p⌉, here 22 features → 5 × 5;\ngroups in order, zero padding) (demo)', fontsize=9)
save(fig, 'g11_models.png')

# 12 evaluation demo ---------------------------------------------------------------------------------
fig, ax = plt.subplots(1, 2, figsize=(11.5, 4.2))
cmx = np.array([[40, 6, 2, 0, 0, 0], [8, 22, 7, 1, 0, 0], [2, 7, 25, 8, 1, 0], [0, 1, 8, 30, 7, 1], [0, 0, 1, 7, 18, 4], [0, 0, 0, 1, 4, 9]])
ax[0].imshow(cmx, cmap='Blues'); [ax[0].text(j, i, cmx[i, j], ha='center', va='center', fontsize=8, color='w' if cmx[i, j] > 20 else 'k') for i in range(6) for j in range(6)]
ax[0].set_xticks(range(6)); ax[0].set_xticklabels(cls); ax[0].set_yticks(range(6)); ax[0].set_yticklabels(cls); ax[0].set_xlabel('predicted DI class'); ax[0].set_ylabel('observed DI class'); ax[0].set_title('a  Confusion matrix on the test plots (demo)', fontsize=9.5)
sets = ['HS', 'MS', 'RGB', 'TIR', 'HS+TIR', 'MS+TIR', 'HS+MS', 'All four']; m = np.array([0.62, 0.55, 0.47, 0.40, 0.66, 0.58, 0.64, 0.68])
ax[1].barh(sets, m, color='#2E75B6'); ax[1].set_xlim(0, 0.85); ax[1].set_xlabel('macro-F1 (Task B) on the test plots'); ax[1].set_title('b  Comparison of sensor sets (demo)', fontsize=9.5)
save(fig, 'g12_eval_demo.png')

# 13 covariate baseline demo --------------------------------------------------------------------------
fig, ax = plt.subplots(figsize=(6.4, 3.8))
v = [0.48, 0.60, 0.66]
ax.bar(['M0\ncovariates only', 'M1\nsensors only', 'M2\nsensors + covariates'], v, color=['#A6A6A6', '#2E75B6', '#548235'])
ax.annotate('ΔS = M1 − M0', xy=(0.5, 0.62), ha='center', fontsize=9); ax.annotate('ΔC = M2 − M1', xy=(1.5, 0.70), ha='center', fontsize=9)
ax.set_ylim(0, 0.8); ax.set_ylabel('macro-F1 on test plots (demo)'); ax.set_title('Gain of the sensors over the covariate baseline (demo)', fontsize=9.5)
save(fig, 'g13_covariate_demo.png')

# 14 leaf chain -----------------------------------------------------------------------------------
fig, ax = plt.subplots(figsize=(11, 4.4)); ax.set_xlim(0, 100); ax.set_ylim(0, 100); ax.axis('off')
it = ['L1 Assemble the\nleaf table, checks', 'L2 Same 7:3\nsplit by plot', 'L3 SG smoothing,\n400–2400 nm, FD,\n5-nm bands', 'L4 48 indices +\n3 red-edge\nparameters', 'L5 Objective 1:\nmaps, SHAP-CARS,\nWRI, ReliefF, VIF',
      'L6 Selection on\ntraining leaves;\nML + DL models', 'L7 Test leaves:\nmetrics', 'L8 Covariate\nbaseline', 'L9 Leaf–canopy\nlink', 'L10 Pre-symptomatic\nleaves (2, 5, 8 DAI)']
for i, t in enumerate(it):
    x = 1 + (i % 5) * 19.8; y = 58 if i < 5 else 14
    boxes(ax, [(x, y, 17.5, 27, t, '#EDE2F6')], fs=8.4)
    if i % 5: arrow(ax, (x - 2.1, y + 13.5), (x - 0.2, y + 13.5))
arrow(ax, (90, 58), (10, 41.5), connectionstyle='arc3,rad=-0.15')
save(fig, 'g14_leaf_chain.png')

# 15 pre-symptomatic demo --------------------------------------------------------------------------
dai = np.array([2, 5, 8, 12, 19, 26]); d = np.array([0.1, 0.25, 0.55, 0.9, 1.3, 1.7]); 
fig, ax = plt.subplots(1, 2, figsize=(11, 3.6))
ax[0].errorbar(dai, d, yerr=0.35, fmt='o-', color='#C0392B', capsize=3); ax[0].axhline(0, color='k', lw=0.7)
ax[0].axvline(8, color='#2E75B6', ls='--'); ax[0].text(8.4, 1.6, 'earliest date with a\nsignificant t-test (demo)', fontsize=8, color='#2E75B6')
ax[0].set_xlabel('days after inoculation'); ax[0].set_ylabel('difference later-infected − healthy (± SD)'); ax[0].set_title('a  Response of one feature (demo)', fontsize=9.5)
ax[1].bar(['2 DAI', '5 DAI', '8 DAI'], [0.55, 0.63, 0.74], color=['#F5CBA7', '#EB984E', '#CA6F1E']); ax[1].axhline(0.5, color='k', ls='--', lw=0.8)
ax[1].set_ylim(0.3, 0.9); ax[1].set_ylabel('AUC on test plots (demo)'); ax[1].set_title('b  Pre-symptomatic AUC by date (demo)', fontsize=9.5)
save(fig, 'g15_presym_demo.png')
print('figures written')
