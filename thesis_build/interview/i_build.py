"""NRSC/SAC (ISRO) interview guide in question-answer form: builds the docx JS (thesis helpers + reference pool)."""
import re, json, os
B = os.path.dirname(os.path.abspath(__file__)) + '/'; S = B + '../'; LD = S + 'leaf/data/'
r1 = json.load(open(LD + 'res1.json'))['RES']; r2 = json.load(open(LD + 'res2.json')); sw = json.load(open(LD + 'swir_tier2.json'))
bc, br = r2['best']['cls'], r2['best']['reg']; C, R = r2['cls'][bc], r2['reg'][br]
WRI = r1['tier3']['vnir']['formula']; WBA = r1['tier3']['vnir']['best']['ba_cv']
f2 = lambda v: '%.2f' % v
K = []; QN = [0]
def esc(t):
    t = t.replace('\\', '\\\\').replace('`', '\\`').replace('${', '\\${')
    return re.sub(r'\[\[(T|F):(\w+)\]\]', lambda m: '${%s(\'%s\')}' % (m.group(1), m.group(2)), t)
js = lambda s: '`' + esc(s) + '`'
def H1(t): K.append("K.push(H1(%s));" % js(t))
def P(t): K.append("K.push(P(%s));" % js(t))
def BL(items): K.extend("K.push(BL(%s));" % js(i) for i in items)
def NOTE(t): K.append("K.push(NOTE(%s));" % js(t))
def FIG(k, f, cap, w=520): K.append("K.push(...fig2('%s', '%s', %s, %d));" % (k, f, js(cap), w))
def TAB(k, rows, widths, cap, size=15):
    Rr = '[' + ',\n'.join('[' + ', '.join(js(str(c)) for c in r) + ']' for r in rows) + ']'
    K.append("K.push(...tab2('%s', %s, %s, %s, %d));" % (k, Rr, json.dumps(widths), js(cap), size))
def Q(q, short):
    QN[0] += 1
    K.append("K.push(H2(%s));" % js('Q%d. %s' % (QN[0], q)))
    K.append("K.push(BOX('Short answer:', %s, 'E8F5E9', '2E7D32'));" % js(short))
def TIP(t): K.append("K.push(BOX('How to say it in the interview:', %s, 'FFF6E0', 'C98A00'));" % js(t))

# ================= TITLE =================
K.append("K.push(new Paragraph({ alignment: AlignmentType.CENTER, spacing: { before: 800, after: 160 }, children: [new TextRun({ text: 'NRSC / SAC (ISRO) interview guide', font: FONT, size: 44, bold: true, color: '1E3A1F' })] }));")
K.append("K.push(new Paragraph({ alignment: AlignmentType.CENTER, spacing: { after: 120 }, children: [new TextRun({ text: 'AI-based multimodal UAV sensing of white rust in mustard — questions and answers', font: FONT, size: 28, color: '2C5F2D' })] }));")
K.append("K.push(new Paragraph({ alignment: AlignmentType.CENTER, spacing: { after: 400 }, children: [new TextRun({ text: 'Agricultural Scientist interview preparation  |  Ph.D. (Agricultural Physics), ICAR-IARI', font: FONT, size: 20, italics: true, color: '555555' })] }));")
NOTE('**How to use this guide.** Every section is a set of questions the panel is likely to ask, each with a **short answer** (30–60 seconds, say it first) and a **detailed answer** (use it when the panel probes). Numbers marked "leaf data" come from your own ASD analysis (2339 leaves, four dates, 2026); UAV results are still to come, so present them as planned work. Every method is followed by its reference (author et al., year). Keep answers problem-oriented: problem → why it is hard → what I do → evidence → limitation.')
K.append("K.push(new TableOfContents('Contents', { hyperlink: true, headingStyleRange: '1-2' }));")
K.append("K.push(new Paragraph({ children: [new PageBreak()] }));")

# ================= PART A =================
H1('A. Introducing the research')
Q('Please introduce your research in one minute.',
  'I work on **early and accurate detection of white rust in Indian mustard using drone-borne hyperspectral, multispectral, RGB and thermal sensors and machine learning**. White rust is assessed today only by visual scoring, which is slow, subjective and late. I find which wavelengths and indices respond to the disease, build a White Rust Index, classify six severity grades and estimate the percent disease index (PDI), test whether the disease can be predicted before symptoms, and identify bands that can be transferred to satellites. My leaf-level results already show that the red edge (690–860 nm) and SWIR water bands carry the white-rust signal.')
TIP('Start with the crop and the problem, then the gap, then your approach, then one result. Avoid jargon in the first minute; the panel will ask for details.')
Q('Give a three-minute overview of your thesis.',
  'Problem → gap → objectives → method → current evidence → relevance to ISRO, as below.')
P('**Problem.** Rapeseed–mustard is India\'s main rabi oilseed (about 8.6–9.2 million ha and 12.6–13.3 million t in 2023–25 according to Ministry of Agriculture estimates), concentrated in Rajasthan, Haryana, Madhya Pradesh and Uttar Pradesh. White rust (*Albugo candida*) causes leaf pustules and, through systemic infection, staghead of the inflorescence, with large losses in epidemic years (Saharan et al., 2014). Fungicide sprays are calendar-based because there is no objective, spatial monitoring.')
P('**Gap.** Remote sensing of mustard diseases in India has used ground spectroscopy for aphids (Shukla et al., 2024) and Hyperion satellite data for Sclerotinia rot (Bhattacharya and Chattopadhyay, 2013); there is no sensor-based study of white rust, no disease-specific index, no comparison of sensors on the same plots and no pre-symptomatic test.')
P('**Objectives.** (1) Characterise white rust with each UAV sensor; (2) classify six severity grades and estimate PDI with single and fused sensors; (3) predict infection before visible symptoms.')
P('**Method.** A field experiment with 48 plots (12 healthy controls and 36 inoculated plots: three varieties × four inoculation dates × three replications) is flown on 8 dates with four sensors; leaf ASD spectra are measured on the same plots. A tiered analysis (feature extraction → band selection with correlation scalogram and ReliefF → White Rust Index → ANOVA → canonical discriminant analysis → Boruta) feeds machine-learning and deep-learning fusion models, validated by leaving one replication out.')
P('**Evidence so far (leaf data).** Red-edge derivatives at 790–830 nm correlate up to r = 0.78 with plot PDI; a White Rust Index %s separates healthy and diseased leaves with balanced accuracy %s; plot PDI is predicted with R² = %s from four features; SWIR regions 1595–1615 nm, 1495–1515 nm and 1965–1995 nm respond through leaf water loss.' % (WRI, f2(WBA), f2(R['r2'])))
P('**Relevance to ISRO.** The thesis identifies disease-sensitive bands for Sentinel-2-type red-edge, HySIS-type hyperspectral and TRISHNA-type thermal sensors, provides UAV maps as training and validation data for satellite models, and fits the multi-stage satellite approach of SAC (Bhattacharya and Chattopadhyay, 2013).')
FIG('master', 'i_master.png', 'Overall workflow of the thesis.', 460)
Q('What problem are you solving, and why is it important?',
  'I replace slow, subjective, point-based visual scoring of white rust with objective, spatial, early sensor-based assessment, so that sprays can be targeted and losses reduced.')
FIG('problem', 'i_problem.png', 'Problem, research gaps, solution and expected outcome.', 540)
BL(['**Scale of the crop:** mustard covers about 9 million ha in India; even small percentage losses are large in absolute terms.',
    '**Disease biology:** white rust develops in cool, humid weather (December–February); staghead reduces seed set; early-sown and late-sown crops differ in risk; in epidemic years losses are substantial (Saharan et al., 2014).',
    '**Current practice:** visual disease scoring on a 0–9 key (Conn et al., 1990) is labour-intensive, subjective (Bock et al., 2010) and covers only sample plants; it detects the disease after pustules appear.',
    '**What sensors add:** objective numbers, whole-field coverage, repeatability, and possibly earlier detection through thermal and spectral changes before visible symptoms (Mahlein, 2016; Mahlein et al., 2019).'])
