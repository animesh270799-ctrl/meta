"""Figures for the revised field methodology: flow charts, architecture diagrams and dummy-data illustrations."""
import os, itertools
import numpy as np
import matplotlib; matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, Rectangle
F = os.path.dirname(os.path.abspath(__file__)) + '/fig/'
plt.rcParams.update({'font.family': 'DejaVu Sans', 'font.size': 9})
C = dict(hs='#00838F', ms='#1565C0', rgb='#2E7D32', tir='#C62828', nav='#1F3864', o1='#2E75B6', o2='#7030A0', o3='#C00000', gold='#B8860B', grey='#616161', dl='#6A1B9A')
L = dict(hs='#E0F2F1', ms='#E3F2FD', rgb='#E8F5E9', tir='#FFEBEE', nav='#EEF1F6', o1='#DEEBF7', o2='#EDE2F6', o3='#F9E0DE', gold='#FFF4D6', grey='#F2F2F2', dl='#F3E5F5')
GC = ['#2E7D32', '#9CCC65', '#FDD835', '#FB8C00', '#E53935', '#7B1FA2']; GL = ['0', '1', '3', '5', '7', '9']
rng = np.random.default_rng(7)

def box(ax, x, y, w, h, title, body='', k='nav', fs=8.3, tfs=9.3, filled=False):
    ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle='round,pad=0.01,rounding_size=0.06', fc=C[k] if filled else L[k], ec=C[k], lw=1.3))
    col = 'white' if filled else '#1a1a1a'
    if body:
        ax.text(x + w / 2, y + h - 0.1, title, ha='center', va='top', fontsize=tfs, fontweight='bold', color='white' if filled else C[k])
        ax.text(x + w / 2, y + h - 0.4, body, ha='center', va='top', fontsize=fs, color=col, linespacing=1.3)
    else:
        ax.text(x + w / 2, y + h / 2, title, ha='center', va='center', fontsize=tfs, fontweight='bold', color=col, linespacing=1.25)
def arr(ax, x1, y1, x2, y2, c='#555'):
    ax.annotate('', xy=(x2, y2), xytext=(x1, y1), arrowprops=dict(arrowstyle='-|>', color=c, lw=1.3))
def canvas(w, h):
    fig, ax = plt.subplots(figsize=(w, h)); ax.set_xlim(0, w); ax.set_ylim(0, h); ax.axis('off'); return fig, ax
def save(fig, name):
    fig.savefig(F + name, dpi=200, bbox_inches='tight'); plt.close(fig)
def chain(name, title, steps, k, w=11):
    h = 0.9 + sum(0.62 + 0.24 * s[1].count('\n') for s in steps) + 0.22 * len(steps)
    fig, ax = canvas(w, h); box(ax, 0.3, h - 0.75, w - 0.6, 0.6, title, '', k, tfs=11, filled=True); y = h - 0.95
    for i, (t, b, o) in enumerate(steps):
        hb = 0.62 + 0.24 * b.count('\n')
        ax.add_patch(FancyBboxPatch((0.3, y - hb), 7.2, hb, boxstyle='round,pad=0.01,rounding_size=0.05', fc=L[k], ec=C[k], lw=1.2))
        ax.text(0.45, y - 0.1, t, fontsize=9.3, fontweight='bold', va='top', color=C[k]); ax.text(0.45, y - 0.37, b, fontsize=8.1, va='top', color='#222', linespacing=1.3)
        ax.add_patch(FancyBboxPatch((7.7, y - hb), w - 8.0, hb, boxstyle='round,pad=0.01,rounding_size=0.05', fc=L['gold'], ec=C['gold'], lw=1))
        ax.text(7.82, y - 0.1, 'Output', fontsize=8.4, fontweight='bold', va='top', color='#7A5900'); ax.text(7.82, y - 0.36, o, fontsize=7.9, va='top', color='#333', linespacing=1.25)
        arr(ax, 7.5, y - hb / 2, 7.7, y - hb / 2, '#999'); y -= hb
        if i < len(steps) - 1: arr(ax, 3.9, y, 3.9, y - 0.2)
        y -= 0.22
    save(fig, name)

# ======================= FLOW CHARTS =======================
fig, ax = canvas(11, 14.6)
rows = [('Common Activity A – Field experiment, ground truth, covariates and datasets', 'four inoculation timings × three varieties (PM 26, Pusa Vijay, PM 37) × three replications + twelve healthy plots = 48 plots; four scored subplots\ncovariates: days after inoculation, variety, timing, growth stage, weather; post-symptomatic and pre-symptomatic datasets', 'nav'),
        ('Common Activity B – Image pre-processing', 'radiometric calibration → mosaics → hyperspectral cube quality control → projection and co-registration → resampling to the hyperspectral grid', 'nav'),
        ('Common Activity C – Endmember extraction and vegetation mask', 'minimum noise fraction → pixel purity index → n-dimensional visualisation → endmember library → spectral angle mapper classes\n→ vegetation mask (soil, grass and shadow removed; leaves and flowers kept)', 'nav'),
        ('Common Activity D – Subplot spectra and feature extraction', 'mean of vegetation pixels per subplot → reflectance, first derivative, red-edge parameters, vegetation indices,\nprincipal-component texture, multispectral, colour and thermal features', 'nav'),
        ('Common Activity E – Normalisation and data preparation', 'thermal normalisation → healthy-plot normalisation (healthy plots rotated across folds)\n→ standardisation with training statistics → class weights', 'gold'),
        ('Common Activity F – Validation design and tuning', 'leave-one-replication-out outer folds grouped by plot; inner grouped folds for selection and tuning; leakage checklist', 'gold'),
        ('Objective 1 – Characterisation (Activities 1.1–1.6)', 'response curves → optimal wavelengths (SHAP-CARS) → two-band and three-band indices (NDSI, RSI, White Rust Index)\n→ index selection (ReliefF) → texture (principal components, co-occurrence matrix, mRMR) and Tri-band Texture Fusion Index → feature sets', 'o1'),
        ('Objective 2 – Detection and severity discrimination (Activities 2.1–2.6), 1920 post-symptomatic samples', 'feature-group inputs and 15 sensor sets with feature-level fusion | machine learning, feature-fusion neural networks,\nDT-EDNet, EfficientNet, ResNet18, ConvNeXt V2 | detection, severity classes, severity score | ablation, maps', 'o2'),
        ('Objective 3 – Pre-symptomatic prediction (Activities 3.1–3.5), 576 pre-symptomatic samples', 'labels from the later status of each subplot | normalisation to healthy plots | same feature selection | machine learning and\nfeature-fusion neural networks | earliest detection day and risk maps', 'o3')]
