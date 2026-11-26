// Advisory-committee deck 2026-27: complete methodology (UAV subplot level + ASD leaf level), grouped 7:3 split, disease-paper references on every slide.
// The user's own slides (field layout, glasshouse study, measurement slide) are inserted afterwards by adv27_merge.py.
const { pres, F, FS, C, THEME, S, sec, T, BL, box, arr, line, chain, tb, circ, refline } = require('./adv_lib.js');
const fs = require('fs');
const SZ = require('./figsizes.json'); const FIG = __dirname + '/../fig/';
function img(s, n, x, y, w, hmax) { const [pw, ph] = SZ[n]; let h = w * ph / pw; if (hmax && h > hmax) { h = hmax; w = h * pw / ph; } s.addImage({ path: FIG + n, x, y, w, h }); return h; }
let s;
// ------------------------------------------------------------------ title
sec('Introduction');
s = pres.addSlide({ masterName: 'TITLE', sectionTitle: 'Introduction' });
s.addText('AI-based Multimodal UAV Sensing of White Rust in Indian Mustard', { placeholder: 'title' });
s.addText([{ text: 'Complete research methodology, field season 2026-27 (UAV cameras + ASD leaf spectra)', options: { breakLine: true, bold: true } }, { text: ' ', options: { breakLine: true } },
  { text: 'Animesh Panda (Roll No. 13098)', options: { breakLine: true } }, { text: 'Ph.D. (Agricultural Physics), ICAR-Indian Agricultural Research Institute, New Delhi', options: { breakLine: true } },
  { text: ' ', options: { breakLine: true } }, { text: 'Presentation to the Advisory Committee', options: { italic: true } }], { placeholder: 'body' });
// ------------------------------------------------------------------ background
s = S('Background: white rust and why multimodal UAV sensing', 'Introduction');
BL(s, ['**Pathogen:** white rust (~~Albugo candida~~) forms white pustules on leaves, chlorosis and, after systemic infection, distorted inflorescences (staghead) (Saharan et al., 2014).'.replace(/~~/g, ''),
  '**Plant changes:** infected mustard leaves lose pigments and water and change their biochemistry (Mishra et al., 2009).', '**Epidemiology:** disease develops under cool and humid weather (Chattopadhyay et al., 2011).',
  '**Limitation of visual scoring:** slow, subjective and possible only after symptoms appear (Bock et al., 2010).',
  '**Opportunity:** UAV cameras record pigment, structure, water and temperature changes that accompany infection (Mahlein, 2016); fusing cameras improved wheat powdery mildew detection (Feng et al., 2022; Liu et al., 2024).'], 0.45, 1.2, 6.6, 5.0);
const resp = [['Pigment loss (chlorosis)', 'Hyperspectral and multispectral: visible and red edge', C.g], ['Pustules, leaf structure', 'Near infrared; RGB texture', C.blue], ['Water loss in tissue', 'Hyperspectral SWIR; ASD leaf spectra', C.teal], ['Changed transpiration', 'Thermal camera: canopy temperature', C.red]];
T(s, '**Plant response → what records it**', 7.35, 1.2, 5.5, 0.35);
resp.forEach((r, i) => { const y = 1.65 + i * 1.18; box(s, 7.35, y, 2.35, 0.95, null, r[0], r[2], 'FFFFFF'); arr(s, 9.72, y + 0.47, 10.12, y + 0.47); box(s, 10.15, y, 2.73, 0.95, null, r[1], r[2], [C.lt, C.lblue, C.lteal, C.lred][i]); });
refline(s, 'Saharan et al. (2014); Mishra et al. (2009); Chattopadhyay et al. (2011); Bock et al. (2010); Mahlein (2016); Feng et al. (2022); Liu et al. (2024).', 6.4, 0.5);
// ------------------------------------------------------------------ objectives
s = S('Research needs, objectives, data and outputs', 'Introduction');
tb(s, [['Objective', 'Research need (question answered)', 'Data used', 'Main output'],
  ['1. To characterise white rust of mustard through multimodal sensing from a UAV platform', 'Which wavelengths, indices, texture and thermal features of each camera (and of the leaf spectrum) respond to severity, and which already differ before symptoms?', '1920 post- and 576 pre-symptomatic subplot samples per camera; 7488 ASD leaf spectra', 'optimal wavelengths, White Rust Index, selected indices, TTFI, disease-specific feature sets; physiological basis'],
  ['2. To detect and discriminate disease severity of white rust through AI-based multimodal data fusion', 'How accurately do 15 sensor sets with ML and deep learning predict (a) healthy vs diseased, (b) DI class, (c) DI (%) on new plots?', '1920 post-symptomatic subplot samples per camera; leaf spectra', 'best sensor set and model per task; gain over a covariate-only model; maps; Bharatpur test'],
  ['3. To predict white rust at the pre-symptomatic stage', 'Can subplots that will develop white rust be separated from healthy subplots before pustules appear, and how early?', '576 pre-symptomatic subplot samples (2, 5, 8 DAI); early leaf spectra', 'pre-symptomatic models; earliest detection day; risk maps']], 0.45, 1.25, 12.43, [2.9, 4.4, 2.4, 2.73], { firstCol: true, fs: 13 });
T(s, 'UAV sample = one subplot on one date (48 plots × 4 subplots = 192 per flight). ASD sample = one leaf on one date (3 leaves of the centre plant per subplot = 576 per date).', 0.45, 6.2, 12.43, 0.6, { italic: true, color: C.g });
// ------------------------------------------------------------------ framework
sec('Research framework');
s = S('Overall research framework', 'Framework');
img(s, 'g01_workflow.png', 1.6, 1.15, 10.1, 5.3);
refline(s, 'framework of the DT-EDNet study: Ma et al. (2026); multi-camera fusion: Feng et al. (2022); leaf spectra with UAV: Yu et al. (2021).', 6.5, 0.45);
// ------------------------------------------------------------------ recent studies
s = S('Recent disease studies (2021–2026) behind the methodology', 'Framework');
tb(s, [['Study', 'Disease and data', 'Used for'],
  ['Ma et al. (2026)', 'rice blast; UAV hyperspectral; DT-EDNet', '7:3 split, SHAP-CARS, Relief indices, mRMR texture, TTFI, networks'], ['Liu et al. (2026)', 'wheat powdery mildew; ground to UAV', 'disease-specific index; leaf–canopy link'],
  ['Selvaprakash et al. (2026)', 'rice blast (IARI); leaf spectra', 'smoothing, index search, PCA (leaf part)'], ['Yuan et al. (2025)', 'rice bacterial blight; UAV + satellite', 'mRMR; RF, SVM, k-NN; transfer'],
  ['Yu et al. (2025)', 'rice sheath blight; spectra + physiology', 'physiology with spectra; multimodal network'], ['Bijlwan et al. (2025)', 'crop disease severity from weather', 'covariate (weather-only) baseline'],
  ['Deng et al. (2024)', 'wheat stripe rust; multimodal deep learning', 'deep network for the disease index'], ['Liu et al. (2024)', 'wheat powdery mildew; UAV multispectral + thermal', 'multi-features, thermal, results by stage'],
  ['Zhang et al. (2024)', 'tomato bacterial leaf spot; hyperspectral', 'pre-symptomatic water and red-edge bands'], ['Abdulridha et al. (2023); Blasch et al. (2023)', 'wheat stem / yellow rust; UAV (+ satellite)', 'RF, severity, varieties, growth stages, maps'],
  ['Nguyen et al. (2023)', 'wheat yellow rust; multispectral UAV', 'red edge, MS indices and texture, early detection'], ['Lv et al. (2023); Mandal et al. (2023)', 'corn leaf blight; rice blast; leaf spectra', 'ReliefF, VIF, SFFS; leaf indices, JM, RPD'],
  ['Zhang et al. (2022); Chatterjee et al. (2022)', 'rice leaf blast (leaf grades); white rust of mustard', 'leaf grades by stage; white rust biochemistry']], 0.45, 1.2, 12.43, [3.4, 4.2, 4.83], { firstCol: true, fs: 12 });
