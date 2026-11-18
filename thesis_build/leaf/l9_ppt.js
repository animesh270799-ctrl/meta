// Full methodology + results deck for the leaf-level ASD analysis.
const pptxgen = require('pptxgenjs');
const path = require('path');
const { applyTheme } = require('/root/.claude/skills/synced/9bf50f97-a337-4b6b-8c8b-ebd229b7e0d3_d565bc3b-4006-4195-b033-a8c25dfdc114/pptx/scripts/apply_theme.js');
const D = require('./data/deck.json'); const k = D.k;
const FIG = path.join(__dirname, 'fig');
const OUT = path.join(__dirname, '../outputs/Leaf_ASD_analysis_presentation_full.pptx');
const THEME = { name: 'White rust leaf', headFontFace: 'Cambria', bodyFontFace: 'Calibri',
  colors: { dk1: '1F2A2A', lt1: 'FFFFFF', dk2: '00463F', lt2: 'EEF4F2', accent1: '00695C', accent2: 'C98A00', accent3: 'AD1457', accent4: '2E7D32', accent5: '7B1FA2', accent6: 'E53935', hlink: '00695C', folHlink: '4A148C' } };
const X = { teal: '00695C', dark: '00463F', mustard: 'C98A00', berry: 'AD1457', green: '2E7D32', grey: '6B7B78', light: 'EEF4F2', text: '1F2A2A', out: 'FFF3D6' };
const GC = ['2E7D32', '9CCC65', 'FDD835', 'FB8C00', 'E53935', '7B1FA2'];
const pres = new pptxgen(); pres.layout = 'LAYOUT_WIDE'; pres.theme = { headFontFace: 'Cambria', bodyFontFace: 'Calibri' };
pres.title = 'Leaf-level hyperspectral analysis of white rust in mustard: methodology and results';
const C = pres.SchemeColor;
pres.defineSlideMaster({ title: 'TITLE', background: { color: X.dark }, objects: [
  { placeholder: { options: { name: 'title', type: 'title', x: 0.8, y: 2.0, w: 11.7, h: 1.8, fontSize: 40, bold: true, color: C.background1, fontFace: 'Cambria', valign: 'bottom' }, text: '' } },
  { placeholder: { options: { name: 'body', type: 'body', x: 0.8, y: 4.0, w: 11.7, h: 1.6, fontSize: 18, color: 'CADFDB', valign: 'top' }, text: '' } }] });
pres.defineSlideMaster({ title: 'SECTION', background: { color: X.teal }, objects: [
  { placeholder: { options: { name: 'title', type: 'title', x: 0.8, y: 2.6, w: 11.7, h: 1.2, fontSize: 40, bold: true, color: C.background1, fontFace: 'Cambria' }, text: '' } },
  { placeholder: { options: { name: 'body', type: 'body', x: 0.8, y: 3.9, w: 11.7, h: 1.4, fontSize: 18, color: 'E0F2F1' }, text: '' } }] });
pres.defineSlideMaster({ title: 'CONTENT', background: { color: 'FFFFFF' }, margin: [0.5, 0.5, 0.6, 0.5],
  slideNumber: { x: 12.4, y: 7.05, w: 0.6, h: 0.3, fontSize: 10, color: X.grey },
  objects: [{ placeholder: { options: { name: 'title', type: 'title', x: 0.5, y: 0.3, w: 12.3, h: 0.8, fontSize: 30, bold: true, color: C.text2, fontFace: 'Cambria', valign: 'middle' }, text: '' } },
            { text: { text: 'Leaf-level ASD analysis  |  White rust of mustard', options: { x: 0.5, y: 7.05, w: 8, h: 0.3, fontSize: 10, color: X.grey } } }] });
let sec = '';
const slide = (t) => { const s = pres.addSlide({ masterName: 'CONTENT', sectionTitle: sec }); s.addText(t, { placeholder: 'title' }); return s; };
const section = (t, sub) => { sec = t; pres.addSection({ title: t }); const s = pres.addSlide({ masterName: 'SECTION', sectionTitle: t }); s.addText(t, { placeholder: 'title' }); if (sub) s.addText(sub, { placeholder: 'body' }); return s; };
const bul = (s, items, o) => s.addText(items.map((t, i) => ({ text: t, options: { bullet: true, breakLine: i < items.length - 1 } })), Object.assign({ isTextBox: true, fontSize: 14, color: X.text, paraSpaceAfter: 5, valign: 'top' }, o));
const refs = (s, t, o) => s.addText('References: ' + t, Object.assign({ isTextBox: true, x: 0.5, y: 5.55, w: 5.1, h: 0.65, fontSize: 11, italic: true, color: X.grey, valign: 'top', margin: 2 }, o));
const output = (s, t) => {
  s.addShape(pres.shapes.ROUNDED_RECTANGLE, { x: 0.5, y: 6.3, w: 12.3, h: 0.62, fill: { color: X.out }, line: { color: X.mustard, width: 1 }, rectRadius: 0.08, objectName: 'output box' });
  s.addText([{ text: 'Output: ', options: { bold: true, color: X.mustard } }, { text: t, options: { color: X.text } }], { isTextBox: true, x: 0.65, y: 6.3, w: 12.0, h: 0.62, fontSize: 13, valign: 'middle', margin: 2, objectName: 'output text' });
};
const img = (s, key, x, y, w, hmax, cap) => {
  const r = D.img[key]; let ww = w, hh = w * r; if (hh > hmax) { hh = hmax; ww = hh / r; }
  s.addImage({ path: path.join(FIG, key + '.png'), x: x + (w - ww) / 2, y, w: ww, h: hh, altText: cap || key, objectName: key });
  if (cap) s.addText(cap, { isTextBox: true, x, y: y + hh + 0.03, w, h: 0.3, fontSize: 10, italic: true, color: X.grey, align: 'center', margin: 0, objectName: key + ' caption' });
};
const H = (t) => ({ text: t, options: { bold: true, color: 'FFFFFF', fill: { color: X.teal } } });
const table = (s, rows, x, y, w, colW, fs, rowH) => s.addTable([rows[0].map(H)].concat(rows.slice(1)), { x, y, w, colW, fontSize: fs || 11, fontFace: 'Calibri', color: X.text, border: { type: 'solid', pt: 0.5, color: 'D5DEDC' }, rowH: rowH || 0.26, valign: 'middle', autoPage: false });
const card = (s, x, y, w, h, big, small, col, name, bs) => {
  s.addShape(pres.shapes.ROUNDED_RECTANGLE, { x, y, w, h, fill: { color: X.light }, line: { color: X.light }, rectRadius: 0.1, objectName: name + ' card' });
  s.addText(big, { isTextBox: true, x: x + 0.12, y: y + 0.08, w: w - 0.24, h: h * 0.5, fontSize: bs || 28, bold: true, color: col, fontFace: 'Cambria', valign: 'bottom', margin: 0, objectName: name + ' value' });
  s.addText(small, { isTextBox: true, x: x + 0.12, y: y + h * 0.58, w: w - 0.24, h: h * 0.4, fontSize: 12, color: X.text, valign: 'top', margin: 0, objectName: name + ' label' });
};
const AX = { catAxisLabelColor: X.grey, valAxisLabelColor: X.grey, catAxisLabelFontFace: '+mn-lt', valAxisLabelFontFace: '+mn-lt', catAxisLabelFontSize: 10, valAxisLabelFontSize: 10, valGridLine: { color: 'E3E8E7', size: 0.5 }, catGridLine: { style: 'none' }, titleFontFace: '+mn-lt', titleFontSize: 12, titleColor: X.text, legendFontFace: '+mn-lt', legendFontSize: 10, dataLabelFontFace: '+mn-lt', dataLabelFontSize: 9 };
const ax = (o) => Object.assign({}, AX, o);

