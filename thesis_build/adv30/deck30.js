// 30-slide Advisory Committee deck, season 2026-27: introduction, objectives, data acquisition, layout, complete methodology (native flowcharts), expected outcomes.
// No demo data. The user's own field-layout slide (6) and sensor slide (8) are inserted afterwards by adv27_merge.py.
const { pres, F, FS, C, THEME, S, sec, T, BL, box, arr, line, tb, circ, refline } = require('../meth2627/deck/adv_lib.js');
const SZ = { 'g03_survey.png': [1975, 717], 'x02_plot_split.png': [1752, 784] };
const FIG = { 'g03_survey.png': __dirname + '/../meth2627/fig/g03_survey.png', 'x02_plot_split.png': __dirname + '/../explain2627/fig/x02_plot_split.png' };
function img(s, n, x, y, w, hmax) { const [pw, ph] = SZ[n]; let h = w * ph / pw; if (hmax && h > hmax) { h = hmax; w = h * pw / ph; } s.addImage({ path: FIG[n], x, y, w, h }); return [w, h]; }
function nd(s, x, y, w, h, head, body, col = C.g, fill = C.lt, o = {}) { box(s, x, y, w, h, head, body, col, fill, Object.assign({ fs: FS, align: 'center', valign: 'middle' }, o)); }
function A(s, x1, y1, x2, y2) { arr(s, x1, y1, x2, y2, '595959', 1.5); }
function Ln(s, x1, y1, x2, y2) { line(s, x1, y1, x2, y2, '595959', 1.5); }
function hchain(s, items, x, y, w, h, gap, col, fill, o = {}) {
  const n = items.length, bw = (w - gap * (n - 1)) / n;
  items.forEach((it, i) => { const bx = x + i * (bw + gap); nd(s, bx, y, bw, h, it[0], it[1], it[2] || col, it[3] || fill, o); if (i < n - 1) A(s, bx + bw + 0.02, y + h / 2, bx + bw + gap - 0.02, y + h / 2); });
  return bw;
}
function label(s, x, y, w, h, t, col) { s.addShape(pres.shapes.RECTANGLE, { x, y, w, h, fill: { color: col }, line: { color: col } }); s.addText(t, { x, y, w, h, fontFace: F, fontSize: FS, bold: true, color: 'FFFFFF', align: 'center', valign: 'middle', isTextBox: true, margin: 0.04 }); }
let s;

// ================================================================ 1 Title
sec('Introduction');
s = pres.addSlide({ masterName: 'TITLE', sectionTitle: 'Introduction' });
s.addText('AI-based Multimodal UAV Sensing of White Rust in Indian Mustard', { placeholder: 'title' });
s.addText([{ text: 'Objectives, data acquisition and complete methodology – field season 2026-27', options: { breakLine: true, bold: true } }, { text: ' ', options: { breakLine: true } },
  { text: 'Animesh Panda (Roll No. 13098)', options: { breakLine: true } }, { text: 'Ph.D. (Agricultural Physics), ICAR-Indian Agricultural Research Institute, New Delhi', options: { breakLine: true } },
  { text: ' ', options: { breakLine: true } }, { text: 'Advisory Committee Meeting', options: { italic: true } }], { placeholder: 'body' });
s.addNotes('Title. The talk covers the background, the three objectives, how the 2026-27 data are acquired, the field layout, the complete analysis methodology and the expected outcomes.');

// ================================================================ 2 Outline
s = S('Outline of the presentation', 'Introduction', 'Six parts in the order of the talk.');
[['1', 'Introduction', 'white rust, why multimodal UAV sensing, research needs'], ['2', 'Objectives', 'three objectives and their questions'], ['3', 'Data acquisition', 'design, timeline, sensors, flights, ground truth'],
 ['4', 'Field layout', '48 plots, 192 subplots, healthy block'], ['5', 'Methodology', 'pre-processing, split, Objectives 1–3, ASD leaf analysis'], ['6', 'Expected outcomes', 'outputs of each objective and work plan']].forEach((r, i) => {
  const x = 0.45 + i * 2.116; circ(s, x + 0.62, 1.45, 0.7, r[0]);
  nd(s, x, 2.35, 1.85, 1.75, r[1], r[2], C.g, C.lt, { valign: 'middle' });
  if (i < 5) A(s, x + 1.87, 3.22, x + 2.1, 3.22);
});
T(s, 'Season 2026-27: four UAV cameras (hyperspectral, multispectral, RGB, thermal) at subplot level and ASD leaf spectra at leaf level, on the same subplots and dates.', 0.45, 4.6, 12.43, 0.8, { align: 'center', italic: true, color: C.g });

// ================================================================ 3 Background
s = S('Background: white rust of Indian mustard', 'Introduction', 'Why white rust matters and why a sensing approach is needed.');
BL(s, ['**Pathogen:** ~~Albugo candida~~, an obligate oomycete; white pustules on leaves, chlorosis, and distorted inflorescences (staghead) after systemic infection (Saharan et al., 2014).'.replace(/~~/g, ''),
  '**Losses:** yield reduction of 20–60% in Indian mustard (Kumar and Kalha, 2005; Saharan et al., 2014).',
  '**Weather:** infection is favoured by cool, very humid conditions – leaf infection at Tmax 16–24 °C with morning RH > 97% (Chattopadhyay et al., 2011).',
  '**Plant changes:** infected leaves lose pigments and water and change their biochemistry (Mishra et al., 2009).',
  '**Present assessment:** visual scoring – slow, subjective and possible only after symptoms (Bock et al., 2010).'], 0.45, 1.2, 7.5, 5.2);
nd(s, 8.25, 1.35, 4.63, 1.5, 'Need', 'fast, objective, field-wide and early assessment of white rust', C.red, C.lred);
A(s, 10.57, 2.9, 10.57, 3.35);
nd(s, 8.25, 3.4, 4.63, 2.2, 'Approach', 'UAV cameras record pigment, structure, water and temperature changes repeatedly and without touching the crop; combined with machine learning (Mahlein, 2016; Feng et al., 2022)', C.g, C.lt);

