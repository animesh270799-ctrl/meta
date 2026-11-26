"""New figures for the step-by-step explanation of the 2026-27 data analysis (diagrams and demo data only)."""
import os
import numpy as np
import matplotlib; matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, Rectangle
plt.rcParams.update({'font.family': 'Liberation Sans', 'font.size': 10})
D = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'fig')
TEST = [1, 4, 5, 8, 13, 14, 18, 25, 27, 31, 35, 37, 44, 46, 48]
VAL = [6, 7, 11, 19, 24, 26, 28, 30, 36, 39, 41]
C_FIT, C_VA, C_TE = '#CFE3C8', '#BBD5EE', '#F6C59C'
rng = np.random.default_rng(11)


def save(fig, n):
    fig.savefig(os.path.join(D, n), dpi=200, bbox_inches='tight'); plt.close(fig)


def box(ax, x, y, w, h, t, c, fs=8.5, bold=False):
    ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle='round,pad=0.2,rounding_size=0.6', fc=c, ec='#333', lw=0.8))
    ax.text(x + w / 2, y + h / 2, t, ha='center', va='center', fontsize=fs, fontweight='bold' if bold else 'normal')


def arrow(ax, a, b):
    ax.annotate('', xy=b, xytext=a, arrowprops=dict(arrowstyle='-|>', color='#333', lw=0.9))


# x01 order of the whole analysis ------------------------------------------------------------------
fig, ax = plt.subplots(figsize=(10.5, 13)); ax.set_xlim(0, 100); ax.set_ylim(0, 130); ax.axis('off')
main = [('Stage 1  Image processing (B1–B6)', 'calibration → mosaics → HS cleaning, smoothing → co-registration → one grid → ROI means', '#E2EFDA'),
        ('Stage 2  Feature extraction (C1–C6)', 'HS bands, derivatives, indices, texture; MS, RGB, thermal features → 4 camera tables', '#E2EFDA'),
        ('Stage 3  Labels and covariates (A5–A6)', 'DI, DI class, healthy/diseased; DAI, variety, sowing date, stage, weather joined to every row', '#E2EFDA'),
        ('Stage 4  Split by whole plots (D1–D2)', '33 training plots / 15 test plots; GroupKFold(3) and 11 validation plots inside training', '#FCE4D6'),
        ('Stage 5  Normalisation and leakage rules (D3–D5)', 'thermal normalised; z-score fitted on the fitting part only; nothing learned from test plots', '#FCE4D6'),
        ('Stage 6  Objective 1 – description (all 48 plots)', 'curves by DI class, correlation with DI, response by stratum; physiology', '#DDEBF7'),
        ('Stage 7  Objective 1 – feature selection per camera (training plots)', 'each camera: bands → SHAP-CARS, indices → ReliefF, texture → mRMR → TTFI; VIF → DSF', '#DDEBF7'),
        ('Stage 8  Objective 2 – 15 sensor sets (feature-level fusion)', 'join the DSFs of the cameras in each set; VIF < 10 again (training plots)', '#EDE2F6'),
        ('Stage 9  Objective 2 – machine learning', 'SFFS (≤ 15 features) → grid search (GroupKFold(3)) → refit on 33 training plots', '#EDE2F6'),
        ('Stage 10  Objective 2 – networks', 'DNN-F1, DNN-F2, DT-EDNet and 3 comparison networks: fit 22 plots, stop on 11 plots', '#EDE2F6'),
        ('Stage 11  Objective 2 – test once (15 test plots)', 'OA, kappa, macro-F1, within-one-class accuracy, AUC; R², RMSE, RPD', '#FFF2CC'),
        ('Stage 12  Objective 2 – comparison and use', 'fusion gain, drop-one-camera, SHAP, covariate baseline, strata, maps, Bharatpur', '#FFF2CC')]
y = 124; h = 7.2
for i, (t, s, c) in enumerate(main):
    box(ax, 2, y - h, 62, h, '', c)
    ax.text(4, y - 2.3, t, fontsize=9.2, fontweight='bold', va='center'); ax.text(4, y - 5.0, s, fontsize=7.9, va='center')
    if i < len(main) - 1: arrow(ax, (33, y - h), (33, y - h - 2.4))
    y -= h + 2.6
