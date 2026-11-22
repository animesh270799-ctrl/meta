// Seminar slides: methodology -> results (Objectives 1, 2, exploratory 3) -> discussion -> conclusions. Native charts where PowerPoint can draw them.
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
const N = DATA.n;
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
s.addText([{ text: 'ASD contact-probe spectra, 2025-26 season: four dates pooled, 2339 leaves', options: { breakLine: true } }, { text: 'Animesh Panda | Ph.D. Agricultural Physics | ICAR-IARI, New Delhi', options: { breakLine: true } }, { text: 'Objective 1: spectral response and features | Objective 2: machine and deep learning | exploratory Objective 3' }], { placeholder: 'body' });
s.addNotes('Title. This talk presents the complete analysis of the 2025-26 leaf spectra, from methodology to discussion.');

s = slide('Outline', 'Order of the talk.');
[['1', 'Introduction and objectives'], ['2', 'Materials and methods'], ['3', 'Results: spectral response and features (Objective 1)'], ['4', 'Results: models (Objective 2) and robustness'], ['5', 'Discussion, conclusions and next steps']].forEach((t, i) => {
  const y = 1.35 + i * 1.08; s.addShape(pres.shapes.OVAL, { x: 0.9, y, w: 0.75, h: 0.75, fill: { color: '2C5F2D' }, line: { color: '2C5F2D' } });
  s.addText(t[0], { x: 0.9, y, w: 0.75, h: 0.75, fontSize: 22, bold: true, color: 'FFFFFF', align: 'center', valign: 'middle', isTextBox: true, margin: 0 });
  s.addText(t[1], { x: 1.9, y, w: 6.5, h: 0.75, fontSize: 20, color: '1B2A1E', valign: 'middle', isTextBox: true, margin: 0 });
});
stat(s, 9.2, 1.35, 3.4, String(N), 'leaf spectra (350–2500 nm)'); stat(s, 9.2, 2.9, 3.4, '4 dates', '6, 19, 26, 36 days after inoculation'); stat(s, 9.2, 4.45, 3.4, '11 models', '5 machine learning + 6 deep learning');

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
card(s, 8.86, 1.3, 3.95, 3.3, 'Objective 3 (exploratory)', 'Do symptomless leaves of inoculated plots differ from healthy-plot leaves? The full pre-symptomatic objective needs the 2026-27 flights.', 'B71C1C', 'F9E0DE', 18);
stat(s, 0.5, 4.95, 3.95, 'Task A', 'detection: healthy vs diseased leaf'); stat(s, 4.68, 4.95, 3.95, 'Task B', 'six grades 0, 1, 3, 5, 7, 9', '7030A0'); stat(s, 8.86, 4.95, 3.95, 'Task C', 'severity score 0–9 (regression)', 'B71C1C');

// =============================== METHODS
sec('Materials and methods', 'Experiment, data, validation, pre-processing and the analysis steps');
s = slide('Workflow of the analysis', 'Twelve steps from data to interpretation; colours = phases.');
img(s, FG + 'f00_workflow.png', 1.3, 1.15, 10.7, 5.75);
s = slide('Experiment and field layout', 'Design of the 2025-26 experiment.');
tbl(s, [['Item', 'Detail'], ['Plots', '48 plots, 5 m × 3.5 m; 0.5-m bunds, 2-m channels; field 48 m × 24 m'], ['Blocks', 'healthy block 1–12 (fungicide-sprayed); R3 13–24, R2 25–36, R1 37–48 (inoculated)'],
  ['Treatments', '3 varieties (V1, V2, V3) × 4 sowing dates (D1–D4) in every block'], ['Inoculation', '5 February 2026, all inoculated plots'], ['Leaves', 'L3, L5 (3rd, 5th fully expanded from top) and LL (lowest green leaf)'], ['Instrument', 'ASD contact probe, 350–2500 nm, splice-corrected']], 0.5, 1.3, 7.3, [1.6, 5.7], 13);