// ===================== 1 TITLE =====================
sec = 'Introduction'; pres.addSection({ title: sec });
let s = pres.addSlide({ masterName: 'TITLE', sectionTitle: sec });
s.addText('Leaf-level hyperspectral analysis of white rust in mustard: methodology and results', { placeholder: 'title' });
s.addText('ASD leaf spectra, four dates (Feb–Mar 2026) | Objective 1 tiers and Objective 2 models | six-grade classification and plot PDI regression', { placeholder: 'body' });

// ===================== 2 OUTLINE =====================
s = slide('Outline');
const parts = [['1', 'Study and data', 'Objectives, design, ground truth (Tier 0)'], ['2', 'Methodology flow with results', 'Objective 1 and Objective 2 flow charts'], ['3', 'Pre-processing and features', 'Splice, smoothing, derivatives, 1047 bands, 48 indices'],
  ['4', 'Objective 1 tiers', 'Band selection, WRI, ANOVA, CDA, Boruta, SWIR regions'], ['5', 'Objective 2 models', 'Nested selection, classification, regression'], ['6', 'Results and discussion', 'Major results, findings, implications, conclusions']];
parts.forEach((p, i) => {
  const x = 0.5 + (i % 3) * 4.15, y = 1.45 + Math.floor(i / 3) * 2.55;
  s.addShape(pres.shapes.ROUNDED_RECTANGLE, { x, y, w: 3.9, h: 2.25, fill: { color: X.light }, line: { color: X.light }, rectRadius: 0.1, objectName: 'part ' + p[0] });
  s.addShape(pres.shapes.OVAL, { x: x + 0.25, y: y + 0.3, w: 0.7, h: 0.7, fill: { color: i < 3 ? X.teal : X.berry }, line: { color: i < 3 ? X.teal : X.berry }, objectName: 'part num ' + p[0] });
  s.addText(p[0], { isTextBox: true, x: x + 0.25, y: y + 0.3, w: 0.7, h: 0.7, align: 'center', valign: 'middle', fontSize: 20, bold: true, color: 'FFFFFF', margin: 0 });
  s.addText(p[1], { isTextBox: true, x: x + 1.1, y: y + 0.3, w: 2.65, h: 0.7, fontSize: 17, bold: true, color: X.dark, valign: 'middle', margin: 0 });
  s.addText(p[2], { isTextBox: true, x: x + 0.25, y: y + 1.15, w: 3.45, h: 0.95, fontSize: 13, color: X.text, valign: 'top', margin: 0 });
});

// ===================== 3 BACKGROUND =====================
s = slide('Background and objectives of the leaf-level analysis');
bul(s, ['White rust (Albugo candida) causes white pustules, chlorosis and staghead in mustard (Saharan et al., 2014)', 'Leaf spectra carry the pure disease signal without soil, shadow, flowers or illumination effects (Mahlein et al., 2012; Mahlein, 2016)',
  'They define which wavelengths and indices to look for in UAV and satellite data', 'The proposed tier methodology was applied unchanged in logic to the ASD leaf data'], { x: 0.5, y: 1.35, w: 6.2, h: 4.6, fontSize: 16 });
card(s, 7.0, 1.4, 2.8, 1.5, 'Objective 1', 'Which wavelengths and indices respond to white rust?', X.teal, 'o1', 22);
card(s, 10.0, 1.4, 2.8, 1.5, 'Objective 2', 'How well can grades and PDI be predicted?', X.berry, 'o2', 22);
card(s, 7.0, 3.1, 2.8, 1.5, '6 grades', 'leaf classification (0, 1, 3, 5, 7, 9)', X.mustard, 'g6', 26);
card(s, 10.0, 3.1, 2.8, 1.5, 'PDI', 'plot-level regression from plot-mean spectra', X.green, 'pdi', 26);
output(s, 'A complete, referenced chain from raw ASD spectra to disease-sensitive features and validated severity models.');

// ===================== 4 FLOW OBJ 1 WITH RESULTS =====================
section('Methodology flow with results', 'Every step, its reference and its result');
s = slide('Objective 1 flow: methods, references and results');
const f1 = [
  ['Tier 0  Data and labels', '2339 leaves, 48 plots, 4 dates; grade 0–9; plot PDI; LORO folds', 'Conn et al., 1990; Wheeler, 1969', k.n_leaves + ' leaves, ' + k.n_pd + ' plot-dates, PDI 0–' + k.pdi_max + '%'],
  ['Pre-processing', 'Splice correction; 400–2400 nm; water bands removed; SG smoothing; FD, SD', 'Hueni and Bialek, 2017; Savitzky and Golay, 1964', k.n_bands + ' bands × R, FD, SD = 1047 features'],
  ['Tier 1  Features', 'Red edge (REP, Dr, SDr); 39 base + 9 SWIR indices', 'Horler et al., 1983; Apan et al., 2004', '1047 band + 51 features per spectrum'],
  ['Tier 2  Scalogram + ReliefF', 'r with PDI; ReliefF on 6 grades; one band per correlated region', 'Shukla et al., 2024; Robnik-Šikonja and Kononenko, 2003', k.n_rob + ' robust, ' + k.n_reg + ' regression, ' + k.n_cls + ' classification bands'],
  ['Tier 3  White Rust Index', 'ND + w·R search (VNIR, SWIR); 8-fold plot-grouped CV', 'Mahlein et al., 2013', k.wri + '; BA ' + k.wri_ba + '; r ' + k.wri_r],
  ['Tier 4  ANOVA + Tukey', 'Six grades (leaves); Pearson r with PDI (plots)', 'Tukey, 1949; Mahlein et al., 2019', k.n_sig + ' of ' + k.n_feat + ' features p < 0.001; top ' + k.top_f[0] + ' (F ' + k.top_f[1] + ')'],
  ['Tier 5  VIF + stepwise CDA', 'Step 1 bands; step 2 indices + WRI', 'Bhattacharya and Chattopadhyay, 2013', 'One severity axis (' + k.cda1[2] + '%); r₁ ' + k.cda1[1] + '; LORO acc. ' + k.cda1[4]],
  ['Tier 6  Boruta', 'All-relevant selection: grades and PDI', 'Kursa and Rudnicki, 2010', k.bor[0] + ' (classification) and ' + k.bor[2] + ' (regression) DSFs']];