// ================================================================ 4 Plant response → camera
s = S('Why multimodal sensing: plant response → camera → feature', 'Introduction', 'Each camera records a different effect of infection; combining them may describe the disease better than one camera.');
[['Plant response', 0.45, 3.6], ['Camera that records it', 4.55, 3.9], ['Features used', 8.95, 3.93]].forEach(r => label(s, r[1], 1.15, r[2], 0.42, r[0], C.g));
[['Pigment loss, chlorosis', 'hyperspectral and multispectral: visible and red edge', 'reflectance bands, red-edge parameters, chlorophyll indices'],
 ['Pustules, uneven canopy', 'RGB, multispectral and hyperspectral images', 'colour indices, GLCM texture, texture fusion index'],
 ['Water loss, tissue damage', 'hyperspectral NIR and SWIR; ASD leaf spectra', 'NIR and SWIR bands, water indices'],
 ['Reduced transpiration', 'thermal camera', 'canopy temperature, CTD, CTR, NRCT']].forEach((r, i) => {
  const y = 1.75 + i * 1.12;
  nd(s, 0.45, y, 3.6, 0.9, null, r[0], C.red, C.lred); A(s, 4.07, y + 0.45, 4.53, y + 0.45);
  nd(s, 4.55, y, 3.9, 0.9, null, r[1], C.blue, C.lblue); A(s, 8.47, y + 0.45, 8.93, y + 0.45);
  nd(s, 8.95, y, 3.93, 0.9, null, r[2], C.g, C.lt);
});
refline(s, 'Mahlein (2016); Feng et al. (2022); Liu et al. (2024); Calderón et al. (2013); Mishra et al. (2009).', 6.35, 0.45);

// ================================================================ 5 Research needs
s = S('Research needs addressed in this study', 'Introduction', 'Each research need leads to one part of the work.');
label(s, 0.45, 1.15, 5.6, 0.42, 'Research need', C.red); label(s, 6.85, 1.15, 6.03, 0.42, 'How this study addresses it', C.g);
[['Which UAV features carry the white rust signal in mustard', 'Objective 1: features of four cameras and ASD leaf spectra; a White Rust Index; disease-specific feature set of each camera'],
 ['Value of each camera and of their combinations', 'Objective 2: all 15 sensor sets with machine learning and deep learning, tested on new plots'],
 ['Detection only after pustules appear', 'Objective 3: prediction 2–8 days after inoculation, labels from the later status'],
 ['Leaf and canopy signals, and the effect of time and weather', 'ASD leaf spectra on the same subplots and dates; covariate-only baseline model']].forEach((r, i) => {
  const y = 1.75 + i * 1.15;
  nd(s, 0.45, y, 5.6, 0.95, null, r[0], C.red, C.lred, { align: 'left' }); A(s, 6.1, y + 0.47, 6.8, y + 0.47);
  nd(s, 6.85, y, 6.03, 0.95, null, r[1], C.g, C.lt, { align: 'left' });
});
refline(s, 'design and models follow Ma et al. (2026); sensor fusion: Feng et al. (2022), Maimaitijiang et al. (2020); pre-symptomatic detection: Tian et al. (2021), Zarco-Tejada et al. (2018).', 6.35, 0.5);

// ================================================================ 6 Objectives
sec('Objectives');
s = S('Objectives', 'Objectives', 'Three objectives; each has its question and its main outputs.');
[['1', 'To characterise white rust of mustard through multimodal sensing from a UAV platform', 'Which wavelengths, indices, texture and thermal features of each camera (and of the leaf spectrum) follow white rust?', 'response curves, optimal wavelengths, White Rust Index, disease-specific feature set of each camera, physiological basis', C.g, C.lt],
 ['2', 'To detect and discriminate disease severity of white rust through AI-based multimodal data fusion', 'Which camera or camera combination and which model detects white rust and grades its severity best on new plots?', 'accuracy of 15 sensor sets and all models, gain over a covariate-only model, severity maps, independent test', C.blue, C.lblue],
 ['3', 'To predict white rust at the pre-symptomatic stage', 'Can subplots that will develop white rust be separated from healthy subplots before pustules appear, and how early?', 'pre-symptomatic models, earliest detection day, risk maps', C.purple, C.lpurple]].forEach((r, i) => {
  const x = 0.45 + i * 4.215; circ(s, x + 1.67, 1.2, 0.65, r[0], r[4]);
  nd(s, x, 2.0, 4.0, 1.45, null, '**' + r[1] + '**', r[4], r[5]);
  nd(s, x, 3.6, 4.0, 1.35, 'Question', r[2], r[4], 'FFFFFF', { valign: 'top' });
  nd(s, x, 5.1, 4.0, 1.4, 'Main outputs', r[3], r[4], 'FFFFFF', { valign: 'top' });
});

// ================================================================ 7 Experimental design
sec('Data acquisition');
s = S('Experimental design and treatments', 'Data acquisition', 'Staggered sowing with one inoculation date gives four crop ages; a separate healthy block gives uninoculated controls of every treatment.');
tb(s, [['Factor', 'Details'], ['Site, season', 'IARI research farm, New Delhi; rabi 2026-27'], ['Varieties (3)', 'V1 = PM 26, V2 = Pusa Vijay, V3 = PM 37'], ['Sowing dates (4)', 'D1 19 Nov, D2 26 Nov, D3 3 Dec, D4 10 Dec 2026'],
  ['Inoculation', '30 Dec 2026; 1.5 × 10⁵ zoosporangia mL⁻¹'], ['Crop age at inoculation', 'D1 41, D2 34, D3 27, D4 20 days'], ['Plot, subplot', '5 m × 3 m; 4 subplots of 2.5 m × 1.5 m']], 0.45, 1.2, 6.6, [2.3, 4.3], { firstCol: true });
nd(s, 7.35, 1.25, 5.53, 0.85, '12 treatments', '4 sowing dates × 3 varieties', C.g, C.lt);
Ln(s, 10.11, 2.1, 10.11, 2.35); Ln(s, 8.75, 2.35, 11.6, 2.35); A(s, 8.75, 2.35, 8.75, 2.6); A(s, 11.6, 2.35, 11.6, 2.6);
nd(s, 7.35, 2.62, 2.75, 1.2, 'Inoculated block', 'R1–R3: 36 plots (plots 13–48)', C.red, C.lred);
nd(s, 10.13, 2.62, 2.75, 1.2, 'Healthy block', '12 plots (1–12), uninoculated', C.blue, C.lblue);
A(s, 8.75, 3.85, 9.9, 4.25); A(s, 11.5, 3.85, 10.35, 4.25);
nd(s, 7.35, 4.3, 5.53, 0.85, '48 plots × 4 subplots', '= 192 subplots (sampling units)', C.g, C.lt);
refline(s, 'inoculum: Mishra et al. (2009); staggered sowing: Chattopadhyay et al. (2011); inoculated and healthy plots for UAV studies: Guo et al. (2021), Liu et al. (2024).', 6.2, 0.5);

