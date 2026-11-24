"""Figures for the UAV transfer test (300 dpi PNG in uavt/fig/)."""
import os, json, numpy as np, pandas as pd, matplotlib
matplotlib.use('Agg'); import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch
HERE = os.path.dirname(os.path.abspath(__file__)); O = HERE + '/out/'; FG = HERE + '/fig/'; os.makedirs(FG, exist_ok=True)
plt.rcParams.update({'font.family': 'DejaVu Sans', 'font.size': 9, 'axes.spines.top': False, 'axes.spines.right': False, 'axes.titleweight': 'bold', 'axes.titlesize': 10,
                     'savefig.dpi': 300, 'savefig.bbox': 'tight'})
GT = pd.read_csv(O + 'ground_truth.csv'); MF = pd.read_csv(O + 'metrics_frozen.csv'); PF = pd.read_csv(O + 'predictions_frozen.csv')
MU = pd.read_csv(O + 'metrics_uav_trained.csv'); PU = pd.read_csv(O + 'predictions_uav_trained.csv'); BM = pd.read_csv(O + 'best_models.csv')
SC = pd.read_csv(O + 'spectra_compare.csv'); DF = pd.read_csv(O + 'domain_features.csv'); PC = pd.read_csv(O + 'pca_domain.csv'); SU = json.load(open(O + 'summary.json'))
VAR = ['Direct', 'Healthy-reference corrected', 'Corrected + brightness-normalised']; VSH = {'Direct': 'Direct', 'Healthy-reference corrected': 'Corrected', 'Corrected + brightness-normalised': 'Normalised'}
CH, CD, CA = '#1A9850', '#D73027', '#555555'; VC = {'Direct': '#4C72B0', 'Healthy-reference corrected': '#DD8452', 'Corrected + brightness-normalised': '#8172B3', 'UAV-trained': '#2CA02C'}
GR = [0, 1, 3, 5, 7, 9]; best = SU['best']
def shade(ax):
    for a, b in SU['gaps']: ax.axvspan(a, b, color='#EEEEEE', zorder=0)
def save(f, name): f.savefig(FG + name); plt.close(f)

# f1 workflow
f, ax = plt.subplots(figsize=(10, 3.3)); ax.axis('off'); ax.set_xlim(0, 10); ax.set_ylim(0, 3.3)
def box(x, y, w, h, t, c):
    ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle='round,pad=0.04,rounding_size=0.08', fc=c, ec='#333333', lw=0.8)); ax.text(x + w / 2, y + h / 2, t, ha='center', va='center', fontsize=8, wrap=True)
def arr(x1, y1, x2, y2): ax.annotate('', (x2, y2), (x1, y1), arrowprops=dict(arrowstyle='->', lw=1, color='#333333'))
box(0.1, 2.2, 2.0, 0.95, 'ASD leaf models 2025-26\n(2330 leaves, LORO;\nbest model per task)', '#E8F5E9')
box(2.6, 2.2, 2.0, 0.95, 'Frozen ASD models\n(no refitting)', '#E8F5E9')
box(0.1, 0.25, 2.0, 0.95, 'UAV hyperspectral\n24 Feb 2026\n48 plot mean spectra', '#E3F2FD')
box(2.6, 0.25, 2.0, 0.95, 'Same pre-processing\n1-nm resample, SG 11/2,\nFD, 5-nm bands, indices', '#FFF8E1')
box(5.1, 0.1, 2.1, 1.25, 'Three input variants\n1 Direct\n2 Healthy-reference corrected\n3 + brightness-normalised', '#FFF3E0')
box(5.1, 2.2, 2.1, 0.95, 'Predictions per plot\n(all 30 models; best per task)', '#E8F5E9')
box(7.7, 2.2, 2.2, 0.95, 'Evaluation vs 24 Feb ASD scores\nA healthy/diseased\nB grade   C mean leaf score', '#FCE4EC')
box(7.7, 0.25, 2.2, 0.95, 'In-domain check:\nbest ML type refitted on\nthe UAV plots (LORO)', '#EDE7F6')
arr(2.1, 2.67, 2.6, 2.67); arr(4.6, 2.67, 5.1, 2.67); arr(7.2, 2.67, 7.7, 2.67)
arr(2.1, 0.72, 2.6, 0.72); arr(4.6, 0.72, 5.1, 0.72); arr(6.15, 1.35, 6.15, 2.2); arr(7.2, 0.72, 7.7, 0.72); arr(8.8, 1.2, 8.8, 2.2)
save(f, 'u01_workflow.png')

