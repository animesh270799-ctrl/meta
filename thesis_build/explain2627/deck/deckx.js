// Detailed deck: the 2026-27 white rust data analysis explained step by step (Times New Roman, 14 pt).
const { pres, F, FS, C, THEME, S, sec, T, BL, box, arr, line, chain, tb, circ, refline } = require('../../meth2627/deck/adv_lib.js');
const fs = require('fs');
const SZ = require('./figsizes.json'); const FIG = __dirname + '/../fig/';
function img(s, n, x, y, w, hmax) { const [pw, ph] = SZ[n]; let h = w * ph / pw; if (hmax && h > hmax) { h = hmax; w = h * pw / ph; } s.addImage({ path: FIG + n, x, y, w, h }); return [w, h]; }
function key(s, text, x, y, w, h) { box(s, x, y, w, h, 'In short', text, C.g, C.lt, { align: 'left', valign: 'top' }); }
function ex(s, text, x, y, w, h) { box(s, x, y, w, h, 'Worked example', text, C.blue, C.lblue, { align: 'left', valign: 'top' }); }
function pos(s, after, feeds, data, y = 1.15) { tb(s, [['Comes after', 'Feeds into', 'Samples used'], [after, feeds, data]], 0.45, y, 12.43, [3.6, 3.6, 5.23]); }
let s;

// ================================================================ Introduction
sec('Introduction');
s = pres.addSlide({ masterName: 'TITLE', sectionTitle: 'Introduction' });
s.addText('The 2026-27 White Rust Data Analysis, Step by Step', { placeholder: 'title' });
s.addText([{ text: 'From raw UAV images and ASD leaf spectra to final results: order of the steps, data split, data used in each step, settings and references', options: { breakLine: true, bold: true } }, { text: ' ', options: { breakLine: true } },
  { text: 'Animesh Panda (Roll No. 13098)', options: { breakLine: true } }, { text: 'Ph.D. (Agricultural Physics), ICAR-Indian Agricultural Research Institute, New Delhi', options: { breakLine: true } },
  { text: ' ', options: { breakLine: true } }, { text: 'Demo numbers only – no results', options: { italic: true } }], { placeholder: 'body' });

s = S('What this presentation explains', 'Introduction');
BL(s, ['**The order** of every analysis step, from raw images to the final test – what comes first, what next, and why.',
  '**The data used in each step:** all 48 plots, the 33 training plots, their inner parts, or the 15 test plots.',
  '**How each step is calculated**, with formulas, settings and small worked examples.',
  '**Which paper each step follows** (disease studies and original method papers).',
  '**How to repeat the analysis** on a new data set.'], 0.45, 1.2, 6.3, 4.4);
tb(s, [['Objective', 'Question'], ['1 Characterisation', 'Which features of each camera carry the white rust signal?'], ['2 Detection and severity', 'Which camera or combination and model works best on new plots?'], ['3 Pre-symptomatic', 'Can later-infected subplots be found 2–8 days after inoculation?']], 6.95, 1.2, 5.93, [2.1, 3.83]);
tb(s, [['Task', 'Target', 'Main metric'], ['A', 'healthy (DI = 0) vs diseased', 'macro-F1'], ['B', 'DI class 0, 1, 3, 5, 7, 9', 'macro-F1'], ['C', 'DI (%)', 'R²']], 6.95, 3.95, 5.93, [0.9, 3.33, 1.7]);
refline(s, 'three tasks of every model: Tian et al. (2021), Chen et al. (2023), Mandal et al. (2023); design and network of the core study: Ma et al. (2026).', 6.2, 0.45);

s = S('The order of the whole analysis: 14 stages', 'Introduction');
img(s, 'x01_stage_order.png', 0.45, 1.1, 6.0, 5.85);
BL(s, ['**Stages 1–5 (done once):** image processing → features → labels → plot-wise split → normalisation and leakage rules.',
  '**Stages 6–7 (Objective 1):** describe the response on all plots; select the features of each camera on the training plots → DSF of each camera.',
  '**Stages 8–12 (Objective 2):** 15 sensor sets → machine learning → networks → test once → comparison, covariate baseline, maps.',
  '**Stage 13 (Objective 3):** the same chain for the pre-symptomatic dates.',
  '**Stage 14 (Part L):** the same chain for the ASD leaves.',
  '**Rule:** each stage uses the output of the stage before it.'], 5.3, 1.2, 7.58, 5.6);

s = S('The 14 stages in order (1/2)', 'Introduction');
tb(s, [['Stage', 'Steps', 'What happens', 'Samples used'],
  ['1', 'B1–B6', 'calibration, mosaics, HS cleaning and smoothing, co-registration, ROI means', 'all 48 plots'],
  ['2', 'C1–C6', 'features of each camera; one table per camera', 'all 48 plots'],
  ['3', 'A3, A5, A6', 'DI, DI class, labels and covariates joined to every row', 'all 48 plots'],
  ['4', 'D1, D2', '33 training / 15 test plots; GroupKFold(3); 11 network validation plots', 'defines the sets'],
  ['5', 'D3–D5', 'thermal normalisation; scaling rules; leakage rules', 'constants from training plots'],
  ['6', '1.1, 1.7', 'response curves, correlation with DI, strata, physiology', 'all 48 plots'],
  ['7', '1.2–1.6', 'feature selection inside each camera; VIF → DSF of each camera and task', '33 training plots']], 0.45, 1.2, 12.43, [0.9, 1.4, 7.4, 2.73], { firstCol: true });
s = S('The 14 stages in order (2/2)', 'Introduction');
tb(s, [['Stage', 'Steps', 'What happens', 'Samples used'],
  ['8', '2.1–2.2', 'DSFs joined for 15 sensor sets; VIF again', '33 training plots'],
  ['9', '2.3–2.4', 'SFFS → grid search → refit of SVM/SVR, RF, k-NN, PLS-DA/PLSR', 'GroupKFold(3) in training plots'],
  ['10', '2.5–2.6', 'DNN-F1, DNN-F2, DT-EDNet and comparison networks', '22 fitting + 11 validation plots'],
  ['11', '2.7', 'every frozen model predicts the test plots once; metrics', '15 test plots'],
  ['12', '2.8–2.11', 'ranking, fusion gain, ablation, SHAP, covariate baseline, strata, maps, Bharatpur', 'test plots (+ Bharatpur)'],
  ['13', '1.8, 3.1–3.6', 'pre-symptomatic labels, normalisation, selection, models, test, earliest day', 'same split'],
  ['14', 'L1–L10', 'ASD leaf table, smoothing, indices, description, selection, models, test, leaf–canopy link', 'same split (by plot)']], 0.45, 1.2, 12.43, [0.9, 1.6, 7.0, 2.93], { firstCol: true });

s = S('The unit of analysis and the journey of one sample', 'Introduction');
BL(s, ['**UAV data – subplot level:** one sample = one subplot on one date; the mean of all ROI pixels of every band of every camera; label = DI of that subplot and date. 48 plots × 4 subplots = 192 samples per date and camera.',
  '**ASD data – leaf level:** one sample = one leaf on one date; label = that leaf\'s grade.'], 0.45, 1.2, 12.43, 1.7);
img(s, 'x07_sample_journey.png', 0.9, 2.95, 11.5, 3.3);
refline(s, 'ROI-mean samples: Ma et al. (2026), Liu et al. (2024); graded leaves with their own spectra: Chen et al. (2023), Tian et al. (2021).', 6.4, 0.4);

s = S('Four rules that hold in every stage', 'Introduction');
[['1', 'Whole plots stay together', 'all subplots of a plot on all dates, and all its leaves, are either training or test data – a model must not recognise the plot instead of the disease'],
 ['2', 'Learn only from training plots', 'selected features, scaling constants, healthy references, settings and weights come from the 33 training plots'],
 ['3', 'Test plots used once', 'the 15 test plots are fixed before the first flight and predicted only after every model is frozen'],
 ['4', 'Same rules for every camera', 'every camera, sensor set and model uses the same split, folds and validation plots']].forEach((r, i) => {
  const y = 1.25 + i * 1.18; circ(s, 0.55, y + 0.12, 0.7, r[0]); box(s, 1.45, y, 11.4, 0.98, r[1], r[2], C.g, C.lt, { align: 'left' });
});
refline(s, 'grouped division of structured data: Roberts et al. (2017); selection bias when selecting on all data: Ambroise and McLachlan (2002); test once: Ma et al. (2026), Bijlwan et al. (2025).', 6.15, 0.5);

