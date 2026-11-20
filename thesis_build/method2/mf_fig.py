"""Flow charts and diagrams for the reconstructed field methodology (Objectives 1-3)."""
import os
import matplotlib; matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch
F = os.path.dirname(os.path.abspath(__file__)) + '/fig/'
plt.rcParams['font.family'] = 'DejaVu Sans'
C = dict(hs='#00838F', ms='#1565C0', rgb='#2E7D32', tir='#C62828', nav='#1F3864', o1='#2E75B6', o2='#7030A0', o3='#C00000', gold='#B8860B', grey='#616161')
L = dict(hs='#E0F2F1', ms='#E3F2FD', rgb='#E8F5E9', tir='#FFEBEE', nav='#EEF1F6', o1='#DEEBF7', o2='#EDE2F6', o3='#F9E0DE', gold='#FFF4D6', grey='#F2F2F2')

def box(ax, x, y, w, h, title, body='', k='nav', fs=8.5, tfs=9.5, filled=False):
    ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle='round,pad=0.01,rounding_size=0.06', fc=C[k] if filled else L[k], ec=C[k], lw=1.3))
    col = 'white' if filled else '#1a1a1a'
    if body:
        ax.text(x + w / 2, y + h - 0.12, title, ha='center', va='top', fontsize=tfs, fontweight='bold', color=col if filled else C[k])
        ax.text(x + w / 2, y + h - 0.42, body, ha='center', va='top', fontsize=fs, color=col, linespacing=1.3, wrap=True)
    else:
        ax.text(x + w / 2, y + h / 2, title, ha='center', va='center', fontsize=tfs, fontweight='bold', color=col)

def arr(ax, x1, y1, x2, y2, c='#555'):
    ax.annotate('', xy=(x2, y2), xytext=(x1, y1), arrowprops=dict(arrowstyle='-|>', color=c, lw=1.3))

def canvas(w, h):
    fig, ax = plt.subplots(figsize=(w, h)); ax.set_xlim(0, w); ax.set_ylim(0, h); ax.axis('off'); return fig, ax

def save(fig, name):
    fig.savefig(F + name, dpi=200, bbox_inches='tight'); plt.close(fig)

# ---------------- F1 overall workflow ----------------
fig, ax = canvas(11, 12.5)
rows = [('A. Field experiment and data (Chapter 2)', 'IARI rabi 2025-26 | 4 inoculation timings × 3 varieties × 3 replications + 12 healthy plots = 48 plots | 4 subplots per plot\nUAV hyperspectral, multispectral, RGB and thermal images | canopy severity score of every subplot', 'nav'),
        ('B. Pre-processing (Chapter 3, steps P1–P8)', 'calibration → mosaics → hyperspectral cube checks → UTM 43N + co-registration → resampling to the hyperspectral grid\n→ vegetation mask (soil, grass, shadow removed; leaves + flowers kept) → plot and subplot polygons → subplot values', 'nav'),
        ('C. Feature extraction (Chapter 4)', 'hyperspectral: bands, derivatives, red-edge parameters, 48 indices | multispectral: bands, indices, texture\nRGB: colour indices, texture, canopy cover | thermal: temperature statistics, normalised temperatures, texture', 'nav'),
        ('D. Validation framework (Chapter 5)', 'unit = subplot-date | outer leave-one-replication-out folds grouped by plot | inner grouped folds for selection and tuning\nevery step that uses the severity labels is repeated inside the training folds', 'gold'),
        ('E. Objective 1 – characterisation (Chapter 6)', 'per sensor: response curves → redundancy removal → scalogram + ReliefF (bands) → White Rust Index → ANOVA / correlation → Boruta\noutput: disease-specific feature (DSF) pools of each sensor, White Rust Index, response by variety and inoculation timing', 'o1'),
        ('F. Objective 2 – detection and severity (Chapter 7, 1536 post-symptomatic samples per sensor)', '15 sensor sets (4 single + 11 combinations) | feature-level fusion | ML: SVM, RF, XGBoost, k-NN, PLS-DA / PLSR | DL: DNN-F1, DNN-F2\nbinary detection, severity classes, severity regression → best sensor set and model; contribution of each sensor; maps', 'o2'),
        ('G. Objective 3 – pre-symptomatic prediction (Chapter 8, 576 pre-symptomatic samples per sensor)', 'control-normalised features | healthy vs infected-not-yet-symptomatic | later severity regression | same 15 sensor sets, ML + DL\nsensitivity, specificity, AUC by day after inoculation → earliest detection day and risk maps', 'o3')]