# f2 spectra
f, axs = plt.subplots(1, 3, figsize=(12, 3.4), sharey=False)
w = SC.wavelength
for ax, (tag, ttl) in zip(axs, [('', 'a  Direct (UAV as measured)'), (' corrected', 'b  Healthy-reference corrected'), (' normalised', 'c  Corrected + brightness-normalised')]):
    shade(ax)
    ax.plot(w, SC['ASD healthy (24 Feb)'], color=CH, lw=1.2, ls='--', label='ASD leaves, healthy'); ax.plot(w, SC['ASD diseased (24 Feb)'], color=CD, lw=1.2, ls='--', label='ASD leaves, diseased')
    ax.plot(w, SC['UAV healthy' + tag], color=CH, lw=1.8, label='UAV plots, healthy'); ax.plot(w, SC['UAV diseased' + tag], color=CD, lw=1.8, label='UAV plots, diseased')
    ax.set_title(ttl, loc='left'); ax.set_xlabel('Wavelength (nm)'); ax.set_xlim(400, 2400)
axs[0].set_ylabel('Reflectance'); axs[0].legend(fontsize=7, frameon=False)
save(f, 'u02_spectra.png')

# f3 PCA domain
f, ax = plt.subplots(figsize=(6.2, 4.6))
a = PC[PC.source == 'ASD leaf']
for g, c in (('Healthy', CH), ('Diseased', CD)): s = a[a.group == g]; ax.scatter(s.PC1, s.PC2, s=5, color=c, alpha=0.18, lw=0, label='ASD leaves, %s' % g.lower())
for src, mk in (('UAV plot (direct)', 's'), ('UAV plot (corrected + brightness-normalised)', '^')):
    u = PC[PC.source == src]
    for g, c in (('Healthy', CH), ('Diseased', CD)):
        s = u[u.group == g]; ax.scatter(s.PC1, s.PC2, s=26, marker=mk, facecolor='none' if mk == 's' else c, edgecolor=c, lw=1, label='UAV %s, %s' % ('direct' if mk == 's' else 'normalised', g.lower()))
ax.set_xlabel('PC1 (%.0f %%)' % (100 * SU['pca_var'][0])); ax.set_ylabel('PC2 (%.0f %%)' % (100 * SU['pca_var'][1]))
ax.set_title('ASD leaves vs UAV plots in the space of the model features', loc='left'); ax.legend(fontsize=6.5, frameon=False, ncol=2, loc='best')
save(f, 'u03_pca.png')

# f4 features out of range
f, ax = plt.subplots(figsize=(7, 0.32 * len(DF) + 1))
y = np.arange(len(DF)); hgt = 0.26
for k, (v, tag) in enumerate(zip(VAR, ['direct', 'corrected', 'normalised'])):
    ax.barh(y + (k - 1) * hgt, DF['uav_%s_out_pct' % tag], height=hgt, color=VC[v], label=VSH[v])
ax.set_yticks(y); ax.set_yticklabels([r.feature + (' (gap)' if r.in_uav_gap else '') for r in DF.itertuples()]); ax.invert_yaxis()
ax.set_xlabel('UAV plots outside the ASD 1st-99th percentile range (%)'); ax.set_xlim(0, 100); ax.legend(frameon=False, fontsize=7, loc='lower right')
ax.set_title('Input features of the best models: UAV values outside the ASD training range', loc='left')
save(f, 'u04_features.png')

# helpers for best models
def mrow(t, model, v): r = MF[(MF.task == t) & (MF.model == model) & (MF.variant == v)]; return r.iloc[0] if len(r) else None
def prow(t, model, v): return PF[(PF.task == t) & (PF.model == model) & (PF.variant == v)].sort_values('plot')
KEYM = {'A': 'macro_F1', 'B': 'macro_F1', 'C': 'R2'}; ASDK = dict(zip(zip(BM.task, BM.role), BM.asd_value))

# f5 summary bars: ASD LORO vs UAV variants vs UAV-trained (best overall model per task, + best ML/DL)
f, axs = plt.subplots(1, 3, figsize=(12, 3.4))
for ax, t, lab in zip(axs, 'ABC', ['A  Detection: macro-F1', 'B  Six grades: macro-F1', 'C  Score: R²']):
    roles = ['overall', 'ML', 'DL']; x = np.arange(len(roles)); wbar = 0.16
    vals = [[ASDK[(t, r)] for r in roles]] + [[mrow(t, best[t][r], v)[KEYM[t]] for r in roles] for v in VAR]
    labs = ['ASD leaves (LORO)'] + [VSH[v] + ' (UAV)' for v in VAR]; cols = ['#999999'] + [VC[v] for v in VAR]
    for k, (vv, l, c) in enumerate(zip(vals, labs, cols)): ax.bar(x + (k - 1.5) * wbar, vv, wbar, color=c, label=l)
    um = MU[MU.task == t].iloc[0]; ax.bar(x[1] + 2.5 * wbar, um[KEYM[t]], wbar, color=VC['UAV-trained'], label='UAV-trained %s (LORO)' % um.model)
    ax.set_xticks(x); ax.set_xticklabels(['%s\n%s' % (r, best[t][r]) for r in roles], fontsize=7.5); ax.axhline(0, color='k', lw=0.6); ax.set_title(lab, loc='left')
    if t == 'C': ax.set_ylim(max(-1.5, min(0, np.nanmin(np.array(vals, dtype=float)) - 0.1)), 1)
    else: ax.set_ylim(0, 1)
