"""Dummy figures for the Objective 1 document (six severity grades 0, 1, 3, 5, 7, 9). Real computations on simulated data."""
import os, json, string
import numpy as np, matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch
from scipy import stats
from scipy.interpolate import PchipInterpolator
from scipy.ndimage import gaussian_filter1d
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis as LDA
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import cross_val_score
from sklearn.ensemble import RandomForestClassifier
from statsmodels.stats.multicomp import pairwise_tukeyhsd

D = os.path.dirname(os.path.abspath(__file__)) + '/'; F = D + 'fig/'
plt.rcParams['font.family'] = 'DejaVu Sans'
rng = np.random.default_rng(21)
G = [0, 1, 3, 5, 7, 9]; GL = ['0', '1', '3', '5', '7', '9']
GC = ['#2E7D32', '#9CCC65', '#FDD835', '#FB8C00', '#E53935', '#7B1FA2']
COL = {'RGB': '#2E7D32', 'MS': '#1565C0', 'HS': '#00838F', 'TIR': '#C62828'}
OUT = {}

# ---------------- dummy plot-level severity ----------------
counts = [130, 90, 60, 70, 50, 32]; n = sum(counts)
lims = [(0, 0), (0.5, 5), (5.01, 10), (10.01, 25), (25.01, 50), (50.01, 85)]
cls = np.repeat(np.arange(6), counts)
area = np.array([rng.uniform(*lims[c]) if c else 0.0 for c in cls])        # plot mean % leaf area
DI = np.clip(area * 1.1 + np.where(cls > 0, rng.normal(0, 2, n), 0), 0, 100)  # PDI (dummy, close to area)
s = area / 100
def grade_of(a):
    return np.select([a <= 0, a <= 5, a <= 10, a <= 25, a <= 50], [0, 1, 2, 3, 4], 5)
assert (grade_of(area) == cls).all()

def box(ax, x, y, w, h, title, lines, fc, ec, tfs=10, lfs=8.4):
    ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle='round,pad=0.02,rounding_size=0.1', fc=fc, ec=ec, lw=1.5))
    ax.text(x + 0.12, y + h - 0.16, title, fontsize=tfs, fontweight='bold', va='top', color='#1E3A1F')
    if lines: ax.text(x + 0.12, y + h - 0.52, '\n'.join(lines), fontsize=lfs, va='top', color='#222', linespacing=1.3)
def head(ax, x, y, w, h, t, c, fs=9.5):
    ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle='round,pad=0.02,rounding_size=0.08', fc=c, ec='none'))
    ax.text(x + w / 2, y + h / 2, t, ha='center', va='center', color='white', fontsize=fs, fontweight='bold')
def arrow(ax, x1, y1, x2, y2):
    ax.annotate('', xy=(x2, y2), xytext=(x1, y1), arrowprops=dict(arrowstyle='-|>', color='#555', lw=1.2))

# ---------------- o1_tiers: tier flow chart ----------------
fig, ax = plt.subplots(figsize=(11, 12.6)); ax.set_xlim(0, 11); ax.set_ylim(0, 12.6); ax.axis('off')
box(ax, 0.25, 11.35, 10.5, 1.0, 'Tier 0 — Common inputs (all sensors)', ['Post-symptomatic plot-dates of the 8 flights; plot grade 0, 1, 3, 5, 7, 9 (0–9 key) and PDI (%); physiology; training replications only'], '#ECEFF1', '#455A64', 10, 8.5)
xs = [0.25, 2.95, 5.65, 8.35]; names = ['HS', 'MS', 'RGB', 'TIR']
for x, k in zip(xs, names):
    head(ax, x, 10.55, 2.4, 0.45, {'HS': 'Hyperspectral (HS)', 'MS': 'Multispectral (MS)', 'RGB': 'RGB', 'TIR': 'Thermal (TIR)'}[k], COL[k], 9); arrow(ax, x + 1.2, 11.35, x + 1.2, 11.02)
t1 = {'HS': ['481 bands, FD, SD', 'REP, Dr, SDr', '48 indices (9 SWIR)'], 'MS': ['5 bands', '12 indices', '40 GLCM textures'], 'RGB': ['24 GLCM textures', 'H, S, V colour', 'VF, CH (+ flower', 'fraction covariate)'], 'TIR': ['CT, CTD, CTR', 'NRCT, MTD', '8 GLCM textures']}
for x, k in zip(xs, names):
    box(ax, x, 8.75, 2.4, 1.65, '%s Tier 1  Features' % k, t1[k], '#F7F9F7', COL[k], 9, 8.1); arrow(ax, x + 1.2, 10.55, x + 1.2, 10.42)