Q('What are the research gaps your study addresses?',
  'Six gaps: no sensor-based white-rust study; no white-rust-specific index; no multi-sensor comparison on the same plots; severity treated only as classes; no pre-symptomatic test; no bridge from UAV to satellite for mustard diseases.')
TAB('gaps', [['Gap', 'Evidence from literature', 'How my thesis fills it'],
             ['1. No sensor study of white rust', 'Indian mustard RS work: aphid (Shukla et al., 2024), rot (Bhattacharya and Chattopadhyay, 2013)', 'Leaf + four UAV sensors on white rust'],
             ['2. No disease-specific index', 'General indices respond to many stresses (Mahlein et al., 2013)', 'White Rust Index (WRI) by systematic search'],
             ['3. Sensors not compared on the same plots', 'Most studies use one sensor (Zhang et al., 2012a; Liu et al., 2024)', 'HS, MS, RGB, TIR flown together; cross-sensor tier'],
             ['4. Severity treated only as few classes', 'Adjacent severity classes overlap (Meng et al., 2020; Mandal et al., 2023)', 'Six grades + PDI regression; ±1-grade accuracy'],
             ['5. No pre-symptomatic test for mustard', 'Pre-symptomatic work in other crops (Tian et al., 2021; Mustafa et al., 2023)', 'Objective 3 with retrospective labels'],
             ['6. No UAV-to-satellite bridge', 'Features may not transfer between scales (Bohnenkamp et al., 2019)', 'Bands mapped to Sentinel-2, HySIS, TRISHNA; UAV maps as training data']],
    [2700, 3500, 3106], 'Research gaps and how they are addressed.')
Q('What is the novelty of your study?',
  'First multi-sensor (HS, MS, RGB, thermal) UAV study of white rust in mustard; first White Rust Index (VNIR and SWIR); six-grade + PDI modelling with leakage-free nested validation; pre-symptomatic prediction; and an explicit path to ISRO satellite sensors.')
BL(['**Scientific novelty:** wavelengths and an index specific to white rust; separation of white rust from water stress with thermal + SWIR water indices.',
    '**Methodological novelty:** a tiered, reproducible pipeline (scalogram + ReliefF → WRI → CDA → Boruta → ML-SFFS) in which every selection step is repeated inside the training replications, so the reported accuracy is honest (Varma and Simon, 2006).',
    '**Multi-sensor novelty:** four sensors on the same plots and dates allow a fair test of which sensor and which combination is worth flying.',
    '**Application novelty:** disease-sensitive bands mapped to satellite spectral response functions and UAV maps used as training data for satellite models.'])
TIP('Do not claim "first in the world" unless sure. Say "to my knowledge, the first sensor-based study of white rust in Indian mustard".')
Q('What have you found so far?',
  'From 2339 leaf spectra: the red-edge first derivative near 790–830 nm is the strongest white-rust feature (r up to 0.78 with plot PDI); the WRI %s gives balanced accuracy %s; SWIR water indices respond (|r| up to 0.63); six-grade leaf classification reaches macro-F1 %s (within one grade %s); plot PDI is predicted with R² %s.' % (WRI, f2(WBA), f2(C['macro_f1']), f2(C['adj']), f2(R['r2'])))
FIG('leafscal', 'i_leaf_scal.png', 'Leaf data: correlation scalograms with plot PDI and ReliefF weights for six grades (red points = selected bands).', 520)
TAB('leafres', [['Analysis', 'Result (leaf data)'], ['Robust bands (both scalogram and ReliefF)', ', '.join(r1['tier2']['robust'][:8]) + ' …'],
                ['White Rust Index', '%s; balanced accuracy %s; r with PDI %s' % (WRI, f2(WBA), f2(r1['tier3']['r_pdi']))],
                ['Robust SWIR regions', '1595–1615, 1495–1515, 1965–1995 nm (leaf-water features)'],
                ['Discriminant analysis', 'one severity axis (≈ 89%% of separation), canonical r ≈ %s' % f2(r1['tier5']['step1']['cancor'][0])],
                ['Six-grade classification (%s)' % bc, 'macro-F1 %s, OA %s, ±1 grade %s, healthy vs diseased %s' % (f2(C['macro_f1']), f2(C['oa']), f2(C['adj']), f2(C['detection_acc']))],
                ['PDI regression (%s)' % br, 'R² %s, RMSE %.1f, RPD %s' % (f2(R['r2']), R['rmse'], f2(R['rpd']))]], [3300, 6006], 'Key leaf-level results.')

# ================= PART B =================
H1('B. Methodology')
Q('Give a complete overview of your methodology.',
  'Common inputs (Tier 0) → Objective 1 sensor tiers (features, band selection, WRI, ANOVA, CDA, Boruta) → Objective 2 models and fusion (VIF → ML-SFFS, SVM/RF/k-NN/PLSR/DNN, eight sensor sets) → Objective 3 pre-symptomatic prediction → maps; all validated by leaving one replication out.')
FIG('tiers', 'i_tiers.png', 'Tier structure of Objective 1 for the four sensors.', 470)
TAB('meth', [['Step', 'What is done', 'Why (reference)'],
             ['Ground truth', 'Leaf scores on the 0–9 key; plot grade; PDI = Σ score/(9n) × 100', 'Standard key for crucifer foliar diseases (Conn et al., 1990)'],
             ['Pre-processing', 'Panel/irradiance calibration, orthomosaics, HS crop mask (NDVI > 0.6 and SAM < 0.3), endmember plot spectrum, flowers removed', 'Removes soil, shadow and flower effects (Kruse et al., 1993; Sulik and Long, 2016)'],
             ['Tier 1 features', 'HS bands, derivatives, red edge, 48 indices; MS indices + texture; RGB texture + colour; TIR CT, CTD, NRCT', 'Guo et al. (2021); Feng et al. (2022); Liu et al. (2024)'],
             ['Tier 2 band selection', 'Correlation scalogram (PDI) + ReliefF (grades); one band per correlated region', 'Shukla et al. (2024); Robnik-Šikonja and Kononenko (2003)'],
             ['Tier 3 WRI', 'ND(λ1, λ2) + w·R(λ3) search, cross-validated', 'Mahlein et al. (2013)'],
             ['Tiers 4–6', 'ANOVA + Tukey; VIF + stepwise CDA; Boruta', 'Bhattacharya and Chattopadhyay (2013); Kursa and Rudnicki (2010)'],
             ['Objective 2', 'VIF → ML-SFFS; SVM, RF, k-NN, PLSR, DNN-F1/F2; sensor sets S1–S8', 'Tian et al. (2021); Maimaitijiang et al. (2020)'],
             ['Objective 3', 'Retrospective labels; t-test + Boruta; SVM/RF/k-NN; risk maps', 'Tian et al. (2021); Mustafa et al. (2023)'],
             ['Validation', 'Leave-one-replication-out; selection inside training folds; independent site (Bharatpur)', 'Roberts et al. (2017); Varma and Simon (2006)']], [1800, 4300, 3206], 'Methodology at a glance.', 14)
Q('Describe your experiment and ground truth.',
  '48 plots: 12 healthy controls and 36 inoculated plots (three varieties × four inoculation dates × three replications); leaves scored on the 0–9 key at each flight; plot PDI computed from leaf scores; plot grade from mean % leaf area.')