// ================================================================ 9 Season timeline (user layout slide inserted before)
s = S('Season timeline: sowing, inoculation and 13 flight dates', 'Data acquisition', 'Three pre-symptomatic flights (2, 5, 8 DAI) and ten weekly post-symptomatic flights; physiology on four dates.');
const d2x = d => 0.85 + d * (11.7 / 116);
Ln(s, 0.75, 3.05, 12.7, 3.05);
[[0, 'D1'], [7, 'D2'], [14, 'D3'], [21, 'D4']].forEach(([d, t]) => { s.addShape(pres.shapes.ISOSCELES_TRIANGLE, { x: d2x(d) - 0.12, y: 3.15, w: 0.24, h: 0.24, fill: { color: C.g2 }, line: { color: C.g2 } }); T(s, t, d2x(d) - 0.3, 3.42, 0.6, 0.3, { align: 'center', fontSize: 12 }); });
s.addShape(pres.shapes.OVAL, { x: d2x(41) - 0.16, y: 2.89, w: 0.32, h: 0.32, fill: { color: C.red }, line: { color: C.red } });
[43, 46, 49].forEach(d => s.addShape(pres.shapes.RECTANGLE, { x: d2x(d) - 0.05, y: 2.3, w: 0.1, h: 0.7, fill: { color: C.gold }, line: { color: C.gold } }));
[53, 60, 67, 74, 81, 88, 95, 102, 109, 116].forEach(d => s.addShape(pres.shapes.RECTANGLE, { x: d2x(d) - 0.05, y: 2.3, w: 0.1, h: 0.7, fill: { color: C.blue }, line: { color: C.blue } }));
[49, 60, 81, 102].forEach(d => s.addShape(pres.shapes.RECTANGLE, { x: d2x(d) - 0.1, y: 1.95, w: 0.2, h: 0.2, fill: { color: C.purple }, line: { color: C.purple } }));
[[0, '19 Nov'], [41, '30 Dec'], [53, '11 Jan'], [81, '8 Feb'], [116, '15 Mar']].forEach(([d, t]) => T(s, t, d2x(d) - 0.45, 3.72, 0.9, 0.3, { align: 'center', fontSize: 12 }));
[[C.g2, 'sowing D1–D4'], [C.red, 'inoculation 30 Dec 2026'], [C.gold, 'pre-symptomatic flights (3)'], [C.blue, 'post-symptomatic flights (10)'], [C.purple, 'physiology (4 dates)']].forEach((r, i) => {
  s.addShape(pres.shapes.RECTANGLE, { x: 0.6 + i * 2.5, y: 1.33, w: 0.22, h: 0.22, fill: { color: r[0] }, line: { color: r[0] } }); T(s, r[1], 0.88 + i * 2.5, 1.25, 2.2, 0.4, { fontSize: 13 });
});
tb(s, [['Date', '1 Jan', '4 Jan', '7 Jan', '11 Jan', '18 Jan', '25 Jan', '1 Feb', '8 Feb', '15 Feb', '22 Feb', '1 Mar', '8 Mar', '15 Mar'],
  ['DAI', '2', '5', '8', '12', '19', '26', '33', '40', '47', '54', '61', '68', '75'], ['Stage', 'pre', 'pre', 'pre', 'post', 'post', 'post', 'post', 'post', 'post', 'post', 'post', 'post', 'post'],
  ['Physiology', '', '', '✓', '', '✓', '', '', '✓', '', '', '✓', '', '']], 0.45, 4.25, 12.43, [1.3, ...Array(13).fill(0.856)], { firstCol: true });
T(s, 'On every flight day: four cameras over the whole field, leaf scoring of 5 plants per subplot and ASD spectra of the centre plant. Bharatpur fields: 2–3 post-symptomatic dates.', 0.45, 6.15, 12.43, 0.7);

// ================================================================ 11 Flight protocol (user sensor slide inserted before)
s = S('UAV flight protocol and the four cameras', 'Data acquisition', 'The same protocol on all 13 dates makes the dates comparable.');
hchain(s, [['Before the flight', 'reflectance panels and ground control points (RTK) placed; panels imaged'], ['Flight', '11:00–14:00 h, clear sky, low wind; 30 m height; about 85% forward and 80% side overlap'],
  ['After the flight', 'panels imaged again; air temperature and humidity of the flight recorded'], ['Same day on the ground', 'leaf scoring (5 plants per subplot) and ASD leaf spectra (centre plant)']], 0.45, 1.25, 12.43, 1.75, 0.3, C.blue, C.lblue, { valign: 'middle' });
tb(s, [['Camera', 'Instrument', 'Spectral information', 'Records'], ['Hyperspectral', 'Headwall Co-Aligned VNIR–SWIR', '400–2500 nm; 483 usable bands after removing water-vapour bands', 'pigments, structure, water'],
  ['Multispectral', 'MicaSense RedEdge-MX', '475, 560, 668, 717, 840 nm', 'red edge, vegetation indices, texture'], ['RGB', 'DJI Phantom', 'red, green, blue', 'colour and texture of pustules'],
  ['Thermal', 'FLIR Vue Pro R', '7.5–13.5 µm', 'canopy temperature']], 0.45, 3.3, 12.43, [1.9, 3.0, 4.7, 2.83], { firstCol: true });
refline(s, 'calibration panels and ground control points every flight: Ma et al. (2026), Liu et al. (2024); air temperature for thermal normalisation: Feng et al. (2022).', 6.15, 0.5);

// ================================================================ 12 Ground truth
s = S('Ground truth: leaf scoring and the disease index (DI)', 'Data acquisition', 'Five plants per subplot (centre and four corners); three leaves per plant; 15 grades give the subplot DI.');
img(s, 'g03_survey.png', 0.45, 1.2, 7.0, 3.0);
T(s, '**DI (%) = Σ(x × f) / (9 × Σf) × 100**', 0.45, 4.45, 7.0, 0.45, { align: 'center' });
T(s, 'x = leaf grade, f = number of leaves with grade x, 9 = highest grade; 15 leaves per subplot (L3, L5 and the lowest green leaf of 5 tagged plants).', 0.45, 4.95, 7.0, 0.9);
tb(s, [['Leaf area with pustules', 'Grade', 'Subplot DI', 'Class'], ['0', '0', '0', '0 healthy'], ['1–5%', '1', '> 0–5', '1 very low'], ['6–10%', '3', '> 5–10', '3 low'], ['11–25%', '5', '> 10–25', '5 moderate'], ['26–50%', '7', '> 25–50', '7 high'], ['> 50%', '9', '> 50', '9 very high']], 7.7, 1.25, 5.18, [1.6, 0.8, 1.2, 1.58]);
refline(s, 'DI formula for white rust: Mishra et al. (2009); centre + four corners and DI as UAV target: Liu et al. (2024); area diagrams: Conn et al. (1990); one trained scorer: Bock et al. (2010).', 6.05, 0.6);

