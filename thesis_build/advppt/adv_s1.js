// Slides 1-20: title, introduction, objectives, data collection, common data processing
const { pres, F, FS, C, S, sec, T, BL, box, arr, line, chain, tb, circ, refline } = require('./adv_lib.js');
let s;
// 1 ------------------------------------------------------------------ title
sec('Introduction');
s = pres.addSlide({ masterName: 'TITLE', sectionTitle: 'Introduction' });
s.addText('AI-based Multimodal UAV Sensing of White Rust in Indian Mustard', { placeholder: 'title' });
s.addText([{ text: 'Objectives, data collection and methodology (field season 2026-27)', options: { breakLine: true, bold: true } }, { text: ' ', options: { breakLine: true } },
  { text: 'Animesh Panda (Roll No. 13098)', options: { breakLine: true } }, { text: 'Ph.D. (Agricultural Physics), ICAR-Indian Agricultural Research Institute, New Delhi', options: { breakLine: true } },
  { text: ' ', options: { breakLine: true } }, { text: 'Presentation to the Advisory Committee', options: { italic: true } }], { placeholder: 'body' });
s.addNotes('Title slide. The presentation covers the three objectives, the data collected in the 2026-27 field season and the step-wise methodology of each objective.');
// 2 ------------------------------------------------------------------ outline
s = S('Outline of the presentation', '', 'Order of the talk.');
const outl = [['1', 'Background, research needs and objectives'], ['2', 'Overall research framework and guiding rules'], ['3', 'Field experiment and data collection (Activity A)'], ['4', 'Common data processing (Activities B, D, E, F)'],
  ['5', 'Objective 1: characterisation of white rust and disease-specific features'], ['6', 'Objective 2: detection and severity discrimination by AI-based data fusion'], ['7', 'Objective 3: prediction at the pre-symptomatic stage'], ['8', 'Expected outputs, work plan and references']];
outl.forEach((o, i) => { const col = i < 4 ? 0 : 1, r = i % 4, x = 0.7 + col * 6.2, y = 1.45 + r * 1.3; circ(s, x, y, 0.62, o[0], [C.g, C.g, C.blue, C.blue, C.g2, C.purple, C.red, C.gold][i]); T(s, o[1], x + 0.8, y + 0.08, 5.1, 0.6, { valign: 'middle', fontSize: 18 }); });
// 3 ------------------------------------------------------------------ background
s = S('Background: white rust and why multimodal UAV sensing', 'Introduction', 'White rust biology, losses and the plant responses that different cameras record.');
BL(s, ['**Pathogen:** white rust is caused by the obligate oomycete Albugo candida; it forms white pustules on the leaves, chlorosis and, after systemic infection, distorted inflorescences (staghead) (Saharan et al., 2014).',
  '**Loss:** yield reduction of 20–60% in Indian mustard (Kumar and Kalha, 2005; Saharan et al., 2014).', '**Epidemiology:** disease develops under cool and humid weather (Chattopadhyay et al., 2011).',
  '**Limitation of visual scoring:** slow, subjective and possible only after symptoms appear (Bock et al., 2010).',
  '**Opportunity:** UAV cameras record changes in pigments, leaf structure, water and temperature that accompany infection, sometimes before symptoms (Mahlein, 2016; Terentev et al., 2022); combining cameras usually improves accuracy (Maimaitijiang et al., 2020; Feng et al., 2022).'], 0.45, 1.2, 6.6, 5.4);
const resp = [['Pigment loss (chlorosis)', 'Hyperspectral and multispectral: visible and red edge', C.g], ['Pustules, leaf structure', 'Near infrared; red–green–blue texture', C.blue], ['Water loss in tissue', 'Hyperspectral short-wave infrared', C.teal], ['Changed transpiration', 'Thermal camera: canopy temperature', C.red]];
T(s, '**Plant response → camera that records it**', 7.35, 1.2, 5.5, 0.35);
resp.forEach((r, i) => { const y = 1.65 + i * 1.18; box(s, 7.35, y, 2.35, 0.95, null, r[0], r[2], 'FFFFFF'); arr(s, 9.72, y + 0.47, 10.12, y + 0.47); box(s, 10.15, y, 2.73, 0.95, null, r[1], r[2], [C.lt, C.lblue, C.lteal, C.lred][i]); });
// 4 ------------------------------------------------------------------ research needs -> objectives
s = S('Research needs and objectives', 'Introduction', 'Each research need leads to one objective.');
const needs = [['Research need 1', 'Which wavelengths, indices, texture and thermal features of each UAV camera respond to white rust in mustard, and does the response change with variety and inoculation timing?'],
  ['Research need 2', 'Which camera or camera combination, and which model (machine learning, feature-fusion networks, DT-EDNet and comparison networks), detects and grades white rust best under leakage-free validation?'],
  ['Research need 3', 'Can subplots that will develop white rust be identified before pustules appear, and how early?']];
