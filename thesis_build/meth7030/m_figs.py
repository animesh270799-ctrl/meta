"""Schematic figures of the methodology document (no results): workflow, data flow after quality control, split map, feature-selection chain.
Leaf counts are taken from the 70:30 pipeline data after removing the nine L4 spectra and the 75 duplicated spectra of 13 March 2026."""
import os, sys, json, numpy as np, pandas as pd
import matplotlib; matplotlib.use('Agg'); import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, Rectangle, Patch
T = '/home/user/meta/thesis_build/'; A = T + 'asd7030/'; D = A + 'data/'; OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'fig/')
os.makedirs(OUT, exist_ok=True)
plt.rcParams.update({'font.family': 'Liberation Sans', 'font.size': 11})
X = np.load(D + 'X_leaf.npy'); M = pd.read_csv(D + 'meta.csv')
_, inv = np.unique(X.round(6), axis=0, return_inverse=True); keep = ~pd.Series(inv.ravel()).duplicated().values
Q = M[keep].reset_index(drop=True); SPJ = json.load(open(D + 'split.json')); TE = set(SPJ['test_plots'])
tr = Q.fold == 1; ptr = np.unique(Q['plot'][tr]); rng = np.random.default_rng(42); VAL = set(int(v) for v in rng.choice(ptr, len(ptr) // 3, replace=False))
C = dict(all=len(Q), removed=int((~keep).sum()), train=int(tr.sum()), test=int((~tr).sum()), dlval=int((tr & Q['plot'].isin(VAL)).sum()), dlfit=int((tr & ~Q['plot'].isin(VAL)).sum()),
         utr=int((tr & (Q.block != 'C')).sum()), ute=int((~tr & (Q.block != 'C')).sum()), val_plots=sorted(VAL), grades=Q.grade.value_counts().sort_index().to_dict(),
         dates=Q.groupby('date').size().to_dict(), test_share=float((~tr).mean()), dup_plots=sorted(int(p) for p in M[~keep]['plot'].unique()))
json.dump(C, open(OUT + 'counts.json', 'w'), indent=1, default=int); print(C)


def box(ax, x, y, w, h, txt, fc, ec='#333', fs=8.8, tc='#111'):
    ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle='round,pad=0.3,rounding_size=1.0', fc=fc, ec=ec, lw=1.1))
    lines = txt.split('\n'); n = len(lines); lh = 2.25
    for k, ln in enumerate(lines):
        ax.text(x + w / 2, y + h / 2 + (n - 1) * lh / 2 - k * lh, ln, ha='center', va='center', fontsize=fs + (0.5 if k == 0 else 0), fontweight='bold' if k == 0 else 'normal', color=tc)


def arr(ax, pts, c='#333', ls='-'):
    for (x1, y1), (x2, y2) in zip(pts[:-2], pts[1:-1]): ax.plot([x1, x2], [y1, y2], color=c, lw=1.3, ls=ls)
    (x1, y1), (x2, y2) = pts[-2], pts[-1]
    ax.annotate('', xy=(x2, y2), xytext=(x1, y1), arrowprops=dict(arrowstyle='-|>', color=c, lw=1.3, ls=ls, shrinkA=0, shrinkB=0))


