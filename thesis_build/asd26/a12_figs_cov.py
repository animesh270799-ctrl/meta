"""Figures of the covariate baseline (Step 2.5.5) for the 2025-26 ASD leaf data – same style as a6_figs.py (300 dpi)."""
import numpy as np, pandas as pd, json, os
import matplotlib; matplotlib.use('Agg'); import matplotlib.pyplot as plt
from matplotlib.patches import Patch
from matplotlib.lines import Line2D
B = os.path.dirname(os.path.abspath(__file__)) + '/'; D = B + 'data/'; FG = B + 'fig/'
plt.rcParams.update({'font.family': 'Liberation Sans', 'font.size': 12, 'axes.titlesize': 13, 'axes.titleweight': 'bold', 'axes.titlelocation': 'left', 'axes.labelsize': 12,
                     'xtick.labelsize': 11, 'ytick.labelsize': 11, 'legend.fontsize': 10, 'legend.frameon': False, 'axes.spines.top': False, 'axes.spines.right': False,
                     'axes.grid': True, 'grid.color': '#E6E6E6', 'axes.axisbelow': True, 'figure.facecolor': 'white', 'mathtext.fontset': 'custom', 'mathtext.rm': 'Liberation Sans', 'mathtext.default': 'regular'})
def save(fig, n): fig.savefig(FG + n, dpi=300, bbox_inches='tight', pad_inches=0.08); plt.close(fig); print('  ', n)
MT = pd.read_csv(D + 'cov2_metrics.csv'); G = pd.read_csv(D + 'cov2_gains.csv'); CO = pd.read_csv(D + 'cov2_b1_coef.csv'); SUM = json.load(open(D + 'cov2_summary.json'))
INP = ['covariates only', 'leaf spectra', 'spectra + covariates']; INL = ['Covariates\nonly', 'Leaf\nspectra', 'Spectra +\ncovariates']
MOD = ['Statistical', 'RF', 'B2']; MC = {'Statistical': '#8C8C8C', 'RF': '#2E7D32', 'B2': '#7030A0'}
ML = {'A': {'Statistical': 'Logistic regression', 'RF': 'Random forest', 'B2': 'SVM (best ML)'}, 'B': {'Statistical': 'Ordinal logistic', 'RF': 'Random forest', 'B2': 'XGBoost (best ML)'},
      'C': {'Statistical': 'Linear (DAI, DAI²)', 'RF': 'Random forest = best ML', 'B2': None}}
# ---------------- F32: models x inputs for the three tasks ----------------
fig, axs = plt.subplots(1, 3, figsize=(15, 5.2))
for ax, t, k, ttl in zip(axs, 'ABC', ['macro_F1', 'macro_F1', 'R2'], ['(a) Detection: macro-F1', '(b) Six grades: macro-F1', '(c) Severity score: R²']):
    mods = [m for m in MOD if not (t == 'C' and m == 'B2')]; wdt = 0.8 / len(mods)
    for j, m in enumerate(mods):
        v = [MT[(MT.task == t) & (MT.input == i) & (MT.model == m)][k].iloc[0] for i in INP]
        bars = ax.bar(np.arange(3) + (j - (len(mods) - 1) / 2) * wdt, v, wdt, color=MC[m], label=ML[t][m], edgecolor='white')
        for b_, vv in zip(bars, v): ax.text(b_.get_x() + b_.get_width() / 2, vv + 0.008, '%.2f' % vv, ha='center', va='bottom', fontsize=9)
    m0 = SUM[t]['M0']; i0 = INP.index(m0['input'])
    ax.annotate('M0', xy=(i0 + (mods.index(m0['model']) - (len(mods) - 1) / 2) * wdt, 0.02), ha='center', fontsize=10, fontweight='bold', color='white')
    ax.set_xticks(range(3)); ax.set_xticklabels(INL); ax.set_title(ttl); ax.grid(axis='x', visible=False)
    ax.set_ylim(0, max(1.0 if t == 'A' else 0.6, MT[MT.task == t][k].max() + 0.08)); ax.legend(loc='upper left', fontsize=9.5)
