"""Presentation-quality figures for the 2025-26 ASD leaf analysis (PNG, 300 dpi, Liberation Sans = Arial metrics).
Run:  python3 a6_figs.py        (all figures)      python3 a6_figs.py obj1   (Objective 1 only)"""
import numpy as np, pandas as pd, os, json, sys
import matplotlib; matplotlib.use('Agg'); import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from matplotlib.patches import FancyBboxPatch, Ellipse, Patch
from matplotlib.lines import Line2D
B = os.path.dirname(os.path.abspath(__file__)) + '/'; D = B + 'data/'; FG = B + 'fig/'; os.makedirs(FG, exist_ok=True)
# ---------------- one style for every figure ----------------
plt.rcParams.update({'font.family': 'Liberation Sans', 'font.size': 12, 'axes.titlesize': 13, 'axes.titleweight': 'bold', 'axes.titlelocation': 'left', 'axes.titlepad': 9,
                     'axes.labelsize': 12, 'xtick.labelsize': 11, 'ytick.labelsize': 11, 'legend.fontsize': 10, 'legend.frameon': False, 'legend.title_fontsize': 10.5,
                     'axes.spines.top': False, 'axes.spines.right': False, 'axes.edgecolor': '#4D4D4D', 'axes.linewidth': 0.9, 'xtick.color': '#333333', 'ytick.color': '#333333',
                     'axes.labelcolor': '#1A1A1A', 'axes.titlecolor': '#1B2A1E', 'lines.linewidth': 1.8, 'axes.grid': True, 'grid.color': '#E6E6E6', 'grid.linewidth': 0.7,
                     'axes.axisbelow': True, 'figure.facecolor': 'white', 'savefig.facecolor': 'white', 'mathtext.fontset': 'custom', 'mathtext.rm': 'Liberation Sans',
                     'mathtext.it': 'Liberation Sans:italic', 'mathtext.bf': 'Liberation Sans:bold', 'mathtext.default': 'regular', 'xtick.major.size': 4, 'ytick.major.size': 4})
GR = [0, 1, 3, 5, 7, 9]; GC = ['#1A9850', '#91CF60', '#E0B000', '#F46D43', '#D73027', '#762A83']
ML_C, DL_C, R_C, FD_C, IDX_C, GREY = '#2E75B6', '#7030A0', '#1565C0', '#C62828', '#2E7D32', '#9E9E9E'
FDU = 'First derivative ($\\times10^{-3}$ nm$^{-1}$)'
P = np.load(D + 'prep.npz'); wl, w5, R5, FD5 = P['wl'], P['w5'], P['R5'], P['FD5']
M = pd.read_csv(D + 'meta.csv'); O1 = json.load(open(D + 'o1_results.json')); F = pd.read_csv(D + 'indices_full.csv')
def save(fig, n): fig.savefig(FG + n, dpi=300, bbox_inches='tight', pad_inches=0.08); plt.close(fig); print('  ', n)
WB = [(1350, 1460), (1790, 1960)]
REG = [(400, 680, 'VIS'), (680, 750, 'RE'), (750, 1300, 'NIR'), (1300, 1900, 'SWIR-1'), (1900, 2400, 'SWIR-2')]
def regions(ax, lo=400, hi=2400, water=True):
    """Spectral-region labels above the axes and shaded water-absorption bands (kept in the analysis)."""
    for a, b, t in REG:
        if b <= lo or a >= hi: continue
        ax.text((max(a, lo) + min(b, hi)) / 2, 1.005, t, transform=ax.get_xaxis_transform(), ha='center', va='bottom', fontsize=9.5, color='#555555')
        if a > lo: ax.axvline(a, color='#BDBDBD', lw=0.7, ls=(0, (3, 3)), zorder=0)
    if water:
        for a, b in WB:
            if a < hi and b > lo:
                ax.axvspan(a, b, color='#DCEBFA', alpha=0.7, lw=0, zorder=0)
                ax.text((a + b) / 2, 0.97, 'H₂O', transform=ax.get_xaxis_transform(), ha='center', va='top', fontsize=8.5, color='#1565C0')
    ax.set_xlim(lo, hi)
def grade_legend(fig_or_ax, ncol=6, loc='lower center', bbox=(0.5, -0.02), counts=True, **kw):
    h = [Line2D([], [], color=c, lw=3) for c in GC]; l = ['grade %d (n = %d)' % (g, (M.grade == g).sum()) if counts else 'grade %d' % g for g in GR]
    return fig_or_ax.legend(h, l, ncol=ncol, loc=loc, bbox_to_anchor=bbox, handlelength=1.6, columnspacing=1.4, **kw)
def label_bars(ax, bars, fmt='%.2f', fs=9.5, horiz=False):
    for b in bars:
        v = b.get_width() if horiz else b.get_height()
        if not np.isfinite(v): continue
        if horiz: ax.text(b.get_x() + v + 0.005 * ax.get_xlim()[1], b.get_y() + b.get_height() / 2, fmt % v, va='center', ha='left', fontsize=fs, color='#222')
        else: ax.text(b.get_x() + b.get_width() / 2, v, fmt % v, ha='center', va='bottom', fontsize=fs, color='#222')
def mname(m, t): return {'SVM': 'SVR', 'PLS': 'PLSR'}.get(m, m) if t == 'C' else m
def nospine(ax):
    for s in ax.spines.values(): s.set_visible(False)

# ---------------- F00 workflow (snake layout) ----------------
def box(ax, x, y, w, h, t, b, c, fc):
    ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle='round,pad=0.012,rounding_size=0.08', fc=fc, ec=c, lw=1.6))
    ax.text(x + w / 2, y + h - 0.13, t, ha='center', va='top', fontsize=11.5, fontweight='bold', color=c)
    ax.text(x + w / 2, y + h - 0.5, b, ha='center', va='top', fontsize=9.8, linespacing=1.35, color='#1A1A1A')
PH = {'c': ('#2C5F2D', '#EEF3E8', 'Data collection and quality control'), 'd': ('#1F3864', '#EEF1F6', 'Pre-processing and features'), 'o1': ('#1F6FB2', '#DEEBF7', 'Objective 1: spectral response and feature selection'),
      'v': ('#A87400', '#FFF4D6', 'Validation design'), 'o2': ('#6A2C9A', '#EDE2F6', 'Objective 2: machine and deep learning'), 'i': ('#B71C1C', '#F9E0DE', 'Covariate baseline, interpretation and discussion')}
