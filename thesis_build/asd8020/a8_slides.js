// Seminar slides: methodology -> results (Objectives 1 and 2; Objective 3 not addressed: no pre-symptomatic dates) -> discussion -> conclusions. Native charts where PowerPoint can draw them.
const { pres, sec, slide, bullets, card, img, caption, chart, tbl, DATA, FG, GRADE_COLS, OUT, THEME, applyTheme, W } = require('./a8_ppt.js');
const C = pres.SchemeColor;
const GR = [0, 1, 3, 5, 7, 9];
const O1 = DATA.O1, MT = DATA.metrics, BEST = DATA.best;
const ML = ['SVM', 'RF', 'XGBoost', 'k-NN', 'PLS-DA', 'PLS'];
const f2 = v => (v === null || v === undefined || Number.isNaN(v)) ? '–' : Number(v).toFixed(2);
const f3 = v => (v === null || v === undefined || Number.isNaN(v)) ? '–' : Number(v).toFixed(3);
const row = (t, m) => MT.find(r => r.task === t && r.model === m);
const mn = (m, t) => t === 'C' ? ({ SVM: 'SVR', PLS: 'PLSR' }[m] || m) : m;
const rA = row('A', BEST.A.overall), rB = row('B', BEST.B.overall), rC = row('C', BEST.C.overall);
const dte = { A: row('A', 'DT-EDNet'), B: row('B', 'DT-EDNet'), C: row('C', 'DT-EDNet') };
const HASDL = !!(dte.A && dte.B && dte.C);
const N = DATA.n; const LBL = DATA.label, SP = DATA.split;
function stat(s, x, y, w, big, label, col = '2C5F2D') {
  s.addShape(pres.shapes.ROUNDED_RECTANGLE, { x, y, w, h: 1.35, fill: { color: 'EEF3E8' }, line: { color: 'EEF3E8' }, rectRadius: 0.08, objectName: 'stat' });
  s.addText(big, { x, y: y + 0.08, w, h: 0.72, fontSize: 30, bold: true, color: col, align: 'center', isTextBox: true, margin: 0, fontFace: 'Cambria' });
  s.addText(label, { x: x + 0.1, y: y + 0.8, w: w - 0.2, h: 0.5, fontSize: 12, color: '1B2A1E', align: 'center', isTextBox: true, margin: 0, fit: 'shrink' });
}
function flow(s, items, y, cols = ['1F3864', '1F6FB2', '1F6FB2', '1F6FB2', '1F6FB2', '1F6FB2'], h = 1.55) {
  const n = items.length, gap = 0.22, w = (12.3 - gap * (n - 1)) / n;
  items.forEach((t, i) => {
    const x = 0.5 + i * (w + gap), c = cols[i % cols.length];
    s.addShape(pres.shapes.ROUNDED_RECTANGLE, { x, y, w, h, fill: { color: 'FFFFFF' }, line: { color: c, width: 1.5 }, rectRadius: 0.08, objectName: 'flow' + i });
    s.addText(t[0], { x: x + 0.08, y: y + 0.06, w: w - 0.16, h: 0.42, fontSize: 13, bold: true, color: c, align: 'center', isTextBox: true, margin: 0, fit: 'shrink' });
    s.addText(t[1], { x: x + 0.08, y: y + 0.5, w: w - 0.16, h: h - 0.56, fontSize: 12.5, color: '1B2A1E', align: 'center', valign: 'top', isTextBox: true, margin: 0, fit: 'shrink' });
    if (i < n - 1) s.addShape(pres.shapes.RIGHT_TRIANGLE, { x: x + w + 0.04, y: y + h / 2 - 0.09, w: 0.14, h: 0.18, fill: { color: '8A9A8C' }, line: { color: '8A9A8C' }, rotate: 90 });
  });
}
const lineData = obj => obj.series.map(s => ({ name: s.name, labels: obj.labels, values: s.values }));

// =============================== TITLE
let s = pres.addSlide({ masterName: 'TITLE' });
s.addText('Leaf-level hyperspectral detection and severity estimation of white rust in Indian mustard', { placeholder: 'title' });
s.addText([{ text: 'ASD contact-probe spectra, 2025-26 (natural infection), ' + N + ' leaves: grouped ' + LBL + ' hold-out compared with leave-one-replication-out (LORO)', options: { breakLine: true } }, { text: 'Animesh Panda | Ph.D. Agricultural Physics | ICAR-IARI, New Delhi', options: { breakLine: true } }, { text: 'Objective 1: spectral response and features | Objective 2: machine and deep learning' }], { placeholder: 'body' });
s.addNotes('Title. This talk presents the complete analysis of the 2025-26 leaf spectra, from methodology to discussion.');

s = slide('Outline', 'Order of the talk.');
[['1', 'Introduction and objectives'], ['2', 'Materials and methods: data collection to analysis steps'], ['3', 'Results: spectral response and features (Objective 1)'], ['4', 'Results: models (Objective 2) and robustness'], ['5', 'Discussion, conclusions and next steps']].forEach((t, i) => {
  const y = 1.35 + i * 1.08; s.addShape(pres.shapes.OVAL, { x: 0.9, y, w: 0.75, h: 0.75, fill: { color: '2C5F2D' }, line: { color: '2C5F2D' } });
  s.addText(t[0], { x: 0.9, y, w: 0.75, h: 0.75, fontSize: 22, bold: true, color: 'FFFFFF', align: 'center', valign: 'middle', isTextBox: true, margin: 0 });
  s.addText(t[1], { x: 1.9, y, w: 6.5, h: 0.75, fontSize: 20, color: '1B2A1E', valign: 'middle', isTextBox: true, margin: 0 });
});
stat(s, 9.2, 1.35, 3.4, String(N), 'leaf spectra (350–2500 nm)'); stat(s, 9.2, 2.9, 3.4, '4 dates', '11 Feb – 13 Mar 2026, natural infection'); stat(s, 9.2, 4.45, 3.4, '11 models', '6 machine learning (incl. PLS-DA and PLSR) + 5 deep learning');

// =============================== INTRODUCTION
sec('Introduction', 'White rust, visual scoring and leaf spectroscopy');
s = slide('Why leaf spectra of white rust?', 'Motivation: objective, non-destructive scoring that can be transferred to UAV sensors.');
card(s, 0.5, 1.3, 3.95, 3.3, 'The disease', 'Albugo candida forms white pustules on the lower leaf surface with chlorosis and necrosis above; systemic infection causes stag heads and yield loss. Cool, humid weather favours epidemics (Saharan et al., 2014; Chattopadhyay et al., 2011).', undefined, undefined, 17);
card(s, 4.68, 1.3, 3.95, 3.3, 'The problem', 'Visual 0–9 grades are subjective; raters disagree most between neighbouring grades (Bock et al., 2010). A plot-scale, objective method is needed for breeding and management.', undefined, undefined, 17);
card(s, 8.86, 1.3, 3.95, 3.3, 'The approach', 'Reflectance responds to pigment, structure and water changes caused by a pathogen (Mahlein, 2016). Leaf spectra give the pure leaf signal without canopy or soil effects – the basis for the UAV phase (Meng et al., 2020).', undefined, undefined, 17);
s.addText('Methods of the DT-EDNet rice-blast study (Ma et al., 2026) are applied: effective ranges → SHAP-CARS → indices → ReliefF → models including DT-EDNet.', { x: 0.5, y: 4.9, w: 12.3, h: 0.8, fontSize: 15, italic: true, color: '2C5F2D', isTextBox: true });
s = slide('Objectives of this analysis');
card(s, 0.5, 1.3, 3.95, 3.3, 'Objective 1', 'Spectral response of leaves to white rust severity and a compact disease-specific feature set (optimal wavelengths, White Rust Index, ReliefF indices, VIF).', undefined, undefined, 18);
card(s, 4.68, 1.3, 3.95, 3.3, 'Objective 2', 'Models for (A) detection, (B) six grades and (C) severity score: SVM, RF, XGBoost, k-NN, PLS-DA/PLSR, DNN-F1, DT-EDNet, EfficientNet-B0, ResNet18, ConvNeXt V2-Atto; ablation, SHAP and robustness.', '7030A0', 'EDE2F6', 18);
card(s, 8.86, 1.3, 3.95, 3.3, 'Reference without sensors', 'Covariate baseline (Step 2.5.5): what do crop age, sowing timing, variety, growth stage and weather explain without spectra, and what do the spectra add?', 'C98A00', 'FFF4D6', 18);
s.addText('Objective 3 (pre-symptomatic detection) is not addressed: no pre-symptomatic dates were sampled in 2025-26; it is planned for the 2026-27 flights.', { x: 0.5, y: 6.4, w: 12.3, h: 0.45, fontSize: 13, italic: true, color: 'B71C1C', isTextBox: true, fit: 'shrink' });
stat(s, 0.5, 4.95, 3.95, 'Task A', 'detection: healthy vs diseased leaf'); stat(s, 4.68, 4.95, 3.95, 'Task B', 'six grades 0, 1, 3, 5, 7, 9', '7030A0'); stat(s, 8.86, 4.95, 3.95, 'Task C', 'severity score 0–9 (regression)', 'B71C1C');

// =============================== METHODS
sec('Materials and methods', 'Experiment, data, validation, pre-processing and the analysis steps');
s = slide('Workflow: from data collection to discussion', 'Sixteen steps from the field experiment to the discussion; colours = phases.');
img(s, FG + 'f00_workflow.png', 0.9, 1.1, 11.5, 5.9);
s = slide('Experiment and field layout', 'Design of the 2025-26 experiment.');
tbl(s, [['Item', 'Detail'], ['Plots', '48 plots, 5 m × 3.5 m; 0.5-m bunds, 2-m channels; field 48 m × 24 m'], ['Blocks', 'healthy block 1–12 (fungicide-sprayed); R3 13–24, R2 25–36, R1 37–48 (unsprayed)'],
  ['Treatments', '3 varieties (V1, V2, V3) × 4 sowing dates (D1–D4) in every block'], ['Infection', 'natural infection; no artificial inoculation'], ['Leaves', 'L3, L5 (3rd, 5th fully expanded from top) and LL (lowest green leaf)'], ['Instrument', 'ASD contact probe, 350–2500 nm, splice-corrected']], 0.5, 1.3, 7.3, [1.6, 5.7], 13);