// ================================================================ 13 Other data and sample numbers
s = S('ASD leaf spectra, plant physiology, weather and the number of samples', 'Data acquisition', 'All data carry plot, subplot and date codes so they can be joined; the numbers follow from the design.');
tb(s, [['Data set', 'Content', 'Samples'],
  ['UAV images (4 cameras)', 'subplot mean of every band; 10 post- and 3 pre-symptomatic dates', '1920 and 576 subplot-dates per camera'],
  ['ASD leaf spectra', 'L3, L5, LL of the centre plant; 2 readings per leaf; 350–2500 nm; 13 dates', '576 leaves per date; 7488 leaves'],
  ['Leaf grades', '15 leaves per subplot on 13 dates', '2880 per date; 37 440'],
  ['Plant physiology', 'chlorophyll a, b, carotenoids, anthocyanin, protein, RWC, MSI, photosynthesis, transpiration, stomatal conductance', '48 per parameter and date; 4 dates'],
  ['Weather and covariates', 'Tmax, Tmin, RH I, RH II, rainfall; DAI, variety, sowing date, growth stage, favourable days', 'one row per sample'],
  ['Bharatpur and glasshouse', 'farm and farmer fields with natural infection; pot experiment with the same treatments', '≥ 300 quadrat-dates; 48 pots']], 0.45, 1.2, 12.43, [2.6, 6.6, 3.23], { firstCol: true });
refline(s, 'leaf clip spectra of graded leaves: Tian et al. (2021), Chen et al. (2023); physiology with spectra: Calderón et al. (2013), Yu et al. (2025); favourable days: Chattopadhyay et al. (2011).', 6.15, 0.5);

// ================================================================ 14 Overall methodology flowchart
sec('Methodology');
s = S('Complete methodology: overall flowchart', 'Methodology', 'Common steps are done once; Objective 1 chooses the features used by Objectives 2 and 3; the ASD leaf analysis runs in parallel with the same split.');
hchain(s, [['Field data', 'images, scores, ASD, physiology, weather'], ['Image processing', 'calibration → ROI means'], ['Features', 'each camera: bands, indices, texture, thermal'],
  ['Labels', 'DI, DI class, healthy/diseased, covariates'], ['7:3 split by plots', '33 training / 15 test plots'], ['Normalisation', 'and leakage rules']], 0.45, 1.2, 12.43, 1.2, 0.2, C.g, C.lt);
label(s, 0.45, 2.65, 12.43, 0.42, 'Everything is learned on the 33 training plots; the 15 test plots are used once, at the end', C.gold);
A(s, 6.66, 2.42, 6.66, 2.63);
const cx = [0.45, 3.58, 6.71, 9.84], cw = 3.04;
[['Objective 1 – characterisation', ['description on all plots: curves, correlation, strata', 'feature selection per camera on training plots', 'VIF → disease-specific feature set (DSF)', 'physiological basis'], C.g, C.lt],
 ['Objective 2 – detection and severity', ['15 sensor sets (feature-level fusion)', 'ML: SVM, RF, k-NN, PLS with SFFS', 'DNN-F1, DNN-F2, DT-EDNet and comparisons', 'test once; comparison; covariate baseline; maps'], C.blue, C.lblue],
 ['Objective 3 – pre-symptomatic', ['labels from later status', 'healthy-baseline normalisation', 'per-camera selection; models', 'earliest detection day; risk maps'], C.purple, C.lpurple],
 ['ASD leaf analysis (Part L)', ['leaf table; same plot split', 'smoothing, indices', 'description and selection', 'leaf models; leaf–canopy link'], C.teal, C.lteal]].forEach((c, i) => {
  A(s, cx[i] + cw / 2, 3.08, cx[i] + cw / 2, 3.28);
  box(s, cx[i], 3.3, cw, 2.55, c[0], c[1].map(t => '• ' + t), c[2], c[3], { fs: FS, align: 'left', valign: 'top' });
});
nd(s, 0.45, 6.05, 12.43, 0.7, null, '**Independent testing:** frozen models applied once to Bharatpur research-farm and farmer fields → maps and conclusions', C.gold, C.lgold);

// ================================================================ 15 Image processing
s = S('Pre-processing: from raw images to subplot values', 'Methodology', 'Six steps in a fixed order; each needs the output of the one before.');
const ip = [['1 Radiometric calibration', 'HS and MS: empirical line with panels, downwelling light sensor; RGB fixed exposure; thermal: radiance → temperature (emissivity 0.98)'],
  ['2 Mosaics and georeferencing', 'structure-from-motion mosaics (MS, RGB, thermal); HS lines georectified with GNSS/IMU; same GCPs on all dates'],
  ['3 Hyperspectral cleaning', 'remove 1335–1460 and 1785–1965 nm and noisy ends → 483 bands; Savitzky–Golay smoothing (5 bands, order 2)'],
  ['4 Co-registration', 'WGS 84 / UTM 43N; RGB, MS and thermal registered to the HS image; check-point error below one HS pixel'],
  ['5 One common grid', 'RGB texture first at native resolution; RGB aggregated, MS bilinear, thermal nearest neighbour'],
  ['6 Subplot ROI means', 'one ROI inside the inner buffer of each subplot; same ROIs on all dates and cameras; mean of every band']];
ip.forEach((r, i) => { const row = Math.floor(i / 3), col = row === 0 ? i : 5 - i; const x = 0.45 + col * 4.32, y = 1.25 + row * 2.3;
  nd(s, x, y, 3.8, 1.85, r[0], r[1], row ? C.teal : C.g, row ? C.lteal : C.lt, { valign: 'top' });
});
A(s, 4.27, 2.17, 4.75, 2.17); A(s, 8.59, 2.17, 9.07, 2.17); A(s, 10.97, 3.12, 10.97, 3.53); A(s, 9.07, 4.47, 8.59, 4.47); A(s, 4.75, 4.47, 4.27, 4.47);
A(s, 2.35, 5.42, 2.35, 5.72);
nd(s, 0.45, 5.75, 12.43, 0.65, null, '**Output:** one table per camera – one row per subplot and date with the mean of every band (and temperature); ROI pixels kept for texture', C.gold, C.lgold);
refline(s, 'water bands: Mandal et al. (2023); Savitzky–Golay (5, 2): Chen et al. (2023); ROI means: Ma et al. (2026), Liu et al. (2024).', 6.5, 0.4);

// ================================================================ 16 Features
s = S('Feature extraction for each camera', 'Methodology', 'Candidate features of each camera before selection; formulas use no labels, so they are computed for every sample.');
[['Hyperspectral', [['reflectance', '483'], ['first derivative', '483'], ['red-edge parameters', '3'], ['published indices', '48'], ['PCA texture (GLCM)', '24']], '≈ 1040', C.g, C.lt],
 ['Multispectral', [['band reflectance', '5'], ['vegetation indices', '12'], ['two-band normalised differences', '10'], ['GLCM texture of 5 bands', '40']], '67', C.blue, C.lblue],
 ['RGB', [['colour indices', '6'], ['hue, saturation, value', '3'], ['GLCM texture of R, G, B', '24']], '33', C.purple, C.lpurple],
 ['Thermal', [['temperature statistics incl. MTD', '6'], ['CTD, CTR, NRCT, ΔT', '4'], ['GLCM texture', '8']], '18', C.red, C.lred]].forEach((c, i) => {
  const x = 0.45 + i * 3.18, w = 2.95;
  label(s, x, 1.2, w, 0.5, c[0], c[3]);
  c[1].forEach((g, k) => { nd(s, x, 1.85 + k * 0.72, w, 0.6, null, g[0] + ' (' + g[1] + ')', c[3], c[4]); });
  nd(s, x, 5.55, w, 0.55, null, '**' + c[2] + ' features**', c[3], 'FFFFFF');
  A(s, x + w / 2, 1.85 + c[1].length * 0.72 - 0.1, x + w / 2, 5.53);
});
refline(s, 'HS texture: Ma et al. (2026); MS indices and texture: Liu et al. (2024), Nguyen et al. (2023); RGB texture and thermal parameters: Feng et al. (2022); GLCM: Haralick et al. (1973).', 6.3, 0.5);

