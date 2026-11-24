"""Plot-level disease maps of the UAV hyperspectral image of 24 Feb 2026 from the best ASD models (and the UAV-trained check).
Inputs: uavt/out (predictions of the transfer test, ground truth) + acm/layout.json (plot arrangement of the experiment).
Outputs: uavm/out/*.csv|json and uavm/fig/*.png."""
import os, json, re, numpy as np, pandas as pd, matplotlib
matplotlib.use('Agg'); import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
from matplotlib.colors import ListedColormap, BoundaryNorm, Normalize
HERE = os.path.dirname(os.path.abspath(__file__)) + '/'; TB = HERE + '../'; T = TB + 'uavt/out/'; O = HERE + 'out/'; FG = HERE + 'fig/'
os.makedirs(O, exist_ok=True); os.makedirs(FG, exist_ok=True)
plt.rcParams.update({'font.family': 'DejaVu Sans', 'font.size': 8, 'savefig.dpi': 300, 'savefig.bbox': 'tight', 'axes.titleweight': 'bold', 'axes.titlesize': 7.5})
GR = [0, 1, 3, 5, 7, 9]; VAR = ['Direct', 'Healthy-reference corrected', 'Corrected + brightness-normalised']; VSH = {'Direct': 'direct', 'Healthy-reference corrected': 'corrected', 'Corrected + brightness-normalised': 'normalised'}
GT = pd.read_csv(T + 'ground_truth.csv'); PF = pd.read_csv(T + 'predictions_frozen.csv'); PU = pd.read_csv(T + 'predictions_uav_trained.csv')
SU = json.load(open(T + 'summary.json')); RN = json.load(open(T + 'report_numbers.json')); best = SU['best']; bv = RN['best_variant']
NP = len(GT)

# ---------------- field layout (plot arrangement of the experiment plan; schematic, not to scale)
L = json.load(open(TB + 'acm/layout.json'))['buffer10']
geo = {}
for e in L:
    mm = re.search(r'D(\d)V(\d)\s*\((\d+)\)', e.get('t') or '')
    if mm: geo[int(mm.group(3))] = dict(x=e['x'], y=e['y'], w=e['w'], h=e['h'], sow='D' + mm.group(1), var='V' + mm.group(2))
assert len(geo) == NP, len(geo)
for p in range(1, NP + 1):                                                  # the layout treatments must match the 2025-26 records
    g, r = geo[p], GT[GT['plot'] == p].iloc[0]
    assert (g['sow'], g['var']) == (r.sowing, r.variety), (p, g, r.sowing, r.variety)
xs = sorted(set(round(g['x'], 2) for g in geo.values())); ys = sorted(set(round(g['y'], 2) for g in geo.values()))
for p, g in geo.items(): g['col'] = xs.index(round(g['x'], 2)); g['row'] = ys.index(round(g['y'], 2))
W, H = geo[1]['w'], geo[1]['h']
def adjacent(a, b):                                                        # rook neighbours: next column in the same row, or next row in the same column, same block
    ga, gb = geo[a], geo[b]
    same_block = GT.block[a - 1] == GT.block[b - 1]
    return same_block and ((ga['row'] == gb['row'] and abs(ga['x'] - gb['x']) < 1.3 * W) or (ga['col'] == gb['col'] and abs(ga['y'] - gb['y']) < 2.6 * H))
Wm = np.array([[1.0 if a != b and adjacent(a, b) else 0.0 for b in range(1, NP + 1)] for a in range(1, NP + 1)])

# ---------------- plot table
def pred(t, model, v): return PF[(PF.task == t) & (PF.model == model) & (PF.variant == v)].sort_values('plot')
tab = GT[['plot', 'block', 'status', 'variety', 'sowing', 'stage', 'A', 'grade', 'score', 'PDI']].copy()
tab['col'] = [geo[p]['col'] for p in tab['plot']]; tab['row'] = [geo[p]['row'] for p in tab['plot']]
for t, key in (('A', 'A'), ('B', 'B'), ('C', 'C')):
    for v in VAR:
        d = pred(t, best[t]['overall'], v); tab['%s_%s' % (key, VSH[v])] = d.pred.values
        if t == 'A': tab['A_%s_score' % VSH[v]] = d.score.values
    u = PU[PU.task == t].sort_values('plot'); tab['%s_uav' % key] = u.pred.values
    if t == 'A': tab['A_uav_score'] = u.score.values