axs[0].legend(fontsize=6.5, frameon=False, loc='upper right')
save(f, 'u05_summary.png')

# f6 confusion matrices: best overall model, three variants + UAV-trained (A and B)
def cm(y, p, labels):
    M_ = np.zeros((len(labels), len(labels)), int)
    for a_, b_ in zip(y, p): M_[labels.index(a_), labels.index(b_)] += 1
    return M_
for t, labels, names, fn in (('A', [0, 1], ['Healthy', 'Diseased'], 'u06_confusion_A.png'), ('B', GR, [str(g) for g in GR], 'u07_confusion_B.png')):
    mdl = best[t]['overall']; panels = [(VSH[v], prow(t, mdl, v)) for v in VAR] + [('UAV-trained %s' % MU[MU.task == t].model.iloc[0], PU[PU.task == t].sort_values('plot'))]
    f, axs = plt.subplots(1, 4, figsize=(12.5, 3.2 if t == 'A' else 3.5))
    for ax, (ttl, d) in zip(axs, panels):
        C_ = cm(d.y.astype(int).tolist(), d.pred.astype(int).tolist(), labels); ax.imshow(C_, cmap='Greens')
        for i in range(len(labels)):
            for j in range(len(labels)):
                if C_[i, j] or t == 'A': ax.text(j, i, C_[i, j], ha='center', va='center', fontsize=8, color='white' if C_[i, j] > C_.max() / 2 else 'black')
        ax.set_xticks(range(len(labels))); ax.set_yticks(range(len(labels))); ax.set_xticklabels(names, fontsize=7); ax.set_yticklabels(names, fontsize=7)
        ax.set_xlabel('Predicted'); ax.set_title(ttl, fontsize=9)
    axs[0].set_ylabel('True (24 Feb plot)')
    f.suptitle('%s: %s' % ('Detection' if t == 'A' else 'Grade (nearest grade of the plot mean leaf score)', 'best ASD model %s' % mdl), x=0.01, ha='left', fontweight='bold', fontsize=10)
    save(f, fn)

# f8 score scatter
mdl = best['C']['overall']; panels = [(VSH[v], prow('C', mdl, v), mrow('C', mdl, v)) for v in VAR] + [('UAV-trained %s' % MU[MU.task == 'C'].model.iloc[0], PU[PU.task == 'C'].sort_values('plot'), MU[MU.task == 'C'].iloc[0])]
f, axs = plt.subplots(1, 4, figsize=(12.5, 3.3), sharey=True)
for ax, (ttl, d, m) in zip(axs, panels):
    h = GT.set_index('plot').loc[d['plot'], 'status'].values
    ax.scatter(d.y[h == 'Healthy'], d.pred[h == 'Healthy'], s=18, color=CH, label='healthy plot'); ax.scatter(d.y[h == 'Diseased'], d.pred[h == 'Diseased'], s=18, color=CD, label='diseased plot')
    ax.plot([0, 9], [0, 9], color='#888888', lw=0.8, ls='--'); ax.set_xlim(-0.3, 7); ax.set_ylim(-0.3, 9.3)
    ax.set_title('%s\nR² %.2f, RMSE %.2f, r %.2f' % (ttl, m.R2, m.RMSE, m.r), fontsize=8.5); ax.set_xlabel('True plot mean leaf score')
axs[0].set_ylabel('Predicted score (%s)' % mdl); axs[0].legend(fontsize=7, frameon=False)
save(f, 'u08_score.png')

# f9 heat map of all models x variants
f, axs = plt.subplots(1, 3, figsize=(12.5, 4.0))
for ax, t, lab, vmin, vmax in zip(axs, 'ABC', ['A macro-F1', 'B macro-F1', 'C R²'], [0, 0, -1], [1, 1, 1]):
    d = MF[MF.task == t].pivot_table(index='model', columns='variant', values=KEYM[t])[VAR]
    um = MU[MU.task == t].iloc[0]; d['UAV-trained'] = np.nan; d.loc[um.model, 'UAV-trained'] = um[KEYM[t]]
    im = ax.imshow(d.values, cmap='RdYlGn', vmin=vmin, vmax=vmax, aspect='auto')
    for i in range(d.shape[0]):
        for j in range(d.shape[1]):
            v = d.values[i, j]
            if np.isfinite(v): ax.text(j, i, '%.2f' % v, ha='center', va='center', fontsize=7)
    ax.set_xticks(range(d.shape[1])); ax.set_xticklabels([VSH.get(c, c).replace('UAV-trained', 'UAV-\ntrained') for c in d.columns], fontsize=7)
    ax.set_yticks(range(d.shape[0])); ax.set_yticklabels(d.index, fontsize=7.5); ax.set_title(lab, loc='left'); plt.colorbar(im, ax=ax, fraction=0.04)
save(f, 'u09_heatmap.png')
print('figures saved', sorted(os.listdir(FG)))
