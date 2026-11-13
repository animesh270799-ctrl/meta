"""New figures for guide v2: crop temporal profiles, masking workflow, detailed satellite pipeline, infection physiology."""
import os, sys, shutil
import numpy as np, matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch
B = os.path.dirname(os.path.abspath(__file__)) + '/'; FG = B + 'fig/'
sys.path.insert(0, B + '../obj1'); from o1_flow import chart, COL, FILL
plt.rcParams.update({'font.family': 'DejaVu Sans', 'font.size': 9})
d = np.arange(0, 197)                                        # days from 1 October
lab = ['1 Oct', '1 Nov', '1 Dec', '1 Jan', '1 Feb', '1 Mar', '1 Apr']; tk = [0, 31, 61, 92, 123, 151, 182]
def dl(mn, mx, up, r1, down, r2): return mn + (mx - mn) * (1 / (1 + np.exp(-r1 * (d - up))) - 1 / (1 + np.exp(-r2 * (d - down))))
nd = {'Mustard': dl(0.15, 0.80, 45, 0.10, 145, 0.12), 'Wheat': dl(0.15, 0.85, 80, 0.08, 170, 0.10), 'Chickpea': dl(0.15, 0.60, 55, 0.07, 150, 0.10),
      'Potato': dl(0.15, 0.80, 35, 0.12, 105, 0.15), 'Fallow': 0.15 + 0 * d}
cc = {'Mustard': '#C98A00', 'Wheat': '#2E7D32', 'Chickpea': '#6A1B9A', 'Potato': '#6D4C41', 'Fallow': '#9E9E9E'}
ndyi = 0.05 + 0.25 * np.exp(-0.5 * ((d - 100) / 9) ** 2)
vh = {'Mustard': -22 + 9 / (1 + np.exp(-0.1 * (d - 55))) - 6 / (1 + np.exp(-0.15 * (d - 150))), 'Wheat': -21 + 6 / (1 + np.exp(-0.08 * (d - 95))) - 4 / (1 + np.exp(-0.12 * (d - 175))),
      'Chickpea': -22 + 5 / (1 + np.exp(-0.07 * (d - 65))) - 4 / (1 + np.exp(-0.1 * (d - 150))), 'Potato': -22 + 7 / (1 + np.exp(-0.12 * (d - 40))) - 7 / (1 + np.exp(-0.15 * (d - 105))), 'Fallow': -22 + 0 * d}
fig, ax = plt.subplots(3, 1, figsize=(11, 9), sharex=True)
for a in ax:
    a.axvspan(31, 85, color='#E8F5E9', zorder=0); a.axvspan(85, 115, color='#FFF8E1', zorder=0); a.axvspan(115, 150, color='#F3E5F5', zorder=0)
ax[0].text(58, 0.9, 'vegetative', ha='center', fontsize=8.5); ax[0].text(100, 0.9, 'flowering', ha='center', fontsize=8.5); ax[0].text(132, 0.9, 'pod / maturity', ha='center', fontsize=8.5)
for k, v in nd.items(): ax[0].plot(d, v, color=cc[k], lw=2, label=k)
ax[0].set_ylabel('NDVI'); ax[0].set_ylim(0, 1); ax[0].legend(ncol=5, frameon=False, fontsize=8, loc='lower center'); ax[0].set_title('(a) NDVI profiles: mustard greens up earlier and senesces earlier than wheat', fontsize=9.5)
ax[1].plot(d, ndyi, color='#C98A00', lw=2, label='Mustard'); ax[1].plot(d, 0.05 + 0 * d, color='#2E7D32', lw=2, label='Wheat, chickpea, potato')
ax[1].set_ylabel('NDYI (G − B)/(G + B)'); ax[1].legend(frameon=False, fontsize=8); ax[1].set_title('(b) Yellow-flower index: unique peak of mustard at flowering', fontsize=9.5)
for k, v in vh.items(): ax[2].plot(d, v, color=cc[k], lw=2, label=k)
ax[2].set_ylabel('Sentinel-1 VH (dB)'); ax[2].set_title('(c) SAR VH backscatter: earlier volume-scattering rise in broad-leaved, branched mustard', fontsize=9.5)
ax[2].set_xticks(tk, lab)
fig.text(0.5, 0.005, 'Schematic, typical profiles for north-west India rabi season (illustrative only; calibrate with local ground truth)', ha='center', fontsize=8.5, style='italic')
plt.tight_layout(rect=(0, 0.02, 1, 1)); plt.savefig(FG + 'i2_profiles.png', dpi=200); plt.close()