tbl(s, [['Timing', 'Sowing', 'Treatment', 'Reached on', 'DAS at the 4 dates'], ...['D1', 'D2', 'D3', 'D4'].map((t, i) => [t, ['9 Dec 2025', '18 Dec 2025', '27 Dec 2025', '9 Jan 2026'][i], ['50', '40', '30', '20'][i] + ' DAS', DATA.das0[t], DATA.das_by[t].join(', ')])], 8.0, 1.3, 4.8, [0.65, 1.05, 0.85, 0.9, 1.35], 12);
s.addText('Natural infection: the four sowing dates give crops of four ages (50, 40, 30, 20 days after sowing at the end of January 2026) exposed to the same inoculum and weather. Crop age at sampling (DAS) is the time variable.', { x: 8.0, y: 3.95, w: 4.8, h: 1.5, fontSize: 12, color: '2C5F2D', isTextBox: true, fit: 'shrink' });
s = slide('Data collection: leaf spectra and disease scoring', 'Step A4: how every leaf spectrum and its grade were recorded on the four sampling dates.');
flow(s, [['1. Plots', 'all 48 plots on each date (healthy block + R1–R3)'], ['2. Leaves', 'L3 and L5 (3rd, 5th fully expanded from top) and LL (lowest green leaf)'], ['3. Contact probe', 'ASD FieldSpec + leaf clip, own halogen light (Milton et al., 2009)'],
  ['4. Spectrum', '350–2500 nm, 1 nm, splice-corrected'], ['5. Score', '0–9 grade of the same leaf (0, 1, 3, 5, 7, 9)'], ['6. Files', 'one Excel file per date; 7 header rows per leaf column']], 1.2, ['1F3864', '1F6FB2', '1F6FB2', '1F6FB2', 'B71C1C', '2C5F2D'], 1.75);
tbl(s, [['Date', 'DAS', 'L3', 'L5', 'LL', 'Leaves', 'Leaves per plot'], ...DATA.leafpos.map((r, i) => [r.date, DATA.dates[i].DAS, r.L3, r.L5, r.LL, r.n, r.med + ' (' + r.mn + '–' + r.mx + ')'])], 0.5, 3.25, 7.6, [1.3, 0.9, 0.8, 0.8, 0.8, 0.9, 2.1], 13);
bullets(s, ['Header rows: wavelength, plot no., variety, growth stage, healthy/diseased, leaf level, score.', 'Plot-average columns in the files were not used (leaf-level analysis).', 'Nine spectra labelled L4 (11 Feb) are not a sampled position and were removed.'], 8.4, 3.25, 4.4, 3.0, 14);
caption(s, 'Leaves per plot = median (range) per plot and date. DAS = crop age in days after sowing (range over D1–D4).');
s = slide('Weather data and covariates', 'Step A6: daily weather from the IARI observatory; covariates known without any sensor.');
tbl(s, [['Date', 'Tmax 7 d', 'Tmin 7 d', 'RH I 7 d', 'RH II 7 d', 'Rain 7 d', 'Fav. leaf days in 7 d', 'Fav. leaf days since sowing D1/D2/D3/D4', 'Staghead days'], ...DATA.cov2_dates.map(r => [r.date.slice(0, 10), r.Tmax7.toFixed(1), r.Tmin7.toFixed(1), r.RH1_7.toFixed(0), r.RH2_7.toFixed(0), r.rain7.toFixed(1), r.fav7_leaf, [r.fav_leaf_D1, r.fav_leaf_D2, r.fav_leaf_D3, r.fav_leaf_D4].join(' / '), r.fav_staghead_max])],
  0.5, 1.3, 12.3, [1.3, 1.0, 1.0, 1.0, 1.0, 1.0, 1.4, 2.6, 2.0], 13);
card(s, 0.5, 3.6, 6.0, 2.9, 'Weather covariates', '• Daily Tmax, Tmin, RH I (morning), RH II (afternoon), rainfall, wind, sunshine, evaporation (1 Dec 2025 – 20 Mar 2026).\n• 7-day means (rain: total) ending the DAY BEFORE each date → no look-ahead.\n• Favourable days from each sowing (Chattopadhyay et al., 2011): leaf infection Tmax 16–24 °C, RH I > 97%, RH II > 40%; staghead Tmax 20–29 °C, Tmin > 12 °C, RH I > 97%.\n• Natural infection: ' + DATA.fav.n + ' favourable leaf days from ' + DATA.fav.first + ' to ' + DATA.fav.last + ', none during sampling.', undefined, undefined, 13);
card(s, 6.8, 3.6, 6.0, 2.9, 'Leaf and plot covariates', '• Crop age at sampling: days after sowing (DAS), ' + DATA.dates[0].DAS.split('–')[0] + '–' + DATA.dates[3].DAS.split('–')[1] + ' days.\n• Sowing timing D1–D4: 50, 40, 30, 20 DAS treatments (sown 9 Dec, 18 Dec, 27 Dec 2025, 9 Jan 2026).\n• Variety V1, V2, V3.\n• Growth stage: vegetative, flowering, pod formation → 1, 2, 3 (BBCH ranges; Lancashire et al., 1991).', '7030A0', 'EDE2F6', 14);
s = slide('Data organisation and quality control', 'From four raw Excel files to one checked leaf table.');
flow(s, [['Parse', N + ' leaf columns (.sco); plot averages skipped'], ['Join layout', 'plot → block, timing, variety; variety agreed for 48/48 plots'], ['Labels', 'grade; diseased = grade > 0; healthy block all grade 0'], ['Derived', 'crop age (DAS), stage code'], ['Checks', 'grades 0–9 only; 1-nm grid; no missing values; range'], ['Folds', 'each leaf → outer fold of its plot']], 1.2, ['1F3864', '1F6FB2', '1F6FB2', '1F6FB2', 'B71C1C', '2C5F2D'], 1.65);
stat(s, 0.5, 3.2, 2.9, String(N), 'leaf spectra × ' + DATA.qc.bands + ' bands'); stat(s, 3.6, 3.2, 2.9, '48 / 48', 'plots on every date'); stat(s, 6.7, 3.2, 2.9, String(DATA.qc.nan), 'missing values', 'B71C1C'); stat(s, 9.8, 3.2, 3.0, DATA.qc.rmin.toFixed(3) + '–' + DATA.qc.rmax.toFixed(3), 'reflectance range', '1565C0');
bullets(s, ['Healthy (fungicide-sprayed) block: ' + DATA.qc.n_healthy_block + ' leaves, ' + DATA.qc.healthy_block_diseased + ' with grade > 0.', 'Unsprayed (naturally infected) plots: ' + DATA.qc.n_inoc + ' leaves (' + DATA.qc.n_inoc_healthy + ' grade 0, ' + DATA.qc.n_inoc_dis + ' diseased) – the sample of the covariate baseline.', DATA.qc.mn + '–' + DATA.qc.mx + ' leaves per plot and date (median ' + DATA.qc.med + ').'], 0.5, 4.8, 12.3, 1.8, 15);
s = slide('Data: leaves by date and grade', 'Native chart: edit the data in PowerPoint or in the Excel sheet 2_Counts.');
const cd = DATA.counts.date;
chart(s, pres.charts.BAR, cd.series.map(x => ({ name: x.name, labels: DATA.dates.map(d => d.date.slice(5) + ' (' + d.DAS + ' DAS)'), values: x.values })), { x: 0.5, y: 1.2, w: 7.4, h: 5.4, barDir: 'col', barGrouping: 'stacked', chartColors: GRADE_COLS, showLegend: true, legendPos: 'b', showTitle: true, title: 'Leaves per sampling date, by grade', valAxisTitle: 'Leaves', showValAxisTitle: true });
tbl(s, [['Date', 'DAS', 'Leaves', 'Mean grade', 'Diseased %'], ...DATA.dates.map(d => [d.date, d.DAS, d.n, f2(d.mean_grade), Number(d.pct).toFixed(0)])], 8.2, 1.3, 4.6, [1.25, 0.75, 0.75, 0.95, 0.9], 12);
s.addText('Grades 0/1/3/5/7/9: ' + GR.map(g => DATA.grade_n[g]).join(' / ') + ' leaves. Grade 9 is the smallest class.', { x: 8.2, y: 4.2, w: 4.6, h: 1.0, fontSize: 13, color: '1B2A1E', isTextBox: true });
s = slide('Tasks and validation design', 'Grouped, stratified ' + LBL + ' hold-out: whole plots are either training or test plots.');
tbl(s, [['Task', 'Target', 'Main metric'], ['A detection', 'grade 0 vs > 0', 'macro-F1, AUC'], ['B six grades', '0, 1, 3, 5, 7, 9', 'macro-F1, QWK'], ['C severity score', '0–9 (regression)', 'R², RMSE, RPD']], 0.5, 1.3, 6.0, [1.8, 2.2, 2.0], 14);
tbl(s, [['Set', 'Plots (healthy + unsprayed)', 'Leaves', 'Mean grade'], ...DATA.split_sets.map(r => [r.set, r.plots + ' (' + r.healthy + ' + ' + r.unsprayed + ')', r.leaves + ' (' + Math.round(100 * r.leaves / N) + '%)', f2(r.mean_grade)])], 6.8, 1.3, 6.0, [1.2, 2.2, 1.5, 1.1], 13);
s.addText('Test plots: healthy ' + SP.test_healthy_plots.join(', ') + '; unsprayed ' + SP.test_unsprayed_plots.join(', ') + ' (one per treatment, spread over R1–R3, varieties and timings; seed ' + 2026 + ').', { x: 6.8, y: 2.75, w: 6.0, h: 0.9, fontSize: 12, color: '444444', isTextBox: true, margin: 0, fit: 'shrink' });
bullets(s, ['Leaves of one plot share soil, microclimate and inoculum → random leaf splits inflate accuracy, so whole plots are split (Roberts et al., 2017).', 'Feature selection, SFFS and tuning on the training plots only; inner GroupKFold(3) by plot; networks stop early on one third of the training plots (Varma and Simon, 2006).', 'The ' + SP.n_test_leaves + ' test leaves are used once; uncertainty from a plot bootstrap of the test set (Field and Welsh, 2007). The earlier LORO analysis is compared in a separate section.'], 0.5, 3.9, 12.3, 2.6, 15);
s = slide('Pre-processing and spectral features', 'Steps B3, D3 and D4 of the methodology for leaf spectra.');
flow(s, [['Raw spectra', '350–2500 nm, 1 nm, splice-corrected'], ['Smoothing', 'Savitzky–Golay, window 11, order 2 (Savitzky and Golay, 1964)'], ['Range', '400–2400 nm; water bands KEPT (contact probe, own light)'], ['First derivative', 'same filter; sharpens the red edge (Tsai and Philpot, 1998)'], ['Features', '5-nm R and FD (802); 41 indices + REP, Dr, REarea']], 1.4, undefined, 2.0);
bullets(s, ['No second derivative (agreed rule: amplifies noise).', 'Plot-average columns in the files were skipped: analysis at leaf level.', 'Data-driven indices added in Objective 1: NDSI_best, RSI_best and the White Rust Index (WRI).'], 0.5, 3.8, 12.3, 2.5, 16);
s = slide('Objective 1: steps', 'Activities 1.1–1.6 for the leaf spectra.');
flow(s, [['1.1 Response', 'mean and derivative spectra, correlation, strata'], ['1.2 Effective ranges', 'NDSI/RSI R² maps; R² ≥ 0.5 or top 5%'], ['1.2 SHAP-CARS', 'XGBoost SHAP top 40% → CARS 50 × 20 runs; ≥ 50%'], ['1.3 Indices', 'best NDSI, RSI; WRI = NDSI + w·R_λ3'], ['1.4 ReliefF', '|r| ≥ 0.95 filter; ReliefF / RReliefF, top 5'], ['1.6 VIF', 'pool OW + VI; remove until VIF < 10 → DSF']], 1.4, undefined, 2.1);
bullets(s, ['References: Ma et al. (2026) for maps and SHAP-CARS; Li et al. (2009) for CARS; Lundberg and Lee (2017) for SHAP; Robnik-Šikonja and Kononenko (2003) for ReliefF; Dormann et al. (2013) for collinearity.', 'Red-edge derivatives (680–760 nm) always kept as candidates; reflectance and derivatives pooled in one SHAP-CARS run.'], 0.5, 3.9, 12.3, 2.6, 15);
s = slide('Objective 2: models and training', 'Activities 2.1–2.4.');
tbl(s, [['Model', 'Tuning (inner grouped folds)'], ['SVM / SVR', 'C, γ (ε for SVR) grid'], ['Random forest', '500 trees; max_features, min_samples_leaf'], ['XGBoost', 'trees, depth, learning rate'], ['k-NN', 'k = 3–11, weights'], ['PLS-DA / PLSR', '1–15 components'], ['All ML', 'SFFS ≤ 15 features (smallest within 1% of best)']], 0.5, 1.3, 5.9, [1.8, 4.1], 14);
tbl(s, [['Network', 'Input / setting'], ['DNN-F1', 'feature vector; 64–32 units'], ['DT-EDNet', '4 × 4 pseudo-image; SE + dual transformer group'], ['EfficientNet-B0', 'MBConv blocks, stride-1 stem'], ['ResNet18', 'residual blocks, stride-1 stem'], ['ConvNeXt V2-Atto', 'GRN blocks, stride-1 stem'], ['Training (paper)', 'AdamW 6e-4, cosine, batch 32, ≤ 100 epochs, patience 20, seed 42']], 6.7, 1.3, 6.1, [1.8, 4.3], 14);
s.addText('Pseudo-image: p selected features placed in a k × k grid (k = ⌈√p⌉, zero-padded) (Sharma et al., 2019; Ma et al., 2026).', { x: 0.5, y: 5.9, w: 12.3, h: 0.6, fontSize: 14, italic: true, color: '2C5F2D', isTextBox: true });
s = slide('DT-EDNet architecture (Ma et al., 2026)', 'Embedding → squeeze-and-excitation → dual transformer group → class token → output.');
flow(s, [['Pseudo-image', 'k × k, 1 channel'], ['Embedding', '3 × 3 conv, 128 channels, BN, GELU'], ['SE', 'channel re-weighting (Hu et al., 2018)'], ['Kernel transformer block', '3 × 3 conv + CBAM (Woo et al., 2018)'], ['4 token transformer blocks', 'class token + positions; 4 heads (Vaswani et al., 2017)'], ['Output', 'LayerNorm(class token) → linear: 2, 6 classes or score']], 1.5, ['6A2C9A'], 2.0);
bullets(s, ['Ablation: without SE, without the dual transformer group (DTG), without both.', 'Comparison networks from the same paper: EfficientNet-B0 (Tan and Le, 2019), ResNet18 (He et al., 2016), ConvNeXt V2 (Woo et al., 2023).', 'Feature configurations compared: optimal wavelengths (OW), selected indices (VI), disease-specific set (DSF).'], 0.5, 3.9, 12.3, 2.6, 15);
s = slide('Evaluation and interpretation', 'Metrics and additional analyses.');
tbl(s, [['Metric', 'Meaning'], ['OA, kappa', 'accuracy; agreement beyond chance (Cohen, 1960)'], ['Macro-F1', 'mean F1 of classes; small classes count equally'], ['AUC', 'area under the ROC curve (Fawcett, 2006)'], ['QWK', 'weighted kappa, ordinal grades (Cohen, 1968)'], ['R², RMSE, RPD', 'regression; RPD = SD/RMSE (Williams, 2001)']], 0.5, 1.3, 6.2, [1.8, 4.4], 15);
bullets(s, ['SHAP of XGBoost on the disease-specific set', 'Strata: stage, variety, leaf position, date', 'Leave-one-variety-out and leave-one-timing-out', 'Selection stability across folds', 'Covariate baseline without sensor data (next three slides)', 'Final models refitted on all leaves and saved'], 7.0, 1.3, 5.8, 5.2, 17);

