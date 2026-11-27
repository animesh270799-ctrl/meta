"""300-dpi figures for the Word report, drawn from the same chart specifications (d2_specs) and tables as the Excel and PPT charts,
plus the figures that have no native chart form (workflow, R² maps, JM and confusion heat maps)."""
import os, sys, json, pickle, numpy as np, pandas as pd, matplotlib
matplotlib.use('Agg'); import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE); sys.path.insert(0, os.path.join(HERE, '..'))
import d2_specs as D, configL as C
plt.rcParams.update({'font.family': 'DejaVu Sans', 'font.size': 9, 'axes.titlesize': 10, 'axes.titleweight': 'bold', 'savefig.dpi': 300, 'savefig.bbox': 'tight', 'axes.spines.top': False, 'axes.spines.right': False,
                     'axes.grid': True, 'grid.color': '#E5E5E5', 'grid.linewidth': 0.6, 'legend.frameon': False, 'legend.fontsize': 8})
T = pickle.load(open(os.path.join(HERE, 'tables.pkl'), 'rb')); F = json.load(open(os.path.join(HERE, 'facts.json'))); FG = os.path.join(HERE, 'fig')
hx = lambda c: '#' + c
def draw(s):
    d = s['data']; x = d.iloc[:, 0]; fig, ax = plt.subplots(figsize=s.get('size', (7.2, 3.6))); n = len(s['series'])
    if s['kind'] == 'line':
        for c, col in zip(s['series'], s['colors']): ax.plot(x, d[c], color=hx(col), lw=1.4, label=c, marker='o' if s.get('markers') else None, ms=3)
    elif s['kind'] == 'scatter':
        for c, col in zip(s['series'], s['colors']):
            m = d[c].notna()
            if c in s.get('line_series', []): ax.plot(x[m], d[c][m], color=hx(col), lw=1.3 if 'ellipse' not in c else 1.0, label=None if 'ellipse' in c else c, ls='--' if c in ('Chance', '1:1 line') else '-')
            else: ax.scatter(x[m], d[c][m], s=9 if m.sum() > 60 else 28, color=hx(col), label=c, alpha=0.6 if m.sum() > 60 else 1, edgecolor='none' if m.sum() > 60 else 'k', linewidth=0.4)
    elif s['kind'] in ('col', 'bar'):
        bars = [c for c in s['series'] if c not in s.get('line_series', [])]; k = np.arange(len(d)); wdt = 0.8 / len(bars)
        for i, (c, col) in enumerate(zip(bars, s['colors'])):
            pos = k - 0.4 + wdt * (i + 0.5); cols = [hx(p) for p in s['point_colors']] if s.get('point_colors') and len(bars) == 1 else hx(col)
            h = (ax.barh if s['kind'] == 'bar' else ax.bar)(pos, d[c], wdt * 0.92, color=cols, label=c)
            if s.get('labels'):
                for p_, v in zip(pos, d[c]):
                    if pd.notna(v): (ax.text(v, p_, ' %s' % fmt(v), va='center', fontsize=7) if s['kind'] == 'bar' else ax.text(p_, v, fmt(v), ha='center', va='bottom', fontsize=7))
        for c, col in zip(s['series'], s['colors']):
            if c in s.get('line_series', []): ax.plot(k, d[c], color=hx(col), marker='o', label=c)
        (ax.set_yticks if s['kind'] == 'bar' else ax.set_xticks)(k); (ax.set_yticklabels if s['kind'] == 'bar' else ax.set_xticklabels)([str(v) for v in x], rotation=0 if s['kind'] == 'bar' or len(d) < 8 else 45, ha='right' if (s['kind'] == 'col' and len(d) >= 8) or s['kind'] == 'bar' else 'center', fontsize=8)
        if s['kind'] == 'bar': ax.grid(axis='y', visible=False)
        else: ax.grid(axis='x', visible=False)
    ax.set_xlabel(s['xlab'] if s['kind'] != 'bar' else s['ylab']); ax.set_ylabel(s['ylab'] if s['kind'] != 'bar' else s['xlab']); ax.set_title(s['title'], loc='left')
    if n > 1 or s['kind'] == 'scatter': ax.legend(ncol=min(n, 4) if n > 3 else 1, loc='best')
    fig.savefig(os.path.join(FG, s['id'] + '.png')); plt.close(fig)
def fmt(v): return '%d' % v if float(v).is_integer() and abs(v) >= 10 else ('%.3f' % v if abs(v) < 10 else '%.1f' % v)
SP = D.specs(T, F)
for s in SP: draw(s)
# ---------------- special figures
def heat(A, w, title, f, thr):
    fig, ax = plt.subplots(figsize=(4.6, 4.0)); im = ax.imshow(A, origin='lower', extent=[w[0], w[-1], w[0], w[-1]], cmap='viridis', vmin=0, vmax=np.nanmax(A))
    ax.contour(w, w, np.nan_to_num(A), levels=[thr], colors='w', linewidths=0.6); ax.set_xlabel('λ2 (nm)'); ax.set_ylabel('λ1 (nm)'); ax.set_title(title, loc='left'); ax.grid(False)
    plt.colorbar(im, ax=ax, shrink=0.85, label='R² with grade'); fig.savefig(os.path.join(FG, f)); plt.close(fig)