BL(['Inoculation at four dates creates a range of disease onset and severity, which is needed for regression and for pre-symptomatic labels.',
    'Controls give true healthy references on every date.',
    'Ground truth on the same day as flights avoids temporal mismatch; the same scorer reduces observer bias (Bock et al., 2010).'])
Q('Which sensors do you use and why four sensors?',
  'Hyperspectral (VNIR + SWIR, 481 bands), multispectral (MicaSense RedEdge-MX, 5 bands), RGB (DJI Phantom) and thermal (FLIR Vue Pro R). Each measures a different process: pigments and water (HS), operational broad bands (MS), pustule texture (RGB) and transpiration (TIR).')
TAB('sensors', [['Sensor', 'Measures', 'White-rust signal', 'Satellite analogue'],
                ['Hyperspectral VNIR + SWIR', 'Narrow-band reflectance 400–2500 nm', 'Red edge, pigments, leaf water, WRI', 'HySIS, EnMAP, PRISMA'],
                ['Multispectral (5 bands)', 'Blue, green, red, red edge, NIR', 'Red-edge indices (NDRE, CI_{rededge})', 'Sentinel-2 MSI'],
                ['RGB (high resolution)', 'Colour and texture', 'White pustules, chlorosis, staghead', 'Very-high-resolution optical (Cartosat-3)'],
                ['Thermal (7.5–13.5 µm)', 'Canopy temperature', 'Stomatal closure, transpiration loss', 'Landsat TIRS, ECOSTRESS, TRISHNA (planned)']], [2200, 2400, 2500, 2206], 'Sensors, signals and satellite analogues.')
Q('How do you validate your models and avoid over-optimistic accuracy?',
  'Leave-one-replication-out: train on two replications, test on the third; every selection step (band selection, Boruta, VIF, ML-SFFS, tuning) is repeated inside the training data; final test on an independent site.')
P('Selecting features on all data and then cross-validating inflates accuracy (Ambroise and McLachlan, 2002; Varma and Simon, 2006). Leaving whole replications out also respects spatial structure of the field (Roberts et al., 2017). In the leaf analysis this nested design gave honest accuracies (macro-F1 %s for six grades; R² %s for PDI).' % (f2(C['macro_f1']), f2(R['r2'])))
Q('Why do you use PDI regression in addition to six-grade classification?',
  'Grades are cuts of a continuous severity, so neighbouring grades overlap; PDI keeps the full information. In my leaf data six-grade macro-F1 was %s but plot PDI R² was %s.' % (f2(C['macro_f1']), f2(R['r2'])))
Q('Why do you start from leaf-level ASD data?',
  'Leaf spectra contain the pure disease signal without soil, shadow, flowers or illumination effects; they tell which wavelengths to look for in UAV and satellite data (Mahlein et al., 2012).')

# ================= PART C =================
H1('C. From UAV to satellite: large-scale use')
Q('How can your research be used at satellite scale? Give the detailed methodology.',
  'In five steps: mustard crop mask → weather-based risk (Stage I) → stress screening with red-edge, SWIR and thermal anomalies (Stage II) → disease discrimination with UAV-derived bands and WRI resampled to satellite bands, trained on UAV maps (Stage III) → validation and products. This follows SAC\'s multi-stage logic (Bhattacharya and Chattopadhyay, 2013).')
FIG('scal', 'i_scaling.png', 'Scaling framework: leaf → UAV → satellite.', 520)
FIG('satflow', 'i_satflow.png', 'Proposed satellite-scale methodology for white rust.', 470)
BL(['**Step 1 – crop mask.** Mustard is mapped from Sentinel-1/EOS-04 SAR and Sentinel-2/LISS-IV time series; the yellow-flower signal at flowering separates mustard from wheat (Fang et al., 2016; Sulik and Long, 2016).',
    '**Step 2 – weather risk.** Gridded temperature, relative humidity, rainfall and dew from IMD and MOSDAC drive a white-rust risk model (cool, humid spells; Chattopadhyay et al., 2011). Only pixels in risk windows are examined further.',
    '**Step 3 – stress screening.** Red-edge (Sentinel-2 B5–B7) and SWIR (B11) anomalies relative to a normal crop profile flag stressed pixels, as SAC did for wheat yellow rust with NDVI deviations (Dutta et al., 2014). Thermal plus a water index separates disease from drought (Bhattacharya and Chattopadhyay, 2013).',
    '**Step 4 – discrimination.** The UAV-selected bands and WRI are resampled to each satellite\'s spectral response function; a classifier (RF/SVM) is trained with satellite pixels labelled by UAV-derived PDI (sub-pixel fraction of diseased canopy).',
    '**Step 5 – validation and products.** Ground surveys with the Conn key and UAV transects validate maps (accuracy, R²); outputs are district maps and advisories.'])
Q('Which satellite sensors and bands match your findings?',
  'The red-edge signal maps to Sentinel-2 B5–B7 (705, 740, 783 nm); SWIR water features to Sentinel-2 B11 (1610 nm), LISS-III/AWiFS SWIR (1.55–1.70 µm) and hyperspectral HySIS/EnMAP/PRISMA; the full WRI needs narrow bands (hyperspectral); thermal needs TRISHNA-class data.')
FIG('bands', 'i_bands.png', 'Real leaf spectra of healthy and severely infected leaves with robust white-rust regions and satellite band positions.', 540)
TAB('satmap', [['Feature from my study', 'Sentinel-2 MSI', 'Resourcesat LISS-IV / LISS-III / AWiFS', 'Hyperspectral (HySIS, EnMAP, PRISMA)', 'Thermal'],
               ['Red-edge derivative 690–860 nm', 'B5, B6, B7 (20 m): red-edge slope', 'Not available (no red-edge band)', 'Yes (≈ 10 nm bands, 30 m)', '—'],
               ['WRI ND(750, 948) − 0.5 R696', 'Approximation: B6/B9 with B5', 'No', 'Yes', '—'],
               ['SWIR 1595–1615 nm (water)', 'B11 (1610 nm, 20 m)', 'LISS-III/AWiFS SWIR (1.55–1.70 µm)', 'Yes', '—'],
               ['SWIR 1495–1515, 1965–1995 nm', 'No', 'No', 'Yes (atmospheric absorption nearby)', '—'],
               ['Canopy temperature (CTD)', '—', '—', '—', 'Landsat TIRS (100 m), ECOSTRESS (≈70 m), TRISHNA (≈57 m, planned)']],
    [2300, 1800, 2000, 1800, 1406], 'Mapping of white-rust features to satellite sensors.', 14)
Q('Satellite pixels are much larger than mustard fields. How will you handle mixed pixels?',
  'Use 10–20 m Sentinel-2 or 5.8 m LISS-IV where possible, restrict analysis to the mustard mask, predict a continuous severity (PDI) rather than a class, and train with sub-pixel labels from UAV maps; spectral unmixing separates soil and canopy fractions.')
BL(['Indian mustard fields are often 0.2–2 ha; a 1 ha field holds about 100 Sentinel-2 10 m pixels but only about 11 pixels at 30 m.',
    'UAV maps aggregated to the satellite grid give the fraction of diseased canopy in each pixel: this is the correct label for a mixed pixel.',
    'Endmember-based unmixing removes soil and shadow (Nascimento and Bioucas-Dias, 2005); Bhattacharya and Chattopadhyay (2013) mapped rot inside a 5.8 m LISS-IV crop mask using 30 m Hyperion.',
    'Spatial transferability must be tested: features selected at one scale may not work at another (Bohnenkamp et al., 2019).'])
Q('How can ISRO use your study for large-scale operational monitoring?',
  'As the disease-detection module of a national system: data layer (Resourcesat, Sentinel-2, EOS-04, HySIS-class, TRISHNA, IMD/MOSDAC weather) → model layer (crop mask, weather risk, spectral anomaly, disease classifier trained on UAV sites) → delivery through Krishi-DSS/Bhuvan and state departments.')