// ------------------------------------------------------------------ A1
sec('Data collection');
s = S('Step A1: Experimental design and treatments', 'Data collection');
BL(s, ['**Site and season:** IARI research farm, New Delhi; rabi 2026-27; field 48 m × 24 m; plots 5 m × 3 m; 4 subplots per plot (2.5 m × 1.5 m).',
  '**Varieties:** V1 = PM 26, V2 = Pusa Vijay, V3 = PM 37.', '**Sowing dates (7-day interval):** D1 = 19 Nov, D2 = 26 Nov, D3 = 3 Dec, D4 = 10 Dec 2026.',
  '**Inoculation:** 30 December 2026, zoosporangial suspension 1.5 × 10⁵ zoosporangia mL⁻¹ → crop age 41, 34, 27 and 20 days after sowing.',
  '**Treatments:** 12 (4 sowing dates × 3 varieties) × 3 replications (R1–R3) inoculated = 36 plots + 12 healthy plots = 48 plots.'], 0.45, 1.2, 6.6, 4.6);
tb(s, [['Timing', 'Sowing date', 'Crop age at inoculation'], ['D1', '19 Nov 2026', '41 days'], ['D2', '26 Nov 2026', '34 days'], ['D3', '3 Dec 2026', '27 days'], ['D4', '10 Dec 2026', '20 days']], 7.35, 1.25, 5.53, [1.1, 1.9, 2.53], { firstCol: true });
[['Healthy block', 'plots 1–12; uninoculated, 10 m from the inoculated block; 1 plot per treatment', C.g, C.lt], ['Inoculated block', 'R3 plots 13–24, R2 25–36, R1 37–48; 12 treatments per replication', C.red, C.lred]].forEach((b, i) => box(s, 7.35, 3.55 + i * 1.25, 5.53, 1.05, b[0], b[1], b[2], b[3]));
refline(s, 'inoculation of B. juncea with A. candida (1.44 × 10⁵ zoosporangia mL⁻¹): Mishra et al. (2009); inoculated + healthy plots for UAV disease studies: Guo et al. (2021), Liu et al. (2024); varieties: Blasch et al. (2023); sowing dates: Chattopadhyay et al. (2011).', 6.15, 0.75);
// ------------------------------------------------------------------ A2
s = S('Step A2: Unmanned aerial vehicle flights and the four cameras', 'Data collection');
tb(s, [['Camera', 'Sensor', 'Spectral range / bands', 'Ground pixel', 'Plant response recorded'],
  ['Hyperspectral', 'Headwall co-aligned VNIR–SWIR imager', '483 usable bands, 399–2398 nm', '≈ 2.2 cm', 'pigments, red edge, structure, water'],
  ['Multispectral', 'MicaSense RedEdge-MX', '475, 560, 668, 717, 840 nm', '≈ 2 cm', 'chlorophyll, red edge, vigour'],
  ['Red–green–blue', 'DJI camera', 'red, green, blue', '≈ 0.8 cm', 'colour, pustule and canopy texture'],
  ['Thermal', 'FLIR Vue Pro R (640 × 480)', '7.5–13.5 µm', '≈ 3.9 cm', 'canopy temperature (transpiration)']], 0.45, 1.25, 12.43, [1.7, 2.9, 3.4, 1.4, 3.03], { firstCol: true });
BL(s, ['**Flight protocol:** 11:00–14:00 h, clear sky, low wind; 30 m above ground; ≈ 85% forward and 80% side overlap.', '**Before every flight:** reflectance panels (imaged before and after) and ground control points; air temperature and relative humidity recorded.',
  '**Dates:** 13 flights with all four cameras (3 pre-symptomatic + 10 post-symptomatic); scoring of 5 plants per subplot and ASD of the centre plant on the flight day (or within one day).'], 0.45, 3.2, 12.43, 1.9);
refline(s, 'hyperspectral + thermal + RGB: Feng et al. (2022); multispectral + thermal: Liu et al. (2024), Calderón et al. (2014); multispectral red edge for yellow rust: Nguyen et al. (2023); UAV hyperspectral: Guo et al. (2021), Ma et al. (2026).', 6.15, 0.6);
// ------------------------------------------------------------------ timeline
s = S('Data collection timeline, 2026-27', 'Data collection');
img(s, 'g04_timeline.png', 0.6, 1.2, 12.1, 4.4);
BL(s, ['**All 13 dates:** four cameras; leaf scoring (L3, L5, LL) of 5 plants per subplot; ASD leaf spectra of the centre plant. **Purple squares:** biochemical and biophysical parameters (7 Jan, 18 Jan, 8 Feb, 1 Mar).'], 0.45, 5.75, 12.43, 0.7);
refline(s, 'leaf measurements on UAV flight days: Yu et al. (2021); Calderón et al. (2014).', 6.5, 0.4);
// ------------------------------------------------------------------ A3/A5
s = S('Steps A3 and A5: Plant scoring, disease index and labels', 'Data collection');
img(s, 'g03_survey.png', 0.45, 1.15, 6.4, 2.6);
box(s, 0.45, 3.95, 6.4, 1.15, 'Disease index of a subplot (Liu et al., 2024)', ['DI = Σ(x × f) / (9 × Σf) × 100 over its 15 graded leaves (Mishra et al., 2009)', 'x = leaf grade 0–9; f = number of leaves at grade x'], C.red, C.lred, { fs: 13 });
BL(s, ['**5 tagged plants per subplot:** centre + four corners inside the inner buffer (960 plants); the centre plant is the ASD plant.',
  '**Leaf scoring:** L3, L5, LL of each plant graded 0, 1, 3, 5, 7, 9 by % leaf area with pustules, judged with the area diagrams of Conn et al. (1990); one trained scorer (Bock et al., 2010).',
  '**Task A:** healthy (DI = 0) vs diseased (DI > 0). **Task B:** DI class. **Task C:** DI (%).', '**Pre-symptomatic label:** healthy plots vs inoculated subplots that show pustules later (Zhu et al., 2017).',
  '**Leaf level (ASD):** grade 0 vs > 0; six grades; grade as a number.'], 7.05, 1.15, 5.83, 4.1, { ps: 3 });