steps = [('1. Field experiment', '48 plots: sprayed healthy\nblock + R1–R3 unsprayed\n(natural infection); 3 V × 4 D', 'c'),
         ('2. Leaf spectra + scores', 'ASD contact probe, 4 dates\n(11 Feb–13 Mar), %d leaves;\nL3, L5, LL; grade 0–9' % len(M), 'c'),
         ('3. Weather + covariates', 'IARI daily weather; 7-day\nwindows (no look-ahead);\nfavourable days; DAS, stage', 'c'),
         ('4. Organisation + QC', 'parse files, join layout,\nlabels; range, missing-\nvalue and plot checks', 'c'),
         ('5. Pre-processing', '400–2400 nm, water bands\nkept (splice-corrected);\nSavitzky–Golay; derivative', 'd'),
         ('6. Features', 'reflectance + derivative\n(5 nm); 41 indices +\n3 red-edge parameters', 'd'),
         ('7. Response analysis', 'mean spectra, derivative\nand correlation curves\nby severity grade', 'o1'),
         ('8. Optimal wavelengths', 'NDSI/RSI R² maps →\neffective ranges →\nSHAP-CARS', 'o1'),
         ('9. Index selection', 'best NDSI, RSI, WRI;\n|r| ≥ 0.95 filter →\nReliefF / RReliefF', 'o1'),
         ('10. Feature set', 'variance inflation\nfactor < 10 → disease-\nspecific feature set', 'o1'),
         ('11. Validation', 'leave-one-replication-\nout (healthy plots\nrotated); inner by plot', 'v'),
         ('12. Machine learning', 'SVM, RF, XGBoost, k-NN,\nPLS; floating forward\nselection; grid search', 'o2'),
         ('13. Deep learning', 'DNN-F1, DT-EDNet,\nEfficientNet-B0, ResNet18,\nConvNeXt V2-Atto', 'o2'),
         ('14. Evaluation', 'OA, kappa, macro-F1,\nweighted kappa, AUC;\nR², RMSE, RPD', 'o2'),
         ('15. Covariate baseline', 'no-sensor models vs\nspectra vs both; plot\nbootstrap, DeLong; SHAP', 'i'),
         ('16. Discussion', 'physical basis, grade\noverlap, ML vs DL,\nlimitations, UAV phase', 'i')]
fig, ax = plt.subplots(figsize=(13, 8.4)); ax.set_xlim(0, 13); ax.set_ylim(0, 8.4); ax.axis('off')
bw, bh, gx, X0 = 2.75, 1.45, 3.25, 0.25; pos = []
for i in range(16):
    r, k = divmod(i, 4); k = k if r % 2 == 0 else 3 - k; pos.append((X0 + k * gx, 6.75 - r * 2.05))
for i, (t, b, ph) in enumerate(steps):
    x, y = pos[i]; c, fc, _ = PH[ph]; box(ax, x, y, bw, bh, t, b, c, fc)
    if i < 15:
        x2, y2 = pos[i + 1]; ap = dict(arrowstyle='-|>', color='#555', lw=1.6, mutation_scale=16)
        if y2 == y:
            xa, xb = (x + bw, x2) if x2 > x else (x, x2 + bw); ax.annotate('', xy=(xb, y + bh / 2), xytext=(xa, y + bh / 2), arrowprops=ap)
        else: ax.annotate('', xy=(x + bw / 2, y2 + bh), xytext=(x + bw / 2, y), arrowprops=ap)
ax.legend([Patch(fc=v[1], ec=v[0], lw=1.5) for v in PH.values()], [v[2] for v in PH.values()], loc='lower center', bbox_to_anchor=(0.5, -0.06), ncol=3, fontsize=10.5, handlelength=1.4)
save(fig, 'f00_workflow.png')

# ---------------- F01 dataset ----------------
fig, axs = plt.subplots(2, 2, figsize=(12, 8.2))
for ax, fac, ttl in zip(axs.ravel(), ['date', 'stage', 'variety', 'leaf'], ['(a) Sampling date (crop age, days after sowing)', '(b) Growth stage', '(c) Variety', '(d) Leaf position']):
    c = pd.crosstab(M[fac], M.grade); bottom = np.zeros(len(c))
    for g, col in zip(GR, GC): ax.bar(range(len(c)), c[g], bottom=bottom, color=col, width=0.62, edgecolor='white', lw=0.6); bottom += c[g].values
    for i, v in enumerate(bottom): ax.text(i, v + bottom.max() * 0.015, 'n = %d' % v, ha='center', va='bottom', fontsize=10, color='#222')
    lab = list(c.index)
    if fac == 'date': lab = ['%s\n(%d–%d DAS)' % (pd.Timestamp(d).strftime('%d %b'), M[M.date == d].DAS.min(), M[M.date == d].DAS.max()) for d in c.index]
    ax.set_xticks(range(len(c))); ax.set_xticklabels(lab); ax.set_title(ttl); ax.set_ylabel('Number of leaves'); ax.set_ylim(0, bottom.max() * 1.12); ax.grid(axis='x', visible=False)
grade_legend(fig, bbox=(0.5, -0.035)); plt.tight_layout(rect=(0, 0.03, 1, 1)); save(fig, 'f01_dataset.png')

# ---------------- F02 mean spectra and derivative, F03 full derivative ----------------
ms = pd.read_csv(D + 'o1_mean_spectra.csv'); fs = pd.read_csv(D + 'o1_mean_fd.csv')
fig, axs = plt.subplots(1, 2, figsize=(13, 5.2), gridspec_kw={'width_ratios': [1.45, 1]})
for g, c in zip(GR, GC): axs[0].fill_between(ms.wl, ms['mean_%d' % g] - ms['sd_%d' % g], ms['mean_%d' % g] + ms['sd_%d' % g], color=c, alpha=0.07, lw=0)
sel = (fs.wl >= 500) & (fs.wl <= 800)
for g, c in zip(GR, GC): axs[0].plot(ms.wl, ms['mean_%d' % g], color=c, lw=1.9); axs[1].plot(fs.wl[sel], fs['mean_%d' % g][sel], color=c, lw=2)
regions(axs[0]); axs[0].set(xlabel='Wavelength (nm)', ylabel='Reflectance'); axs[0].set_title('(a) Mean leaf reflectance (± SD band) by severity grade', pad=22)
regions(axs[1], 500, 800, water=False); axs[1].set(xlabel='Wavelength (nm)', ylabel=FDU); axs[1].set_title('(b) First derivative, 500–800 nm', pad=22)
grade_legend(fig, bbox=(0.5, -0.06)); plt.tight_layout(rect=(0, 0.04, 1, 1)); save(fig, 'f02_mean_spectra.png')
fig, ax = plt.subplots(figsize=(13, 4.6))
for g, c in zip(GR, GC): ax.plot(fs.wl, fs['mean_%d' % g], color=c, lw=1.4)
regions(ax); ax.axhline(0, color='#555', lw=0.7); ax.set(xlabel='Wavelength (nm)', ylabel=FDU); ax.set_title('First derivative of the mean leaf spectra, 400–2400 nm (water bands kept)', pad=22)
grade_legend(ax, bbox=(0.5, -0.32)); save(fig, 'f03_fd_full.png')

# ---------------- F04 correlation curves ----------------
cc = pd.read_csv(D + 'o1_corr_curves.csv')
fig, ax = plt.subplots(figsize=(13, 4.8)); ax.plot(cc.wl, cc.r_R, color=R_C, lw=2, label='Reflectance'); ax.plot(cc.wl, cc.r_FD, color=FD_C, lw=1.4, label='First derivative')
ax.axhline(0, color='#333', lw=0.8); regions(ax)
for v in (0.3, -0.3): ax.axhline(v, color='#757575', ls=':', lw=1)
for col, c in (('r_R', R_C), ('r_FD', FD_C)):
    i = cc[col].abs().idxmax(); ax.plot(cc.wl[i], cc[col][i], 'o', ms=8, mfc='white', mec=c, mew=2)
    ax.annotate('%d nm, r = %.2f' % (cc.wl[i], cc[col][i]), (cc.wl[i], cc[col][i]), xytext=(12, -14 if cc[col][i] < 0 else 8), textcoords='offset points', fontsize=10, color=c, fontweight='bold')