FIG('ops', 'i_ops.png', 'Proposed architecture for a national white-rust monitoring service.', 470)
BL(['**Integration with existing systems:** FASAL already combines remote sensing, agrometeorology and statistics for crop forecasts (Parihar and Oza, 2006); Krishi-DSS (launched August 2024 with the Department of Space; uses RISAT-1A and SAC\'s VEDAS) hosts parcel-level crop maps, drought and pest-related layers into which a white-rust layer can fit.',
    '**UAV sentinel sites:** a few calibrated UAV sites per district provide training and validation pixels every season.',
    '**Uses:** targeted spraying advisories, pesticide supply planning, input for crop-insurance (PMFBY) loss assessment, breeding (resistance screening).',
    '**Pilot:** start in the Rajasthan–Haryana mustard belt where the crop is concentrated, then scale.'])
Q('Which current and future ISRO missions are most relevant?',
  'Resourcesat-2/2A (LISS-IV, LISS-III, AWiFS) for crop masks and SWIR; EOS-04/RISAT-1A and NISAR SAR for all-weather crop mapping; HySIS for hyperspectral; TRISHNA (ISRO–CNES, planned) for high-resolution thermal; INSAT-3D/3DR via MOSDAC for weather and land-surface temperature.')
TAB('missions', [['Mission / sensor', 'Key specifications', 'Use in white-rust monitoring'],
                 ['Resourcesat-2/2A LISS-IV', '5.8 m; green, red, NIR', 'Crop mask, field-level stress (no red edge)'],
                 ['LISS-III / AWiFS', '23.5 m / 56 m; green, red, NIR, SWIR', 'Regional stress, SWIR water status'],
                 ['HySIS', '≈ 30 m; VNIR and SWIR hyperspectral', 'WRI and narrow-band disease features'],
                 ['EOS-04 (RISAT-1A), NISAR', 'C-band SAR; L- and S-band SAR', 'Cloud-free crop mapping, canopy structure'],
                 ['TRISHNA (planned, ISRO–CNES)', 'Thermal infrared ≈ 57 m, frequent revisit', 'Canopy temperature stress'],
                 ['INSAT-3D/3DR (MOSDAC)', 'Geostationary LST, humidity, insolation', 'Weather-risk inputs'],
                 ['Sentinel-2 (ESA, free)', '10–20 m; three red-edge bands; SWIR; 5-day revisit', 'Operational red-edge disease screening']], [2600, 3200, 3506], 'Missions relevant to scaling the thesis.', 14)
NOTE('Verify the latest mission status before the interview (launch dates and specifications of planned missions can change).')
Q('Why not go directly to satellite data instead of UAVs?',
  'Because the disease signal must first be understood where pixels are pure and ground truth is exact. UAVs give centimetre pixels, all four sensors at once, flexible timing under cloud-free windows and plot-level ground truth; they then calibrate satellite models.')

# ================= PART D =================
H1('D. Practical problems with drones and satellites')
Q('What are the actual issues with drones for disease detection?',
  'Radiometric (illumination change, calibration, BRDF), geometric (co-registration of four sensors), thermal drift, limited area and battery, regulation, data volume, and confounders such as flowers and shadows.')
TAB('drone', [['Issue', 'Effect', 'My mitigation'],
              ['Changing illumination, clouds', 'Reflectance drifts within a flight', 'Calibration panels + downwelling irradiance sensor; flights 10:30–13:30 under clear sky'],
              ['BRDF / view angle', 'Brightness varies across the image', 'Nadir flights, high overlap, plot centres only'],
              ['Mixed pixels (soil, shadow, flowers)', 'Diluted disease signal', 'NDVI + SAM crop mask; endmember plot spectrum; flowers removed (Sulik and Long, 2016)'],
              ['Thermal camera drift', 'Biased temperatures', 'Warm-up, blackbody/ground targets, CTD and NRCT normalisation'],
              ['Co-registration of four sensors', 'Feature mismatch', 'Ground control points; plot-level features; edge erosion'],
              ['Area, battery, wind', 'Few hectares per flight', 'Use UAV for calibration sites, satellite for coverage'],
              ['Regulation', 'Permissions needed', 'Drone Rules 2021 / Digital Sky registration'],
              ['Data volume, processing', 'Hundreds of GB per season', 'Standardised pipeline, plot-level extraction']], [2500, 2700, 4106], 'Drone issues and mitigation.', 14)
Q('What are the actual issues with satellites for disease detection?',
  'Coarse pixels relative to small fields, revisit and cloud gaps, atmospheric effects, few narrow red-edge/SWIR/thermal bands at high resolution, late detection, confounding stresses and scarce ground truth.')
TAB('sat', [['Issue', 'Why it matters for white rust', 'Possible solution'],
            ['Spatial resolution vs small fields', 'Pustules are millimetres; fields 0.2–2 ha', 'Severity (PDI) per pixel; 10 m Sentinel-2; sub-pixel training from UAV'],
            ['Revisit and clouds', 'Epidemics develop in 1–2 weeks; winter fog', 'Rabi is mostly clear; combine Sentinel-2 + Resourcesat + Landsat; SAR for masks'],
            ['Atmospheric correction', 'Red-edge and SWIR anomalies are small', 'Standard surface-reflectance products; water-vapour bands excluded'],
            ['Spectral resolution', 'WRI needs narrow bands', 'HySIS-class hyperspectral; Sentinel-2 red-edge approximation'],
            ['Thermal resolution', '100 m thermal mixes fields', 'TRISHNA-class thermal; disaggregation with optical data'],
            ['Specificity', 'Many stresses lower NDVI', 'Weather risk + thermal–water check + disease index (Part G)'],
            ['Ground truth', 'Few georeferenced disease records', 'UAV sentinel sites; KVK/ICAR surveys with GPS; mobile apps']], [2500, 2900, 3906], 'Satellite issues and possible solutions.', 14)
Q('Why is disease detection harder than crop mapping or drought monitoring?',
  'Crop mapping uses large phenological differences; drought affects whole regions uniformly. Disease starts in small foci, its spectral effect overlaps with other stresses, it changes within days and needs exact timing and specific features.')
FIG('timeline', 'i_timeline.png', 'Expected detection windows of sensors along the white-rust development (hypothesis).', 540)

# ================= PART E =================
H1('E. Existing work by ISRO, NRSC and SAC')
Q('What work has ISRO (NRSC, SAC) done on crop disease and pest remote sensing?',
  'SAC: mustard rot with Hyperion + LISS-IV and weather (Bhattacharya and Chattopadhyay, 2013); mustard aphid growth from satellite weather data (Dutta et al., 2008); wheat yellow rust forewarning from NDVI deviations (Dutta et al., 2014); mustard aphid detection with ground spectroscopy (Shukla et al., 2024); AVIRIS-NG crop health (Nigam et al., 2019). NRSC: rice bacterial leaf blight with ground hyperspectral + LISS-IV (Das et al., 2015).')