tb(s, [['DI (%)', '0', '0–5', '5–10', '10–25', '25–50', '> 50'], ['DI class', '0', '1', '3', '5', '7', '9']], 0.45, 5.3, 12.43, [2.0, 1.73, 1.74, 1.74, 1.74, 1.74, 1.74], { fs: 13, firstCol: true });
refline(s, 'DI from graded leaves: Liu et al. (2024), Mishra et al. (2009); area diagrams usable for white rust: Conn et al. (1990); Bock et al. (2010); grades 0, 1, 3, 5, 7, 9: Chen et al. (2023); early labels: Zhu et al. (2017).', 6.2, 0.6);
// ------------------------------------------------------------------ A4
s = S('Step A4: ASD FieldSpec leaf spectra of the centre plant of each subplot', 'Data collection');
chain(s, [{ h: 'Same leaves', b: 'L3, L5, LL of the centre plant of each subplot, right after grading' }, { h: 'White reference', b: 'start, then every 10–15 min or each plot' }, { h: 'Readings', b: '2 per leaf, contact probe + leaf clip, 350–2500 nm' },
  { h: 'Record', b: 'date, plot, subplot, leaf, reading, grade' }, { h: 'Volume', b: '576 leaves (1152 readings) per date; 7488 leaves in 13 dates' }], 0.45, 1.3, 12.43, 1.65, 0.28, C.teal, C.lteal);
BL(s, ['**Why:** a leaf spectrum of a graded leaf records the disease without sun, sky, soil or atmosphere, and links leaf and canopy at the same points.',
  '**When:** all 13 flight dates (same day or ± 1 day); the clip has its own lamp, so the time of day does not matter.', '**Unit of analysis:** one leaf on one date (leaf level); the UAV data stay at subplot level.'], 0.45, 3.2, 12.43, 2.2);
refline(s, 'Mandal et al. (2023) (handheld spectroradiometer, 0–9 scale); Chen et al. (2023) (ASD FieldSpec 4); Lv et al. (2023) (leaf clip); Martínez-Martínez et al. (2018) (contact spectra); Yu et al. (2021).', 6.1, 0.7);
// ------------------------------------------------------------------ A7 physiology (user references kept)
s = S('Step A7: Biochemical and biophysical parameters', 'Data collection');
tb(s, [['Parameter (unit)', 'Method', 'Reference'],
  ['Chlorophyll a, b (µg mg⁻¹ FW)', 'DMSO extraction (100 mg, 10 mL, 65 °C); A665, A649', 'Hiscox and Israelstam (1979); Wellburn (1994)'],
  ['Total carotenoids (mg g⁻¹ FW)', 'same DMSO extract; A480', 'Lichtenthaler and Wellburn (1983)'], ['Anthocyanin (µg g⁻¹ FW)', 'pH-differential: 520 and 700 nm at pH 1.0 and 4.5', 'Lee et al. (2005)'],
  ['Total protein (µg mg⁻¹ FW)', 'Bradford dye binding; 595 nm; BSA standard', 'Bradford (1976); Kuril (2024)'], ['Relative water content (%)', 'fresh, turgid (4 h) and dry (48 h, 70 °C) weight', 'Barrs and Weatherley (1962)'],
  ['Membrane stability index (%)', 'conductivity at 40 °C (C₁) and 100 °C (C₂)', 'Sairam (1994); Premachandra et al. (1990)'],
  ['Photosynthesis, transpiration, stomatal conductance', 'LI-6400 portable gas exchange', 'Riches et al. (2020); Long and Bernacchi (2003)'],
  ['Leaf area index (m² m⁻²)', 'canopy analyser: 1 reading above, 4 below; diffuse light', 'Singh et al. (2021); Bréda (2003)']], 0.45, 1.2, 8.55, [2.6, 3.65, 2.3], { firstCol: true, fs: 12 });
box(s, 9.2, 1.2, 3.68, 3.4, 'Sampling design', ['Dates: 7 Jan (pre), 18 Jan, 8 Feb, 1 Mar 2027', 'One designated subplot per plot, rotated (plot mod 4 + 1)', 'Gas exchange on L3 of the centre plant, 09:30–11:30 h', 'Lab samples: L3 of 3 untagged plants', 'LAI in all 4 subplots'], C.teal, C.lteal, { valign: 'top', fs: 13 });
BL(s, ['**Use:** explain the camera responses (Activity 1.7) and pre-symptomatic changes; not model inputs.'], 0.45, 5.35, 12.43, 0.5);
refline(s, 'white rust biochemistry: Mishra et al. (2009), Chatterjee et al. (2022); spectra + physiology: Yu et al. (2025); physiology explaining thermal and spectral signals: Calderón et al. (2013), Zarco-Tejada et al. (2018); Brassica leaves: Baranowski et al. (2015).', 5.9, 0.7);
// ------------------------------------------------------------------ A6 covariates
s = S('Step A6: Covariates and weather data', 'Data collection');
tb(s, [['Covariate', 'Coding', 'Main use'], ['Days after inoculation (DAI)', 'numeric (flight date − 30 Dec 2026)', 'covariate baseline'], ['Variety (V1–V3)', 'categorical', 'baseline; results by variety'],
  ['Sowing date / crop age at inoculation', 'D1–D4 or 41, 34, 27, 20 days', 'baseline; results by sowing date'], ['Growth stage (BBCH)', '1 vegetative (10–49), 2 flowering (60–69), 3 pod formation (70+)', 'baseline; results by stage'],
  ['Weather (Tmax, Tmin, RH I, RH II, rainfall)', '7-day summaries ending the day before each flight; favourable days since inoculation', 'baseline; interpretation']], 0.45, 1.25, 12.43, [3.6, 5.2, 3.63], { firstCol: true });