ax.set(xlabel='Wavelength (nm)', ylabel='Pearson r with leaf grade'); ax.set_title('Correlation of reflectance and first derivative with leaf severity grade (n = %d leaves)' % len(M), pad=22)
ax.legend(loc='lower right', ncol=2); save(fig, 'f04_corr_curves.png')

# ---------------- F05 NDSI / RSI maps ----------------
Nm = np.load(D + 'o1_ndsi_r2.npy'); Sm = np.load(D + 'o1_rsi_r2.npy')
fig, axs = plt.subplots(1, 2, figsize=(13, 5.8))
for ax, Mp, ttl, bp in zip(axs, (Nm, Sm), ('(a) NDSI(λ₁, λ₂)', '(b) RSI(λ₁, λ₂)'), (O1['best_ndsi'], O1['best_rsi'])):
    A = np.where(np.isfinite(Mp), Mp, np.nan); A = np.fmax(A, A.T); ax.grid(False)
    im = ax.imshow(A, origin='lower', extent=[w5[0], w5[-1], w5[0], w5[-1]], cmap='turbo', vmin=0, vmax=np.nanmax(A), interpolation='nearest')
    cb = plt.colorbar(im, ax=ax, fraction=0.046, pad=0.03); cb.set_label('R² with leaf grade'); cb.outline.set_visible(False)
    ax.contour(w5, w5, A, levels=[O1['eff_thr']], colors='white', linewidths=0.8)
    ax.plot(bp[0], bp[1], marker='*', color='white', ms=17, mec='black', mew=1.2)
    ax.annotate('best (%d, %d) nm\nR² = %.2f' % (bp[0], bp[1], bp[2]), (bp[0], bp[1]), xytext=(1150, 600), fontsize=10.5, fontweight='bold', color='white',
                bbox=dict(boxstyle='round,pad=0.3', fc='black', alpha=0.6, ec='none'), arrowprops=dict(arrowstyle='-', color='white', lw=1))
    ax.set(xlabel='λ₁ (nm)', ylabel='λ₂ (nm)'); ax.set_title(ttl); ax.set_xticks(range(500, 2401, 500)); ax.set_yticks(range(500, 2401, 500))
fig.text(0.5, -0.01, 'White contour: effective-range threshold (R² = %.2f, top 5%% of band pairs)' % O1['eff_thr'], ha='center', fontsize=10.5, color='#444')
plt.tight_layout(); save(fig, 'f05_ndsi_rsi_maps.png')

# ---------------- F06 SHAP-CARS, F07 optimal wavelengths ----------------
sa = pd.read_csv(D + 'o1_shap_all.csv'); sc = pd.read_csv(D + 'o1_shapcars.csv'); ch = pd.read_csv(D + 'o1_cars_hist.csv'); mc = pd.read_csv(D + 'o1_mccv.csv')
sa['type'] = sa.feature.str.extract(r'^([A-Z]+)'); sa['w'] = sa.feature.str.extract(r'(\d+)').astype(int)
thr = np.sort(sa.mean_abs_shap.values)[::-1][len(sc) - 1]
fig, axs = plt.subplots(2, 2, figsize=(13, 9))
for t, c in (('R', R_C), ('FD', FD_C)):
    d = sa[sa.type == t]; axs[0, 0].bar(d.w, d.mean_abs_shap, width=4.5, color=c, alpha=.85, label='Reflectance' if t == 'R' else 'First derivative')
axs[0, 0].axhline(thr, color='k', ls='--', lw=1); axs[0, 0].text(2390, thr, 'top 40% kept', ha='right', va='bottom', fontsize=10)
axs[0, 0].set(xlabel='Wavelength (nm)', ylabel='mean |SHAP|', xlim=(400, 2400)); axs[0, 0].set_title('(a) Shapley pre-screening of all bands'); axs[0, 0].legend(loc='upper right')
axs[0, 1].plot(mc.ncomp, mc.rmse, 'o-', color=DL_C, ms=6, lw=1.8); axs[0, 1].axvline(O1['cars_ncomp'], color=FD_C, ls='--', lw=1.2)
axs[0, 1].set(xlabel='Number of PLS components', ylabel='RMSE (Monte Carlo CV, 50 splits)'); axs[0, 1].set_title('(b) PLS components chosen = %d' % O1['cars_ncomp'])
axs[1, 0].plot(ch.iteration, ch.n_vars, color='#333', lw=1.8); ax2 = axs[1, 0].twinx(); ax2.plot(ch.iteration, ch.rmsecv, color=FD_C, lw=1.8); bi = ch.rmsecv.idxmin()
ax2.axvline(ch.iteration[bi], color=FD_C, ls=':', lw=1.2); ax2.spines['right'].set_visible(True); ax2.grid(False); ax2.set_ylabel('RMSECV', color=FD_C); ax2.tick_params(axis='y', colors=FD_C)
axs[1, 0].set(xlabel='CARS iteration', ylabel='Variables kept'); axs[1, 0].set_title('(c) CARS run 1: variables kept (black) and RMSECV (red)')
f = sc[sc.cars_freq > 0].sort_values('cars_freq', ascending=False).head(22)
axs[1, 1].bar(range(len(f)), f.cars_freq, color=[FD_C if x.startswith('FD') else R_C for x in f.feature], width=0.7)
axs[1, 1].axhline(0.5, color='k', ls='--', lw=1); axs[1, 1].set_xticks(range(len(f))); axs[1, 1].set_xticklabels(f.feature, rotation=90, fontsize=9.5)
axs[1, 1].set(ylabel='Selection frequency (20 runs)', ylim=(0, 1.05)); axs[1, 1].set_title('(d) Stability of CARS selection (≥ 0.5 kept)'); axs[1, 1].grid(axis='x', visible=False)
plt.tight_layout(); save(fig, 'f06_shapcars.png')
fig, axs = plt.subplots(1, 2, figsize=(13, 4.8)); mean_all = R5.mean(0); fd_all = FD5.mean(0) * 1000
axs[0].plot(w5, mean_all, color=IDX_C, lw=2); axs[1].plot(w5, fd_all, color=IDX_C, lw=1.6); regions(axs[0]); regions(axs[1])
for n in O1['OW']:
    w = int(n.lstrip('RFD')); a = axs[0] if n.startswith('R') else axs[1]; c = FD_C if n.startswith('FD') else R_C
    a.axvline(w, color=c, lw=1.4, alpha=.85); a.text(w, 0.92, str(w), transform=a.get_xaxis_transform(), rotation=90, fontsize=8, color=c, ha='right', va='top')
axs[0].set(xlabel='Wavelength (nm)', ylabel='Reflectance'); axs[0].set_title('(a) Optimal wavelengths on reflectance (%d)' % O1['OW_n_R'], pad=22)
axs[1].set(xlabel='Wavelength (nm)', ylabel=FDU); axs[1].set_title('(b) Optimal wavelengths on first derivative (%d)' % O1['OW_n_FD'], pad=22)
plt.tight_layout(); save(fig, 'f07_optimal_wavelengths.png')

