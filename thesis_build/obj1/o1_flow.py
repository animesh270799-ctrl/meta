"""Detailed flow charts of Objective 1 for each sensor."""
import os
import matplotlib; matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch
F = os.path.dirname(os.path.abspath(__file__)) + '/fig/'
plt.rcParams['font.family'] = 'DejaVu Sans'
COL = {'HS': '#00838F', 'MS': '#1565C0', 'RGB': '#2E7D32', 'TIR': '#C62828'}
FILL = {'HS': '#E0F2F1', 'MS': '#E3F2FD', 'RGB': '#E8F5E9', 'TIR': '#FFEBEE'}

def chart(key, title, tiers, outfile):
    h_box = [0.55 + 0.27 * max(len(t[1]), len(t[3]) + (2 if t[2] else 0)) for t in tiers]
    H = sum(h_box) + 0.45 * len(tiers) + 2.2
    fig, ax = plt.subplots(figsize=(10.5, H * 0.78)); ax.set_xlim(0, 10.5); ax.set_ylim(0, H); ax.axis('off')
    y = H - 0.25
    ax.add_patch(FancyBboxPatch((0.2, y - 0.6), 10.1, 0.6, boxstyle='round,pad=0.02,rounding_size=0.08', fc=COL[key], ec='none'))
    ax.text(5.25, y - 0.3, title, ha='center', va='center', color='white', fontsize=11.5, fontweight='bold'); y -= 0.95
    for (name, lines, side, outp), hb in zip(tiers, h_box):
        ax.add_patch(FancyBboxPatch((0.2, y - hb), 7.45, hb, boxstyle='round,pad=0.02,rounding_size=0.08', fc=FILL[key], ec=COL[key], lw=1.4))
        ax.text(0.35, y - 0.12, name, fontsize=10, fontweight='bold', va='top', color='#1E3A1F')
        ax.text(0.35, y - 0.45, '\n'.join(lines), fontsize=7.8, va='top', color='#222', linespacing=1.35)
        ax.add_patch(FancyBboxPatch((7.85, y - hb), 2.45, hb, boxstyle='round,pad=0.02,rounding_size=0.08', fc='#FFFDE7', ec='#C98A00', lw=1.1))
        ax.text(7.97, y - 0.12, 'Output', fontsize=8.8, fontweight='bold', va='top', color='#7A5900')
        ax.text(7.97, y - 0.42, '\n'.join(outp + (['', 'Basis: ' + side] if side else [])), fontsize=7.5, va='top', color='#333', linespacing=1.3)
        ax.annotate('', xy=(7.83, y - hb / 2), xytext=(7.67, y - hb / 2), arrowprops=dict(arrowstyle='-|>', color='#999', lw=1))
        y -= hb
        ax.annotate('', xy=(3.9, y - 0.4), xytext=(3.9, y - 0.03), arrowprops=dict(arrowstyle='-|>', color='#555', lw=1.3)); y -= 0.45
    ax.add_patch(FancyBboxPatch((0.2, y - 0.55), 10.1, 0.55, boxstyle='round,pad=0.02,rounding_size=0.08', fc='#F3E5F5', ec='#6A1B9A', lw=1.3))
    ax.text(5.25, y - 0.27, 'To the cross-sensor tier and to Objectives 2 and 3 (DSF pools for 6-grade classification and PDI regression)', ha='center', va='center', fontsize=8.8, fontweight='bold', color='#4A148C')
    plt.savefig(F + outfile, dpi=200, bbox_inches='tight'); plt.close()

chart('HS', 'Hyperspectral (VNIR 400–1000 nm + SWIR 1000–2500 nm): Objective 1 flow', [
 ('HS Tier 1  Feature extraction', ['Plot spectrum = mean of crop endmembers (30 per plot; soil, shadow, flowers out)', 'Remove 1350–1450 and 1800–1950 nm; Savitzky–Golay smoothing', '481 bands R + first derivative FD + second derivative SD (1443 band features)', 'Red-edge REP, Dr, SDr; 39 base indices (ROTI only if 1982 nm passes the noise check)', '+ 9 SWIR disease indices: DWSI-2/3/5, NDWI, MSI, NDII, RBI/NDBI (1148/1301), RBI (1068/1560)'], '', ['1443 band features', '3 red-edge parameters', '48 indices (39 + 9 SWIR)']),
 ('HS Tier 2  Band-level selection (bands only)', ['Correlation scalogram: Pearson r of R, FD, SD with PDI; p < 0.01 and top 5% |r|', 'ReliefF: 6 grades, k = 10, same-plot neighbours excluded; top 5% weights', 'Correlated regions (band-to-band r >= 0.95); keep one band per region from each list', 'Common -> both tasks; scalogram-only -> regression; ReliefF-only -> classification'], 'Shukla 2024; Mahlein 2013', ['Robust white-rust bands', 'Regression band list', 'Classification band list']),
 ('HS Tier 3  White Rust Index (WRI)', ['450–950 nm at 6 nm (84 bands); ReliefF top 25% of bands and of ND (>= 50 nm apart)', 'All ND x band x weight (-1, -0.5, 0, 0.5, 1) combinations; threshold per candidate', '8-fold stratified, plot-grouped CV; balanced accuracy healthy vs diseased', 'Repeat with SWIR; keep the better index; report r with PDI and grade means'], 'Mahlein 2013', ['WRI formula and threshold', 'Balanced accuracy', 'r with PDI']),
 ('HS Tier 4  Univariate response  (Method M1)', ['Input: 48 indices, REP/Dr/SDr, WRI, robust bands', 'One-way ANOVA + Tukey HSD across grades 0, 1, 3, 5, 7, 9', 'Pearson r with PDI; correlation with chlorophyll, carotenoid, anthocyanin, RWC'], '', ['Responding features', 'Direction of change', 'Physiological meaning']),
 ('HS Tier 5  Class discrimination  (Method M3, two steps)', ['VIF < 10 on each input set (Method M2)', 'Step 1: stepwise CDA on robust bands; Step 2: stepwise CDA on indices + WRI', 'Read canonical correlation, Wilks lambda, weights, score plot; held-out accuracy'], 'Bhattacharya 2013', ['Discriminating bands', 'Discriminating indices', 'Separability of 6 grades']),
 ('HS Tier 6  Disease-specific features  (Method M4)', ['Input: robust bands + red-edge + indices + WRI', 'Boruta (500 trees, <= 100 runs, p = 0.01) twice: 6-grade classes and PDI'], 'Mustafa 2023', ['HS DSF pool (classification)', 'HS DSF pool (regression)']),
], 'o1_flow_HS.png')