y = 14.3
for i, (t, b, k) in enumerate(rows):
    box(ax, 0.3, y - 1.35, 10.4, 1.25, t, b, k, fs=7.9, tfs=9.8)
    if i < len(rows) - 1: arr(ax, 5.5, y - 1.35, 5.5, y - 1.52)
    y -= 1.6
save(fig, 'g01_overall.png')

chain('g02_preproc.png', 'Common Activity B – Image pre-processing (Steps B1–B5)', [
    ('B1  Radiometric calibration', 'hyperspectral and multispectral: reflectance panels (empirical line) and sunlight sensor\nred–green–blue: fixed exposure; thermal: temperature with emissivity 0.98', 'reflectance and temperature images'),
    ('B2  Orthomosaics and georeferencing', 'structure-from-motion mosaics; push-broom hyperspectral lines georectified;\nsame ground control points on all dates', 'georeferenced mosaics'),
    ('B3  Hyperspectral cube quality control', '613 → 483 bands; drop 916–920 nm; Savitzky–Golay smoothing on each\ncontinuous band segment; reflectance on a 0–1 scale', 'clean 483-band cube'),
    ('B4  Projection and co-registration', 'all images to WGS 84 / UTM zone 43N; image-to-image registration to the\nhyperspectral image; check-point error below one hyperspectral pixel', 'aligned images'),
    ('B5  Resampling to the hyperspectral grid', 'red–green–blue: pixel aggregate; multispectral: bilinear; thermal: nearest neighbour\n(red–green–blue texture computed before resampling)', 'one 2.2 cm grid for all cameras')], 'nav')

chain('g03_endmember.png', 'Common Activity C – Endmember extraction and vegetation mask (Steps C1–C7)', [
    ('C1  Sampling of pixels from all dates', 'random vegetation-and-background pixels from each date inside the field', 'pooled pixel sample'),
    ('C2  Minimum noise fraction (MNF) transformation', 'noise estimated from neighbouring-pixel differences; noise whitening; components\nordered by signal-to-noise ratio; keep components with eigenvalue clearly above 1', 'MNF components'),
    ('C3  Pixel purity index (PPI)', '10 000 random projections ("skewers") of the MNF pixel cloud; count how often each\npixel is an extreme; high counts = spectrally pure pixels', 'pure-pixel candidates'),
    ('C4  n-dimensional visualisation and endmember selection', 'clusters of pure pixels at the corners of the MNF pixel cloud; endmember spectrum =\nmean reflectance of each cluster', 'endmember library'),
    ('C5  Endmember identification', 'name each endmember (green canopy, stressed canopy, flower, soil, grass, shadow)\nwith field photographs, red–green–blue images and leaf spectra', 'labelled endmember library'),
    ('C6  Spectral angle mapper (SAM) classification', 'class of each pixel = endmember with the smallest spectral angle (calibrated threshold)', 'class map'),
    ('C7  Vegetation mask and accuracy check', 'keep green canopy, stressed canopy and flower; remove soil, grass, shadow;\nNDVI rule for flowers; one-pixel erosion; confusion matrix on reference pixels', 'vegetation mask')], 'nav')

chain('g04_features.png', 'Common Activity D – Subplot spectra and feature extraction (Steps D1–D6)', [
    ('D1  Plot and subplot polygons', '48 plots × 4 quadrant subplots; inner buffer; same polygons on all dates', '192 subplots'),
    ('D2  Subplot mean spectra', 'mean of the masked vegetation pixels in each subplot for every band and camera', 'subplot spectra'),
    ('D3  Hyperspectral features', 'reflectance (483 bands), first derivative, red-edge parameters, published indices', 'hyperspectral groups'),
    ('D4  Texture features', 'principal components of the cube → grey-level co-occurrence matrix (8 measures)\non 3 components; red–green–blue, multispectral and thermal texture', 'texture groups'),
    ('D5  Multispectral and red–green–blue features', 'band reflectance, indices, colour indices', 'multispectral and colour groups'),
    ('D6  Thermal features', 'canopy temperature statistics; canopy minus air temperature; normalised temperatures', 'thermal group')], 'nav')

chain('g05_obj1.png', 'Objective 1 – Characterisation of white rust by each camera (Activities 1.1–1.6)', [
    ('Activity 1.1  Response curves', 'spectra, indices, texture and temperature by severity class, variety, inoculation timing and date', 'response figures'),
    ('Activity 1.2  Optimal wavelengths (SHAP-CARS)', 'effective ranges from NDSI and RSI maps → Shapley values on a tree ensemble →\ncompetitive adaptive reweighted sampling with partial least squares', 'optimal wavelength set'),
    ('Activity 1.3  Spectral index construction', 'all-pair NDSI and RSI search; three-band White Rust Index', 'best spectral indices'),
    ('Activity 1.4  Vegetation index selection (ReliefF)', 'published indices + red-edge parameters + constructed indices → ReliefF weights', 'selected indices'),
    ('Activity 1.5  Texture selection (mRMR) and TTFI', 'principal-component texture → mRMR → ordered triplets → Tri-band Texture Fusion Index', 'selected texture + best TTFI'),
    ('Activity 1.6  Disease-specific feature sets', 'union of selected groups per camera; variance inflation factor below 10; treatment response', 'disease-specific feature set\nof each camera')], 'o1')