const bw = 2.9, bh = 2.3;
f1.forEach((b, i) => {
  const row = i < 4 ? 0 : 1, col = row === 0 ? i : 7 - i, x = 0.5 + col * 3.15, y = row === 0 ? 1.35 : 3.85;
  const fill = i < 2 ? X.dark : X.teal;
  s.addShape(pres.shapes.ROUNDED_RECTANGLE, { x, y, w: bw, h: bh, fill: { color: 'FFFFFF' }, line: { color: fill, width: 1.5 }, rectRadius: 0.08, objectName: 'flow box ' + i });
  s.addShape(pres.shapes.RECTANGLE, { x: x + 0.02, y: y + 0.02, w: bw - 0.04, h: 0.45, fill: { color: fill }, line: { color: fill }, objectName: 'flow head ' + i });
  s.addText(b[0], { isTextBox: true, x: x + 0.05, y: y + 0.02, w: bw - 0.1, h: 0.45, fontSize: 13, bold: true, color: 'FFFFFF', valign: 'middle', margin: 2 });
  s.addText([{ text: b[1], options: { fontSize: 11, color: X.text, breakLine: true } }, { text: b[2], options: { fontSize: 10, italic: true, color: X.grey, breakLine: true } }, { text: '► ' + b[3], options: { fontSize: 11, bold: true, color: X.berry } }],
    { isTextBox: true, x: x + 0.08, y: y + 0.52, w: bw - 0.16, h: bh - 0.58, valign: 'top', paraSpaceAfter: 4, margin: 2 });
  if (i < 7) {
    if (i === 3) s.addShape(pres.shapes.LINE, { x: x + bw / 2, y: y + bh, w: 0, h: 3.85 - (y + bh), line: { color: X.grey, width: 1.5, endArrowType: 'triangle' } });
    else if (row === 0) s.addShape(pres.shapes.LINE, { x: x + bw, y: y + bh / 2, w: 0.25, h: 0, line: { color: X.grey, width: 1.5, endArrowType: 'triangle' } });
    else s.addShape(pres.shapes.LINE, { x: x - 0.25, y: y + bh / 2, w: 0.25, h: 0, flipH: true, line: { color: X.grey, width: 1.5, endArrowType: 'triangle' } });
  }
});
output(s, 'Disease-sensitive bands, a White Rust Index, ranked responding features, separability of six grades and two disease-specific feature pools.');

// ===================== 5 FLOW OBJ 2 WITH RESULTS =====================
s = slide('Objective 2 flow: nested models and results');
const p2 = [['Tier 2 bands', 'Shukla et al., 2024'], ['Boruta', 'Kursa and Rudnicki, 2010'], ['VIF < 10', 'Dormann et al., 2013'], ['ML-SFFS per model', 'Pudil et al., 1994'], ['Tuning (inner CV)', 'Varma and Simon, 2006'], ['Test held-out replication', 'Roberts et al., 2017']];
p2.forEach((p, i) => {
  const x = 0.5 + i * 2.08;
  s.addShape(pres.shapes.ROUNDED_RECTANGLE, { x, y: 1.35, w: 1.85, h: 1.15, fill: { color: i === 5 ? X.mustard : X.berry }, line: { color: i === 5 ? X.mustard : X.berry }, rectRadius: 0.08, objectName: 'pipe ' + i });
  s.addText([{ text: p[0], options: { bold: true, fontSize: 13, breakLine: true } }, { text: p[1], options: { fontSize: 10, italic: true } }], { isTextBox: true, x, y: 1.35, w: 1.85, h: 1.15, align: 'center', valign: 'middle', color: 'FFFFFF', margin: 3 });
  if (i < 5) s.addShape(pres.shapes.LINE, { x: x + 1.85, y: 1.92, w: 0.23, h: 0, line: { color: X.grey, width: 1.5, endArrowType: 'triangle' } });
});
s.addText('Repeated inside each training replication (leave-one-replication-out); models: SVM, RF, k-NN, MLP; SVR, RFR, k-NN, PLSR, MLP (Cortes and Vapnik, 1995; Breiman, 2001; Wold et al., 2001)', { isTextBox: true, x: 0.5, y: 2.6, w: 12.3, h: 0.45, fontSize: 12, italic: true, color: X.grey, margin: 0 });
s.addText('Six-grade classification (2339 leaves)', { isTextBox: true, x: 0.5, y: 3.15, w: 6.0, h: 0.4, fontSize: 15, bold: true, color: X.teal, margin: 0 });
card(s, 0.5, 3.6, 1.95, 1.45, k.c_mf1, 'macro-F1 (' + k.bc + ')', X.teal, 'cmf1'); card(s, 2.55, 3.6, 1.95, 1.45, k.c_adj, 'within ±1 grade', X.teal, 'cadj'); card(s, 4.6, 3.6, 1.95, 1.45, k.c_det, 'healthy vs diseased', X.teal, 'cdet');
s.addText('Plot PDI regression (192 plot-dates)', { isTextBox: true, x: 6.85, y: 3.15, w: 6.0, h: 0.4, fontSize: 15, bold: true, color: X.berry, margin: 0 });
card(s, 6.85, 3.6, 1.95, 1.45, k.r_r2, 'R² (' + k.br + ')', X.berry, 'rr2'); card(s, 8.9, 3.6, 1.95, 1.45, k.r_rmse, 'RMSE (PDI %)', X.berry, 'rrmse'); card(s, 10.95, 3.6, 1.85, 1.45, k.r_rpd, 'RPD', X.berry, 'rrpd');
bul(s, ['Baselines: PLS-DA full spectrum macro-F1 ' + k.plsda + '; RF on all 53 features ' + k.rfall + '; PLSR full spectrum R² ' + k.plsr + '; RFR all features ' + k.rfrall, 'Bottom-up PDI from predicted leaf grades: R² ' + k.bu_r2], { x: 0.5, y: 5.15, w: 12.3, h: 1.05, fontSize: 13 });
output(s, 'Validated models: compact feature sets (' + k.ofc_sizes[0] + '–' + k.ofc_sizes[1] + ' features) match or exceed all-feature and full-spectrum baselines.');