BL(s, ['**Favourable days** (weather-based white rust forecasting, Chattopadhyay et al., 2011): leaf infection Tmax 16–24 °C, RH I > 97%, RH II > 40%; staghead Tmax 20–29 °C, Tmin > 12 °C, RH I > 97% (RH I = morning, RH II = afternoon; checked in the paper).', '**Covariates are not camera features:** they enter only the covariate models (Steps 2.9, 3.5, L8) and the results by stratum.'], 0.45, 4.3, 12.43, 1.3);
refline(s, 'Chattopadhyay et al. (2011); weather vs weather + remote sensing: Zhang et al. (2014a); mustard rot: Bhattacharya and Chattopadhyay (2013); stage effects: Blasch et al. (2023).', 6.1, 0.6);
// ------------------------------------------------------------------ A8 Bharatpur
s = S('Step A8: Independent test data at Bharatpur', 'Data collection');
chain(s, [{ h: 'Sites', b: 'research farms and farmers\' fields, natural white rust' }, { h: 'Quadrats', b: '2.5 m × 1.5 m; pegs, markers, RTK GNSS; 15–20 per field' }, { h: 'Flights', b: 'same four cameras, 2–3 dates (Feb–Mar)' },
  { h: 'Ground truth', b: '5 plants per quadrat; same 0–9 grades and scorer' }, { h: 'Covariates', b: 'variety, sowing, stage, sprays, weather' }], 0.45, 1.3, 12.43, 1.75, 0.28, C.gold, C.lgold);
BL(s, ['**Size:** ≥ 300 quadrat-dates covering healthy to severe.', '**Rule:** never used for selection, tuning or training; used once to test the frozen IARI models (Step 2.11).'], 0.45, 3.3, 12.43, 1.5);
refline(s, 'independent test data: Ma et al. (2026); transfer of UAV disease models: Yuan et al. (2025), Liu et al. (2026); Bharatpur white rust site: Chattopadhyay et al. (2011).', 6.1, 0.6);
// ------------------------------------------------------------------ data sets
s = S('Data sets needed for the whole analysis', 'Data collection');
tb(s, [['Data set', 'Content', 'When', 'Amount'],
  ['Field plan', 'plot, block, replication, sowing date, variety; plot and subplot corners (GPS)', 'before sowing', '48 plots, 192 subplots'],
  ['UAV images (4 cameras)', 'HS VNIR–SWIR cubes + GNSS/IMU; MS frames + light sensor; RGB frames; thermal frames', '13 dates', 'whole field per date'],
  ['Calibration and flight data', 'panel certificates and images (before/after); GCPs (RTK); flight log (time, sky, wind, air temperature, RH)', 'every flight', '13 sets'],
  ['Leaf scoring sheets', 'plot, subplot, plant (centre, corners 1–4), leaf (L3, L5, LL), grade 0–9; staghead racemes', '13 dates', '2880 grades per date'],
  ['ASD leaf spectra', 'centre plant: .asd files (2 readings per leaf) + ASCII; white-reference log', '13 dates', '1152 readings per date'],
  ['Growth stage, inoculation record', 'BBCH stage per plot and date; inoculation date, concentration, method', '13 dates; 30 Dec', '624 records'],
  ['Weather', 'daily Tmax, Tmin, RH I, RH II, rainfall (IARI observatory), 1 Dec 2026 – 31 Mar 2027', 'daily', '≈ 120 days'],
  ['Plant parameters', '11 biochemical/biophysical parameters; LI-6400 and canopy-analyser files', '4 dates', '48 per date (LAI 192)'],
  ['Bharatpur test data', 'images of 4 cameras; quadrat positions; 3-point surveys; covariates; local weather', '2–3 dates', '≥ 300 quadrat-dates'],
  ['Glasshouse data', 'pot plan; inoculation record; 0–6 severity; ASD spectra', '2, 5, 8, 11 DAI, then weekly', '48 pots']], 0.45, 1.2, 12.43, [2.6, 6.4, 1.8, 1.63], { firstCol: true, fs: 12 });
// ------------------------------------------------------------------ B
sec('UAV processing and features');
s = S('Part B: Unmanned aerial vehicle image processing and subplot average spectra', 'UAV processing');
img(s, 'g06_processing.png', 0.45, 1.15, 12.43, 2.3);
tb(s, [['Step', 'What is done', 'Disease papers'], ['B1 Calibration', 'empirical line with panels (HS, MS); fixed RGB settings; radiance → temperature (ε 0.98)', 'Ma et al. (2026); Guo et al. (2021); Yuan et al. (2025)'],
  ['B2 Mosaics', 'structure-from-motion mosaics; HS georectification; same GCPs every date', 'Ma et al. (2026); Feng et al. (2022)'], ['B3 HS quality, smoothing', 'remove 1335–1460, 1785–1965 nm; Savitzky–Golay (5 bands, order 2) per segment', 'Ma et al. (2026); Mandal et al. (2023); Mustafa et al. (2023)'],
  ['B4–B5 Co-registration, grid', 'UTM 43N; register to HS (RMSE < 2.2 cm); resample to the HS grid', 'Feng et al. (2022); Guo et al. (2021)'],
  ['B6 Subplot ROI averages', 'one ROI per subplot (inner buffer); mean of all ROI pixels per band = field-level average spectrum; same ROIs for all cameras and dates', 'Ma et al. (2026) (ENVI ROI means); Liu et al. (2024); Guo et al. (2021)']], 0.45, 3.55, 12.43, [2.6, 6.0, 3.83], { firstCol: true, fs: 12 });
// ------------------------------------------------------------------ C features
s = S('Part C: Features of the four cameras (C1–C6)', 'UAV features');
tb(s, [['Camera', 'Features', 'Number', 'Disease papers'],
  ['Hyperspectral', 'reflectance 483; first derivative 483; red-edge position, amplitude, area; 48 published indices; PCA texture (3 PCs × 8 GLCM, 3 × 3, 64 levels)', '≈ 1040', 'Yu et al. (2021); Lv et al. (2023); Ma et al. (2026); Guo et al. (2021); Mandal et al. (2023)'],
  ['Multispectral', '5 bands; 12 indices; 10 normalised differences; GLCM of 5 bands', '67', 'Liu et al. (2024); Blasch et al. (2023)'],
  ['RGB', 'ExG, ExR, ExG − ExR, VARI, GLI, NGRDI; hue, saturation, value; GLCM of R, G, B', '33', 'Feng et al. (2022)'],
  ['Thermal', 'ROI temperature statistics; CTD = Tc − Ta, NRCT, difference from healthy plots; thermal GLCM', '17', 'Calderón et al. (2014); Oerke et al. (2006); Feng et al. (2022)']], 0.45, 1.25, 12.43, [1.7, 5.9, 1.1, 3.73], { firstCol: true, fs: 13 });