s = slide('Covariate baseline: purpose and inputs', 'Step 2.5.5. A model built WITHOUT spectra, from what is known about the leaf, plot and season. The spectra are credited only with what they add to it.');
card(s, 0.5, 1.25, 6.0, 4.3, 'Why a model without sensor data?', '• Calendar effect: severity rises with crop age and sampling date and differs with variety, sowing timing, stage and weather; a spectral model can look good only by learning the calendar (De Wolf and Isard, 2007).\n• Weather alone predicted disease severity (Bijlwan et al., 2025).\n• Sensors add to weather: reflectance + meteorological data raised accuracy from 69% to 78% for wheat powdery mildew (Zhang et al., 2014; Ruan et al., 2022).\n• Rule: spectra are useful only if they beat the covariate-only model (Kuhn and Johnson, 2013).', '1565C0', 'E3F2FD', 14);
tbl(s, [['Covariate (no spectra)', 'Coding'], ['Crop age (days after sowing)', 'numeric, ' + DATA.dates[0].DAS.split('–')[0] + '–' + DATA.dates[3].DAS.split('–')[1] + ' DAS'], ['Sowing timing D1–D4', 'one-hot (50, 40, 30, 20 DAS treatments)'], ['Variety V1–V3', 'one-hot'], ['Growth stage', '1 vegetative, 2 flowering, 3 pod formation'],
  ['7-day weather', 'Tmax, Tmin, RH I, RH II, rain (ending the day before)'], ['Favourable days since sowing', 'leaf infection; staghead (Chattopadhyay et al., 2011)']], 6.8, 1.25, 6.0, [2.3, 3.7], 13);
card(s, 6.8, 4.55, 6.0, 1.95, 'Samples', 'Unsprayed, naturally infected leaves only: n = ' + DATA.qc.n_inoc + ' (' + DATA.qc.n_inoc_healthy + ' healthy, ' + DATA.qc.n_inoc_dis + ' diseased). The sprayed healthy plots share every covariate with the unsprayed plots and would teach a false rule.', 'C98A00', 'FFF4D6', 14);
s = slide('Covariate baseline: models and comparison design', 'Three models per input, same ' + LBL + ' split, same inner tuning grouped by plot.');
tbl(s, [['Model', 'A detection', 'B six grades', 'C score', 'Covariates'], ['B1 statistical (interpretable)', 'logistic regression', 'proportional-odds ordinal logistic (McCullagh, 1980)', 'linear with DAS, DAS² (Madden et al., 2007)', 'variety, timing, stage, DAS, DAS²'],
  ['Random forest (Breiman, 2001)', 'tuned', 'tuned', 'tuned (= best ML)', 'all incl. weather, favourable days'], ['B2 best ML of Activity 2.2', 'SVM', 'XGBoost', 'random forest', 'all incl. weather, favourable days']], 0.5, 1.25, 12.3, [2.7, 2.0, 2.9, 2.6, 2.1], 13);
tbl(s, [['Model set', 'Input', 'Question answered'], ['M0 covariate baseline', 'covariates only – the stronger of B1, RF, B2', 'how much do time, stage, variety and weather explain?'], ['M1 sensor model', 'leaf spectra (fold-wise disease-specific features), B2', 'what do the spectra achieve alone?'], ['M2 sensor + covariates', 'spectra + covariates, B2', 'does known context add to the spectra?']], 0.5, 3.45, 12.3, [2.7, 4.6, 5.0], 13);
s.addText('With only four dates the 7-day weather is collinear with the date and favourable days since sowing with the timing; in B1 the time effect is carried by DAS and DAS². Standardisation with training statistics only.', { x: 0.5, y: 5.6, w: 12.3, h: 0.8, fontSize: 14, italic: true, color: '2C5F2D', isTextBox: true });
s = slide('Covariate baseline: gain of the spectra and decision rule', 'One test set: whole test plots are resampled to judge each gain.');
card(s, 0.5, 1.25, 6.0, 2.1, 'Gains', 'ΔS (spectra) = metric(M1) − metric(M0)\nΔC (covariates added) = metric(M2) − metric(M1)\nΔT (both) = metric(M2) − metric(M0)\nA: macro-F1, AUC, balanced accuracy;  B: macro-F1, QWK;  C: R², RMSE', '1565C0', 'E3F2FD', 15);
card(s, 0.5, 3.55, 6.0, 2.95, 'Is the gain real?', '• Plot-block bootstrap: 2000 resamples of whole plots → 95% CI of Δ (Efron and Tibshirani, 1993).\n• Detection AUC: DeLong test of correlated ROC curves (DeLong et al., 1988).\n• Real gain = CI excludes 0 AND |Δ| > fold-to-fold SD AND same sign in all three folds.', undefined, undefined, 15);
tbl(s, [['Outcome', 'Meaning'], ['M1 > M0 (CI above 0)', 'spectra see disease beyond calendar and stage'], ['M1 ≈ M0', 'spectra mainly track time or stage'], ['M2 > M1', 'known context adds information (within-season use)'], ['M0 high only for detection', 'epidemic level follows time; spectral value lies in grading']], 6.8, 1.25, 6.0, [2.4, 3.6], 14);
s.addText('The baseline is applied to all three tasks (detection, six grades, severity score) on the same folds as the spectral models.', { x: 6.8, y: 4.6, w: 6.0, h: 1.2, fontSize: 14, italic: true, color: '2C5F2D', isTextBox: true, fit: 'shrink' });