# ---------------- F08 WRI ----------------
W = O1['WRI']; fig, axs = plt.subplots(1, 2, figsize=(13, 5))
data = [F.WRI[M.grade == g].values for g in GR]
vp = axs[0].violinplot(data, positions=range(6), showextrema=False, widths=0.8)
for b, c in zip(vp['bodies'], GC): b.set_facecolor(c); b.set_alpha(0.35); b.set_edgecolor('none')
bp = axs[0].boxplot(data, positions=range(6), widths=0.25, patch_artist=True, showfliers=False, medianprops=dict(color='k', lw=1.6))
for p_, c in zip(bp['boxes'], GC): p_.set_facecolor(c); p_.set_edgecolor('#333')
axs[0].set_xticks(range(6)); axs[0].set_xticklabels(GR); axs[0].set(xlabel='Leaf severity grade', ylabel='White Rust Index'); axs[0].set_title('(a) WRI distribution by grade'); axs[0].grid(axis='x', visible=False)
jit = M.grade + np.random.default_rng(0).uniform(-0.3, 0.3, len(M)); axs[1].scatter(jit, F.WRI, s=7, c=[GC[GR.index(g)] for g in M.grade], alpha=.45, lw=0)
mm = F.WRI.groupby(M.grade).mean(); sd = F.WRI.groupby(M.grade).std(); axs[1].errorbar(mm.index, mm.values, yerr=sd.values, fmt='o-', color='k', ms=6, capsize=4, lw=1.5, label='mean ± SD')
axs[1].set(xlabel='Leaf severity grade (jittered)', ylabel='White Rust Index'); axs[1].set_xticks(GR); axs[1].set_title('(b) WRI vs grade, r = %.2f' % W['r']); axs[1].legend(loc='upper right')
fig.suptitle('White Rust Index = NDSI(%d, %d) %+0.1f × R%d' % (W['l1'], W['l2'], W['w'], W['l3']), fontsize=13.5, fontweight='bold', color='#1B2A1E', y=1.02); plt.tight_layout(); save(fig, 'f08_wri.png')

# ---------------- F09 index correlation, F10 ReliefF, F11 VIF, F12 PCA ----------------
ic = pd.read_csv(D + 'o1_index_corr.csv', index_col=0); n = len(ic); mask = np.triu(np.ones((n, n), bool), 1); A = np.where(mask, np.nan, ic.values)
fig, ax = plt.subplots(figsize=(10.5, 9)); ax.grid(False); im = ax.imshow(A, cmap='RdBu_r', vmin=-1, vmax=1)
for i in range(n):
    for j in range(i):
        ax.text(j, i, '%.1f' % ic.values[i, j], ha='center', va='center', fontsize=7, color='white' if abs(ic.values[i, j]) > 0.7 else '#222')
ax.set_xticks(range(n)); ax.set_xticklabels(ic.columns, rotation=90, fontsize=10); ax.set_yticks(range(n)); ax.set_yticklabels(ic.index, fontsize=10); nospine(ax)
cb = plt.colorbar(im, fraction=0.04, pad=0.02); cb.set_label('Pearson r'); cb.outline.set_visible(False)
ax.set_title('Correlation among indices kept after the |r| ≥ 0.95 redundancy filter (%d indices)' % n); save(fig, 'f09_index_corr.png')
rl = pd.read_csv(D + 'o1_relief.csv'); fig, axs = plt.subplots(1, 3, figsize=(14, 5.6))
for ax, col, ttl in zip(axs, ['ReliefF_binary', 'ReliefF_classes', 'RReliefF_score'], ['(a) ReliefF: detection', '(b) ReliefF: six grades', '(c) RReliefF: severity score']):
    d = rl.sort_values(col).tail(15); cols = [ML_C if i >= len(d) - 5 else '#C5CAE9' for i in range(len(d))]
    ax.barh(d['index'], d[col], color=cols, height=0.7); ax.set_title(ttl); ax.set_xlabel('ReliefF weight'); ax.tick_params(axis='y', labelsize=10); ax.grid(axis='y', visible=False)
fig.legend([Patch(color=ML_C), Patch(color='#C5CAE9')], ['top 5 (selected)', 'next 10'], loc='lower center', ncol=2, bbox_to_anchor=(0.5, -0.04))
plt.tight_layout(rect=(0, 0.04, 1, 1)); save(fig, 'f10_relief.png')
vf = pd.Series(O1['VIF_final']).sort_values(); fig, ax = plt.subplots(figsize=(9, 5))
bars = ax.barh(vf.index, vf.values, color=[FD_C if k.startswith('FD') else IDX_C for k in vf.index], height=0.65)
ax.set(xlabel='Variance inflation factor', xlim=(0, max(11.5, vf.max() * 1.15))); label_bars(ax, bars, '%.1f', horiz=True, fs=10)
ax.axvline(10, color='k', ls='--', lw=1.2); ax.text(10, len(vf) - 0.4, ' VIF = 10', fontsize=10, va='center'); ax.grid(axis='y', visible=False)
ax.legend([Patch(color=FD_C), Patch(color=IDX_C)], ['optimal derivative band', 'vegetation index'], loc='lower right'); ax.set_title('Disease-specific feature set (%d features) after VIF < 10' % len(vf)); save(fig, 'f11_vif.png')
pc = pd.read_csv(D + 'o1_pca.csv'); fig, ax = plt.subplots(figsize=(8.5, 7))
for g, c in zip(GR, GC):
    d = pc[pc.grade == g]; ax.scatter(d.PC1, d.PC2, s=9, color=c, alpha=.4, lw=0)
    ev, evec = np.linalg.eigh(np.cov(d.PC1, d.PC2)); ang = np.degrees(np.arctan2(evec[1, 1], evec[0, 1])); wd, ht = 2 * np.sqrt(5.991 * ev[::-1])
    ax.add_patch(Ellipse((d.PC1.mean(), d.PC2.mean()), wd, ht, angle=ang, fc='none', ec=c, lw=2.2)); ax.plot(d.PC1.mean(), d.PC2.mean(), 'o', color=c, mec='k', ms=9)
ax.set(xlabel='PC1 (%.1f%% of variance)' % (100 * O1['pca_var'][0]), ylabel='PC2 (%.1f%% of variance)' % (100 * O1['pca_var'][1])); ax.set_title('PCA scores of leaf reflectance with 95% ellipses')
grade_legend(ax, ncol=3, bbox=(0.5, -0.27), counts=False); save(fig, 'f12_pca.png')

# ---------------- F13 spectra by stage, F14 grade by factor ----------------
fig, axs = plt.subplots(1, 3, figsize=(14, 4.9), sharey=True)
for ax, stg in zip(axs, ['Vegetative', 'Flowering', 'Pod formation']):
    for g, c in zip(GR, GC):
        m = (M.stage == stg) & (M.grade == g)
        if m.sum() > 5: ax.plot(w5, R5[m.values].mean(0), color=c, lw=1.6)
    regions(ax); ax.set_title('%s (n = %d)' % (stg, (M.stage == stg).sum()), pad=22); ax.set_xlabel('Wavelength (nm)'); ax.set_xticks([500, 1000, 1500, 2000])