BL(s, ['**No second derivative, no continuum removal, no wavelets:** the feature families of the DT-EDNet study (bands, indices, texture) plus thermal.', '**Feature table:** one per camera, one row per subplot-date, with identifiers, labels, covariates and group prefixes (R_, FD_, RE_, VI_, TX_, TH_).'], 0.45, 4.75, 12.43, 1.3);
refline(s, 'Ma et al. (2026); Feng et al. (2022); Liu et al. (2024); Nguyen et al. (2023); Mandal et al. (2022) (red-edge amplitude); Kundu et al. (2021) (DWSI); Calderón et al. (2014).', 6.3, 0.45);
require('./adv_idx.js')();
require('./adv_ms.js')();
// ------------------------------------------------------------------ D split
sec('Split and preparation');
s = S('Part D: The 7:3 split by whole plots and inner validation', 'Validation design');
img(s, 'g02_layout.png', 0.45, 1.15, 7.3, 3.6);
BL(s, ['**7:3:** 33 training plots, 15 test plots; all subplots and leaves of a plot on one side.', '**Test plots (fixed before the first flight):** 1, 4, 5, 8 (healthy) and 13, 14, 18, 25, 27, 31, 35, 37, 44, 46, 48 (11 different treatments over R1–R3).',
  '**ML tuning:** GroupKFold(3) by plot inside the 33 training plots.', '**Networks:** 22 plots fit, 11 plots (one third) for early stopping: 6, 7, 11, 19, 24, 26, 28, 30, 36, 39, 41.', '**Test plots used once**, at the end.'], 7.95, 1.15, 4.93, 4.6, { ps: 3 });
img(s, 'g05_split.png', 0.45, 4.8, 7.3, 1.75);
refline(s, '7:3 stratified split, 10% of training as validation, highest-validation model tested once: Ma et al. (2026); one-third hold-out: Mandal et al. (2023); 4-fold CV for SFFS/SVM: Tian et al. (2021), Lv et al. (2023) – here always by whole plots.', 6.55, 0.5);
// ------------------------------------------------------------------ D prep
s = S('Part D: Thermal normalisation, scaling, class balance and leakage rules', 'Data preparation');
tb(s, [['Step', 'What is done', 'Disease papers'], ['D3 Thermal normalisation', 'CTD = Tc − Ta; NRCT; difference from healthy training plots of the same date and variety', 'Calderón et al. (2014); Oerke et al. (2006)'],
  ['D4 Scaling and balance', 'z-score with fitting-part statistics (inside every fold); balanced class weights (SVM, RF); networks: label smoothing 0.01', 'Lv et al. (2023); Ma et al. (2026)'],
  ['D5 Leakage rules', 'no plot on both sides; selection, scaling, healthy references and weights from training plots only; test plots used once', 'Ma et al. (2026); Mandal et al. (2023)']], 0.45, 1.25, 12.43, [2.8, 6.0, 3.63], { firstCol: true });