// =============================== RESULTS OBJECTIVE 1
sec('Results – Objective 1', 'Spectral response and disease-specific features');
s = slide('Dataset composition', 'Leaves by date, growth stage, variety and leaf position.');
img(s, FG + 'f01_dataset.png', 1.9, 1.15, 9.5, 5.6);
s = slide('Disease progress and weather', 'Natural infection: favourable weather in December–January, warm and dry weather during sampling.');
img(s, FG + 'f15_weather_progress.png', 0.5, 1.15, 9.0, 5.3);
const pr = DATA.prog;
tbl(s, [['Date', 'Grade', 'Dis. %', 'Tmax 7 d'], ...pr.map((r, i) => [DATA.dates[i].date.slice(5), f2(r.mean_grade), Number(r.pct_diseased).toFixed(0), Number(r.Tmax7).toFixed(1)])], 9.8, 1.4, 3.0, [0.7, 0.7, 0.7, 0.9], 12);
s.addText(DATA.fav.n + ' favourable leaf-infection days (Tmax 16–24 °C, RH I > 97%, RH II > 40%; Chattopadhyay et al., 2011) from ' + DATA.fav.first + ' to ' + DATA.fav.last + '; none during the sampling period.', { x: 9.8, y: 3.8, w: 3.0, h: 1.8, fontSize: 12, color: '1B2A1E', isTextBox: true, fit: 'shrink' });
s = slide('Mean leaf spectra by grade', 'Native line chart (10-nm steps); water bands kept.');
chart(s, pres.charts.LINE, lineData(DATA.mean_spectra), { x: 0.5, y: 1.2, w: 8.6, h: 5.5, chartColors: GRADE_COLS, lineSize: 2, lineDataSymbol: 'none', showLegend: true, legendPos: 'b', showTitle: true, title: 'Mean reflectance, 400–2400 nm', catAxisLabelFrequency: 20, valAxisTitle: 'Reflectance', showValAxisTitle: true, catAxisTitle: 'Wavelength (nm)', showCatAxisTitle: true });
const b = DATA.bands, pc = (w, g) => { const r = b.find(x => x[0] === w); return r[1 + GR.indexOf(g)]; };
stat(s, 9.4, 1.3, 3.4, f3(pc(800, 0)) + ' → ' + f3(pc(800, 9)), 'NIR reflectance at 800 nm (grade 0 → 9)');
stat(s, 9.4, 2.85, 3.4, f3(pc(680, 0)) + ' → ' + f3(pc(680, 9)), 'red reflectance at 680 nm', 'B71C1C');
stat(s, 9.4, 4.4, 3.4, f3(pc(1450, 0)) + ' → ' + f3(pc(1450, 9)), 'water band 1450 nm', '1565C0');
s = slide('Red-edge first derivative and blue shift', 'The red-edge peak falls and moves to shorter wavelengths with severity.');
chart(s, pres.charts.LINE, lineData(DATA.fd_rededge), { x: 0.5, y: 1.2, w: 7.9, h: 5.5, chartColors: GRADE_COLS, lineSize: 2, lineDataSymbol: 'none', showLegend: true, legendPos: 'b', showTitle: true, title: 'First derivative (×10⁻³ nm⁻¹), 500–800 nm', catAxisLabelFrequency: 10 });
chart(s, pres.charts.BAR, [{ name: 'REP (nm)', labels: GR.map(g => 'g' + g), values: DATA.rep }], { x: 8.6, y: 1.2, w: 4.2, h: 2.75, barDir: 'col', chartColors: ['2C5F2D'], showValue: true, dataLabelFormatCode: '0.0', dataLabelPosition: 'outEnd', valAxisMinVal: 695, valAxisMaxVal: 712, showTitle: true, title: 'Red-edge position (nm)', showLegend: false });
chart(s, pres.charts.BAR, [{ name: 'Dr', labels: GR.map(g => 'g' + g), values: DATA.dr }], { x: 8.6, y: 4.0, w: 4.2, h: 2.75, barDir: 'col', chartColors: ['97BC62'], showValue: true, dataLabelFormatCode: '0.0', dataLabelPosition: 'outEnd', valAxisMinVal: 9, valAxisMaxVal: 13.5, showTitle: true, title: 'Red-edge peak Dr (×10⁻³)', showLegend: false });
s = slide('Correlation with the leaf grade', 'The derivative correlates more strongly than reflectance.');
chart(s, pres.charts.LINE, lineData(DATA.corr), { x: 0.5, y: 1.2, w: 9.0, h: 5.5, chartColors: ['1565C0', 'C62828'], lineSize: 2, lineDataSymbol: 'none', showLegend: true, legendPos: 'b', showTitle: true, title: 'Pearson r with grade (n = ' + N + ')', catAxisLabelFrequency: 20, valAxisMinVal: -0.7, valAxisMaxVal: 0.7, valAxisMajorUnit: 0.2, valAxisLabelFormatCode: '0.0' });
stat(s, 9.8, 1.4, 3.0, 'r = ' + f2(O1.corr_FD_max[1]), 'first derivative at ' + O1.corr_FD_max[0] + ' nm', 'C62828');
stat(s, 9.8, 3.0, 3.0, 'r = ' + f2(O1.corr_R_max[1]), 'reflectance at ' + O1.corr_R_max[0] + ' nm', '1565C0');
s = slide('Spectra by growth stage', 'The grade effect appears at every stage; the level changes with stage.');
img(s, FG + 'f13_spectra_by_stage.png', 0.6, 1.3, 12.1, 4.3);
s.addText('Mean grade by stage: ' + DATA.grade_by.stage.map(x => x[0] + ' ' + f2(x[1])).join('; ') + '. Stage and date are linked in this design.', { x: 0.6, y: 5.8, w: 12.1, h: 0.7, fontSize: 14, color: '1B2A1E', isTextBox: true });
s = slide('Effective ranges: NDSI and RSI maps', 'No pair reached R² 0.5 → top 5% of pairs used.');
img(s, FG + 'f05_ndsi_rsi_maps.png', 0.5, 1.15, 8.9, 4.4);
tbl(s, [['Item', 'Result'], ['Threshold', 'R² ≥ ' + f3(O1.eff_thr)], ['Effective ranges', O1.eff_ranges.map(r => r[0] + '–' + r[1]).join(', ') + ' nm'], ['Bands', String(O1.eff_nbands)], ['Best NDSI', '(' + O1.best_ndsi[0] + ', ' + O1.best_ndsi[1] + ') R² ' + f2(O1.best_ndsi[2])], ['Best RSI', '(' + O1.best_rsi[0] + ', ' + O1.best_rsi[1] + ') R² ' + f2(O1.best_rsi[2])]], 9.6, 1.3, 3.2, [1.2, 2.0], 12);
s = slide('Optimal wavelengths by SHAP-CARS', 'All ' + O1.OW.length + ' selected bands are first derivatives.');
img(s, FG + 'f06_shapcars.png', 0.5, 1.15, 7.3, 5.05);
tbl(s, [['Region', 'Optimal wavelengths'], ['Visible', O1.OW.filter(o => +o.slice(2) < 680).join(', ')], ['Red edge / NIR shoulder', O1.OW.filter(o => +o.slice(2) >= 680 && +o.slice(2) < 900).join(', ')], ['NIR–SWIR', O1.OW.filter(o => +o.slice(2) >= 900).join(', ')]], 7.9, 1.3, 4.9, [1.6, 3.3], 13);
s.addText('PLS components: ' + O1.cars_ncomp + '; 20 CARS runs × 50 iterations; kept if ≥ 50% of runs.', { x: 7.9, y: 4.0, w: 4.9, h: 0.8, fontSize: 12, italic: true, color: '6B7B6E', isTextBox: true });
s = slide('Optimal wavelengths on the spectra', 'Red: first-derivative bands; the red edge and NIR shoulder dominate.');
img(s, FG + 'f07_optimal_wavelengths.png', 0.5, 1.3, 12.3, 4.5);
s.addText('Selected: ' + O1.OW.join(', '), { x: 0.5, y: 5.95, w: 12.3, h: 0.6, fontSize: 14, color: '1B2A1E', isTextBox: true });
s = slide('White Rust Index (three-band search)', 'WRI = NDSI(λ₁, λ₂) + w·R(λ₃); the best weight was w = ' + O1.WRI.w + '.');
img(s, FG + 'f08_wri.png', 0.5, 1.2, 8.6, 3.6);
chart(s, pres.charts.BAR, [{ name: 'mean WRI', labels: GR.map(g => 'grade ' + g), values: DATA.wri_by_grade }], { x: 9.3, y: 1.2, w: 3.5, h: 3.6, barDir: 'col', chartColors: ['2C5F2D'], showLegend: false, showTitle: true, title: 'Mean WRI by grade', valAxisLabelFormatCode: '0.000' });
bullets(s, ['WRI = NDSI(' + O1.WRI.l1 + ', ' + O1.WRI.l2 + ') nm, r = ' + f2(O1.WRI.r) + ' with the grade.', 'A third band did not improve the leaf-level index; the excel sheet 8_WRI lets you test other wavelengths and weights.'], 0.5, 5.0, 12.3, 1.5, 15);
s = slide('Index selection: redundancy filter and ReliefF', O1.idx_kept.length + ' indices kept after |r| ≥ 0.95; top five per task.');
img(s, FG + 'f10_relief.png', 0.5, 1.2, 8.8, 3.6);
tbl(s, [['Task', 'Selected indices'], ['Detection', O1.VI_binary.join(', ')], ['Six grades', O1.VI_classes.join(', ')], ['Score', O1.VI_score.join(', ')]], 9.5, 1.3, 3.3, [1.1, 2.2], 12);
s.addText('ReliefF: k = 10 neighbours, neighbours from the same plot excluded (Robnik-Šikonja and Kononenko, 2003).', { x: 0.5, y: 5.0, w: 12.3, h: 0.6, fontSize: 14, italic: true, color: '2C5F2D', isTextBox: true });
s = slide('Disease-specific feature set (VIF < 10)', O1.DSF.length + ' features kept; ' + O1.VIF_removed.length + ' removed for collinearity.');
const vk = Object.keys(DATA.vif).sort((a, b) => DATA.vif[a] - DATA.vif[b]);
chart(s, pres.charts.BAR, [{ name: 'VIF', labels: vk, values: vk.map(k => DATA.vif[k]) }], { x: 0.5, y: 1.2, w: 6.2, h: 5.4, barDir: 'bar', chartColors: ['7030A0'], showValue: true, dataLabelFormatCode: '0.0', dataLabelPosition: 'outEnd', valAxisMaxVal: 12, showLegend: false, showTitle: true, title: 'Variance inflation factor' });
img(s, FG + 'f30_dsf_by_grade.png', 6.9, 1.2, 5.9, 4.4);
s.addText('Removed first (VIF): ' + O1.VIF_removed.slice(0, 5).map(x => x[0] + ' (' + Math.round(x[1]) + ')').join(', '), { x: 6.9, y: 5.75, w: 5.9, h: 0.8, fontSize: 12, color: '1B2A1E', isTextBox: true, fit: 'shrink' });
s = slide('PCA and selection on the training plots', 'Grades form overlapping, ordered clouds; the ' + LBL + ' training set chose features close to the LORO training parts.');
img(s, FG + 'f12_pca.png', 0.5, 1.2, 4.7, 5.2);
tbl(s, [['Training set', 'OW', 'Best NDSI', 'DSF six grades'], [LBL + ' training', DATA.folds['0'].OW.length, '(' + DATA.folds['0'].ndsi.join(', ') + ')', DATA.folds['0'].DSF.B.join(', ')], ...Object.keys(DATA.loro_folds).map(f => ['LORO fold ' + (+f + 1), DATA.loro_folds[f].OW.length, '(' + DATA.loro_folds[f].ndsi.join(', ') + ')', DATA.loro_folds[f].DSF.B.join(', ')])], 5.4, 1.3, 7.4, [1.3, 0.5, 1.1, 4.5], 11);
img(s, FG + 'f29_stability.png', 5.4, 4.2, 7.4, 2.5);