// ===================== 6 WORKFLOW FIGURE + TIERS TABLE =====================
s = slide('Workflow of the analysis (report Figure 1 and Table 1)');
img(s, 'l_flow', 0.5, 1.3, 5.6, 4.85, 'Workflow with references in the output boxes');
table(s, [['Step', 'Method (reference)', 'Output'], ['Tier 0', 'Grades (Conn et al., 1990); PDI (Wheeler, 1969); LORO folds', 'Labelled tables'], ['Pre-processing', 'Splice (Hueni and Bialek, 2017); SG (Savitzky and Golay, 1964)', 'Clean spectra'],
  ['Tier 1', 'Red edge (Horler et al., 1983); indices (Apan et al., 2004)', '1047 + 51 features'], ['Tier 2', 'Scalogram (Shukla et al., 2024); ReliefF (Robnik-Šikonja and Kononenko, 2003)', 'Band lists'], ['Tier 3', 'WRI search (Mahlein et al., 2013)', 'WRI'],
  ['Tier 4', 'ANOVA + Tukey (Tukey, 1949)', 'Responding features'], ['Tier 5', 'VIF + stepwise CDA (Bhattacharya and Chattopadhyay, 2013)', 'Separability'], ['Tier 6', 'Boruta (Kursa and Rudnicki, 2010)', 'DSF pools'], ['Objective 2', 'Nested LORO; ML-SFFS (Pudil et al., 1994)', 'Validated models']],
  6.4, 1.3, 6.4, [1.25, 3.75, 1.4], 11, 0.44);

// ===================== DATA AND PRE-PROCESSING =====================
section('Study data and pre-processing', 'Tier 0, pre-processing and Tier 1');
s = slide('Tier 0: data, labels and validation design');
bul(s, ['Four ASD files: 11 Feb, 24 Feb, 3 Mar, 13 Mar 2026; 350–2500 nm at 1 nm', '48 plots: 12 controls + 36 inoculated (3 varieties × 4 inoculation dates × 3 replications)', 'Leaf grade 0–9 key → six classes', 'Plot PDI = Σ score / (9 n) × 100 → regression target', 'Leave-one-replication-out; controls split by variety; leaves of a plot never split'], { x: 0.5, y: 1.3, w: 5.1, h: 4.2 });
refs(s, 'Conn et al., 1990; Wheeler, 1969; Roberts et al., 2017.');
table(s, D.t_data, 5.85, 1.3, 6.95, [1.15, 1.15, 0.65, 0.55, 0.55, 0.55, 0.55, 0.55, 0.55, 0.7], 10.5, 0.36);
output(s, k.n_leaves + ' labelled leaf spectra and ' + k.n_pd + ' plot-dates (PDI 0–' + k.pdi_max + '%); three balanced LORO folds.');

s = slide('Tier 0: grade distribution across dates');
s.addChart(pres.charts.BAR, [0, 1, 3, 5, 7, 9].map((g, i) => ({ name: 'Grade ' + g, labels: Object.keys(D.counts).map(d => d.slice(5)), values: Object.keys(D.counts).map(d => D.counts[d][i]) })),
  ax({ x: 0.5, y: 1.3, w: 7.6, h: 4.85, barDir: 'col', barGrouping: 'stacked', chartColors: GC, showLegend: true, legendPos: 'b', showTitle: true, title: 'Leaves per grade and date (month-day)', valAxisTitle: 'Leaves', showValAxisTitle: true }));
bul(s, ['11 February: mostly grades 0–1 (onset)', 'From 24 February all grades present', '13 March: grades 5 and 7 dominate', 'Controls remain grade 0 on all dates', 'Grade 9 is the smallest class: class weights and macro-F1 are needed'], { x: 8.4, y: 1.4, w: 4.4, h: 4.6 });
output(s, 'All six grades represented; severity increases over time; unequal class sizes handled in modelling.');

s = slide('Pre-processing of the ASD spectra');
bul(s, ['Splice correction at 1000 nm (mean step ' + k.splice + ')', '400–2400 nm kept; 350–399 nm noisy', '1350–1450 and 1800–1950 nm removed', 'Savitzky–Golay smoothing, 11 nm, 2nd order', 'First and second derivatives', '5 nm bands → 349 × (R, FD, SD)', 'Plot spectrum = mean of leaves per plot-date'], { x: 0.5, y: 1.3, w: 5.1, h: 4.2 });
refs(s, 'Hueni and Bialek, 2017; Thenkabail et al., 2004; Savitzky and Golay, 1964; Tsai and Philpot, 1998.');
img(s, 'l_spectra', 5.8, 1.35, 7.0, 4.5, 'Mean leaf reflectance (a) and first derivative (b) of the six grades');
output(s, 'Clean spectra: visible and SWIR reflectance rise, NIR falls and the red-edge peak drops and shifts with increasing grade.');

s = slide('Tier 1: features extracted from each spectrum');
card(s, 0.5, 1.35, 2.9, 1.45, '1047', 'band features: R, FD, SD at 349 bands', X.teal, 'f1');
card(s, 3.6, 1.35, 2.9, 1.45, '39', 'base indices: pigment, structure, water', X.green, 'f2');
card(s, 0.5, 3.0, 2.9, 1.45, '9', 'SWIR disease indices', X.berry, 'f3');
card(s, 3.6, 3.0, 2.9, 1.45, '3', 'red-edge parameters: REP, Dr, SDr', X.mustard, 'f4');
refs(s, 'Horler et al., 1983; Filella and Peñuelas, 1994; Blackburn, 1998; Gitelson et al., 2001; Apan et al., 2004; Gao, 1996; Hunt and Rock, 1989; Mandal et al., 2023.', { y: 4.7, w: 6.0, h: 0.8 });
table(s, [['SWIR index', 'Formula', 'Reference'], ['DWSI-2', 'R1660/R550', 'Apan et al., 2004'], ['DWSI-3', 'R1660/R680', 'Apan et al., 2004'], ['DWSI-5', '(R800+R550)/(R1660+R680)', 'Apan et al., 2004'], ['NDWI', '(R860−R1240)/(R860+R1240)', 'Gao, 1996'],
  ['MSI', 'R1600/R820', 'Hunt and Rock, 1989'], ['NDII', '(R819−R1649)/(R819+R1649)', 'Hardisky et al., 1983'], ['RBI_M / NDBI', 'R1148, R1301', 'Mandal et al., 2023'], ['RBI_R', '(R1068−R1560)/(R1068+R1560)', 'Ramalingam et al., 2026']], 6.8, 1.35, 6.0, [1.4, 2.6, 2.0], 11, 0.4);
output(s, 'Leaf feature table (2339 × 1098) and plot feature table (192 × 1098) from leaf and plot-mean spectra.');