axs[0].set_ylabel('Reflectance'); grade_legend(fig, bbox=(0.5, -0.07), counts=False); plt.tight_layout(rect=(0, 0.04, 1, 1)); save(fig, 'f13_spectra_by_stage.png')
fig, axs = plt.subplots(2, 2, figsize=(12, 8))
for ax, fac, ttl in zip(axs.ravel(), ['stage', 'variety', 'leaf', 'timing'], ['(a) Growth stage', '(b) Variety', '(c) Leaf position', '(d) Sowing timing (D1–D4 = 50, 40, 30, 20 DAS)']):
    g = M.groupby(fac).grade.agg(['mean', 'sem', 'size'])
    ax.bar(range(len(g)), g['mean'], yerr=1.96 * g['sem'], color='#5B8DB8', capsize=5, width=0.6, error_kw=dict(lw=1.3))
    for i, (v, nn) in enumerate(zip(g['mean'], g['size'])): ax.text(i, v / 2, '%.2f\nn = %d' % (v, nn), ha='center', va='center', fontsize=10, color='white', fontweight='bold')
    ax.set_xticks(range(len(g))); ax.set_xticklabels(g.index); ax.set_ylabel('Mean leaf grade (± 95% CI)'); ax.set_title(ttl); ax.grid(axis='x', visible=False)
plt.tight_layout(); save(fig, 'f14_grade_by_factor.png')

# ---------------- F15 weather and disease progress ----------------
if os.path.exists(D + 'weather_season.csv'):
    Wd = pd.read_csv(D + 'weather_season.csv', parse_dates=['date']); pr = pd.read_csv(D + 'disease_progress.csv', parse_dates=['date'])
    Wd = Wd[(Wd.date >= '2025-12-01') & (Wd.date <= '2026-03-20')]
    SOW = ['2025-12-09', '2025-12-18', '2025-12-27', '2026-01-09']
    fig, (ax, axr) = plt.subplots(2, 1, figsize=(13, 7.6), sharex=True, gridspec_kw={'height_ratios': [1.3, 1]})
    ax.axhspan(16, 24, color='#E8F5E9', alpha=0.8, lw=0, zorder=0, label='favourable T (16–24 °C)')
    ax.fill_between(Wd.date, Wd.Tmin, Wd.Tmax, color='#FFCDD2', alpha=0.45, lw=0); ax.plot(Wd.date, Wd.Tmax, color='#C62828', lw=1.8, label='T max'); ax.plot(Wd.date, Wd.Tmin, color='#1565C0', lw=1.8, label='T min')
    ax.set_ylabel('Temperature (°C)'); ax.set_ylim(-2, 40)
    axr.bar(Wd.date, Wd.rain, color='#64B5F6', width=0.8, label='rainfall (mm)'); axr2 = axr.twinx()
    axr2.plot(Wd.date, Wd.RH1, color='#37474F', lw=1.4, label='RH I (morning)'); axr2.plot(Wd.date, Wd.RH2, color='#90A4AE', lw=1.4, label='RH II (afternoon)')
    axr2.spines['right'].set_visible(True); axr2.grid(False); axr2.set_ylabel('Relative humidity (%)'); axr2.set_ylim(0, 128); axr2.set_yticks([0, 20, 40, 60, 80, 100]); axr.set_ylim(0, Wd.rain.max() * 1.3); axr.set_ylabel('Rainfall (mm)')
    for a in (ax, axr):
        for dt in SOW: a.axvline(pd.Timestamp(dt), color='#2E7D32', lw=1, ls=':')
        for d_ in pr.date: a.axvline(d_, color='#7B1FA2', lw=1.2, alpha=.6)
    fv = Wd[(Wd.Tmax.between(16, 24)) & (Wd.RH1 > 97) & (Wd.RH2 > 40)]
    ax.plot(fv.date, np.full(len(fv), 34.5), 'v', color='#2E7D32', ms=8, label='favourable leaf-infection day*')
    for lab, dt in zip(['D1', 'D2', 'D3', 'D4'], SOW): ax.text(pd.Timestamp(dt), 39, ' ' + lab, fontsize=10, color='#2E7D32', va='top', fontweight='bold')
    for _, r in pr.iterrows():
        ax.text(r.date, -1, '%s\ngrade %.1f\n%d%% dis.' % (r.date.strftime('%d %b'), r.mean_grade, r.pct_diseased), ha='center', va='bottom', fontsize=8.8,
                color='#4A148C', fontweight='bold', bbox=dict(fc='white', ec='#CE93D8', boxstyle='round,pad=0.2', alpha=0.92))
    ax.legend(loc='upper left', ncol=3, bbox_to_anchor=(0.0, 0.88), fontsize=9.5)
    h1, l1 = axr.get_legend_handles_labels(); h2, l2 = axr2.get_legend_handles_labels(); axr.legend(h1 + h2, l1 + l2, loc='upper left', ncol=3, fontsize=9.5, bbox_to_anchor=(0, 1.02))
    ax.set_title('(a) Temperature, sowing dates (D1–D4), favourable days and leaf sampling dates (purple); natural infection'); axr.set_title('(b) Rainfall and relative humidity (IARI agro-meteorological observatory)')
    axr.xaxis.set_major_locator(mdates.WeekdayLocator(byweekday=0, interval=2)); axr.xaxis.set_major_formatter(mdates.DateFormatter('%d %b'))
    fig.text(0.01, -0.01, '* T max 16–24 °C, RH I > 97% and RH II > 40% (Chattopadhyay et al., 2011)', fontsize=9.5, color='#444')
    plt.tight_layout(); save(fig, 'f15_weather_progress.png')

# ---------------- F30 disease-specific features by grade (box plots, as in index figures of disease papers) ----------------
dsf = O1['DSF']; nc = 4; nr = int(np.ceil(len(dsf) / nc)); fig, axs = plt.subplots(nr, nc, figsize=(14, 3.4 * nr))
for ax, ft in zip(axs.ravel(), dsf):
    v = FD5[:, list(w5).index(int(ft[2:]))] * 1000 if ft.startswith('FD') else F[ft].values
    data = [v[(M.grade == g).values] for g in GR]; bp = ax.boxplot(data, patch_artist=True, showfliers=False, widths=0.6, medianprops=dict(color='k', lw=1.4))
    for p_, c in zip(bp['boxes'], GC): p_.set_facecolor(c); p_.set_alpha(0.85)
    r = np.corrcoef(v, M.grade)[0, 1]; ax.set_xticklabels(GR, fontsize=10); ax.set_title('%s  (r = %.2f)' % (ft, r), fontsize=12); ax.grid(axis='x', visible=False); ax.tick_params(axis='y', labelsize=9.5)
for ax in axs.ravel()[len(dsf):]: ax.axis('off')
for ax in axs[-1]: ax.set_xlabel('Leaf grade')
plt.tight_layout(); save(fig, 'f30_dsf_by_grade.png')
print('objective-1 figures ok')
if len(sys.argv) > 1 and sys.argv[1] == 'obj1': sys.exit()

# ================= Objective 2 figures =================
MT = pd.read_csv(D + 'metrics_all.csv'); best = json.load(open(D + 'best_models.json'))
mlm = ['SVM', 'RF', 'XGBoost', 'k-NN', 'PLS-DA', 'PLS']
PAL = ['#2E75B6', '#2E7D32', '#E07B00', '#C62828', '#7030A0', '#00838F', '#6D4C41', '#AD1457', '#455A64', '#9E9D24']
fig, axs = plt.subplots(1, 3, figsize=(14.5, 5.4))
for ax, t, key, ttl in zip(axs, 'ABC', ['macro_F1', 'macro_F1', 'R2'], ['(a) Detection: macro-F1', '(b) Six grades: macro-F1', '(c) Severity score: R²']):
    d = MT[MT.task == t].copy(); d['grp'] = d.model.map(lambda m: 'ML' if m in mlm else 'DL'); d = d.sort_values(key)
    sdk = 'macro_F1_sd' if key == 'macro_F1' else None
    bars = ax.barh([mname(m, t) for m in d.model], d[key], xerr=d[sdk] if sdk else None, color=[ML_C if g == 'ML' else DL_C for g in d.grp], height=0.65, capsize=3, error_kw=dict(lw=1, ecolor='#555'))
    for b, v in zip(bars, d[key]): ax.text(0.01, b.get_y() + b.get_height() / 2, '%.3f' % v, va='center', ha='left', fontsize=10, color='white', fontweight='bold')
    ax.set_title(ttl); ax.set_xlim(0, 1 if key != 'R2' else max(0.7, d[key].max() + 0.1)); ax.grid(axis='y', visible=False)
    ax.set_xlabel(key.replace('_', '-').replace('R2', 'R²') + (' (± SD over folds)' if sdk else ''))