box(ax, 0.25, 7.05, 2.4, 1.45, 'HS Tier 2  Band level', ['Scalogram + ReliefF', 'one band per region'], '#E0F2F1', COL['HS'], 9, 8.1)
box(ax, 0.25, 5.35, 2.4, 1.45, 'HS Tier 3  WRI', ['ND(λ1, λ2) + w R(λ3)', 'Mahlein 2013'], '#E0F2F1', COL['HS'], 9, 8.1)
arrow(ax, 1.45, 8.75, 1.45, 8.52); arrow(ax, 1.45, 7.05, 1.45, 6.82)
for x in xs[1:]: ax.annotate('', xy=(x + 1.2, 4.95), xytext=(x + 1.2, 8.75), arrowprops=dict(arrowstyle='-|>', color='#999', lw=1.0, ls='--'))
arrow(ax, 1.45, 5.35, 1.45, 4.95)
box(ax, 0.25, 3.85, 10.5, 1.05, 'Univariate response  (HS Tier 4 | MS, RGB, TIR Tier 2)  — Common method M1', ['One-way ANOVA + Tukey HSD across 6 grades; Pearson r with PDI; physiology correlation'], '#E3F2FD', '#1565C0', 9.5, 8.4)
box(ax, 0.25, 2.65, 10.5, 1.0, 'Class discrimination  (HS Tier 5 | MS, RGB, TIR Tier 3)  — Common methods M2 (VIF) + M3 (CDA)', ['Stepwise canonical discriminant analysis (CDA); HS: two steps (bands, then indices + WRI)'], '#FCE4EC', '#AD1457', 9.5, 8.4)
box(ax, 0.25, 1.45, 10.5, 1.0, 'Disease-specific features  (HS Tier 6 | MS, RGB, TIR Tier 4)  — Common method M4', ['Boruta for 6-grade classification and for PDI regression → 2 DSF pools per sensor'], '#FFF8E1', '#C98A00', 9.5, 8.4)
box(ax, 0.25, 0.1, 10.5, 1.1, 'Cross-sensor tier', ['Correlation between sensors\' DSFs; optional combined CDA; comparison of sensors → 8 DSF pools to Objectives 2 and 3'], '#F3E5F5', '#6A1B9A', 9.5, 8.4)
for y1, y2 in ((3.85, 3.67), (2.65, 2.47), (1.45, 1.22)): arrow(ax, 5.5, y1, 5.5, y2)
plt.savefig(F + 'o1_tiers.png', dpi=200, bbox_inches='tight'); plt.close()

# ---------------- o1_classes: grade key and dummy distribution ----------------
fig, axs = plt.subplots(1, 2, figsize=(11.5, 3.9), gridspec_kw=dict(width_ratios=[1.6, 1]))
ax = axs[0]; ax.hist(area[area > 0], bins=np.arange(0, 86, 2), color='#90A4AE', edgecolor='white')
for xl in (5, 10, 25, 50): ax.axvline(xl, color='k', ls='--', lw=0.9)
for xm, t, c in ((2.5, '1', GC[1]), (7.5, '3', GC[2]), (17.5, '5', GC[3]), (37.5, '7', GC[4]), (67, '9', GC[5])):
    ax.text(xm, ax.get_ylim()[1] * 0.9, 'grade ' + t, ha='center', fontsize=8.5, color='black', fontweight='bold', bbox=dict(fc=c, ec='none', alpha=0.5, pad=1.5))
ax.set_xlabel('Plot mean leaf area with pustules (%)'); ax.set_ylabel('Plot-dates'); ax.set_title('(a) Dummy % area of diseased plot-dates with the 0–9 key limits (grade 0 = no pustules)', fontsize=9.5)
ax = axs[1]; ax.bar(GL, counts, color=GC); [ax.text(i, c + 2, str(c), ha='center', fontsize=9) for i, c in enumerate(counts)]
ax.set_xlabel('Grade'); ax.set_ylabel('Plot-dates'); ax.set_title('(b) Dummy class sizes (432 plot-dates)', fontsize=9.5)
plt.tight_layout(); plt.savefig(F + 'o1_classes.png', dpi=200); plt.close()