// ===================== OBJECTIVE 1 =====================
section('Objective 1: characterisation (Tiers 2–6)', 'Methods, figures, tables and outputs of each tier');
s = slide('Tier 2: correlation scalogram and ReliefF');
bul(s, ['Scalogram: Pearson r of R, FD, SD with plot PDI (n = 192)', 'Candidates: p < 0.01 and top 5% |r|', 'ReliefF: six grades, k = 10, same-plot neighbours excluded; top 5% weights', 'One band per correlated region (r ≥ 0.95)', 'Derivatives near splice and water-band edges not eligible'], { x: 0.5, y: 1.3, w: 5.1, h: 4.2 });
refs(s, 'Shukla et al., 2024; Cheng et al., 2010; Robnik-Šikonja and Kononenko, 2003; Tian et al., 2021.');
img(s, 'l_scal_relief', 5.8, 1.3, 7.0, 4.85, '');
output(s, 'Strongest correlation: FD at ' + k.maxr_fd[1] + ' nm (r = ' + k.maxr_fd[0] + '); reflectance at ' + k.maxr_r[1] + ' nm (r = ' + k.maxr_r[0] + '); ReliefF peaks in the red edge.');

s = slide('Tier 2 results: correlated regions and band lists');
img(s, 'l_regions', 0.5, 1.3, 5.2, 4.85, 'Band-to-band correlation with correlated regions');
table(s, D.t_bands, 6.0, 1.3, 6.8, [2.3, 2.25, 2.25], 10, 0.245);
s.addText('Regions R / FD / SD: ' + k.regions.R + ' / ' + k.regions.FD + ' / ' + k.regions.SD + ';  scalogram ' + k.scal[0] + ' → ' + k.scal[1] + ';  ReliefF ' + k.rel[0] + ' → ' + k.rel[1] + ' (one per region);  median adjacent-band r = ' + k.adj_r,
  { isTextBox: true, x: 6.0, y: 5.72, w: 6.8, h: 0.5, fontSize: 11, color: X.grey, margin: 0 });
output(s, k.n_rob + ' robust bands (red to red edge, 630–860 nm, mostly derivatives), ' + k.n_reg + ' regression-only and ' + k.n_cls + ' classification-only bands.');

s = slide('Tier 3: White Rust Index search');
bul(s, ['WRI = ND(λ1, λ2) + w × R(λ3), w ∈ {−1, −0.5, 0, 0.5, 1}', 'Bands every 6 nm; ND bands ≥ 50 nm apart', 'ReliefF top 25% of bands and NDs (healthy vs diseased)', 'VNIR: ' + k.wri_ncand + ' candidates; SWIR: ' + k.wri_sw_ncand, 'Threshold fitted on training folds; 8-fold plot-grouped CV'], { x: 0.5, y: 1.3, w: 5.1, h: 4.2 });
refs(s, 'Mahlein et al., 2013; Robnik-Šikonja and Kononenko, 2003.');
img(s, 'l_wri', 5.8, 1.5, 7.0, 4.4, 'ReliefF weights (a) and best VNIR (b) and SWIR (c) indices by grade');
output(s, 'WRI = ' + k.wri + ': balanced accuracy ' + k.wri_ba + ', r with PDI ' + k.wri_r + '; SWIR index ' + k.wri_sw + ' weaker (' + k.wri_sw_ba + ').');

s = slide('Tier 3 results: best candidates and WRI by grade');
table(s, D.t_wri, 0.5, 1.35, 6.6, [2.9, 1.25, 1.25, 1.2], 11, 0.38);
s.addChart(pres.charts.BAR, [{ name: 'Mean WRI', labels: ['G0', 'G1', 'G3', 'G5', 'G7', 'G9'], values: D.wri_means }],
  ax({ x: 7.4, y: 1.3, w: 5.4, h: 4.85, barDir: 'col', chartColors: GC, showValue: true, dataLabelPosition: 'outEnd', dataLabelFormatCode: '0.000', showLegend: false, showTitle: true, title: 'Mean VNIR WRI by leaf grade' }));
output(s, 'The WRI decreases steadily from grade 0 to 9, combining NIR structure (750 nm), water (948 nm) and red-edge chlorophyll (696 nm).');

s = slide('Tier 4: univariate response (ANOVA, Tukey HSD, r with PDI)');
bul(s, ['One-way ANOVA across six grades (leaves): F, η²', 'Tukey HSD pairwise grade groups', 'Pearson r with PDI (plot-mean features)', 'Spearman ρ with leaf grade', 'p-values used only to rank (leaves within plots)'], { x: 0.5, y: 1.3, w: 5.1, h: 4.0 });
refs(s, 'Tukey, 1949; Gomez and Gomez, 1984; Spearman, 1904; Mahlein et al., 2019.');
table(s, D.t_anova, 5.8, 1.3, 7.0, [1.35, 1.25, 0.9, 0.9, 1.3, 1.3], 11, 0.35);
output(s, k.n_sig + ' of ' + k.n_feat + ' features differ at p < 0.001; strongest: red-edge FD (' + k.top_f[0] + ', F ' + k.top_f[1] + ', η² ' + k.top_f[2] + '), WRI, red-edge SD, RVSI, HI, ARI.');

s = slide('Tier 4 results: grade responses and Tukey groups');
img(s, 'l_anova', 0.5, 1.3, 7.4, 4.85, 'Six strongest features by grade with Tukey letters');
table(s, D.t_tukey, 8.2, 1.4, 4.6, [1.3, 0.55, 0.55, 0.55, 0.55, 0.55, 0.55], 11, 0.38);
bul(s, ['Grades sharing a letter do not differ (Tukey, 1949)', 'First derivatives and WRI separate all six grades'], { x: 8.2, y: 4.3, w: 4.6, h: 1.8, fontSize: 13 });
output(s, 'Monotonic response with severity; grades 0 and 1 overlap for some second-derivative features and RVSI.');

s = slide('Tier 4 results: SWIR indices and relation with PDI');
table(s, D.t_swir, 0.5, 1.35, 5.0, [1.5, 1.1, 1.1, 1.3], 11, 0.38);
img(s, 'l_r_pdi', 5.8, 1.5, 7.0, 3.6, 'Plot PDI against the four indices most correlated with it (colour = date)');
refs(s, 'Apan et al., 2004; Gao, 1996; Hunt and Rock, 1989; Hardisky et al., 1983; Yu et al., 2018; Kundu et al., 2021.', { x: 0.5, y: 5.25, w: 5.0, h: 0.85 });
output(s, 'SWIR water indices respond to white rust; strongest ' + k.swir_best[0] + ' (r = ' + k.swir_best[1] + '); |r| up to ' + k.swir_maxr + '.');