const objs = [['Objective 1', 'To characterise white rust of mustard through multimodal sensing from a UAV platform'], ['Objective 2', 'To detect and discriminate disease severity of white rust in mustard through AI-based multimodal data fusion'], ['Objective 3', 'To predict white rust at the pre-symptomatic stage using machine learning']];
needs.forEach((n, i) => { const y = 1.3 + i * 1.8; box(s, 0.45, y, 6.0, 1.5, n[0], n[1], C.blue, C.lblue, { align: 'left' }); arr(s, 6.5, y + 0.75, 7.0, y + 0.75); box(s, 7.05, y, 5.83, 1.5, objs[i][0], objs[i][1], [C.g, C.purple, C.red][i], [C.lt, C.lpurple, C.lred][i], { align: 'left' }); });
// 5 ------------------------------------------------------------------ objectives table
s = S('Objectives: questions, data and outputs', 'Introduction', 'Objectives, data used and main outputs as in the methodology.');
tb(s, [['Objective', 'Question answered', 'Data used', 'Main output'],
  ['1. Characterise white rust through multimodal UAV sensing', 'Which wavelengths, vegetation indices, texture and thermal features of each camera respond to severity; does the response change with variety and inoculation timing?', '1920 post-symptomatic subplot samples per camera', 'Optimal wavelengths, White Rust Index, selected indices, Tri-band Texture Fusion Index, disease-specific feature set of each camera'],
  ['2. Detect and discriminate severity by AI-based multimodal fusion', 'How accurately can (a) healthy vs diseased, (b) severity classes and (c) severity score be predicted by each of 15 sensor sets with machine and deep learning?', '1920 post-symptomatic subplot samples per camera', 'Best sensor set and model per task; contribution of each camera; DT-EDNet vs EfficientNet, ResNet18, ConvNeXt V2; severity maps'],
  ['3. Predict white rust at the pre-symptomatic stage', 'Can subplots that will develop white rust be separated from healthy subplots before symptoms, and can later severity be predicted?', '576 pre-symptomatic subplot samples per camera', 'Pre-symptomatic models; earliest detection day; risk maps']], 0.45, 1.25, 12.43, [2.6, 4.0, 2.2, 3.63], { firstCol: true });
// 6 ------------------------------------------------------------------ framework
sec('Research framework');
s = S('Overall research framework', 'Framework', 'Common activities A to F prepare the data once; each objective then has its own activities and steps; validation has two stages.');
chain(s, [{ h: 'A. Field experiment', b: 'design, flights, scoring, ASD, physiology, covariates' }, { h: 'B. Pre-processing', b: 'calibration, mosaics, smoothing, co-registration' }, { h: 'D. Features', b: 'subplot spectra, indices, texture, thermal' },
  { h: 'E. Normalisation', b: 'thermal, healthy-plot, z-score, class weights' }, { h: 'F. Validation design', b: 'LORO folds, nested inner CV, leakage checks' }], 0.45, 1.3, 12.43, 1.45, 0.28, C.blue, C.lblue);
T(s, '**Common activities A–F (once)**', 3.1, 2.85, 3.2, 0.35, { color: C.blue, align: 'center' });
const ob = [['Objective 1', 'Characterisation: response analysis; SHAP-CARS optimal wavelengths; White Rust Index; ReliefF indices; texture and TTFI; VIF; physiological basis', C.g, C.lt],
  ['Objective 2', 'Detection and severity: 15 sensor sets; machine learning; DNN-F1, DNN-F2; DT-EDNet vs EfficientNet, ResNet18, ConvNeXt V2; evaluation, ablation, SHAP, maps', C.purple, C.lpurple],
  ['Objective 3', 'Pre-symptomatic prediction: labels from later status; healthy-plot normalisation; selection; models; earliest detection day; risk maps', C.red, C.lred]];
ob.forEach((o, i) => { const x = 0.45 + i * 4.2; box(s, x, 3.35, 4.03, 1.9, o[0], o[1], o[2], o[3]); arr(s, x + 2.0, 2.78, x + 2.0, 3.33); });
arr(s, 4.48, 4.3, 4.65, 4.3); arr(s, 8.68, 4.3, 8.85, 4.3);
box(s, 0.45, 5.55, 6.1, 0.95, 'Validation stage 1 (internal)', 'IARI field: leave-one-replication-out, nested', C.gold, C.lgold); box(s, 6.78, 5.55, 6.1, 0.95, 'Validation stage 2 (independent)', 'Bharatpur research farms and farmers\' fields; frozen models', C.gold, C.lgold);
arr(s, 6.57, 6.02, 6.76, 6.02);
// 7 ------------------------------------------------------------------ rules
s = S('Eight guiding rules applied to every activity', 'Framework', 'Rules from the methodological literature and from weaknesses of earlier disease-sensing studies.');
const rules = ['One sample = one subplot on one date; the four subplots of a plot always stay together in training or in test.', 'All cameras are measured on the same vegetation pixels of each subplot.',
  'Features are grouped by type; one selection method is used for each type of feature (Objective 1).', 'Every step that uses severity labels (index search, selection, tuning, early stopping) runs inside the training part only.',
  'All normalisation constants (means, standard deviations, healthy references) come from the training part.', 'Every sensor model is compared with a covariate-only model (days after inoculation, variety, timing, stage, weather).',
  'The same folds are used for all sensor sets and models, so accuracies are directly comparable.', 'Two-stage validation: IARI field (nested LORO), then independent Bharatpur data with frozen models.'];