chain('g06_obj2.png', 'Objective 2 – Detection and severity discrimination (Activities 2.1–2.6)', [
    ('Activity 2.1  Tasks and inputs', 'detection, severity classes, severity score; hyperspectral feature-group inputs;\n15 sensor sets with feature-level fusion', 'input matrices per fold'),
    ('Activity 2.2  Machine-learning models', 'support vector machine, random forest, extreme gradient boosting, k-nearest\nneighbours, partial least squares', 'predictions'),
    ('Activity 2.3  Deep-learning models', 'feature-fusion networks (DNN-F1, DNN-F2) and pseudo-image networks\n(DT-EDNet, EfficientNet, ResNet18, ConvNeXt V2)', 'predictions'),
    ('Activity 2.4  Evaluation', 'overall accuracy, kappa, macro recall and F1, per-class scores; R², RMSE, RPD', 'metric tables'),
    ('Activity 2.5  Comparison, ablation and interpretation', 'best model per sensor set; fusion gain; drop-one-sensor; DT-EDNet ablation;\nSHAP; gain over the covariate-only baseline', 'best sensor set and model'),
    ('Activity 2.6  Robustness and maps', 'results by variety and inoculation timing; leave-one-variety-out; subplot maps', 'robustness tables, maps')], 'o2')

chain('g07_obj3.png', 'Objective 3 – Pre-symptomatic prediction (Activities 3.1–3.5)', [
    ('Activity 3.1  Pre-symptomatic samples and labels', 'healthy plots vs inoculated subplots that become diseased later; later severity score', 'labelled 576 samples'),
    ('Activity 3.2  Normalisation to healthy plots', 'feature minus mean of healthy plots of the same date and variety', 'normalised features'),
    ('Activity 3.3  Feature selection', 'same one-method-per-feature-type procedure with pre-symptomatic labels', 'pre-symptomatic feature sets'),
    ('Activity 3.4  Models for 15 sensor sets', 'machine-learning models and feature-fusion neural networks (smaller)', 'predictions'),
    ('Activity 3.5  Earliest detection and risk maps', 'sensitivity, specificity, balanced accuracy, AUC by day after inoculation;\ncovariate-only baseline', 'earliest detection day; maps')], 'o3')

chain('g08_selection.png', 'One feature-selection method for each feature type (inside each training fold)', [
    ('Spectral bands (reflectance + first derivative)', 'SHAP-CARS: Shapley pre-screening, then competitive adaptive reweighted sampling', '10–15 optimal wavelengths'),
    ('Two-band indices (NDSI, RSI) and White Rust Index', 'exhaustive search; strongest correlation with severity on training plots', '3–5 constructed indices'),
    ('Vegetation indices and red-edge parameters', 'ReliefF (classes) or RReliefF (severity score)', 'top 5–8 indices'),
    ('Texture (co-occurrence) features', 'minimum redundancy maximum relevance (mRMR)', 'top 6 texture features'),
    ('Tri-band Texture Fusion Index', 'all ordered triplets of selected texture features in 3 formulas; strongest |r|', 'best TTFI'),
    ('Thermal and multispectral bands', 'small groups: kept (only near-duplicates removed)', 'thermal and band features'),
    ('Across groups', 'variance inflation factor below 10', 'disease-specific feature set')], 'o1')


chain('g25_normalisation.png', 'Common Activity E – Normalisation and data preparation (Steps E1–E4)', [
    ('E1  Thermal normalisation', 'canopy minus air temperature; normalised relative canopy temperature over the field;\ncrop water stress index with wet and dry references', 'weather-independent thermal features'),
    ('E2  Healthy-plot normalisation', 'feature minus the mean of the healthy plots of the same date and variety\n(divided by their standard deviation); healthy plots of the training part only', 'date- and variety-free features\n(used in Objective 3)'),
    ('E3  Standardisation with training statistics', 'z-score of every feature with the mean and standard deviation of the training part;\nthe same values applied to the test part', 'standardised features'),
    ('E4  Class weights', 'weight of each class inversely proportional to its size in the training part', 'balanced loss functions')], 'gold')

# validation
fig, ax = canvas(11, 5.6)
for f in range(3):
    y = 4.4 - f * 1.25; ax.text(0.35, y + 0.3, 'Outer fold %d' % (f + 1), fontsize=10, fontweight='bold', va='center')
    for j in range(3):
        test = j == f; box(ax, 1.9 + j * 2.0, y, 1.85, 0.6, 'R%d + 4 healthy\n(V1–V3 rotated)' % (j + 1), '', 'o3' if test else 'o1', tfs=8.5, filled=test)
    ax.text(8.1, y + 0.3, 'test = replication %d (≈ 640 samples)\ntrain = other two (≈ 1280)' % (f + 1), fontsize=8.5, va='center')
box(ax, 0.3, 0.15, 10.4, 0.95, 'Inside each training part', 'inner 3-fold cross-validation grouped by plot: feature selection, tuning, early stopping (validation plots, not random samples)\nthe test replication is used only once, for the final evaluation', 'gold', fs=8.4)
save(fig, 'g09_validation.png')

# 15 combinations
fig, ax = canvas(11, 5.0); S = ['Hyperspectral', 'Multispectral', 'Red–green–blue', 'Thermal']; colk = ['hs', 'ms', 'rgb', 'tir']
combos = [c for r in range(1, 5) for c in itertools.combinations(range(4), r)]
for j, c in enumerate(combos):
    x = 2.3 + j * 0.57; ax.text(x + 0.23, 4.55, 'S%d' % (j + 1), ha='center', fontsize=8.3, fontweight='bold')
    for i in range(4): ax.add_patch(FancyBboxPatch((x, 3.6 - i * 0.62), 0.46, 0.5, boxstyle='round,pad=0.01,rounding_size=0.05', fc=C[colk[i]] if i in c else '#F4F4F4', ec='#BBB', lw=0.8))
for i, s in enumerate(S): ax.text(2.15, 3.85 - i * 0.62, s, ha='right', va='center', fontsize=9.5, fontweight='bold', color=C[colk[i]])
for lab, a, b in (('single cameras', 0, 3), ('pairs', 4, 9), ('triples', 10, 13), ('all four', 14, 14)):
    xa, xb = 2.3 + a * 0.57, 2.3 + b * 0.57 + 0.46; ax.plot([xa, xb], [1.15, 1.15], color='#555', lw=1.2); ax.text((xa + xb) / 2, 0.8, lab, ha='center', fontsize=9)
ax.text(5.8, 0.25, '15 sensor sets = 4 single + 6 pairs + 4 triples + 1 all-four (feature-level fusion)', ha='center', fontsize=9.5, style='italic')
save(fig, 'g10_combinations.png')