MX = pd.read_csv(T + 'maxstat.csv').set_index('task'); top = MX.loc['A']
dtop = pred('A', top.model, top.variant); tab['A_top'] = dtop.pred.values; tab['A_top_score'] = dtop.score.values
cat = lambda y, p: np.where((y == 1) & (p == 1), 'TP', np.where((y == 0) & (p == 0), 'TN', np.where((y == 0) & (p == 1), 'FP', 'FN')))
gi = {g: i for i, g in enumerate(GR)}
tab['A_top_cat'] = cat(tab.A.values, tab['A_top'].values.astype(int))
for tag in [VSH[v] for v in VAR] + ['uav']:
    tab['A_%s_cat' % tag] = cat(tab.A.values, tab['A_%s' % tag].values.astype(int))
    tab['B_%s_steps' % tag] = [gi[int(p)] - gi[int(y)] for p, y in zip(tab['B_%s' % tag], tab.grade)]
    tab['C_%s_res' % tag] = tab['C_%s' % tag] - tab.score
tab.to_csv(O + 'map_table.csv', index=False)

# ---------------- spatial autocorrelation of the errors (Moran's I, rook neighbours, permutation test)
rng = np.random.default_rng(42)
def moran(x, w=Wm):
    z = x - x.mean(); s0 = w.sum()
    return (len(x) / s0) * (z @ w @ z) / (z @ z) if (z @ z) > 0 else np.nan
def moran_test(x, n=999):
    I = moran(x); null = np.array([moran(rng.permutation(x)) for _ in range(n)])
    return I, -1 / (len(x) - 1), float((1 + np.sum(null >= I)) / (n + 1))
mrows = []
for tag, lab in [(VSH[v], 'Best ASD model, %s input' % VSH[v]) for v in VAR] + [('uav', 'UAV-trained model')]:
    for kind, x in (('C residual (pred - true score)', tab['C_%s_res' % tag].values.astype(float)), ('A error (1 = wrong)', (tab['A_%s_cat' % tag].isin(['FP', 'FN'])).astype(float).values),
                    ('B grade steps (pred - true)', tab['B_%s_steps' % tag].values.astype(float))):
        I, EI, p = moran_test(x); mrows.append(dict(model=lab, tag=tag, variable=kind, moran_I=I, expected_I=EI, p_value=p))
dmask = (tab.status == 'Diseased').values; Wd = Wm[np.ix_(dmask, dmask)]
def moran_test_d(x, n=999):
    I = moran(x, Wd); null = np.array([moran(rng.permutation(x), Wd) for _ in range(n)]); return I, -1 / (len(x) - 1), float((1 + np.sum(null >= I)) / (n + 1))
for tag, lab in [(VSH[v], 'Best ASD model, %s input' % VSH[v]) for v in VAR] + [('uav', 'UAV-trained model')]:
    I, EI, p = moran_test_d(tab['C_%s_res' % tag].values[dmask].astype(float)); mrows.append(dict(model=lab, tag=tag, variable='C residual, diseased plots only', moran_I=I, expected_I=EI, p_value=p))
I, EI, p = moran_test_d(tab.score.values[dmask]); mrows.append(dict(model='Ground truth', tag='truth', variable='True score, diseased plots only', moran_I=I, expected_I=EI, p_value=p))
I, EI, p = moran_test((tab['A_top_cat'].isin(['FP', 'FN'])).astype(float).values); mrows.append(dict(model='Best-transferring frozen model (%s, %s input)' % (top.model, VSH[top.variant]), tag='top', variable='A error (1 = wrong)', moran_I=I, expected_I=EI, p_value=p))
for kind, x in (('True plot mean score', tab.score.values), ('True PDI', tab.PDI.values)):
    I, EI, p = moran_test(x); mrows.append(dict(model='Ground truth', tag='truth', variable=kind, moran_I=I, expected_I=EI, p_value=p))
MO = pd.DataFrame(mrows); MO.to_csv(O + 'moran.csv', index=False)