rules.forEach((r, i) => { const col = i % 2, row = Math.floor(i / 2), x = 0.45 + col * 6.3, y = 1.25 + row * 1.25; circ(s, x, y + 0.15, 0.55, String(i + 1), col ? C.blue : C.g); T(s, r, x + 0.7, y + 0.02, 5.4, 1.15, { valign: 'middle' }); });
refline(s, 'Ambroise and McLachlan (2002); Varma and Simon (2006); Cawley and Talbot (2010); Roberts et al. (2017); Ma et al. (2026).', 6.3);
// 8 ------------------------------------------------------------------ A1 design
sec('Data collection');
s = S('Step A1: Experimental design and treatments', 'Data collection', 'Staggered sowing with one inoculation gives four crop ages at inoculation; healthy controls are in a separate block.');
// schematic layout
T(s, '**Field layout (schematic, not to scale)**', 0.45, 1.15, 6.2, 0.35);
s.addShape(pres.shapes.RECTANGLE, { x: 0.45, y: 1.55, w: 6.2, h: 4.75, fill: { color: 'FBFCF9' }, line: { color: '8A9A8C', width: 1 } });
box(s, 0.6, 1.7, 1.25, 4.0, 'Healthy block', 'plots 1–12 (fungicide-protected, uninoculated); 9.4 m', C.g, C.lt, { valign: 'top' });
box(s, 1.95, 1.7, 0.85, 4.0, null, '10 m buffer', C.grey, C.lgrey);
const reps = [['R3', 'plots 13–24'], ['R2', 'plots 25–36'], ['R1', 'plots 37–48']];
reps.forEach((r, i) => { const x = 2.9 + i * 1.22; box(s, x, 1.7, 1.12, 4.0, r[0], r[1], C.red, C.lred, { valign: 'top' }); });
T(s, 'Inoculated block (28.6 m)', 2.9, 5.8, 3.6, 0.35, { align: 'center', italic: true });
BL(s, ['**Site and season:** IARI research farm, New Delhi; rabi 2026-27; field 48 m × 24 m; plots 5 m × 3 m, 0.2 m bunds, 2 m channels.',
  '**Varieties:** V1 = PM 26, V2 = Pusa Vijay, V3 = PM 37.', '**Sowing dates (8-day interval):** D1 = 19 Nov, D2 = 27 Nov, D3 = 5 Dec, D4 = 13 Dec 2026.',
  '**Inoculation:** 10 January 2027, zoosporangial suspension 1.5 × 10⁵ zoosporangia mL⁻¹ (Mishra et al., 2009) → crop age 52, 44, 36 and 28 days after sowing.',
  '**Treatments:** 12 (4 sowing dates × 3 varieties) × 3 replications (R1–R3) inoculated = 36 plots + 12 healthy plots = 48 plots.',
  '**Code** (treatment, replication, plot number) stored with every sample.'], 6.9, 1.2, 6.0, 4.6);
refline(s, 'staggered sowing/inoculation with healthy controls: Guo et al. (2021); Feng et al. (2022); Liu et al. (2024); Tian et al. (2021); Ma et al. (2026).', 6.4, 0.6);
// 9 ------------------------------------------------------------------ A2 cameras
s = S('Step A2: UAV flights and the four cameras', 'Data collection', 'Four cameras on the same day, each recording a different plant response.');
tb(s, [['Camera', 'Sensor', 'Spectral range / bands', 'Ground pixel', 'Plant response recorded'],
  ['Hyperspectral', 'Headwall co-aligned VNIR–SWIR imager', '483 usable bands, 399–2398 nm (after quality control)', '≈ 2.2 cm', 'pigments, red edge, structure, water'],
  ['Multispectral', 'MicaSense RedEdge-MX', '475, 560, 668, 717, 840 nm', '≈ 2 cm', 'chlorophyll, red edge, canopy vigour'],
  ['Red–green–blue', 'DJI camera', 'red, green, blue', '≈ 0.8 cm', 'colour, pustule and canopy texture'],
  ['Thermal', 'FLIR Vue Pro R', '7.5–13.5 µm', '≈ 3.9 cm', 'canopy temperature (transpiration)']], 0.45, 1.25, 12.43, [1.7, 2.9, 3.4, 1.4, 3.03], { firstCol: true });