box(ax, 70, 76, 28, 22, 'Stage 13  Objective 3\npre-symptomatic\n(1.8, 3.1–3.6)\n\nsame split; labels from\nlater status; healthy-\nbaseline normalisation;\nper-camera selection →\nmodels → test once', '#FDECEA', fs=8)
box(ax, 70, 40, 28, 30, 'Stage 14  Part L\nASD leaf spectra\n(L1–L10)\n\nleaf table → same split\n→ smoothing, 5-nm bands\n→ indices → description\n(all leaves) → selection\n(training leaves) → leaf\nmodels → test leaves →\ncovariate baseline →\nleaf–canopy link', '#FDECEA', fs=8)
arrow(ax, (64, 61), (70, 80)); arrow(ax, (64, 81), (70, 60))
ax.text(84, 100, 'runs after Stage 7', ha='center', fontsize=8, style='italic'); ax.text(84, 72, 'runs after Stage 5', ha='center', fontsize=8, style='italic')
ax.text(50, 1.5, 'Stages 1–5 are done once for all objectives; every later stage uses their outputs. Step codes (B1, 1.6.5, …) refer to the methodology document.', ha='center', fontsize=8.5, style='italic')
save(fig, 'x01_stage_order.png')

# x02 plot split on the field layout --------------------------------------------------------------
fig, ax = plt.subplots(figsize=(11, 4.6)); ax.set_xlim(0, 13.5); ax.set_ylim(-0.6, 4.6); ax.axis('off')
blocks = [('R1 inoculated', 37), ('R2 inoculated', 25), ('R3 inoculated', 13), ('Healthy block', 1)]
for r, (name, start) in enumerate(blocks):
    yy = 3 - r
    ax.text(0.05, yy + 0.4, name, fontsize=9, va='center', fontweight='bold')
    for k in range(12):
        pnum = start + k
        c = C_TE if pnum in TEST else (C_VA if pnum in VAL else C_FIT)
        ax.add_patch(Rectangle((1.4 + k, yy), 0.92, 0.8, fc=c, ec='#333', lw=0.7))
        ax.text(1.86 + k, yy + 0.4, str(pnum), ha='center', va='center', fontsize=9)
for i, (c, t) in enumerate([(C_FIT, 'training plot – fits model weights (22)'), (C_VA, 'training plot – network validation (11)'), (C_TE, 'test plot – used once at the end (15)')]):
    ax.add_patch(Rectangle((1.4 + i * 4, -0.5), 0.4, 0.3, fc=c, ec='#333', lw=0.7)); ax.text(1.9 + i * 4, -0.35, t, fontsize=8.5, va='center')
ax.set_title('The 48 plots: 33 training plots (green + blue) and 15 test plots (orange); the same division for every camera, sensor set, model and the ASD leaves', fontsize=9.5)
save(fig, 'x02_plot_split.png')

# x03 sample flow --------------------------------------------------------------------------------
fig, ax = plt.subplots(figsize=(11, 5.6)); ax.set_xlim(0, 100); ax.set_ylim(0, 100); ax.axis('off')
rows = [('UAV post-symptomatic\n48 plots × 4 subplots × 10 dates\n= 1920 per camera', '1320 training\n(33 plots)', '880 fit (22 plots)\n440 validation (11 plots)', '600 test\n(15 plots)'),
        ('UAV pre-symptomatic\n48 × 4 × 3 dates\n= 576 per camera', '396 training', '264 fit\n132 validation', '180 test'),
        ('ASD leaves\n576 per date × 13 dates\n= 7488 leaves', '5148 training', '3432 fit\n1716 validation', '2340 test')]
for i, (a, b, c, d) in enumerate(rows):
    yy = 78 - i * 30
    box(ax, 1, yy, 26, 18, a, '#F2F2F2', fs=8.5)
    box(ax, 36, yy + 6, 18, 12, b, C_FIT, fs=8.5); box(ax, 36, yy - 7, 18, 9, d, C_TE, fs=8.5)
    box(ax, 63, yy + 5, 22, 14, c, C_VA, fs=8.3)
    arrow(ax, (27, yy + 12), (36, yy + 12)); arrow(ax, (27, yy + 6), (36, yy - 2.5)); arrow(ax, (54, yy + 12), (63, yy + 12))
    ax.text(87, yy + 12, 'networks only;\nML uses GroupKFold(3)\n(3 × 22 / 11 plots)', fontsize=7.5, va='center')