// ================================================================ Data
sec('Data');
s = S('Field design: 48 plots, 12 treatments, healthy block', 'Data');
img(s, 'g02_layout.png', 0.45, 1.15, 6.6, 4.9);
BL(s, ['**4 sowing dates** (19, 26 Nov; 3, 10 Dec 2026) × **3 varieties** (PM 26, Pusa Vijay, PM 37) = 12 treatments.',
  '**36 inoculated plots** (R1–R3) on 30 Dec 2026, ~~Albugo candida~~ 1.5 × 10⁵ zoosporangia mL⁻¹; crop age 41, 34, 27, 20 days.'.replace(/~~/g, ''),
  '**12 healthy plots** in a separate block (one per treatment).',
  '**Each plot** 5 m × 3 m, divided into **4 subplots** of 2.5 m × 1.5 m → 192 subplots.'], 7.3, 1.2, 5.58, 4.9);
refline(s, 'staggered sowing for white rust: Chattopadhyay et al. (2011); inoculated + healthy plots for UAV: Guo et al. (2021), Liu et al. (2024); inoculum: Mishra et al. (2009).', 6.25, 0.45);

s = S('Dates: 3 pre-symptomatic and 10 post-symptomatic flights', 'Data');
tb(s, [['Date', '1 Jan', '4 Jan', '7 Jan', '11 Jan', '18 Jan', '25 Jan', '1 Feb', '8 Feb', '15 Feb', '22 Feb', '1 Mar', '8 Mar', '15 Mar'],
  ['DAI', '2', '5', '8', '12', '19', '26', '33', '40', '47', '54', '61', '68', '75'], ['Stage', 'pre', 'pre', 'pre', 'post', 'post', 'post', 'post', 'post', 'post', 'post', 'post', 'post', 'post'],
  ['Physiology', '', '', '✓', '', '✓', '', '', '✓', '', '', '✓', '', '']], 0.45, 1.2, 12.43, [1.3, ...Array(13).fill(0.856)], { firstCol: true });
img(s, 'g04_timeline.png', 2.2, 3.0, 8.9, 3.2);
BL(s, ['On every flight day: four cameras, leaf scoring of 5 plants per subplot, ASD spectra of the centre plant.'], 0.45, 6.35, 12.43, 0.45);

s = S('What is measured on every date', 'Data');
tb(s, [['Measurement', 'Instrument and setting', 'Unit'],
  ['Hyperspectral', 'Headwall VNIR–SWIR, 400–2500 nm, 483 usable bands, about 2.2 cm', 'whole field'],
  ['Multispectral', 'MicaSense RedEdge-MX: 475, 560, 668, 717, 840 nm, about 2 cm', 'whole field'],
  ['RGB', 'DJI camera, about 0.8 cm', 'whole field'],
  ['Thermal', 'FLIR Vue Pro R, 7.5–13.5 µm, about 3.9 cm; air temperature and RH', 'whole field'],
  ['Leaf grades', 'L3, L5, lowest green leaf of 5 tagged plants (centre + 4 corners), 0–9', '15 leaves per subplot'],
  ['ASD spectra', 'leaf clip, own lamp; L3, L5, LL of the centre plant; 2 readings; 350–2500 nm', '3 leaves per subplot'],
  ['Physiology (4 dates)', 'pigments, anthocyanin, protein, RWC, MSI, gas exchange (LI-6400)', '1 subplot per plot'],
  ['Weather', 'IARI observatory: Tmax, Tmin, RH I, RH II, rainfall', 'daily']], 0.45, 1.2, 12.43, [2.4, 7.4, 2.63], { firstCol: true });

s = S('From leaf grades to the disease index (DI) of a subplot', 'Data');
T(s, '**DI (%) = Σ(x × f) / (9 × Σf) × 100**   (x = grade, f = number of leaves with grade x, 9 = highest grade; 15 leaves per subplot)', 0.45, 1.2, 12.43, 0.5);
tb(s, [['Leaf area with pustules', 'Grade', 'Subplot DI (%)', 'Class', 'Name'], ['0', '0', '0', '0', 'healthy'], ['1–5%', '1', '> 0–5', '1', 'very low'], ['6–10%', '3', '> 5–10', '3', 'low'], ['11–25%', '5', '> 10–25', '5', 'moderate'], ['26–50%', '7', '> 25–50', '7', 'high'], ['> 50%', '9', '> 50', '9', 'very high']], 0.45, 1.85, 6.9, [2.0, 0.9, 1.6, 0.9, 1.5]);
ex(s, ['Subplot 25-2, 18 January – 15 grades: 0, 0, 1, 1, 1, 3, 3, 3, 3, 5, 5, 5, 7, 7, 9.', 'Σ(x × f) = 0×2 + 1×3 + 3×4 + 5×3 + 7×2 + 9×1 = 53', 'DI = 53 / (9 × 15) × 100 = 39.3% → class 7 (high); Task A = diseased.'], 7.6, 1.85, 5.28, 3.0);
refline(s, 'DI formula for white rust: Mishra et al. (2009); DI from graded leaves as UAV target: Liu et al. (2024); area diagrams: Conn et al. (1990); trained single scorer: Bock et al. (2010).', 6.0, 0.6);

s = S('Labels of the three tasks and the covariates', 'Data');
tb(s, [['Data', 'Task A', 'Task B', 'Task C'], ['UAV post-symptomatic', 'healthy (DI = 0) / diseased (DI > 0), from the survey', 'DI class', 'DI (%)'],
  ['UAV pre-symptomatic', 'healthy plots vs inoculated subplots that show pustules later', '–', '–'], ['ASD leaves', 'grade 0 / > 0', 'leaf grade', 'grade as a number']], 0.45, 1.2, 12.43, [2.6, 6.0, 1.8, 2.03], { firstCol: true });
BL(s, ['**Rare classes:** a DI class with < 5% of the samples is merged with its neighbour (e.g. 7 + 9).',
  '**Covariates** (not used in feature selection): DAI; variety; sowing date; BBCH stage (vegetative, flowering, pod); 7-day weather ending the day before the flight; favourable days since inoculation (leaf: Tmax 16–24 °C, RH I > 97%, RH II > 40%; staghead: Tmax 20–29 °C, Tmin > 12 °C, RH I > 97%).'], 0.45, 3.35, 12.43, 2.4);
refline(s, 'labels from the later status: Zhu et al. (2017), Tian et al. (2021); favourable-day conditions: Chattopadhyay et al. (2011).', 6.15, 0.45);

s = S('How many samples', 'Data');
tb(s, [['Data set', 'How it is counted', 'All', 'Training plots (33)', 'Test plots (15)'],
  ['UAV post-symptomatic (per camera)', '48 plots × 4 subplots × 10 dates', '1920', '1320', '600'],
  ['UAV pre-symptomatic (per camera)', '48 × 4 × 3 dates', '576', '396', '180'],
  ['ASD leaves', '48 × 4 subplots × 1 centre plant × 3 leaves × 13 dates', '7488', '5148', '2340'],
  ['Leaf grades for the DI', '192 subplots × 15 leaves × 13 dates', '37 440', '–', '–'],
  ['Physiology', '48 subplots × 4 dates per parameter', '192', 'description only', '–']], 0.45, 1.2, 12.43, [3.2, 4.4, 1.2, 1.9, 1.73], { firstCol: true });

// ================================================================ Preparation
sec('Preparation');
s = S('Stage 1: from raw images to one value per band and subplot', 'Stage 1');
pos(s, 'data collection (Part A)', 'feature extraction (Stage 2)', 'all 48 plots, all 13 dates, all four cameras');
chain(s, [{ h: 'B1 Calibration', b: 'reflectance (panels, light sensor); temperature' }, { h: 'B2 Mosaics', b: 'structure-from-motion; HS georectified; same GCPs' }, { h: 'B3 HS cleaning', b: 'remove water bands → 483 bands; Savitzky–Golay (5, 2)' },
  { h: 'B4 Co-register', b: 'UTM 43N; RGB, MS, TIR → HS; error < 1 pixel' }, { h: 'B5 One grid', b: '2.2-cm HS grid (RGB texture first)' }, { h: 'B6 ROI means', b: 'mean of all ROI pixels per band and subplot' }], 0.45, 2.3, 12.43, 1.9, 0.18, C.g, C.lt);
key(s, 'Each image becomes reflectance (or temperature), all cameras are put on one map grid, and every subplot ROI is averaged. Result: one row per subplot and date with the mean of every band.', 0.45, 4.45, 12.43, 1.1);
refline(s, 'water bands removed: Mandal et al. (2023); Savitzky–Golay window 5, order 2: Chen et al. (2023), Savitzky and Golay (1964); smoothing: Ma et al. (2026), Feng et al. (2022); ROI means: Ma et al. (2026), Liu et al. (2024); mosaics: Liu et al. (2024).', 5.8, 0.75);