# ---------------- spectra per grade ----------------
pts_h = [(400,.040),(450,.045),(500,.060),(550,.120),(600,.070),(650,.045),(680,.040),(700,.090),(720,.250),(750,.420),(800,.460),(900,.470),(970,.440),(1050,.460),(1200,.400),(1300,.420),(1450,.200),(1650,.300),(1800,.270),(1940,.080),(2100,.180),(2200,.200),(2300,.150),(2400,.110)]
pts_d = [(400,.060),(450,.070),(500,.090),(550,.150),(600,.110),(650,.090),(680,.085),(700,.130),(720,.240),(750,.350),(800,.380),(900,.390),(970,.370),(1050,.390),(1200,.360),(1300,.380),(1450,.240),(1650,.330),(1800,.300),(1940,.120),(2100,.220),(2200,.240),(2300,.190),(2400,.140)]
wl = np.arange(400, 2401); Hs = PchipInterpolator(*zip(*pts_h))(wl); Ds = PchipInterpolator(*zip(*pts_d))(wl)
mask = ((wl >= 1350) & (wl <= 1450)) | ((wl >= 1800) & (wl <= 1950))
fig, axs = plt.subplots(1, 2, figsize=(12, 4.2))
for k, a in enumerate([0, 0.03, 0.08, 0.18, 0.38, 0.7]):
    sp = Hs + a * (Ds - Hs) / 0.7; sp2 = sp.copy(); sp2[mask] = np.nan; axs[0].plot(wl, sp2, color=GC[k], lw=1.6, label='grade ' + GL[k])
    fd = np.gradient(sp, wl) * 1000; fd[mask] = np.nan; axs[1].plot(wl[wl <= 1000], fd[wl <= 1000], color=GC[k], lw=1.6, label='grade ' + GL[k])
for a in axs: a.legend(fontsize=7.5, frameon=False, ncol=2)
axs[0].set_title('(a) Dummy grade-mean reflectance (water bands removed)', fontsize=10); axs[0].set_xlabel('Wavelength (nm)'); axs[0].set_ylabel('Reflectance')
axs[1].set_title('(b) Dummy first derivative, 400–1000 nm (red-edge peak)', fontsize=10); axs[1].set_xlabel('Wavelength (nm)'); axs[1].set_ylabel('FD (×10^-3 per nm)')
plt.tight_layout(); plt.savefig(F + 'o1_spectra.png', dpi=200); plt.close()

# ---------------- SWIR index bands ----------------
fig, ax = plt.subplots(figsize=(11, 3.9))
for k in (0, 5):
    a = [0, 0.03, 0.08, 0.18, 0.38, 0.7][k]; sp = Hs + a * (Ds - Hs) / 0.7; sp[mask] = np.nan
    ax.plot(wl, sp, color=GC[k], lw=1.8, label='grade ' + GL[k])
for lo, hi in ((1350, 1450), (1800, 1950)): ax.axvspan(lo, hi, color='#BDBDBD', alpha=0.5)
ax.text(1400, 0.49, 'removed\n(water vapour)', ha='center', fontsize=7.5, color='#555'); ax.text(1875, 0.49, 'removed\n(water vapour)', ha='center', fontsize=7.5, color='#555')
bands = [(1068, 'RBI', '#6A1B9A'), (1148, 'NDBI', '#AD1457'), (1175, 'ROTI', '#00838F'), (1240, 'NDWI', '#1565C0'), (1301, 'NDBI', '#AD1457'), (1560, 'RBI', '#6A1B9A'),
         (1600, 'MSI', '#2E7D32'), (1649, 'NDII', '#EF6C00'), (1660, 'DWSI', '#C62828'), (1982, 'ROTI', '#00838F')]
for i, (b, lab, c) in enumerate(bands):
    ax.axvline(b, color=c, lw=1.1, ls='--'); ax.text(b + 6, 0.02 + 0.045 * (i % 4), '%s %d' % (lab, b), fontsize=7.2, color=c, rotation=0)
ax.set_xlim(950, 2400); ax.set_ylim(0, 0.56); ax.set_xlabel('Wavelength (nm)'); ax.set_ylabel('Reflectance')
ax.set_title('Dummy SWIR reflectance of grades 0 and 9 with the bands of the SWIR disease indices (VNIR partners not shown)', fontsize=9.5)
ax.legend(fontsize=8, frameon=False, loc='upper right'); plt.tight_layout(); plt.savefig(F + 'o1_swir.png', dpi=200); plt.close()