ax.set_title('How the samples of each data set are divided (plot-wise, so every sample of a plot stays on one side)', fontsize=9.5)
save(fig, 'x03_sample_flow.png')

# x04 which data is used in which stage -------------------------------------------------------------
stages = ['1–3 Processing, features, labels', '4 Split (defines the sets)', '5 Thermal normalisation (healthy ΔT)', '5 z-score constants',
          '6 Description: curves, r, strata', '6 Physiology (1.7)', '7 Feature selection per camera', '7 Stability by stage (1.6.6)',
          '8 Fusion + VIF (2.2)', '9 SFFS + grid search', '9 Refit final ML model', '10 Network weights', '10 Early stopping, model choice',
          '11 Test metrics', '12 Covariate models M0–M2', '12 Maps', '13 Pre-symptomatic selection', '13 Healthy baseline (3.2)', '14 Leaf selection (L5.2–L5.5)', 'Bharatpur test']
cols = ['all 48 plots', '33 training\nplots', 'inner fit\n(22 plots)', 'inner score /\nvalidation\n(11 plots)', '15 test\nplots']
M = np.array([[1, 0, 0, 0, 0], [1, 0, 0, 0, 0], [0, 1, 0, 0, 0], [0, 0, 1, 0, 0], [1, 0, 0, 0, 0], [1, 0, 0, 0, 0], [0, 1, 0, 0, 0], [1, 0, 0, 0, 0],
              [0, 1, 0, 0, 0], [0, 0, 1, 1, 0], [0, 1, 0, 0, 0], [0, 0, 1, 0, 0], [0, 0, 0, 1, 0], [0, 0, 0, 0, 1], [0, 1, 1, 1, 1], [1, 0, 0, 0, 1],
              [0, 1, 0, 0, 0], [0, 1, 0, 0, 0], [0, 1, 0, 0, 0], [0, 0, 0, 0, 0]])
fig, ax = plt.subplots(figsize=(11, 8.6))
ax.imshow(np.zeros_like(M), cmap='Greys', vmin=0, vmax=1, aspect='auto')
for i in range(M.shape[0]):
    for j in range(M.shape[1]):
        if M[i, j]: ax.add_patch(Rectangle((j - 0.45, i - 0.4), 0.9, 0.8, fc=[ '#BFBFBF', C_FIT, '#9FD39A', C_VA, C_TE][j], ec='#333', lw=0.6))
ax.text(4, 19, 'external\nquadrats', ha='center', va='center', fontsize=7.5)
ax.set_xticks(range(5)); ax.set_xticklabels(cols, fontsize=8.5); ax.xaxis.tick_top()
ax.set_yticks(range(len(stages))); ax.set_yticklabels(stages, fontsize=8.5)
ax.set_xlim(-0.6, 4.6); ax.set_ylim(len(stages) - 0.5, -0.5)
for s in ax.spines.values(): s.set_visible(False)
ax.set_title('Which samples each stage uses (filled cell = used). Test plots are only predicted, never learned from.', fontsize=9.5, pad=46)
save(fig, 'x04_data_use.png')

# x05 GroupKFold rounds and the network split ------------------------------------------------------
tr = [p for p in range(1, 49) if p not in TEST]
folds = [tr[0::3], tr[1::3], tr[2::3]]
fig, ax = plt.subplots(figsize=(11, 4.4)); ax.set_xlim(0, 34.5); ax.set_ylim(-0.4, 4.8); ax.axis('off')
for r in range(3):
    yy = 3.6 - r * 1.15
    ax.text(0, yy + 0.35, 'ML round %d' % (r + 1), fontsize=9, va='center', fontweight='bold')
    for k, pnum in enumerate(tr):
        c = C_VA if pnum in folds[r] else C_FIT
        ax.add_patch(Rectangle((3 + k * 0.95, yy), 0.88, 0.7, fc=c, ec='#333', lw=0.5)); ax.text(3.44 + k * 0.95, yy + 0.35, str(pnum), ha='center', va='center', fontsize=6.6)