s = S('Stage 1 in detail: why each step comes where it does', 'Stage 1');
BL(s, ['**Calibration first:** only reflectance (not digital numbers) can be compared between dates.',
  '**Mosaics with the same ground control points:** a subplot falls on the same map position on all 13 dates.',
  '**Smoothing before derivatives:** derivatives amplify noise; never smooth across a removed water band.',
  '**Co-registration before ROI means:** one ROI must cover the same plants in all four cameras.',
  '**RGB texture before resampling:** averaging to 2.2 cm would remove the fine texture of pustules.',
  '**Flowers stay in the ROI:** staghead belongs to the disease; results are reported by growth stage.'], 0.45, 1.2, 7.2, 4.9);
ex(s, ['Subplot 25-2, 18 Jan: 6 090 ROI pixels; R550 = 0.084, R670 = 0.052, R800 = 0.371; 24.1 °C; DI 28.4%.', 'Healthy 7-1: R670 = 0.041, R800 = 0.418; 22.8 °C; DI 0.', 'Diseased: more red (less chlorophyll), less NIR (damaged leaves), warmer (less transpiration).'], 7.9, 1.2, 4.98, 3.6);

s = S('Stage 2: features of the hyperspectral camera', 'Stage 2');
BL(s, ['**Reflectance** of 483 bands.', '**First derivative:** FD(λi) = [R(λi+1) − R(λi−1)] / (λi+1 − λi−1).', '**Red-edge parameters:** position, amplitude Dr and area SDr over 680–760 nm.',
  '**48 published indices** (39 base + 9 SWIR disease indices).', '**Texture:** PCA of HS pixels → 3 component images → GLCM (3 × 3 window, distance 1, 4 directions, 64 levels) → 8 measures × 3 = 24 features.'], 0.45, 1.2, 6.9, 4.4);
ex(s, ['GLCM: count pairs of grey levels (i, j) of neighbouring pixels → probability P(i, j).', 'Contrast = Σ(i − j)² P(i, j); homogeneity = Σ P(i, j)/[1 + (i − j)²].', '4 × 4 demo image: contrast 0.583, homogeneity 0.808.', 'Pustules and chlorotic patches → contrast up, homogeneity down.'], 7.6, 1.2, 5.28, 3.4);
refline(s, 'red-edge derivative features: Zhang et al. (2012); PCA texture: Ma et al. (2026), Guo et al. (2021); GLCM: Haralick et al. (1973).', 6.15, 0.45);

s = S('Stage 2: features of the multispectral, RGB and thermal cameras', 'Stage 2');
tb(s, [['Camera', 'Group', 'Features', 'n'],
  ['Multispectral', 'bands, indices', '5 bands; NDVI, GNDVI, NDRE, CIgreen, CIrededge, MTCI, OSAVI, SAVI, TCARI, MCARI, MSR, PSRI; 10 two-band NDs', '27'],
  ['', 'texture', '8 GLCM measures × 5 bands', '40'],
  ['RGB', 'colour', 'ExG, ExR, ExG − ExR, VARI, GLI, NGRDI; mean hue, saturation, value', '9'],
  ['', 'texture', '8 GLCM measures × R, G, B (native 0.8 cm)', '24'],
  ['Thermal', 'temperature', 'mean, median, SD, P10, P90, MTD; CTD, CTR, NRCT, ΔT', '10'],
  ['', 'texture', '8 GLCM measures of the temperature image', '8']], 0.45, 1.2, 12.43, [1.8, 1.7, 8.1, 0.83], { firstCol: true });
refline(s, 'MS indices and texture: Liu et al. (2024), Nguyen et al. (2023); RGB texture: Feng et al. (2022); thermal: Feng et al. (2022), Calderón et al. (2014), Oerke et al. (2006); features kept by sensor: Maimaitijiang et al. (2020).', 5.7, 0.6);

s = S('Stage 2 output: one table per camera', 'Stage 2');
tb(s, [['Column group', 'Columns'], ['Identifiers', 'date, DAI, plot, subplot, replication, treatment, variety, sowing date, split'], ['Labels', 'DI, DI class, healthy/diseased'], ['Covariates', 'growth stage, 7-day weather, favourable days'], ['Features', 'prefixes R_, FD_, RE_, VI_, TX_, TH_']], 0.45, 1.2, 7.2, [1.9, 5.3], { firstCol: true });
tb(s, [['Camera', 'Candidate features'], ['Hyperspectral', 'about 1040'], ['Multispectral', '67'], ['RGB', '33'], ['Thermal', '18']], 8.0, 1.2, 4.88, [2.5, 2.38], { firstCol: true });
key(s, 'The four tables have identical rows (subplot-dates), so any sensor set is a join of tables by subplot code and date. Feature formulas use no labels, so they are computed for all samples.', 0.45, 4.3, 12.43, 1.1);

// ================================================================ Split
sec('Data split');
s = S('Stages 3–4: why the data are divided by whole plots', 'Stage 4');
pos(s, 'Stages 1–2 (camera tables with labels)', 'every later stage', 'the plot list – the division is made once, before the first flight');
BL(s, ['**Subplots of one plot share** soil, row spacing, microclimate and inoculum.', '**If a plot were on both sides,** the model could learn the plot instead of the disease → test accuracy too high.',
  '**So whole plots are divided:** 33 training plots, 15 test plots (7:3).', '**The proportion 7:3** is that of the DT-EDNet study and of other disease and UAV studies.'], 0.45, 2.3, 12.43, 3.0);
refline(s, 'grouped cross-validation for structured data: Roberts et al. (2017); 7:3 split: Ma et al. (2026), Bijlwan et al. (2025), Abdulridha et al. (2023), Maimaitijiang et al. (2020); one-third hold-out: Mandal et al. (2023).', 5.7, 0.6);

s = S('How the 15 test plots are chosen (D1)', 'Stage 4');
tb(s, [['Block', 'Test plots', 'Training plots'], ['Healthy (1–12)', '1, 4, 5, 8', '2, 3, 6, 7, 9, 10, 11, 12'], ['R3 (13–24)', '13, 14, 18', '15, 16, 17, 19, 20, 21, 22, 23, 24'], ['R2 (25–36)', '25, 27, 31, 35', '26, 28, 29, 30, 32, 33, 34, 36'], ['R1 (37–48)', '37, 44, 46, 48', '38, 39, 40, 41, 42, 43, 45, 47']], 0.45, 1.2, 6.3, [1.6, 1.6, 3.1], { firstCol: true });
BL(s, ['**30% of each block type:** 4 of 12 healthy, 11 of 36 inoculated plots.', '**All 4 sowing dates and 3 varieties** are in the test set, spread over R1–R3.', '**Same test plots as 2025-26** (same plot plan).', '**Split column (TRAIN/TEST)** written into every table before any analysis.'], 7.0, 1.2, 5.88, 3.0);
img(s, 'x02_plot_split.png', 1.8, 4.05, 9.6, 2.6);

s = S('Validation inside the 33 training plots (D2)', 'Stage 4');
img(s, 'x05_groupkfold.png', 0.45, 1.15, 12.43, 2.7);
BL(s, ['**Machine learning – GroupKFold(3):** three rounds; in each round 22 plots fit and 11 plots score; the mean of the three rounds judges a setting or a feature subset.',
  '**Networks – 11 fixed validation plots** (6, 7, 11, 19, 24, 26, 28, 30, 36, 39, 41; seed 42): weights fitted on 22 plots; the validation plots decide when to stop.',
  '**Same folds and validation plots** for every camera, sensor set and model.'], 0.45, 4.0, 12.43, 2.0);
refline(s, 'cross-validation inside the training data for SFFS and SVM: Tian et al. (2021), Lv et al. (2023) – here by whole plots; validation set for the networks: Ma et al. (2026) (10% of samples ≈ 3 plots, so one third of the plots is used).', 6.1, 0.6);

s = S('Number of samples in every part', 'Stage 4');
img(s, 'x03_sample_flow.png', 0.45, 1.15, 7.4, 3.9);
tb(s, [['Data set', 'Train', 'Fit', 'Val.', 'Test'], ['UAV post (per camera)', '1320', '880', '440', '600'], ['UAV pre (per camera)', '396', '264', '132', '180'], ['ASD leaves', '5148', '3432', '1716', '2340']], 8.0, 1.2, 4.88, [1.9, 0.75, 0.75, 0.73, 0.75], { firstCol: true });
BL(s, ['**Fit / validation** = network split of the training plots.', '**ML** uses GroupKFold(3): about 880 samples fit and 440 score in each round.'], 8.0, 3.2, 4.88, 1.9);