// ================================================================ 17 Split
s = S('Data split: 7:3 by whole plots and validation inside the training plots', 'Methodology', 'Whole plots stay together; the test plots are fixed before the first flight and predicted once.');
nd(s, 0.45, 1.85, 2.5, 1.25, 'All 48 plots', '192 subplots; 13 dates; 7488 leaves', C.grey, C.lgrey);
nd(s, 3.4, 1.2, 3.1, 1.1, '33 training plots', '8 healthy + 25 inoculated; learn everything', C.g, C.lt);
nd(s, 3.4, 2.75, 3.1, 1.1, '15 test plots', '4 healthy + 11 inoculated; used once', C.gold, C.lgold);
A(s, 2.97, 2.3, 3.38, 1.75); A(s, 2.97, 2.65, 3.38, 3.3);
nd(s, 6.95, 1.15, 5.93, 0.72, null, '**Machine learning – GroupKFold(3):** 3 rounds of 22 fitting / 11 scoring plots', C.g, C.lt);
nd(s, 6.95, 1.95, 5.93, 0.72, null, '**Networks:** fit on 22 plots; stop on plots 6, 7, 11, 19, 24, 26, 28, 30, 36, 39, 41', C.g, C.lt);
nd(s, 6.95, 2.82, 5.93, 1.05, null, '**Test plots:** 1, 4, 5, 8, 13, 14, 18, 25, 27, 31, 35, 37, 44, 46, 48 – predicted once after all models are frozen', C.gold, C.lgold);
A(s, 6.52, 1.6, 6.93, 1.5); A(s, 6.52, 1.9, 6.93, 2.3); A(s, 6.52, 3.3, 6.93, 3.33);
tb(s, [['Data set', 'All', 'Training (network fit / validation)', 'Test'], ['UAV post-symptomatic, per camera', '1920', '1320 (880 / 440)', '600'], ['UAV pre-symptomatic, per camera', '576', '396 (264 / 132)', '180'], ['ASD leaves', '7488', '5148 (3432 / 1716)', '2340']], 0.45, 4.15, 12.43, [4.0, 1.4, 4.6, 2.43], { firstCol: true });
refline(s, '7:3 split and validation set: Ma et al. (2026); 70:30: Bijlwan et al. (2025), Maimaitijiang et al. (2020); cross-validation inside training: Tian et al. (2021), Lv et al. (2023); grouped division: Roberts et al. (2017).', 6.0, 0.6);

// ================================================================ 18 Normalisation and leakage
s = S('Normalisation and leakage control', 'Methodology', 'No scaling at the start; every constant comes from the training plots (or the fitting part of a fold).');
tb(s, [['Stage', 'What is normalised and how', 'Constants from'], ['Pre-processing', 'reflectance from panels; mean of ROI pixels', 'panels of each flight'], ['Thermal', 'CTD = Tc − Ta; CTR = Tc/Ta; NRCT within the date; ΔT to healthy plots', 'air temperature; image of the date; healthy training plots'],
  ['Feature selection', 'min–max 0–1 inside ReliefF; z-score before PLS/CARS', 'training plots'], ['Models', 'z-score in the model pipeline (random forest unscaled)', 'fitting part of each fold; then 33 training plots'],
  ['Pre-symptomatic', 'spectrum × healthy baseline / healthy mean of the date', 'healthy training plots']], 0.45, 1.2, 12.43, [2.3, 6.2, 3.93], { firstCol: true });
[['No plot on both sides', 'of any division'], ['Learn only from training plots', 'features, constants, settings, weights'], ['Freeze, then test once', 'test plots predicted only at the end']].forEach((r, i) => nd(s, 0.45 + i * 4.215, 3.85, 4.0, 1.05, r[0], r[1], C.red, C.lred));
refline(s, 'thermal: Feng et al. (2022), Calderón et al. (2014), Oerke et al. (2006); z-score in the training part: Bijlwan et al. (2025), Shafiee et al. (2021); healthy baseline: Lv et al. (2023).', 5.2, 0.6);

// ================================================================ 19 Objective 1 flowchart
s = S('Objective 1: characterisation – flowchart', 'Objective 1', 'Description uses all plots because nothing from it enters a model; feature selection uses only the training plots and its result is used unchanged by Objectives 2 and 3.');
label(s, 0.45, 1.3, 1.6, 1.05, 'Description\n(all 48 plots)', C.teal);
hchain(s, [['1.1.1', 'mean spectra by DI class'], ['1.1.2', 'correlation with DI'], ['1.1.3', 'by stage, variety, weather'], ['1.7', 'physiological basis']], 2.25, 1.3, 10.63, 1.05, 0.25, C.teal, C.lteal);
label(s, 0.45, 2.85, 1.6, 1.25, 'Selection\n(33 training plots)', C.g);
hchain(s, [['1.2', 'maps → optimal wavelengths'], ['1.3', 'best NDSI, RSI; WRI'], ['1.4', 'filter + ReliefF indices'], ['1.5', 'mRMR texture; TTFI'], ['1.6', 'per camera → VIF']], 2.25, 2.85, 10.63, 1.25, 0.22, C.g, C.lt);
Ln(s, 11.9, 4.12, 11.9, 4.28); Ln(s, 11.9, 4.28, 5.55, 4.28); A(s, 5.55, 4.28, 5.55, 4.43);
nd(s, 2.25, 4.45, 6.6, 1.05, null, '**Disease-specific feature set (DSF) of each camera and task** – fixed; input of Objectives 2 and 3', C.gold, C.lgold);
nd(s, 9.1, 4.45, 3.78, 1.05, null, '1.6.6 stability by stage; 1.6.7 complementarity; 1.8 pre-symptomatic', C.teal, C.lteal);
refline(s, 'response analysis: Ma et al. (2026), Mandal et al. (2023), Zhang et al. (2012); one selection method per feature group: Ma et al. (2026); physiology: Calderón et al. (2013), Tian et al. (2021).', 5.8, 0.6);