chart('MS', 'Multispectral (MicaSense RedEdge-MX: 475, 560, 668, 717, 840 nm): Objective 1 flow', [
 ('MS Tier 1  Feature extraction', ['Reflectance from panels + irradiance sensor; HS canopy mask transferred (edge erosion)', 'Plot means of 5 bands; 12 indices of the ORW (CIrededge, NDRE, PSRI, MTCI ...)', 'GLCM (32 levels, d = 1, 4 directions averaged): 8 measures x 5 bands = 40 textures', 'No band-level tier or WRI search: only 5 broad bands'], 'Liu 2024', ['57 MS features']),
 ('MS Tier 2  Univariate response  (Method M1)', ['ANOVA + Tukey across 6 grades; Pearson r with PDI', 'Correlation of red-edge indices with chlorophyll; textures with visual pustule cover'], '', ['Responding MS features', 'Direction and meaning']),
 ('MS Tier 3  Class discrimination  (Method M3, one step)', ['VIF < 10 (Method M2) -> stepwise CDA on the MS features', 'Canonical correlation, weights, score plot; held-out accuracy'], '', ['MS separability of 6 grades', 'Discriminating MS features']),
 ('MS Tier 4  Disease-specific features  (Method M4)', ['Boruta on 57 features: 6-grade classes and PDI'], '', ['MS DSF pools (2)']),
], 'o1_flow_MS.png')

chart('RGB', 'RGB (DJI Phantom): Objective 1 flow', [
 ('RGB Tier 1  Feature extraction', ['Orthomosaic + surface model; HS canopy mask transferred (edge erosion)', 'GLCM on R, G, B (32 levels, d = 1, 4 directions averaged): 8 measures x 3 = 24 textures', 'Mean hue, saturation, value; vegetation fraction VF; canopy height CH', 'Flower fraction (yellow pixels / canopy) stored as covariate, not as a disease feature'], 'Haralick 1973; Feng 2022', ['29 RGB features', 'Flower-fraction covariate']),
 ('RGB Tier 2  Univariate response  (Method M1)', ['ANOVA + Tukey across 6 grades; Pearson r with PDI', 'Check that features do not simply follow flower fraction (r with covariate)'], '', ['Responding RGB features', 'Confounding check']),
 ('RGB Tier 3  Class discrimination  (Method M3, one step)', ['VIF < 10 (Method M2) -> stepwise CDA on RGB features', 'Canonical correlation, weights, score plot; held-out accuracy'], '', ['RGB separability of 6 grades']),
 ('RGB Tier 4  Disease-specific features  (Method M4)', ['Boruta on 29 features: 6-grade classes and PDI'], '', ['RGB DSF pools (2)']),
], 'o1_flow_RGB.png')

chart('TIR', 'Thermal (FLIR Vue Pro R, 7.5–13.5 µm): Objective 1 flow', [
 ('TIR Tier 1  Feature extraction', ['Camera warm-up 15–20 min; radiometric conversion (emissivity, air T, RH, height)', 'HS canopy mask transferred with edge erosion (no warm soil pixels)', 'CT; CTD = CT - AT; CTR in kelvin; NRCT within image; MTD = max - min in plot', 'GLCM on temperature image (common range for all flights): 8 textures'], 'Feng 2022; Mahlein 2019', ['13 TIR features']),
 ('TIR Tier 2  Univariate response  (Method M1)', ['ANOVA + Tukey across 6 grades; Pearson r with PDI', 'Correlation with stomatal conductance and transpiration', 'Thermal–water check: warmer plots must not have lower RWC / water index'], 'Bhattacharya 2013', ['Responding TIR features', 'Disease vs drought check']),
 ('TIR Tier 3  Class discrimination  (Method M3, one step)', ['VIF < 10 (Method M2) -> stepwise CDA on TIR features', 'Canonical correlation, weights, score plot; held-out accuracy'], '', ['TIR separability of 6 grades']),
 ('TIR Tier 4  Disease-specific features  (Method M4)', ['Boruta on 13 features: 6-grade classes and PDI'], '', ['TIR DSF pools (2)']),
], 'o1_flow_TIR.png')
print('ok')