# ---------------- 1. workflow ----------------
fig, ax = plt.subplots(figsize=(11, 9.4)); ax.set_xlim(0, 100); ax.set_ylim(0, 100); ax.axis('off')
G, Bc, Y, Pc, R, Gy = '#E2EFDA', '#DDEBF7', '#FFF2CC', '#EDE2F6', '#FCE4D6', '#F2F2F2'
box(ax, 1, 86, 31, 12, 'A  Experiment and data\nA1 48 plots, healthy block + R1–R3\nA2 ASD leaf spectra, 4 dates\nA3 0–9 grade of the same leaf\nA4 weather and crop covariates', G)
box(ax, 35, 86, 30, 12, 'A5  Quality control\nL4 spectra removed\nduplicated spectra removed\nsplice step at 1000 nm corrected\ngrade, range, missing-value checks', G)
box(ax, 68, 86, 31, 12, 'B  Grouped, stratified 70:30 split\nwhole plots; healthy and unsprayed\nsplit separately; fixed once (seed 2026)\ninner folds by plot inside TRAIN', Y)
box(ax, 1, 63, 31, 18, 'C  Pre-processing and features\nC1 detector joins; C2 Savitzky–Golay\nC3 400–2400 nm; C4 water bands kept\nC5 first derivative\nC6 5-nm reduced sampling (bands)\nC7–C8 41 indices, REP, Dr, REarea\nC9 continuum removal\nC10 continuous wavelet features', Bc)
box(ax, 35, 63, 30, 18, 'D  Objective 1 (description)\nD1–D3 mean, correlation and\nstage-wise spectra\nD4 NDSI/RSI R² maps → effective ranges\nD5 SHAP-CARS → optimal wavelengths\nD6–D9 indices: WRI, |r| filter, ReliefF\nwavelets: separability, regions\nD10 VIF < 10 → DSF; D11 JM; D12 PCA', Bc)
box(ax, 68, 63, 31, 18, 'E  Objective 2 (models, TRAIN only)\nE2 selection repeated on TRAIN\nE3 scaling and class weights\nE4 SFFS in inner folds\nE5 SVM, RF, XGBoost, k-NN, PLS\nE6 DNN-F1, DT-EDNet, EfficientNet-B0,\nResNet18, ConvNeXt V2 (early stopping)\nE7 feature configurations, ablation', Pc)
box(ax, 68, 38, 31, 18, 'F  Evaluation (TEST once)\nF1 OA, kappa, macro-F1, sensitivity,\nspecificity, AUC\nF2 QWK, within one class, per-grade F1\nF3 R², RMSE, RPD, bias\nF4 plot bootstrap (95% intervals)\nF5 SHAP; F6 strata, LOVO, LOTO\nF7 selection stability', R)
box(ax, 35, 38, 30, 18, 'G  Covariate baseline\nunsprayed leaves, same split\nM0 covariates only (no sensor)\nM1 spectra; M2 spectra + covariates\ngains ΔS, ΔC, ΔT\nplot bootstrap; DeLong test', R)
box(ax, 1, 38, 31, 18, 'H  Check of the validation design\nH1 20 other grouped 70:30 splits\nH2 random leaf-level 70:30 splits\n(leakage check)\nH3 paired comparison with\nleave-one-replication-out', R)
box(ax, 1, 16, 98, 15, 'I  Reproducibility and deliverables\nfixed seeds (split 2026, models 42); scripts in run order; the tested models are the delivered models (trained on TRAIN only)\nfeature definitions and prediction script for new spectra; every setting written in the settings table (Appendix B)', Gy)
box(ax, 1, 2, 98, 10, 'Rules that hold in every step\n(1) whole plots are never split   (2) nothing is chosen from the test plots   (3) the test plots are opened once\n(4) every choice is reported with its reference paper and setting', '#FFFFFF', ec='#C00000')
arr(ax, [(32, 92), (35, 92)]); arr(ax, [(65, 92), (68, 92)]); arr(ax, [(83.5, 86), (83.5, 83)]); arr(ax, [(83.5, 83), (16.5, 83), (16.5, 81.3)])
arr(ax, [(32, 72), (35, 72)]); arr(ax, [(65, 72), (68, 72)]); arr(ax, [(83.5, 63), (83.5, 56.3)]); arr(ax, [(68, 47), (65.3, 47)]); arr(ax, [(35, 47), (32.3, 47)]); arr(ax, [(50, 38), (50, 31.3)])
fig.savefig(OUT + 'm01_workflow.png', dpi=200, bbox_inches='tight'); plt.close(fig)