y = 12.2
for i, (t, b, k) in enumerate(rows):
    box(ax, 0.3, y - 1.45, 10.4, 1.35, t, b, k, fs=8.2, tfs=10)
    if i < len(rows) - 1: arr(ax, 5.5, y - 1.45, 5.5, y - 1.62)
    y -= 1.72
save(fig, 'f1_overall.png')

# ---------------- F2 dataset ----------------
fig, ax = canvas(11, 4.6)
lv = [('flight dates\n(pre- and post-\nsymptomatic)', 'nav'), ('4 sensors\nper date', 'ms'), ('48 plots\nper image', 'rgb'), ('4 scored\nsubplots\nper plot', 'tir')]
for i, (t, k) in enumerate(lv):
    box(ax, 0.3 + i * 2.7, 2.7, 2.45, 1.4, t, '', k, tfs=10, filled=True)
    if i < 3: arr(ax, 2.75 + i * 2.7, 3.4, 3.0 + i * 2.7, 3.4)
box(ax, 0.3, 0.4, 5.1, 1.8, 'Post-symptomatic set (Objectives 1 and 2)', '1536 subplot samples per sensor\n(8 dates × 48 plots × 4 subplots)\nlabels: severity score, class, healthy / diseased', 'o2', fs=9)
box(ax, 5.7, 0.4, 5.0, 1.8, 'Pre-symptomatic set (Objective 3)', '576 subplot samples per sensor\n(dates before the first visible pustule)\nlabels: healthy / infected, later severity', 'o3', fs=9)
save(fig, 'f2_dataset.png')

# ---------------- generic vertical chain with outputs ----------------
def chain(name, title, steps, k, w=11):
    h = 0.9 + sum(0.62 + 0.24 * s[1].count('\n') for s in steps) + 0.22 * len(steps)
    fig, ax = canvas(w, h)
    box(ax, 0.3, h - 0.75, w - 0.6, 0.6, title, '', k, tfs=11, filled=True)
    y = h - 0.95
    for i, (t, b, o) in enumerate(steps):
        hb = 0.62 + 0.24 * b.count('\n')
        ax.add_patch(FancyBboxPatch((0.3, y - hb), 7.2, hb, boxstyle='round,pad=0.01,rounding_size=0.05', fc=L[k], ec=C[k], lw=1.2))
        ax.text(0.45, y - 0.1, t, fontsize=9.5, fontweight='bold', va='top', color=C[k])
        ax.text(0.45, y - 0.37, b, fontsize=8.2, va='top', color='#222', linespacing=1.3)
        ax.add_patch(FancyBboxPatch((7.7, y - hb), w - 8.0, hb, boxstyle='round,pad=0.01,rounding_size=0.05', fc=L['gold'], ec=C['gold'], lw=1))
        ax.text(7.82, y - 0.1, 'Output', fontsize=8.5, fontweight='bold', va='top', color='#7A5900')
        ax.text(7.82, y - 0.36, o, fontsize=8, va='top', color='#333', linespacing=1.25)
        arr(ax, 7.5, y - hb / 2, 7.7, y - hb / 2, '#999')
        y -= hb
        if i < len(steps) - 1: arr(ax, 3.9, y, 3.9, y - 0.2)
        y -= 0.22
    save(fig, name)