// =============================== RESULTS OBJECTIVE 2
sec('Results – Objective 2', 'Machine learning, deep learning, interpretation and robustness');
s = slide('Floating forward selection and tuning', 'Each model chose its own compact subset inside the training part.');
tbl(s, [['Task', 'Model', 'Candidates', 'Selected', 'Inner score'], ...DATA.sffs.map(r => [r[0], mn(r[1], r[0]), f2(r[3]), f2(r[2]), f3(r[4])])], 0.5, 1.25, 7.0, [0.8, 1.6, 1.5, 1.5, 1.6], 11);
bullets(s, ['SFFS up to 15 features; smallest subset within 1% of the best inner score (Pudil et al., 1994).', 'Grid search with GroupKFold(3) by plot; macro-F1 (A, B) or RMSE (C).', 'Chosen most often over all models and folds: ' + DATA.sffs_top.join(', ') + '.'], 7.8, 1.3, 5.0, 4.5, 14);
function taskBars(t, key, title, lab) {
  const d = MT.filter(r => r.task === t).sort((a, b) => key === 'RMSE' ? b[key] - a[key] : a[key] - b[key]);
  return [{ name: lab, labels: d.map(r => mn(r.model, t)), values: d.map(r => r[key]) }];
}
const mlCol = r => ML.includes(r.model) ? '2E75B6' : '7030A0';
s = slide('Task A – detection', 'Best: ' + BEST.A.overall + ' (macro-F1 ' + f3(rA.macro_F1) + ', AUC ' + f3(rA.AUC) + ').');
const dA = MT.filter(r => r.task === 'A').sort((a, b) => a.macro_F1 - b.macro_F1);
chart(s, pres.charts.BAR, [{ name: 'macro-F1', labels: dA.map(r => r.model), values: dA.map(r => r.macro_F1) }], { x: 0.5, y: 1.2, w: 6.3, h: 5.4, barDir: 'bar', chartColors: dA.map(mlCol), showValue: true, dataLabelFormatCode: '0.000', dataLabelPosition: 'outEnd', valAxisMinVal: 0, valAxisMaxVal: 1, showLegend: false, showTitle: true, title: 'Macro-F1 (blue ML, purple DL)' });
img(s, FG + 'f18_roc.png', 7.1, 1.2, 5.7, 5.3);
s = slide('Task B – six grades', 'Best: ' + BEST.B.overall + ' (macro-F1 ' + f3(rB.macro_F1) + ', QWK ' + f3(rB.QWK) + ', ' + Math.round(100 * rB.within1) + '% within one class).');
const dB = MT.filter(r => r.task === 'B').sort((a, b) => b.macro_F1 - a.macro_F1);
chart(s, pres.charts.BAR, [{ name: 'macro-F1', labels: dB.map(r => r.model), values: dB.map(r => r.macro_F1) }, { name: 'QWK', labels: dB.map(r => r.model), values: dB.map(r => r.QWK) }, { name: 'within one class', labels: dB.map(r => r.model), values: dB.map(r => r.within1) }],
  { x: 0.5, y: 1.2, w: 7.6, h: 5.4, barDir: 'col', barGrouping: 'clustered', chartColors: ['7030A0', '2E75B6', '97BC62'], showLegend: true, legendPos: 'b', valAxisMinVal: 0, valAxisMaxVal: 1, showTitle: true, title: 'Six-grade metrics' });
tbl(s, [['Grade', ...GR.map(String)], ...[...new Set([BEST.B.ML, BEST.B.DL].filter(Boolean))].map(m => ['F1 (' + m + ')', ...GR.map(g => f2(row('B', m)['F1_g' + g]))])], 8.4, 1.3, 4.4, [1.6, 0.47, 0.47, 0.47, 0.47, 0.46, 0.46], 11);
const fg = GR.map(g => [g, rB['F1_g' + g]]).sort((a, b) => b[1] - a[1]);
s.addText('Grade ' + fg[0][0] + ' is recognised best (F1 ' + f2(fg[0][1]) + '); grade ' + fg[5][0] + ' worst (F1 ' + f2(fg[5][1]) + '). Intermediate grades overlap.', { x: 8.4, y: 3.0, w: 4.4, h: 1.4, fontSize: 15, color: '1B2A1E', isTextBox: true });
s = slide('Confusion matrices (six grades)', 'Most errors fall in neighbouring grades.');
img(s, FG + 'f17_confusion.png', 0.8, 1.2, 11.7, 5.1);
s = slide('Per-grade profile of the models', 'Radar of F1 per grade, OA, kappa and macro-F1.');
img(s, FG + 'f19_radar.png', 0.5, 1.15, 6.0, 5.4);
const cand = ['XGBoost', 'RF', 'SVM', 'DT-EDNet', 'DNN-F1'].filter(m => row('B', m));
chart(s, pres.charts.BAR, cand.map(m => ({ name: m, labels: GR.map(g => 'grade ' + g), values: GR.map(g => row('B', m)['F1_g' + g]) })), { x: 6.7, y: 1.2, w: 6.1, h: 5.4, barDir: 'col', barGrouping: 'clustered', chartColors: ['2E75B6', '2E7D32', 'E07B00', '7030A0', 'C62828'], showLegend: true, legendPos: 'b', valAxisMinVal: 0, valAxisMaxVal: 1, showTitle: true, title: 'F1 of each grade' });
s = slide('Task C – severity score', 'Best: ' + mn(BEST.C.overall, 'C') + ' (R² ' + f3(rC.R2) + ', RMSE ' + f2(rC.RMSE) + ' grades, RPD ' + f2(rC.RPD) + ').');
img(s, FG + 'f20_pred_obs.png', 0.5, 1.2, 7.4, 3.3);
const dC = MT.filter(r => r.task === 'C').sort((a, b) => a.RMSE - b.RMSE);
tbl(s, [['Model', 'R²', 'RMSE', 'RPD', 'Bias'], ...dC.map(r => [mn(r.model, 'C'), f3(r.R2), f2(r.RMSE), f2(r.RPD), f2(r.bias)])], 8.1, 1.3, 4.7, [1.6, 0.75, 0.75, 0.75, 0.85], 13);
bullets(s, ['Predictions follow the 1:1 line; extreme grades shrink towards the mean (typical of regression on ordinal scores).', 'RPD ' + f2(rC.RPD) + ': fair for screening, not for exact grading (Williams, 2001).'], 0.5, 4.75, 12.3, 1.8, 15);
s = slide('All models, all metrics', 'Heat-map of the test metrics on the ' + LBL + ' test plots (darker = better within a column).');
img(s, FG + 'f31_metric_heatmap.png', 0.5, 1.3, 12.3, 4.6);
if (HASDL) {
  s = slide('Deep learning: training behaviour', 'Validation on one third of the training plots; early stopping (patience 20).');
  img(s, FG + 'f21_learning_curves.png', 0.6, 1.15, 8.3, 5.4);
  bullets(s, ['DT-EDNet: macro-F1 ' + f3(dte.A.macro_F1) + ' (A), ' + f3(dte.B.macro_F1) + ' (B); R² ' + f3(dte.C.R2) + ' (C).', 'Best networks: ' + BEST.A.DL + ' (A ' + f3(row('A', BEST.A.DL).macro_F1) + '), ' + BEST.B.DL + ' (B ' + f3(row('B', BEST.B.DL).macro_F1) + '), ' + BEST.C.DL + ' (C R² ' + f3(row('C', BEST.C.DL).R2) + ').', 'Validation loss rises after a few epochs (over-fitting); early stopping keeps the best epoch.', 'Pseudo-images are 4 × 4: little spatial structure for convolution and attention.', 'Paper settings, CPU, no separate tuning.'], 9.1, 1.4, 3.7, 5.2, 13);
}
if (DATA.config) {
  s = slide('Networks on three feature configurations', 'Six grades; OW = optimal wavelengths, VI = indices, DSF = disease-specific set.');
  const nets = [...new Set(DATA.config.map(r => r.net))], cfgs = ['OW', 'VI', 'DSF'].filter(c => DATA.config.some(r => r.config === c));
  chart(s, pres.charts.BAR, cfgs.map(c => ({ name: c, labels: nets, values: nets.map(n => (DATA.config.find(r => r.net === n && r.config === c) || {}).macro_F1) })), { x: 0.8, y: 1.2, w: 11.7, h: 5.4, barDir: 'col', barGrouping: 'clustered', chartColors: ['90CAF9', 'A5D6A7', '7030A0'], showValue: true, dataLabelFormatCode: '0.00', dataLabelPosition: 'outEnd', showLegend: true, legendPos: 'b', valAxisMinVal: 0, showTitle: true, title: 'Macro-F1 (six grades)' });
}
if (DATA.ablation) {
  s = slide('DT-EDNet module ablation', 'Contribution of squeeze-and-excitation (SE) and the dual transformer group (DTG).');
  const ab = DATA.ablation;
  chart(s, pres.charts.BAR, ['OA', 'kappa', 'macro_F1', 'QWK'].filter(k => ab[0][k] !== undefined).map(k => ({ name: k.replace('_', '-'), labels: ab.map(r => r.net), values: ab.map(r => r[k]) })), { x: 0.8, y: 1.2, w: 8.0, h: 5.4, barDir: 'col', barGrouping: 'clustered', chartColors: ['90CAF9', '5C9BD5', '7030A0', '97BC62'], showValue: true, dataLabelFormatCode: '0.00', dataLabelPosition: 'outEnd', showLegend: true, legendPos: 'b', valAxisMinVal: 0, showTitle: true, title: 'Six-grade metrics' });
  tbl(s, [['Variant', 'Macro-F1'], ...ab.map(r => [r.net, f3(r.macro_F1)])], 9.1, 1.4, 3.7, [2.4, 1.3], 12);
}
s = slide('Interpretation with SHAP', 'Which features drive the predicted severity score?');
img(s, FG + 'f24_shap.png', 0.5, 1.2, 12.3, 5.1);
s = slide('Robustness by stratum', 'Six-grade macro-F1 by growth stage, variety, leaf position and date.');
img(s, FG + 'f25_strata.png', 1.6, 1.15, 10.1, 5.55);
if (DATA.transfer) {
  s = slide('Transfer to a new variety or timing', 'Random forest trained on the other groups; selection repeated inside.');
  const tb = DATA.transfer.filter(r => r.task === 'B'), tc = DATA.transfer.filter(r => r.task === 'C');
  chart(s, pres.charts.BAR, [{ name: 'macro-F1', labels: tb.map(r => r.test + ' ' + r.level), values: tb.map(r => r.macro_F1) }], { x: 0.5, y: 1.2, w: 6.1, h: 5.4, barDir: 'col', chartColors: ['2E75B6'], showValue: true, dataLabelFormatCode: '0.00', dataLabelPosition: 'outEnd', showLegend: false, valAxisMinVal: 0, valAxisMaxVal: 0.6, showTitle: true, title: 'Six grades: macro-F1 on held-out group' });
  chart(s, pres.charts.BAR, [{ name: 'RMSE', labels: tc.map(r => r.test + ' ' + r.level), values: tc.map(r => r.RMSE) }], { x: 6.8, y: 1.2, w: 6.0, h: 5.4, barDir: 'col', chartColors: ['C62828'], showValue: true, dataLabelFormatCode: '0.00', dataLabelPosition: 'outEnd', showLegend: false, valAxisMinVal: 0, showTitle: true, title: 'Score: RMSE on held-out group' });
}
const CM = DATA.cov2_metrics, CG = DATA.cov2_gains, CS = DATA.cov2_summary;
const cmv = (t, inp, m, k) => (CM.find(r => r.task === t && r.input === inp && r.model === m) || {})[k];
const cg = (t, k, gname) => CG.find(r => r.task === t && r.metric === k && r.gain.startsWith(gname));
const realImp = r => r.real_gain && r.direction === 'improves';
const fg3 = r => (r.delta >= 0 ? '+' : '') + r.delta.toFixed(3) + ' (' + r.ci_low.toFixed(3) + ' to ' + r.ci_high.toFixed(3) + ')' + (realImp(r) ? ' ✓' : (r.real_gain ? ' ✗' : ''));
const m0v = (t, k) => cmv(t, CS[t].M0.input, CS[t].M0.model, k);
s = slide('Covariate baseline: models without and with spectra', 'Unsprayed, naturally infected leaves (n = ' + DATA.qc.n_inoc + '); test leaves of the ' + LBL + ' split.');
img(s, FG + 'f32_cov_models.png', 0.5, 1.15, 12.3, 4.3);
tbl(s, [['Model set', 'Detection macro-F1', 'Detection AUC', 'Six grades macro-F1', 'Six grades QWK', 'Score R²', 'Score RMSE'],
  ...[['M0 covariates only', 'M0'], ['M1 leaf spectra', 'M1'], ['M2 spectra + covariates', 'M2']].map(([lab, k]) => [lab + ' (' + ['A', 'B', 'C'].map(t => CS[t][k].model_name.replace(' (best ML)', '').replace('Linear regression (DAS, DAS²)', 'linear').replace('Ordinal logistic regression', 'ordinal').replace('Logistic regression', 'logistic').replace('Random forest', 'RF')).join(' / ') + ')',
    f3(cmv('A', CS.A[k].input, CS.A[k].model, 'macro_F1')), f3(cmv('A', CS.A[k].input, CS.A[k].model, 'AUC')), f3(cmv('B', CS.B[k].input, CS.B[k].model, 'macro_F1')), f3(cmv('B', CS.B[k].input, CS.B[k].model, 'QWK')), f3(cmv('C', CS.C[k].input, CS.C[k].model, 'R2')), f2(cmv('C', CS.C[k].input, CS.C[k].model, 'RMSE'))])],
  0.5, 5.5, 12.3, [4.1, 1.4, 1.3, 1.5, 1.3, 1.2, 1.5], 12);