BL(s, ['**Flight protocol:** 11:00–14:00 h, clear sky, low wind; 30 m above ground; ≈ 85% forward and 80% side overlap.', '**Before every flight:** reflectance calibration panels and ground control points; air temperature and relative humidity recorded during the flight.',
  '**Dates:** 13 flights with all four cameras (3 pre-symptomatic + 10 post-symptomatic); subplots scored and ASD leaf spectra measured on the flight day (or within one day).'], 0.45, 3.2, 12.43, 1.8);
refline(s, 'four-camera fusion: Feng et al. (2022); Maimaitijiang et al. (2020); UAV spectroscopy protocols: Aasen et al. (2018); thermal flights: Messina and Modica (2020).', 6.2, 0.6);
// 10 ------------------------------------------------------------------ timeline
s = S('Data collection timeline, 2026-27', 'Data collection', 'Sowing, inoculation and the 13 flight dates; physiological sampling on four of them.');
const tx0 = 0.7, tx1 = 12.7; line(s, tx0, 3.2, tx1, 3.2, '2C5F2D', 3);
const sow = [['19 Nov', 'D1'], ['27 Nov', 'D2'], ['5 Dec', 'D3'], ['13 Dec', 'D4']];
sow.forEach((d, i) => { const x = 0.75 + i * 0.62; s.addShape(pres.shapes.OVAL, { x: x, y: 3.08, w: 0.24, h: 0.24, fill: { color: C.gold }, line: { color: C.gold } }); T(s, d[1] + '\n' + d[0], x - 0.25, 2.25, 0.75, 0.8, { align: 'center', valign: 'bottom', color: C.gold }); });
T(s, '**Sowing**', 0.75, 1.8, 2.5, 0.35, { color: C.gold });
s.addShape(pres.shapes.OVAL, { x: 3.4, y: 3.03, w: 0.34, h: 0.34, fill: { color: C.red }, line: { color: C.red } }); T(s, '**Inoculation**\n10 Jan', 3.0, 3.45, 1.2, 0.7, { align: 'center', color: C.red });
const fl = [['12 Jan', 2], ['15 Jan', 5], ['18 Jan', 8], ['21 Jan', 11], ['28 Jan', 18], ['4 Feb', 25], ['11 Feb', 32], ['18 Feb', 39], ['25 Feb', 46], ['4 Mar', 53], ['11 Mar', 60], ['18 Mar', 67], ['25 Mar', 74]];
fl.forEach((f, i) => { const x = 4.25 + i * 0.65, pre = i < 3, col = pre ? C.blue : C.purple; s.addShape(pres.shapes.OVAL, { x, y: 3.08, w: 0.24, h: 0.24, fill: { color: col }, line: { color: col } });
  T(s, f[0], x - 0.22, (i % 2 ? 3.4 : 2.4), 0.7, 0.35, { align: 'center', fontSize: FS, color: col }); T(s, f[1] + ' d', x - 0.22, (i % 2 ? 3.72 : 2.72), 0.7, 0.3, { align: 'center', fontSize: FS, color: '555555' });
  if ([2, 4, 7, 10].includes(i)) { s.addShape(pres.shapes.ISOSCELES_TRIANGLE, { x: x + 0.02, y: 4.15, w: 0.2, h: 0.2, fill: { color: C.g }, line: { color: C.g } }); } });
box(s, 4.15, 1.45, 1.95, 0.6, null, 'Pre-symptomatic (3)', C.blue, C.lblue); box(s, 6.3, 1.45, 6.4, 0.6, null, 'Post-symptomatic (10): 11–74 days after inoculation', C.purple, C.lpurple);
BL(s, ['**All 13 dates:** hyperspectral, multispectral, red–green–blue and thermal flights; canopy severity of every subplot; ASD leaf spectra (L3, L5, LL of 3 tagged plants per subplot).',
  '**Green triangles (18 Jan, 28 Jan, 18 Feb, 11 Mar):** biochemical and biophysical parameters (1 pre- and 3 post-symptomatic dates).', '**Numbers below dates:** days after inoculation (d).'], 0.45, 4.6, 12.43, 1.9);