# ---------------- 2. data flow ----------------
fig, ax = plt.subplots(figsize=(11, 7.4)); ax.set_xlim(0, 100); ax.set_ylim(0, 100); ax.axis('off')
box(ax, 15, 87, 70, 11, 'Recorded: 2339 leaf spectra, 48 plots, 4 dates\n− 9 spectra labelled L4 (not a sampled position)\n− %d duplicated spectra (identical copies, 13 March 2026, plots %s)' % (C['removed'], ', '.join(map(str, C['dup_plots']))), G)
box(ax, 30, 71, 40, 8, 'ALL after quality control: %d leaf spectra\n(48 plots; used leaf by leaf in Steps C and D)' % C['all'], G)
box(ax, 2, 50, 44, 13, 'TRAIN – 33 plots, %d leaves\nhealthy 8; unsprayed R1 8, R2 8, R3 9\nevery learning step (selection, SFFS, tuning, fitting)\nuses these leaves only' % C['train'], Bc)
box(ax, 54, 50, 44, 13, 'TEST – 15 plots, %d leaves (%.1f%%)\nhealthy 1, 4, 5, 8; unsprayed 13, 14, 18, 25, 27,\n31, 35, 37, 44, 46, 48\nlocked; opened once for the final evaluation' % (C['test'], 100 * C['test_share']), '#404040', tc='white')
box(ax, 2, 27, 21, 15, 'Machine learning\ninner GroupKFold(3)\nby plot: 22 plots fit,\n11 plots score\n(three rounds)', Bc, fs=8.4)
box(ax, 25, 27, 21, 15, 'Deep learning\nfit: 22 plots, %d leaves\nvalidation (early\nstopping): 11 plots,\n%d leaves' % (C['dlfit'], C['dlval']), Bc, fs=8.4)
box(ax, 54, 27, 44, 15, 'Evaluation of every model (ML and DL)\non the %d test leaves; uncertainty from\nresampling whole test plots (bootstrap)' % C['test'], R)
box(ax, 2, 4, 44, 15, 'Covariate baseline (unsprayed leaves only)\nTRAIN: %d leaves of 25 plots\nTEST: %d leaves of 11 plots' % (C['utr'], C['ute']), Pc)
box(ax, 54, 4, 44, 15, 'Check of the design (separate runs)\n20 other grouped 70:30 splits; 5 random\nleaf-level splits; paired comparison with LORO', Pc)
arr(ax, [(50, 87), (50, 79.3)]); arr(ax, [(42, 71), (24, 63.3)]); arr(ax, [(58, 71), (76, 63.3)]); arr(ax, [(13, 50), (12.5, 42.3)]); arr(ax, [(35, 50), (35.5, 42.3)])
arr(ax, [(46.3, 34.5), (54, 34.5)], c='#C00000'); arr(ax, [(76, 50), (76, 42.3)], c='#C00000', ls='--')
fig.savefig(OUT + 'm02_dataflow.png', dpi=200, bbox_inches='tight'); plt.close(fig)

# ---------------- 3. split map ----------------
LAY = {}
exec(open(A + 'a1_prep.py').read().split('blk = lambda')[0].split('# ---- treatments')[1].split('\n', 1)[1])
BLOCKS = [('Healthy (sprayed) 1–12', range(1, 13)), ('R3 13–24', range(13, 25)), ('R2 25–36', range(25, 37)), ('R1 37–48', range(37, 49))]
fig, ax = plt.subplots(figsize=(11, 4.0))
for bi, (bn, rgp) in enumerate(BLOCKS):
    for j, p in enumerate(rgp):
        c = '#404040' if p in TE else ('#7030A0' if p in VAL else '#DDEBF7'); dark = c != '#DDEBF7'
        ax.add_patch(Rectangle((j, -bi), 0.92, 0.82, facecolor=c, edgecolor='#555', lw=0.6))
        ax.text(j + 0.46, -bi + 0.53, str(p), ha='center', va='center', fontsize=8.5, color='white' if dark else '#222', fontweight='bold')
        ax.text(j + 0.46, -bi + 0.2, LAY[p], ha='center', va='center', fontsize=6.5, color='white' if dark else '#444')
    ax.text(-0.25, -bi + 0.41, bn, ha='right', va='center', fontsize=9.5)