# ======================= DUMMY DATA FIGURES =======================
wl = np.arange(400, 2401, 2.0)
def canopy(sev):
    s = sev / 9
    vis = 0.04 + 0.05 * np.exp(-((wl - 550) / 35) ** 2) * (1 - 0.3 * s) + 0.03 * s * np.exp(-((wl - 650) / 60) ** 2)
    rep = 718 - 12 * s; nir = (0.48 - 0.12 * s) / (1 + np.exp(-(wl - rep) / 11))
    water = (1 - 0.6 * np.exp(-((wl - 1450) / 70) ** 2) - 0.75 * np.exp(-((wl - 1940) / 90) ** 2) - 0.15 * np.exp(-((wl - 1200) / 50) ** 2) - 0.1 * np.exp(-((wl - 970) / 30) ** 2))
    swir = np.where(wl > 1300, (0.10 + 0.06 * s) * np.exp(-((wl - 1650) / 400) ** 2) + (0.05 + 0.04 * s) * np.exp(-((wl - 2200) / 200) ** 2), 0)
    r = vis + nir * np.where(wl < 1300, 1, np.exp(-(wl - 1300) / 900)) * water + swir * water
    return r
gap = ((wl > 1329) & (wl < 1461)) | ((wl > 1779) & (wl < 1971)) | ((wl > 898) & (wl < 921))
fig, axs = plt.subplots(1, 2, figsize=(11, 3.8))
for g, c in zip([0, 1, 3, 5, 7, 9], GC):
    r = canopy(g); rr = r.copy(); rr[gap] = np.nan; axs[0].plot(wl, rr, color=c, lw=1.4, label='grade %d' % g)
    m = (wl >= 650) & (wl <= 800); axs[1].plot(wl[m], np.gradient(r[m], wl[m]) * 1000, color=c, lw=1.4)
axs[0].set(xlabel='Wavelength (nm)', ylabel='Reflectance', title='(a) Subplot mean reflectance by severity grade'); axs[0].legend(fontsize=7, ncol=2)
axs[1].set(xlabel='Wavelength (nm)', ylabel='First derivative (×10⁻³ nm⁻¹)', title='(b) First derivative in the red edge')
for a in axs: a.grid(alpha=.3)
fig.text(0.5, -0.02, 'Dummy data for illustration only', ha='center', fontsize=8, style='italic', color='#777'); plt.tight_layout(); save(fig, 'g11_dummy_spectra.png')

# MNF / PPI / endmembers
fig, axs = plt.subplots(1, 3, figsize=(12, 3.6))
ev = np.r_[np.array([310, 120, 48, 22, 11, 6, 4.2, 3.1, 2.4]), 1 + 0.6 * np.exp(-np.arange(16) / 4) + rng.normal(0, .05, 16)]
axs[0].semilogy(np.arange(1, 26), ev, 'o-', ms=3); axs[0].axhline(1, color='k', ls='--', lw=.8); axs[0].axhline(2, color='r', ls=':', lw=.8)
axs[0].set(xlabel='MNF component', ylabel='Eigenvalue', title='(a) MNF eigenvalues (≈ 1 = noise)')
corners = np.array([[3.2, 0.2], [-2.6, 2.4], [-2.2, -2.3], [0.8, 3.0], [1.3, -2.9]])
w = rng.dirichlet(np.ones(5) * 0.6, 4000); pts = w @ corners + rng.normal(0, .15, (4000, 2))
axs[1].scatter(pts[:, 0], pts[:, 1], s=2, c='#90A4AE')
names = ['green canopy', 'soil', 'shadow', 'yellow flower', 'stressed canopy']; cc = ['#2E7D32', '#8D6E63', '#424242', '#F9A825', '#9E9D24']
for (x, y), n, c in zip(corners, names, cc): axs[1].scatter([x], [y], s=60, c=c, edgecolor='k', zorder=3); axs[1].text(x + 0.15, y + 0.15, n, fontsize=7.5)
axs[1].set(xlabel='MNF 1', ylabel='MNF 2', title='(b) Pure pixels (PPI) at the corners')
specs = {'green canopy': canopy(0), 'stressed canopy': canopy(7), 'yellow flower': canopy(0) * 0.75 + 0.25 * np.clip((wl - 500) / 60, 0, 1) * np.exp(-((wl - 900) / 900) ** 2),
         'soil': 0.12 + 0.18 * (wl - 400) / 2000 - 0.03 * np.exp(-((wl - 1940) / 80) ** 2), 'shadow': canopy(0) * 0.18}
for (n, s), c in zip(specs.items(), ['#2E7D32', '#9E9D24', '#F9A825', '#8D6E63', '#424242']):
    ss = s.copy(); ss[gap] = np.nan; axs[2].plot(wl, ss, color=c, lw=1.3, label=n)
axs[2].set(xlabel='Wavelength (nm)', ylabel='Reflectance', title='(c) Endmember library'); axs[2].legend(fontsize=7)
for a in axs: a.grid(alpha=.3)
fig.text(0.5, -0.03, 'Dummy data for illustration only', ha='center', fontsize=8, style='italic', color='#777'); plt.tight_layout(); save(fig, 'g12_dummy_endmember.png')

# SAM angle diagram + mask grid
fig, axs = plt.subplots(1, 2, figsize=(10.5, 3.9))
a = axs[0]; a.set_xlim(0, 1); a.set_ylim(0, 1); a.set_aspect('equal')
for v, lab, c in (((0.85, 0.35), 'endmember r (green canopy)', '#2E7D32'), ((0.6, 0.62), 'pixel t', '#1565C0')): a.annotate('', xy=v, xytext=(0, 0), arrowprops=dict(arrowstyle='-|>', color=c, lw=2)); a.text(v[0] + 0.01, v[1] + 0.02, lab, color=c, fontsize=8.5)
th = np.linspace(np.arctan2(0.35, 0.85), np.arctan2(0.62, 0.6), 30); a.plot(0.25 * np.cos(th), 0.25 * np.sin(th), color='k'); a.text(0.27, 0.17, 'α', fontsize=12)
a.set(xlabel='reflectance in band 1', ylabel='reflectance in band 2', title='(a) Spectral angle between two spectra'); a.grid(alpha=.3)
cls = rng.choice(5, (12, 12), p=[.55, .1, .08, .12, .15]); cls[0, :] = 3; cls[:, 0] = 3
cmap = matplotlib.colors.ListedColormap(['#2E7D32', '#9E9D24', '#F9A825', '#8D6E63', '#424242'])
axs[1].imshow(cls, cmap=cmap, vmin=0, vmax=4); keep = np.isin(cls, [0, 1, 2])
for i in range(12):
    for j in range(12):
        if keep[i, j]: axs[1].text(j, i, '1', ha='center', va='center', fontsize=6.5, color='white')
