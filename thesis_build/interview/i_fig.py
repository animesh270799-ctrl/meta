"""Figures for the NRSC/SAC interview guide (Q&A)."""
import os, sys, shutil, json
import numpy as np, matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch, Circle
B = os.path.dirname(os.path.abspath(__file__)) + '/'; FG = B + 'fig/'; os.makedirs(FG, exist_ok=True)
sys.path.insert(0, B + '../obj1'); from o1_flow import chart, COL, FILL
plt.rcParams.update({'font.family': 'DejaVu Sans', 'font.size': 9})
def box(ax, x, y, w, h, t, fc, ec, fs=9, bold=False, tc='#1E2A2A'):
    ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle='round,pad=0.02,rounding_size=0.08', fc=fc, ec=ec, lw=1.3))
    ax.text(x + w / 2, y + h / 2, t, ha='center', va='center', fontsize=fs, fontweight='bold' if bold else 'normal', color=tc, wrap=True)
def arr(ax, x1, y1, x2, y2, c='#555'):
    ax.annotate('', xy=(x2, y2), xytext=(x1, y1), arrowprops=dict(arrowstyle='-|>', color=c, lw=1.4))

# ---------- 1. problem -> gap -> solution ----------
fig, ax = plt.subplots(figsize=(11, 3.3)); ax.set_xlim(0, 11); ax.set_ylim(0, 3.3); ax.axis('off')
cols = [('PROBLEM', '#C62828', '#FFEBEE', ['White rust (Albugo candida):', 'leaf pustules + staghead', 'Visual scoring: slow, subjective,', 'point-based, late', 'Sprays are calendar-based,', 'not need-based']),
        ('RESEARCH GAPS', '#C98A00', '#FFF8E1', ['No sensor study of white rust', 'No disease-specific index', 'Sensors never compared on', 'the same plots', 'No pre-symptomatic test', 'No link to satellite scale']),
        ('MY SOLUTION', '#2E7D32', '#E8F5E9', ['Leaf ASD + UAV HS, MS, RGB, TIR', 'Tiered feature analysis + WRI', 'ML / DNN fusion: 6 grades + PDI', 'Pre-symptomatic risk maps', 'Bands mapped to satellites']),
        ('OUTCOME FOR ISRO', '#1565C0', '#E3F2FD', ['Disease-sensitive bands and', 'index for sensor design', 'Training/validation data for', 'satellite models', 'Input to advisories', '(Krishi-DSS type platforms)'])]
for i, (t, ec, fc, lines) in enumerate(cols):
    x = 0.2 + i * 2.72
    box(ax, x, 2.55, 2.4, 0.6, t, ec, ec, 10, True, 'white')
    ax.add_patch(FancyBboxPatch((x, 0.15), 2.4, 2.2, boxstyle='round,pad=0.02,rounding_size=0.08', fc=fc, ec=ec, lw=1.3))
    ax.text(x + 0.12, 2.2, '\n'.join(lines), va='top', fontsize=8.6, linespacing=1.55)
    if i < 3: arr(ax, x + 2.42, 1.25, x + 2.7, 1.25)
plt.tight_layout(); plt.savefig(FG + 'i_problem.png', dpi=200); plt.close()

# ---------- 2. scaling framework leaf -> UAV -> satellite ----------
fig, ax = plt.subplots(figsize=(11, 4.4)); ax.set_xlim(0, 11); ax.set_ylim(0, 4.4); ax.axis('off')
lv = [('Leaf (ASD)', 'cm', 'Pure disease signal;\nwavelengths and WRI', '#00695C'), ('UAV (HS/MS/RGB/TIR)', '3–36 cm', 'Plot severity, fusion,\npre-symptomatic maps', '#AD1457'),
      ('Satellite', '5.8–30 m (opt.)\n57–100 m (TIR)', 'District/state maps,\nadvisories, insurance', '#1565C0')]
for i, (t, res, out, c) in enumerate(lv):
    x = 0.3 + i * 3.6
    box(ax, x, 2.5, 3.0, 1.4, t + '\n' + res, c, c, 11, True, 'white')
    box(ax, x, 0.6, 3.0, 1.4, out, '#F5F7F7', c, 9.5)
    arr(ax, x + 1.5, 2.48, x + 1.5, 2.02)
    if i < 2: arr(ax, x + 3.02, 3.2, x + 3.58, 3.2, c)
ax.text(5.5, 4.2, 'Each level calibrates and validates the next (spectral resampling, ground truth, sub-pixel training)', ha='center', fontsize=9.5, style='italic')
ax.text(3.6, 2.25, 'band selection\n→ sensor SRF', ha='center', fontsize=7.5, color='#555'); ax.text(7.2, 2.25, 'UAV maps = training\n& validation pixels', ha='center', fontsize=7.5, color='#555')
plt.tight_layout(); plt.savefig(FG + 'i_scaling.png', dpi=200); plt.close()