# ---------------- multi-class ReliefF on simulated spectra (6 grades) ----------------
w = np.arange(400, 2401, 5); keep = ~(((w >= 1350) & (w <= 1450)) | ((w >= 1800) & (w <= 1950))); w = w[keep]
H = PchipInterpolator(*zip(*pts_h))(w); Dd = PchipInterpolator(*zip(*pts_d))(w)
a = np.clip(s / 0.7, 0, 1.2)
X = H + 0.5 * a[:, None] * (Dd - H)
X += 0.03 * np.minimum(a, 0.15)[:, None] / 0.15 * np.exp(-((w - 555) / 25) ** 2)
X += 0.05 * (a ** 0.5)[:, None] * np.exp(-((w - 705) / 12) ** 2)
X += 0.10 * (a ** 3)[:, None] * np.exp(-((w - 1620) / 140) ** 2)
X *= rng.uniform(0.97, 1.03, (n, 1)); X += gaussian_filter1d(rng.normal(0, 0.004, X.shape), 3, axis=1)
def relieff(X, y, k=10):
    Z = (X - X.min(0)) / (X.max(0) - X.min(0)); Dm = np.abs(Z[:, None, :] - Z[None, :, :]).sum(2); np.fill_diagonal(Dm, np.inf)
    cl = np.unique(y); P = {c: np.mean(y == c) for c in cl}; m = len(y); W = np.zeros(X.shape[1])
    for i in range(m):
        same = np.where(y == y[i])[0]; same = same[same != i]; hits = same[np.argsort(Dm[i, same])[:k]]
        W -= np.abs(Z[i] - Z[hits]).sum(0) / (m * k)
        for c in cl:
            if c == y[i]: continue
            oth = np.where(y == c)[0]; miss = oth[np.argsort(Dm[i, oth])[:k]]
            W += P[c] / (1 - P[y[i]]) * np.abs(Z[i] - Z[miss]).sum(0) / (m * k)
    return W
W = relieff(X, cls)
C = np.corrcoef(X.T); regions = []; i = 0
while i < len(w):
    j = i
    while j + 1 < len(w) and C[i, j + 1] >= 0.95 and w[j + 1] - w[j] == 5: j += 1
    regions.append((i, j)); i = j + 1
thr = np.percentile(W, 95); sel = []
for (i, j) in regions:
    idx = np.arange(i, j + 1); idx = idx[W[idx] >= thr]
    if len(idx): sel.append(idx[np.argmax(W[idx])])
sel = sorted(sel)
adj = [(0, 1), (1, 2), (2, 3), (3, 4), (4, 5), (0, 5)]
PW = np.array([relieff(X[(cls == p) | (cls == q)][:, sel], cls[(cls == p) | (cls == q)]) for p, q in adj])
fig = plt.figure(figsize=(12, 7.6)); gs = fig.add_gridspec(2, 1, height_ratios=[1, 1.05], hspace=0.45)
ax = fig.add_subplot(gs[0]); wf = np.arange(400, 2401, 5); Wf = np.zeros(len(wf)); Wf[np.isin(wf, w)] = W
ax.fill_between(wf, 0, Wf, color='#1565C0', alpha=0.45, step='mid'); ax.axhline(thr, color='#C62828', ls='--', lw=1)
ax.text(2395, thr, ' top 5%', color='#C62828', fontsize=8, va='bottom', ha='right'); ax.plot(w[sel], W[sel], '*', color='#C62828', ms=12)
for b in sel: ax.text(w[b], W[b] * 1.04, '%d' % w[b], ha='center', va='bottom', fontsize=8)
for x0, x1 in ((1350, 1450), (1800, 1950)): ax.axvspan(x0, x1, color='#EEEEEE')
ax.set_xlim(400, 2400); ax.set_ylim(0, W.max() * 1.25); ax.set_ylabel('ReliefF weight'); ax.set_xlabel('Wavelength (nm)')
ax.set_title('(a) Multi-class ReliefF weights for six grades (0, 1, 3, 5, 7, 9; k = 10); stars = one band kept per correlated region', fontsize=10)
ax = fig.add_subplot(gs[1]); im = ax.imshow(PW, cmap='YlGnBu', aspect='auto')
for r in range(PW.shape[0]):
    for c in range(PW.shape[1]): ax.text(c, r, '%.2f' % PW[r, c], ha='center', va='center', fontsize=8.5, color='white' if PW[r, c] > PW.max() * 0.6 else 'black')
ax.set_xticks(range(len(sel)), ['%d nm' % w[b] for b in sel]); ax.set_yticks(range(len(adj)), ['grade %s vs %s' % (GL[p], GL[q]) for p, q in adj])
plt.colorbar(im, ax=ax, fraction=0.025, label='Pairwise ReliefF weight')
ax.set_title('(b) Pairwise ReliefF at the kept bands: adjacent grades and 0 vs 9', fontsize=10)
fig.suptitle('Dummy data: multi-class ReliefF for the six white-rust grades', fontsize=11.5, fontweight='bold', y=0.97)
plt.savefig(F + 'o1_relief.png', dpi=200, bbox_inches='tight'); plt.close()
OUT['relief_sel'] = [int(w[b]) for b in sel]; OUT['relief_regions'] = len(regions)