tbl(s, [['Timing', 'Sowing', 'Planned DAS', 'From dates'], ['D1', '9 Dec 2025', '50', String(DATA.das0.D1)], ['D2', '18 Dec 2025', '40', String(DATA.das0.D2)], ['D3', '27 Dec 2025', '30', String(DATA.das0.D3)], ['D4', '9 Jan 2026', '20', String(DATA.das0.D4)]], 8.2, 1.3, 4.6, [0.9, 1.4, 1.1, 1.2], 13);
s.addText('Note: with inoculation on 5 Feb 2026 the sowing dates give a crop age of 58, 49, 40 and 27 days, not the planned 50, 40, 30, 20 DAS. The analysis uses the actual dates.', { x: 8.2, y: 4.0, w: 4.6, h: 1.4, fontSize: 12, color: 'B71C1C', isTextBox: true, fit: 'shrink' });
s = slide('Data: leaves by date and grade', 'Native chart: edit the data in PowerPoint or in the Excel sheet 2_Counts.');
const cd = DATA.counts.date;
chart(s, pres.charts.BAR, cd.series.map(x => ({ name: x.name, labels: DATA.dates.map(d => d.date.slice(5) + ' (' + d.DAI + ' DAI)'), values: x.values })), { x: 0.5, y: 1.2, w: 7.4, h: 5.4, barDir: 'col', barGrouping: 'stacked', chartColors: GRADE_COLS, showLegend: true, legendPos: 'b', showTitle: true, title: 'Leaves per sampling date, by grade', valAxisTitle: 'Leaves', showValAxisTitle: true });
tbl(s, [['Date', 'DAI', 'Leaves', 'Mean grade', 'Diseased %'], ...DATA.dates.map(d => [d.date, d.DAI, d.n, f2(d.mean_grade), Number(d.pct).toFixed(0)])], 8.2, 1.3, 4.6, [1.3, 0.6, 0.8, 1.0, 0.9], 12);
s.addText('Grades 0/1/3/5/7/9: ' + GR.map(g => DATA.grade_n[g]).join(' / ') + ' leaves. Grade 9 is the smallest class.', { x: 8.2, y: 4.2, w: 4.6, h: 1.0, fontSize: 13, color: '1B2A1E', isTextBox: true });
s = slide('Tasks and validation design', 'Leave-one-replication-out keeps whole plots out of training.');
tbl(s, [['Task', 'Target', 'Main metric'], ['A detection', 'grade 0 vs > 0', 'macro-F1, AUC'], ['B six grades', '0, 1, 3, 5, 7, 9', 'macro-F1, QWK'], ['C severity score', '0–9 (regression)', 'R², RMSE, RPD']], 0.5, 1.3, 6.0, [1.8, 2.2, 2.0], 14);
tbl(s, [['Fold', 'Test replication', 'Healthy plots in test', 'Test / train leaves'], ...DATA.fold_sizes.map((f, i) => [f.fold, ['R1 (37–48)', 'R2 (25–36)', 'R3 (13–24)'][i], ['7, 2, 10, 12', '5, 8, 4, 1', '3, 9, 11, 6'][i], f.test + ' / ' + f.train])], 6.8, 1.3, 6.0, [0.7, 1.6, 1.9, 1.8], 13);
bullets(s, ['Leaves of one plot share soil, microclimate and inoculum → random splits inflate accuracy (Roberts et al., 2017).', 'All feature selection, SFFS and tuning repeated inside each training part; inner GroupKFold(3) by plot (Varma and Simon, 2006).', 'Every leaf is tested exactly once → pooled test predictions for all models.'], 0.5, 3.9, 12.3, 2.6, 15);
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
bullets(s, ['SHAP of XGBoost on the disease-specific set', 'Strata: stage, variety, leaf position, date', 'Leave-one-variety-out and leave-one-timing-out', 'Selection stability across folds', 'Covariate baseline: variety, timing, DAI, stage, 7-day weather (inoculated plots only)', 'Exploratory: symptomless inoculated vs healthy-plot leaves', 'Final models refitted on all leaves and saved'], 7.0, 1.3, 5.8, 5.2, 17);