ax.set_xlim(-0.1, 12); ax.set_ylim(-3.3, 1.0); ax.axis('off')
ax.legend([Patch(color='#404040'), Patch(facecolor='#DDEBF7', edgecolor='#555'), Patch(color='#7030A0')],
          ['test plot (15)', 'training plot (33)', 'training plot used for early stopping of the networks (11)'], loc='lower center', bbox_to_anchor=(0.5, -0.2), ncol=3, fontsize=9, frameon=False)
fig.savefig(OUT + 'm03_split_map.png', dpi=200, bbox_inches='tight'); plt.close(fig)

# ---------------- 4. feature chain ----------------
fig, ax = plt.subplots(figsize=(11, 7.6)); ax.set_xlim(0, 100); ax.set_ylim(0, 100); ax.axis('off')
box(ax, 1, 78, 31, 18, 'Family 1 – spectral bands\nreflectance and first derivative\n(5-nm grid, 400–2400 nm)\n→ NDSI / RSI R² maps\n→ effective ranges\n(R² ≥ 0.5, else top 5% of pairs)', Bc)
box(ax, 35, 78, 30, 18, 'Family 2 – indices\n41 published indices, REP, Dr,\nREarea, continuum-removal\nfeatures, best NDSI, best RSI,\nWhite Rust Index\n→ |r| ≥ 0.95 redundancy filter', Bc)
box(ax, 68, 78, 31, 18, 'Family 3 – wavelet features\ncontinuous wavelet transform\n(Mexican hat, scales 2^1–2^6)\n→ separability of each coefficient\n→ top 5%, merged into regions\n(one representative per region)', Bc)
box(ax, 1, 55, 31, 14, 'SHAP-CARS\nXGBoost SHAP top 40%\n→ MCCV (PLS components)\n→ CARS 50 iterations × 20 runs\n→ bands in ≥ 50% of runs = OW', Bc)
box(ax, 35, 55, 30, 14, 'ReliefF / RReliefF\nk = 10 nearest neighbours,\nneighbours of the same plot excluded\n→ top 5 indices per task = VI', Bc)
box(ax, 68, 55, 31, 14, 'ReliefF / RReliefF on the\nregion representatives\n→ top 5 wavelet features\nper task = WF', Bc)
box(ax, 20, 33, 60, 13, 'Variance inflation factor\npool OW + VI + WF of each task; remove the feature with the largest VIF\nuntil all VIF < 10 → disease-specific feature set (DSF) of the task', '#FFF2CC')
box(ax, 1, 6, 46, 18, 'Machine learning\nstandardise with TRAIN statistics\n→ SFFS (≤ 15 features, inner GroupKFold(3))\n→ grid search → refit on all training plots', Pc)
box(ax, 53, 6, 46, 18, 'Deep learning\nDNN-F1: feature vector\nDT-EDNet, EfficientNet-B0, ResNet18, ConvNeXt V2:\nk × k pseudo-image of the DSF (configurations\nOW, VI, WF, DSF compared)', Pc)
for x in (16.5, 50, 83.5): arr(ax, [(x, 78), (x, 69.3)])
arr(ax, [(16.5, 55), (30, 46.3)]); arr(ax, [(50, 55), (50, 46.3)]); arr(ax, [(83.5, 55), (70, 46.3)]); arr(ax, [(40, 33), (24, 24.3)]); arr(ax, [(60, 33), (76, 24.3)])
ax.text(50, 99, 'Every step below is run on the training plots only when it feeds the models (Step E2); run on all leaves it is the Objective 1 description (Step D).', ha='center', fontsize=9, color='#C00000')
fig.savefig(OUT + 'm04_feature_chain.png', dpi=200, bbox_inches='tight'); plt.close(fig)
print('figures', sorted(os.listdir(OUT)))