fig.legend([Patch(color=ML_C), Patch(color=DL_C)], ['machine learning', 'deep learning'], loc='lower center', ncol=2, bbox_to_anchor=(0.5, -0.04)); plt.tight_layout(rect=(0, 0.04, 1, 1)); save(fig, 'f16_model_comparison.png')
fig, axs = plt.subplots(1, 3, figsize=(15.5, 5.8), gridspec_kw={'width_ratios': [6, 6, 5]})
spec = {'A': ['OA', 'kappa', 'macro_F1', 'sensitivity', 'specificity', 'AUC'], 'B': ['OA', 'kappa', 'macro_F1', 'macro_R', 'QWK', 'within1'], 'C': ['R2', 'RMSE', 'MAE', 'RPD', 'r']}
for ax, t, ttl in zip(axs, 'ABC', ['(a) Detection', '(b) Six grades', '(c) Severity score']):
    d = MT[MT.task == t].set_index('model')[spec[t]]; V = d.values.astype(float); Z = (V - np.nanmin(V, 0)) / (np.nanmax(V, 0) - np.nanmin(V, 0) + 1e-12)
    for j, k in enumerate(spec[t]):
        if k in ('RMSE', 'MAE'): Z[:, j] = 1 - Z[:, j]
    ax.imshow(Z, cmap='Greens', vmin=-0.15, vmax=1.15, aspect='auto'); ax.grid(False)
    for i in range(V.shape[0]):
        for j in range(V.shape[1]): ax.text(j, i, '%.2f' % V[i, j], ha='center', va='center', fontsize=10, color='white' if Z[i, j] > 0.65 else '#1A1A1A', fontweight='bold' if Z[i, j] > 0.99 else 'normal')
    ax.set_xticks(range(len(spec[t]))); ax.set_xticklabels([k.replace('macro_', 'macro-').replace('within1', '±1 grade').replace('R2', 'R²') for k in spec[t]], rotation=35, ha='right')
    ax.set_yticks(range(len(d))); ax.set_yticklabels([mname(m, t) for m in d.index]); ax.set_title(ttl); nospine(ax)
fig.text(0.5, -0.02, 'Pooled leave-one-replication-out test predictions; darker = better within each column (RMSE, MAE reversed)', ha='center', fontsize=10.5, color='#444')
plt.tight_layout(); save(fig, 'f31_metric_heatmap.png')
cms = np.load(D + 'confusion.npy', allow_pickle=True).item()
fig, axs = plt.subplots(1, 2, figsize=(13.5, 5.8)); im = None
for ax, src in zip(axs, ('ML', 'DL')):
    mn = best['B'][src]; cm = cms.get('B|' + str(mn)); ax.grid(False)
    if cm is None: ax.axis('off'); ax.text(0.5, 0.5, 'deep-learning results pending', ha='center', transform=ax.transAxes); continue
    cmn = cm / cm.sum(1, keepdims=True); im = ax.imshow(cmn, cmap='Greens', vmin=0, vmax=1)
    for i in range(6):
        for j in range(6): ax.text(j, i, '%d\n%.0f%%' % (cm[i, j], 100 * cmn[i, j]), ha='center', va='center', fontsize=9.5, color='white' if cmn[i, j] > .5 else '#1A1A1A')
    for k in range(6): ax.add_patch(plt.Rectangle((k - 0.5, k - 0.5), 1, 1, fill=False, ec='#1B2A1E', lw=1.6))
    r = MT[(MT.task == 'B') & (MT.model == mn)].iloc[0]
    ax.set_xticks(range(6)); ax.set_yticks(range(6)); ax.set_xticklabels(GR); ax.set_yticklabels(GR); ax.set(xlabel='Predicted grade', ylabel='Observed grade')
    ax.set_title('%s (%s): OA %.2f, macro-F1 %.2f, QWK %.2f' % (mn, src, r.OA, r.macro_F1, r.QWK), fontsize=12); nospine(ax)
if im is not None: cb = fig.colorbar(im, ax=axs, fraction=0.025, pad=0.02); cb.set_label('Row-normalised proportion'); cb.outline.set_visible(False)
save(fig, 'f17_confusion.png')
from sklearn.metrics import roc_curve
allp = pd.read_csv(D + 'all_predictions.csv')
fig, ax = plt.subplots(figsize=(7.5, 7)); dA = MT[MT.task == 'A'].sort_values('AUC', ascending=False)
for i, mn in enumerate(dA.model):
    d = allp[(allp.task == 'A') & (allp.model == mn) & allp.score.notna()]
    if not len(d): continue
    fpr, tpr, _ = roc_curve(d.y, d.score); ax.plot(fpr, tpr, lw=2.4 if i == 0 else 1.6, color=PAL[i % len(PAL)], ls='-' if mn in mlm else '--', label='%s (AUC %.3f)' % (mn, dA.AUC.iloc[i]))
ax.plot([0, 1], [0, 1], color='#9E9E9E', ls=':', lw=1); ax.set(xlabel='False-positive rate (1 − specificity)', ylabel='True-positive rate (sensitivity)', xlim=(0, 1), ylim=(0, 1.01)); ax.set_aspect('equal')
ax.set_title('ROC curves, detection (pooled test folds)'); ax.legend(loc='lower right', fontsize=10); save(fig, 'f18_roc.png')
cand = [m for m in ['DT-EDNet', 'EfficientNet-B0', 'ResNet18', 'ConvNeXt V2-Atto', 'DNN-F1', 'XGBoost', 'SVM', 'RF'] if m in MT[MT.task == 'B'].model.values][:6]
labels = ['F1 grade %d' % g for g in GR] + ['OA', 'kappa', 'macro-F1']; ang = np.linspace(0, 2 * np.pi, len(labels), endpoint=False).tolist(); ang += ang[:1]
fig = plt.figure(figsize=(8.5, 7.5)); ax = plt.subplot(111, polar=True)
for i, mn in enumerate(cand):
    r = MT[(MT.task == 'B') & (MT.model == mn)].iloc[0]; v = [r['F1_g%d' % g] for g in GR] + [r.OA, r.kappa, r.macro_F1]; v += v[:1]
    ax.plot(ang, v, lw=2.2, color=PAL[i], label=mn, marker='o', ms=4); ax.fill(ang, v, alpha=.07, color=PAL[i])