yy = 0.0
ax.text(0, yy + 0.35, 'Networks', fontsize=9, va='center', fontweight='bold')
for k, pnum in enumerate(tr):
    c = C_VA if pnum in VAL else C_FIT
    ax.add_patch(Rectangle((3 + k * 0.95, yy), 0.88, 0.7, fc=c, ec='#333', lw=0.5)); ax.text(3.44 + k * 0.95, yy + 0.35, str(pnum), ha='center', va='center', fontsize=6.6)
ax.text(17, 4.55, 'Only the 33 training plots: green = fitting plots, blue = scoring (ML) or validation (networks) plots. The ML fold assignment shown is illustrative (made by GroupKFold); the network validation plots are fixed.', ha='center', fontsize=8.3)
save(fig, 'x05_groupkfold.png')

# x06 SFFS demo -----------------------------------------------------------------------------------
fig, ax = plt.subplots(1, 2, figsize=(11.5, 3.9))
steps = ['+ NDRE', '+ WRI', '+ CTD', '+ PC2-Con', '− CTD', '+ NRCT', '+ FD716', '+ PSRI', '+ ExG−ExR', '+ R560']
score = [0.52, 0.61, 0.66, 0.69, 0.70, 0.72, 0.735, 0.738, 0.736, 0.733]
ax[0].plot(range(1, 11), score, 'o-', color='#2E75B6'); best = int(np.argmax(score))
for i, t in enumerate(steps): ax[0].annotate(t, (i + 1, score[i]), textcoords='offset points', xytext=(0, 7 if i % 2 == 0 else -13), ha='center', fontsize=7.4, color='#C0392B' if t.startswith('−') else 'k')
ax[0].plot(best + 1, score[best], 'o', ms=12, mfc='none', mec='#C0392B'); ax[0].set_xlabel('SFFS step'); ax[0].set_ylabel('GroupKFold(3) macro-F1 (demo)')
ax[0].set_title('a  SFFS adds the best feature, then tries to remove one (red); best subset circled', fontsize=9)
feats = ['WRI', 'NDRE', 'NRCT', 'PC2-Con', 'FD716', 'PSRI', 'CTD', 'R560', 'ExG−ExR', 'MTD']; freq = [97, 93, 81, 74, 66, 52, 31, 22, 15, 6]
ax[1].barh(feats[::-1], freq[::-1], color=['#2E75B6' if f >= 50 else '#BBBBBB' for f in freq[::-1]]); ax[1].axvline(50, color='k', ls='--', lw=0.8)
ax[1].set_xlabel('% of 100 repeated SFFS runs that selected the feature (demo)'); ax[1].set_title('b  Stability check of the best model (Step 2.3)', fontsize=9)
save(fig, 'x06_sffs.png')

# x07 one sample row and its journey ---------------------------------------------------------------
fig, ax = plt.subplots(figsize=(11, 3.4)); ax.set_xlim(0, 100); ax.set_ylim(0, 40); ax.axis('off')
items = [('Subplot 25-2\n18 Jan 2027', '#F2F2F2'), ('ROI mean of every\nband of 4 cameras', '#E2EFDA'), ('~1160 features\n+ DI 28.4, class 7,\ndiseased, covariates', '#E2EFDA'),
         ('plot 25 = TEST\n→ never used to\nlearn anything', C_TE), ('features of the DSF\ncomputed with the\ntraining wavelengths', '#DDEBF7'), ('frozen models\npredict it once\n→ metrics', '#FFF2CC')]
for i, (t, c) in enumerate(items):
    box(ax, 1 + i * 16.5, 10, 14.5, 20, t, c, fs=8.2)
    if i < len(items) - 1: arrow(ax, (15.5 + i * 16.5, 20), (17.5 + i * 16.5, 20))
ax.text(50, 3, 'A training-plot sample (for example subplot 26-1) goes the same way but is used for selection, tuning and fitting instead.', ha='center', fontsize=8.5, style='italic')
save(fig, 'x07_sample_journey.png')
print('explain figures written')