s = S('Which samples each stage uses', 'Stage 4');
img(s, 'x04_data_use.png', 0.45, 1.1, 7.8, 5.6);
BL(s, ['**Descriptive stages** (curves, correlations, physiology, stability) may use **all plots** – nothing from them enters a model.',
  '**Learning stages** (selection, constants, tuning, fitting) use **only training plots** or their inner parts.',
  '**Test plots** are only predicted, once.'], 8.5, 1.3, 4.38, 4.4);

s = S('Leakage rules (D5)', 'Stage 4');
[['No plot on both sides', 'of any division: training/test, fitting/scoring, fitting/validation'], ['Everything learned from training plots', 'features, scaling constants, healthy references, weights; test indices use the training wavelengths'], ['Freeze, then test once', 'every model is frozen before the test plots are predicted']].forEach((r, i) => {
  box(s, 0.45 + i * 4.2, 1.4, 3.95, 2.6, r[0], r[1], C.red, C.lred);
});
key(s, 'On a new data set: make a new plot-wise split before any analysis (30% of plots of each block type, all treatments), fix new folds and validation plots. To test frozen models only, all new data are test data.', 0.45, 4.4, 12.43, 1.2);

// ================================================================ Normalisation
sec('Normalisation');
s = S('Stage 5: normalisation – what, when and with which numbers (1/2)', 'Stage 5');
key(s, 'No z-score or min–max at the start. Physical normalisation first; thermal relative to air and healthy plots; z-score only inside model pipelines with constants of the fitting part.', 0.45, 1.15, 12.43, 0.95);
tb(s, [['Where', 'What', 'How', 'Constants from'],
  ['Stage 1', 'all spectra', 'reflectance from panels; mean of ROI pixels', 'panels of each flight'],
  ['Stage 2', 'spectral features', 'indices and derivatives remove part of the brightness effect', 'formulas only'],
  ['Stage 5 (D3)', 'canopy temperature', 'CTD, CTR, NRCT within each date, ΔT to healthy plots', 'air temperature; image; healthy training plots'],
  ['Stage 7', 'indices (ReliefF); bands (PLS/CARS)', 'min–max 0–1 inside ReliefF; z-score before PLS', 'training plots']], 0.45, 2.3, 12.43, [1.7, 2.9, 4.6, 3.23], { firstCol: true });
refline(s, 'Ma et al. (2026); Zhang et al. (2012); Feng et al. (2022); Calderón et al. (2014); Oerke et al. (2006); Maimaitijiang et al. (2020); Robnik-Šikonja and Kononenko (2003); Bijlwan et al. (2025).', 5.9, 0.5);
s = S('Stage 5: normalisation (2/2) and worked examples', 'Stage 5');
tb(s, [['Where', 'What', 'How', 'Constants from'],
  ['Stages 9–10 (D4)', 'inputs of SVM/SVR, k-NN, PLS, networks', 'z = (x − mean)/SD in a pipeline; random forest unscaled', 'fitting part of each fold; then 33 training plots'],
  ['Stage 13 (3.2)', 'pre-symptomatic spectra', 'spectrum × baseline/healthy mean of the date, per variety', 'healthy training plots']], 0.45, 1.2, 12.43, [1.9, 3.0, 4.4, 3.13], { firstCol: true });
ex(s, ['Thermal: Tc = 24.1 °C, Ta = 22.0 °C → CTD = +2.1 °C, CTR = 1.095; healthy mean 22.9 °C → ΔT = +1.2 °C.', 'NRCT = (Tc − Tmin)/(Tmax − Tmin) within the image of the date.'], 0.45, 3.0, 6.1, 2.2);
ex(s, ['z-score: NDRE on the 22 fitting plots of a round has mean 0.31, SD 0.05.', 'A scoring sample with NDRE 0.24 → z = (0.24 − 0.31)/0.05 = −1.4.', 'The scoring plots never change the mean and SD.'], 6.78, 3.0, 6.1, 2.2);
refline(s, 'z-score in the training part, trees unscaled: Bijlwan et al. (2025), Shafiee et al. (2021); healthy-baseline normalisation: Lv et al. (2023); thermal: Feng et al. (2022).', 5.5, 0.5);

// ================================================================ Objective 1
sec('Objective 1');
s = S('Stage 6: describing the response (all 48 plots)', 'Objective 1');
pos(s, 'Stages 1–5', 'interpretation of the selected features', 'all 48 plots, 1920 subplot-dates per camera – description only');
img(s, 'g07_spectra_demo.png', 0.45, 2.25, 7.6, 2.6);
BL(s, ['**6.1** mean ± SD reflectance and FD per DI class; % difference from class 0.', '**6.2** Pearson r of every feature with the DI; top 10 per camera.', '**6.3** same curves within each growth stage, variety and date; DI vs favourable days.'], 8.3, 2.25, 4.58, 3.4);
refline(s, 'class spectra: Ma et al. (2026), Mandal et al. (2023); correlation with DI: Zhang et al. (2012); by growth stage: Blasch et al. (2023), Liu et al. (2024), Zhang et al. (2022).', 5.95, 0.6);

s = S('Stage 6: plant physiology, in order', 'Objective 1');
chain(s, [{ h: '1 Screen', b: 'values beyond median ± 3 SD flagged; removed only if faulty' }, { h: '2 Infected vs healthy', b: 'paired t-test per date (Wilcoxon if not normal)' }, { h: '3 Treatments', b: 'two-way ANOVA (variety × sowing date), LSD 5%' }, { h: '4 Link', b: 'r with DI and with the selected features' }], 0.45, 1.3, 12.43, 2.0, 0.3, C.teal || C.g, C.lt);
BL(s, ['**Ten parameters on 4 dates:** chlorophyll a, b, carotenoids, anthocyanin, protein, relative water content, membrane stability, photosynthesis, transpiration, stomatal conductance.', '**Purpose:** explain why a feature responds (e.g. red edge ↔ chlorophyll, thermal ↔ stomatal conductance).'], 0.45, 3.6, 12.43, 1.8);
refline(s, 'outlier screening and day-by-day tests: Tian et al. (2021); physiology explaining thermal and spectral signals: Calderón et al. (2013); spectra with physiology: Yu et al. (2025); white rust biochemistry: Mishra et al. (2009).', 5.8, 0.6);

s = S('Stage 7: why features are selected this way', 'Objective 1');
BL(s, ['**Inside each camera:** ~1000 HS features would swamp 18 thermal and 33 RGB features; select within each sensor, then fuse.',
  '**One method per feature type:** bands → SHAP-CARS; indices → filter + ReliefF; texture → mRMR + TTFI.',
  '**On the training plots only:** the selected features are model inputs.',
  '**For each task:** ReliefF for classes (A, B), RReliefF for DI (C); VIF per task → 3 DSFs per camera.'], 0.45, 1.2, 6.0, 4.6);
img(s, 'g10_selection_chain.png', 6.7, 1.15, 6.18, 4.7);
refline(s, 'selection within each sensor, VIF, then fusion: Mustafa et al. (2023); one method per feature group: Ma et al. (2026); selection bias: Ambroise and McLachlan (2002).', 6.0, 0.5);

s = S('Stage 7: the selection of each camera (training plots, each task)', 'Objective 1');
tb(s, [['Camera', 'Group (candidates)', 'Selection, in order', 'Kept'],
  ['Hyperspectral', 'bands R + FD (966)', 'NDSI/RSI maps → SHAP top 40% → CARS', 'OW 10–15'], ['', 'indices 48 + 3 RE + NDSI, RSI, WRI', '|r| ≥ 0.95 → ReliefF / RReliefF', '5'], ['', 'PCA texture (24)', '|r| ≥ 0.95 → mRMR → TTFI', '6 + TTFI'],
  ['Multispectral', '5 bands + 12 indices + best ND', '|r| ≥ 0.95 → ReliefF / RReliefF', '5'], ['', 'GLCM of 5 bands (40)', '|r| ≥ 0.95 → mRMR → TTFI-MS', '6 + TTFI'],
  ['RGB', '6 colour indices + H, S, V', '|r| ≥ 0.95 → ReliefF / RReliefF', '5'], ['', 'GLCM of R, G, B (24)', '|r| ≥ 0.95 → mRMR → TTFI-RGB', '6 + TTFI'],
  ['Thermal', '18 features', '|r| ≥ 0.95 → ReliefF; 4 normalised kept', '5 + 4'], ['Each camera', 'pooled survivors', 'VIF: remove largest until all < 10', 'DSF']], 0.45, 1.2, 12.43, [1.9, 3.7, 5.1, 1.73], { firstCol: true });