axs[1].set(title='(b) SAM classes → mask (1 = kept: canopy, stressed, flower)'); axs[1].set_xticks([]); axs[1].set_yticks([])
fig.text(0.5, -0.02, 'Dummy data for illustration only', ha='center', fontsize=8, style='italic', color='#777'); plt.tight_layout(); save(fig, 'g13_dummy_sam.png')

# NDSI R2 map
w2 = np.arange(450, 1001, 10); W1, W2 = np.meshgrid(w2, w2)
r2 = 0.15 + 0.55 * np.exp(-((W1 - 760) / 90) ** 2 - ((W2 - 560) / 70) ** 2) + 0.45 * np.exp(-((W1 - 940) / 60) ** 2 - ((W2 - 700) / 40) ** 2) + rng.normal(0, .02, W1.shape)
r2 = np.clip((r2 + r2.T) / 2, 0, 0.8)
fig, ax = plt.subplots(figsize=(5.6, 4.6)); im = ax.contourf(W1, W2, r2, levels=16, cmap='viridis'); plt.colorbar(im, label='R² with severity score')
i, j = np.unravel_index(np.argmax(r2), r2.shape); ax.plot(W1[i, j], W2[i, j], 'r*', ms=12)
ax.set(xlabel='λ₁ (nm)', ylabel='λ₂ (nm)', title='NDSI(λ₁, λ₂): R² with severity (training plots)')
fig.text(0.5, -0.02, 'Dummy data for illustration only', ha='center', fontsize=8, style='italic', color='#777'); plt.tight_layout(); save(fig, 'g14_dummy_ndsi.png')

# SHAP-CARS
fig, axs = plt.subplots(1, 3, figsize=(12.5, 3.7))
bw = np.arange(450, 1001, 6); shap = 0.02 + 0.5 * np.exp(-((bw - 560) / 25) ** 2) + 0.8 * np.exp(-((bw - 720) / 20) ** 2) + 0.4 * np.exp(-((bw - 940) / 25) ** 2) + rng.gamma(1, 0.03, bw.size)
thr = np.quantile(shap, 0.6); axs[0].bar(bw, shap, width=5, color=np.where(shap >= thr, '#00838F', '#B0BEC5'))
axs[0].axhline(thr, color='r', ls='--', lw=.8); axs[0].set(xlabel='Wavelength (nm)', ylabel='mean |SHAP|', title='(a) Shapley pre-screening (top 40% kept)')
it = np.arange(1, 51); nvar = np.maximum(12, (np.sum(shap >= thr) * np.exp(-0.06 * it)).astype(int))
rmse = 1.6 - 0.5 * (1 - np.exp(-it / 9)) + 0.004 * np.maximum(0, it - 30) ** 1.6 + rng.normal(0, .01, it.size)
axs[1].plot(it, nvar, 'k-'); axs[1].set(xlabel='CARS iteration', ylabel='number of wavelengths', title='(b) Wavelengths kept per iteration')
best = int(np.argmin(rmse)); axs[2].plot(it, rmse, color='#7030A0'); axs[2].axvline(it[best], color='r', ls='--', lw=.8)
axs[2].text(it[best] + 1, rmse.max() * 0.97, 'minimum RMSECV\n→ %d wavelengths' % nvar[best], fontsize=8, va='top')
axs[2].set(xlabel='CARS iteration', ylabel='RMSE of cross-validation', title='(c) Choice of the optimal subset')
for a in axs: a.grid(alpha=.3)
fig.text(0.5, -0.03, 'Dummy data for illustration only', ha='center', fontsize=8, style='italic', color='#777'); plt.tight_layout(); save(fig, 'g15_dummy_shapcars.png')

# ReliefF + mRMR + texture PCA
fig, axs = plt.subplots(1, 3, figsize=(12.5, 3.7))
vis = ['RVI', 'PSSRb', 'CIrededge', 'CIgreen', 'SR', 'NDRE', 'PRI', 'ARI', 'WRI', 'REP', 'MTCI', 'NDVI']; wts = np.sort(rng.uniform(0.005, 0.06, len(vis)))[::-1]
axs[0].barh(vis[::-1], wts[::-1], color=['#2E75B6' if i >= len(vis) - 6 else '#B0BEC5' for i in range(len(vis))]); axs[0].set(xlabel='ReliefF weight', title='(a) Index weights (top 6 kept)')
pc = np.cumsum([78, 13, 5.4, 1.6, 0.9, 0.5, 0.3, 0.3]); axs[1].plot(range(1, 9), pc, 'o-'); axs[1].axhline(95, color='r', ls='--', lw=.8); axs[1].set(xlabel='principal component', ylabel='cumulative variance (%)', title='(b) Cube principal components (3 kept)', ylim=(70, 101))
tf = ['PC2-Dis', 'PC2-Con', 'PC2-Hom', 'PC3-Mea', 'PC2-Var', 'PC2-Ent', 'PC1-Var', 'PC1-Con', 'PC3-Hom', 'PC1-Sec']; sc = np.sort(rng.uniform(0.1, 0.7, len(tf)))[::-1]
axs[2].barh(tf[::-1], sc[::-1], color=['#2E7D32' if i >= len(tf) - 6 else '#B0BEC5' for i in range(len(tf))]); axs[2].set(xlabel='mRMR score', title='(c) Texture ranking (top 6 kept)')
for a in axs: a.grid(alpha=.3, axis='x')
fig.text(0.5, -0.03, 'Dummy data for illustration only', ha='center', fontsize=8, style='italic', color='#777'); plt.tight_layout(); save(fig, 'g16_dummy_relief_mrmr.png')

