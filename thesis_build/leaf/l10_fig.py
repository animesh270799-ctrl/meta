"""Figures for the full-range WRI comparison (l10_wri_full.py)."""
import numpy as np, pandas as pd, json, os
import matplotlib; matplotlib.use('Agg')
import matplotlib.pyplot as plt
B = os.path.dirname(os.path.abspath(__file__)) + '/'; D = B + 'data/'; FG = B + 'fig/'
plt.rcParams.update({'font.family': 'DejaVu Sans', 'font.size': 9})
GL = ['0', '1', '3', '5', '7', '9']; GC = ['#2E7D32', '#9CCC65', '#FDD835', '#FB8C00', '#E53935', '#7B1FA2']; G6 = [0, 1, 3, 5, 7, 9]
W = json.load(open(D + 'wri_full.json')); V = np.load(D + 'wri_full_vals.npz'); M = pd.read_csv(D + 'meta_leaf2.csv'); y = M.grade.values
C = pd.DataFrame(W['comparison']); names = C.Index.tolist()
short = {n: n.split(' (')[0] for n in names}
# ---------- (a) ReliefF weights over 400-2400 nm, (b-e) the four WRIs by grade ----------
fig = plt.figure(figsize=(13, 6.6)); gs = fig.add_gridspec(2, 4, height_ratios=[1, 1.15])
a = fig.add_subplot(gs[0, :]); bands = np.array(W['bands_full']); wb = np.array(W['wb_full'])
a.plot(bands, wb, color='#00695C', lw=1.2)
for lo, hi in ((1350, 1450), (1800, 1950)): a.axvspan(lo, hi, color='#90CAF9', alpha=0.35, lw=0)
a.text(1400, wb.max() * 0.95, 'water band\n(kept)', ha='center', fontsize=8, color='#1565C0'); a.text(1875, wb.max() * 0.95, 'water band\n(kept)', ha='center', fontsize=8, color='#1565C0')
d = W['indices'][names[3]][1]
for w_, lab, c, ha, hy in ((d['l1'], 'λ1', '#AD1457', 'left', 0.05), (d['l2'], 'λ2', '#AD1457', 'left', 0.05), (d['l3'], 'λ3', '#C98A00', 'right', 0.18)):
    if w_ is not None: a.axvline(w_, color=c, ls='--', lw=1); a.text(w_ + (8 if ha == 'left' else -8), wb.min() + hy * (wb.max() - wb.min()), '%s = %d' % (lab, w_), color=c, fontsize=8, ha=ha)
a.set_xlim(400, 2400); a.set_xlabel('Wavelength (nm)'); a.set_ylabel('ReliefF weight')
a.set_title('(a) ReliefF weights of single bands, 400–2400 nm (healthy vs diseased); dashed: bands of WRI-FULL = %s' % W['indices'][names[3]][0], fontsize=9.5)
for i, n in enumerate(names[:4]):
    ax = fig.add_subplot(gs[1, i]); v = V['leaf_%d' % i]
    bp = ax.boxplot([v[y == g] for g in G6], tick_labels=GL, patch_artist=True, showfliers=False, medianprops=dict(color='k'))
    for b_, c in zip(bp['boxes'], GC): b_.set_facecolor(c)
    lt = W['letters'][n]; lo, hi = ax.get_ylim(); ax.set_ylim(lo, hi + 0.12 * (hi - lo))
    for j, g in enumerate(GL): ax.text(j + 1, hi + 0.03 * (hi - lo), lt[g], ha='center', fontsize=8, fontweight='bold')
    r = C.iloc[i]; ax.set_title('(%s) %s\n%s\nBA %.3f, AUC %.3f, r$_{PDI}$ %.2f' % ('bcde'[i], short[n], W['indices'][n][0], r.BA_CV, r.AUC, r.r_PDI), fontsize=8.5)
    ax.set_xlabel('Leaf grade')
    if i == 0: ax.set_ylabel('Index value')
plt.tight_layout(); plt.savefig(FG + 'l_wri_full.png', dpi=200); plt.close()
print('fig ok')