s = slide('Gain of the leaf spectra over the covariates', 'ΔS = M1 − M0, ΔC = M2 − M1, ΔT = M2 − M0 with 95% plot-block bootstrap intervals.');
img(s, FG + 'f33_cov_gains.png', 0.4, 1.05, 8.6, 3.47);
tbl(s, [['Gain (95% CI)', 'Detection macro-F1', 'Six grades macro-F1', 'Score R²'], ...[['ΔS', 'ΔS = M1 − M0 (spectra)'], ['ΔC', 'ΔC = M2 − M1 (covariates added)'], ['ΔT', 'ΔT = M2 − M0 (both)']].map(([gn, lab]) => [lab, fg3(cg('A', 'macro_F1', gn)), fg3(cg('B', 'macro_F1', gn)), fg3(cg('C', 'R2', gn))])], 0.5, 4.7, 12.3, [3.0, 3.1, 3.1, 3.1], 13);
const DL2 = DATA.cov2_delong || [];
tbl(s, [['DeLong (detection AUC)', 'AUC', 'p'], ...DL2.map(r => [r.comparison, r.AUC_a.toFixed(3) + ' vs ' + r.AUC_b.toFixed(3), r.p < 0.001 ? '< 0.001' : r.p.toFixed(3)])], 9.2, 1.2, 3.6, [1.2, 1.5, 0.9], 12);
bullets(s, ['✓ real gain: 95% plot-bootstrap CI excludes 0 (one test set, no fold rules); ✗ real loss.', 'Spectra vs calendar (ΔS): ' + ['detection', 'six grades', 'score'].map((n, i) => n + ' ' + (realImp(cg('ABC'[i], ['macro_F1', 'macro_F1', 'R2'][i], 'ΔS')) ? 'real gain' : (cg('ABC'[i], ['macro_F1', 'macro_F1', 'R2'][i], 'ΔS').delta > 0 ? 'positive, not consistent' : 'no gain'))).join('; ') + '.'], 9.2, 2.65, 3.6, 1.95, 12);
if (DATA.cov2_coef && DATA.cov2_coef.length) {
  s = slide('Interpretable covariate model (B1)', 'Standardised effects (per SD) fitted on all unsprayed leaves; red raises, blue lowers disease (p < 0.05).');
  img(s, FG + 'f34_cov_b1.png', 0.5, 1.0, 12.3, 4.5);
  const TN = { variety_V2: 'variety V2', variety_V3: 'variety V3', timing_D2: 'timing D2', timing_D3: 'timing D3', timing_D4: 'timing D4', stage_code: 'growth stage', DAS: 'days after sowing', DAS2: '(DAS)²' };
  const oo = DATA.cov2_coef.filter(r => r.model.startsWith('Ordinal')).filter(r => r.p < 0.05).sort((a, b) => Math.abs(b.estimate) - Math.abs(a.estimate)).slice(0, 5);
  tbl(s, [['Six grades (ordinal B1)', ...oo.map(r => TN[r.term] || r.term)], ['log-odds per SD', ...oo.map(r => (r.estimate >= 0 ? '+' : '') + r.estimate.toFixed(2))], ['odds ratio', ...oo.map(r => Math.exp(r.estimate).toFixed(2))]], 0.5, 5.6, 12.3, [2.3, ...oo.map(() => 10.0 / oo.length)], 12);
  const oc = k => (DATA.cov2_coef.find(r => r.model.startsWith('Ordinal') && r.term === k) || {}).estimate;
  s.addText('Crop age (DAS) ' + (oc('DAS') > 0 ? 'raises' : 'lowers') + ' the grade' + (oc('DAS2') < 0 ? ' at a slowing rate' : '') + '; at the same crop age the latest sowing D4 ' + (oc('timing_D4') > 0 ? 'raises' : 'lowers') + ' it and V3 ' + (oc('variety_V3') > 0 ? 'raises' : 'lowers') + ' it. Weather is not in B1: with four dates it is collinear with date and timing.', { x: 0.5, y: 6.6, w: 12.3, h: 0.4, fontSize: 12, italic: true, color: '2C5F2D', isTextBox: true, fit: 'shrink' });
}