s = slide('Tier 5: VIF and two-step stepwise CDA');
bul(s, ['VIF < 10 removes collinear features', 'Forward stepwise selection by Wilks\' lambda (p < 0.001, ≤ 10 variables)', 'Step 1: classification bands; step 2: indices + red edge + WRI', 'LDA (equal priors) accuracy on held-out replications'], { x: 0.5, y: 1.3, w: 5.1, h: 3.9 });
refs(s, 'Dormann et al., 2013; Klecka, 1980; Fisher, 1936; Whittingham et al., 2006; Bhattacharya and Chattopadhyay, 2013.');
table(s, D.t_cda, 5.8, 1.3, 7.0, [2.1, 2.45, 2.45], 11, 0.5);
output(s, 'One dominant severity axis (' + k.cda1[2] + '% / ' + k.cda2[2] + '%); r₁ ' + k.cda1[1] + ' / ' + k.cda2[1] + '; six-grade LDA accuracy ' + k.cda1[4] + ' / ' + k.cda2[4] + '; ±1 grade ' + k.cda1[5] + ' / ' + k.cda2[5] + '.');

s = slide('Tier 5 results: canonical score plots');
img(s, 'l_cda', 0.5, 1.3, 12.3, 4.6, 'Canonical scores of the two steps; X = grade centroids ordered 0 → 9 along function 1');
output(s, 'Grades lie on one severity axis; neighbouring grades overlap, so exact six-grade separation is limited (Zhang et al., 2012a).');

s = slide('Tier 6: Boruta disease-specific feature pools');
bul(s, ['Random forest importance vs shuffled shadow features', 'alpha = 0.01, up to 100 iterations', 'Classification on leaves; regression on plots'], { x: 0.5, y: 1.3, w: 4.6, h: 3.0 });
refs(s, 'Kursa and Rudnicki, 2010; Mustafa et al., 2023.', { w: 4.6 });
img(s, 'l_boruta', 5.3, 1.3, 7.5, 4.85, '');
output(s, k.bor[0] + ' of ' + k.bor[1] + ' features confirmed for classification; ' + k.bor[2] + ' of ' + k.bor[3] + ' for regression, led by the WRI.');

s = slide('Tier 6 results: disease-specific feature (DSF) pools');
table(s, D.t_dsf, 0.5, 1.35, 12.3, [2.6, 9.7], 13, [0.45, 1.2, 0.9]);
bul(s, ['Classification pool: red-edge derivatives plus pigment indices (HI, ARI, NPCI, PRI)', 'Regression pool: WRI, red reflectance (695 nm), red-edge derivatives, DWSI-5', 'Agreement with ANOVA ranking and CDA variables'], { x: 0.5, y: 4.3, w: 12.3, h: 1.8 });
output(s, 'Two DSF pools: classification and regression, the inputs of Objective 2.');

s = slide('Additional analysis: robust SWIR regions');
bul(s, ['Tier 2 repeated on 1000–2400 nm only', 'Stability tested in each training fold and by date'], { x: 0.5, y: 1.3, w: 5.1, h: 1.2 });
table(s, D.t_swirreg, 0.5, 2.5, 12.3, [2.6, 9.7], 12, 0.6);
bul(s, ['1595–1615 nm: SWIR-1 water and dry matter (same region as MSI, NDII, DWSI)', '1495–1515 nm and 1965–1995 nm: shoulders of leaf-water absorption bands', 'SWIR signal stronger at higher severity (later dates)'], { x: 0.5, y: 4.95, w: 12.3, h: 1.25, fontSize: 13 });
output(s, 'Robust SWIR regions (1495–1515, 1595–1615, 1965–1995 nm) reflect leaf-water loss; 1595–1615 nm is the most usable for UAV and satellite sensors.');

// ===================== OBJECTIVE 2 =====================
section('Objective 2: classification and regression', 'Nested leave-one-replication-out models');
s = slide('Nested selection in each training fold');
bul(s, ['All selection repeated on training replications only', 'ML-SFFS: floating forward selection, inner 3-fold plot-grouped CV', 'Smallest subset within 0.01 (2% RMSE) of the best'], { x: 0.5, y: 1.3, w: 12.3, h: 1.2 });
table(s, D.t_folds, 0.5, 2.5, 12.3, [1.1, 1.3, 1.3, 1.2, 3.7, 3.7], 11, 0.6);
refs(s, 'Pudil et al., 1994; Tian et al., 2021; Varma and Simon, 2006; Ambroise and McLachlan, 2002.', { x: 0.5, y: 5.2, w: 12.3, h: 0.5 });
output(s, 'Compact, fold-specific optimum feature sets; red-edge derivatives and pigment/water indices recur across folds.');

s = slide('ML-SFFS curves (fold 1 training data)');
img(s, 'l_sffs', 0.5, 1.3, 12.3, 4.6, 'Inner-CV score against number of selected features: classification (a) and regression (b)');
output(s, 'Performance saturates after a few features, supporting compact models and limiting overfitting.');

s = slide('Six-grade leaf classification');
table(s, D.t_cls, 0.5, 1.35, 6.9, [2.3, 0.75, 0.8, 0.95, 0.9, 1.2], 11, 0.42);
const ck = Object.keys(D.cls_bar);
s.addChart(pres.charts.BAR, [{ name: 'Macro-F1', labels: ck, values: ck.map(c => D.cls_bar[c][0]) }, { name: '±1 grade', labels: ck, values: ck.map(c => D.cls_bar[c][1]) }],
  ax({ x: 7.6, y: 1.3, w: 5.2, h: 4.85, barDir: 'col', chartColors: [X.teal, X.mustard], showValue: true, dataLabelPosition: 'outEnd', dataLabelFormatCode: '0.00', showLegend: true, legendPos: 'b', valAxisMaxVal: 1, valAxisMinVal: 0, showTitle: true, title: 'Held-out performance', catAxisLabelFontSize: 9 }));
refs(s, 'Cortes and Vapnik, 1995; Breiman, 2001; Cover and Hart, 1967; Rumelhart et al., 1986; Cohen, 1960; Sokolova and Lapalme, 2009.', { x: 0.5, y: 4.4, w: 6.9, h: 0.6 });
output(s, 'Best ' + k.bc + ': macro-F1 ' + k.c_mf1 + ', OA ' + k.c_oa + ', kappa ' + k.c_kap + ', ±1 grade ' + k.c_adj + ', healthy vs diseased ' + k.c_det + '.');

s = slide('Classification detail: confusion matrix and per-grade metrics');
img(s, 'l_eval', 0.5, 1.3, 8.0, 4.0, 'Confusion matrix (a) and observed vs predicted plot PDI (b)');
table(s, D.t_grade, 8.8, 1.4, 4.0, [1.0, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5], 11, 0.42);
bul(s, ['Grade 0 recognised best', 'Grades 1–5 confused with neighbours', 'Grade 9 partly predicted as 5 or 7'], { x: 8.8, y: 3.4, w: 4.0, h: 2.5, fontSize: 13 });
output(s, 'Errors are mainly between neighbouring grades: grades are cuts of a continuous severity (Mandal et al., 2023; Meng et al., 2020).');

