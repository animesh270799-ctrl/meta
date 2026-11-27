"""New figures of the step-by-step protocol document (data flow, split search, inner folds, step x data matrix).
All numbers are read from the 70:30 pipeline (asd7030/data); nothing is typed by hand except box labels."""
import os, sys, json, numpy as np, pandas as pd
import matplotlib; matplotlib.use('Agg'); import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, Rectangle, Patch
from sklearn.model_selection import GroupKFold
T = '/home/user/meta/thesis_build/'; A = T + 'asd7030/'; D = A + 'data/'; OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'fig/')
os.makedirs(OUT, exist_ok=True); sys.path.insert(0, A)
import split_lib as SL
plt.rcParams.update({'font.family': 'Liberation Sans', 'font.size': 11})
M = pd.read_csv(D + 'meta.csv'); SPJ = json.load(open(D + 'split.json')); TE = set(SPJ['test_plots'])
tr = (M.fold == 1).values; plots = M['plot'].values
# ---------------- inner GroupKFold(3) of the training plots (exactly as in a3_ml.py) ----------------
inner = list(GroupKFold(3).split(np.zeros(tr.sum()), groups=plots[tr]))
ptr = plots[tr]; IF = {}
for k, (_, va) in enumerate(inner):
    for p in np.unique(ptr[va]): IF[int(p)] = k + 1