// 11 ------------------------------------------------------------------ A3 + A5
s = S('Steps A3 and A5: Subplots, severity score, labels and datasets', 'Data collection', 'The sampling unit is one subplot on one date; labels come from the canopy severity score.');
T(s, '**Subplots of one plot**', 0.45, 1.15, 3.2, 0.35);
s.addShape(pres.shapes.RECTANGLE, { x: 0.55, y: 1.55, w: 3.0, h: 2.0, fill: { color: 'FFFFFF' }, line: { color: C.g, width: 2 } });
[[0.7, 1.7], [2.1, 1.7], [0.7, 2.6], [2.1, 2.6]].forEach((p, i) => box(s, p[0], p[1], 1.3, 0.8, null, 'Subplot ' + (i + 1), C.g2, C.lt));
T(s, 'Inner buffer excludes border rows; 48 plots × 4 = 192 subplots per image', 0.45, 3.6, 3.3, 0.9, { fontSize: FS });
tb(s, [['Grade (Conn et al., 1990)', '0', '1', '3', '5', '7', '9'], ['Canopy leaf area with pustules', 'no symptoms', '1–5%', '6–10%', '11–25%', '26–50%', '> 50%']], 0.45, 4.75, 12.43, [3.2, 1.6, 1.5, 1.5, 1.55, 1.55, 1.53]);
T(s, '**Plot summary:** percent disease index PDI = Σ grade_i / (n × 9) × 100, with n = 4 subplots per plot', 0.45, 5.65, 12.43, 0.4);
BL(s, ['**Scoring:** one trained scorer grades the canopy of each subplot on the flight day; written grade limits keep scoring consistent (Bock et al., 2010).',
  '**Task A label (detection):** healthy (grade 0) vs diseased (grade > 0), from the observed score, not the treatment.', '**Task B label (severity classes):** grades 0, 1, 3, 5, 7, 9; a grade with < 5% of samples is merged with its neighbour.',
  '**Task C label (severity score):** grade treated as a continuous number (regression).', '**Post-symptomatic dataset:** 10 dates × 192 subplots = 1920 samples per camera (Objectives 1, 2).',
  '**Pre-symptomatic dataset:** 3 dates × 192 = 576 samples per camera (Objective 3); infected = inoculated subplots that show pustules later.'], 3.95, 1.2, 8.93, 3.45);
refline(s, 'Conn et al. (1990); Bock et al. (2010); Tian et al. (2021); Feng et al. (2022); Zhu et al. (2017).', 6.3);
// 12 ------------------------------------------------------------------ A4 ASD
s = S('Step A4: Leaf spectra with the ASD field spectroradiometer', 'Data collection', 'Leaf-level spectra and grades from the same subplots on the same days as the flights (acquisition only).');
chain(s, [{ h: 'Tag plants', b: '3 plants per subplot (12 per plot; 576), before inoculation' }, { h: 'White reference', b: 'Spectralon; every 10–15 min or each plot' }, { h: 'Leaves', b: 'L3, L5 (from top) and lowest green leaf (LL)' },
  { h: 'Readings', b: '3 per leaf (tip, middle, base); 10–25 scans; 350–2500 nm' }, { h: 'Leaf grade + metadata', b: '0–9 key; date, plot, subplot, plant, leaf, operator' }], 0.45, 1.3, 12.43, 1.65, 0.28, C.teal, C.lteal);
BL(s, ['**Instrument:** ASD FieldSpec with plant probe and leaf clip (contact probe with its own light source), so readings do not depend on time of day or sky.',
  '**Dates:** all 13 flight dates, on the flight day or within one day; the same tagged plants on every date (a dead plant replaced by its nearest neighbour and recorded).',
  '**Leaf positions** are recounted on every date because they shift as the plant grows; a missing leaf (senesced LL) is recorded as missing.',
  '**Volume:** 1728 leaves and 5184 readings per date (≈ 22 500 leaves and ≈ 67 000 readings over 13 dates); ≈ 29 operator-hours per date; 3 teams, one replication each.'], 0.45, 3.2, 12.43, 2.9);
refline(s, 'field spectroscopy protocols: Milton et al. (2009); leaf and UAV data together: Calderón et al. (2014), Yu et al. (2021); leaf-to-UAV indices: Huang et al. (2014).', 6.2, 0.6);
// 13 ------------------------------------------------------------------ A8 parameters
s = S('Step A8: Biochemical and biophysical parameters – methods', 'Data collection', 'Eleven parameters on one designated subplot per plot; methods and references.');
tb(s, [['Parameter (unit)', 'Method', 'Reference'],
  ['Chlorophyll a, b (mg g⁻¹ FW)', 'DMSO extraction without grinding (100 mg in 10 mL, 65 °C); absorbance 665, 649 nm', 'Hiscox and Israelstam (1979); Wellburn (1994)'],
  ['Total carotenoids (mg g⁻¹ FW)', 'same DMSO extract; absorbance 480 nm', 'Lichtenthaler and Wellburn (1983); Wellburn (1994)'],
  ['Anthocyanin (µg g⁻¹ FW)', 'pH-differential method: 520 and 700 nm in pH 1.0 and pH 4.5 buffers', 'Lee et al. (2005)'],
  ['Total soluble protein (mg g⁻¹ FW)', 'Bradford dye binding; 595 nm; bovine serum albumin standard', 'Bradford (1976)'],
  ['Relative water content (%)', 'fresh, turgid (4 h floating) and dry weight (48 h, 70 °C)', 'Barrs and Weatherley (1962)'],
  ['Membrane stability index (%)', 'electrolyte leakage: conductivity at 40 °C (C₁) and 100 °C (C₂)', 'Premachandra et al. (1990); Sairam (1994)'],
  ['Photosynthesis, transpiration, stomatal conductance', 'LI-6400 gas exchange: LED 1200 µmol m⁻² s⁻¹, CO₂ 400 µmol mol⁻¹, flow 500 µmol s⁻¹', 'Long and Bernacchi (2003); Riches et al. (2020)'],
  ['Leaf area index (m² m⁻²)', 'plant canopy analyser: 1 reading above, 4 below canopy; view cap; diffuse light', 'Bréda (2003); Goyal et al. (2021)']], 0.45, 1.25, 12.43, [3.1, 5.6, 3.73], { firstCol: true });