// ================================================================ 20 Per-camera selection flowchart
s = S('Objective 1: feature selection for each camera separately', 'Objective 1', 'Inside each camera, each feature type has its own selector; the survivors are thinned by VIF into the DSF of that camera.');
const lanes = [['Hyperspectral', C.g, C.lt, [['bands R + FD (966)', 'maps → SHAP → CARS', 'OW 10–15'], ['indices 48 + 3 RE + NDSI, RSI, WRI', '|r| ≥ 0.95 → ReliefF', 'VI 5'], ['PCA texture (24)', '|r| ≥ 0.95 → mRMR → TTFI', '6 + TTFI']]],
  ['Multispectral', C.blue, C.lblue, [['5 bands + 12 indices + best ND', '|r| ≥ 0.95 → ReliefF', '5'], ['GLCM of 5 bands (40)', '|r| ≥ 0.95 → mRMR → TTFI', '6 + TTFI']]],
  ['RGB', C.purple, C.lpurple, [['colour indices + H, S, V (9)', '|r| ≥ 0.95 → ReliefF', '5'], ['GLCM of R, G, B (24)', '|r| ≥ 0.95 → mRMR → TTFI', '6 + TTFI']]],
  ['Thermal', C.red, C.lred, [['statistics, normalised, texture (18)', '|r| ≥ 0.95 → ReliefF; normalised kept', '5 + 4']]]];
let yy = 1.2; const lh = 0.46, lg = 0.08;
lanes.forEach(([name, col, fill, rows]) => {
  const top = yy, hgt = rows.length * lh + (rows.length - 1) * lg;
  label(s, 0.45, top, 1.6, hgt, name, col);
  rows.forEach((r, k) => { const y = top + k * (lh + lg);
    nd(s, 2.2, y, 3.6, lh, null, r[0], col, fill, { fs: 13 }); A(s, 5.82, y + lh / 2, 6.0, y + lh / 2);
    nd(s, 6.02, y, 3.35, lh, null, r[1], col, 'FFFFFF', { fs: 13 }); A(s, 9.39, y + lh / 2, 9.57, y + lh / 2);
    nd(s, 9.59, y, 1.25, lh, null, r[2], col, fill, { fs: 13 }); A(s, 10.86, y + lh / 2, 11.08, top + hgt / 2);
  });
  nd(s, 11.1, top, 1.78, hgt, null, 'VIF < 10 → DSF', col, fill, { fs: 13 });
  yy = top + hgt + 0.16;
});
refline(s, 'selection within each sensor, VIF, then fusion: Mustafa et al. (2023); SHAP-CARS, Relief, mRMR, TTFI: Ma et al. (2026); MS three-texture indices: Liu et al. (2024); colour and texture screened separately: Huang et al. (2020); thermal: Feng et al. (2022).', 5.95, 0.7);

// ================================================================ 21 HS selection details
s = S('Objective 1: hyperspectral selection steps and formulas', 'Objective 1', 'The same order for bands, indices and texture; formulas fixed on the training plots and then computed for every sample.');
[['Bands', C.g, C.lt, [['Band-pair maps', 'NDSI = (Ri − Rj)/(Ri + Rj); RSI = Ri/Rj; R² > 0.5 → effective ranges'], ['SHAP', 'random forest (500 trees); mean |SHAP|; top 40%'], ['CARS', 'PLS; 50 iterations; lowest GroupKFold(3) RMSE'], ['Optimal wavelengths', '10–15 bands']]],
 ['Indices', C.blue, C.lblue, [['Data-driven indices', 'best NDSI, RSI; WRI = ND(λ1, λ2) + w·R(λ3); λ1, λ2 ≥ 50 nm'], ['Redundancy filter', 'clusters at |r| ≥ 0.95; keep best with DI'], ['ReliefF / RReliefF', 'k = 10; min–max scaled'], ['Selected indices', 'top 5 per task']]],
 ['Texture', C.purple, C.lpurple, [['GLCM of 3 PCs', '3 × 3, distance 1, 4 directions, 64 levels: 24 features'], ['Redundancy filter', '|r| ≥ 0.95'], ['mRMR', 'relevance minus redundancy'], ['TF1–TF6 + TTFI', '120 triplets × 3 formulas']]]].forEach(([name, col, fill, items], i) => {
  const y = 1.25 + i * 1.45; label(s, 0.45, y, 1.4, 1.2, name, col);
  hchain(s, items, 2.0, y, 10.88, 1.2, 0.22, col, fill, { fs: 13 });
});
nd(s, 0.45, 5.6, 12.43, 0.6, null, '**VIF_j = 1 / (1 − R_j²)** – remove the largest until all VIF < 10 → disease-specific feature set', C.gold, C.lgold);
refline(s, 'maps and SHAP-CARS: Ma et al. (2026); WRI form, 50-nm rule, weights: Mahlein et al. (2013); ReliefF: Robnik-Šikonja and Kononenko (2003); mRMR: Peng et al. (2005); CARS: Li et al. (2009); VIF < 10: Lv et al. (2023).', 6.3, 0.6);

// ================================================================ 22 Physiology and pre-symptomatic characterisation
s = S('Objective 1: physiological basis and pre-symptomatic characterisation', 'Objective 1', 'Physiology explains why features respond; the pre-symptomatic characterisation prepares Objective 3.');
const vflow = (x, head, col, fill, items) => { label(s, x, 1.2, 6.0, 0.45, head, col); items.forEach((t, k) => { const y = 1.8 + k * 0.85; nd(s, x, y, 6.0, 0.65, null, t, col, fill); if (k < items.length - 1) A(s, x + 3.0, y + 0.66, x + 3.0, y + 0.83); }); };
vflow(0.45, '1.7 Physiological basis (4 dates)', C.teal, C.lteal, ['10 parameters on one designated subplot per plot', 'outliers beyond median ± 3 SD checked', 'paired t-test inoculated vs healthy (Wilcoxon if not normal)', 'two-way ANOVA: variety × sowing date', 'correlation with DI and with the selected features']);
vflow(6.88, '1.8 Pre-symptomatic characterisation (2, 5, 8 DAI)', C.purple, C.lpurple, ['labels: healthy plots vs subplots infected later', 'healthy-baseline normalisation of spectra', 't-test of plot means per feature and date', 'per-camera selection with the binary label', 'earliest responding feature of each camera']);
refline(s, 'Tian et al. (2021); Calderón et al. (2013); Mishra et al. (2009); Zhu et al. (2017); Lv et al. (2023); Mahlein et al. (2019).', 6.2, 0.45);