s = S('Step 7.1: band-pair maps and effective ranges (1.2.1)', 'Objective 1');
T(s, '**NDSI(i, j) = (Ri − Rj) / (Ri + Rj)      RSI(i, j) = Ri / Rj**', 0.45, 1.2, 7.4, 0.5);
BL(s, ['For every band pair (every 2nd band, ~29 000 pairs) compute both indices for all training samples.', 'Draw R² with the DI as maps.', '**Effective ranges** = bands in pairs with **R² > 0.5 in both maps**; if none, the top 5% of pairs.', 'Best NDSI and RSI pairs kept for Step 7.3.'], 0.45, 1.8, 7.4, 3.6);
img(s, 'g08_ndsi_demo.png', 8.1, 1.15, 4.78, 4.7);
refline(s, 'R² maps and the 0.5 rule (effective ranges 455–503, 520–661, 702–1000 nm): Ma et al. (2026); maps on calibration data only: Mandal et al. (2023); top 5%: Tian et al. (2021).', 6.0, 0.6);

s = S('Step 7.2: optimal wavelengths by SHAP-CARS (1.2.2)', 'Objective 1');
chain(s, [{ h: 'Candidates', b: 'R and FD bands in the effective ranges' }, { h: 'SHAP', b: 'random forest (500 trees) of DI; mean |SHAP|; top 40%' }, { h: 'PLS components', b: 'z-score; MCCV 50 divisions by plot; 1–15 components' },
  { h: 'CARS', b: '50 iterations: drop small PLS coefficients, re-sample by weight' }, { h: 'OW', b: 'subset with lowest GroupKFold(3) RMSE; 10–15 bands' }], 0.45, 1.25, 12.43, 1.6, 0.22, C.blue, C.lblue);
img(s, 'g09_shapcars_demo.png', 0.9, 3.05, 11.5, 2.9);
refline(s, 'SHAP-CARS (12 key wavelengths): Ma et al. (2026); SHAP: Lundberg and Lee (2017); random forest: Breiman (2001); CARS: Li et al. (2009).', 6.15, 0.45);

s = S('Step 7.3: data-driven indices and the White Rust Index (1.3)', 'Objective 1');
T(s, '**WRI = (Rλ1 − Rλ2) / (Rλ1 + Rλ2) + w × Rλ3**', 0.45, 1.2, 12.43, 0.45);
BL(s, ['Best NDSI and RSI pairs of Step 7.1 (bands ≥ 10 nm apart) → two indices.', 'WRI search: 6-nm steps in the effective ranges; λ1, λ2 ≥ 50 nm apart; w ∈ {−1, −0.5, 0, 0.5, 1}.', 'Score: |r| with DI and balanced accuracy healthy vs diseased (one threshold); repeat once with SWIR.', 'Wavelengths fixed on training plots → computed for every sample.'], 0.45, 1.75, 6.6, 3.6);
tb(s, [['Rank', 'λ1', 'λ2', 'λ3', 'w', '|r|', 'Bal. acc.'], ['1', '754', '700', '532', '−0.5', '0.71', '0.83'], ['2', '760', '694', '550', '−0.5', '0.70', '0.82'], ['3', '790', '718', '—', '0', '0.68', '0.80']], 7.3, 1.8, 5.58, [0.7, 0.75, 0.75, 0.75, 0.75, 0.75, 1.13]);
T(s, 'Demo output of the WRI search', 7.3, 3.4, 5.58, 0.35, { italic: true });
refline(s, 'index form, 6-nm steps, 50-nm rule, weights, balanced accuracy: Mahlein et al. (2013); best band pair as a new index (RBI, NDBI): Mandal et al. (2023).', 5.8, 0.6);

s = S('Steps 7.4–7.5: redundancy filter and ReliefF ranking (1.4)', 'Objective 1');
BL(s, ['**Filter:** indices with |r| ≥ 0.95 form clusters; keep the one with the highest |r| with the DI.', '**ReliefF (A, B) / RReliefF (C), k = 10,** after min–max scaling to 0–1.', '**Weight update:** W(f) ← W(f) − diff(f, x, hit)/(m·k) + diff(f, x, miss)/(m·k).', '**Keep the top five per task** = VI.'], 0.45, 1.2, 6.6, 3.8);
ex(s, ['Diseased sample: scaled NDRE 0.20.', 'Nearest diseased (hits): 0.24 → difference 0.04.', 'Nearest healthy (misses): 0.65 → difference 0.45.', 'Large miss difference, small hit difference → NDRE gains weight.'], 7.3, 1.2, 5.58, 2.9);
refline(s, 'redundancy among indices: Ma et al. (2026), Lv et al. (2023); Relief top five: Ma et al. (2026); RELIEF-F for disease features: Mahlein et al. (2013); ReliefF/RReliefF: Robnik-Šikonja and Kononenko (2003).', 5.6, 0.6);

s = S('Steps 7.6–7.7: texture – mRMR and the Tri-band Texture Fusion Index (1.5)', 'Objective 1');
BL(s, ['**Filter** the 24 texture features at |r| ≥ 0.95.', '**mRMR:** add the feature with the largest relevance minus redundancy: score(f) = I(f; DI) − mean I(f; chosen).', '**Keep the top six** (TF1–TF6).', '**TTFI:** 120 ordered triplets × 3 formulas; the highest |r| with the DI wins.'], 0.45, 1.2, 6.6, 3.6);
tb(s, [['Formula', 'Demo (0.8, 1.2, 0.5)', 'Value'], ['TTFI1 = (TF1 + TF2)/TF3', '2.0/0.5', '4.00'], ['TTFI2 = TF1 × TF2/TF3', '0.96/0.5', '1.92'], ['TTFI3 = TF1 × (TF1 + TF2)/(TF2 + TF3)', '0.8 × 2.0/1.7', '0.94']], 7.3, 1.2, 5.58, [3.0, 1.6, 0.98]);
refline(s, 'mRMR top six and TTFI (TTFI3 |r| = 0.756): Ma et al. (2026); mRMR: Peng et al. (2005); mRMR for disease features: Yuan et al. (2025).', 5.6, 0.5);

s = S('Steps 7.8–7.10: multispectral, RGB and thermal cameras (1.6.2–1.6.4)', 'Objective 1');
box(s, 0.45, 1.2, 4.0, 4.0, 'Multispectral (67)', ['best of 10 two-band NDs added', 'spectral (18): filter → ReliefF top 5', 'texture (40): filter → mRMR top 6 → TTFI-MS', '→ 12 candidates'], C.blue, C.lblue, { align: 'left', valign: 'top' });
box(s, 4.67, 1.2, 4.0, 4.0, 'RGB (33)', ['colour (9): filter → ReliefF top 5', 'texture (24): filter → mRMR top 6 → TTFI-RGB', '→ 12 candidates'], C.purple, C.lpurple, { align: 'left', valign: 'top' });
box(s, 8.89, 1.2, 4.0, 4.0, 'Thermal (18)', ['statistics + texture: filter → ReliefF top 5', '4 normalised temperatures always kept (weather)', '→ ≤ 9 candidates; VIF removes collinear ones'], C.red, C.lred, { align: 'left', valign: 'top' });
refline(s, 'MS indices and three-texture indices from 40 MS textures: Liu et al. (2024); MS indices and GLCM: Nguyen et al. (2023); colour and texture screened separately: Huang et al. (2020); RGB/thermal texture and temperature parameters: Feng et al. (2022); NRCT: Maimaitijiang et al. (2020); weather and leaf temperature: Oerke et al. (2006).', 5.45, 0.8);