# ---------------- WRI figure ----------------
fig, axs = plt.subplots(1, 2, figsize=(11.5, 4.3), gridspec_kw=dict(width_ratios=[1.15, 1]))
l = np.arange(450, 951, 6); L1, L2 = np.meshgrid(l, l)
BA = 0.55 + 0.33 * np.exp(-((L1 - 558) ** 2 / 900 + (L2 - 702) ** 2 / 500)) + 0.2 * np.exp(-((L1 - 702) ** 2 / 500 + (L2 - 558) ** 2 / 900)) + rng.normal(0, 0.01, L1.shape)
BA[np.abs(L1 - L2) < 50] = np.nan
im = axs[0].imshow(BA, origin='lower', extent=[450, 950, 450, 950], cmap='viridis', vmin=0.5, vmax=0.9)
plt.colorbar(im, ax=axs[0], label='Balanced accuracy'); axs[0].set_xlabel('λ1 (nm)'); axs[0].set_ylabel('λ2 (nm)')
k_ = np.nanargmax(BA); axs[0].plot(L1.flat[k_], L2.flat[k_], 'r*', ms=14)
axs[0].set_title('(a) Dummy balanced accuracy of ND(λ1, λ2)\n(diagonal blank: bands < 50 nm apart excluded)', fontsize=9.5)
wri = 0.05 + 0.6 * np.sqrt(s) + rng.normal(0, 0.05, n)
vp = axs[1].violinplot([wri[cls == k] for k in range(6)], showmedians=True)
for b, c in zip(vp['bodies'], GC): b.set_facecolor(c); b.set_alpha(0.6)
axs[1].axhline(0.12, color='k', ls='--', lw=1); axs[1].text(6.4, 0.13, 'threshold t', ha='right', fontsize=8)
axs[1].set_xticks(range(1, 7), ['grade ' + g for g in GL], fontsize=8); axs[1].set_ylabel('WRI'); axs[1].set_title('(b) Dummy WRI by grade', fontsize=9.5)
plt.tight_layout(); plt.savefig(F + 'o1_wri.png', dpi=200); plt.close()
OUT['wri_best'] = [int(L1.flat[k_]), int(L2.flat[k_]), round(float(np.nanmax(BA)), 2)]

# ---------------- sensor features (dummy) ----------------
def f(mu, slope, sd, shape=1.0): return mu + slope * (s ** shape) + rng.normal(0, sd, n)
sens = {
 'HS': {'PSSRa': f(9.5, -8, 0.8, 0.8), 'REP (nm)': f(722, -20, 2.0, 0.7), 'WRI': wri, 'DWSI-1': f(2.6, -1.4, 0.18), 'PSRI': f(0.01, 0.12, 0.02), 'PRI': f(-0.02, -0.06, 0.012),
        'NDVI780': f(0.82, -0.25, 0.04), 'WI': f(1.06, -0.06, 0.015), 'RVSI': f(0.0, 0.0, 0.01), 'NPQI': f(0.02, 0.0, 0.01)},
 'MS': {'NDRE': f(0.42, -0.35, 0.04, 0.8), 'CIrededge': f(1.5, -1.6, 0.25, 0.8), 'PSRI_MS': f(0.02, 0.18, 0.025), 'MTCI': f(3.2, -2.2, 0.4), 'NDVI': f(0.85, -0.3, 0.05),
        'RE band': f(0.25, -0.06, 0.012), 'NIR band': f(0.46, -0.12, 0.03), 'CON_NIR': f(6, 10, 2.2), 'ENT_NIR': f(4.0, 1.2, 0.35), 'HOM_B': f(0.6, 0, 0.05), 'MEA_G': f(30, 0, 3)},
 'RGB': {'Contrast_G': f(8, 22, 3.5, 0.8), 'Entropy_G': f(4.2, 1.5, 0.35), 'Homogeneity_G': f(0.62, -0.25, 0.05), 'Dissimilarity_R': f(2.0, 3.2, 0.6), 'Hue': f(95, -40, 7),
         'Saturation': f(0.45, -0.18, 0.05), 'VF': f(0.92, -0.25, 0.05), 'CH (m)': f(1.45, -0.25, 0.1), 'Mean_B': f(60, 0, 6)},
 'TIR': {'CT (°C)': f(24, 3.5, 1.4), 'CTD (°C)': f(-3.0, 4.0, 0.9, 0.9), 'CTR': f(0.99, 0.012, 0.004), 'NRCT': f(0.35, 0.5, 0.12, 0.9), 'MTD (°C)': f(2.5, 3.0, 0.8),
         'CON_T': f(3, 6, 1.6), 'ENT_T': f(3.5, 0.8, 0.3), 'HOM_T': f(0.7, 0, 0.05)},
}
# extra SWIR disease indices (separate random stream so the other dummy values do not change)
rng2 = np.random.default_rng(77)
def f2(mu, slope, sd, shape=1.0): return mu + slope * (s ** shape) + rng2.normal(0, sd, n)
sens['HS'].update({'DWSI-5': f2(1.9, -0.9, 0.12, 0.8), 'NDWI': f2(0.06, -0.05, 0.012), 'MSI': f2(0.62, 0.20, 0.07), 'NDBI': f2(0.03, -0.035, 0.012), 'RBI (1068/1560)': f2(0.18, -0.06, 0.03)})