// 14 ------------------------------------------------------------------ A8 design and formulas
s = S('Step A8: Sampling design and calculations', 'Data collection', 'When and where the parameters are sampled, and the formulas used.');
BL(s, ['**Dates (all flight days):** 18 Jan 2027 (pre-symptomatic, 8 days after inoculation); 28 Jan, 18 Feb and 11 Mar 2027 (18, 39, 60 days after inoculation).',
  '**Designated subplot:** one per plot, rotated (position = plot number modulo 4, + 1) so that each subplot position is sampled in 12 plots; joined to UAV features and canopy score.',
  '**Gas exchange:** leaf L3 of one tagged plant, 09:30–11:30 h, before the flight (non-destructive).', '**Laboratory samples:** L3 leaves of 3 untagged plants of the designated subplot; cool box; processed the same day.',
  '**Leaf area index:** all four subplots, under diffuse light; BBCH growth stage recorded on every date.', '**Output:** 11 parameters × 48 plots × 4 dates (192 samples per parameter) → Activity 1.7 and Step 3.1.2.'], 0.45, 1.2, 7.0, 5.3);
box(s, 7.7, 1.25, 5.18, 4.9, 'Calculations', ['C_a = 12.47 A665 − 3.62 A649', 'C_b = 25.06 A649 − 6.5 A665', 'C_x+c = (1000 A480 − 1.29 C_a − 53.78 C_b) / 220', '(Wellburn, 1994)', ' ', 'A = (A520 − A700)pH1.0 − (A520 − A700)pH4.5', 'cyanidin-3-glucoside equivalents (Lee et al., 2005)', ' ', 'RWC (%) = (FW − DW) / (TW − DW) × 100', 'MSI (%) = [1 − (C₁ / C₂)] × 100'], C.teal, C.lteal, { valign: 'top' });
// 15 ------------------------------------------------------------------ A6 covariates
s = S('Step A6: Covariates and weather data', 'Data collection', 'Known factors recorded so that their effect can be separated from what the cameras add.');
tb(s, [['Covariate', 'Type and coding', 'Varies between subplots on one date?', 'Main use'],
  ['Days after inoculation (DAI)', 'numeric (flight date − 10 Jan 2027)', 'no', 'time trend; covariate baseline'],
  ['Variety (V1 PM 26, V2 Pusa Vijay, V3 PM 37)', 'categorical, one-hot', 'yes', 'baseline; stratified results; transfer test'],
  ['Inoculation timing (D1–D4)', 'categorical or crop age at inoculation (days)', 'yes', 'baseline; stratified results; transfer test'],
  ['Growth stage (BBCH)', 'ordinal: 1 vegetative (10–59), 2 flowering (60–69), 3 pod formation (70+)', 'yes (staggered sowing)', 'baseline; results by stage; flowering check'],
  ['Weather (Tmax, Tmin, RH I, RH II, rainfall)', '7-day summaries before each flight + favourable days since inoculation', 'no (one value per date)', 'interpretation; baseline (time effect)']], 0.45, 1.25, 12.43, [3.4, 4.0, 2.2, 2.83], { firstCol: true });
BL(s, ['**Favourable day for white rust:** Tmax 16–24 °C, RH I > 97% and RH II > 40% (Chattopadhyay et al., 2011; Saharan et al., 2014).', '**Covariates are not camera features:** they enter only the covariate models and the stratified results; models containing weather are labelled "within-season".'], 0.45, 4.75, 12.43, 1.2);
refline(s, 'BBCH scale: Lancashire et al. (1991); weather with remote sensing: Zhang et al. (2014); stage-dependent signals: Blasch et al. (2023).', 6.15, 0.6);
// 16 ------------------------------------------------------------------ A7 Bharatpur
s = S('Step A7: Second-stage validation data at Bharatpur', 'Data collection', 'Independent data from research farms and farmers\' fields with natural infection.');
chain(s, [{ h: 'Sites', b: 'research-farm plots and farmers\' fields with natural white rust (rabi 2026-27)' }, { h: 'Quadrats', b: '2.5 m × 1.5 m (subplot size); pegs, markers, RTK GNSS' }, { h: 'Flights', b: 'same four cameras and settings; panels and ground control points' },
  { h: 'Ground truth', b: 'same 0–9 key (Conn et al., 1990), same scorer, flight day' }, { h: 'Covariates', b: 'variety, sowing date, BBCH, sprays, nearest weather station' }], 0.45, 1.3, 12.43, 1.75, 0.28, C.gold, C.lgold);