s = S('Step 7.11: variance inflation factor → DSF of each camera (1.6.5)', 'Objective 1');
T(s, '**VIF_j = 1 / (1 − R_j²)**  (R_j² from regressing feature j on the other candidates of the camera); remove the largest until all VIF < 10.', 0.45, 1.2, 12.43, 0.75);
tb(s, [['Round', 'Largest VIF', 'Removed', 'Left'], ['1', '86.4', 'FD_722', '26'], ['2', '31.2', 'NDVI780', '25'], ['3', '14.8', 'PC2-Var', '24'], ['12', '8.9 (< 10)', '—', '15 = DSF']], 0.45, 2.1, 5.2, [1.0, 1.4, 1.6, 1.2]);
tb(s, [['Camera', 'DSF (Task C, demo)', 'n'], ['HS', 'R560, FD716, FD742, R1450, WRI, PSRI, CIrededge, PC2-Mea, PC2-Con, TTFI …', '15'], ['MS', 'NDRE, PSRI, MTCI, RE band, NIR-Con, RE-Hom, TTFI-MS', '7'], ['RGB', 'ExG − ExR, VARI, saturation, G-Ent, R-Con, TTFI-RGB', '6'], ['Thermal', 'CTD, NRCT, ΔT, MTD', '4']], 5.9, 2.1, 6.98, [1.1, 5.2, 0.68], { firstCol: true });
refline(s, 'VIF < 10: Lv et al. (2023), Tian et al. (2021); VIF on the selected features of each sensor: Mustafa et al. (2023).', 5.6, 0.45);

s = S('Steps 7.12–7.13: stability and complementarity (1.6.6–1.6.7)', 'Objective 1');
box(s, 0.45, 1.2, 6.1, 3.4, 'Stability by growth stage (all plots, description)', ['within vegetative, flowering, pod stages: t-test healthy vs diseased and r with DI', 'box plots by DI class', 'stable = significant with the same sign in all three stages'], C.g, C.lt, { align: 'left', valign: 'top' });
box(s, 6.78, 1.2, 6.1, 3.4, 'Complementarity of cameras', ['correlation between the DSFs of different cameras', 'low correlation → fusion may help', 'checked in Objective 2 (fusion gain, ablation)'], C.blue, C.lblue, { align: 'left', valign: 'top' });
refline(s, 'features common to all days: Tian et al. (2021); indices consistent only in later stages: Liu et al. (2024); bands change with stage: Zhang et al. (2024); stable features: Mustafa et al. (2023); sensor complementarity: Mahlein et al. (2019), Feng et al. (2022).', 4.9, 0.8);

// ================================================================ Objective 2
sec('Objective 2');
s = S('Stage 8: building the 15 sensor sets (2.1–2.2)', 'Objective 2');
tb(s, [['Type', 'Sensor sets'], ['Single (4)', 'S1 HS, S2 MS, S3 RGB, S4 TIR'], ['Pairs (6)', 'S5 HS+MS, S6 HS+RGB, S7 HS+TIR, S8 MS+RGB, S9 MS+TIR, S10 RGB+TIR'], ['Triplets (4)', 'S11 HS+MS+RGB, S12 HS+MS+TIR, S13 HS+RGB+TIR, S14 MS+RGB+TIR'], ['All (1)', 'S15 HS+MS+RGB+TIR']], 0.45, 1.2, 12.43, [1.9, 10.53], { firstCol: true });
chain(s, [{ h: '1', b: 'take the DSF of each camera for the task' }, { h: '2', b: 'join by subplot code and date' }, { h: '3', b: 'VIF < 10 again (training plots)' }, { h: '4', b: 'same features for test samples (training wavelengths)' }], 0.45, 3.65, 12.43, 1.4, 0.3, C.purple, C.lpurple);
T(s, '**15 sets × 3 tasks = 45 input tables.** No new selection: the DSFs were already chosen on the training plots.', 0.45, 5.2, 12.43, 0.45);
refline(s, 'every sensor and every combination modelled: Maimaitijiang et al. (2020), Mahlein et al. (2019); feature-level fusion: Feng et al. (2022), Liu et al. (2024); per-sensor selection then fusion with VIF: Mustafa et al. (2023).', 5.8, 0.6);

s = S('Stage 9: the four machine-learning models', 'Objective 2');
tb(s, [['Model', 'Idea', 'A, B', 'C'], ['SVM / SVR (RBF)', 'boundary (or tube) with the largest margin in a transformed space', 'SVM', 'SVR'], ['Random forest', 'many trees on bootstrap samples; vote or mean', 'classifier', 'regressor'], ['k-NN', 'label of the k most similar training samples', 'classifier', 'regressor'], ['PLS-DA / PLSR', 'few latent components explaining features and target', 'PLS-DA', 'PLSR']], 0.45, 1.2, 12.43, [2.4, 6.6, 1.7, 1.73], { firstCol: true });
key(s, 'For every model × sensor set × task: (1) SFFS chooses the subset; (2) grid search tunes the settings on that subset; (3) refit on all 33 training plots and freeze → 4 × 15 × 3 = 180 frozen ML models.', 0.45, 4.1, 12.43, 1.2);
refline(s, 'SVM: Cortes and Vapnik (1995), Tian et al. (2021); random forest: Breiman (2001), Abdulridha et al. (2023); k-NN: Mustafa et al. (2023); PLS: Wold et al. (2001), Zhang et al. (2012), Krishna et al. (2014).', 5.6, 0.6);

s = S('Step 9.1: sequential floating forward selection (2.3)', 'Objective 2');
BL(s, ['Start empty; add the feature with the best GroupKFold(3) score.', 'After each addition try removing one feature; remove it if the score improves ("floating").', 'Up to 15 features; keep the subset with the best score.', 'Score: macro-F1 (A, B), −RMSE (C); default settings during SFFS; scaler inside the pipeline.', '**Stability check** for the best model: SFFS over 100 random GroupKFold(3) divisions; selection frequency.'], 0.45, 1.2, 5.6, 4.7);
img(s, 'x06_sffs.png', 6.2, 1.25, 6.68, 2.4);
refline(s, 'SFFS: Pudil et al. (1994); ML-SFFS with LDA, k-NN, SVM (100 repetitions, most frequent combination): Tian et al. (2021); Relief-F + SFFS: Lv et al. (2023); mlxtend SFFS: Mustafa et al. (2023), Raschka (2018); SFS + SVR: Shafiee et al. (2021).', 6.0, 0.7);

s = S('Steps 9.2–9.3: grid search and final fit (2.4)', 'Objective 2');
tb(s, [['Model', 'Settings searched (GroupKFold(3))'], ['SVM / SVR', 'C ∈ {0.1, 1, 10, 100}; γ ∈ {0.001, 0.01, 0.1, scale}; ε ∈ {0.1, 0.5}; balanced weights'], ['Random forest', '500 trees; max_features ∈ {sqrt, 0.3}; min_samples_leaf ∈ {1, 3, 5}; balanced'], ['k-NN', 'k ∈ {3, 5, 7, 9, 11}; uniform or distance weights'], ['PLS-DA / PLSR', '1–15 components']], 0.45, 1.2, 12.43, [2.2, 10.23], { firstCol: true });
ex(s, ['Random forest, S7 (HS + TIR), Task B: joined DSF 18 features → SFFS keeps 7 (inner macro-F1 0.61) → grid: max_features = sqrt, min_samples_leaf = 3 (0.63) → refit on 1320 training samples → frozen.'], 0.45, 3.7, 12.43, 1.3);
refline(s, 'grid search of SVM C and γ: Tian et al. (2021); grid search inside the training set: Chen et al. (2023), Bijlwan et al. (2025), Shafiee et al. (2021).', 5.3, 0.5);

s = S('Stage 10: feature-fusion networks DNN-F1 and DNN-F2 (2.5)', 'Objective 2');
box(s, 0.45, 1.2, 6.1, 2.9, 'DNN-F1 – input-level fusion (15 sets)', ['joined feature vector → dense 64 → dense 32 (batch norm, ReLU, dropout 0.3) → softmax (A, B) or linear (C)'], C.purple, C.lpurple, { align: 'left', valign: 'top' });
box(s, 6.78, 1.2, 6.1, 2.9, 'DNN-F2 – intermediate fusion (11 fused sets)', ['one branch per camera (dense 32) → squeeze-and-excitation camera weights → join → dense 32 → output; camera weights recorded'], C.purple, C.lpurple, { align: 'left', valign: 'top' });
BL(s, ['Inputs z-scored with the 22 fitting plots; AdamW + cosine schedule; early stopping on the 11 validation plots; best epoch kept.'], 0.45, 4.3, 12.43, 0.8);
refline(s, 'DNN-F1 and DNN-F2 (DNN-F2 only for sensor combinations, better than DNN-F1): Maimaitijiang et al. (2020); one encoder per modality: Deng et al. (2024); dual branch with attention: Yu et al. (2025); squeeze-and-excitation: Hu et al. (2018), Ma et al. (2026).', 5.3, 0.7);