key3 = {'HS': ['PSSRa', 'REP (nm)', 'WRI'], 'MS': ['NDRE', 'PSRI_MS', 'CON_NIR'], 'RGB': ['Contrast_G', 'Hue', 'VF'], 'TIR': ['CTD (°C)', 'NRCT', 'MTD (°C)']}
cdaF = {'HS': ['PSSRa', 'REP (nm)', 'WRI', 'DWSI-1'], 'MS': ['NDRE', 'PSRI_MS', 'MTCI', 'CON_NIR'], 'RGB': ['Contrast_G', 'Hue', 'VF', 'Entropy_G'], 'TIR': ['CTD (°C)', 'NRCT', 'MTD (°C)', 'CON_T']}

def letters_for(vals):
    tk = pairwise_tukeyhsd(vals, cls); rej = {}
    for a1, b1, r in zip(tk._multicomp.pairindices[0], tk._multicomp.pairindices[1], tk.reject): rej[(min(a1, b1), max(a1, b1))] = r
    means = [vals[cls == k].mean() for k in range(6)]; order = list(np.argsort(means)); L = iter(string.ascii_lowercase); cur = next(L); lt = [''] * 6; lt[order[0]] = cur
    for q in range(1, 6):
        p_, c_ = order[q - 1], order[q]
        if rej[(min(p_, c_), max(p_, c_))]: cur = next(L)
        lt[c_] = cur
    return lt

def boruta_lite(Xs, y, runs=30):
    nfe = Xs.shape[1]; hits = np.zeros(nfe); imps = []
    for r in range(runs):
        sh = np.apply_along_axis(rng.permutation, 0, Xs); rf = RandomForestClassifier(200, random_state=r, n_jobs=-1).fit(np.column_stack([Xs, sh]), y)
        im = rf.feature_importances_; hits += im[:nfe] > im[nfe:].max(); imps.append(np.concatenate([im[:nfe], [im[nfe:].max()]]))
    p_hi = stats.binom.sf(hits - 1, runs, 0.5); p_lo = stats.binom.cdf(hits, runs, 0.5)
    status = ['Confirmed' if ph < 0.01 else ('Rejected' if pl < 0.01 else 'Tentative') for ph, pl in zip(p_hi, p_lo)]
    return np.array(imps), status