BL(s, ['**Objective 1 (description)** uses all samples; **for the models** the same selection is repeated on the training plots only (Step 2.2).'], 0.45, 4.0, 12.43, 0.8);
// ------------------------------------------------------------------ Objective 1
sec('Objective 1');
s = S('Objective 1: Characterisation of white rust (overview)', 'Objective 1');
img(s, 'g10_selection_chain.png', 0.45, 1.15, 8.0, 4.4);
BL(s, ['**1.1** response curves, correlation, strata', '**1.2** NDSI/RSI maps → SHAP-CARS optimal wavelengths', '**1.3** best NDSI, RSI; White Rust Index', '**1.4** filter + ReliefF indices', '**1.5** mRMR texture + TTFI', '**1.6** VIF → DSF; camera complementarity', '**1.7** physiological basis', '**1.8** pre-symptomatic stage'], 8.65, 1.15, 4.23, 4.6, { ps: 3 });
refline(s, 'one selection method per feature group, as in Ma et al. (2026); VIF: Lv et al. (2023); physiology: Calderón et al. (2013); pre-symptomatic: Zarco-Tejada et al. (2018), Zhu et al. (2017).', 6.0, 0.6);
s = S('Activity 1.1: Response analysis (Steps 1.1.1–1.1.3)', 'Objective 1');
img(s, 'g07_spectra_demo.png', 0.45, 1.15, 12.43, 2.8);
BL(s, ['**1.1.1** mean ± SD reflectance and first derivative by DI class; % difference from class 0; class means of MS, RGB, thermal features.', '**1.1.2** Pearson r of every feature with the DI.', '**1.1.3** the same by variety, sowing date, growth stage, DAI; DI against favourable days.'], 0.45, 4.15, 12.43, 1.6);
refline(s, 'mean spectra by severity: Ma et al. (2026), Mandal et al. (2023), Bohnenkamp et al. (2021); correlation with DI: Zhang et al. (2012), Guo et al. (2021); by growth stage: Blasch et al. (2023), Liu et al. (2024), Zhang et al. (2022).', 5.95, 0.7);
s = S('Step 1.2.1: Effective ranges from normalised difference and ratio spectral index maps', 'Objective 1');
img(s, 'g08_ndsi_demo.png', 0.45, 1.15, 4.6, 4.2);
BL(s, ['**What:** NDSI = (Ri − Rj)/(Ri + Rj) and RSI = Ri/Rj for every pair of HS bands (reduced sampling); R² with the DI drawn as maps.', '**Rule:** bands in pairs with R² > 0.5 in both maps = effective ranges; if none reach 0.5, top 5% of pairs.', '**Output:** effective ranges → SHAP-CARS; best NDSI and RSI pairs → indices (1.3).'], 5.3, 1.15, 7.58, 4.0);
refline(s, 'Ma et al. (2026): R² maps of NDSI and RSI with rice blast severity, effective ranges where R² > 0.5 (455–503, 520–661, 702–1000 nm); top 5%: Tian et al. (2021); two-band search: Huang et al. (2014).', 5.6, 0.75);
s = S('Step 1.2.2: Optimal wavelengths by Shapley additive explanations and competitive adaptive reweighted sampling', 'Objective 1');
img(s, 'g09_shapcars_demo.png', 0.45, 1.15, 12.43, 3.0);
chain(s, [{ h: 'Candidates', b: 'R and FD bands in the effective ranges, standardised' }, { h: 'SHAP', b: 'random forest of DI; mean |SHAP|; top 40% kept' }, { h: 'MCCV', b: '50 divisions by plot → number of PLS components' }, { h: 'CARS', b: '50 iterations; subset with the best cross-validated RMSE' }, { h: 'OW', b: '≈ 10–15 bands labelled R_λ / FD_λ' }], 0.45, 4.35, 12.43, 1.35, 0.25, C.blue, C.lblue, { fs: 13 });
refline(s, 'Ma et al. (2026): SHAP values of an ensemble model ranked the bands, MCCV chose the PLS components, CARS removed redundant variables and the subset was fixed by validation performance (12 key wavelengths).', 5.95, 0.7);
s = S('Activities 1.3–1.4: White Rust Index and vegetation index selection', 'Objective 1');
box(s, 0.45, 1.2, 6.1, 2.2, '1.3 Data-driven indices', ['Best NDSI and RSI (bands ≥ 10 nm apart)', 'WRI = NDSI(λ1, λ2) + w × R(λ3); λ1, λ2 ≥ 50 nm apart; w ∈ {−1, −0.5, 0, 0.5, 1}; 6-nm steps', 'Best by |r| with DI and balanced accuracy healthy vs diseased; MS: best of 10 two-band NDs'], C.g, C.lt, { fs: 13, align: 'left', valign: 'top' });
box(s, 6.78, 1.2, 6.1, 2.2, '1.4 Vegetation index selection', ['48 indices + 3 red-edge parameters + NDSI, RSI, WRI', 'Redundancy filter: clusters at |r| ≥ 0.95, keep the one best related to DI', 'ReliefF (Tasks A, B) / RReliefF (Task C), k = 10 → top 5 = VI'], C.blue, C.lblue, { fs: 13, align: 'left', valign: 'top' });
tb(s, [['Rank', 'λ1', 'λ2', 'λ3', 'w', '|r| with DI', 'Balanced accuracy'], ['1', '754', '700', '532', '−0.5', '0.71', '0.83'], ['2', '760', '694', '550', '−0.5', '0.70', '0.82']], 0.45, 3.65, 6.1, [0.7, 0.8, 0.8, 0.8, 0.8, 1.0, 1.2], { fs: 12 });
T(s, 'WRI search output (demo data)', 0.45, 4.75, 6.1, 0.3, { italic: true, fontSize: 12 });
refline(s, 'WRI form and 50-nm rule: Mahlein et al. (2013); three-band index: Zheng et al. (2018); ground-to-UAV index: Liu et al. (2026); Relief top 5 indices and correlation among indices: Ma et al. (2026); k = 10: Lv et al. (2023).', 5.6, 0.75);
s = S('Activities 1.5–1.6: Texture, Tri-band Texture Fusion Index and disease-specific feature set', 'Objective 1');
box(s, 0.45, 1.2, 6.1, 2.6, '1.5 Texture', ['24 PCA texture features → |r| ≥ 0.95 filter → mRMR top 6 (TF1–TF6)', '120 ordered triplets × 3 formulas: TTFI1 = (TF1 + TF2)/TF3; TTFI2 = TF1 × TF2/TF3; TTFI3 = TF1 × (TF1 + TF2)/(TF2 + TF3)', 'Best |r| with DI = TTFI'], C.purple, C.lpurple, { fs: 13, align: 'left', valign: 'top' });
box(s, 6.78, 1.2, 6.1, 2.6, '1.6 Disease-specific feature set (DSF)', ['MS, RGB, thermal: filter + ReliefF top 5 (normalised thermal kept)', 'HS: OW + VI + TF + TTFI pooled', 'VIF = 1/(1 − R²): remove the largest until all < 10 → DSF of each camera and task', 'Cross-camera correlation → complementarity'], C.g, C.lt, { fs: 13, align: 'left', valign: 'top' });
refline(s, 'mRMR top six textures and TTFI (TTFI3 |r| = 0.756): Ma et al. (2026); mRMR: Yuan et al. (2025); VIF < 10: Lv et al. (2023), Tian et al. (2021), Mustafa et al. (2023); sensor complementarity: Mahlein et al. (2019), Feng et al. (2022).', 4.1, 0.75);
s = S('Activities 1.7–1.8: Physiological basis and the pre-symptomatic stage', 'Objective 1');
box(s, 0.45, 1.2, 6.1, 2.4, '1.7 Physiological basis', ['Paired t-test inoculated vs healthy plot of the same treatment, per date', 'Two-way ANOVA (variety × sowing date) within R1–R3, LSD 5%', 'r of parameters with DI and with the DSF features'], C.teal, C.lteal, { fs: 13, align: 'left', valign: 'top' });
box(s, 6.78, 1.2, 6.1, 2.4, '1.8 Pre-symptomatic stage (2, 5, 8 DAI)', ['Later-infected vs healthy: mean curves and t-test of plot means per feature and date', 'Selection chain with the binary label → pre-symptomatic DSF', 'Earliest significant date of each feature'], C.red, C.lred, { fs: 13, align: 'left', valign: 'top' });
img(s, 'g15_presym_demo.png', 3.2, 3.75, 6.9, 2.0);
refline(s, 'white rust biochemistry: Mishra et al. (2009); physiology vs severity: Calderón et al. (2013); pre-visual traits: Zarco-Tejada et al. (2018); pre-symptomatic: Zhu et al. (2017), Terentev et al. (2023), Zhang et al. (2024), Gold et al. (2020); earliest day: Mahlein et al. (2019).', 5.95, 0.75);
// ------------------------------------------------------------------ Objective 2
sec('Objective 2');
s = S('Objective 2: Detection and severity discrimination (overview)', 'Objective 2');
img(s, 'g11_models.png', 0.45, 1.15, 12.43, 4.0);
BL(s, ['**15 sensor sets** (4 single, 6 pairs, 4 triplets, all four) × **3 tasks**; selection repeated on the 33 training plots; camera DSFs concatenated (feature-level fusion) and VIF < 10 again.'], 0.45, 5.25, 12.43, 0.75);
refline(s, 'single vs fused sources: Feng et al. (2022); feature-level fusion: Liu et al. (2024), Huang et al. (2020); multimodal networks: Deng et al. (2024), Yu et al. (2025); selection on training data only: Ma et al. (2026).', 6.15, 0.5);
s = S('Activity 2.3: Sequential floating forward selection and machine-learning models', 'Objective 2');
tb(s, [['Model', 'Grid (GroupKFold(3) by plot)', 'Disease papers'], ['SVM / SVR (RBF)', 'C ∈ {0.1, 1, 10, 100}; γ ∈ {0.001, 0.01, 0.1, scale}; ε ∈ {0.1, 0.5}', 'Tian et al. (2021); Lv et al. (2023); Yuan et al. (2025)'],
  ['Random forest', '500 trees; max_features ∈ {sqrt, 0.3}; min_samples_leaf ∈ {1, 3, 5}', 'Abdulridha et al. (2023); Liu et al. (2024); Yuan et al. (2025)'], ['k-NN', 'k ∈ {3, 5, 7, 9, 11}; uniform or distance weights', 'Tian et al. (2021); Yuan et al. (2025)'],
  ['PLS-DA / PLSR', '1–15 components', 'Zhang et al. (2012); Mandal et al. (2023)']], 0.45, 1.25, 12.43, [2.2, 5.6, 4.63], { firstCol: true, fs: 13 });