s = S('Stage 10: pseudo-image networks (2.6)', 'Objective 2');
BL(s, ['Features arranged as a **k × k pseudo-image** (k = ⌈√p⌉, ≥ 3; groups in order; zeros fill) – e.g. 22 features → 5 × 5.', '**DT-EDNet** vs EfficientNet-B0, ResNet18, ConvNeXt V2-Atto, identical settings (Tasks A, B).', 'Configurations OW, VI, TF, OW+VI, OW+TTFI, OW+VI+TTFI; module ablation; all 15 sets.'], 0.45, 1.2, 12.43, 1.8);
tb(s, [['Setting', 'Value (Ma et al., 2026)', 'Validation here'], ['Optimiser', 'AdamW 6 × 10⁻⁴, weight decay 10⁻⁵; cosine to 10⁻⁶', '11 of the 33 training plots'], ['Epochs, patience', '300; 60 (min. improvement 5 × 10⁻⁵)', '(Ma et al.: 10% of samples)'], ['Batch, smoothing, clipping', '32; 0.01; 1.2; seed 42', ''], ['Model kept', 'highest validation overall accuracy', '']], 0.45, 3.1, 12.43, [2.8, 6.0, 3.63], { firstCol: true });
refline(s, 'DT-EDNet and its comparisons: Ma et al. (2026); EfficientNet: Tan and Le (2019); ResNet: He et al. (2016); ConvNeXt V2: Woo et al. (2023); AdamW and cosine: Loshchilov and Hutter (2017, 2019).', 5.7, 0.6);

s = S('Stage 11: test once – the metrics (2.7)', 'Objective 2');
tb(s, [['Metric', 'Formula / meaning', 'Task'], ['OA, kappa', 'correct/all; agreement beyond chance', 'A, B'], ['Precision, recall, F1, macro-F1', 'TP/(TP+FP); TP/(TP+FN); 2PR/(P+R); mean over classes', 'A, B'], ['Within one class; QWK', 'prediction ≤ 1 class away; weighted kappa', 'B'],
  ['Sensitivity, specificity, AUC', 'recall diseased; recall healthy; area under ROC', 'A'], ['R², RMSE, RPD', '1 − SSres/SStot; √(mean squared error); SD/RMSE', 'C'], ['Low severity', 'recall for DI ≤ 5; RMSE for DI ≤ 10', 'A, C']], 0.45, 1.2, 12.43, [3.3, 7.6, 1.53], { firstCol: true });
refline(s, 'Ma et al. (2026); within one class: Cross et al. (2024); RPD: Mandal et al. (2023); kappa: Cohen (1960, 1968); AUC: Fawcett (2006); low severity: Abdulridha et al. (2023), Deng et al. (2024).', 5.6, 0.5);

s = S('Stage 11: worked example of the test metrics', 'Objective 2');
tb(s, [['', 'Pred. healthy', 'Pred. diseased'], ['Obs. healthy', '150 (TN)', '30 (FP)'], ['Obs. diseased', '40 (FN)', '380 (TP)']], 0.45, 1.2, 5.6, [1.8, 1.9, 1.9], { firstCol: true });
ex(s, ['OA = (150 + 380)/600 = 0.883', 'Sensitivity = 380/420 = 0.905; specificity = 150/180 = 0.833', 'Kappa = 0.73; macro-F1 = 0.86'], 0.45, 2.75, 5.6, 2.0);
img(s, 'g12_eval_demo.png', 6.3, 1.2, 6.58, 2.6);
T(s, 'Every frozen model predicts the 600 test samples once; features of test samples are computed with the training wavelengths and formulas.', 6.3, 4.1, 6.58, 0.9);

s = S('Stage 12: comparison, ablation and SHAP (2.8)', 'Objective 2');
BL(s, ['**Ranking** of all model × sensor-set results per task.', '**Fusion gain** = metric(fused set) − metric(best single camera in it).', '**Drop-one-camera ablation** of S15; compared with DNN-F2 camera weights – more cameras are not assumed better.', '**Network comparison and DT-EDNet ablation** on the HS configurations.', '**SHAP** of the best ML model of each task.'], 0.45, 1.2, 12.43, 3.6);
refline(s, 'fusion gain: Feng et al. (2022), Deng et al. (2024) (three modalities beat one or two); two sensors beat three: Mahlein et al. (2019); comparison, ablation, SHAP: Ma et al. (2026), Lundberg and Lee (2017).', 5.1, 0.6);

s = S('Stage 12: covariate baseline – what the cameras add (2.9)', 'Objective 2');
tb(s, [['Model', 'Inputs', 'Built as'], ['M0', 'DAI, variety, sowing date, stage, 7-day weather, favourable days', 'random forest, GroupKFold(3) tuning'], ['M1', 'best sensor set', 'best model of the task, unchanged'], ['M2', 'DSF + covariates', 'M1 model type; SFFS + grid repeated']], 0.45, 1.2, 7.4, [0.9, 3.9, 2.6], { firstCol: true });
T(s, '**ΔS = M1 − M0** (what the cameras add)    **ΔC = M2 − M1** (what covariates add)', 0.45, 3.3, 7.4, 0.5);
img(s, 'g13_covariate_demo.png', 8.1, 1.2, 4.78, 3.2);
BL(s, ['Weather windows end the day before each flight (no look-ahead).', 'In one season weather is the same for all plots on a date → M0 is a within-season baseline.'], 0.45, 3.95, 7.4, 1.4);
refline(s, 'weather vs weather + remote sensing (69% → 78%): Zhang et al. (2014a); weather-only ML: Bijlwan et al. (2025); sensors + weather RF: Ruan et al. (2022); white rust and weather: Chattopadhyay et al. (2011).', 5.6, 0.6);

s = S('Stage 12: strata, maps and the Bharatpur test (2.10–2.11)', 'Objective 2');
chain(s, [{ h: 'Strata', b: 'test metrics by variety, sowing date, growth stage, date' }, { h: 'Maps', b: 'predicted class and DI per subplot on the field layout; error maps on test plots' }, { h: 'Bharatpur', b: 'frozen models applied once to processed quadrats; no refitting or tuning' }], 0.45, 1.3, 12.43, 2.2, 0.35, C.g, C.lt);
refline(s, 'results by stage: Blasch et al. (2023), Liu et al. (2024); DI of every pixel: Deng et al. (2024); independent test year: Ma et al. (2026).', 3.9, 0.5);

// ================================================================ Objective 3
sec('Objective 3');
s = S('Stage 13: pre-symptomatic analysis – order of the steps', 'Objective 3');
chain(s, [{ h: '13.1 Labels', b: 'healthy plots vs later-infected subplots' }, { h: '13.2 Normalise', b: 'healthy baseline per date and variety' }, { h: '13.3 Describe', b: 't-tests of plot means per date (all plots)' },
  { h: '13.4 Select', b: 'per camera, binary label, training plots' }, { h: '13.5 Models', b: '15 sets; SFFS ≤ 10; DNN-F1, DNN-F2' }, { h: '13.6 Test', b: 'per date; earliest day; risk maps' }], 0.45, 1.25, 12.43, 1.9, 0.18, C.red, C.lred);
T(s, '**ratio(λ) = baseline(λ) / healthy mean of the date(λ);  normalised R(λ) = R(λ) × ratio(λ)**  (baseline = healthy training plots on 1 January)', 0.45, 3.35, 12.43, 0.5);
ex(s, ['PM 26, 7 Jan, 800 nm: baseline 0.420; healthy mean 0.400 → ratio 1.05.', 'Later-infected 0.380 → 0.399; healthy 0.402 → 0.422: the difference is kept, the date effect removed.'], 0.45, 4.0, 12.43, 1.3);
refline(s, 'labels from later status: Zhu et al. (2017), Tian et al. (2021); healthy-baseline normalisation: Lv et al. (2023); healthy references: Oerke et al. (2006), Zarco-Tejada et al. (2018).', 5.6, 0.5);

s = S('Stage 13: selection, models, test and the earliest detection day', 'Objective 3');
BL(s, ['**Selection:** Stage 7 chain with the binary label on ≤ 396 training samples → pre-symptomatic DSF of each camera.', '**Models:** SVM, RF, k-NN, PLS-DA (SFFS ≤ 10), DNN-F1, DNN-F2; no pseudo-image networks (small data).', '**Test:** 180 test samples once; metrics per date (2, 5, 8 DAI) and pooled.', '**Earliest day:** first DAI on which predicted scores of later-infected and healthy test subplots differ (t-test, p < 0.05).', '**Earliest feature:** first date with a significant difference for every DSF feature.'], 0.45, 1.2, 6.7, 4.6);
img(s, 'g15_presym_demo.png', 7.3, 1.3, 5.58, 2.2);
refline(s, 'stage-specific selection and SFFS: Tian et al. (2021); earliest day per sensor: Mahlein et al. (2019); accuracy per day: Gold et al. (2020); pre-symptomatic bands: Zhang et al. (2024), Terentev et al. (2023); risk maps: Zarco-Tejada et al. (2018).', 6.0, 0.6);