ax.set_xticks(ang[:-1]); ax.set_xticklabels(labels, fontsize=11); ax.set_ylim(0, 0.9); ax.set_yticks([0.2, 0.4, 0.6, 0.8]); ax.tick_params(axis='y', labelsize=9)
ax.set_title('Six-grade performance profile', pad=24, loc='center'); ax.legend(loc='upper right', bbox_to_anchor=(1.38, 1.08)); save(fig, 'f19_radar.png')
fig, axs = plt.subplots(1, 2, figsize=(13, 5.8))
for ax, src in zip(axs, ('ML', 'DL')):
    mn = best['C'][src]
    if mn is None: ax.axis('off'); ax.text(0.5, 0.5, 'deep-learning results pending', ha='center', transform=ax.transAxes); continue
    d = allp[(allp.task == 'C') & (allp.model == mn)]; r = MT[(MT.task == 'C') & (MT.model == mn)].iloc[0]
    jit = d.y + np.random.default_rng(1).uniform(-0.3, 0.3, len(d)); ax.scatter(jit, d.pred, s=8, alpha=.35, color=[GC[GR.index(int(g))] for g in d.y], lw=0)
    ax.plot([-0.5, 9.5], [-0.5, 9.5], color='#333', ls='--', lw=1, label='1:1 line'); g_ = d.groupby('y').pred
    ax.errorbar(g_.mean().index, g_.mean().values, yerr=g_.std().values, fmt='s-', color='k', ms=7, capsize=4, lw=1.6, label='mean ± SD')
    ax.set(xlabel='Observed grade (jittered)', ylabel='Predicted severity score', xlim=(-0.7, 9.7), ylim=(-1, 10.5)); ax.set_xticks(GR); ax.set_aspect('equal')
    ax.set_title('%s (%s)' % (mname(mn, 'C'), src))
    ax.text(0.03, 0.97, 'R² = %.2f\nRMSE = %.2f\nRPD = %.2f\nbias = %.2f' % (r.R2, r.RMSE, r.RPD, r.bias), transform=ax.transAxes, va='top', fontsize=11, bbox=dict(fc='white', ec='#BDBDBD', boxstyle='round,pad=0.4'))
    ax.legend(loc='lower right')
plt.tight_layout(); save(fig, 'f20_pred_obs.png')
if os.path.exists(D + 'dl_main.json'):
    R = json.load(open(D + 'dl_main.json')); fig, axs = plt.subplots(2, 2, figsize=(13, 8.4)); hs = None
    for ax, net in zip(axs.ravel(), ['DT-EDNet', 'EfficientNet-B0', 'ResNet18', 'ConvNeXt V2-Atto']):
        r = [x for x in R if x['net'] == net and x['task'] == 'B' and x['fold'] == 0]
        if not r: ax.axis('off'); continue
        h = np.array(r[0]['hist']); l1, = ax.plot(h[:, 0], h[:, 1], color=ML_C, lw=1.8); l2, = ax.plot(h[:, 0], h[:, 2], color='#E07B00', lw=1.8); a2 = ax.twinx(); l3, = a2.plot(h[:, 0], h[:, 3], color=IDX_C, lw=1.8); hs = [l1, l2, l3]
        be = int(h[np.argmax(h[:, 3]), 0]); ax.axvline(be, color='#555', ls=':', lw=1); a2.set_ylim(0, 1); a2.grid(False); a2.spines['right'].set_visible(True); a2.set_ylabel('Validation macro-F1', color=IDX_C); a2.tick_params(axis='y', colors=IDX_C)
        ax.set(xlabel='Epoch', ylabel='Loss'); ax.set_title('%s (fold 1, six grades; best epoch %d)' % (net, be), fontsize=12)
    if hs: fig.legend(hs, ['training loss', 'validation loss', 'validation macro-F1'], loc='lower center', ncol=3, bbox_to_anchor=(0.5, -0.03))
    plt.tight_layout(rect=(0, 0.03, 1, 1)); save(fig, 'f21_learning_curves.png')
CFG_C = {'OW': '#90CAF9', 'VI': '#A5D6A7', 'DSF': '#7030A0'}; CFG_L = {'OW': 'OW: optimal wavelengths', 'VI': 'VI: selected indices', 'DSF': 'DSF: disease-specific set'}
if os.path.exists(D + 'dl_summary_config.csv'):
    cf = pd.read_csv(D + 'dl_summary_config.csv'); fig, ax = plt.subplots(figsize=(12, 5.2)); nets = list(cf.net.unique()); cfgs = [c for c in ['OW', 'VI', 'DSF'] if c in cf.config.values]
    for i, cg in enumerate(cfgs):
        d = cf[cf.config == cg].set_index('net').reindex(nets); bars = ax.bar(np.arange(len(nets)) + (i - (len(cfgs) - 1) / 2) * 0.26, d.macro_F1, 0.26, label=CFG_L[cg], color=CFG_C[cg], edgecolor='white'); label_bars(ax, bars, '%.2f', fs=9.5)
    ax.set_xticks(range(len(nets))); ax.set_xticklabels(nets); ax.set(ylabel='Macro-F1 (six grades)', ylim=(0, max(0.6, cf.macro_F1.max() + 0.08))); ax.grid(axis='x', visible=False)
    ax.set_title('Networks on three feature configurations'); ax.legend(loc='upper center', ncol=3, bbox_to_anchor=(0.5, -0.1)); save(fig, 'f22_config.png')
if os.path.exists(D + 'dl_summary_ablation.csv'):
    ab = pd.read_csv(D + 'dl_summary_ablation.csv'); fig, ax = plt.subplots(figsize=(11, 5)); x = np.arange(len(ab)); KS = ['OA', 'kappa', 'macro_R', 'macro_F1']; KC = ['#90CAF9', '#5C9BD5', '#2E75B6', '#7030A0']
    for i, k in enumerate(KS): bars = ax.bar(x + (i - 1.5) * 0.2, ab[k], 0.2, label=k.replace('macro_', 'macro-'), color=KC[i], edgecolor='white'); label_bars(ax, bars, '%.2f', fs=8.5)
    ax.set_xticks(x); ax.set_xticklabels(ab.net); ax.set(ylim=(0, max(0.7, ab[KS].values.max() + 0.1)), ylabel='Score (six grades)'); ax.grid(axis='x', visible=False)
    ax.set_title('DT-EDNet module ablation (SE = squeeze-excitation; DTG = dual-token gating)'); ax.legend(ncol=4, loc='upper center', bbox_to_anchor=(0.5, -0.1)); save(fig, 'f23_ablation.png')
if os.path.exists(D + 'shap_C.npy'):
    sv = np.load(D + 'shap_C.npy'); X = pd.read_csv(D + 'shap_X.csv'); order = np.argsort(np.abs(sv).mean(0))
    fig, axs = plt.subplots(1, 2, figsize=(14.5, 6))
    for k, j in enumerate(order):
        v = X.iloc[:, j].values; lo, hi = np.percentile(v, [2, 98]); vn = np.clip((v - lo) / (hi - lo + 1e-12), 0, 1); y_ = k + np.random.default_rng(k).uniform(-0.32, 0.32, len(v))
        sc_ = axs[0].scatter(sv[:, j], y_, c=vn, cmap='coolwarm', s=6, alpha=.6, lw=0, vmin=0, vmax=1)
    axs[0].set_yticks(range(len(order))); axs[0].set_yticklabels(X.columns[order]); axs[0].axvline(0, color='#333', lw=0.8); axs[0].grid(axis='y', visible=False)
    axs[0].set(xlabel='SHAP value (effect on predicted score)'); axs[0].set_title('(a) SHAP summary, severity score (XGBoost)')
    cb = fig.colorbar(sc_, ax=axs[0], fraction=0.04, pad=0.02, ticks=[0, 1]); cb.ax.set_yticklabels(['low', 'high']); cb.set_label('Feature value'); cb.outline.set_visible(False)
    ib = pd.read_csv(D + 'shap_B_importance.csv', index_col=0); ib = ib.loc[ib.sum(1).sort_values().index]; left = np.zeros(len(ib))
    for i, c in enumerate(ib.columns): axs[1].barh(ib.index, ib[c], left=left, color=GC[i % 6], height=0.7, label='grade %s' % GR[i] if len(ib.columns) == 6 else c, edgecolor='white', lw=0.5); left += ib[c].values
    axs[1].set(xlabel='mean |SHAP| (stacked over grades)'); axs[1].set_title('(b) SHAP importance by grade, six grades (XGBoost)'); axs[1].legend(loc='lower right', ncol=2); axs[1].grid(axis='y', visible=False)
    plt.tight_layout(); save(fig, 'f24_shap.png')