BL(s, ['**Size:** at least 300 quadrat-dates (e.g., 8–10 fields and research-farm plots × 15–20 quadrats × 2–3 post-symptomatic flights in February–March), all grades including healthy.',
  '**Optional:** one flight before symptoms with the same quadrats revisited later (for the pre-symptomatic models).', '**Healthy reference:** a fungicide-protected strip of the main variety at the research farm, where possible.',
  '**Rule:** Bharatpur data are never used for selection, tuning or training; they are used once, for the second-stage validation of the frozen models.'], 0.45, 3.3, 12.43, 2.6);
refline(s, 'independent validation: Ma et al. (2026); Roberts et al. (2017); Ploton et al. (2020); Bharatpur white rust site: Chattopadhyay et al. (2011); transfer of UAV disease models: Yuan et al. (2025).', 6.1, 0.6);
// 17 ------------------------------------------------------------------ Activity B
sec('Common data processing');
s = S('Activity B: Image pre-processing (Steps B1–B5)', 'Data processing', 'Raw images become calibrated, aligned layers on one common grid.');
const bsteps = [['B1 Radiometric calibration', 'Empirical line with panels before/after each flight; downwelling sensor; thermal: emissivity 0.98, air T and RH', 'Smith and Milton (1999); Jones et al. (2009)'],
  ['B2 Orthomosaics', 'Structure-from-motion mosaics (frame cameras); push-broom georectification; same ground control points every date', 'Maimaitijiang et al. (2020)'],
  ['B3 Hyperspectral quality control', 'Remove water-vapour regions (1335–1460, 1785–1965 nm) → 483 bands; Savitzky–Golay (5 bands, order 2) per segment', 'Savitzky and Golay (1964); Thenkabail et al. (2004)'],
  ['B4 Co-registration', 'WGS 84 / UTM 43N; tie points + polynomial warping; check-point RMSE < 1 pixel (2.2 cm)', 'Zitová and Flusser (2003)'],
  ['B5 Resampling to 2.2 cm grid', 'RGB: pixel aggregate; multispectral: bilinear; thermal: nearest neighbour; RGB texture computed before resampling', 'Richards (2013)']];
bsteps.forEach((b, i) => { const x = 0.45 + i * 2.53; box(s, x, 1.3, 2.3, 0.8, null, b[0], C.blue, C.lblue); if (i < 4) arr(s, x + 2.32, 1.7, x + 2.51, 1.7); box(s, x, 2.25, 2.3, 2.75, null, b[1], C.blue, 'FFFFFF', { valign: 'top', align: 'left' }); T(s, b[2], x, 5.1, 2.3, 0.95, { italic: true, align: 'center', color: '3A3A3A' }); });
T(s, 'Output: calibrated, co-registered layers of all four cameras on the hyperspectral grid; plant (vegetation) pixels of each subplot are used for all cameras.', 0.45, 6.15, 12.43, 0.6, { bold: true, color: C.blue });
// 18 ------------------------------------------------------------------ Activity D
s = S('Activity D: Feature extraction (Steps D1–D8)', 'Data processing', 'Features are calculated per subplot-date and kept in groups by type.');
chain(s, [{ h: 'D1 Polygons', b: '192 subplot polygons, inner buffer' }, { h: 'D2 Subplot means', b: 'mean of plant pixels per band; covariates joined' }, { h: 'D3–D4 Spectral', b: 'R, first derivative, red edge; published indices' },
  { h: 'D5–D7 Texture, MS, RGB, thermal', b: 'GLCM; colour indices; temperature' }, { h: 'D8 Feature table', b: 'one row per subplot-date; group prefixes' }], 0.45, 1.25, 12.43, 1.35, 0.25, C.blue, C.lblue);
tb(s, [['Camera', 'Feature groups (before selection)', 'Number'],
  ['Hyperspectral', 'reflectance 483; first derivative 483, FD(λi) = [R(λi+1) − R(λi−1)] / (λi+1 − λi−1); red-edge position, amplitude, area (680–760 nm); ≈ 48 published indices; texture of 3 principal components (24)', '≈ 1040'],
  ['Multispectral', '5 bands; 12 indices (NDVI, GNDVI, NDRE, CIgreen, CIrededge, MTCI, OSAVI, SAVI, TCARI, MCARI, MSR, PSRI); 10 normalised differences; 40 texture', '67'],
  ['Red–green–blue', 'ExG, ExR, ExG − ExR, VARI, GLI, NGRDI; mean hue, saturation, value; 24 texture', '33'],
  ['Thermal', 'mean, median, SD, 10th and 90th percentile temperature; CTD, NRCT, CWSI, healthy difference; 8 texture', '17']], 0.45, 2.8, 12.43, [1.8, 9.4, 1.23], { firstCol: true });