# ---------------- summaries by block, sowing date and variety
def summ(by):
    rows = []
    for tag, lab in [(bv['A'] and VSH[bv['A']], 'Best ASD (%s input)' % VSH[bv['A']]), ('uav', 'UAV-trained')]:
        for g, d in tab.groupby(by):
            rows.append(dict(group=g, model=lab, n=len(d), mean_true_score=d.score.mean(), A_accuracy=(d['A_%s_cat' % tag].isin(['TP', 'TN'])).mean(),
                             B_within1=(d['B_%s_steps' % (VSH[bv['B']] if tag != 'uav' else 'uav')].abs() <= 1).mean(),
                             C_mean_residual=d['C_%s_res' % (VSH[bv['C']] if tag != 'uav' else 'uav')].mean(), C_mean_pred=d['C_%s' % (VSH[bv['C']] if tag != 'uav' else 'uav')].mean()))
    return pd.DataFrame(rows)
SB = {k: summ(k) for k in ('block', 'sowing', 'variety')}
for k, d in SB.items(): d.to_csv(O + 'summary_by_%s.csv' % k, index=False)

# ---------------- maps
def draw(ax, values, kind, title, cmap=None, norm=None, labels=True, fmt='%.1f'):
    for p in range(1, NP + 1):
        g = geo[p]; v = values[p - 1]
        if kind == 'cat': fc = cmap[v]
        else: fc = cmap(norm(v)) if np.isfinite(v) else '#DDDDDD'
        ax.add_patch(Rectangle((g['x'], -g['y']), g['w'] * 0.96, -g['h'] * 0.94, fc=fc, ec='#555555', lw=0.5))
        if labels:
            txt = ('%d' % p) + ('\n' + (str(v) if kind == 'cat' else (fmt % v)) if v is not None else '')
            lum = 0.5 if kind == 'cat' else np.mean(matplotlib.colors.to_rgb(fc)) if not isinstance(fc, str) else 0.6
            ax.text(g['x'] + g['w'] * 0.48, -g['y'] - g['h'] * 0.47, txt, ha='center', va='center', fontsize=5.2, color='white' if (kind != 'cat' and lum < 0.45) else 'black')
    for blk, x0, x1 in (('Healthy', 'C', None), ('R3', 'R3', None), ('R2', 'R2', None), ('R1', 'R1', None)):
        ps = [p for p in range(1, NP + 1) if GT.block[p - 1] == x0]
        xm = np.mean([geo[p]['x'] + geo[p]['w'] / 2 for p in ps]); ym = max(geo[p]['y'] + geo[p]['h'] for p in ps)
        ax.text(xm, -ym - 0.18, blk, ha='center', va='top', fontsize=6.5, fontweight='bold')
    ax.set_xlim(min(g['x'] for g in geo.values()) - 0.1, max(g['x'] + g['w'] for g in geo.values()) + 0.1)
    ax.set_ylim(-max(g['y'] + g['h'] for g in geo.values()) - 0.5, -min(g['y'] for g in geo.values()) + 0.1)
    ax.set_aspect('equal'); ax.axis('off'); ax.set_title(title, loc='left')
def cbar(fig, ax, cmap, norm, label):
    sm = plt.cm.ScalarMappable(cmap=cmap, norm=norm); sm.set_array([]); c = fig.colorbar(sm, ax=ax, fraction=0.025, pad=0.01); c.set_label(label, fontsize=7); c.ax.tick_params(labelsize=6)
SCM = plt.get_cmap('YlOrRd'); SNORM = Normalize(0, 9); RCM = plt.get_cmap('RdBu_r'); RNORM = Normalize(-4, 4)
GCM = ListedColormap(['#1A9850', '#FEE08B', '#FDAE61', '#F46D43', '#D73027', '#7F0000']); GNORM = BoundaryNorm([-0.5, 0.5, 2, 4, 6, 8, 9.5], 6)
STC = {0: '#1A9850', 1: '#D73027'}; CATC = {'TP': '#D73027', 'TN': '#1A9850', 'FP': '#FDAE61', 'FN': '#4575B4'}
def save(f, n):
    f.subplots_adjust(wspace=0.35, hspace=0.25); f.savefig(FG + n); plt.close(f)