// =============================== COMPARISON WITH LORO
if (DATA.cmp_paired) {
  sec('Comparison with LORO', 'Does the ' + LBL + ' split improve the accuracy?');
  s = slide('Types of split used in plant-disease studies', 'Most papers split images or leaves at random; grouped splits are recommended for dependent samples.');
  tbl(s, [['Split type', 'Example in disease studies'], ['Random hold-out 80:20', 'PlantVillage 80–20 … 20–80 (Mohanty et al., 2016); ≈ 80:20 (Ferentinos, 2018)'], ['Random hold-out 70:30', 'rule of thumb 20–30% for testing (Gholamy et al., 2018); √p : 1 (Joseph, 2022)'],
    ['Train : validation : test (70:15:15)', 'validation tunes, test is used once (Ripley, 1996; Hastie et al., 2009)'], ['Repeated hold-out', 'stripe rust spectra, 80:20 × 100 (Cross et al., 2024)'], ['Leave-one-out / k-fold CV', 'wheat rusts, LOOCV + external test (Wang et al., 2016)'],
    ['Grouped / blocked', 'random hold-outs up to 28% optimistic vs spatial blocks (Kattenborn et al., 2022; Roberts et al., 2017)'], ['This study', 'LORO = grouped CV by replication; ' + LBL + ' = grouped, stratified hold-out of whole plots']], 0.5, 1.3, 12.3, [3.4, 8.9], 13);
  s = slide('How the two designs were compared', 'Four checks, each answering one part of the question.');
  flow(s, [['1 Side by side', 'every metric of every model: LORO vs ' + LBL], ['2 Same test leaves', 'LORO predictions of the ' + SP.n_test_leaves + ' ' + LBL + ' test leaves vs ' + LBL + '; plot bootstrap'], ['3 Repeated splits', 'light pipeline on LORO, the main split and 20 other ' + LBL + ' splits'], ['4 Leakage check', '5 random leaf-level ' + LBL + ' splits (plots ignored)']], 1.4, undefined, 2.2);
  bullets(s, ['A hold-out estimate depends on which plots are tested; with few test plots its variance is large (Kohavi, 1995; Vabalas et al., 2019).', 'A higher ' + LBL + ' number counts as an improvement only if it holds on the same leaves and across other ' + LBL + ' splits.'], 0.6, 4.0, 12.1, 2.2, 16);
  s = slide('1. All models side by side', 'Raw numbers mix the design with the fact that different leaves are tested.');
  img(s, FG + 'f36_cmp_side.png', 0.5, 1.15, 12.3, 4.3);
  const sd_ = (DATA.cmp_side || []).filter(r => r.metric === ({ A: 'macro_F1', B: 'macro_F1', C: 'R2' })[r.task]);
  ['A', 'B', 'C'].forEach((t, i) => { const v = sd_.filter(r => r.task === t).map(r => r['d_' + LBL]); const m = v.reduce((a, b) => a + b, 0) / Math.max(v.length, 1);
    stat(s, 0.5 + i * 4.18, 5.55, 3.95, (m >= 0 ? '+' : '') + m.toFixed(3), 'mean Δ ' + ['detection macro-F1', 'six-grade macro-F1', 'score R²'][i] + ' (' + LBL + ' − LORO)', m >= 0 ? '2C5F2D' : 'B71C1C'); });
  s = slide('2. Same test leaves: the fair comparison', DATA.cmp_summary ? DATA.cmp_summary.summary_sentence : '');
  img(s, FG + 'f37_cmp_paired.png', 0.5, 1.15, 7.4, 5.6);
  const cp = DATA.cmp_paired, cnt = v => cp.filter(r => r.verdict === v).length;
  stat(s, 8.3, 1.3, 4.5, String(cnt('higher')), 'really higher with ' + LBL, '2C5F2D'); stat(s, 8.3, 2.85, 4.5, String(cnt('lower')), 'really lower with ' + LBL, 'B71C1C'); stat(s, 8.3, 4.4, 4.5, String(cnt('no real difference')), 'no real difference (CI includes 0)', '555555');
  if (DATA.cmp_repeat) {
    s = slide('3. How much does the answer depend on the split?', 'Light pipeline (A SVM, B RF, C XGBoost) under LORO and 21 grouped ' + LBL + ' splits.');
    img(s, FG + 'f38_cmp_repeat.png', 0.5, 1.15, 12.3, 3.9);
    const rp = DATA.cmp_repeat.filter(r => r.metric === ({ A: 'macro_F1', B: 'macro_F1', C: 'R2' })[r.task]);
    tbl(s, [['Task', 'LORO', 'Main ' + LBL, '20 splits mean ± SD', 'Range', 'Above LORO'], ...rp.map(r => [r.task, f3(r.LORO_light), f3(r.main_light), f3(r.rep_mean) + ' ± ' + f3(r.rep_sd), f3(r.rep_min) + '–' + f3(r.rep_max), r.rep_above + ' / ' + r.rep_n])], 0.5, 5.2, 12.3, [1.0, 1.6, 1.8, 3.0, 2.8, 2.1], 13);
  }
  if (DATA.cmp_leak) {
    s = slide('4. Leakage check: splitting leaves instead of plots', 'Leaves of the same plot in training and test make the accuracy look better than it is.');
    img(s, FG + 'f39_cmp_leak.png', 0.5, 1.15, 7.0, 4.6);
    card(s, 7.8, 1.3, 5.0, 4.4, 'What it shows', DATA.cmp_summary ? DATA.cmp_summary.leak_sentence : '', 'B71C1C', 'FDECEA', 15);
  }
  s = slide('Answer: does ' + LBL + ' improve the accuracy?');
  card(s, 0.5, 1.3, 12.3, 3.6, 'Conclusion of the comparison', DATA.cmp_summary ? DATA.cmp_summary.verdict + ' ' + DATA.cmp_summary.summary_sentence.split('. ')[0] + '.' : '', '1565C0', 'E3F2FD', 18);
  bullets(s, ['Main accuracy estimate: LORO (every leaf tested once, follows the experimental design).', 'The ' + LBL + ' models are deployable models; read their single-split accuracy with the repeated-split range.', 'The decisive test is an independent season or site (2026-27, Bharatpur).'], 0.6, 5.1, 12.1, 1.8, 16);
}

// =============================== DISCUSSION
sec('Discussion', 'What the results mean');
s = slide('Physical basis of the white rust signal');
card(s, 0.5, 1.3, 3.95, 3.5, 'Pigments → red edge', 'Chlorophyll loss raises red reflectance, lowers the red-edge peak and shifts the red-edge position by ' + (DATA.rep[0] - DATA.rep[5]).toFixed(1) + ' nm towards shorter wavelengths (Filella and Peñuelas, 1994; Mahlein et al., 2013).', undefined, undefined, 18);
card(s, 4.68, 1.3, 3.95, 3.5, 'Structure → NIR', 'White pustules and collapsed mesophyll change internal scattering, lowering the near-infrared plateau (Mishra et al., 2009).', '1565C0', 'E3F2FD', 18);
card(s, 8.86, 1.3, 3.95, 3.5, 'Water → SWIR', 'Dehydrated tissue raises shortwave-infrared reflectance; derivatives at the water-band edges (FD1245, FD1805) entered the feature set – keeping water bands was useful (Peñuelas et al., 1997).', 'B71C1C', 'F9E0DE', 18);
stat(s, 0.5, 5.05, 3.95, DATA.rep[0].toFixed(1) + ' → ' + DATA.rep[5].toFixed(1) + ' nm', 'red-edge position, grade 0 → 9'); stat(s, 4.68, 5.05, 3.95, (100 * (pc(800, 9) - pc(800, 0)) / pc(800, 0)).toFixed(0) + '%', 'reflectance at 800 nm, grade 0 → 9', '1565C0'); stat(s, 8.86, 5.05, 3.95, '+' + (100 * (pc(1450, 9) - pc(1450, 0)) / pc(1450, 0)).toFixed(0) + '%', 'reflectance at 1450 nm, grade 0 → 9', 'B71C1C');
s = slide('Why detection works but six grades are hard');
stat(s, 0.5, 1.3, 3.0, f2(rA.macro_F1), 'detection macro-F1'); stat(s, 0.5, 2.85, 3.0, f2(rB.macro_F1), 'six-grade macro-F1', 'B71C1C'); stat(s, 0.5, 4.4, 3.0, f2(rB.QWK), 'quadratic weighted kappa', '7030A0');
bullets(s, ['Grades are ordinal steps of a continuous process; neighbouring grades differ only in pustule area.', 'Visual raters disagree most between intermediate grades (Bock et al., 2010).', 'Spectral distributions of neighbouring grades overlap (PCA, box plots).', 'Errors are small in grade terms: ' + Math.round(100 * rB.within1) + '% within one class.', 'Same pattern in wheat rust/FHB and rice blast studies (Huang et al., 2020; Lv et al., 2023; Mandal et al., 2023).', 'Remedy: report severity as a score or a few classes (methodology: 4 classes + regression).'], 3.9, 1.3, 8.9, 5.2, 16);
s = slide('Machine learning vs deep learning; role of covariates');
card(s, 0.5, 1.3, 6.0, 4.2, 'Models', (HASDL ? 'All models within about one plot-bootstrap SE: best network ' + BEST.B.DL + ' ' + f3(row('B', BEST.B.DL).macro_F1) + ' vs ' + BEST.B.ML + ' ' + f3(row('B', BEST.B.ML).macro_F1) + ' (six grades); DT-EDNet ' + f3(dte.B.macro_F1) + '. ' : '') + 'With 10–16 features the 4 × 4 pseudo-images carry little spatial pattern (Sharma et al., 2019). The DT-EDNet advantage reported for rice canopies (Ma et al., 2026) is expected on UAV hyperspectral images.', '7030A0', 'EDE2F6', 17);
card(s, 6.8, 1.3, 6.0, 4.2, 'Covariates and weather', '• Without spectra the covariates reached detection macro-F1 ' + f2(m0v('A', 'macro_F1')) + ' (AUC ' + f2(m0v('A', 'AUC')) + '): inside unsprayed plots healthy leaves occur mainly on the first date, so the calendar detects disease (spectra alone ΔS ' + cg('A', 'macro_F1', 'ΔS').delta.toFixed(3) + ').\n• For severity the spectra add what the calendar cannot: ΔS ' + (cg('B', 'macro_F1', 'ΔS').delta >= 0 ? '+' : '') + cg('B', 'macro_F1', 'ΔS').delta.toFixed(3) + ' macro-F1 (grades), ' + (cg('C', 'R2', 'ΔS').delta >= 0 ? '+' : '') + cg('C', 'R2', 'ΔS').delta.toFixed(3) + ' R² (score); with covariates ΔT +' + cg('B', 'macro_F1', 'ΔT').delta.toFixed(3) + ' and +' + cg('C', 'R2', 'ΔT').delta.toFixed(3) + ' R².\n• Weather soon left the favourable range (Chattopadhyay et al., 2011); four dates are too few to test it independently.', undefined, undefined, 15);
s = slide('Limitations and implications for the UAV phase');
card(s, 0.5, 1.3, 6.0, 3.9, 'Limitations', '• One season, one location (Bharatpur validation next).\n• Subjective leaf grades; grade 9 small (' + DATA.grade_n['9'] + ' leaves).\n• Stage and date confounded.\n• Networks on CPU with paper settings, no tuning.\n• No pre-symptomatic dates in 2025-26 → Objective 3 not addressed.', 'B71C1C', 'F9E0DE', 18);
card(s, 6.8, 1.3, 6.0, 3.9, 'Implications', '• Key regions: red edge 690–760 nm, NIR shoulder 780–870 nm, SWIR water-band edges.\n• Keep hyperspectral derivatives in the UAV features.\n• Detection is realistic at canopy level; report severity as a score or few classes.\n• Final leaf models can check UAV predictions on the sampled leaves.', undefined, undefined, 18);