summary = {}
for sname, feats in sens.items():
    names_ = list(feats); M = np.column_stack([feats[k] for k in names_])
    fig, axs = plt.subplots(1, 3, figsize=(13.5, 4.3), gridspec_kw=dict(width_ratios=[1.6, 1.1, 1.2]))
    # (a) boxplots of three key features (normalised panels side by side)
    ax = axs[0]; ax.axis('off'); inner = ax.inset_axes([0, 0, 1, 1]); inner.axis('off')
    rows = []
    for q, fe in enumerate(key3[sname]):
        sub = ax.inset_axes([q * 0.345, 0.0, 0.31, 0.86]); vals = feats[fe]
        bp = sub.boxplot([vals[cls == k] for k in range(6)], tick_labels=GL, patch_artist=True, widths=0.6, showfliers=False)
        for pch, c in zip(bp['boxes'], GC): pch.set_facecolor(c); pch.set_alpha(0.65)
        Fv, pv = stats.f_oneway(*[vals[cls == k] for k in range(6)]); rv, _ = stats.pearsonr(vals, DI); lt = letters_for(vals)
        lo_, hi_ = sub.get_ylim(); sub.set_ylim(lo_, hi_ + 0.2 * (hi_ - lo_))
        for k in range(6): sub.text(k + 1, hi_ + 0.04 * (hi_ - lo_), lt[k], ha='center', fontsize=8, fontweight='bold')
        sub.set_title('%s\nF = %.0f, r = %.2f' % (fe, Fv, rv), fontsize=8.5); sub.tick_params(labelsize=7.5); sub.set_xlabel('grade', fontsize=7.5)
    for fe in names_:
        vals = feats[fe]; Fv, pv = stats.f_oneway(*[vals[cls == k] for k in range(6)]); rv, prv = stats.pearsonr(vals, DI)
        rows.append([fe, '%.0f' % Fv, '<0.001' if pv < 0.001 else '%.2f' % pv, '%.2f' % rv])
    ax.set_title('(a) Key features by grade (ANOVA F, Tukey letters, r with PDI)', fontsize=9.5, pad=14)
    # (b) CDA
    Xc = StandardScaler().fit_transform(np.column_stack([feats[k] for k in cdaF[sname]]))
    lda = LDA(n_components=2).fit(Xc, cls); Zs = lda.transform(Xc); ev = lda.explained_variance_ratio_
    Sw = sum(np.cov(Xc[cls == k].T) * ((cls == k).sum() - 1) for k in range(6)); St = np.cov(Xc.T) * (n - 1)
    eig = np.sort(np.real(np.linalg.eigvals(np.linalg.solve(Sw, St - Sw))))[::-1]; wilks = float(np.prod(1 / (1 + eig))); can = np.sqrt(eig / (1 + eig))
    acc = cross_val_score(LDA(), Xc, cls, cv=4).mean()
    ax = axs[1]
    for k in range(6):
        ax.scatter(Zs[cls == k, 0], Zs[cls == k, 1], s=6, color=GC[k], alpha=0.5, label='grade ' + GL[k]); ax.plot(Zs[cls == k, 0].mean(), Zs[cls == k, 1].mean(), 'X', color='black', ms=7)
    ax.set_xlabel('Canonical function 1 (%.0f%%)' % (100 * ev[0]), fontsize=8.5); ax.set_ylabel('Canonical function 2 (%.0f%%)' % (100 * ev[1]), fontsize=8.5)
    ax.legend(fontsize=6.5, markerscale=2, ncol=2); ax.tick_params(labelsize=7.5)
    ax.set_title('(b) CDA score plot (canonical r1 = %.2f)' % can[0], fontsize=9.5)
    # (c) Boruta
    imps, status = boruta_lite(M, cls)
    order = np.argsort(imps[:, :-1].mean(0)); scol = {'Confirmed': '#2E7D32', 'Tentative': '#F9A825', 'Rejected': '#C62828'}
    ax = axs[2]; data = [imps[:, -1]] + [imps[:, q] for q in order]
    bp = ax.boxplot(data, patch_artist=True, showfliers=False, widths=0.6, orientation='horizontal', medianprops=dict(color='black'))
    bp['boxes'][0].set_facecolor('#90A4AE')
    for pch, q in zip(bp['boxes'][1:], order): pch.set_facecolor(scol[status[q]])
    ax.set_yticks(range(1, len(data) + 1), ['shadowMax'] + [names_[q] for q in order], fontsize=7.5); ax.tick_params(axis='x', labelsize=7.5)
    ax.set_xlabel('RF importance', fontsize=8.5); ax.set_title('(c) Boruta (green confirmed, red rejected)', fontsize=9.5)
    fig.suptitle('Dummy data — %s sensor' % sname, fontsize=11, fontweight='bold', y=1.0)
    plt.tight_layout(); plt.savefig(F + 'o1_prof_%s.png' % sname, dpi=200, bbox_inches='tight'); plt.close()
    summary[sname] = {'anova': rows, 'cda': {'can': [round(float(x), 2) for x in can[:3]], 'wilks': round(wilks, 3), 'acc': round(float(acc), 2),
                      'coef': [[cdaF[sname][q], '%.2f' % lda.scalings_[q, 0]] for q in range(len(cdaF[sname]))], 'ev1': round(float(ev[0]) * 100)},
                      'boruta': [[names_[q], status[q]] for q in range(len(names_))]}
OUT['sensors'] = summary