BL(s, ['**SFFS:** adds the feature that most improves the GroupKFold(3) score and tries to remove one after each addition; best subset ≤ 15 features (macro-F1 for A, B; −RMSE for C).', '**Final fit:** best setting refitted on all 33 training plots; test plots predicted once.'], 0.45, 4.0, 12.43, 1.5);
refline(s, 'SFFS wrapped around LDA, k-NN, SVM (2–4 features best): Tian et al. (2021); SFFS with macro-F1 after ReliefF and VIF: Lv et al. (2023).', 6.0, 0.5);
s = S('Activity 2.4: Deep neural network with feature fusion and the pseudo-image networks', 'Objective 2');
tb(s, [['Setting', 'Ma et al. (2026)', 'This study'], ['Networks', 'DT-EDNet vs EfficientNet, ResNet18, ConvNeXt V2', 'same (Tasks A, B); DNN-F1 for A, B, C'], ['Input', 'feature vector reshaped into a pseudo-2D representation', 'k × k pseudo-image of the selected features'],
  ['Optimiser, schedule', 'AdamW 6 × 10⁻⁴, weight decay 10⁻⁵; cosine to 10⁻⁶', 'same'], ['Epochs, patience', '300; 60 (min. improvement 5 × 10⁻⁵)', 'same'], ['Batch, label smoothing, clipping', '32; 0.01; 1.2', 'same'],
  ['Validation', '10% of the training set', '11 of the 33 training plots'], ['Model selection', 'highest validation OA', 'same'], ['Comparisons', 'feature configurations; module ablation', 'OW, VI, TF, OW+VI, OW+TTFI, OW+VI+TTFI; −SE, −DTG, −both']], 0.45, 1.25, 12.43, [2.7, 4.9, 4.83], { firstCol: true, fs: 13 });
refline(s, 'Ma et al. (2026); multimodal deep network for the disease index: Deng et al. (2024); neural network on UAV features: Liu et al. (2020); network severity estimation: Martínez-Martínez et al. (2018).', 6.0, 0.6);
s = S('Activity 2.5: Evaluation on the 15 test plots', 'Objective 2');
img(s, 'g12_eval_demo.png', 0.45, 1.15, 7.4, 3.3);
BL(s, ['**Tasks A, B:** confusion matrix, OA, kappa, per-class precision, recall, F1, macro recall, macro-F1; Task A also sensitivity, specificity, AUC.', '**Task C:** R², RMSE, RPD = SD/RMSE.', '**Main metrics:** macro-F1 (A, B), R² (C).'], 8.05, 1.15, 4.83, 3.4);
tb(s, [['', 'Pred. healthy', 'Pred. diseased', 'Metric', 'Value'], ['Obs. healthy', '150', '30', 'OA', '0.883'], ['Obs. diseased', '40', '380', 'sens. / spec.', '0.905 / 0.833']], 0.45, 4.6, 7.4, [1.5, 1.4, 1.5, 1.6, 1.4], { fs: 12 });
refline(s, 'metrics of Ma et al. (2026); AUC: Liu et al. (2020); R², RMSE: Guo et al. (2021), Feng et al. (2022); RPD: Mandal et al. (2023).', 6.15, 0.5);
s = S('Activity 2.6: Comparison, interpretation and covariate baseline', 'Objective 2');
box(s, 0.45, 1.2, 6.1, 2.4, 'Comparison and interpretation', ['Ranking of models × sensor sets per task', 'Fusion gain = fused set − best single camera in it', 'Network comparison on HS configurations; DT-EDNet ablation', 'SHAP of the best model of each task'], C.purple, C.lpurple, { fs: 13, align: 'left', valign: 'top' });
img(s, 'g13_covariate_demo.png', 7.0, 1.15, 5.4, 3.5);
BL(s, ['**Covariate baseline (Step 2.9):** M0 = random forest on days after inoculation, variety, sowing date, growth stage, 7-day weather, favourable days; M1 = best sensor model; M2 = M1 model type on sensors + covariates; same training and test plots.', '**Gains on the test plots:** ΔS = M1 − M0 (what the cameras add), ΔC = M2 − M1 (what weather and crop add). Zhang et al. (2014a): adding remote sensing to weather raised wheat powdery mildew forecast accuracy from about 69% to 78%.'], 0.45, 3.75, 6.4, 2.1, { ps: 3 });
refline(s, 'fusion gain: Feng et al. (2022); comparison, ablation, SHAP: Ma et al. (2026); weather only vs weather + remote sensing: Zhang et al. (2014a); weather-only ML: Bijlwan et al. (2025); remote sensing + weather for stripe rust: Ruan et al. (2022); white rust forecasting: Chattopadhyay et al. (2011); mustard rot: Bhattacharya and Chattopadhyay (2013).', 5.95, 0.75);
s = S('Activity 2.7: Results by stratum, maps and independent testing', 'Objective 2');
box(s, 0.45, 1.2, 6.1, 2.6, 'Strata and maps', ['Macro-F1 and R² by variety, sowing date, growth stage and date (test plots)', 'Maps of predicted DI class and DI per subplot for all 10 post-symptomatic dates; error maps'], C.g, C.lt, { fs: 13, align: 'left', valign: 'top' });
box(s, 6.78, 1.2, 6.1, 2.6, 'Independent testing at Bharatpur', ['Tested IARI models frozen', 'Same processing (one ROI per quadrat; IARI scaling)', 'Applied once; same metrics by site type and variety; farm maps'], C.gold, C.lgold, { fs: 13, align: 'left', valign: 'top' });
refline(s, 'by growth stage and maps: Liu et al. (2024), Blasch et al. (2023), Abdulridha et al. (2023), Deng et al. (2024); independent test data: Ma et al. (2026); transfer: Yuan et al. (2025), Liu et al. (2026).', 4.1, 0.7);
// ------------------------------------------------------------------ Objective 3
sec('Objective 3');
s = S('Objective 3: Pre-symptomatic prediction (Steps 3.1–3.4)', 'Objective 3');
chain(s, [{ h: '3.1 Labels', b: 'healthy plots vs inoculated subplots that show pustules later; never-symptomatic excluded' }, { h: '3.2 Normalisation', b: 'z to healthy training plots of the same date and variety' }, { h: '3.3 Selection', b: 'chain of 1.8.2 on training plots; VIF; SFFS ≤ 10' }, { h: '3.4 Models', b: 'SVM, RF, k-NN, PLS-DA, DNN-F1; 15 sensor sets' }], 0.45, 1.3, 12.43, 2.0, 0.3, C.red, C.lred);
BL(s, ['**Data:** 576 subplot-dates (1, 4, 7 January; 2, 5, 8 DAI): 396 training, 180 test.', '**No pseudo-image networks:** about 400 training samples are too few for them.'], 0.45, 3.6, 12.43, 1.3);
refline(s, 'labels from later status: Zhu et al. (2017), Tian et al. (2021), Yu et al. (2021); healthy reference: Oerke et al. (2006), Zarco-Tejada et al. (2018); ML classifiers before symptoms: Zhu et al. (2017), Tian et al. (2021).', 5.9, 0.75);
s = S('Activity 3.5–3.6: Earliest detection day and risk maps', 'Objective 3');
img(s, 'g15_presym_demo.png', 0.45, 1.15, 7.6, 2.95);
BL(s, ['**Metrics per date:** sensitivity, specificity, OA, kappa, macro-F1, AUC on the test plots.', '**Earliest detection day:** first DAI on which predicted scores of later-infected and healthy test subplots differ (t-test, p < 0.05).', '**Covariate model** as reference.', '**Risk maps:** probability of later infection per subplot.'], 8.25, 1.15, 4.63, 4.4);
refline(s, 'earliest detection day per sensor: Mahlein et al. (2019); accuracy by date: Gold et al. (2020), Nguyen et al. (2023), Zhang et al. (2024); pre-visual maps: Zarco-Tejada et al. (2018); covariate reference: Zhang et al. (2014a).', 5.95, 0.7);
// ------------------------------------------------------------------ Part L
sec('ASD leaf spectra');
s = S('Part L: Analysis of the ASD FieldSpec leaf spectra (leaf level)', 'ASD analysis');
img(s, 'g14_leaf_chain.png', 0.45, 1.15, 7.8, 3.2);
BL(s, ['**Data:** 7488 leaves (13 dates × 576, centre plant of every subplot); each spectrum = mean of 2 readings; already splice-corrected.', '**Same split:** leaves of the 15 test plots = 2340 test leaves; 5148 training leaves.', '**Tasks:** grade 0 vs > 0; six grades; grade as a number.'], 8.45, 1.15, 4.43, 3.6);
tb(s, [['Step', 'Settings', 'Disease papers'], ['L1 Leaf table', 'join grades; average 2 readings; L3, L5, LL only; duplicates removed', 'Chen et al. (2023); Lv et al. (2023)'],
  ['L3 Pre-processing', 'Savitzky–Golay (11, 2); 400–2400 nm, water bands kept; FD; 5-nm band means for searches', 'Ma et al. (2026); Selvaprakash et al. (2026); Meng et al. (2020); Mandal et al. (2023)'],
  ['L4 Indices', '48 published indices + REP, Dr, SDr (1 nm)', 'Mandal et al. (2023); Zhang et al. (2012)']], 0.45, 4.45, 12.43, [2.2, 6.0, 4.23], { firstCol: true, fs: 12 });