# ---------------- validation plots of the networks (exactly as in a4_dl.py, seed 42) ----------------
rng = np.random.default_rng(42); VAL = set(int(v) for v in rng.choice(np.unique(ptr), len(np.unique(ptr)) // 3, replace=False))
info = dict(inner={k + 1: dict(plots=sorted(int(p) for p in np.unique(ptr[va])), n_val=int(len(va)), n_fit=int(len(ptr) - len(va))) for k, (_, va) in enumerate(inner)},
            val_plots=sorted(VAL), n_val=int(M[tr & M['plot'].isin(VAL).values].shape[0]), n_fit=int(M[tr & ~M['plot'].isin(VAL).values].shape[0]))
for k, d in info['inner'].items():
    sub = M[M['plot'].isin(d['plots'])]; d['blocks'] = sub.groupby('block')['plot'].nunique().to_dict()
json.dump(info, open(OUT + 'inner_info.json', 'w'), indent=1)
print(json.dumps(info))

LAY = {}
exec(open(A + 'a1_prep.py').read().split('blk = lambda')[0].split('# ---- treatments')[1].split('\n', 1)[1])
BLOCKS = [('Healthy (sprayed) 1–12', range(1, 13)), ('R3 13–24', range(13, 25)), ('R2 25–36', range(25, 37)), ('R1 37–48', range(37, 49))]
def plotmap(ax, colour_of, title):
    for bi, (bn, rg) in enumerate(BLOCKS):
        for j, p in enumerate(rg):
            c = colour_of(p); ax.add_patch(Rectangle((j, -bi), 0.92, 0.82, facecolor=c, edgecolor='#555', lw=0.6))
            dark = c in ('#404040', '#1F4E79', '#2E75B6', '#C55A11', '#548235', '#7030A0')
            ax.text(j + 0.46, -bi + 0.53, str(p), ha='center', va='center', fontsize=8.5, color='white' if dark else '#222', fontweight='bold')
            ax.text(j + 0.46, -bi + 0.2, LAY[p], ha='center', va='center', fontsize=6.5, color='white' if dark else '#444')
        ax.text(-0.25, -bi + 0.41, bn, ha='right', va='center', fontsize=9.5)
    ax.set_xlim(-0.1, 12); ax.set_ylim(-3.3, 1.0); ax.axis('off'); ax.set_title(title, fontsize=11.5, loc='left')

FC = {1: '#2E75B6', 2: '#C55A11', 3: '#548235'}
fig, axs = plt.subplots(2, 1, figsize=(11, 7.4))
plotmap(axs[0], lambda p: '#404040' if p in TE else FC[IF[p]], '(a) Machine learning: inner GroupKFold(3) of the 33 training plots (colour = inner fold in which the plot is the validation part)')
axs[0].legend([Patch(color=FC[1]), Patch(color=FC[2]), Patch(color=FC[3]), Patch(color='#404040')],
              ['inner fold 1 (%d plots, %d leaves)' % (len(info['inner'][1]['plots']), info['inner'][1]['n_val']), 'inner fold 2 (%d plots, %d leaves)' % (len(info['inner'][2]['plots']), info['inner'][2]['n_val']),
               'inner fold 3 (%d plots, %d leaves)' % (len(info['inner'][3]['plots']), info['inner'][3]['n_val']), 'test plot (locked, not used)'], loc='lower center', bbox_to_anchor=(0.5, -0.2), ncol=4, fontsize=9, frameon=False)
plotmap(axs[1], lambda p: '#404040' if p in TE else ('#7030A0' if p in VAL else '#E4D7F0'), '(b) Deep learning: 22 fitting plots (light) and 11 validation plots for early stopping (purple)')
axs[1].legend([Patch(facecolor='#E4D7F0', edgecolor='#555'), Patch(color='#7030A0'), Patch(color='#404040')],
              ['fitting plots (%d leaves)' % info['n_fit'], 'validation plots (%d leaves)' % info['n_val'], 'test plot (locked, not used)'], loc='lower center', bbox_to_anchor=(0.5, -0.2), ncol=3, fontsize=9, frameon=False)
plt.tight_layout(h_pad=2.2); fig.savefig(OUT + 'p03_inner_folds.png', dpi=200, bbox_inches='tight'); plt.close(fig)

# ---------------- split search: scores of the 5000 candidates ----------------
C = SL.candidates(M, 0.30, 5000, 2026); sc = SL._Scorer(M, 0.30); S = np.array([sc(c) for c in C]); i = int(np.argmin(S))
assert sorted(C[i]) == sorted(SPJ['test_plots']), 'split search does not reproduce split.json'
frac = np.array([M['plot'].isin(c).mean() for c in C])
fig, axs = plt.subplots(1, 2, figsize=(11, 3.9))
axs[0].hist(S, bins=60, color='#9DC3E6', edgecolor='white'); axs[0].axvline(S[i], color='#C00000', lw=2); axs[0].axvline(np.median(S), color='#404040', ls='--', lw=1.2)
axs[0].text(S[i] + 0.001, axs[0].get_ylim()[1] * 0.9, 'chosen split\nscore %.4f' % S[i], color='#C00000', fontsize=9.5, va='top')
axs[0].text(np.median(S) + 0.001, axs[0].get_ylim()[1] * 0.6, 'median %.4f' % np.median(S), color='#404040', fontsize=9.5)
axs[0].set_xlabel('distance score (lower = closer to 30% and to the overall grade/date mix)'); axs[0].set_ylabel('number of candidate splits')
axs[0].set_title('(a) %d rule-conforming candidate splits (seed 2026)' % len(C), loc='left', fontsize=11.5)
axs[1].scatter(100 * frac, S, s=5, color='#9DC3E6', alpha=0.6); axs[1].scatter([100 * frac[i]], [S[i]], s=60, color='#C00000', zorder=3)
axs[1].axvline(30, color='#404040', ls='--', lw=1); axs[1].set_xlabel('test leaves (% of 2330)'); axs[1].set_ylabel('distance score')
axs[1].set_title('(b) leaf share of the test set vs score', loc='left', fontsize=11.5)
for a in axs: a.spines['top'].set_visible(False); a.spines['right'].set_visible(False)
plt.tight_layout(); fig.savefig(OUT + 'p02_split_search.png', dpi=200, bbox_inches='tight'); plt.close(fig)
json.dump(dict(n=len(C), best=float(S[i]), median=float(np.median(S)), p05=float(np.percentile(S, 5)), frac_min=float(frac.min()), frac_max=float(frac.max()), rank_pct=float((S <= S[i]).mean() * 100)),
          open(OUT + 'split_search.json', 'w'), indent=1)

# ---------------- data flow ----------------
fig, ax = plt.subplots(figsize=(11, 9.6)); ax.set_xlim(0, 100); ax.set_ylim(0, 100); ax.axis('off')
def box(x, y, w, h, txt, fc, ec='#333', fs=8.7, tc='#111'):
    ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle='round,pad=0.3,rounding_size=1.0', fc=fc, ec=ec, lw=1.1))
    lines = txt.split('\n'); n = len(lines); lh = 2.2
    for k, ln in enumerate(lines):
        ax.text(x + w / 2, y + h / 2 + (n - 1) * lh / 2 - k * lh, ln, ha='center', va='center', fontsize=fs + (0.5 if k == 0 else 0), fontweight='bold' if k == 0 else 'normal', color=tc)
def arr(pts, c='#333', ls='-'):
    for (x1, y1), (x2, y2) in zip(pts[:-2], pts[1:-1]): ax.plot([x1, x2], [y1, y2], color=c, lw=1.3, ls=ls)
    (x1, y1), (x2, y2) = pts[-2], pts[-1]
    ax.annotate('', xy=(x2, y2), xytext=(x1, y1), arrowprops=dict(arrowstyle='-|>', color=c, lw=1.3, ls=ls, shrinkA=0, shrinkB=0))