# ---------------- MS 5-band and TIR panels ----------------
fig, axs = plt.subplots(1, 2, figsize=(11.5, 3.9))
bands = [475, 560, 668, 717, 840]; base = np.array([0.045, 0.12, 0.045, 0.25, 0.46]); dis = np.array([0.07, 0.15, 0.09, 0.24, 0.36])
for k, a_ in enumerate([0, 0.03, 0.08, 0.18, 0.38, 0.7]):
    axs[0].plot(bands, base + a_ / 0.7 * (dis - base), 'o-', color=GC[k], label='grade ' + GL[k])
axs[0].set_xticks(bands, ['B 475', 'G 560', 'R 668', 'RE 717', 'NIR 840']); axs[0].set_ylabel('Reflectance'); axs[0].legend(fontsize=7.5, ncol=2, frameon=False)
axs[0].set_title('(a) Dummy MS grade-mean reflectance (5 bands)', fontsize=9.5)
ct = sens['TIR']['CTD (°C)']
for k in range(6): axs[1].hist(ct[cls == k], bins=np.arange(-6, 4, 0.4), histtype='step', lw=1.6, color=GC[k], density=True, label='grade ' + GL[k])
axs[1].set_xlabel('CTD = CT − AT (°C)'); axs[1].set_ylabel('Density'); axs[1].legend(fontsize=7.5, ncol=2, frameon=False); axs[1].set_title('(b) Dummy canopy–air temperature difference by grade', fontsize=9.5)
plt.tight_layout(); plt.savefig(F + 'o1_ms_tir.png', dpi=200); plt.close()

fig, ax = plt.subplots(figsize=(6.4, 4.2))
rwc = 85 - 3 * rng.random(n) - 0.5 * np.where(cls == 5, 0, 0) + rng.normal(0, 2, n)
sc = ax.scatter(sens['TIR']['CTD (°C)'], rwc, c=[GC[k] for k in cls], s=10, alpha=0.7)
ax.set_xlabel('CTD (°C)'); ax.set_ylabel('Relative water content (%)'); r_, p_ = stats.pearsonr(sens['TIR']['CTD (°C)'], rwc)
ax.set_title('Dummy thermal–water check: CTD rises with grade\nwhile RWC stays uniform (r = %.2f)' % r_, fontsize=9.5)
plt.tight_layout(); plt.savefig(F + 'o1_tir_check.png', dpi=200); plt.close()
OUT['tir_check_r'] = round(float(r_), 2)

# ---------------- cross-sensor ----------------
dsf = {'HS': ['PSSRa', 'REP (nm)', 'WRI', 'DWSI-1'], 'MS': ['NDRE', 'PSRI_MS', 'CON_NIR'], 'RGB': ['Contrast_G', 'Hue', 'VF'], 'TIR': ['CTD (°C)', 'NRCT', 'MTD (°C)']}
labs = []; cols_ = []
for k_, v in dsf.items():
    for fe in v: labs.append('%s (%s)' % (fe, k_)); cols_.append(sens[k_][fe])
Cm = np.corrcoef(np.column_stack(cols_).T)
fig, ax = plt.subplots(figsize=(8, 6.6)); im = ax.imshow(Cm, cmap='RdBu_r', vmin=-1, vmax=1)
for i in range(len(labs)):
    for j in range(len(labs)): ax.text(j, i, '%.1f' % Cm[i, j], ha='center', va='center', fontsize=6.8)
ax.set_xticks(range(len(labs)), labs, rotation=60, ha='right', fontsize=7.5); ax.set_yticks(range(len(labs)), labs, fontsize=7.5)
plt.colorbar(im, label='Pearson r'); ax.set_title('Dummy correlation between DSFs of the four sensors', fontsize=10)
plt.tight_layout(); plt.savefig(F + 'o1_xcorr.png', dpi=200); plt.close()
Xall = StandardScaler().fit_transform(np.column_stack(cols_))
lda = LDA().fit(Xall, cls); ev = lda.explained_variance_ratio_
Sw = sum(np.cov(Xall[cls == k].T) * ((cls == k).sum() - 1) for k in range(6)); St = np.cov(Xall.T) * (n - 1)
eig = np.sort(np.real(np.linalg.eigvals(np.linalg.solve(Sw, St - Sw))))[::-1]; can = np.sqrt(eig / (1 + eig))
OUT['combined'] = {'can1': round(float(can[0]), 2), 'acc': round(float(cross_val_score(LDA(), Xall, cls, cv=4).mean()), 2)}
OUT['counts'] = counts
json.dump(OUT, open(D + 'o1_dummy.json', 'w'), indent=1, default=lambda o: o.item())
print(json.dumps({k: (v if k != 'sensors' else {s_: {'cda': v[s_]['cda']} for s_ in v}) for k, v in OUT.items()}, default=lambda o: o.item())[:2500])