chain('f3_preproc.png', 'Pre-processing of every flight date (steps P1–P8)', [
    ('P1  Radiometric calibration', 'HS and MS: reflectance from calibration panels (empirical line) and sunlight sensor\nRGB: fixed exposure, digital numbers; TIR: radiometric temperature, emissivity 0.98', 'reflectance / °C images'),
    ('P2  Orthomosaics and georeferencing', 'structure-from-motion mosaics (RGB, MS, TIR); HS cubes georectified;\nsame RTK ground control points on all dates', 'georeferenced mosaics'),
    ('P3  Hyperspectral cube quality', '613 → 483 bands (water and noisy bands removed); 916–920 nm dropped;\nSavitzky–Golay smoothing on each band segment separately', 'clean 2.2 cm HS cube'),
    ('P4  Projection and co-registration', 'all images to WGS 84 / UTM 43N; image-to-image registration to HS;\nRMSE of check points < 1 HS pixel', 'aligned images'),
    ('P5  Resampling to the HS grid', 'RGB: pixel aggregate (mean); MS: bilinear; TIR: nearest neighbour\n(RGB texture computed at native resolution before resampling)', 'one grid for all sensors'),
    ('P6  Vegetation mask', 'hourglass endmembers (MNF → PPI → n-D) → SAM classes; keep canopy, stressed canopy,\nflowers; remove soil, grass, shadow; NDVI > 0.6 OR flower class; 1-pixel erosion', 'binary mask'),
    ('P7  Plot and subplot polygons', '48 plot polygons with plot number; 4 quadrant subplots per plot;\ninner buffer to avoid border rows', '192 subplots'),
    ('P8  Subplot values', 'mean of masked pixels per band and sensor; pixel count; flower % and canopy cover %;\nthermal normalised to air temperature and to healthy plots of the same date', 'subplot tables per date and sensor'),
], 'nav')

# ---------------- F4 feature groups ----------------
fig, ax = canvas(11, 5.4)
fg = [('Hyperspectral', 'Reflectance (R, 483 bands)\n1st derivative (FD)\n2nd derivative (SD)\nRed-edge: REP, Dr, SDr\n48 vegetation indices\n(pigment, structure, water,\ndisease, SWIR)\nWhite Rust Index (searched)', 'hs'),
      ('Multispectral', '5 band reflectances\n(475, 560, 668, 717, 840 nm)\n12 vegetation indices\n10 two-band NDSI\nGLCM texture: 8 × 5 bands', 'ms'),
      ('RGB', 'colour indices: ExG, ExR,\nExG−ExR, VARI, GLI, NGRDI\nHSV means\nGLCM texture: 8 × 3 bands\n(native resolution)\ncanopy cover', 'rgb'),
      ('Thermal', 'CT mean, median, SD,\n10th and 90th percentile\nCTD = CT − Tair, CTR\nNRCT, ΔT to healthy plots\nCWSI\nGLCM texture (8)', 'tir')]
for i, (t, b, k) in enumerate(fg):
    box(ax, 0.3 + i * 2.7, 0.9, 2.5, 4.2, t, b, k, fs=8.8, tfs=11)
ax.text(5.5, 0.45, 'Covariates (not disease features): flower %, canopy cover %, days after inoculation, variety, inoculation timing', ha='center', fontsize=9, style='italic', color='#444')
save(fig, 'f4_features.png')

# ---------------- F5 validation ----------------
fig, ax = canvas(11, 5.6)
reps = ['R1', 'R2', 'R3']
for f in range(3):
    y = 4.4 - f * 1.25
    ax.text(0.35, y + 0.3, 'Outer fold %d' % (f + 1), fontsize=10, fontweight='bold', va='center')
    for j, r in enumerate(reps):
        test = j == f
        box(ax, 1.9 + j * 2.0, y, 1.85, 0.6, r + ' + controls of V%d' % (j + 1), '', 'o3' if test else 'o1', tfs=8.5, filled=test)
    ax.text(8.1, y + 0.3, 'test = %s (≈ 512 samples)\ntrain = other two (≈ 1024)' % reps[f], fontsize=8.5, va='center')
box(ax, 0.3, 0.15, 10.4, 0.95, 'Inside each training set', 'inner 3-fold cross-validation grouped by plot → feature selection (Stages 2–4), hyper-parameter tuning, early stopping\nthe test replication is used once, for the final evaluation only', 'gold', fs=8.5)
save(fig, 'f5_validation.png')

# ---------------- F6 staged selection ----------------
chain('f6_selection.png', 'Staged feature selection for one sensor (inside each training fold)', [
    ('Stage 0  Feature groups', 'features built per group with physical meaning (Chapter 4)', 'groups per sensor'),
    ('Stage 1  Redundancy within each group (no labels)', 'drop near-constant features; correlation clusters |r| ≥ 0.95 → keep one per cluster\n(bands: one band per correlated spectral region)', 'thinned groups'),
    ('Stage 2  Relevance within each group (labels, training folds only)', 'bands and derivatives: correlation scalogram (regression) + ReliefF (classes)\nindices: Boruta | texture: mRMR | two-band indices / WRI: search | thermal: kept', '5–10 per group'),
    ('Stage 3  Redundancy across groups (no labels)', 'pool the group survivors; remove features with VIF ≥ 10', 'sensor DSF set (≈ 10–25)'),
    ('Fusion (sensor combinations only)', 'concatenate the DSF sets of the sensors in the combination; VIF < 10 again', 'fused pool'),
    ('Stage 4  Model-specific selection', 'ML models: sequential floating forward selection (≤ 15 features, inner CV)\nDL models: use the fused pool directly (weights learned by the network)', 'optimum feature set'),
], 'o2')