s = S('Part L: Leaf Objective 1, models and the leaf–canopy link', 'ASD analysis');
tb(s, [['Step', 'What is done', 'Disease papers'], ['L5 Leaf Objective 1', 'mean/difference/r spectra; NDSI/RSI maps; SHAP-CARS; NDSI, RSI, WRI; filter + ReliefF; VIF → leaf DSF; JM distance; PCA', 'Ma et al. (2026); Mahlein et al. (2013); Mandal et al. (2023); Lv et al. (2023)'],
  ['L6 Leaf models', 'selection on training leaves; SVM, RF, k-NN, PLS (SFFS + grid, GroupKFold(3)); DNN-F1; four networks (A, B)', 'Tian et al. (2021); Lv et al. (2023); Zhang et al. (2022); Ma et al. (2026)'],
  ['L7 Test metrics', 'OA, kappa, macro-F1, per-class F1, AUC; R², RMSE, RPD on 2340 test leaves', 'Ma et al. (2026); Lv et al. (2023); Mandal et al. (2023)'],
  ['L8 Covariate baseline', 'M0, M1, M2 at leaf level', 'Zhang et al. (2014a); Bijlwan et al. (2025)'],
  ['L9 Leaf–canopy link', 'leaf vs canopy OW and VI; subplot mean leaf spectrum resampled to Headwall bands vs UAV spectrum; leaf WRI on UAV subplot spectra vs DI', 'Liu et al. (2026); Bohnenkamp et al. (2019); Poblete et al. (2023); Zheng et al. (2018)'],
  ['L10 Pre-symptomatic leaves', 'leaves of 1, 4, 7 Jan; later-infected plants vs healthy; selection and models', 'Gold et al. (2020); Tian et al. (2021); Lv et al. (2023)']], 0.45, 1.25, 12.43, [2.4, 6.0, 4.03], { firstCol: true, fs: 12 });
// ------------------------------------------------------------------ outcomes + plan
sec('Outputs');
s = S('Expected outcomes and six-month work plan', 'Outputs');
tb(s, [['Objective', 'Expected outcome'], ['1', 'Sensitive spectral ranges, signatures and indices for white rust under glasshouse and field conditions, across crop stages and severity levels.'], ['2', 'The best suitable sensor or fusion of sensors for detection and monitoring of white rust throughout the crop growth stages.'], ['3', 'Early, pre-symptomatic detection so that preventive measures can be taken in time.']], 0.45, 1.2, 12.43, [1.3, 11.13], { firstCol: true, fs: 13 });
tb(s, [['Month', 'Work'], ['1', 'Parts A–B; subplot ROI averages; leaf table (L1)'], ['2', 'Parts C–D; Activity 1.1; L3–L5.1'], ['3', 'Activities 1.2–1.8; L5.2–L5.7; physiology statistics'], ['4', 'Objective 2: ML and DNN-F1, 15 sensor sets; leaf models'], ['5', 'Objective 2: networks, ablation, SHAP, covariate baseline, maps; L7–L9'], ['6', 'Objective 3, L10; Bharatpur test; glasshouse data; writing']], 0.45, 3.55, 12.43, [1.3, 11.13], { firstCol: true, fs: 13 });
// ------------------------------------------------------------------ references
const REFS = JSON.parse(fs.readFileSync(__dirname + '/deck_refs.json', 'utf8'));
const third = Math.ceil(REFS.length / 3);
[REFS.slice(0, third), REFS.slice(third, 2 * third), REFS.slice(2 * third)].forEach((part, i) => {
  s = S('Key references (' + (i + 1) + '/3)', 'References');
  const h1 = Math.ceil(part.length / 2);
  [part.slice(0, h1), part.slice(h1)].forEach((col, j) => T(s, col.map((r, k) => ({ text: r, options: { breakLine: k < col.length - 1, paraSpaceAfter: 3 } })), 0.45 + j * 6.3, 1.15, 6.15, 5.85, { fontSize: 9.5 }));
});
s = pres.addSlide({ masterName: 'TITLE', sectionTitle: 'Outputs' });
s.addText('Thank you', { placeholder: 'title' });
s.addText('Suggestions of the Advisory Committee are welcome', { placeholder: 'body' });
const { applyTheme } = require(process.env.SKILL_DIR + '/scripts/apply_theme.js');
const OUT = process.env.OUT;
pres.writeFile({ fileName: OUT }).then(async f => { await applyTheme(OUT, THEME); console.log('saved', f); });