TAB('isro', [['Study (centre)', 'Crop / stress', 'Data', 'Method (technical core)', 'Main result / lesson'],
             ['Bhattacharya and Chattopadhyay (2013) (SAC + DRMR)', 'Mustard Sclerotinia rot', 'Surface weather, MODIS/Landsat-type thermal and water indices, EO-1 Hyperion (30 m), LISS-IV (5.8 m)', 'Stage I weather anomaly; Stage II TVDI–NDWI space; Stage III two-step stepwise canonical discriminant analysis (25 bands; 254 indices); new indices DRI, ROTI with thresholds', 'Multi-stage tracking; ROTI best; indirect validation'],
             ['Dutta et al. (2008) (SAC team)', 'Mustard aphid (Lipaphis erysimi)', 'Satellite (TOVS) air temperature and humidity, sowing dates', 'Growth model driven by cumulative temperature weighted by specific humidity', 'Regional onset, peak and severity of aphid'],
             ['Dutta et al. (2014) (SAC)', 'Wheat yellow rust', 'Multi-date NDVI', 'Normal crop growth profile; inter-annual NDVI deviation flags affected areas', 'Forewarning of yellow-rust areas; low specificity'],
             ['Das et al. (2015) (NRSC)', 'Rice bacterial leaf blight', 'Ground spectroradiometer + LISS-IV', 'Stepwise discriminant analysis: 540, 680, 760, 990 nm; PSRI and PPSRb maps', 'Broad-band LISS-IV can map disease severity'],
             ['Nigam et al. (2019) (SAC)', 'Wheat biotic stress', 'AVIRIS-NG airborne (≈425 bands, 380–2500 nm, ≈5 nm)', 'Absorption band depth at 662–702 and 2155–2175 nm', 'Hyperspectral maps of crop health at field scale'],
             ['Shukla et al. (2024) (NCIPM + SAC)', 'Mustard aphid', 'Ground ASD 400–2500 nm, Bharatpur', 'Correlation of R, FD, SD with grade; PCA and PLSR loadings; key bands 483–487, 509–515, 690–723 nm', 'Hyperspectral detects aphid severity'],
             ['Krishna et al. (2014) (IARI)', 'Wheat yellow rust', 'Field hyperspectral', 'Indices and multivariate models for severity', 'Basis for satellite-scale yellow-rust work']],
    [1900, 1400, 1900, 2400, 1706], 'ISRO and partner studies on crop disease and pest remote sensing.', 13)
Q('Explain the SAC multi-stage method for mustard rot in technical detail.',
  'Three stages: weather anomalies identify favourable periods; the TVDI–NDWI space separates canopy stress without soil-water stress; Hyperion spectra are discriminated with two-step stepwise canonical discriminant analysis and new indices (DRI, ROTI) mapped inside a LISS-IV crop mask.')
BL(['**Stage I (weather):** departures of temperature and humidity from normal during flowering signalled conditions favourable for *Sclerotinia*.',
    '**Stage II (stress):** the temperature–vegetation dryness index (Sandholt et al., 2002) plotted against NDWI: high TVDI with normal water status means canopy stress not caused by drought.',
    '**Stage III (discrimination):** stepwise canonical discriminant analysis (Wilks\' lambda) first on 25 Hyperion bands (canonical correlation > 0.5), then on 30 published and 224 new indices; DWSI-1, DWSI-4, DRI and ROTI retained; ROTI = R1175/(R1982 + R691) recommended; thresholds from observed incidence.',
    '**What I adopt:** the two-step discriminant design (my Tier 5), the indices (DWSI, ROTI in my 48 indices), the disease-vs-drought logic (my thermal–water check) and the multi-stage scaling (my satellite pathway).',
    '**What I improve:** plot-level ground truth with six grades and PDI instead of incidence; leakage-free validation instead of group means; four sensors; UAV resolution.'])
Q('Explain Shukla et al. (2024) and how it relates to your work.',
  'NCIPM and SAC measured mustard canopies with an ASD (400–2500 nm) at Bharatpur, graded aphid infestation, computed correlation of reflectance and first and second derivatives with grade and used PCA and PLSR loadings to select bands (key region 690–723 nm). I adopt their correlation scalogram as the first step of band selection and add ReliefF, one-band-per-region and cross-validated models.')
Q('What other ISRO programmes and platforms are relevant, and what are their technical aspects?',
  'FASAL (multiple in-season crop forecasts from remote sensing, agrometeorology and land observations; Parihar and Oza, 2006), NADAMS (drought assessment from NDVI/NDWI anomalies), CHAMAN (horticulture assessment), Krishi-DSS (2024; parcel-level crop maps, drought and pest layers; uses RISAT-1A and VEDAS), VEDAS and Bhuvan (data visualisation and delivery), MOSDAC (meteorological and oceanographic satellite data, including LST and humidity).')
P('**Technical link to the thesis:** a white-rust layer needs exactly these pieces – a crop mask (FASAL/Krishi-DSS), a weather layer (MOSDAC/IMD), a stress layer (NADAMS-type anomalies) and a disease-specific discriminator, which my thesis provides and validates.')
Q('How will you use the work of Bhattacharya, Shukla and other ISRO studies to make your study better?',
  'By adopting their proven components and filling their gaps: SAC\'s multi-stage design and discriminant analysis, Shukla\'s scalogram band selection on mustard, SAC\'s NDVI-profile forewarning and aphid weather model for the risk layer, NRSC\'s ground-to-LISS-IV upscaling, and AVIRIS-NG band-depth analysis as an extra feature.')
TAB('use', [['Study', 'What I borrow', 'How it improves my thesis'],
            ['Bhattacharya and Chattopadhyay (2013)', 'Two-step CDA; DWSI, ROTI; TVDI–NDWI logic; multi-stage scaling', 'Discrimination of grades; disease-vs-drought check; satellite pathway'],
            ['Shukla et al. (2024)', 'Correlation scalogram of R, FD, SD with grade', 'Objective, crop-specific band selection (Tier 2)'],
            ['Dutta et al. (2008)', 'Weather-driven pest model (temperature × humidity)', 'Template for a white-rust weather-risk layer'],
            ['Dutta et al. (2014)', 'Normal growth profile and NDVI deviation', 'Stage II anomaly screening at satellite scale'],
            ['Das et al. (2015)', 'Ground hyperspectral → LISS-IV upscaling with discriminant bands', 'Template for transferring my bands to Resourcesat'],
            ['Nigam et al. (2019)', 'Absorption band depth (662–702, 2155–2175 nm)', 'Additional SWIR feature; airborne bridge to HySIS']], [2600, 3300, 3406], 'Using ISRO and partner studies to strengthen the thesis.', 14)

# ================= PART F =================
H1('F. Weather and micro-weather of white rust')
Q('Explain the disease cycle of white rust.',
  'Oospores in soil and debris give primary infection; zoospores released in free water infect leaves in cool weather; white pustules form on the lower leaf surface; sporangia spread by wind and rain for secondary cycles; systemic infection of the inflorescence causes staghead, often together with downy mildew (Saharan et al., 2014).')
FIG('cycle', 'i_cycle.png', 'Disease cycle of white rust and its weather drivers.', 460)
Q('Which meteorological parameters influence white rust?',
  'Moderate temperature (cool days and nights), high relative humidity, dew, fog and leaf wetness, rainfall and cloudy spells during December–February; late sowing increases incidence. Indian field studies report severity favoured by morning RH above about 97%, afternoon RH above about 40% and maximum temperature of about 16–24 °C (Chattopadhyay et al., 2011; Saharan et al., 2014).')
TAB('met', [['Parameter', 'Role in the disease', 'Data source for large-scale use'],
            ['Air temperature (Tmax, Tmin)', 'Moderate temperatures favour zoospore release and infection; cold nights with dew', 'IMD gridded data, AWS; MOSDAC; ERA5 reanalysis'],
            ['Relative humidity (morning, afternoon)', 'High RH sustains sporulation and infection', 'IMD AWS; INSAT-3D humidity profiles'],
            ['Rainfall and drizzle', 'Free water for zoospores; rain splash spreads sporangia', 'IMD rain gauges; GPM/IMERG'],
            ['Dew and fog', 'Long leaf wetness at night', 'Derived from Tmin and RH; fog from INSAT imagery'],
            ['Cloudiness and sunshine hours', 'Reduce leaf drying; favour sporulation', 'INSAT insolation products'],
            ['Wind', 'Disperses sporangia between fields', 'IMD AWS; reanalysis'],
            ['Sowing date / crop stage', 'Late sowing and susceptible stages increase incidence', 'Crop calendar from satellite time series']], [2500, 3600, 3206], 'Meteorological parameters influencing white rust.', 14)