// =============================== CONCLUSIONS
sec('Conclusions', 'Summary, cross-check and outputs');
s = slide('Conclusions');
bullets(s, ['White rust lowers NIR, raises red and SWIR reflectance and shifts the red edge by ~' + Math.round(DATA.rep[0] - DATA.rep[5]) + ' nm (grade 0 → 9).',
  'First derivatives carry the strongest signal: SHAP-CARS selected ' + O1.OW.length + ' derivative bands; the disease-specific set has ' + O1.DSF.length + ' features.',
  'Detection is reliable (macro-F1 ' + f2(rA.macro_F1) + ', AUC ' + f2(rA.AUC) + '); six grades are limited by class overlap (QWK ' + f2(rB.QWK) + '); score R² ' + f2(rC.R2) + ', RMSE ' + f2(rC.RMSE) + '.',
  'Without sensor data the calendar detected disease inside unsprayed plots as well as the spectra; spectra added +' + cg('B', 'macro_F1', 'ΔS').delta.toFixed(3) + ' macro-F1 (grades) and +' + cg('C', 'R2', 'ΔS').delta.toFixed(3) + ' R² (score) beyond it; spectra + covariates gave real gains for grades and score; models transfer across varieties and timings.',
  'The tested models themselves (trained on the ' + SP.n_train_leaves + ' training leaves) are saved for the UAV phase and the Bharatpur validation.'], 0.6, 1.3, 12.1, 5.2, 18);
s = slide('Cross-check with the methodology', 'All steps that apply to non-imaging leaf spectra were performed.');
tbl(s, [['Done', 'Adapted', 'Not applicable to leaf spectra'], ['Design A1, A4–A6; B3, D3, D4; E3, E4; F1–F3', 'Effective ranges: top 5% (no pair R² ≥ 0.5)', 'B1, B2, B4, B5 (image processing); C1–C8 (crop mask)'],
  ['1.1–1.4, 1.6.2; 2.1.1, 2.1.2, 2.1.4, 2.1.5', 'DL: paper settings on CPU, ≤ 100 epochs, no extra tuning', 'D5–D7, 1.5 (texture, TTFI, thermal); 1.3.3 (multispectral)'],
  ['2.2.1–2.2.6; 2.3.1, 2.3.3–2.3.8; 2.4', 'Covariate baseline (B1, RF, best ML; bootstrap, DeLong) on unsprayed plots only', '2.1.3, 2.3.2 (fusion of 15 sensor sets, DNN-F2)'],
  ['2.5.3–2.5.5; 2.6.1–2.6.2; 2.7.1', 'Crop age (DAS) as time variable (natural infection)', '2.6.3 maps; 2.7.2–2.7.4 Bharatpur; 1.7; Objective 3 (no pre-symptomatic dates)']], 0.5, 1.3, 12.3, [4.1, 4.1, 4.1], 15);
s = slide('Outputs delivered', 'Everything is editable and reproducible.');
card(s, 0.5, 1.3, 3.95, 3.6, 'Excel workbook', '33 numbered sheets (29–33: split and comparison with LORO): data, live formulas (counts, mean spectra, correlation, WRI with editable wavelengths, indices, confusion and regression metrics), native charts, the covariate baseline with formula gains and all result tables.', undefined, undefined, 17);
card(s, 4.68, 1.3, 3.95, 3.6, 'Word report + PDF', 'Thesis-seminar style: introduction, methods (step cards), results with ' + require('fs').readdirSync(FG).filter(f => f.endsWith('.png')).length + ' figures and editable tables, discussion, conclusions, cross-check, questions and references.', '1565C0', 'E3F2FD', 18);
card(s, 8.86, 1.3, 3.95, 3.6, 'Model files', (DATA.ml_files ? DATA.ml_files.length : 15) + ' machine-learning models (joblib) and ' + (DATA.dl_files ? DATA.dl_files.length : 15) + ' networks (PyTorch) trained on all leaves, plus 11 covariate-baseline models, with feature definitions and prediction scripts.', '7030A0', 'EDE2F6', 18);
s.addText('Files: ASD_2025-26_80-20_leaf_analysis_white_rust.xlsx | ASD_2025-26_80-20_leaf_analysis_white_rust_report.docx / .pdf | ASD_2025-26_80-20_leaf_analysis_seminar.pptx | ASD_2025-26_80-20_models.zip', { x: 0.5, y: 5.2, w: 12.3, h: 0.8, fontSize: 14, italic: true, color: '2C5F2D', isTextBox: true });

// references (key works cited on the slides)
const keys = [['Bock', '2010'], ['Chattopadhyay', '2011'], ['Cohen', '1960'], ['Cohen', '1968'], ['Dormann', '2013'], ['Fawcett', '2006'], ['Filella', '1994'], ['He', '2016'], ['Hu', '2018'], ['Huang', '2020'], ['Li', '2009'], ['Lundberg', '2017'], ['Lv', '2023'], ['Ma', '2026'], ['Mahlein', '2013'], ['Mahlein', '2016'],
  ['Mandal', '2023'], ['Meng', '2020'], ['Milton', '2009'], ['Bijlwan', '2025'], ['Breiman', '2001'], ['De Wolf', '2007'], ['DeLong', '1988'], ['Efron', '1993'], ['Kuhn', '2013'], ['Lancashire', '1991'], ['Madden', '2007'], ['McCullagh', '1980'], ['Ruan', '2022'], ['Zhang', '2014'], ['Mishra', '2009'], ['Peñuelas', '1997'], ['Pudil', '1994'], ['Roberts', '2017'], ['Robnik-Šikonja', '2003'], ['Saharan', '2014'], ['Savitzky', '1964'], ['Sharma', '2019'], ['Tan', '2019'], ['Tsai', '1998'], ['Varma', '2006'], ['Vaswani', '2017'], ['Williams', '2001'], ['Woo', '2018'], ['Woo', '2023']];
const refs = keys.map(([a, y]) => DATA.refs.find(r => r.startsWith(a) && r.includes('(' + y))).filter(Boolean);
refs.sort((a, b) => a.localeCompare(b)); const third = Math.ceil(refs.length / 3);
[refs.slice(0, third), refs.slice(third, 2 * third), refs.slice(2 * third)].forEach((part, i) => {
  s = slide('References (' + (i + 1) + '/3)', 'Key references cited on the slides; the full list is in the Word report.');
  s.addText(part.map((r, j) => ({ text: r, options: { breakLine: j < part.length - 1 } })), { x: 0.5, y: 1.2, w: 12.3, h: 5.6, fontSize: 11, color: '1B2A1E', valign: 'top', paraSpaceAfter: 4, isTextBox: true, fit: 'shrink' });
});
// ---------------- appendix: every table and figure of the Word report (same numbering)
{
  const fs_ = require('fs'); const RT = JSON.parse(fs_.readFileSync(__dirname + '/data/report_tables.json', 'utf8')); const RF = JSON.parse(fs_.readFileSync(__dirname + '/data/report_figures.json', 'utf8'));
  const TN = {}, FN = {}; RT.forEach(t => TN[t.key] = t.number); RF.forEach(f => FN[f.key] = f.number);
  const cl = t => String(t).replace(/\[\[(T|F):(\w+)\]\]/g, (m, a, k) => (a === 'T' ? 'Table ' + (TN[k] || k) : 'Figure ' + (FN[k] || k))).replace(/\*\*/g, '').replace(/_\{([^}]*)\}/g, '$1').replace(/\^\{([^}]*)\}/g, '^$1');
  const SRC = fs_.readFileSync(__filename, 'utf8').split('// ---------------- appendix')[0];
  sec('Appendix: all report tables and figures', 'Every table and figure of the Word report with the same number; figures already shown as images earlier are not repeated');
  RT.forEach(t => {
    const rows = t.rows.map(r => r.map(cl)); const hdr = rows[0], body = rows.slice(1); const nc = hdr.length;
    const len = j => Math.min(50, Math.max(4, ...rows.map(r => String(r[j]).length))); const tot = hdr.reduce((a, _, j) => a + len(j), 0); const colW = hdr.map((_, j) => 12.3 * len(j) / tot);
    const longest = Math.max(...rows.map(r => r.reduce((a, c) => a + String(c).length, 0)));
    const per = longest > 400 ? 4 : longest > 250 ? 7 : body.length > 16 ? 14 : body.length; const fsz = nc > 10 || longest > 300 ? 8.5 : nc > 7 || longest > 160 ? 10 : 12;
    const parts = Math.max(1, Math.ceil(body.length / per));
    for (let p = 0; p < parts; p++) {
      const s_ = slide('Table ' + t.number + (parts > 1 ? ' (' + (p + 1) + '/' + parts + ')' : ''), cl(t.caption));
      const hc = hdr.map(c => ({ text: String(c), options: { bold: true, color: 'FFFFFF', fill: { color: '2C5F2D' }, align: 'center', valign: 'middle' } }));
      const bc = body.slice(p * per, (p + 1) * per).map((r, i) => r.map(c => ({ text: String(c), options: { fill: { color: i % 2 ? 'FFFFFF' : 'F4F7F1' }, valign: 'middle' } })));
      s_.addTable([hc, ...bc], { x: 0.5, y: 1.15, w: 12.3, colW, fontSize: fsz, fontFace: 'Calibri', color: '1B2A1E', border: { type: 'solid', pt: 0.5, color: 'C9D3C4' }, margin: 0.04, autoPage: false });
      s_.addText('Table ' + t.number + '. ' + cl(t.caption), { x: 0.5, y: 6.45, w: 12.3, h: 0.55, fontSize: 10, italic: true, color: '6B7B6E', isTextBox: true, fit: 'shrink' });
    }
  });
  RF.forEach(f => {
    if (SRC.includes(f.file)) return;
    const s_ = slide('Figure ' + f.number, cl(f.caption));
    s_.addImage({ path: FG + f.file, x: 0.5, y: 1.15, w: 12.3, h: 5.25, sizing: { type: 'contain', w: 12.3, h: 5.25 } });
    s_.addText('Figure ' + f.number + '. ' + cl(f.caption), { x: 0.5, y: 6.45, w: 12.3, h: 0.55, fontSize: 10.5, italic: true, color: '6B7B6E', isTextBox: true, fit: 'shrink' });
  });
}
s = pres.addSlide({ masterName: 'TITLE' });
s.addText('Thank you', { placeholder: 'title' });
s.addText('Questions and discussion', { placeholder: 'body' });

pres.writeFile({ fileName: OUT }).then(async f => { await applyTheme(OUT, THEME); console.log('saved', f); });