# ---------- 3. schematic spectra with satellite bands (no measured data) ----------
from scipy.interpolate import PchipInterpolator
w = np.arange(400, 2401)
ph = [(400,.040),(450,.045),(500,.060),(550,.120),(600,.070),(650,.045),(680,.040),(700,.090),(720,.250),(750,.420),(800,.460),(900,.470),(970,.440),(1050,.460),(1200,.400),(1300,.420),(1450,.200),(1650,.300),(1800,.270),(1940,.080),(2100,.180),(2200,.200),(2300,.150),(2400,.110)]
pd_ = [(400,.060),(450,.070),(500,.090),(550,.150),(600,.110),(650,.090),(680,.085),(700,.130),(720,.240),(750,.350),(800,.380),(900,.390),(970,.370),(1050,.390),(1200,.360),(1300,.380),(1450,.240),(1650,.330),(1800,.300),(1940,.120),(2100,.220),(2200,.240),(2300,.190),(2400,.140)]
keep = ~((w >= 1350) & (w <= 1450)) & ~((w >= 1800) & (w <= 1950))
fig, ax = plt.subplots(figsize=(12, 6.2))
for pts, c, lab in ((ph, '#2E7D32', 'healthy canopy (schematic)'), (pd_, '#7B1FA2', 'infected canopy (schematic)')):
    m = PchipInterpolator(*zip(*pts))(w); m[~keep] = np.nan; ax.plot(w, m, color=c, lw=2, label=lab)
for lo, hi, c, tx in ((680, 760, '#FFCDD2', 'red edge'), (500, 680, '#FFF9C4', 'pigments'), (1450, 1800, '#BBDEFB', 'SWIR-1 water'), (1950, 2400, '#E1F5FE', 'SWIR-2 water / dry matter')):
    ax.axvspan(lo, hi, color=c, alpha=0.8, zorder=0); ax.text((lo + hi) / 2, 0.66, tx, ha='center', fontsize=8, color='#333')
sens = [('Sentinel-2 MSI', [(490, 65), (560, 35), (665, 30), (705, 15), (740, 15), (783, 20), (842, 115), (865, 20), (1610, 90), (2190, 180)], '#1565C0'),
        ('LISS-IV (RS-2/2A)', [(555, 70), (650, 60), (815, 90)], '#C62828'),
        ('LISS-III / AWiFS', [(555, 70), (650, 60), (815, 90), (1625, 150)], '#EF6C00'),
        ('HySIS / EnMAP / PRISMA', [(1400, 2000)], '#6A1B9A')]
for k, (nm, bands, c) in enumerate(sens):
    yy = -0.04 - 0.045 * k
    for cen, wid in bands: ax.plot([cen - wid / 2, cen + wid / 2], [yy, yy], color=c, lw=6, solid_capstyle='butt')
    ax.text(2410, yy, nm, va='center', fontsize=8, color=c)
ax.set_xlim(380, 2900); ax.set_ylim(-0.23, 0.72); ax.set_xlabel('Wavelength (nm)'); ax.set_ylabel('Reflectance')
ax.set_title('Schematic canopy spectra (healthy vs infected) with disease-sensitive regions from the literature and satellite band positions', fontsize=10)
ax.legend(loc='upper right', fontsize=8.5, frameon=False); ax.axhline(0, color='grey', lw=0.5)
plt.tight_layout(); plt.savefig(FG + 'i_bands.png', dpi=200); plt.close()