# ---------------- F7 15 combinations ----------------
import itertools
fig, ax = canvas(11, 5.0)
S = ['HS', 'MS', 'RGB', 'TIR']; colk = ['hs', 'ms', 'rgb', 'tir']
combos = [c for r in range(1, 5) for c in itertools.combinations(range(4), r)]
for j, c in enumerate(combos):
    x = 1.6 + j * 0.62
    ax.text(x + 0.25, 4.55, 'S%d' % (j + 1), ha='center', fontsize=8.5, fontweight='bold')
    for i in range(4):
        on = i in c
        ax.add_patch(FancyBboxPatch((x, 3.6 - i * 0.62), 0.5, 0.5, boxstyle='round,pad=0.01,rounding_size=0.05', fc=C[colk[i]] if on else '#F4F4F4', ec='#BBB', lw=0.8))
for i, s in enumerate(S): ax.text(1.45, 3.85 - i * 0.62, s, ha='right', va='center', fontsize=10, fontweight='bold', color=C[colk[i]])
for lab, a, b in (('single sensors', 0, 3), ('pairs', 4, 9), ('triples', 10, 13), ('all four', 14, 14)):
    xa, xb = 1.6 + a * 0.62, 1.6 + b * 0.62 + 0.5
    ax.plot([xa, xb], [1.15, 1.15], color='#555', lw=1.2); ax.text((xa + xb) / 2, 0.8, lab, ha='center', fontsize=9)
ax.text(5.5, 0.25, '15 sensor sets = 4 single + 6 pairs + 4 triples + 1 all-four (feature-level fusion)', ha='center', fontsize=9.5, style='italic')
save(fig, 'f7_combinations.png')

# ---------------- F8 DL architectures ----------------
fig, ax = canvas(11, 6.3)
ax.text(2.6, 6.05, 'DNN-F1: input-level feature fusion', ha='center', fontsize=10.5, fontweight='bold', color=C['o2'])
for i, (s, k) in enumerate(zip(S, colk)): box(ax, 0.3, 4.9 - i * 0.75, 1.3, 0.55, s + ' features', '', k, tfs=8.5)
box(ax, 2.0, 2.9, 1.3, 1.6, 'concatenate', '', 'nav', tfs=8.5)
for i in range(4): arr(ax, 1.6, 5.17 - i * 0.75, 2.0, 3.7)
box(ax, 3.5, 3.85, 1.75, 0.6, 'Dense 64\nBN, ReLU, dropout', '', 'o2', tfs=7.5, filled=True)
box(ax, 3.5, 2.95, 1.75, 0.6, 'Dense 32\nBN, ReLU, dropout', '', 'o2', tfs=7.5, filled=True)
arr(ax, 3.3, 3.7, 3.5, 4.1); arr(ax, 4.37, 3.85, 4.37, 3.55)
box(ax, 3.5, 2.05, 1.75, 0.6, 'output', '', 'gold', tfs=8.5); arr(ax, 4.37, 2.95, 4.37, 2.65)
ax.text(8.3, 6.05, 'DNN-F2: intermediate feature fusion with sensor attention', ha='center', fontsize=10.5, fontweight='bold', color=C['o2'])
for i, (s, k) in enumerate(zip(S, colk)):
    yb = 4.9 - i * 0.75
    box(ax, 5.6, yb, 1.2, 0.55, s, '', k, tfs=8.5); box(ax, 7.0, yb, 1.3, 0.55, 'sub-network\nDense 16–32', '', k, tfs=7.5); arr(ax, 6.8, yb + 0.27, 7.0, yb + 0.27)
    arr(ax, 8.3, yb + 0.27, 8.7, 3.7)