// ================================================================ Leaf
sec('ASD leaf analysis');
s = S('Stage 14: the ASD leaf analysis in order (1/2)', 'Part L');
tb(s, [['Order', 'Step', 'What is done', 'Leaves'], ['1', 'L1 Table', 'join files to plot, subplot, leaf, date, grade; average 2 readings; duplicates; Isolation Forest outliers', 'all'], ['2', 'L2 Split', 'plot split of D1; same folds and validation plots', '—'],
  ['3', 'L3 Pre-process', 'Savitzky–Golay (11, 2); 400–2400 nm, water bands kept; FD; 5-nm bands', 'all'], ['4', 'L4 Indices', '48 indices + REP, Dr, SDr at 1 nm', 'all'], ['5', 'L5.1, L5.7', 'description: spectra by grade, r curves, PCA', 'all 7488']], 0.45, 1.2, 12.43, [0.9, 1.9, 7.9, 1.73], { firstCol: true });
refline(s, 'Chen et al. (2023); Selvaprakash et al. (2026); Zhang et al. (2012); Mandal et al. (2023); Cross et al. (2024).', 5.2, 0.45);
s = S('Stage 14: the ASD leaf analysis in order (2/2)', 'Part L');
tb(s, [['Order', 'Step', 'What is done', 'Leaves'], ['6', 'L5.2–L5.5', 'maps → SHAP-CARS → leaf OW; leaf NDSI, RSI, WRI; filter + ReliefF; VIF → leaf DSF', '5148 training'], ['7', 'L5.6', 'Jeffries–Matusita distance between grades', 'training'],
  ['8', 'L6 Models', 'ML (SFFS + grid), DNN-F1, pseudo-image networks', 'fit / validation'], ['9', 'L7 Test', 'all metrics on test leaves; by leaf position and stage', '2340 test'], ['10', 'L8–L10', 'covariate baseline; leaf–canopy link; pre-symptomatic leaves', 'same split']], 0.45, 1.2, 12.43, [0.9, 1.9, 7.6, 2.03], { firstCol: true });
BL(s, ['**Differences from UAV:** 1-nm spectra (5-nm means for searches); water bands kept (own lamp); one "camera", so no fusion.'], 0.45, 4.75, 12.43, 0.8);
refline(s, 'Ma et al. (2026); Mahlein et al. (2013); Lv et al. (2023); Mandal et al. (2023); Tian et al. (2021); Liu et al. (2026); Bohnenkamp et al. (2019).', 5.7, 0.45);

// ================================================================ Repeat
sec('New data');
s = S('Repeating the analysis on a new data set', 'New data');
tb(s, [['Situation', 'What is repeated', 'What is reused'], ['A – new season analysed on its own', 'everything (Stages 1–14) with a new plot split, new selection, new models', 'procedure and settings'],
  ['B – testing the frozen 2026-27 models', 'Stages 1–3 and Stage 11 only', 'DSF wavelengths and formulas, scaling constants, frozen models; no selection, tuning or refitting']], 0.45, 1.2, 12.43, [3.2, 4.8, 4.43], { firstCol: true });
BL(s, ['**Situation B in practice:** process images exactly as in Stages 1–2 → compute only the frozen DSF features → apply the frozen pipelines → metrics with the new survey, by site and variety → maps.'], 0.45, 3.5, 12.43, 1.2);
refline(s, 'frozen models tested once on independent data: Ma et al. (2026).', 5.0, 0.4);
s = S('Checklist for situation A, in order', 'New data');
BL(s, ['Collect data with the same protocols and codes.', 'Stage 1: process the images.', 'Stage 2: features → four camera tables.', 'Stage 3: DI, classes, labels, covariates.', 'Stage 4: plot-wise split before looking at the data; folds; validation plots.', 'Stage 5: thermal normalisation; scaling rules.', 'Stage 6: describe on all plots.'], 0.45, 1.2, 6.1, 5.2);
BL(s, ['Stage 7: select per camera on training plots → DSFs.', 'Stage 8: 15 sensor sets with VIF.', 'Stages 9–10: train ML and networks; freeze.', 'Stage 11: predict test plots once; metrics.', 'Stage 12: compare, ablate, SHAP, covariates, maps.', 'Stages 13–14: pre-symptomatic and leaf chains.', 'Keep seed 42, files of split/folds, a settings log.'], 6.78, 1.2, 6.1, 5.2);
s = S('Files to keep and software', 'New data');
tb(s, [['File', 'Content'], ['plot_table.xlsx', 'split, validation flag, treatment'], ['features_<camera>.csv', 'identifiers, labels, covariates, features'], ['folds.csv', 'GroupKFold rounds; validation plots'], ['dsf_<camera>_<task>.json', 'selected features with wavelengths, formulas'], ['model_*.joblib / .pt', 'frozen pipelines and networks'], ['metrics_test.csv', 'test predictions and metrics']], 0.45, 1.2, 6.3, [2.6, 3.7], { firstCol: true });
tb(s, [['Stage', 'Software'], ['1', 'Metashape; ENVI or GDAL/rasterio'], ['2', 'numpy, scipy savgol_filter, scikit-image GLCM'], ['7', 'shap, PLS (CARS), skrebate ReliefF, mrmr, statsmodels VIF'], ['9', 'scikit-learn, mlxtend SFFS'], ['10', 'PyTorch'], ['11', 'scikit-learn metrics']], 6.98, 1.2, 5.9, [0.9, 5.0], { firstCol: true });
refline(s, 'scikit-learn: Pedregosa et al. (2011); mlxtend: Raschka (2018).', 5.7, 0.4);

s = S('Questions you may be asked (1/2)', 'Questions');
BL(s, ['**Why is the split made before feature selection?** Selection learns from labels; if it saw the test plots, the test accuracy would be too high.', '**Why are descriptive analyses on all plots?** They decide nothing about the models.',
  '**Why GroupKFold for ML but fixed validation plots for networks?** ML can be scored in three rounds; networks need one validation set to stop – both inside training plots.', '**Is SFFS selecting twice?** Objective 1 gives each camera a compact set for all models; SFFS lets each model pick its subset – both on training plots.'], 0.45, 1.2, 12.43, 5.4);
s = S('Questions you may be asked (2/2)', 'Questions');
BL(s, ['**Why VIF again after joining cameras?** Features of different cameras can repeat each other; this appears only after joining.', '**What is frozen before the test?** Split, DSF formulas, VIF-kept features, SFFS subsets, settings, scaling constants, healthy references, weights.',
  '**How many models?** 180 ML + 45 DNN-F1 + 33 DNN-F2 + pseudo-image networks, plus pre-symptomatic and leaf models.', '**How would you analyse a new season?** Repeat Stages 1–14 with a new plot-wise split; or test the frozen models only (situation B).'], 0.45, 1.2, 12.43, 5.4);

// ================================================================ References
sec('References');
const refs = JSON.parse(fs.readFileSync(__dirname + '/deck_refs.json', 'utf8'));
const per = Math.ceil(refs.length / Math.ceil(refs.length / 12));
for (let k = 0; k < refs.length; k += per) {
  s = S('References' + (refs.length > per ? ' (' + (k / per + 1) + '/' + Math.ceil(refs.length / per) + ')' : ''), 'References');
  const part = refs.slice(k, k + per); const h1 = Math.ceil(part.length / 2);
  [part.slice(0, h1), part.slice(h1)].forEach((col, j) => T(s, col.map((r, i) => ({ text: r, options: { breakLine: i < col.length - 1, paraSpaceAfter: 3 } })), 0.45 + j * 6.3, 1.15, 6.15, 5.85, { fontSize: FS }));
}
s = pres.addSlide({ masterName: 'TITLE', sectionTitle: 'References' });
s.addText('Thank you', { placeholder: 'title' });
s.addText('The full explanation is in the document "White rust 2026-27: the data analysis explained step by step"', { placeholder: 'body' });
const { applyTheme } = require(process.env.SKILL_DIR + '/scripts/apply_theme.js');
const OUT = process.env.OUT;
pres.writeFile({ fileName: OUT }).then(async f => { await applyTheme(OUT, THEME); console.log('saved', f); });