// ================================================================ 23 Objective 2 flowchart
s = S('Objective 2: detection and severity – flowchart', 'Objective 2', 'Every sensor set and every model uses the same training and test plots; the test plots are predicted once.');
hchain(s, [['DSF of 4 cameras', 'from Objective 1'], ['15 sensor sets', '4 single, 6 pairs, 4 triplets, 1 all'], ['Feature-level fusion', 'join DSFs; VIF < 10 again']], 0.45, 1.2, 12.43, 0.95, 0.35, C.blue, C.lblue);
Ln(s, 10.93, 2.17, 10.93, 2.35); Ln(s, 0.3, 2.35, 10.93, 2.35); Ln(s, 0.3, 2.35, 0.3, 4.3); A(s, 0.3, 3.1, 0.43, 3.1); A(s, 0.3, 4.3, 0.43, 4.3);
label(s, 0.45, 2.6, 1.5, 1.0, 'Machine learning', C.g);
hchain(s, [['SVM/SVR, RF, k-NN, PLS-DA/PLSR', 'Tasks A, B, C'], ['SFFS', '≤ 15 features, GroupKFold(3)'], ['Grid search', 'same folds'], ['Refit', '33 training plots → frozen']], 2.1, 2.6, 10.78, 1.0, 0.25, C.g, C.lt, { fs: 13 });
label(s, 0.45, 3.8, 1.5, 1.0, 'Deep learning', C.purple);
hchain(s, [['DNN-F1, DNN-F2', '15 sets; 11 fused sets'], ['DT-EDNet + 3 networks', 'pseudo-image; Tasks A, B'], ['Training', 'fit 22 plots; stop on 11'], ['Best epoch', '→ frozen']], 2.1, 3.8, 10.78, 1.0, 0.25, C.purple, C.lpurple, { fs: 13 });
Ln(s, 12.88, 3.1, 13.05, 3.1); Ln(s, 13.05, 3.1, 13.05, 5.25); Ln(s, 12.88, 4.3, 13.05, 4.3); A(s, 13.05, 5.25, 12.9, 5.25);
nd(s, 0.45, 5.0, 12.43, 0.9, null, '**Test plots predicted once → metrics** → ranking, fusion gain, drop-one-camera ablation, SHAP → covariate baseline → maps → Bharatpur test', C.gold, C.lgold);
refline(s, 'every sensor and combination, DNN-F1/DNN-F2: Maimaitijiang et al. (2020); SFFS: Tian et al. (2021), Mustafa et al. (2023); DT-EDNet and comparisons: Ma et al. (2026); multimodal networks: Deng et al. (2024), Yu et al. (2025).', 6.05, 0.6);

// ================================================================ 24 Models and settings
s = S('Objective 2: models and settings', 'Objective 2', 'Settings chosen on the training plots only; identical network settings for all networks.');
tb(s, [['Model', 'Grid search (GroupKFold(3))'], ['SVM / SVR (RBF)', 'C 0.1–100; γ 0.001–0.1, scale; ε 0.1, 0.5'], ['Random forest', '500 trees; max_features sqrt, 0.3; leaf 1, 3, 5'], ['k-NN', 'k 3–11; uniform or distance'], ['PLS-DA / PLSR', '1–15 components']], 0.45, 1.2, 6.3, [2.2, 4.1], { firstCol: true });
tb(s, [['Network setting', 'Value'], ['Optimiser', 'AdamW 6 × 10⁻⁴, weight decay 10⁻⁵'], ['Schedule, epochs', 'cosine to 10⁻⁶; 300; patience 60'], ['Batch, smoothing, clipping', '32; 0.01; 1.2'], ['Validation', '11 of the 33 training plots'], ['Model kept', 'highest validation accuracy']], 6.98, 1.2, 5.9, [2.6, 3.3], { firstCol: true });
nd(s, 0.45, 3.55, 12.43, 1.0, null, '**Number of frozen models:** 4 ML models × 15 sets × 3 tasks = 180; DNN-F1 45; DNN-F2 33; DT-EDNet and three comparison networks on the hyperspectral configurations and all sensor sets (Tasks A, B)', C.blue, C.lblue);
refline(s, 'grid search: Tian et al. (2021), Chen et al. (2023), Bijlwan et al. (2025); network settings: Ma et al. (2026).', 4.8, 0.45);

// ================================================================ 25 Evaluation and covariate baseline
s = S('Objective 2: evaluation, comparison and covariate baseline', 'Objective 2', 'Metrics on the 15 test plots; the cameras are credited only with what they add to time, crop and weather.');
tb(s, [['Task', 'Metrics on the test plots'], ['A healthy vs diseased', 'OA, kappa, macro-F1, sensitivity, specificity, AUC'], ['B DI class', 'OA, kappa, macro-F1, per-class F1, accuracy within one class, weighted kappa'], ['C DI (%)', 'R², RMSE, RPD'], ['Low severity', 'recall for DI ≤ 5; RMSE for DI ≤ 10']], 0.45, 1.2, 6.6, [2.0, 4.6], { firstCol: true });
nd(s, 7.3, 1.2, 5.58, 0.85, 'M0 – covariates only', 'DAI, variety, sowing date, stage, weather', C.grey, C.lgrey);
nd(s, 7.3, 2.45, 5.58, 0.85, 'M1 – sensors only', 'best sensor set and model', C.blue, C.lblue);
nd(s, 7.3, 3.7, 5.58, 0.85, 'M2 – sensors + covariates', 'same model type as M1', C.g, C.lt);
A(s, 10.09, 2.07, 10.09, 2.43); A(s, 10.09, 3.32, 10.09, 3.68);
T(s, 'ΔS = M1 − M0', 10.25, 2.05, 2.5, 0.4, { bold: true, color: C.blue }); T(s, 'ΔC = M2 − M1', 10.25, 3.3, 2.5, 0.4, { bold: true, color: C.g });
BL(s, ['**Comparison:** ranking of sensor sets and models; fusion gain = fused set − best single camera in it; drop-one-camera ablation; SHAP.'], 0.45, 4.8, 12.43, 0.8);
refline(s, 'metrics: Ma et al. (2026), Cross et al. (2024), Mandal et al. (2023); covariate baseline: Zhang et al. (2014a), Bijlwan et al. (2025), Ruan et al. (2022); fusion gain: Feng et al. (2022), Deng et al. (2024); two sensors can beat three: Mahlein et al. (2019).', 5.7, 0.7);