def gmap(values):           # grade values on the 0..9 scale for the grade colour map
    return np.array(values, float)

# m01 ground truth
f, axs = plt.subplots(1, 3, figsize=(15, 3.6))
draw(axs[0], [int(a) for a in tab.A], 'cat', 'a  True status (0 healthy, 1 diseased)', {0: STC[0], 1: STC[1]})
draw(axs[1], tab.score.values, 'num', 'b  True mean leaf score (0–9)', SCM, SNORM); cbar(f, axs[1], SCM, SNORM, 'score')
draw(axs[2], gmap(tab.grade), 'num', 'c  True grade', GCM, GNORM, fmt='%.0f'); cbar(f, axs[2], GCM, GNORM, 'grade')
save(f, 'm01_truth.png')
# m02 best ASD model (best input per task): predictions
f, axs = plt.subplots(1, 3, figsize=(15, 3.6))
draw(axs[0], [int(a) for a in tab['A_%s' % VSH[bv['A']]]], 'cat', 'a  Predicted status: %s (%s input)' % (best['A']['overall'], VSH[bv['A']]), {0: STC[0], 1: STC[1]})
draw(axs[1], gmap(tab['B_%s' % VSH[bv['B']]]), 'num', 'b  Predicted grade: %s (%s input)' % (best['B']['overall'], VSH[bv['B']]), GCM, GNORM, fmt='%.0f'); cbar(f, axs[1], GCM, GNORM, 'grade')
draw(axs[2], tab['C_%s' % VSH[bv['C']]].values, 'num', 'c  Predicted score: %s (%s input)' % (best['C']['overall'], VSH[bv['C']]), SCM, SNORM); cbar(f, axs[2], SCM, SNORM, 'score')
save(f, 'm02_pred_best.png')
# m03 best ASD model: error maps
f, axs = plt.subplots(1, 3, figsize=(15, 3.6))
draw(axs[0], list(tab['A_%s_cat' % VSH[bv['A']]]), 'cat', 'a  Detection outcome', CATC)
draw(axs[1], tab['B_%s_steps' % VSH[bv['B']]].values.astype(float), 'num', 'b  Grade error (steps)', RCM, Normalize(-5, 5), fmt='%+.0f'); cbar(f, axs[1], RCM, Normalize(-5, 5), 'steps')
draw(axs[2], tab['C_%s_res' % VSH[bv['C']]].values, 'num', 'c  Score error (pred − true)', RCM, RNORM, fmt='%+.1f'); cbar(f, axs[2], RCM, RNORM, 'score units')
save(f, 'm03_err_best.png')
# m04 predicted score for the three inputs + UAV-trained
f, axs = plt.subplots(2, 2, figsize=(11, 6.6))
for ax, (tag, ttl) in zip(axs.ravel(), [(VSH[v], '%s, %s input' % (best['C']['overall'], VSH[v])) for v in VAR] + [('uav', 'UAV-trained %s (LORO)' % PU[PU.task == 'C'].model.iloc[0])]):
    draw(ax, tab['C_%s' % tag].values, 'num', 'Predicted score: ' + ttl, SCM, SNORM)