COL.update({'K': '#C98A00', 'S2': '#1565C0'}); FILL.update({'K': '#FFF8E1', 'S2': '#E3F2FD'})
chart('K', 'Mustard crop masking: vegetative stage to flowering (proposed workflow)', [
 ('1  Prior knowledge and reference data', ['Crop calendar by district; previous-season crop maps; agricultural mask (exclude forest, water, built-up)', 'Ground truth: geotagged fields of mustard, wheat, chickpea, potato, others, fallow (two dates)'], 'Olofsson 2014', ['Training and validation sets']),
 ('2  Data cube (5–10-day steps)', ['Sentinel-2 / LISS-IV / LISS-III / AWiFS surface reflectance with cloud masks', 'Sentinel-1 / EOS-04 SAR (VV, VH, VH/VV), speckle-filtered; same grid'], 'Veloso 2017', ['Gap-filled time series']),
 ('3  Vegetative-stage features (Nov–mid-Dec)', ['Green-up date and slope, NDVI/NDRE level, SWIR ratios (canopy water, leaf structure)', 'SAR VH rise and VH/VV (broad-leaved branched canopy); temporal offset vs wheat'], 'Inglada 2016', ['Early mustard probability']),
 ('4  Flowering-stage features (late Dec–Jan)', ['Yellow-flower indices: NDYI (G−B)/(G+B), (R+G)/B, flowering date', 'Flowering confirms or corrects the early map'], 'Sulik 2016; Ashourloo 2019', ['Refined mustard map']),
 ('5  Classifier and post-processing', ['Random forest / SVM on all features; time-weighted DTW; parcel (object) majority', 'Train with previous-season labels for early-season maps'], 'Belgiu 2018', ['Mustard mask (10 m)']),
 ('6  Accuracy and area', ['Stratified random reference sample; confusion matrix; error-adjusted area with CI'], 'Olofsson 2014', ['Acreage with uncertainty']),
], 'i2_maskflow.png', foot='Early (vegetative) maps are provisional; flowering-stage evidence gives the final mask')
chart('S2', 'Using the thesis at satellite scale: detailed pipeline (proposed)', [
 ('1  Spectral transfer', ['UAV/leaf disease features → satellite bands by spectral response function convolution', 'Keep features that survive band broadening (red edge, SWIR-1, thermal)'], 'Thenkabail 2004', ['Satellite-ready features']),
 ('2  Crop mask', ['Mustard mask from vegetative + flowering features (separate workflow)'], 'Ashourloo 2019', ['Mustard pixels']),
 ('3  Weather risk (when)', ['Cool, humid, dew/fog spells; sowing date; risk score per day and grid cell'], 'Chattopadhyay 2011', ['Risk windows']),
 ('4  Normal-profile anomaly (where)', ['Deviation of red edge, SWIR and LST from the stage-specific normal; z-scores'], 'Dutta 2014', ['Stressed mustard pixels']),
 ('5  Stress attribution (what)', ['Drought: LST ↑ + water index ↓ + soil moisture ↓; disease: LST ↑ with normal water + disease index', 'Nutrient, frost, flowering checks'], 'Bhattacharya 2013', ['Disease-probable pixels']),
 ('6  Severity model (how much)', ['Classifier/regressor trained with UAV-derived sub-pixel PDI at sentinel sites'], 'This thesis', ['Severity map']),
 ('7  Validation and delivery', ['Independent ground surveys and UAV transects; district statistics; advisories'], 'Olofsson 2014', ['Operational product']),
], 'i2_satflow.png', foot='When (weather) → where (anomaly) → what (attribution) → how much (severity)')
for f in ('i2_maskflow.png', 'i2_satflow.png'): shutil.move(B + '../obj1/fig/' + f, FG + f)

fig, ax = plt.subplots(figsize=(12, 5.4)); ax.set_xlim(0, 12); ax.set_ylim(0, 5.4); ax.axis('off')
def bx(x, y, w, h, t, fc, ec, fs=8.3, bold=False, tc='#1E2A2A'):
    ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle='round,pad=0.02,rounding_size=0.06', fc=fc, ec=ec, lw=1.2)); ax.text(x + w / 2, y + h / 2, t, ha='center', va='center', fontsize=fs, fontweight='bold' if bold else 'normal', color=tc)
def ar(x1, y1, x2, y2): ax.annotate('', xy=(x2, y2), xytext=(x1, y1), arrowprops=dict(arrowstyle='-|>', color='#666', lw=1.1))
bx(0.2, 2.2, 2.0, 1.0, 'Albugo candida\ninfection (biotroph)', '#C62828', '#C62828', 9, True, 'white')
phys = ['Stomatal closure,\ntranspiration ↓', 'Photosynthesis ↓,\nxanthophyll / NPQ change', 'Chlorophyll loss,\nchlorosis', 'Pustules break epidermis;\nmesophyll disrupted', 'Leaf water loss', 'Hypertrophy, staghead\n(structure change)']
sig = ['Canopy temperature ↑\n(thermal, CWSI)', 'PRI, fluorescence\nchange', 'Visible ↑, red-edge\nshift to shorter λ', 'NIR ↓; white pustule\ntexture (RGB)', 'SWIR reflectance ↑\n(1450–2400 nm)', 'Canopy height / texture\n(DSM, GLCM)']
for i, (p_, s_) in enumerate(zip(phys, sig)):
    y = 4.65 - i * 0.85
    bx(3.0, y - 0.35, 3.0, 0.7, p_, '#FFF8E1', '#C98A00'); bx(7.0, y - 0.35, 3.0, 0.7, s_, '#E3F2FD', '#1565C0')
    ar(2.22, 2.7, 2.98, y); ar(6.02, y, 6.98, y)
ax.text(4.5, 5.25, 'Physiological response', ha='center', fontsize=9.5, fontweight='bold'); ax.text(8.5, 5.25, 'Remote-sensing signal', ha='center', fontsize=9.5, fontweight='bold')
ax.text(11.1, 4.3, 'earlier\n(pre-symptomatic)', ha='center', fontsize=8, color='#2E7D32'); ax.text(11.1, 0.9, 'later\n(visible)', ha='center', fontsize=8, color='#C62828')
ax.annotate('', xy=(11.1, 1.35), xytext=(11.1, 3.9), arrowprops=dict(arrowstyle='-|>', color='#555', lw=1.5))
ax.set_title('From infection to remote-sensing signal: why each sensor can see white rust (after Mahlein, 2016; Mahlein et al., 2019)', fontsize=10)
plt.tight_layout(); plt.savefig(FG + 'i2_physio.png', dpi=200); plt.close()
print('ok')