s = slide('Plot-level PDI regression');
table(s, D.t_reg, 0.5, 1.35, 6.9, [3.2, 0.8, 1.2, 0.85, 0.85], 11, 0.42);
const rk = Object.keys(D.reg_bar);
s.addChart(pres.charts.BAR, [{ name: 'R²', labels: rk, values: rk.map(r => D.reg_bar[r]) }],
  ax({ x: 7.6, y: 1.3, w: 5.2, h: 4.85, barDir: 'bar', chartColors: [X.berry], showValue: true, dataLabelPosition: 'outEnd', dataLabelFormatCode: '0.00', showLegend: false, valAxisMaxVal: 1, valAxisMinVal: 0, catAxisOrientation: 'maxMin', showTitle: true, title: 'Held-out R²', catAxisLabelFontSize: 9 }));
refs(s, 'Wold et al., 2001; Breiman, 2001; Cover and Hart, 1967; Chang et al., 2001; Liu et al., 2024.', { x: 0.5, y: 5.3, w: 6.9, h: 0.6 });
output(s, 'Best ' + k.br + ': R² ' + k.r_r2 + ', RMSE ' + k.r_rmse + ' PDI units, RPD ' + k.r_rpd + '; bottom-up PDI from leaf grades R² ' + k.bu_r2 + '.');

s = slide('Model comparison (report figure)');
img(s, 'l_models', 0.5, 1.3, 12.3, 4.6, 'Six-grade classification (a) and PDI regression (b) on held-out replications');
output(s, 'Selected-feature models are as good as or better than all-feature and full-spectrum baselines with far fewer features.');

s = slide('Performance by date and variety');
table(s, D.t_date, 0.5, 1.35, 6.6, [1.6, 1.0, 1.3, 1.3, 1.4], 12, 0.5);
table(s, D.t_var, 7.4, 1.35, 5.4, [1.6, 1.9, 1.9], 12, 0.5);
bul(s, ['11 February: little PDI variation, so R² is not meaningful though RMSE is smallest', 'Similar performance across varieties: features are not variety-specific'], { x: 0.5, y: 4.4, w: 12.3, h: 1.6 });
output(s, 'Models are consistent across dates with sufficient severity range and across the three varieties.');

// ===================== RESULTS AND DISCUSSION =====================
section('Results, findings and discussion', 'What the leaf analysis shows and what it means');
s = slide('Outputs of each step');
table(s, [['Step', 'Output', 'Key result'], ['Tier 0', 'Labelled data, folds', k.n_leaves + ' leaves; ' + k.n_pd + ' plot-dates'], ['Pre-processing', 'Clean spectra', '349 bands × R, FD, SD'], ['Tier 1', 'Feature tables', '1047 band + 51 features'],
  ['Tier 2', 'Band lists', k.n_rob + ' robust bands (630–860 nm); max r ' + k.maxr_fd[0] + ' (FD' + k.maxr_fd[1] + ')'], ['Tier 3', 'White Rust Index', k.wri + '; BA ' + k.wri_ba + '; r ' + k.wri_r], ['Tier 4', 'Responding features', k.n_sig + '/' + k.n_feat + ' significant; SWIR |r| up to ' + k.swir_maxr],
  ['Tier 5', 'Separability', 'One severity axis; r₁ ' + k.cda1[1] + '; ±1 grade ' + k.cda1[5]], ['Tier 6', 'DSF pools', k.bor[0] + ' classification, ' + k.bor[2] + ' regression features'], ['SWIR analysis', 'Robust SWIR regions', '1495–1515, 1595–1615, 1965–1995 nm'],
  ['Objective 2 (grades)', 'Classifier', k.bc + ': macro-F1 ' + k.c_mf1 + '; ±1 grade ' + k.c_adj + '; healthy vs diseased ' + k.c_det], ['Objective 2 (PDI)', 'Regressor', k.br + ': R² ' + k.r_r2 + '; RMSE ' + k.r_rmse + '; RPD ' + k.r_rpd]],
  0.5, 1.3, 12.3, [2.3, 2.6, 7.4], 12, 0.4);

s = slide('Major results');
card(s, 0.5, 1.35, 2.9, 1.6, k.maxr_fd[0], 'max r with PDI: red-edge FD at ' + k.maxr_fd[1] + ' nm', X.teal, 'm1');
card(s, 3.6, 1.35, 2.9, 1.6, k.wri_ba, 'WRI balanced accuracy (healthy vs diseased)', X.mustard, 'm2');
card(s, 6.7, 1.35, 2.9, 1.6, k.swir_maxr, 'max |r| of SWIR water indices with PDI', X.green, 'm3');
card(s, 9.8, 1.35, 3.0, 1.6, k.cda1[2] + '%', 'separation on one canonical severity axis', X.berry, 'm4');
card(s, 0.5, 3.2, 2.9, 1.6, k.c_mf1, 'six-grade macro-F1 (' + k.bc + ')', X.teal, 'm5');
card(s, 3.6, 3.2, 2.9, 1.6, k.c_adj, 'leaves within ±1 grade', X.mustard, 'm6');
card(s, 6.7, 3.2, 2.9, 1.6, k.c_det, 'healthy vs diseased accuracy', X.green, 'm7');
card(s, 9.8, 3.2, 3.0, 1.6, k.r_r2, 'plot PDI R² (' + k.br + ', 4 features)', X.berry, 'm8');
bul(s, ['All accuracies are from held-out replications with every selection step nested in the training data'], { x: 0.5, y: 5.05, w: 12.3, h: 0.6, fontSize: 13 });
output(s, 'Red edge and WRI carry the white-rust signal; SWIR adds water information; PDI is predicted better than exact grades.');

s = slide('Key findings and literature support');
table(s, [['Finding', 'Evidence in this study', 'Literature'], ['Red-edge derivatives are the most robust features', 'Tiers 2, 4, 5, 6 all select FD/SD at 680–860 nm', 'Horler et al., 1983; Filella and Peñuelas, 1994; Shukla et al., 2024'],
  ['A disease-specific index works better than general indices', 'WRI top univariate and regression feature', 'Mahlein et al., 2013; Ashourloo et al., 2014; Meng et al., 2020'], ['SWIR adds water-loss information', 'DWSI-5, MSI, NDII, NDWI respond; DWSI-5 in DSF pool', 'Apan et al., 2004; Yu et al., 2018; Kundu et al., 2021'],
  ['Neighbouring grades overlap', 'One canonical axis; errors mostly adjacent', 'Mandal et al., 2023; Meng et al., 2020; Lv et al., 2023'], ['PDI regression is more reliable than exact grades', 'Plot averaging reduces within-plot noise', 'Liu et al., 2024; Feng et al., 2022'],
  ['Compact nested models generalise', 'Selected features match all-feature baselines', 'Varma and Simon, 2006; Tian et al., 2021; Mustafa et al., 2023']], 0.5, 1.3, 12.3, [3.6, 4.0, 4.7], 12, 0.62);