cbar(f, axs.ravel().tolist(), SCM, SNORM, 'predicted score (0–9)')
save(f, 'm04_score_variants.png')
# m05 UAV-trained maps and errors
f, axs = plt.subplots(2, 3, figsize=(15, 6.8))
draw(axs[0, 0], [int(a) for a in tab.A_uav], 'cat', 'a  Predicted status (UAV-trained %s)' % PU[PU.task == 'A'].model.iloc[0], {0: STC[0], 1: STC[1]})
draw(axs[0, 1], gmap(tab.B_uav), 'num', 'b  Predicted grade (UAV-trained %s)' % PU[PU.task == 'B'].model.iloc[0], GCM, GNORM, fmt='%.0f'); cbar(f, axs[0, 1], GCM, GNORM, 'grade')
draw(axs[0, 2], tab.C_uav.values, 'num', 'c  Predicted score (UAV-trained %s)' % PU[PU.task == 'C'].model.iloc[0], SCM, SNORM); cbar(f, axs[0, 2], SCM, SNORM, 'score')
draw(axs[1, 0], list(tab.A_uav_cat), 'cat', 'd  Detection outcome', CATC)
draw(axs[1, 1], tab.B_uav_steps.values.astype(float), 'num', 'e  Grade error (steps)', RCM, Normalize(-5, 5), fmt='%+.0f'); cbar(f, axs[1, 1], RCM, Normalize(-5, 5), 'steps')
draw(axs[1, 2], tab.C_uav_res.values, 'num', 'f  Score error', RCM, RNORM, fmt='%+.1f'); cbar(f, axs[1, 2], RCM, RNORM, 'score units')
save(f, 'm05_uav_trained.png')
# m06 detection probability map (best ASD model, best input) and UAV-trained score
f, axs = plt.subplots(1, 2, figsize=(11, 3.6))
sA = tab['A_%s_score' % VSH[bv['A']]].values.astype(float); sU = tab.A_uav_score.values.astype(float)
PN = Normalize(np.nanmin(sA), np.nanmax(sA)); draw(axs[0], sA, 'num', 'a  Disease score of %s (%s input)' % (best['A']['overall'], VSH[bv['A']]), plt.get_cmap('RdYlGn_r'), PN, fmt='%.2f'); cbar(f, axs[0], plt.get_cmap('RdYlGn_r'), PN, 'decision value / probability')
PN2 = Normalize(np.nanmin(sU), np.nanmax(sU)); draw(axs[1], sU, 'num', 'b  Disease score of the UAV-trained model', plt.get_cmap('RdYlGn_r'), PN2, fmt='%.2f'); cbar(f, axs[1], plt.get_cmap('RdYlGn_r'), PN2, 'decision value / probability')
save(f, 'm06_disease_score.png')
f, axs = plt.subplots(1, 3, figsize=(15, 3.6))
draw(axs[0], [int(a) for a in tab.A_top], 'cat', 'a  Predicted status: %s (%s input)' % (top.model, VSH[top.variant]), {0: STC[0], 1: STC[1]})
draw(axs[1], list(tab.A_top_cat), 'cat', 'b  Detection outcome', CATC)
sT = tab.A_top_score.values.astype(float); PN3 = Normalize(np.nanmin(sT), np.nanmax(sT)); draw(axs[2], sT, 'num', 'c  Probability of disease', plt.get_cmap('RdYlGn_r'), PN3, fmt='%.2f'); cbar(f, axs[2], plt.get_cmap('RdYlGn_r'), PN3, 'probability')
save(f, 'm08_best_transfer_detection.png')
# m07 block / sowing summaries
f, axs = plt.subplots(1, 3, figsize=(13, 3.4))
for ax, k, ttl in zip(axs, ('block', 'sowing', 'variety'), ('a  By block', 'b  By sowing date', 'c  By variety')):
    d = SB[k]; gs = list(dict.fromkeys(d.group)); x = np.arange(len(gs)); w = 0.38
    for j, (mdl, col) in enumerate(zip(d.model.unique(), ['#4C72B0', '#2CA02C'])):
        dd = d[d.model == mdl].set_index('group').loc[gs]; ax.bar(x + (j - 0.5) * w, dd.C_mean_residual, w, color=col, label=mdl)
    ax.axhline(0, color='k', lw=0.6); ax.set_xticks(x); ax.set_xticklabels(gs); ax.set_title(ttl, loc='left'); ax.set_ylabel('mean score error (pred − true)')
axs[0].legend(fontsize=6.5, frameon=False)
save(f, 'm07_group_errors.png')
json.dump(dict(top_model=top.model, top_variant=top.variant, top_macro_F1=float(top.observed), top_p=float(top.p_value), top_ci=[float(top.ci_lo), float(top.ci_hi)], top_AUC=float(top.AUC), best=best, best_variant=bv, n_plots=NP, n_neighbour_pairs=int(Wm.sum() / 2), uav_models={t: PU[PU.task == t].model.iloc[0] for t in 'ABC'}), open(O + 'map_summary.json', 'w'), indent=1)
pd.DataFrame(Wm.astype(int), index=range(1, NP + 1), columns=range(1, NP + 1)).to_csv(O + 'neighbours.csv')
print('maps saved', sorted(os.listdir(FG))); print(MO.round(3).to_string(index=False))