box(ax, 8.7, 2.9, 1.0, 1.6, 'sensor\nattention\n(SE)', '', 'nav', tfs=8)
box(ax, 9.95, 3.3, 0.95, 0.8, 'concat +\nDense 32', '', 'o2', tfs=7.5, filled=True); arr(ax, 9.7, 3.7, 9.95, 3.7)
box(ax, 9.95, 2.2, 0.95, 0.6, 'output', '', 'gold', tfs=8.5); arr(ax, 10.42, 3.3, 10.42, 2.8)
box(ax, 0.3, 0.2, 10.4, 1.4, 'Shared settings', 'outputs: healthy/diseased (sigmoid), severity classes (softmax) or severity score (linear)\nloss: weighted cross-entropy or mean squared error | optimiser: Adam with weight decay\nearly stopping on an inner validation split | 5 random seeds averaged | inputs standardised with training-fold statistics', 'grey', fs=8)
save(fig, 'f8_dl.png')

# ---------------- F9 objective 3 timeline ----------------
fig, ax = canvas(11, 3.8)
ax.annotate('', xy=(10.6, 1.95), xytext=(0.4, 1.95), arrowprops=dict(arrowstyle='-|>', color='#333', lw=1.6)); ax.text(10.6, 1.7, 'time', ha='right', fontsize=8.5)
ax.text(0.4, 2.85, 'inoculation\n10 Jan 2026', fontsize=8.5, ha='left')
ax.add_patch(FancyBboxPatch((1.4, 2.1), 3.4, 0.6, boxstyle='round,pad=0.01,rounding_size=0.05', fc=L['o3'], ec=C['o3']))
ax.text(3.1, 2.4, 'pre-symptomatic dates (576 samples)', ha='center', va='center', fontsize=9, fontweight='bold', color=C['o3'])
ax.add_patch(FancyBboxPatch((5.2, 2.1), 5.1, 0.6, boxstyle='round,pad=0.01,rounding_size=0.05', fc=L['o2'], ec=C['o2']))
ax.text(7.75, 2.4, 'post-symptomatic dates (1536 samples)', ha='center', va='center', fontsize=9, fontweight='bold', color=C['o2'])
ax.plot([5.0, 5.0], [1.7, 3.1], color=C['o3'], ls='--'); ax.text(5.0, 3.25, 'first visible pustule', ha='center', fontsize=8.5, color=C['o3'])
ax.text(3.1, 1.2, 'label = later status of the same subplot\n(healthy control vs inoculated that becomes diseased)', ha='center', fontsize=8.5)
ax.text(7.75, 1.2, 'label = canopy severity score\nobserved on the same date', ha='center', fontsize=8.5)
ax.annotate('', xy=(4.2, 0.55), xytext=(6.6, 0.55), arrowprops=dict(arrowstyle='-|>', color=C['o3'], lw=1.2)); ax.text(5.4, 0.25, 'later status links the two periods', ha='center', fontsize=8, color=C['o3'])
save(fig, 'f9_obj3.png')

# ---------------- F10 Gantt ----------------
fig, ax = canvas(11, 5.2)
tasks = [('Pre-processing of all dates (P1–P8)', 0, 1.2, 'nav'), ('Feature extraction, feature tables (Chapter 4)', 1.0, 1.8, 'nav'), ('Objective 1: characterisation, DSF pools', 1.6, 2.6, 'o1'),
         ('Objective 2: single sensors (S1–S4), ML + DL', 2.4, 3.4, 'o2'), ('Objective 2: 11 combinations, contribution, maps', 3.2, 4.4, 'o2'), ('Objective 3: pre-symptomatic models, earliest day', 4.0, 5.2, 'o3'),
         ('Interpretation (SHAP), figures, writing', 5.0, 6.0, 'gold')]
for m in range(7): ax.plot([4.3 + m * 1.08, 4.3 + m * 1.08], [0.4, 4.6], color='#DDD', lw=0.8)
for m in range(6): ax.text(4.3 + m * 1.08 + 0.54, 4.75, 'Month %d' % (m + 1), ha='center', fontsize=9, fontweight='bold')
for i, (t, a, b, k) in enumerate(tasks):
    y = 4.1 - i * 0.55
    ax.text(0.2, y + 0.18, t, fontsize=8.6, va='center')
    ax.add_patch(FancyBboxPatch((4.3 + a * 1.08, y), (b - a) * 1.08, 0.36, boxstyle='round,pad=0.01,rounding_size=0.05', fc=C[k], ec=C[k]))
save(fig, 'f10_gantt.png')
print('figures ok')