# ---------- 4. satellite upscaling pipeline & 5. operational architecture (flow charts) ----------
COL.update({'S': '#1565C0', 'O': '#1E3A1F'}); FILL.update({'S': '#E3F2FD', 'O': '#EEF3E8'})
chart('S', 'Satellite-scale methodology for white rust (proposed)', [
 ('Step 1  Mustard crop mask', ['Sentinel-1 / EOS-04 SAR + Sentinel-2 / LISS-IV time series (Nov–Feb)', 'Yellow-flower signal at flowering (NDYI); parcel boundaries (Krishi-DSS parcels)'], 'Fang 2016', ['Mustard mask', '(10 m)']),
 ('Step 2  Weather risk layer (Stage I)', ['IMD gridded / AWS + MOSDAC: T, RH, rainfall, dew, cloud', 'White rust risk model (cool, humid spells; late sowing)'], 'Chattopadhyay 2011', ['Daily risk map', '(district/5 km)']),
 ('Step 3  Stress screening (Stage II)', ['Red-edge and SWIR anomalies vs normal profile (S2 B5–B7, B11)', 'Thermal (Landsat / TRISHNA) + water index: disease vs drought'], 'Dutta 2014; Bhattacharya 2013', ['Stressed mustard', 'pixels']),
 ('Step 4  Disease discrimination (Stage III)', ['UAV-derived bands/WRI resampled to satellite SRF; RF/SVM', 'Training pixels from UAV maps (sub-pixel PDI)'], 'This thesis', ['White rust probability', 'and severity class']),
 ('Step 5  Validation and products', ['Ground surveys (Conn key), UAV transects; accuracy, R²', 'District maps, advisories, insurance support'], 'Feng 2022', ['Operational maps']),
], 'i_satflow.png', foot='Same three-stage logic as Bhattacharya and Chattopadhyay (2013), with UAV-derived disease bands added')
chart('O', 'How ISRO could run a national white-rust service (proposed architecture)', [
 ('Data layer', ['Sentinel-2, Resourcesat (LISS-IV/III, AWiFS), EOS-04 SAR, HySIS-class HS, TRISHNA TIR', 'IMD/MOSDAC weather; ICAR/KVK ground observations; UAV calibration sites'], 'VEDAS; Bhuvan', ['Analysis-ready data cube']),
 ('Model layer', ['Crop mask → weather risk → spectral anomaly → disease classifier', 'Models trained with UAV + ground data; retrained each season'], 'This thesis', ['Risk and severity maps']),
 ('Delivery layer', ['Krishi-DSS / Bhuvan dashboards; SMS advisories via KVKs and state departments', 'Inputs for PMFBY loss assessment and pesticide planning'], 'Krishi-DSS 2024', ['Advisories, statistics']),
 ('Feedback layer', ['Farmer and KVK reports, sentinel plots, drone surveys', 'Accuracy tracking; model updates'], '', ['Continuous improvement']),
], 'i_ops.png', foot='Pilot first in Rajasthan, Haryana and Madhya Pradesh mustard belts; then scale nationally')
for f in ('i_satflow.png', 'i_ops.png'): shutil.move(B + '../obj1/fig/' + f, FG + f)

# ---------- 6. disease cycle and weather ----------
fig, ax = plt.subplots(figsize=(9.5, 6.4)); ax.set_xlim(-5.2, 5.2); ax.set_ylim(-3.6, 3.6); ax.set_aspect('equal'); ax.axis('off')
st = [('Oospores in soil /\ncrop debris\n(primary inoculum)', 90), ('Zoospores in free water\ninfect cotyledons/leaves\n(10–20 °C, wet leaf)', 18), ('White pustules\n(sori) on lower\nleaf surface', -54), ('Sporangia spread by\nwind and rain splash\n(secondary cycles)', -126), ('Systemic infection:\nstaghead of inflorescence\n(often with downy mildew)', 162)]
r = 2.55
for i, (t, a) in enumerate(st):
    x, y_ = r * np.cos(np.radians(a)), r * np.sin(np.radians(a))
    box(ax, x - 1.15, y_ - 0.55, 2.3, 1.1, t, '#E0F2F1', '#00695C', 8)
    a2 = st[(i + 1) % 5][1]; a2 = a2 if a2 < a else a2 - 360
    for aa in np.linspace(a - 22, a2 + 22, 2)[:1]:
        pass
    x1, y1 = (r - 0.2) * np.cos(np.radians(a - 25)), (r - 0.2) * np.sin(np.radians(a - 25)); x2, y2 = (r - 0.2) * np.cos(np.radians(a2 + 25)), (r - 0.2) * np.sin(np.radians(a2 + 25))
    ax.add_patch(FancyArrowPatch((x1, y1), (x2, y2), connectionstyle='arc3,rad=-0.25', arrowstyle='-|>', mutation_scale=14, color='#555', lw=1.3))
ax.add_patch(Circle((0, 0), 1.05, fc='#FFF8E1', ec='#C98A00', lw=1.4))
ax.text(0, 0, 'Weather drivers\ncool nights, high RH,\ndew/fog, leaf wetness,\nrain, cloudy spells\n(Dec–Feb)', ha='center', va='center', fontsize=8.2)
ax.set_title('Disease cycle of white rust in mustard and the weather that drives it (after Saharan et al., 2014)', fontsize=10)
plt.tight_layout(); plt.savefig(FG + 'i_cycle.png', dpi=200); plt.close()