if os.path.exists(D + 'strata_metrics.csv'):
    sm = pd.read_csv(D + 'strata_metrics.csv'); d = sm[(sm.task == 'B')]; facs = ['stage', 'variety', 'leafpos', 'date']
    fig, axs = plt.subplots(2, 2, figsize=(13, 8.4))
    for ax, fac, ttl in zip(axs.ravel(), facs, ['(a) Growth stage', '(b) Variety', '(c) Leaf position', '(d) Sampling date']):
        srcs_ = [s for s in ['ML', 'DL'] if len(d[(d.factor == fac) & (d.source == s)])]
        for i, src in enumerate(srcs_):
            dd = d[(d.factor == fac) & (d.source == src)]; off = (i - (len(srcs_) - 1) / 2) * 0.38
            bars = ax.bar(np.arange(len(dd)) + off, dd.macro_F1, 0.38, color=ML_C if src == 'ML' else DL_C, label='%s: %s' % (src, dd.model.iloc[0])); label_bars(ax, bars, '%.2f', fs=9.5)
        ax.set_xticks(range(len(dd))); ax.set_xticklabels(['%s\n(n = %d)' % (l, n_) for l, n_ in zip(dd.level, dd.n)], fontsize=10)
        ax.set(ylabel='Macro-F1 (six grades)', ylim=(0, 0.75)); ax.set_title(ttl); ax.legend(loc='upper left'); ax.grid(axis='x', visible=False)
    plt.tight_layout(); save(fig, 'f25_strata.png')
if os.path.exists(D + 'transfer_tests.csv'):
    tt = pd.read_csv(D + 'transfer_tests.csv'); fig, axs = plt.subplots(1, 2, figsize=(13, 5))
    for ax, t, k, c, c2, ttl in ((axs[0], 'B', 'macro_F1', ML_C, '#9FA8DA', '(a) Six grades: macro-F1 on the held-out group'), (axs[1], 'C', 'RMSE', FD_C, '#EF9A9A', '(b) Severity score: RMSE on the held-out group')):
        d = tt[tt.task == t]; lab = ['%s\n%s' % (a, b) for a, b in zip(d.test, d.level)]
        bars = ax.bar(range(len(d)), d[k], color=[c if a == 'variety' else c2 for a in d.test], width=0.65); label_bars(ax, bars, '%.2f', fs=10)
        ax.set_xticks(range(len(d))); ax.set_xticklabels(lab, fontsize=10); ax.set_ylabel(k.replace('_', '-')); ax.set_title(ttl, fontsize=12); ax.grid(axis='x', visible=False)
    fig.text(0.5, -0.02, 'Random forest trained on the other varieties (or timings) and tested on the one left out; feature selection repeated inside', ha='center', fontsize=10.5, color='#444')
    plt.tight_layout(); save(fig, 'f26_transfer.png')
if os.path.exists(D + 'covariate_baseline.csv'):
    cb_ = pd.read_csv(D + 'covariate_baseline.csv'); fig, axs = plt.subplots(1, 3, figsize=(14, 5))
    for ax, t, k in zip(axs, 'ABC', ['macro_F1', 'macro_F1', 'R2']):
        d = cb_[cb_.task == t]; bars = ax.bar(range(len(d)), d[k], color=[GREY, ML_C, DL_C], width=0.6); label_bars(ax, bars, '%.3f', fs=10.5)
        ax.set_xticks(range(len(d))); ax.set_xticklabels(['covariates\nonly', 'leaf spectra\n(DSF)', 'spectra +\ncovariates']); ax.grid(axis='x', visible=False)
        ax.set(ylabel=k.replace('_', '-').replace('R2', 'R²'), ylim=(0, max(d[k]) * 1.18)); ax.set_title({'A': '(a) Detection', 'B': '(b) Six grades', 'C': '(c) Severity score'}[t])
    fig.text(0.5, -0.02, 'Unsprayed (naturally infected) plots only; covariates = variety, sowing timing, days after sowing, growth stage and 7-day weather', ha='center', fontsize=10.5, color='#444')
    plt.tight_layout(); save(fig, 'f27_covariates.png')
if os.path.exists(D + 'exploratory_asymptomatic.csv'):
    ex = pd.read_csv(D + 'exploratory_asymptomatic.csv'); fig, ax = plt.subplots(figsize=(10, 5)); x = np.arange(len(ex)); KS = ['balanced_acc', 'AUC', 'sensitivity', 'specificity']; KC = ['#7030A0', '#2E75B6', '#E07B00', '#2E7D32']
    for i, k in enumerate(KS): bars = ax.bar(x + (i - 1.5) * 0.2, ex[k], 0.2, label=k.replace('_', ' ').replace('acc', 'accuracy'), color=KC[i]); label_bars(ax, bars, '%.2f', fs=9)
    ax.axhline(0.5, color='#333', ls=':', lw=1); ax.text(len(ex) - 0.5, 0.505, 'chance', fontsize=9.5, ha='right', va='bottom'); ax.set_xticks(x); ax.set_xticklabels(ex.model); ax.set(ylim=(0, 1.05), ylabel='Score'); ax.grid(axis='x', visible=False)
    ax.set_title('Exploratory: symptomless leaves of unsprayed plots vs sprayed healthy-plot leaves'); ax.legend(ncol=4, loc='upper center', bbox_to_anchor=(0.5, -0.1)); save(fig, 'f28_asymptomatic.png')
if os.path.exists(D + 'selection_stability.csv'):
    st = pd.read_csv(D + 'selection_stability.csv'); d = st[st.group == 'optimal wavelengths'].sort_values(['folds', 'feature'], ascending=[False, True])
    fig, ax = plt.subplots(figsize=(13, 4.6)); ax.bar(range(len(d)), d.folds, color=[FD_C if f.startswith('FD') else R_C for f in d.feature], width=0.7)
    ax.set_xticks(range(len(d))); ax.set_xticklabels(d.feature, rotation=90, fontsize=9.5); ax.set(ylabel='Folds selected (of 3)', yticks=[0, 1, 2, 3]); ax.grid(axis='x', visible=False)
    ax.legend([Patch(color=FD_C), Patch(color=R_C)], ['first derivative', 'reflectance'], loc='upper right'); ax.set_title('Stability of the optimal wavelengths across the three outer folds'); save(fig, 'f29_stability.png')
print('all figures ok')