NOTE('Reported thresholds differ between locations and years; present them as "reported ranges" and say that your risk model would be calibrated with local data.')
Q('Which micro-meteorological parameters matter, and how would you measure them?',
  'Leaf wetness duration, canopy-air humidity, canopy temperature, dew deposition, radiation inside the canopy and air movement; measured with leaf wetness sensors, canopy temperature/humidity loggers, infrared thermometers and the UAV thermal camera.')
BL(['**Leaf wetness duration** controls zoospore infection: dense canopies, irrigation and dew keep leaves wet longer.',
    '**Canopy microclimate** differs from screen weather: humidity is higher and temperature lower in dense canopies; high nitrogen and close spacing increase both.',
    '**Canopy temperature** (thermal camera) integrates transpiration; diseased plots should be warmer than healthy plots under the same weather (Mahlein et al., 2019).',
    '**Use in the thesis:** CTD (canopy minus air temperature) and the thermal–water check; logging air temperature and humidity at each flight also allows CWSI (Idso et al., 1981; Jackson et al., 1981).'])
Q('How would you build a forecasting or risk model and combine it with remote sensing?',
  'A weather-based risk model (for example logistic regression of epidemic occurrence on humid-cool spell indices, or a degree-hour model of infection) gives "when and where" risk; satellite red-edge/SWIR/thermal anomalies confirm "whether" disease developed; UAV sites calibrate both.')
BL(['Weather-based models for crucifer diseases in India: Chattopadhyay et al. (2011) for white rust; a satellite-weather aphid model (Dutta et al., 2008).',
    'Combination follows Bhattacharya and Chattopadhyay (2013): weather (Stage I) → stress (Stage II) → spectral discrimination (Stage III).',
    'Validation: hindcast past seasons; compare with survey data; report hit rate and false-alarm rate.'])

# ================= PART G =================
H1('G. Separating white rust from other stresses')
Q('How can you differentiate white rust from other stresses?',
  'With five lines of evidence: (1) a disease-specific spectral signature (WRI, red-edge derivatives) instead of NDVI; (2) thermal + water index (warm canopy with normal water = disease, warm + dry = drought); (3) texture (white pustules in RGB); (4) spatial–temporal pattern (patchy foci spreading after cool, humid spells); (5) weather consistency and ground truth.')
FIG('tree', 'i_tree.png', 'Decision framework to separate white rust from other biotic and abiotic stresses.', 540)
Q('How is white rust different from other biotic stresses of mustard?',
  'White rust gives raised white pustules on the lower leaf surface and staghead; Alternaria blight gives dark concentric necrotic spots; downy mildew gives angular yellow lesions with grey growth and often co-occurs with staghead; Sclerotinia causes stem rot and wilting; aphids cluster on inflorescences with honeydew and sooty mould.')
TAB('biotic', [['Stress', 'Visible symptom', 'Expected spectral/thermal signal', 'Discriminating evidence'],
               ['White rust', 'White pustules (lower leaf), staghead', 'Visible ↑, NIR ↓, red edge shift, SWIR ↑ (water loss); WRI ↓', 'White texture; Dec–Feb; cool humid weather'],
               ['Alternaria blight', 'Dark brown concentric spots, later season', 'Visible ↑, strong necrosis (brown pigments), NIR ↓', 'Dark lesion texture; warmer, later period'],
               ['Downy mildew', 'Angular yellow lesions, grey growth', 'Chlorosis (visible ↑), red edge shift', 'Lesion shape; often with white rust on staghead'],
               ['Sclerotinia rot', 'Stem lesions, wilting, lodging', 'Strong water stress signal, canopy temperature ↑', 'Patches with lodging; flowering–pod stage (Bhattacharya and Chattopadhyay, 2013)'],
               ['Aphids', 'Colonies on tips, honeydew, curling', 'Changes at 483–515 and 690–723 nm (Shukla et al., 2024)', 'Inflorescence-focused; Jan–Feb; warm dry spells'],
               ['Powdery mildew', 'White powdery coating, upper surface', 'Visible and NIR ↑ (white coating)', 'Upper-surface coating, late dry season']], [1500, 2400, 2900, 2506], 'White rust versus other biotic stresses (symptoms after Saharan et al., 2014).', 13)
Q('How is white rust different from abiotic stresses?',
  'Drought: warm canopy with low water index across the field; nitrogen deficiency: uniform chlorosis of older leaves, no pustules, no temperature rise; frost: sudden damage after cold nights, field-wide; waterlogging/salinity: soil-related patterns; senescence and flowering: phenological, all plots together. White rust is patchy, progressive and linked to humid weather.')
TAB('abiotic', [['Abiotic stress', 'Spatial / temporal pattern', 'Spectral and thermal signal', 'How I separate it'],
                ['Drought / water stress', 'Field-wide, follows irrigation and soil', 'Canopy temperature ↑, water index ↓, SWIR ↑', 'Uniform irrigation; thermal–water check; RWC'],
                ['Nitrogen deficiency', 'Uniform, older leaves first', 'Chlorophyll indices ↓; no thermal rise', 'No pustules; soil/fertiliser records'],
                ['Frost / cold injury', 'Sudden, after a cold night', 'Abrupt NIR drop, necrosis', 'Date of event; temperature records'],
                ['Waterlogging, salinity', 'Low-lying or saline patches', 'Chlorosis, stunting', 'Soil maps, elevation'],
                ['Flowering', 'All plots at the same stage', 'Yellow: 500–650 nm ↑', 'Flower pixels removed; flower fraction as covariate (Sulik and Long, 2016)'],
                ['Senescence', 'Late season, all plots', 'Red edge shift, PSRI ↑', 'Compare with controls of the same date']], [2100, 2400, 2500, 2306], 'White rust versus abiotic stresses.', 13)

# ================= PART H =================
H1('H. Other remote-sensing approaches for disease detection and forecasting')
Q('What other methods are used for disease detection with remote sensing, and what are their drawbacks?',
  'Vegetation-index thresholds and anomalies, spectral disease indices, band-depth analysis, machine learning on hyperspectral data, deep learning on images, sun-induced fluorescence, thermal indices, radiative-transfer inversion, time-series anomalies, SAR, and weather-based or hybrid forecasting. Each has strengths; the common drawback is low specificity or poor transferability.')