n_tr, n_te = SPJ['n_train_leaves'], SPJ['n_test_leaves']
L, Mx, R = 1.5, 35, 68.5; W = 31
box(26, 90, 48, 7, 'ALL  –  2330 leaf spectra, 48 plots, 4 dates\nSteps 1–4: experiment, spectra, grades, weather, data checks', '#F2F2F2')
box(L, 74.5, W, 11, 'Step 6  Pre-processing (all 2330)\nper leaf: smoothing, 400–2400 nm,\n1st derivative, 5-nm bands,\n41 indices + REP, Dr, REarea\n(nothing is learned from the data)', '#E2EFDA')
box(Mx, 74.5, W, 11, 'Step 5  Grouped, stratified 70:30 split\nwhole plots go to one side only;\nhealthy and unsprayed split separately;\nbest of 5000 candidates (seed 2026)', '#FFF2CC')
box(L, 58, W, 11.5, 'Step 7  Objective 1 description (all 2330)\nmean spectra, correlation, NDSI/RSI maps,\nSHAP-CARS, WRI, ReliefF, VIF\n= what the disease does to the spectrum\n(not used to train the models)', '#E2EFDA')
box(Mx, 58, W, 11.5, 'TRAIN  –  33 plots, %d leaves (70%%)\nhealthy 8; unsprayed R1 8, R2 8, R3 9\nused for EVERY learning step:\nselection, SFFS, tuning, fitting' % n_tr, '#DDEBF7')
box(R, 58, 30, 11.5, 'TEST  –  15 plots, %d leaves (30%%)\nhealthy 1, 4, 5, 8; unsprayed 13, 14,\n18, 25, 27, 31, 35, 37, 44, 46, 48\nLOCKED until Step 11' % n_te, '#404040', tc='white')
box(Mx, 43, W, 10.5, 'Step 8  Feature selection (TRAIN)\neffective ranges → SHAP-CARS (15 OW)\n→ NDSI/RSI/WRI → |r| ≥ 0.95 filter\n→ ReliefF top 5 → VIF < 10 → DSF', '#DDEBF7')
box(L, 27, W, 12.5, 'Step 9  Machine learning (TRAIN)\nscaler = mean/SD of the 1631 leaves\ninner GroupKFold(3) by plot\n(22 plots fit / 11 validate, 3 times)\nSFFS ≤ 15 → grid search → refit (33)', '#DDEBF7')
box(Mx, 27, W, 12.5, 'Step 10  Deep learning (TRAIN)\nfit: 22 plots, %d leaves\nvalidation: 11 plots, %d leaves\nAdamW, ≤ 100 epochs, patience 20\nbest-epoch network = final model' % (info['n_fit'], info['n_val']), '#DDEBF7')
box(L, 21, 64.5, 3.2, '30 trained models (15 machine-learning + 15 networks), all fitted on TRAIN only', '#FFE7E7', ec='#C00000', fs=8.5)
box(R, 30, 30, 21.5, 'Step 11  Test once (TEST)\nthe 30 models predict the\n%d test leaves one time\n\nmetrics: macro-F1, AUC, OA,\nkappa, QWK, R², RMSE, RPD\n\nuncertainty: 1000 bootstrap\nresamples of whole test plots' % n_te, '#FCE4D6')
box(R, 13.5, 30, 12, 'Steps 12–13\nconfigurations, ablation (TEST)\nstrata of TEST predictions\nSHAP, LOVO/LOTO transfer (ALL)\nselection stability', '#FCE4D6')
box(R, 0.5, 30, 9.5, 'Step 16  Deliverables\nthe tested models themselves\n(15 ML, 15 networks, 11 covariate)\nExcel, Word/PDF, slides', '#F2F2F2')
box(L, 0.5, W, 15.5, 'Step 14  Covariate baseline\nunsprayed leaves only, same split\ntrain %d (25 plots), test %d (11 plots)\nM0 covariates, M1 spectra, M2 both\n2000 plot-bootstrap resamples;\nDeLong test for AUC' % (int(((M.fold == 1) & (M.block != 'C')).sum()), int(((M.fold == 0) & (M.block != 'C')).sum())), '#EDE2F6')
box(Mx, 0.5, W, 15.5, 'Step 15  Comparison with LORO\n(1) side by side\n(2) same 699 test leaves: LORO vs 70:30\n(3) 20 other grouped 70:30 splits\n(4) 5 random leaf-level splits\n(3–4 with a light pipeline)', '#EDE2F6')
arr([(38, 90), (17, 85.8)]); arr([(55, 90), (50.5, 85.8)])
arr([(17, 74.5), (17, 69.8)]); arr([(50.5, 74.5), (50.5, 69.8)]); arr([(64, 74.5), (83.5, 69.8)])
arr([(50.5, 58), (50.5, 53.8)]); arr([(42, 43), (17, 39.8)]); arr([(50.5, 43), (50.5, 39.8)])
arr([(17, 27), (17, 24.5)], c='#C00000'); arr([(50.5, 27), (50.5, 24.5)], c='#C00000'); arr([(66, 22.6), (67, 22.6), (67, 35), (68.2, 35)], c='#C00000')
arr([(83.5, 58), (83.5, 51.8)], c='#C00000', ls='--'); arr([(83.5, 30), (83.5, 25.8)]); arr([(83.5, 13.5), (83.5, 10.3)])
ax.text(84.5, 55, 'opened once, at the end', fontsize=8.3, color='#C00000', va='center')
ax.text(18, 18.2, 'separate analyses on the same split (Steps 14–15)', fontsize=8.3, color='#555', va='center')
fig.savefig(OUT + 'p01_dataflow.png', dpi=200, bbox_inches='tight'); plt.close(fig)