// =============================== RESULTS OBJECTIVE 1
sec('Results – Objective 1', 'Spectral response and disease-specific features');
s = slide('Dataset composition', 'Leaves by date, growth stage, variety and leaf position.');
img(s, FG + 'f01_dataset.png', 1.9, 1.15, 9.5, 5.6);
s = slide('Disease progress and weather', 'Warm, dry weather after inoculation; disease rose mainly in the first three weeks.');
img(s, FG + 'f15_weather_progress.png', 0.5, 1.15, 9.0, 5.3);
const pr = DATA.prog;
tbl(s, [['DAI', 'Grade', 'Dis. %', 'Tmax 7 d'], ...pr.map((r, i) => [DATA.dates[i].DAI, f2(r.mean_grade), Number(r.pct_diseased).toFixed(0), Number(r.Tmax7).toFixed(1)])], 9.8, 1.4, 3.0, [0.6, 0.75, 0.75, 0.9], 12);
s.addText('Favourable days (16–24 °C, RH II > 40%) occurred mainly in the first week after inoculation (Chattopadhyay et al., 2011).', { x: 9.8, y: 3.8, w: 3.0, h: 1.8, fontSize: 12, color: '1B2A1E', isTextBox: true, fit: 'shrink' });
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
s = slide('PCA and fold-wise selection', 'Grades form overlapping, ordered clouds; selection was repeated in every fold.');
img(s, FG + 'f12_pca.png', 0.5, 1.2, 4.7, 5.2);
tbl(s, [['Fold', 'OW', 'Best NDSI', 'DSF six grades'], ...['0', '1', '2'].map(f => [+f + 1, DATA.folds[f].OW.length, '(' + DATA.folds[f].ndsi.join(', ') + ')', DATA.folds[f].DSF.B.join(', ')])], 5.4, 1.3, 7.4, [0.6, 0.6, 1.3, 4.9], 11);
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
s = slide('All models, all metrics', 'Heat-map of the pooled test metrics (darker = better within a column).');
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
s = slide('Covariates and weather vs leaf spectra', 'Inoculated, unsprayed plots only; random forest.');
const cv = DATA.covariates, vv = ['covariates only', 'leaf spectra (DSF)', 'leaf spectra + covariates'];
const g = (t, v, k) => (cv.find(r => r.task === t && r.variant === v) || {})[k];
chart(s, pres.charts.BAR, vv.map(v => ({ name: v, labels: ['Detection macro-F1', 'Six grades macro-F1', 'Score R²'], values: [g('A', v, 'macro_F1'), g('B', v, 'macro_F1'), g('C', v, 'R2')] })), { x: 0.5, y: 1.2, w: 8.4, h: 5.4, barDir: 'col', barGrouping: 'clustered', chartColors: ['9E9E9E', '2E75B6', '7030A0'], showValue: true, dataLabelFormatCode: '0.00', dataLabelPosition: 'outEnd', showLegend: true, legendPos: 'b', valAxisMinVal: 0, valAxisMaxVal: 1, showTitle: true, title: 'Covariate baseline' });
bullets(s, ['Covariates: variety, timing, days after inoculation, growth stage, 7-day Tmax, Tmin, RH I, RH II, rain, wind, sunshine, evaporation.', 'Healthy plots excluded (fungicide-sprayed).', 'Spectra add leaf-to-leaf information within a stage; the combination is best.'], 9.1, 1.4, 3.7, 5.0, 13);
if (DATA.exploratory) {
  s = slide('Exploratory: symptomless leaves (Objective 3 proxy)', 'Grade-0 leaves of inoculated plots vs healthy-plot leaves.');
  img(s, FG + 'f28_asymptomatic.png', 0.5, 1.3, 8.0, 4.0);
  const eb = DATA.exploratory.reduce((a, b) => (b.balanced_acc > a.balanced_acc ? b : a));
  stat(s, 8.9, 1.4, 3.9, f2(eb.balanced_acc), 'best balanced accuracy (' + eb.model + ')', 'B71C1C');
  bullets(s, ['Groups also differ in fungicide treatment → only a hint of a pre-visual signal.', 'Proper test: the three pre-symptomatic flights of 2026-27.'], 8.9, 3.0, 3.9, 3.2, 14);
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
card(s, 0.5, 1.3, 6.0, 4.2, 'Models', (HASDL ? 'All models within about one fold SD: best network ' + BEST.B.DL + ' ' + f3(row('B', BEST.B.DL).macro_F1) + ' vs ' + BEST.B.ML + ' ' + f3(row('B', BEST.B.ML).macro_F1) + ' (six grades); DT-EDNet ' + f3(dte.B.macro_F1) + '. ' : '') + 'With 10–16 features the 4 × 4 pseudo-images carry little spatial pattern (Sharma et al., 2019). The DT-EDNet advantage reported for rice canopies (Ma et al., 2026) is expected on UAV hyperspectral images.', '7030A0', 'EDE2F6', 17);
card(s, 6.8, 1.3, 6.0, 4.2, 'Covariates and weather', 'Stage, timing and days after inoculation follow the epidemic, so covariates alone detect disease well; spectra improve grades and score, and the combination is best. Weather left the favourable range soon after inoculation; four dates are too few to test weather as an independent predictor – 13 flights in 2026-27 will be.', undefined, undefined, 18);
s = slide('Limitations and implications for the UAV phase');
card(s, 0.5, 1.3, 6.0, 3.9, 'Limitations', '• One season, one location (Bharatpur validation next).\n• Subjective leaf grades; grade 9 small (' + DATA.grade_n['9'] + ' leaves).\n• Stage and date confounded.\n• Networks on CPU with paper settings, no tuning.\n• No pre-symptomatic dates in 2025-26.', 'B71C1C', 'F9E0DE', 18);
card(s, 6.8, 1.3, 6.0, 3.9, 'Implications', '• Key regions: red edge 690–760 nm, NIR shoulder 780–870 nm, SWIR water-band edges.\n• Keep hyperspectral derivatives in the UAV features.\n• Detection is realistic at canopy level; report severity as a score or few classes.\n• Final leaf models can check UAV predictions on the sampled leaves.', undefined, undefined, 18);

// =============================== CONCLUSIONS
sec('Conclusions', 'Summary, cross-check and outputs');
s = slide('Conclusions');
bullets(s, ['White rust lowers NIR, raises red and SWIR reflectance and shifts the red edge by ~' + Math.round(DATA.rep[0] - DATA.rep[5]) + ' nm (grade 0 → 9).',
  'First derivatives carry the strongest signal: SHAP-CARS selected ' + O1.OW.length + ' derivative bands; the disease-specific set has ' + O1.DSF.length + ' features.',
  'Detection is reliable (macro-F1 ' + f2(rA.macro_F1) + ', AUC ' + f2(rA.AUC) + '); six grades are limited by class overlap (QWK ' + f2(rB.QWK) + '); score R² ' + f2(rC.R2) + ', RMSE ' + f2(rC.RMSE) + '.',
  'Spectra add information beyond stage, timing and weather; models transfer across varieties and timings.',
  'Final models trained on all ' + N + ' leaves are saved for the UAV phase and the Bharatpur validation.'], 0.6, 1.3, 12.1, 5.2, 18);
s = slide('Cross-check with the methodology', 'All steps that apply to non-imaging leaf spectra were performed.');
tbl(s, [['Done', 'Adapted', 'Not applicable to leaf spectra'], ['Design A1, A4–A6; B3, D3, D4; E3, E4; F1–F3', 'Effective ranges: top 5% (no pair R² ≥ 0.5)', 'B1, B2, B4, B5 (image processing); C1–C8 (crop mask)'],
  ['1.1–1.4, 1.6.2; 2.1.1, 2.1.2, 2.1.4, 2.1.5', 'DL: paper settings on CPU, ≤ 100 epochs, no extra tuning', 'D5–D7, 1.5 (texture, TTFI, thermal); 1.3.3 (multispectral)'],
  ['2.2.1–2.2.6; 2.3.1, 2.3.3–2.3.8; 2.4', 'Covariates on inoculated plots only', '2.1.3, 2.3.2 (fusion of 15 sensor sets, DNN-F2)'],
  ['2.5.3–2.5.5; 2.6.1–2.6.2; 2.7.1', 'Objective 3 only as exploratory proxy', '2.6.3 maps; 2.7.2–2.7.4 Bharatpur (next season); 1.7 not measured']], 0.5, 1.3, 12.3, [4.1, 4.1, 4.1], 15);
s = slide('Outputs delivered', 'Everything is editable and reproducible.');
card(s, 0.5, 1.3, 3.95, 3.6, 'Excel workbook', '26 sheets: data, live formulas (counts, mean spectra, correlation, WRI with editable wavelengths, indices, confusion and regression metrics), native charts and all result tables.', undefined, undefined, 18);
card(s, 4.68, 1.3, 3.95, 3.6, 'Word report + PDF', 'Thesis-seminar style: introduction, methods (step cards), results with ' + require('fs').readdirSync(FG).filter(f => f.endsWith('.png')).length + ' figures and editable tables, discussion, conclusions, cross-check, questions and references.', '1565C0', 'E3F2FD', 18);
card(s, 8.86, 1.3, 3.95, 3.6, 'Model files', (DATA.ml_files ? DATA.ml_files.length : 15) + ' machine-learning models (joblib) and ' + (DATA.dl_files ? DATA.dl_files.length : 15) + ' networks (PyTorch), trained on all leaves, with feature definitions and a prediction script for new ASD spectra.', '7030A0', 'EDE2F6', 18);
s.addText('Files: ASD_2025-26_leaf_analysis_white_rust.xlsx | ASD_2025-26_leaf_analysis_white_rust_report.docx / .pdf | ASD_2025-26_leaf_analysis_seminar.pptx | ASD_2025-26_models.zip', { x: 0.5, y: 5.2, w: 12.3, h: 0.8, fontSize: 14, italic: true, color: '2C5F2D', isTextBox: true });

// references (key works cited on the slides)
const keys = [['Bock', '2010'], ['Chattopadhyay', '2011'], ['Cohen', '1960'], ['Cohen', '1968'], ['Dormann', '2013'], ['Fawcett', '2006'], ['Filella', '1994'], ['He', '2016'], ['Hu', '2018'], ['Huang', '2020'], ['Li', '2009'], ['Lundberg', '2017'], ['Lv', '2023'], ['Ma', '2026'], ['Mahlein', '2013'], ['Mahlein', '2016'],
  ['Mandal', '2023'], ['Meng', '2020'], ['Mishra', '2009'], ['Peñuelas', '1997'], ['Pudil', '1994'], ['Roberts', '2017'], ['Robnik-Šikonja', '2003'], ['Saharan', '2014'], ['Savitzky', '1964'], ['Sharma', '2019'], ['Tan', '2019'], ['Tsai', '1998'], ['Varma', '2006'], ['Vaswani', '2017'], ['Williams', '2001'], ['Woo', '2018'], ['Woo', '2023']];
const refs = keys.map(([a, y]) => DATA.refs.find(r => r.startsWith(a) && r.includes('(' + y))).filter(Boolean);
const half = Math.ceil(refs.length / 2);
[refs.slice(0, half), refs.slice(half)].forEach((part, i) => {
  s = slide('References (' + (i + 1) + '/2)', 'Key references cited on the slides; the full list is in the Word report.');
  s.addText(part.map((r, j) => ({ text: r, options: { breakLine: j < part.length - 1 } })), { x: 0.5, y: 1.2, w: 12.3, h: 5.6, fontSize: 11, color: '1B2A1E', valign: 'top', paraSpaceAfter: 4, isTextBox: true, fit: 'shrink' });
});
s = pres.addSlide({ masterName: 'TITLE' });
s.addText('Thank you', { placeholder: 'title' });
s.addText('Questions and discussion', { placeholder: 'body' });

pres.writeFile({ fileName: OUT }).then(async f => { await applyTheme(OUT, THEME); console.log('saved', f); });