TAB('other', [['Approach', 'Examples (references)', 'Strengths', 'Drawbacks'],
              ['VI thresholds / NDVI anomaly', 'Yellow-rust forewarning (Dutta et al., 2014)', 'Simple, satellite-ready', 'Not disease-specific; late'],
              ['Spectral disease indices', 'Mahlein et al. (2013); Ashourloo et al. (2014); Zheng et al. (2018)', 'Specific, transferable to multispectral', 'Developed for one disease/crop; need recalibration'],
              ['Band depth / continuum removal', 'Nigam et al. (2019); Kokaly and Clark (1999)', 'Physically based absorption features', 'Needs narrow bands; sensitive to noise'],
              ['Machine learning on hyperspectral data', 'SVM (Rumpf et al., 2010); RF, k-NN (Mustafa et al., 2023)', 'Uses many features; good accuracy', 'Over-fitting, needs ground truth, transferability'],
              ['Deep learning on images', 'CNN on leaf images (Mohanty et al., 2016); UAV fusion (Maimaitijiang et al., 2020)', 'Learns features automatically', 'Large labelled data; black box; lab-to-field gap'],
              ['Sun-induced fluorescence (SIF)', 'Mohammed et al. (2019); pre-visual stress (Zarco-Tejada et al., 2018)', 'Direct photosynthesis signal; early', 'Weak signal; special sensors; coarse satellites'],
              ['Thermal indices (CTD, CWSI)', 'Calderón et al. (2013); Mahlein et al. (2019)', 'Early transpiration changes', 'Not specific (drought); weather dependent'],
              ['Radiative-transfer inversion', 'PROSAIL (Jacquemoud et al., 2009)', 'Retrieves chlorophyll, water, LAI', 'Ill-posed; calibration effort'],
              ['Time-series anomalies', 'Sentinel-2 profiles; normal-profile deviation', 'Uses phenology; operational', 'Confounded by sowing date and management'],
              ['SAR', 'Canopy structure, moisture (EOS-04, NISAR)', 'All-weather', 'Weak sensitivity to leaf disease'],
              ['Weather-based forecasting', 'Chattopadhyay et al. (2011); Dutta et al. (2008)', 'Predicts before infection', 'Location-specific; no spatial detail of actual disease'],
              ['Hybrid weather + RS', 'Bhattacharya and Chattopadhyay (2013)', 'Combines when, where and whether', 'Needs good weather and ground data']], [2100, 2800, 2100, 2306], 'Remote-sensing approaches for crop disease detection and forecasting.', 13)
Q('Why did you choose your approach over a deep CNN or a single index?',
  'A single index is simple but not specific; a CNN needs thousands of labelled images and is hard to interpret. My tiered approach finds interpretable, physically meaningful features first, then uses compact ML models and tests small DNN fusion against them, which suits a field experiment with a few hundred plot-dates.')

# ================= PART I =================
H1('I. Expected technical questions')
QA = [
 ('What causes the red-edge shift in diseased plants?', 'Loss of chlorophyll narrows the red absorption feature, so the steep rise between red and NIR moves to shorter wavelengths and becomes less steep; tissue damage lowers NIR reflectance (Horler et al., 1983; Filella and Peñuelas, 1994). In my leaf data the first-derivative peak fell and shifted with grade.'),
 ('Why do diseased leaves reflect more in the SWIR?', 'SWIR reflectance is controlled by leaf water absorption (1450, 1940 nm and the 1600–2200 nm continuum); infection reduces leaf water, so reflectance rises (Carter and Knapp, 2001; Apan et al., 2004).'),
 ('Why use derivative spectra?', 'Derivatives remove additive offsets (illumination, background) and sharpen inflection points such as the red edge (Tsai and Philpot, 1998). In my data, red-edge first derivatives were the strongest features.'),
 ('Neighbouring hyperspectral bands are highly correlated. How do you handle it?', 'Leaf reflectance bands 5 nm apart have median r = 0.9998; I keep one band per correlated region (r ≥ 0.95), remove collinearity with VIF < 10 and select compact subsets with ML-SFFS (Tian et al., 2021; Dormann et al., 2013).'),
 ('What is the Hughes phenomenon?', 'With a fixed number of samples, accuracy first rises then falls as features are added because parameters cannot be estimated reliably (Hughes, 1968); band selection prevents it.'),
 ('How do you correct UAV hyperspectral data?', 'Dark current and radiometric calibration, reflectance from calibration panels and an irradiance sensor, geometric correction with GPS/IMU and ground control points, and removal of noisy and water-vapour bands.'),
 ('What is ReliefF and why use it?', 'A filter method that weights features by how well they separate nearest neighbours of different classes; it handles multi-class, noisy, overlapping data (Robnik-Šikonja and Kononenko, 2003). I exclude neighbours from the same plot to avoid pseudo-replication.'),
 ('What does canonical discriminant analysis tell you?', 'It finds linear combinations of features that maximise between-grade versus within-grade variance (Fisher, 1936); canonical correlations and Wilks\' lambda measure separability. In my leaf data one function carried about 89% of the separation.'),
 ('Why Boruta after ANOVA and CDA?', 'ANOVA is univariate and CDA keeps a minimal linear set; Boruta selects all relevant features with non-linear random-forest importance against shuffled shadow features (Kursa and Rudnicki, 2010).'),
 ('What is ML-SFFS?', 'Sequential floating forward selection with a model\'s cross-validated score as the criterion; the floating step removes earlier features that became redundant (Pudil et al., 1994).'),
 ('Why macro-F1 and kappa, not only overall accuracy?', 'Grades have unequal sizes; macro-F1 weights each grade equally and kappa corrects for chance agreement (Cohen, 1960; Sokolova and Lapalme, 2009).'),
 ('What is RPD?', 'Ratio of the standard deviation of observations to RMSE; values near or above 2 indicate useful quantitative models (Chang et al., 2001). My leaf PDI model gave RPD %s.' % f2(R['rpd'])),
 ('How do you handle flowers in mustard images?', 'Yellow petals dominate 500–650 nm and change with phenology; flower pixels are removed from the leaf spectrum and the flower fraction is kept as a covariate (Sulik and Long, 2016; Fang et al., 2016).'),
 ('How do you make thermal data comparable between flights?', 'Radiometric calibration with emissivity, air temperature, humidity and distance; canopy-air temperature difference (CTD) and normalised relative canopy temperature (NRCT) reduce weather effects (Feng et al., 2022).'),
 ('What is the difference between TVDI and CWSI?', 'TVDI scales surface temperature between dry and wet edges of the temperature–vegetation-index space of one scene and reflects surface moisture (Sandholt et al., 2002); CWSI scales canopy temperature between weather-based or reference limits and reflects the crop transpiration deficit (Idso et al., 1981; Jackson et al., 1981). CWSI suits UAV canopy pixels.'),
 ('Can SAR detect white rust?', 'SAR responds to canopy structure and moisture, not to leaf pigments; it can map mustard and detect severe structural damage (staghead, lodging) but not early pustules. It is useful for the crop mask under cloud.'),
 ('How does SIF relate to disease?', 'Sun-induced fluorescence tracks photosynthetic activity and can change before visible symptoms (Zarco-Tejada et al., 2018; Mohammed et al., 2019); it needs very high spectral resolution, so it is a future option, not part of my UAV set.'),
 ('What if fusion does not improve accuracy?', 'That is a valid result: the cheaper sensor is then sufficient (Mahlein et al., 2019). For ISRO it would mean a red-edge multispectral sensor is enough for operational monitoring.'),
 ('How large an area can your approach cover?', 'UAV: a few hectares per flight for calibration and validation; satellites: national coverage; the thesis links the two.'),
 ('What are the limitations of your study?', 'One season and site so far; leaf results are an upper bound for canopy; six-grade separation is limited by overlap; thermal is weather dependent; satellite transfer still has to be demonstrated.'),
 ('If you join ISRO, what would you do first with this work?', 'Test the red-edge and SWIR white-rust features on Sentinel-2 and HySIS scenes over the Rajasthan–Haryana mustard belt using UAV sites for validation, and prototype a white-rust layer combining weather risk and spectral anomalies.'),
]
for q, a in QA:
    QN[0] += 1
    K.append("K.push(H2(%s));" % js('Q%d. %s' % (QN[0], q)))
    P(a)

exec(open(B + 'i_extra.py').read())
H1('J. Closing statement')
Q('Summarise the contribution of your thesis in one sentence.',
  'My thesis identifies the spectral and thermal signature of white rust in mustard, turns it into a disease-specific index and validated severity models from UAV sensors, and provides the bands and training data needed to monitor the disease at satellite scale.')