# TTFI
fig, ax = plt.subplots(figsize=(8, 3.6)); labels = ['TTFI1\n(Con, Var, Dis)', 'TTFI2\n(Mea, Dis, Con)', 'TTFI3\n(Dis, Con, Hom)', 'best single\ntexture (Dis)', 'best index\n(RVI)']
vals = [0.71, -0.73, 0.76, 0.69, 0.66]; ax.bar(labels, np.abs(vals), color=['#7030A0', '#7030A0', '#C00000', '#9E9E9E', '#9E9E9E'])
for i, v in enumerate(vals): ax.text(i, abs(v) + 0.01, 'r = %.2f' % v, ha='center', fontsize=8.5)
ax.set(ylabel='|r| with severity score', ylim=(0, 0.9), title='Best triplet of each TTFI formula compared with single features'); ax.grid(alpha=.3, axis='y')
fig.text(0.5, -0.03, 'Dummy data for illustration only', ha='center', fontsize=8, style='italic', color='#777'); plt.tight_layout(); save(fig, 'g17_dummy_ttfi.png')

# pseudo-image reshaping
fig, ax = canvas(11, 3.6)
vals = np.round(rng.uniform(-1.5, 1.5, 22), 1) + 0.0; vals[vals == 0] = 0.1; grp = ['W'] * 10 + ['I'] * 6 + ['T'] * 5 + ['F']
colmap = {'W': '#B2EBF2', 'I': '#BBDEFB', 'T': '#C8E6C9', 'F': '#FFE0B2'}
for i, (v, g) in enumerate(zip(vals, grp)): ax.add_patch(Rectangle((0.3 + i * 0.27, 2.6), 0.25, 0.5, fc=colmap[g], ec='#666', lw=.6)); ax.text(0.3 + i * 0.27 + 0.125, 2.85, '%.1f' % v, ha='center', va='center', fontsize=5.5)
ax.text(3.3, 3.3, 'standardised feature vector (22 features: wavelengths, indices, texture, TTFI)', ha='center', fontsize=8.5)
arr(ax, 3.3, 2.5, 3.3, 1.9)
for k in range(25):
    i, j = divmod(k, 5); g = grp[k] if k < 22 else None
    ax.add_patch(Rectangle((2.05 + j * 0.5, 0.15 + (4 - i) * 0.33), 0.48, 0.31, fc=colmap[g] if g else '#EEEEEE', ec='#666', lw=.6)); ax.text(2.05 + j * 0.5 + 0.24, 0.15 + (4 - i) * 0.33 + 0.155, '%.1f' % vals[k] if k < 22 else '0', ha='center', va='center', fontsize=6)
ax.text(4.8, 1.0, '5 × 5 pseudo-image\n(row-wise filling, zero padding,\nfeatures ordered by group and\nwavelength so neighbours are related)', fontsize=8.5, va='center')
box(ax, 8.2, 0.5, 2.5, 1.3, 'network input\n1 × 5 × 5', '', 'dl', tfs=9); arr(ax, 7.4, 1.15, 8.2, 1.15)
for g, lab, x in (('W', 'wavelengths', 0.3), ('I', 'indices', 1.7), ('T', 'texture', 2.8), ('F', 'TTFI', 3.9)): ax.add_patch(Rectangle((x + 6.2, 2.0), 0.22, 0.2, fc=colmap[g], ec='#666')); ax.text(x + 6.5, 2.1, lab, fontsize=7.5, va='center')
save(fig, 'g18_pseudoimage.png')

# DT-EDNet architecture
import textwrap
def wbox(ax, x, y, w, h, title, body, k, width, fs=7.6, tfs=8.6):
    box(ax, x, y, w, h, title, textwrap.fill(body, width), k, fs=fs, tfs=tfs)
fig, ax = canvas(12, 6.6)
seq = [('Input\npseudo-image', 'grey', 0.2), ('3 × 3\nconvolution\nembedding\n(128 channels)', 'dl', 1.75), ('Squeeze-and-\nexcitation\nblock', 'o1', 3.3), ('Flatten to\ntokens +\nclass token', 'grey', 4.85)]
for t, k, x in seq: box(ax, x, 4.3, 1.4, 1.3, t, '', k, tfs=8.0)
for x in (1.6, 3.15, 4.7): arr(ax, x, 4.95, x + 0.15, 4.95)
ax.add_patch(FancyBboxPatch((6.5, 3.95), 3.65, 2.35, boxstyle='round,pad=0.01,rounding_size=0.08', fc='#FAF5FF', ec=C['dl'], lw=1.4, ls='--'))
ax.text(8.32, 6.12, 'Dual Transformer Group', ha='center', fontsize=9.5, fontweight='bold', color=C['dl'])
box(ax, 6.65, 4.2, 1.6, 1.6, 'Kernel\nTransformer\nBlock\n(convolution\n+ CBAM)', '', 'dl', tfs=7.6); box(ax, 8.4, 4.2, 1.6, 1.6, '4 × Token\nTransformer\nBlock\n(self-attention\n+ feed-forward)', '', 'dl', tfs=7.6)
arr(ax, 6.25, 4.95, 6.65, 4.95); arr(ax, 8.25, 5.0, 8.4, 5.0)
box(ax, 10.45, 4.3, 1.4, 1.3, 'Layer norm.\nof class token\n→ linear head', '', 'gold', tfs=7.8); arr(ax, 10.15, 4.95, 10.45, 4.95)
ax.text(11.15, 4.15, 'softmax: classes\nlinear: severity score', ha='center', va='top', fontsize=7.6)
det = [('Squeeze-and-excitation block', 'Global average pooling of each channel, a small two-layer network and a sigmoid give one weight per channel; the channels are multiplied by their weights, which suppresses redundant responses.', 'o1'),
       ('CBAM (in the Kernel Transformer Block)', 'Channel attention (average and maximum pooling followed by a shared network) and then spatial attention (convolution on the pooled maps) focus on the informative positions of the pseudo-image.', 'dl'),
       ('Token Transformer Block', 'Every token attends to all other tokens with four-head scaled dot-product self-attention, followed by a feed-forward network; this links distant features, for example a red-edge band and a texture feature.', 'dl')]