BL(s, ['**GLCM texture:** 32 grey levels, 3 × 3 window, distance 1, four directions; mean, variance, homogeneity, contrast, dissimilarity, entropy, second moment, correlation (Haralick et al., 1973). **No second derivative** (amplifies noise; Rinnan et al., 2009).'], 0.45, 5.75, 12.43, 0.8);
refline(s, 'Tsai and Philpot (1998); Filella and Peñuelas (1994); Mahlein et al. (2013); Hall-Beyer (2017); Guo et al. (2021); Ma et al. (2026).', 6.55, 0.45);
// 19 ------------------------------------------------------------------ Activity E
s = S('Activity E: Normalisation and data preparation (Steps E1–E4)', 'Data processing', 'Removes effects not caused by disease; E2-E4 use training statistics only.');
const es = [['E1 Thermal normalisation', ['CTD = Tc − Tair', 'NRCT = (Tc − Tmin) / (Tmax − Tmin)', 'CWSI = (Tc − Twet) / (Tdry − Twet)'], 'Idso et al. (1981); Jones et al. (2009); Calderón et al. (2014)', C.red, C.lred],
  ['E2 Healthy-plot normalisation', ['z_h = (x − mean_healthy) / SD_healthy', 'healthy plots of the same date and variety in the training part'], 'Oerke et al. (2006); Zarco-Tejada et al. (2018)', C.g, C.lt],
  ['E3 Standardisation (z-score)', ['z = (x − mean_train) / SD_train', 'statistics from the training part of each fold only'], 'Kuhn and Johnson (2013)', C.blue, C.lblue],
  ['E4 Class weights', ['w_c = N / (k × n_c)', 'used in the loss; macro-averaged metrics reported'], 'Johnson and Khoshgoftaar (2019); Sokolova and Lapalme (2009)', C.purple, C.lpurple]];
es.forEach((e, i) => { const x = 0.45 + i * 3.15; box(s, x, 1.3, 2.95, 0.75, null, e[0], e[3], e[4]); box(s, x, 2.2, 2.95, 2.6, null, e[1], e[3], 'FFFFFF'); T(s, e[2], x, 4.9, 2.95, 0.95, { italic: true, align: 'center', color: '3A3A3A' }); if (i < 3) arr(s, x + 2.97, 1.67, x + 3.13, 1.67); });
T(s, 'E1 uses no labels and is run once on all data; E2–E4 are computed on the training part of every fold and applied to its test part. Date-to-date reflectance consistency relies on the panels flown on every date (B1).', 0.45, 5.95, 12.43, 0.8);
// 20 ------------------------------------------------------------------ Activity F
s = S('Activity F: Validation design (LORO and nested tuning)', 'Data processing', 'Outer LORO folds with rotated healthy plots; inner folds grouped by plot; leakage checklist.');
T(s, '**Outer folds (same for all sensor sets, tasks and models)**', 0.45, 1.15, 6.4, 0.35);
const fh = [['Fold 1', 'R1 (37–48)', '7, 2, 10, 12'], ['Fold 2', 'R2 (25–36)', '5, 8, 4, 1'], ['Fold 3', 'R3 (13–24)', '3, 9, 11, 6']];
fh.forEach((f, i) => { const y = 1.6 + i * 0.95; box(s, 0.45, y, 1.1, 0.8, null, f[0], C.grey, C.lgrey); ['R1', 'R2', 'R3'].forEach((r, j) => { const test = j === i; box(s, 1.7 + j * 1.15, y, 1.05, 0.8, null, (test ? 'test ' : 'train ') + r, test ? C.red : C.g, test ? C.lred : C.lt); });
  box(s, 5.2, y, 1.7, 0.8, null, 'healthy test: ' + f[2], C.gold, C.lgold); });
T(s, 'Each test fold has one healthy plot of every inoculation timing and every variety at least once; ≈ 1280 training and ≈ 640 test samples (post-symptomatic).', 0.45, 4.5, 6.45, 1.0);
BL(s, ['**Inner loop:** 3 folds grouped by plot inside the training replications.', '**Inside the inner loop:** index search, SHAP-CARS, ReliefF, mRMR, TTFI search, SFFS, grid search and early stopping.',
  '**Then:** retrain on the whole training part and predict the test replication once.', '**Leakage checklist:** pre-processing and features once on all data (no labels); statistics in the training part; label-based steps in inner folds; Bharatpur only with frozen models.'], 7.15, 1.2, 5.73, 4.4);
refline(s, 'Roberts et al. (2017); Varma and Simon (2006); Cawley and Talbot (2010); Ambroise and McLachlan (2002); Ploton et al. (2020); healthy references: Oerke et al. (2006).', 6.0, 0.6);
module.exports = {};