# ================= assemble =================
T = open(S + 'thesis/t_docx.js').read()
head = T[:T.index('// ======================= TITLE')]
head = re.sub(r"const B = '.*?';", "const B = '%s';" % B, head)
head = re.sub(r"const OUT = '.*?';", "const OUT = '%s';" % (S + 'outputs/ISRO_interview_guide_white_rust.docx'), head)
head = re.sub(r"const FORDER = \[.*?\];", "const FORDER = __FORDER__;", head)
head = re.sub(r"const TORDER = \[.*?\];", "const TORDER = __TORDER__;", head)
head = head.replace('children: [new Paragraph({ children: runs(String(c)', 'children: [new Paragraph({ keepNext: true, children: runs(String(c)')
body = '\n'.join(K)
i = T.index("K.push(H1('References'))"); pool = [r.replace("\\'", "'") for r in re.findall(r"^  '(.*)',$", T[i:], re.M)]
pool += re.findall(r'^ "(.*)",$', open(S + 'obj1/o1_assemble.py').read(), re.M)
pool += re.findall(r'^         "(.*)",$', open(S + 'leaf/l7_assemble.py').read(), re.M)
pool += ["Dutta, S., Bhattacharya, B.K., Dadhwal, V.K., et al. (2008). Modelling regional level spatial distribution of aphid (Lipaphis erysimi) growth in Indian mustard using satellite-based remote sensing data. International Journal of Pest Management 54(1), 51–62.",
         "Dutta, S., et al. (2014). A case study on forewarning of yellow rust affected areas on wheat crop using satellite data. Journal of the Indian Society of Remote Sensing 42(2), 335–342.",
         "Das, P.K., Laxman, B., Kameswara Rao, S.V.C., Seshasai, M.V.R., Dadhwal, V.K. (2015). Monitoring of bacterial leaf blight in rice using ground-based hyperspectral and LISS IV satellite data in Kurnool, Andhra Pradesh, India. International Journal of Pest Management 61(4), 359–368.",
         "Nigam, R., et al. (2019). Crop type discrimination and health assessment using hyperspectral imaging. Current Science 116(7), 1108.",
         "Chattopadhyay, C., et al. (2011). Epidemiology and development of forecasting models for white rust of Brassica juncea in India. Archives of Phytopathology and Plant Protection 44(8), 751–763.",
         "Parihar, J.S., Oza, M.P. (2006). FASAL: an integrated approach for crop assessment and production forecasting. Proceedings of SPIE 6411, Agriculture and Hydrology Applications of Remote Sensing, 641101.",
         "Sandholt, I., Rasmussen, K., Andersen, J. (2002). A simple interpretation of the surface temperature/vegetation index space for assessment of surface moisture status. Remote Sensing of Environment 79(2–3), 213–224.",
         "Idso, S.B., Jackson, R.D., Pinter, P.J., Reginato, R.J., Hatfield, J.L. (1981). Normalizing the stress-degree-day parameter for environmental variability. Agricultural Meteorology 24, 45–55.",
         "Jackson, R.D., Idso, S.B., Reginato, R.J., Pinter, P.J. (1981). Canopy temperature as a crop water stress indicator. Water Resources Research 17(4), 1133–1138.",
         "Calderón, R., Navas-Cortés, J.A., Lucena, C., Zarco-Tejada, P.J. (2013). High-resolution airborne hyperspectral and thermal imagery for early detection of Verticillium wilt of olive using fluorescence, temperature and narrow-band spectral indices. Remote Sensing of Environment 139, 231–245.",
         "Mohanty, S.P., Hughes, D.P., Salathé, M. (2016). Using deep learning for image-based plant disease detection. Frontiers in Plant Science 7, 1419.",
         "Mohammed, G.H., et al. (2019). Remote sensing of solar-induced chlorophyll fluorescence (SIF) in vegetation: 50 years of progress. Remote Sensing of Environment 231, 111177.",
         "Zarco-Tejada, P.J., Camino, C., Beck, P.S.A., et al. (2018). Previsual symptoms of Xylella fastidiosa infection revealed in spectral plant-trait alterations. Nature Plants 4, 432–439.",
         "Hueni, A., Bialek, A. (2017). Cause, effect, and correction of field spectroradiometer interchannel radiometric steps. IEEE Journal of Selected Topics in Applied Earth Observations and Remote Sensing 10(4), 1542–1551.",
         "Jones, H.G. (1999). Use of infrared thermometry for estimation of stomatal conductance as a possible aid to irrigation scheduling. Agricultural and Forest Meteorology 95(3), 139–149.",
         "Zheng, Q., Huang, W., Cui, X., Shi, Y., Liu, L. (2018). New spectral index for detecting wheat yellow rust using Sentinel-2 multispectral imagery. Sensors 18(3), 868."]
pat = re.compile(r"([A-Z][A-Za-zÀ-ÿŠš\-]+)(?: et al\.| and [A-Z][A-Za-zÀ-ÿ\-]+)?,? \(?(\d{4})[a-z]?")
cites = set((m.group(1), m.group(2)) for m in pat.finditer(body))
def rk(r):
    a = r.split(',')[0].strip(); y = re.search(r'\((\d{4})[a-z]?\)', r); return (a, y.group(1) if y else '')
used, seen = [], set()
for r in sorted(pool, key=lambda r: (r.split('(')[0].lower(), r)):
    key = (r.split('(')[0], rk(r)[1])
    if rk(r) in cites and key not in seen and rk(r) not in {rk(u) for u in used if u.split(',')[0] == r.split(',')[0] and rk(u)[1] == rk(r)[1] and 'et al' in u}: seen.add(key); used.append(r)
have = set(rk(r) for r in used)
fp = {('Šikonja', '2003'), ('Kononenko', '2003'), ('Chattopadhyay', '2013'), ('Rudnicki', '2010'), ('Philpot', '1998'), ('Peñuelas', '1994'), ('McLachlan', '2002'), ('Simon', '2006'), ('Knapp', '2001'), ('Oza', '2006'), ('Clark', '1999'), ('Long', '2016'), ('Lapalme', '2009'), ('Dias', '2005'), ('Rapeseed', '2023')}
missing = sorted(x for x in cites if x not in have and 1900 < int(x[1]) < 2027 and x not in fp and x[0] not in {'Ministry', 'ICAR-IARI', 'Rules', 'August'})
print('missing refs:', missing)
q = lambda s: "'" + s.replace("\\", "\\\\").replace("'", "\\'") + "'"
body += "\nK.push(H1('References'));\nconst refPara = r => new Paragraph({ spacing: { after: 70, line: 255 }, indent: { left: 400, hanging: 400 }, children: [new TextRun({ text: r, font: FONT, size: 18 })] });\n[\n" + '\n'.join('  ' + q(r) + ',' for r in used) + "\n].forEach(r => K.push(refPara(r)));\n"
FO = [m.group(2) for m in re.finditer(r"\b(fig2|FIG)\('([A-Za-z0-9]+)'", body)]
TO = [m.group(2) for m in re.finditer(r"\b(tab2|TAB)\('([A-Za-z0-9]+)'", body)]
assert len(FO) == len(set(FO)) and len(TO) == len(set(TO))
head = head.replace('__FORDER__', repr(FO)).replace('__TORDER__', repr(TO))
tail = T[T.index('\nconst numcfg'):]
tail = tail.replace("title: 'AI-based multimodal UAV sensing of white rust in mustard: complete methodology'", "title: 'NRSC/SAC interview guide: white rust in mustard'")
tail = re.sub(r"'eqs', \d+, 'refs', \d+", "'eqs', 0, 'refs', %d" % len(used), tail)
open(B + 'i_build.js', 'w').write(head + '\n' + body + '\n' + tail)
print('questions', QN[0], 'figs', len(FO), 'tabs', len(TO), 'refs', len(used))