# ---------- 7. stress discrimination decision tree ----------
fig, ax = plt.subplots(figsize=(11.5, 6.6)); ax.set_xlim(0, 11.5); ax.set_ylim(0, 6.6); ax.axis('off')
box(ax, 4.0, 5.75, 3.5, 0.65, 'Stressed mustard pixel / plot\n(red-edge or NDVI anomaly)', '#ECEFF1', '#455A64', 9, True)
box(ax, 0.3, 4.3, 3.3, 0.85, 'Q1 Canopy warmer AND\nwater index / RWC low?', '#E3F2FD', '#1565C0', 8.6)
box(ax, 4.1, 4.3, 3.3, 0.85, 'Q2 Uniform field-wide pattern\nfollowing soil / irrigation?', '#E3F2FD', '#1565C0', 8.6)
box(ax, 7.9, 4.3, 3.3, 0.85, 'Q3 Weather favourable for\nwhite rust in last 7–14 days?', '#E3F2FD', '#1565C0', 8.6)
for x in (1.95, 5.75, 9.55): arr(ax, 5.75, 5.73, x, 5.17)
box(ax, 0.3, 2.85, 3.3, 0.9, 'Yes → drought / water stress\n(check rainfall, irrigation,\nNADAMS-type indices)', '#FFEBEE', '#C62828', 8.3)
box(ax, 4.1, 2.85, 3.3, 0.9, 'Yes → nutrient, salinity,\nwaterlogging or herbicide\n(check soil maps, history)', '#FFEBEE', '#C62828', 8.3)
box(ax, 7.9, 2.85, 3.3, 0.9, 'Yes → biotic suspect:\npatchy foci, spreading\nbetween dates', '#FFF8E1', '#C98A00', 8.3)
for x in (1.95, 5.75, 9.55): arr(ax, x, 4.28, x, 3.77)
box(ax, 5.2, 1.25, 6.0, 1.15, 'Q4 Disease signature?\nred-edge shift + visible ↑ (chlorophyll loss), SWIR ↑ (leaf water loss), disease index,\nwhite pustule texture (RGB), flowers excluded, timing Dec–Feb, lower leaves first', '#E8F5E9', '#2E7D32', 8.3)
arr(ax, 9.55, 2.83, 8.6, 2.42)
box(ax, 0.3, 0.25, 4.5, 1.0, 'Alternaria blight: dark concentric spots, later season;\naphids: honeydew, colonies on tips, Jan–Feb;\ndowny mildew: often with staghead, angular lesions', '#F3E5F5', '#6A1B9A', 8)
box(ax, 5.2, 0.12, 6.0, 0.8, 'Confirm with ground truth (Conn key) → white rust map', '#2E7D32', '#2E7D32', 9, True, 'white')
arr(ax, 8.2, 1.23, 8.2, 0.94); arr(ax, 5.18, 1.6, 4.82, 0.9)
ax.text(4.0, 1.75, 'other biotic\nsignature', fontsize=7.5, color='#6A1B9A', ha='center')
ax.set_title('Decision framework to separate white rust from other biotic and abiotic stresses (proposed)', fontsize=10)
plt.tight_layout(); plt.savefig(FG + 'i_tree.png', dpi=200); plt.close()

# ---------- 8. detectability timeline ----------
fig, ax = plt.subplots(figsize=(11.5, 4.3)); ax.set_xlim(0, 100); ax.set_ylim(0, 5.3); ax.axis('off')
ph = [(0, 18, 'Infection\n(zoospores)', '#E8F5E9'), (18, 38, 'Pre-symptomatic\n(physiology changes)', '#FFF8E1'), (38, 65, 'Pustules visible\n(grades 1–5)', '#FFE0B2'), (65, 100, 'Severe + staghead\n(grades 7–9)', '#FFCDD2')]
for a, b, t, c in ph: ax.add_patch(FancyBboxPatch((a, 4.1), b - a - 0.6, 0.9, boxstyle='round,pad=0.02', fc=c, ec='#999')); ax.text((a + b) / 2, 4.55, t, ha='center', va='center', fontsize=8.5)
rows = [('Thermal (stomatal closure)', 22, 100, '#C62828'), ('Hyperspectral red edge / WRI', 30, 100, '#00695C'), ('SWIR water indices', 50, 100, '#1565C0'), ('Multispectral red edge', 40, 100, '#2E7D32'), ('RGB texture (pustules)', 45, 100, '#6D4C41'), ('Satellite (10–30 m)', 62, 100, '#455A64')]
for i, (t, a, b, c) in enumerate(rows):
    yy = 3.45 - i * 0.58; ax.plot([a, b], [yy, yy], color=c, lw=7, solid_capstyle='butt', alpha=0.85); ax.text(a - 1, yy, t, ha='right', va='center', fontsize=8.3)
ax.text(50, 0.0, 'Expected detection window by sensor (hypothesis to be tested in Objectives 1–3)', ha='center', fontsize=8.5, style='italic')
plt.tight_layout(); plt.savefig(FG + 'i_timeline.png', dpi=200); plt.close()

# copies of existing figures
for src, dst in ((B + '../obj1/fig/o_master.png', 'i_master.png'), (B + '../obj1/fig/o1_tiers.png', 'i_tiers.png')):
    shutil.copy(src, FG + dst)
print('ok')