s = slide('Discussion: physiological interpretation');
const dz = [['Red edge', 'Pustules and chlorosis reduce chlorophyll and disturb mesophyll structure, lowering and shifting the red-edge slope; first derivatives at 790–830 nm capture this best (Horler et al., 1983; Carter and Knapp, 2001).', X.teal],
  ['White Rust Index', 'Combines NIR plateau (750 nm), the 970 nm water-band shoulder (948 nm) and red-edge chlorophyll (696 nm): structure, water and pigment in one index (Mahlein et al., 2013).', X.mustard],
  ['SWIR', 'Infected leaves lose water, raising reflectance near 1500, 1600 and 1970 nm; the SWIR signal grows with severity, so it is a severity rather than an early marker (Apan et al., 2004).', X.green]];
dz.forEach((d, i) => {
  const x = 0.5 + i * 4.15;
  s.addShape(pres.shapes.ROUNDED_RECTANGLE, { x, y: 1.35, w: 3.95, h: 4.75, fill: { color: X.light }, line: { color: X.light }, rectRadius: 0.1, objectName: 'disc ' + i });
  s.addText(d[0], { isTextBox: true, x: x + 0.2, y: 1.5, w: 3.55, h: 0.6, fontSize: 20, bold: true, color: d[2], fontFace: 'Cambria', margin: 0 });
  s.addText(d[1], { isTextBox: true, x: x + 0.2, y: 2.2, w: 3.55, h: 3.7, fontSize: 14, color: X.text, valign: 'top', margin: 0 });
});
output(s, 'The selected features are physically meaningful, which supports their transfer to UAV and satellite sensors.');

s = slide('Discussion: severity, validation and other studies');
bul(s, ['Exact six-grade accuracy (macro-F1 ' + k.c_mf1 + ') is limited because grades 0 and 1 differ by only 1–5% leaf area and neighbouring grades overlap spectrally', 'Similar limits: 70% for three yellow-rust levels (Meng et al., 2020); severity 81.8% vs detection 93.1% (Lv et al., 2023); adjacent blast grades inseparable (Mandal et al., 2023)',
  'Within-one-grade accuracy (' + k.c_adj + ') and healthy-vs-diseased accuracy (' + k.c_det + ') are the decision-relevant measures', 'Plot PDI (R² ' + k.r_r2 + ') is predicted better than leaf grades because averaging leaves removes within-plot variation; bottom-up PDI from leaf grades (R² ' + k.bu_r2 + ') confirms consistency',
  'Nested leave-one-replication-out validation gives honest accuracy; selecting on all data would inflate it (Varma and Simon, 2006)'], { x: 0.5, y: 1.3, w: 12.3, h: 4.85, fontSize: 15 });
output(s, 'Report PDI regression and ±1-grade accuracy alongside exact grade accuracy.');

s = slide('Implications for UAV and satellite analysis, and limitations');
s.addText('Implications', { isTextBox: true, x: 0.5, y: 1.3, w: 6.0, h: 0.45, fontSize: 18, bold: true, color: X.teal, margin: 0 });
bul(s, ['Prioritise the red edge (690–860 nm) in UAV band selection; MS red-edge band expected to be most useful', 'Test the leaf WRI on UAV canopy spectra (recalibration likely)', 'Use SWIR water indices and 1595–1615 nm as complementary features', 'Apply the same nested chain (Tier 2 → Boruta → VIF → ML-SFFS) to UAV data'], { x: 0.5, y: 1.8, w: 6.0, h: 4.3, fontSize: 14 });
s.addText('Limitations', { isTextBox: true, x: 6.8, y: 1.3, w: 6.0, h: 0.45, fontSize: 18, bold: true, color: X.berry, margin: 0 });
bul(s, ['Leaf data are an upper bound for canopy performance (Mahlein, 2016)', 'WRI formula searched on all leaves; threshold and accuracy cross-validated', 'Leaf-level p-values optimistic (leaves within plots)', 'One season, one site; independent validation pending', 'Physiological measurements (pigments, RWC) to be added'], { x: 6.8, y: 1.8, w: 6.0, h: 4.3, fontSize: 14 });
output(s, 'Leaf results fix the wavelengths and index to test at canopy and satellite scale.');

s = slide('Conclusions');
const cc = [['1', 'Red-edge first and second derivatives (680–860 nm) are the most robust white-rust features'], ['2', 'A VNIR White Rust Index (' + k.wri + ') separates healthy and diseased leaves and tracks PDI'], ['3', 'SWIR water regions (1495–1515, 1595–1615, 1965–1995 nm) add severity information'],
  ['4', 'Severity acts as one spectral axis; neighbouring grades overlap, so PDI and ±1-grade accuracy are essential'], ['5', 'Compact nested models predict plot PDI well and give honest accuracy estimates']];
cc.forEach((c, i) => {
  const y = 1.35 + i * 0.95;
  s.addShape(pres.shapes.OVAL, { x: 0.6, y: y + 0.1, w: 0.6, h: 0.6, fill: { color: X.teal }, line: { color: X.teal }, objectName: 'conc ' + c[0] });
  s.addText(c[0], { isTextBox: true, x: 0.6, y: y + 0.1, w: 0.6, h: 0.6, align: 'center', valign: 'middle', fontSize: 16, bold: true, color: 'FFFFFF', margin: 0 });
  s.addText(c[1], { isTextBox: true, x: 1.4, y, w: 11.4, h: 0.8, fontSize: 16, color: X.text, valign: 'middle', margin: 0 });
});
output(s, 'Next: apply the same chain to UAV hyperspectral, multispectral, RGB and thermal data and test transfer to satellite bands.');

// ===================== REFERENCES =====================
const R = D.refs.concat(['Cohen, J. (1960). A coefficient of agreement for nominal scales. Educational and Psychological Measurement 20(1), 37–46.', 'Sokolova, M., Lapalme, G. (2009). A systematic analysis of performance measures for classification tasks. Information Processing and Management 45(4), 427–437.']).sort((a, b) => a.localeCompare(b)); const chunks = []; for (let i = 0; i < R.length; i += 16) chunks.push(R.slice(i, i + 16));
chunks.forEach((part, j) => {
  const s2 = slide('References (' + (j + 1) + '/' + chunks.length + ')'); const h = Math.ceil(part.length / 2);
  [part.slice(0, h), part.slice(h)].forEach((col, c) => s2.addText(col.map((r, i) => ({ text: r, options: { breakLine: i < col.length - 1 } })), { isTextBox: true, x: 0.5 + c * 6.25, y: 1.3, w: 6.05, h: 5.6, fontSize: 10, color: X.text, valign: 'top', paraSpaceAfter: 2 }));
});
pres.writeFile({ fileName: OUT }).then(async () => { await applyTheme(OUT, THEME); console.log('saved', OUT); });