fig.text(0.5, -0.02, 'Inoculated (unsprayed) leaves only, n = 1961; leave-one-replication-out; M0 = the stronger covariate-only model', ha='center', fontsize=10.5, color='#444')
plt.tight_layout(); save(fig, 'f32_cov_models.png')
# ---------------- F33: gains with 95% plot-block bootstrap CI ----------------
GN = {'ΔS = M1 − M0': ('#2E75B6', 'ΔS: spectra over covariates'), 'ΔC = M2 − M1': ('#E07B00', 'ΔC: covariates added to spectra'), 'ΔT = M2 − M0': ('#7030A0', 'ΔT: spectra + covariates over covariates')}
lab = {'macro_F1': 'macro-F1', 'AUC': 'AUC', 'balanced_acc': 'balanced accuracy', 'QWK': 'quadratic weighted kappa', 'R2': 'R²', 'RMSE': 'RMSE (lower is better)'}
fig, axs = plt.subplots(1, 3, figsize=(15, 5.4), gridspec_kw={'width_ratios': [3, 2, 2]})
for ax, t, ttl in zip(axs, 'ABC', ['(a) Detection', '(b) Six grades', '(c) Severity score']):
    d = G[G.task == t].reset_index(drop=True); mets = list(dict.fromkeys(d.metric)); y = 0; yt, yl = [], []
    for mt in mets:
        for gname in GN:
            r = d[(d.metric == mt) & (d.gain == gname)]
            if not len(r): continue
            r = r.iloc[0]; c = GN[gname][0]
            ax.plot([r.ci_low, r.ci_high], [y, y], color=c, lw=2.2); ax.plot(r.delta, y, 'o', ms=9, color=c, mfc=c if r.real_gain else 'white', mew=2)
            y -= 1
        yt.append(y + 2); yl.append(lab[mt]); y -= 0.8
    lo_, hi_ = min(d.ci_low.min(), 0), max(d.ci_high.max(), 0); pad = 0.08 * (hi_ - lo_); ax.set_xlim(lo_ - pad, hi_ + pad)
    ax.axvline(0, color='#333', lw=1); ax.set_yticks(yt); ax.set_yticklabels(yl); ax.grid(axis='y', visible=False); ax.set_title(ttl); ax.set_xlabel('Difference (95% CI)')
fig.legend([Line2D([], [], color=v[0], marker='o', lw=2.2, ms=8) for v in GN.values()] + [Line2D([], [], color='#555', marker='o', mfc='white', lw=0, ms=8)],
           [v[1] for v in GN.values()] + ['filled = real difference (CI excludes 0, |Δ| > fold SD, same sign in all folds); open = not real.  Right of 0 = better (RMSE: left of 0 = better)'], loc='lower center', ncol=2, bbox_to_anchor=(0.5, -0.12))
plt.tight_layout(rect=(0, 0.06, 1, 1)); save(fig, 'f33_cov_gains.png')
# ---------------- F34: interpretable B1 model, standardised effects ----------------
TN = {'variety_V2': 'variety V2 (vs V1)', 'variety_V3': 'variety V3 (vs V1)', 'timing_D2': 'timing D2 (vs D1)', 'timing_D3': 'timing D3 (vs D1)', 'timing_D4': 'timing D4 (vs D1)', 'stage_code': 'growth stage', 'DAI': 'days after inoculation', 'DAI2': '(days after inoculation)²'}
mods = [m for m in ['Logistic (detection)', 'Ordinal logistic (six grades)', 'Linear (score)'] if m in set(CO.model)]
fig, axs = plt.subplots(1, len(mods), figsize=(5 * len(mods), 5.2), sharey=True)
axs = np.atleast_1d(axs)
for ax, m in zip(axs, mods):
    d = CO[CO.model == m].reset_index(drop=True); yy = np.arange(len(d))[::-1]
    for y_, r in zip(yy, d.itertuples()):
        sig = r.p < 0.05; c = '#C62828' if (sig and r.estimate > 0) else ('#1565C0' if sig else '#9E9E9E')
        ax.plot([r.ci_low, r.ci_high], [y_, y_], color=c, lw=2.2); ax.plot(r.estimate, y_, 'o', color=c, ms=8)
    ax.axvline(0, color='#333', lw=1); ax.set_yticks(yy); ax.set_yticklabels([TN.get(x, x) for x in d.term]); ax.grid(axis='y', visible=False)
    ax.set_title(m.replace(' (', '\n('), fontsize=12); ax.set_xlabel('log-odds per SD' if 'ogistic' in m else 'grade units per SD')
fig.legend([Line2D([], [], color=c, marker='o', lw=2) for c in ('#C62828', '#1565C0', '#9E9E9E')], ['raises disease (p < 0.05)', 'lowers disease (p < 0.05)', 'not significant'], loc='lower center', ncol=3, bbox_to_anchor=(0.5, -0.06))
plt.tight_layout(rect=(0, 0.04, 1, 1)); save(fig, 'f34_cov_b1.png')
print('covariate figures ok')