O = C.OUT; w5 = np.load(os.path.join(O, 'L3_spectra.npz'))['w5']; Nm = np.load(os.path.join(O, 'L5_2_NDSI_R2.npy')); Rm = np.load(os.path.join(O, 'L5_2_RSI_R2.npy'))
heat(Nm, w5, 'NDSI R² map (training leaves)', 'h01_ndsi.png', F['l52']['thr']['NDSI']); heat(Rm, w5, 'RSI R² map (training leaves)', 'h02_rsi.png', F['l52']['thr']['RSI'])
def mat(M, lab, title, f, fmtc='%.2f', cmap='YlOrRd', vmax=None, xl='', yl=''):
    fig, ax = plt.subplots(figsize=(4.4, 3.8)); im = ax.imshow(M, cmap=cmap, vmin=0, vmax=vmax or np.nanmax(M)); ax.grid(False)
    ax.set_xticks(range(len(lab))); ax.set_yticks(range(len(lab))); ax.set_xticklabels(lab); ax.set_yticklabels(lab); ax.set_xlabel(xl); ax.set_ylabel(yl); ax.set_title(title, loc='left')
    for i in range(M.shape[0]):
        for j in range(M.shape[1]): ax.text(j, i, fmtc % M[i, j], ha='center', va='center', fontsize=7, color='w' if M[i, j] > 0.6 * (vmax or np.nanmax(M)) else 'k')
    plt.colorbar(im, ax=ax, shrink=0.8); fig.savefig(os.path.join(FG, f)); plt.close(fig)
mat(T['l56_matrix'].values, [str(g) for g in D.GR], 'Jeffries–Matusita distance (task-B DSF)', 'h03_jm.png', vmax=2, xl='Grade', yl='Grade')
if 'l7_conf' in T:
    cf = T['l7_conf']
    for t, lab in (('A', ['Healthy', 'Diseased']), ('B', [str(g) for g in D.GR])):
        m = F['best'][t]; q = cf[(cf.task == t) & (cf.model == m)]; K = len(lab); A = np.zeros((K, K))
        for _, r in q.iterrows(): A[int(r.observed), int(r.predicted)] = r.n
        mat(A, lab, 'Confusion matrix, task %s (%s)' % (t, m), 'h04_conf_%s.png' % t, '%d', 'Blues', xl='Predicted', yl='Observed')
# workflow (snake layout: row 1 left to right, row 2 right to left, row 3 left to right)
fig, ax = plt.subplots(figsize=(8.0, 4.9)); ax.axis('off'); ax.set_xlim(0, 10); ax.set_ylim(0.3, 6.5)
X4 = [0.1, 2.6, 5.1, 7.6]; BW, BH = 2.25, 1.0; Y3 = [5.3, 3.5, 1.7]
rows = [['L1 Leaf table + checks\n2339 → 2255 leaves', 'L2 Split by plot\n33 train / 15 test plots', 'L3 SG 11/2, 400–2400 nm\nFD, 5-nm bands', 'L4 48 indices\n+ REP, Dr, SDr'],
        ['L5.5 VIF < 10 → DSF\nL5.6 JM · L5.7 PCA', 'L5.3–L5.4 NDSI, RSI, WRI\n|r| filter + ReliefF → VI', 'L5.2 R² maps, SHAP-CARS\n→ 32 optimal wavelengths', 'L5.1 Response curves\n(all leaves)'],
        ['L6 ML: SFFS + grid\n4 models × 3 tasks', 'L6 Networks\nDNN-F1 + 4 image nets', 'L7 Test metrics\n684 test leaves (once)', 'L8 Covariate baseline\nL9 Leaf–UAV link']]
cols = ['E8F1FA', 'EAF5E4', 'F6E6F0']
for r, (y, labs) in enumerate(zip(Y3, rows)):
    for x, t in zip(X4, labs):
        ax.add_patch(FancyBboxPatch((x, y), BW, BH, boxstyle='round,pad=0.03,rounding_size=0.12', fc='#' + (cols[r] if not t.startswith('L5.1') else 'FFF4DC'), ec='#555555', lw=0.8))
        ax.text(x + BW / 2, y + BH / 2, t, ha='center', va='center', fontsize=7.2)
arr = lambda x1, y1, x2, y2: ax.annotate('', xy=(x2, y2), xytext=(x1, y1), arrowprops=dict(arrowstyle='->', color='#444444', lw=1))
for i in range(3):
    arr(X4[i] + BW + 0.02, Y3[0] + BH / 2, X4[i + 1] - 0.02, Y3[0] + BH / 2); arr(X4[i + 1] - 0.02, Y3[1] + BH / 2, X4[i] + BW + 0.02, Y3[1] + BH / 2); arr(X4[i] + BW + 0.02, Y3[2] + BH / 2, X4[i + 1] - 0.02, Y3[2] + BH / 2)
arr(X4[3] + BW / 2, Y3[0] - 0.02, X4[3] + BW / 2, Y3[1] + BH + 0.02); arr(X4[0] + BW / 2, Y3[1] - 0.02, X4[0] + BW / 2, Y3[2] + BH + 0.02)
ax.text(5, 0.95, 'L5.2–L5.6 selection and all model fitting use the 1571 training leaves only; L5.1 and L5.7 describe all 2255 leaves;\nthe 684 test leaves (15 plots) are predicted once at L7.', ha='center', va='center', fontsize=7.4, style='italic')
ax.set_title('Order of the Part L steps applied to the 2025-26 ASD leaf data', loc='left'); fig.savefig(os.path.join(FG, 'w01_workflow.png')); plt.close(fig)
json.dump([dict(id=s['id'], title=s['title'], sheet=s['sheet'], note=s['note']) for s in SP], open(os.path.join(HERE, 'figlist.json'), 'w'), indent=1)
print('figures', len(SP) + 4, 'written to', FG)