for i, (t, b_, k) in enumerate(det): wbox(ax, 0.2 + i * 3.95, 1.75, 3.8, 1.85, t, b_, k, 46)
ax.set_ylim(1.6, 6.6); fig.set_size_inches(12, 5.0)
save(fig, 'g19_dtednet.png')

# CNN comparators
fig, ax = canvas(12, 2.9)
cmp_ = [('ResNet18', 'stem: 3 × 3 convolution, stride 1 (small input)\n4 stages × 2 basic residual blocks\n(two 3 × 3 convolutions + identity shortcut)\nglobal average pooling → linear head', 'ms'),
        ('EfficientNet-B0', 'stem: 3 × 3 convolution, stride 1\nmobile inverted bottleneck blocks\n(depthwise convolution + squeeze-and-excitation)\ncompound scaling of depth, width, resolution\nglobal average pooling → linear head', 'rgb'),
        ('ConvNeXt V2 (Atto size)', 'stem: 2 × 2 convolution, stride 1\nblocks: 7 × 7 depthwise convolution,\nlayer normalisation, feed-forward network\nwith global response normalisation\nglobal average pooling → linear head', 'tir')]
for i, (t, b, k) in enumerate(cmp_): box(ax, 0.2 + i * 3.95, 0.65, 3.8, 2.15, t, b, k, fs=7.8, tfs=10)
ax.text(6, 0.3, 'Same input pseudo-images, same folds and the same training settings as DT-EDNet (fair comparison)', ha='center', fontsize=9, style='italic')
save(fig, 'g20_cnns.png')

# DNN F1/F2
fig, ax = canvas(11, 5.0)
ax.text(2.6, 4.8, 'DNN-F1: input-level feature fusion', ha='center', fontsize=10, fontweight='bold', color=C['o2'])
for i, (s, k) in enumerate(zip(['hyperspectral', 'multispectral', 'red–green–blue', 'thermal'], colk)): box(ax, 0.2, 3.75 - i * 0.75, 1.5, 0.55, s, '', k, tfs=7.8); arr(ax, 1.7, 4.02 - i * 0.75, 2.05, 2.95)
box(ax, 2.05, 2.15, 1.1, 1.6, 'concat', '', 'nav', tfs=8.5); box(ax, 3.4, 3.0, 1.6, 0.55, 'dense 64', '', 'o2', tfs=8, filled=True); box(ax, 3.4, 2.2, 1.6, 0.55, 'dense 32', '', 'o2', tfs=8, filled=True); box(ax, 3.4, 1.4, 1.6, 0.55, 'output', '', 'gold', tfs=8)
arr(ax, 3.15, 2.95, 3.4, 3.25); arr(ax, 4.2, 3.0, 4.2, 2.75); arr(ax, 4.2, 2.2, 4.2, 1.95)
ax.text(8.2, 4.8, 'DNN-F2: intermediate fusion with sensor attention', ha='center', fontsize=10, fontweight='bold', color=C['o2'])
for i, (s, k) in enumerate(zip(['hyperspectral', 'multispectral', 'red–green–blue', 'thermal'], colk)):
    yb = 3.75 - i * 0.75; box(ax, 5.6, yb, 1.5, 0.55, s, '', k, tfs=7.8); box(ax, 7.3, yb, 1.2, 0.55, 'dense 16–32', '', k, tfs=7.5); arr(ax, 7.1, yb + 0.27, 7.3, yb + 0.27); arr(ax, 8.5, yb + 0.27, 8.85, 2.95)
box(ax, 8.85, 2.15, 0.95, 1.6, 'sensor\nattention', '', 'nav', tfs=8); box(ax, 9.95, 2.6, 0.85, 0.7, 'dense\n32', '', 'o2', tfs=7.8, filled=True); box(ax, 9.95, 1.6, 0.85, 0.55, 'output', '', 'gold', tfs=7.8)
arr(ax, 9.8, 2.95, 9.95, 2.95); arr(ax, 10.37, 2.6, 10.37, 2.15)
ax.text(5.5, 0.6, 'Inputs: selected features of each camera (standardised); Adam optimiser, early stopping on grouped validation plots, 5 random seeds', ha='center', fontsize=8.5, style='italic')
save(fig, 'g21_dnn.png')

# confusion matrix dummy
cm = np.array([[118, 9, 1, 0, 0, 0], [14, 61, 15, 2, 0, 0], [2, 13, 52, 16, 2, 0], [0, 2, 14, 71, 12, 1], [0, 0, 2, 13, 64, 7], [0, 0, 0, 2, 9, 30]])
fig, ax = plt.subplots(figsize=(5, 4.2)); ax.imshow(cm, cmap='Greens')
for i in range(6):
    for j in range(6): ax.text(j, i, cm[i, j], ha='center', va='center', fontsize=8, color='white' if cm[i, j] > 60 else 'k')
ax.set_xticks(range(6)); ax.set_yticks(range(6)); ax.set_xticklabels(GL); ax.set_yticklabels(GL); ax.set(xlabel='predicted grade', ylabel='observed grade', title='Confusion matrix of one test replication')
fig.text(0.5, -0.02, 'Dummy data for illustration only', ha='center', fontsize=8, style='italic', color='#777'); plt.tight_layout(); save(fig, 'g22_dummy_cm.png')
np.save(F + 'cm.npy', cm)

# earliest detection
fig, ax = plt.subplots(figsize=(7, 3.6)); dai = np.array([2, 5, 8])
for lab, c, vals in (('hyperspectral + thermal', '#7030A0', [0.58, 0.66, 0.74]), ('hyperspectral', '#00838F', [0.56, 0.63, 0.71]), ('thermal', '#C62828', [0.56, 0.62, 0.68]), ('red–green–blue', '#2E7D32', [0.48, 0.52, 0.57])):
    ax.plot(dai, vals, 'o-', color=c, label=lab)