// ================================================================ 26 Objective 3 flowchart
sec('Objective 3 and ASD');
s = S('Objective 3: pre-symptomatic prediction – flowchart', 'Objective 3', '576 pre-symptomatic subplot-dates per camera (2, 5, 8 DAI): at most 396 training and 180 test samples.');
hchain(s, [['Labels', 'healthy plots vs subplots that show pustules later'], ['Normalisation', 'healthy baseline of each date and variety'], ['Description', 't-test of plot means per date'], ['Selection', 'per camera, binary label, training plots']], 0.45, 1.3, 12.43, 1.45, 0.3, C.purple, C.lpurple);
A(s, 11.35, 2.77, 11.35, 3.25);
const r2 = [['Fusion', '15 sensor sets; VIF < 10'], ['Models', 'SVM, RF, k-NN, PLS-DA (SFFS ≤ 10); DNN-F1, DNN-F2'], ['Test once', 'metrics for 2, 5 and 8 DAI'], ['Outputs', 'earliest detection day; earliest features; risk maps']];
const bw2 = (12.43 - 0.9) / 4; r2.forEach((it, i) => { const x = 0.45 + (3 - i) * (bw2 + 0.3); nd(s, x, 3.3, bw2, 1.45, it[0], it[1], C.red, C.lred); if (i < 3) A(s, x - 0.02, 4.02, x - 0.28, 4.02); });
refline(s, 'labels from later status: Zhu et al. (2017), Tian et al. (2021); healthy-baseline normalisation: Lv et al. (2023); earliest day per sensor: Mahlein et al. (2019); accuracy per day: Gold et al. (2020); risk maps: Zarco-Tejada et al. (2018).', 5.2, 0.6);

// ================================================================ 27 ASD leaf analysis flowchart
s = S('ASD leaf analysis (Part L) – flowchart', 'ASD', '7488 leaves of the centre plants: 5148 training and 2340 test leaves, divided by plot like the UAV data.');
hchain(s, [['L1 Leaf table', 'grades joined; 2 readings averaged; outliers checked'], ['L2 Same split', 'plot split of the UAV data'], ['L3 Pre-processing', 'Savitzky–Golay (11, 2); 400–2400 nm; derivative'], ['L4 Indices', '48 indices; red-edge parameters'], ['L5 Description', 'all leaves: spectra by grade, PCA']], 0.45, 1.3, 12.43, 1.45, 0.25, C.teal, C.lteal, { fs: 13 });
A(s, 11.85, 2.77, 11.85, 3.25);
const r3 = [['L5 Selection', 'training leaves: maps, SHAP-CARS, WRI, ReliefF, VIF'], ['L6 Leaf models', 'ML with SFFS; DNN-F1; networks'], ['L7 Test leaves', 'all metrics, once'], ['L8 Covariates', 'M0, M1, M2'], ['L9–L10', 'leaf–canopy link; pre-symptomatic leaves']];
const bw3 = (12.43 - 1.0) / 5; r3.forEach((it, i) => { const x = 0.45 + (4 - i) * (bw3 + 0.25); nd(s, x, 3.3, bw3, 1.45, it[0], it[1], C.g, C.lt, { fs: 13 }); if (i < 4) A(s, x - 0.02, 4.02, x - 0.23, 4.02); });
refline(s, 'leaf spectra and grades: Chen et al. (2023), Tian et al. (2021); pre-processing and leaf indices: Selvaprakash et al. (2026); selection: Ma et al. (2026), Lv et al. (2023); leaf–canopy link: Liu et al. (2026), Bohnenkamp et al. (2019).', 5.2, 0.6);

// ================================================================ 28 Expected outcomes
sec('Expected outcomes');
s = S('Expected outcomes', 'Expected outcomes', 'What each objective will deliver at the end of the 2026-27 analysis.');
[['Objective 1', ['response of each camera to white rust severity', 'optimal wavelengths and a White Rust Index', 'disease-specific feature set of each camera', 'physiological explanation of the selected features'], C.g, C.lt],
 ['Objective 2', ['best camera and camera combination for detection and severity', 'performance of ML and deep-learning models on new plots', 'gain of the cameras over weather and crop information', 'severity maps; test at Bharatpur'], C.blue, C.lblue],
 ['Objective 3', ['earliest day on which white rust can be predicted', 'camera and features that respond first', 'pre-symptomatic risk maps'], C.purple, C.lpurple],
 ['ASD leaf level', ['leaf-level disease features and models', 'link between leaf and canopy signals'], C.teal, C.lteal]].forEach((c, i) => {
  const x = 0.45 + i * 3.18; box(s, x, 1.25, 2.95, 3.4, c[0], c[1].map(t => '• ' + t), c[2], c[3], { fs: FS, align: 'left', valign: 'top' });
});
nd(s, 0.45, 4.9, 12.43, 0.7, null, '**Overall:** a tested, field-validated protocol for UAV-based detection and early warning of white rust in Indian mustard', C.gold, C.lgold);

// ================================================================ 29 Work plan
s = S('Work plan for the 2026-27 data', 'Expected outcomes', 'Field season November 2026 – March 2027, followed by six months of analysis.');
const cols = ['Activity', 'Nov–Dec 2026', 'Jan–Mar 2027', 'Month 1', 'Month 2', 'Month 3', 'Month 4', 'Month 5', 'Month 6'];
const plan = [['Field experiment, flights, scoring, ASD, physiology', [1, 2]], ['Image processing, ROI means, leaf table', [2, 3]], ['Features, split, folds; response analysis', [4]], ['Objective 1 selection; physiology statistics; leaf Objective 1', [5]],
  ['Objective 2: ML and DNN-F1, 15 sensor sets; leaf models', [6]], ['Objective 2: networks, ablation, SHAP, covariate baseline, maps', [7]], ['Objective 3; Bharatpur test; thesis writing', [8]]];
const head = cols.map(c => ({ text: c, options: { bold: true, color: 'FFFFFF', fill: { color: C.g }, align: 'center', valign: 'middle' } }));
const body = plan.map((r, i) => cols.map((c, j) => j === 0 ? { text: r[0], options: { fill: { color: 'E4ECDD' }, bold: true } } : { text: '', options: { fill: { color: r[1].includes(j) ? C.g2 : (i % 2 ? 'FFFFFF' : 'F5F8F2') } } }));
s.addTable([head, ...body], { x: 0.45, y: 1.2, w: 12.43, colW: [4.6, 1.15, 1.15, 0.92, 0.92, 0.92, 0.92, 0.92, 0.93], fontFace: F, fontSize: FS, color: C.dk, border: { type: 'solid', pt: 0.5, color: 'B9C6B2' }, margin: [0.03, 0.06, 0.03, 0.06], rowH: 0.55 });
T(s, 'Seeds fixed (42); split, folds and validation plots stored as files and reused for every camera, sensor set and model; every setting logged.', 0.45, 5.9, 12.43, 0.6, { italic: true, color: C.g });

// ================================================================ 30 Thank you
s = pres.addSlide({ masterName: 'TITLE', sectionTitle: 'Expected outcomes' });
s.addText('Thank you', { placeholder: 'title' });
s.addText('Suggestions of the Advisory Committee are welcome', { placeholder: 'body' });

const { applyTheme } = require(process.env.SKILL_DIR + '/scripts/apply_theme.js');
const OUT = process.env.OUT;
pres.writeFile({ fileName: OUT }).then(async f => { await applyTheme(OUT, THEME); console.log('saved', f); });