# ---------------- step x data matrix ----------------
cols = ['ALL\n2330', 'TRAIN\n1631', 'inner\nfolds', 'DL fit /\nvalidation', 'TEST\n699', 'unsprayed\n1379 / 573', 'other\nsplits']
rows = [('1–4  Experiment, spectra, grades, weather, checks', {0: 'D'}),
        ('5  Grouped, stratified 70:30 split', {0: 'D'}),
        ('6  Pre-processing and index features', {0: 'D'}),
        ('7  Objective 1 description', {0: 'D'}),
        ('8  Feature selection (models)', {1: 'L'}),
        ('9  ML: scaler, SFFS, grid, refit', {1: 'L', 2: 'L'}),
        ('10  DL: fit, early stopping', {1: 'L', 3: 'L'}),
        ('11  Test evaluation + plot bootstrap', {4: 'E'}),
        ('12  Feature configurations, ablation', {3: 'L', 4: 'E'}),
        ('13a  Strata of the test predictions', {4: 'E'}),
        ('13b  SHAP (descriptive)', {0: 'D'}),
        ('13c  Transfer: leave-one-variety/timing-out', {0: 'L'}),
        ('14  Covariate baseline M0, M1, M2', {5: 'L'}),
        ('15a  LORO vs 70:30 side by side', {4: 'E', 6: 'E'}),
        ('15b  Same 699 test leaves (paired)', {4: 'E', 6: 'E'}),
        ('15c  20 other splits / 15d leaf-level splits', {6: 'L'}),
        ('16  Deliverable models (= tested models)', {1: 'L'})]
STY = {'D': ('#A9D18E', 'describe'), 'L': ('#2E75B6', 'learn / fit'), 'E': ('#C55A11', 'evaluate only')}
fig, ax = plt.subplots(figsize=(11, 7.2)); nr, nc = len(rows), len(cols)
for j, c in enumerate(cols): ax.text(j + 0.5, nr + 0.15, c, ha='center', va='bottom', fontsize=8.6, fontweight='bold')
for i, (lab, d) in enumerate(rows):
    y = nr - 1 - i; ax.text(-0.15, y + 0.5, lab, ha='right', va='center', fontsize=9.5)
    for j in range(nc):
        ax.add_patch(Rectangle((j + 0.04, y + 0.08), 0.92, 0.84, fc='#F7F7F7' if (i % 2) else 'white', ec='#DDDDDD', lw=0.6))
        if j in d:
            col, _ = STY[d[j]]; ax.scatter([j + 0.5], [y + 0.5], s=330, color=col, zorder=3)
            ax.text(j + 0.5, y + 0.5, d[j], ha='center', va='center', fontsize=8.5, color='white', fontweight='bold', zorder=4)
ax.set_xlim(-6.2, nc); ax.set_ylim(-1.1, nr + 1.3); ax.axis('off')
ax.legend([plt.Line2D([], [], marker='o', ls='', ms=11, color=STY[k][0]) for k in 'DLE'], ['D = ' + STY['D'][1] + ' (no model is fitted for prediction)', 'L = ' + STY['L'][1] + ' (parameters, features or settings are chosen from these leaves)', 'E = ' + STY['E'][1] + ' (predictions are scored; nothing is changed)'],
          loc='lower center', bbox_to_anchor=(0.42, -0.06), ncol=1, fontsize=9, frameon=False)
fig.savefig(OUT + 'p04_step_data_matrix.png', dpi=200, bbox_inches='tight'); plt.close(fig)
print('figures done', os.listdir(OUT))