ax.axhline(0.7, color='k', ls='--', lw=.8); ax.text(5.0, 0.705, 'chosen reliability level (0.70)', fontsize=8, ha='center')
ax.set_xticks(dai); ax.set_xticklabels(['12 Jan\n(2 DAI)', '15 Jan\n(5 DAI)', '18 Jan\n(8 DAI)'])
ax.set(xlabel='pre-symptomatic flight date (days after inoculation)', ylabel='balanced accuracy', title='Accuracy on the three pre-symptomatic dates', ylim=(0.4, 0.8)); ax.legend(fontsize=7.5, loc='lower right'); ax.grid(alpha=.3)
fig.text(0.5, -0.03, 'Dummy data for illustration only', ha='center', fontsize=8, style='italic', color='#777'); plt.tight_layout()
save(fig, 'g23_dummy_earliest.png')

# Gantt
fig, ax = canvas(11, 5.4)
tasks = [('Common Activities A–C (all dates, all cameras)', 0, 1.2, 'nav'), ('Common Activity D: features; Activity E: folds', 1.0, 1.8, 'nav'), ('Objective 1: Activities 1.1–1.6', 1.6, 2.7, 'o1'),
         ('Objective 2: machine learning, feature-fusion networks', 2.5, 3.6, 'o2'), ('Objective 2: DT-EDNet and convolutional networks', 3.0, 4.3, 'o2'), ('Objective 2: comparison, ablation, maps', 4.0, 4.7, 'o2'), ('Objective 3: Activities 3.1–3.5', 4.3, 5.4, 'o3'), ('Interpretation, figures, writing', 5.2, 6.0, 'gold')]
for m in range(7): ax.plot([4.6 + m * 1.03, 4.6 + m * 1.03], [0.4, 4.9], color='#DDD', lw=0.8)
for m in range(6): ax.text(4.6 + m * 1.03 + 0.51, 5.05, 'Month %d' % (m + 1), ha='center', fontsize=9, fontweight='bold')
for i, (t, a, b, k) in enumerate(tasks):
    y = 4.4 - i * 0.52; ax.text(0.15, y + 0.17, t, fontsize=8.4, va='center')
    ax.add_patch(FancyBboxPatch((4.6 + a * 1.03, y), (b - a) * 1.03, 0.34, boxstyle='round,pad=0.01,rounding_size=0.05', fc=C[k], ec=C[k]))
save(fig, 'g24_gantt.png')

# dataset structure (13 flight dates)
fig, ax = canvas(11, 4.6)
lv = [('13 flight dates\n(3 pre- and 10 post-\nsymptomatic)', 'nav'), ('4 cameras\nper date', 'ms'), ('48 plots\nper image', 'rgb'), ('4 scored\nsubplots\nper plot', 'tir')]
for i, (t, k) in enumerate(lv):
    box(ax, 0.3 + i * 2.7, 2.7, 2.45, 1.4, t, '', k, tfs=10, filled=True)
    if i < 3: arr(ax, 2.75 + i * 2.7, 3.4, 3.0 + i * 2.7, 3.4)
box(ax, 0.3, 0.4, 5.1, 1.8, 'Post-symptomatic set (Objectives 1 and 2)', '1920 subplot samples per camera\n(10 dates × 48 plots × 4 subplots; 21 Jan – 25 Mar 2027)\nlabels: severity score, class, healthy / diseased', 'o2', fs=9)
box(ax, 5.7, 0.4, 5.0, 1.8, 'Pre-symptomatic set (Objective 3)', '576 subplot samples per camera\n(3 dates × 48 plots × 4 subplots; 12, 15, 18 Jan 2027)\nlabels: healthy / infected (later status), later severity', 'o3', fs=9)
save(fig, 'g26_dataset.png')

# timeline of the 13 flights
fig, ax = canvas(12, 4.2)
dates = [('12 Jan', 2), ('15 Jan', 5), ('18 Jan', 8), ('21 Jan', 11), ('28 Jan', 18), ('4 Feb', 25), ('11 Feb', 32), ('18 Feb', 39), ('25 Feb', 46), ('4 Mar', 53), ('11 Mar', 60), ('18 Mar', 67), ('25 Mar', 74)]
x0, sc = 1.6, 0.135
ax.annotate('', xy=(11.85, 2.3), xytext=(1.45, 2.3), arrowprops=dict(arrowstyle='-|>', color='#333', lw=1.5))
ax.plot([x0, x0], [2.05, 2.55], color='k', lw=2); ax.text(x0 - 0.12, 2.3, 'inoculation\n10 Jan 2027', ha='right', va='center', fontsize=7.8)
for i, (d, dai) in enumerate(dates):
    x = x0 + dai * sc; c = C['o3'] if i < 3 else C['o2']
    ax.plot(x, 2.3, 'o', color=c, ms=8)
    yl = 1.45 if i in (1, 3) else 1.95
    ax.text(x, yl, '%s\n%d DAI' % (d, dai), ha='center', va='top', fontsize=7.2)
ax.add_patch(FancyBboxPatch((x0 + 1.0 * sc, 2.75), 8.2 * sc, 0.55, boxstyle='round,pad=0.01,rounding_size=0.05', fc=L['o3'], ec=C['o3']))
ax.text(x0 + 5.1 * sc, 3.02, 'pre-\nsymptomatic', ha='center', va='center', fontsize=7.0, fontweight='bold', color=C['o3'])
ax.text(x0 + 5.1 * sc, 3.62, '3 dates\n576 samples', ha='center', va='center', fontsize=7.4, color=C['o3'])
ax.add_patch(FancyBboxPatch((x0 + 10 * sc, 2.75), 65 * sc, 0.55, boxstyle='round,pad=0.01,rounding_size=0.05', fc=L['o2'], ec=C['o2']))
ax.text(x0 + 42.5 * sc, 3.02, 'post-symptomatic: 10 dates, 1920 samples (label = severity score observed on the same date)', ha='center', va='center', fontsize=8.2, fontweight='bold', color=C['o2'])
ax.text(0.4, 0.55, 'pre-symptomatic label = later status of the same subplot (healthy control vs inoculated subplot that becomes diseased)', ha='left', fontsize=8)
ax.text(0.4, 0.2, 'all four cameras (red–green–blue, multispectral, thermal, hyperspectral) and visual severity scoring on every date', ha='left', fontsize=8, style='italic')
save(fig, 'g27_obj3.png')
print('figures ok')
