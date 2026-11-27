// Slide deck: plot-level evaluation of the three random-forest pixel maps (UAV hyperspectral image, 24 Feb 2026).
// Data: deck_data.json (prep_data.py) from outputs/Plot_level_evaluation_RF_24Feb2026_step4. Output: same folder, .pptx
const pptxgen = require('pptxgenjs');
const path = require('path');
const fs = require('fs');
const { applyTheme } = require(process.env.PPTX_SKILL + '/scripts/apply_theme.js');
const D = JSON.parse(fs.readFileSync(path.join(__dirname, 'deck_data.json'), 'utf8'));
const OUTDIR = path.join(__dirname, '../../outputs/Plot_level_evaluation_RF_24Feb2026_step4');
const OUT = path.join(OUTDIR, 'Plot_level_evaluation_RF_maps_24Feb2026.pptx');
const FIG6 = path.join(OUTDIR, 'fig6_plot_maps.png');

const THEME = {
  name: 'Mustard field', headFontFace: 'Cambria', bodyFontFace: 'Calibri',
  colors: { dk1: '1E2B24', lt1: 'FFFFFF', dk2: '1F4D3A', lt2: 'EEF3EF', accent1: 'C99A12', accent2: '1A9850', accent3: 'C62D28',
            accent4: '4F7F6A', accent5: 'E86A3A', accent6: '6B7570', hlink: '1F4D3A', folHlink: '4F7F6A' },
};
const H = THEME.colors;           // hex values for hex-only options (chart colours, grid lines, shades)
const pres = new pptxgen();
pres.layout = 'LAYOUT_WIDE';      // 13.333 x 7.5 in
pres.theme = { headFontFace: THEME.headFontFace, bodyFontFace: THEME.bodyFontFace };
pres.title = 'Plot-level evaluation of the random-forest disease maps';
pres.subject = 'White rust of mustard, UAV hyperspectral image of 24 February 2026';
const C = pres.SchemeColor;
const W = 13.333, M = 0.6, CW = W - 2 * M;
const M3 = ['det', 'grd', 'scr'];
const NAME = { det: 'RF detection', grd: 'RF six grades', scr: 'RF severity score' };
const fx = (v, d = 2) => (v === null || v === undefined || Number.isNaN(v) ? '–' : Number(v).toFixed(d).replace(/^-/, '\u2212'));
const met = (k, key) => D.metrics[k][key];
const boot = (k, key) => D.boot[k][key];

// ---------- layouts
pres.defineSlideMaster({
  title: 'TITLE_DARK', background: { color: C.text2 },
  objects: [
    { placeholder: { options: { name: 'title', type: 'title', x: M, y: 2.0, w: CW, h: 1.6, fontFace: THEME.headFontFace, fontSize: 40, bold: true, color: C.background1, align: 'left', valign: 'bottom' }, text: '' } },
    { placeholder: { options: { name: 'body', type: 'body', x: M, y: 3.85, w: CW, h: 1.6, fontSize: 18, color: C.background2, align: 'left', valign: 'top' }, text: '' } },
  ],
});
pres.defineSlideMaster({
  title: 'CLOSING_DARK', background: { color: C.text2 },
  objects: [
    { placeholder: { options: { name: 'title', type: 'title', x: M, y: 0.35, w: CW, h: 0.95, fontFace: THEME.headFontFace, fontSize: 36, bold: true, color: C.background1, align: 'left', valign: 'middle' }, text: '' } },
  ],
});
pres.defineSlideMaster({
  title: 'CONTENT', background: { color: C.background1 }, margin: [0.5, 0.6, 0.6, 0.6],
  objects: [
    { placeholder: { options: { name: 'title', type: 'title', x: M, y: 0.35, w: CW, h: 0.85, fontFace: THEME.headFontFace, fontSize: 32, bold: true, color: C.text2, align: 'left', valign: 'middle' }, text: '' } },
    { text: { text: 'White rust of mustard · UAV hyperspectral image, 24 Feb 2026 · plot-level evaluation', options: { x: M, y: 7.0, w: 9, h: 0.3, fontSize: 10, color: C.accent6, margin: 0 } } },
  ],
  slideNumber: { x: 12.2, y: 7.0, w: 0.55, h: 0.3, fontSize: 10, color: C.accent6, align: 'right' },
});

const card = (s, x, y, w, h, fill, name) => s.addShape(pres.shapes.ROUNDED_RECTANGLE, { x, y, w, h, rectRadius: 0.12, fill: { color: fill }, line: { color: fill }, objectName: name });
const txt = (s, t, o) => s.addText(t, Object.assign({ isTextBox: true, margin: 0, color: C.text1, fontSize: 14, valign: 'top' }, o));
const badge = (s, x, y, label, fill, name) => {
  s.addShape(pres.shapes.OVAL, { x, y, w: 0.5, h: 0.5, fill: { color: fill }, line: { color: fill }, objectName: name });
  txt(s, label, { x, y, w: 0.5, h: 0.5, align: 'center', valign: 'middle', fontSize: 16, bold: true, color: C.background1, objectName: name + ' label' });
};
const axisStyle = () => ({ catAxisLabelColor: H.accent6, valAxisLabelColor: H.accent6, catAxisLabelFontFace: '+mn-lt', valAxisLabelFontFace: '+mn-lt', catAxisLabelFontSize: 11, valAxisLabelFontSize: 11,
  valGridLine: { color: 'D9DED9', size: 0.5 }, catGridLine: { style: 'none' }, catAxisLineColor: 'B8BFBA', valAxisLineShow: false,
  titleFontFace: '+mn-lt', titleColor: H.dk2, titleFontSize: 13, legendFontFace: '+mn-lt', legendFontSize: 11, legendColor: H.dk1,
  valAxisTitleFontFace: '+mn-lt', catAxisTitleFontFace: '+mn-lt', valAxisTitleColor: H.accent6, catAxisTitleColor: H.accent6, valAxisTitleFontSize: 11, catAxisTitleFontSize: 11 });
const TH = (t) => ({ text: t, options: { bold: true, color: C.background1, fill: { color: C.text2 }, align: 'center', valign: 'middle' } });
const TD = (t, o = {}) => ({ text: t, options: Object.assign({ align: 'center', valign: 'middle', color: C.text1 }, o) });

// ======================= 1 Title
pres.addSection({ title: 'Overview' });
let s = pres.addSlide({ masterName: 'TITLE_DARK', sectionTitle: 'Overview' });
s.addText('Plot-level evaluation of the random-forest disease maps', { placeholder: 'title' });
s.addText([
  { text: 'White rust of mustard · UAV hyperspectral image of 24 February 2026 · 48 plots', options: { breakLine: true } },
  { text: 'Three LORO random-forest models applied pixel by pixel; plot values compared with the plot Disease Index', options: { fontSize: 16 } },
], { placeholder: 'body' });
txt(s, `Maps at SPATIAL_STEP ${D.info.step} (preview, 1 pixel in 16); final numbers to be confirmed at full resolution`, { x: M, y: 6.55, w: CW, h: 0.4, fontSize: 12, color: C.accent1, objectName: 'preview note' });
s.addNotes('This deck evaluates the three random-forest models of the ASD leaf analysis (LORO-selected, refitted on all 2330 leaves) after applying them pixel by pixel to the UAV hyperspectral image of 24 February 2026. For each of the 48 plots the pixel classes inside the plot ROI are counted and turned into a plot value, which is compared with the plot Disease Index from the leaf ratings. The maps are previews at SPATIAL_STEP 4; the final numbers will come from a full-resolution run.');

// ======================= 2 Key findings
s = pres.addSlide({ masterName: 'CONTENT', sectionTitle: 'Overview' });
s.addText('Key findings', { placeholder: 'title' });
const kf = [
  { big: '≥ 47/48', lab: 'plots mapped diseased', body: 'With the 50% pixel rule every model calls (almost) every plot diseased: sensitivity 1.00, specificity 0.00–0.08.', col: C.accent3 },
  { big: fx(met('det', 'AUC')), lab: 'AUC of the plot values', body: `Healthy plots still get lower plot values than diseased plots (95% CI about ${fx(boot('scr', 'AUC')[1])}–${fx(boot('det', 'AUC')[2])}): a weak but real signal.`, col: C.accent1 },
  { big: 'ρ ≈ 0', lab: 'severity ranking', body: `Inside the 36 diseased plots the mapped value does not follow the field DI (ρ between ${fx(met('scr', 'Spearman ρ, diseased plots'))} and +${fx(met('det', 'Spearman ρ, diseased plots'))}).`, col: C.accent4 },
];
kf.forEach((k, i) => {
  const x = M + i * (3.85 + 0.275);
  card(s, x, 1.45, 3.85, 3.65, C.background2, 'finding card ' + (i + 1));
  txt(s, k.big, { x: x + 0.3, y: 1.7, w: 3.25, h: 1.1, fontSize: 54, bold: true, color: k.col, fontFace: THEME.headFontFace, valign: 'middle', objectName: 'finding number ' + (i + 1) });
  txt(s, k.lab, { x: x + 0.3, y: 2.85, w: 3.25, h: 0.4, fontSize: 16, bold: true, color: C.text2, objectName: 'finding label ' + (i + 1) });
  txt(s, k.body, { x: x + 0.3, y: 3.35, w: 3.25, h: 1.6, fontSize: 14, objectName: 'finding text ' + (i + 1) });
});
card(s, M, 5.4, CW, 1.25, C.text2, 'takeaway card');
txt(s, 'The leaf models carry a weak presence signal into the UAV image, but their leaf-scale decision rule calls almost every plot diseased, and none of them measures severity at plot level.',
  { x: M + 0.35, y: 5.5, w: CW - 0.7, h: 1.05, fontSize: 18, color: C.background1, valign: 'middle', objectName: 'takeaway text' });
s.addNotes('Three messages. First, with the agreed rule (a plot is diseased when more than half of its crop pixels are diseased) all three maps call almost every plot diseased, so specificity is zero or close to it. Second, the plot values are not random: healthy plots get lower values than diseased plots, AUC 0.73 for all three models with a bootstrap interval above 0.5. Third, within the diseased plots the maps do not rank severity. Likely question: why is accuracy 0.75 if the model is poor? Because 36 of 48 plots are diseased; a map that calls everything diseased gets 0.75.');

// ======================= 3 Data, models, ground truth
pres.addSection({ title: 'Data and method' });
s = pres.addSlide({ masterName: 'CONTENT', sectionTitle: 'Data and method' });
s.addText('Data, models and ground truth', { placeholder: 'title' });
const models = [
  ['A', 'Detection (healthy / diseased)', 'Map: probability and class per pixel · 9 features (FD, REP)', C.accent3],
  ['B', 'Six grades (0, 1, 3, 5, 7, 9)', 'Map: grade per pixel · 9 features (FD, DWSI-2)', C.accent1],
  ['C', 'Severity score (0–9)', 'Map: continuous score per pixel · 7 features (FD, Dr)', C.accent4],
];
txt(s, 'Models – random forest, 500 trees', { x: M, y: 1.4, w: 6.0, h: 0.4, fontSize: 20, bold: true, color: C.text2, objectName: 'models heading' });
models.forEach((m, i) => {
  const y = 1.95 + i * 1.05;
  card(s, M, y, 6.0, 0.85, C.background2, 'model card ' + m[0]);
  badge(s, M + 0.2, y + 0.175, m[0], m[3], 'model badge ' + m[0]);
  txt(s, m[1], { x: M + 0.9, y: y + 0.1, w: 4.9, h: 0.35, fontSize: 16, bold: true, color: C.text2, objectName: 'model name ' + m[0] });
  txt(s, m[2], { x: M + 0.9, y: y + 0.45, w: 4.9, h: 0.33, fontSize: 14, objectName: 'model detail ' + m[0] });
});
txt(s, 'LORO-selected models refitted on all 2330 ASD leaf spectra (4 dates, 2025-26); input = direct UAV reflectance (their best input on the 48 plots).',
  { x: M, y: 5.2, w: 6.0, h: 0.9, fontSize: 14, color: C.accent6, objectName: 'models note' });
const facts = [
  ['48', 'plots: 12 Healthy, 25 High, 11 Very high (plot DI from leaf ratings)'],
  [Number(D.info.crop_pixels).toLocaleString('en-US'), `crop pixels inside the plots (${D.info.px_min}–${D.info.px_max.toLocaleString('en-US')} per plot)`],
  ['0.6', 'NDVI(898, 684) threshold of the crop mask'],
  [String(D.info.step), 'SPATIAL_STEP of the maps (preview; 1 = full resolution)'],
];
txt(s, 'Image and ground truth', { x: 7.05, y: 1.4, w: 5.7, h: 0.4, fontSize: 20, bold: true, color: C.text2, objectName: 'facts heading' });
facts.forEach((f, i) => {
  const y = 1.95 + i * 1.05;
  txt(s, f[0], { x: 7.05, y, w: 1.75, h: 0.85, fontSize: 30, bold: true, color: C.accent1, fontFace: THEME.headFontFace, valign: 'middle', objectName: 'fact number ' + (i + 1) });
  txt(s, f[1], { x: 8.9, y, w: 3.85, h: 0.85, fontSize: 14, valign: 'middle', objectName: 'fact text ' + (i + 1) });
});
s.addNotes('The three models are the random forests of the leaf analysis: features and settings were chosen in the leave-one-replication-out analysis, then each model was refitted once on all 2330 leaves. They were applied to the direct UAV reflectance, which was their best input on the 48 plot-mean spectra. Ground truth is the plot Disease Index from the leaf ratings of 24 February: 12 healthy plots, 25 High and 11 Very high. Likely question: why not the 70:30 or 80:20 models? Because the final application model uses all the training data; the hold-out designs were used only to check the evaluation.');

// ======================= 4 From pixels to plot values
s = pres.addSlide({ masterName: 'CONTENT', sectionTitle: 'Data and method' });
s.addText('From pixel classes to plot values', { placeholder: 'title' });
const flow = ['Pixel class on the model map', 'Count the crop pixels of each class inside each plot ROI', 'Plot value: share of diseased pixels, or DI from the pixel grades', 'Compare with the plot DI from the leaf ratings'];
flow.forEach((t, i) => {
  const x = M + i * 3.13;
  card(s, x, 1.45, 2.75, 1.25, i === 2 ? C.text2 : C.background2, 'flow step ' + (i + 1));
  txt(s, t, { x: x + 0.15, y: 1.5, w: 2.45, h: 1.15, fontSize: 14, align: 'center', valign: 'middle', bold: i === 2, color: i === 2 ? C.background1 : C.text1, objectName: 'flow text ' + (i + 1) });
  if (i < 3) s.addShape(pres.shapes.CHEVRON, { x: x + 2.84, y: 1.88, w: 0.2, h: 0.4, fill: { color: C.accent1 }, line: { color: C.accent1 }, objectName: 'flow arrow ' + (i + 1) });
});
txt(s, [{ text: 'DI = Σ(x · f) / (n · Σf) × 100', options: { bold: true, color: C.text2, breakLine: true } }, { text: 'x = pixel grade, f = number of pixels at grade x, n = 9 – the same formula as the leaf DI', options: { fontSize: 14 } }],
  { x: M, y: 2.95, w: CW, h: 0.75, fontSize: 18, objectName: 'DI formula' });
s.addTable([
  [TH('Model map'), TH('Pixel class'), TH('Plot value'), TH('Plot called diseased if')],
  [TD('Detection', { bold: true }), TD('healthy or diseased'), TD('share of diseased pixels (%)'), TD('share > 50%')],
  [TD('Six grades', { bold: true }), TD('grade 0, 1, 3, 5, 7, 9'), TD('plot DI and DI class'), TD('> 50% of pixels above grade 0')],
  [TD('Severity score', { bold: true }), TD('score put in the nearest grade'), TD('plot DI and DI class'), TD('> 50% of pixels above grade 0')],
], { x: M, y: 3.85, w: CW, colW: [2.4, 3.1, 3.1, 3.533], fontSize: 14, rowH: 0.42, border: { type: 'solid', pt: 0.5, color: 'C9D1CB' }, objectName: 'rules table' });
const cls = [['Healthy', '0', H.accent2], ['Very low', '≤ 5', '91CF60'], ['Low', '≤ 10', 'FEE08B'], ['Moderate', '≤ 25', 'FDAE61'], ['High', '≤ 50', 'E86A3A'], ['Very high', '> 50', 'A50026']];
txt(s, 'DI classes', { x: M, y: 5.75, w: 1.5, h: 0.6, fontSize: 14, bold: true, color: C.text2, valign: 'middle', objectName: 'DI classes label' });
cls.forEach((c, i) => {
  const x = M + 1.55 + i * 1.75;
  s.addShape(pres.shapes.ROUNDED_RECTANGLE, { x, y: 5.75, w: 1.6, h: 0.6, rectRadius: 0.08, fill: { color: c[2] }, line: { color: c[2] }, objectName: 'class box ' + c[0] });
  txt(s, `${c[0]}  ${c[1]}`, { x, y: 5.75, w: 1.6, h: 0.6, fontSize: 14, bold: true, align: 'center', valign: 'middle', color: i >= 4 || i === 0 ? C.background1 : C.text1, objectName: 'class text ' + c[0] });
});
s.addNotes('Every model map is turned into plot values the same way. The crop pixels inside each plot ROI are counted by class. For the grade map the plot DI is computed with exactly the leaf formula, with f now the number of pixels at each grade. The score map is first put in the nearest grade. For plot status every model uses one rule, more than half of the pixels diseased, so the three models are compared alike. A plot is Healthy only if its DI is exactly 0, which a pixel map almost never gives.');

// ======================= 5 Statistics used
s = pres.addSlide({ masterName: 'CONTENT', sectionTitle: 'Data and method' });
s.addText('Statistics used', { placeholder: 'title' });
const st = [
  ['1', 'Healthy vs diseased plots', 'Overall accuracy, sensitivity, specificity, balanced accuracy, Cohen\'s kappa, AUC of the plot value', 'Congalton (1991); Cohen (1960); Hanley and McNeil (1982)', C.accent3],
  ['2', 'Plot DI agreement', 'R², RMSE, MAE, bias, Pearson r, Spearman ρ, Lin\'s CCC; ρ on the 36 diseased plots', 'Lin (1989)', C.accent1],
  ['3', 'DI class agreement', 'Exact agreement, within one class, quadratic weighted kappa (6 classes)', 'Cohen (1968)', C.accent4],
  ['4', 'Uncertainty and model comparison', '95% bootstrap intervals (2000 resamples within healthy / diseased); McNemar exact test; Wilcoxon signed-rank test', 'Efron and Tibshirani (1993); McNemar (1947); Foody (2004); Wilcoxon (1945)', C.text2],
];
st.forEach((q, i) => {
  const x = M + (i % 2) * 6.2, y = 1.45 + Math.floor(i / 2) * 2.7;
  card(s, x, y, 5.93, 2.45, C.background2, 'statistics card ' + q[0]);
  badge(s, x + 0.3, y + 0.3, q[0], q[4], 'statistics badge ' + q[0]);
  txt(s, q[1], { x: x + 1.0, y: y + 0.3, w: 4.7, h: 0.5, fontSize: 18, bold: true, color: C.text2, valign: 'middle', objectName: 'statistics title ' + q[0] });
  txt(s, q[2], { x: x + 0.3, y: y + 0.95, w: 5.35, h: 0.95, fontSize: 14, objectName: 'statistics text ' + q[0] });
  txt(s, q[3], { x: x + 0.3, y: y + 1.9, w: 5.35, h: 0.4, fontSize: 12, italic: true, color: C.accent6, objectName: 'statistics refs ' + q[0] });
});
s.addNotes('Only a small set of statistics. For plot status: the usual confusion-matrix measures plus kappa and AUC; AUC does not depend on the 50% rule. For plot DI: R² and RMSE for accuracy, bias for systematic error, Pearson and Spearman for association, and Lin\'s concordance, which combines both. For the six DI classes: exact agreement, within one class and weighted kappa. Bootstrap intervals resample plots within healthy and diseased; McNemar compares plot-status accuracy between models; Wilcoxon compares their DI errors.');

// ======================= 6 Share of diseased pixels
pres.addSection({ title: 'Results' });
s = pres.addSlide({ masterName: 'CONTENT', sectionTitle: 'Results' });
s.addText('Healthy plots also get mostly diseased pixels', { placeholder: 'title' });
const P = D.plots.det, labels = P.plot.map(String);
const hv = P.share.map((v, i) => (P.status[i] === 0 ? v : 0)), dv = P.share.map((v, i) => (P.status[i] === 1 ? v : 0));
s.addChart([
  { type: pres.charts.BAR, data: [{ name: 'Healthy plot (ground truth)', labels, values: hv }, { name: 'Diseased plot (ground truth)', labels, values: dv }], options: { barGrouping: 'stacked', chartColors: [H.accent2, H.accent3], barGapWidthPct: 35 } },
  { type: pres.charts.LINE, data: [{ name: 'Plot rule: 50%', labels, values: labels.map(() => 50) }], options: { chartColors: [H.dk1], lineSize: 1.5, lineDash: 'dash', lineDataSymbol: 'none' } },
], Object.assign(axisStyle(), { x: M, y: 1.35, w: 8.3, h: 5.4, showTitle: true, title: 'RF detection – diseased pixels in each plot (%)', valAxisMinVal: 0, valAxisMaxVal: 100, valAxisMajorUnit: 20,
  catAxisLabelFontSize: 9, showLegend: true, legendPos: 'b', catAxisTitle: 'plot', showCatAxisTitle: true, objectName: 'share chart' }));
const ss = (k) => D.plots[k].summary;
txt(s, 'Diseased pixels per plot', { x: 9.25, y: 1.45, w: 3.5, h: 0.4, fontSize: 18, bold: true, color: C.text2, objectName: 'share heading' });
s.addTable([
  [TH('Model'), TH('Healthy plots'), TH('Diseased plots')],
  [TD('Detection', { bold: true }), TD(`${ss('det').share_h[0].toFixed(0)}–${ss('det').share_h[1].toFixed(0)}%`), TD(`${ss('det').share_d[0].toFixed(0)}–${ss('det').share_d[1].toFixed(0)}%`)],
  [TD('Six grades', { bold: true }), TD(`${ss('grd').share_h[0].toFixed(0)}–${ss('grd').share_h[1].toFixed(0)}%`), TD(`${ss('grd').share_d[0].toFixed(0)}–${ss('grd').share_d[1].toFixed(0)}%`)],
  [TD('Severity score', { bold: true }), TD('≈ 100%'), TD('≈ 100%')],
], { x: 9.25, y: 1.95, w: 3.5, colW: [1.3, 1.1, 1.1], fontSize: 13, rowH: 0.45, border: { type: 'solid', pt: 0.5, color: 'C9D1CB' }, objectName: 'share table' });
txt(s, [
  { text: `Mean pixel probability: ${ss('det').mv_h.toFixed(2)} in healthy and ${ss('det').mv_d.toFixed(2)} in diseased plots – most pixels sit just above the 0.5 cut-off.`, options: { breakLine: true } },
  { text: ' ', options: { breakLine: true, fontSize: 8 } },
  { text: 'So every plot passes the 50% rule, although healthy plots are on average a little lower.', options: { bold: true, color: C.text2 } },
], { x: 9.25, y: 4.1, w: 3.5, h: 2.5, fontSize: 14, objectName: 'share commentary' });
s.addNotes('Each bar is one plot; green bars are the 12 healthy plots of the ground truth, red bars the 36 diseased plots. Even healthy plots have 63 to 81 percent diseased pixels in the detection map, so all bars cross the 50% line. The pixel probabilities cluster just above 0.5 (mean 0.61 in healthy and 0.63 in diseased plots). The grade map gives 45 to 70 percent pixels above grade 0; the score map practically 100 percent because almost no pixel score is below 0.5.');

// ======================= 7 Healthy vs diseased table
s = pres.addSlide({ masterName: 'CONTENT', sectionTitle: 'Results' });
s.addText('Plot status: almost every plot is called diseased', { placeholder: 'title' });
const rowsBin = [['TP / FN / FP / TN', (k) => `${met(k, 'TP')} / ${met(k, 'FN')} / ${met(k, 'FP')} / ${met(k, 'TN')}`],
  ['Overall accuracy', (k) => fx(met(k, 'Overall accuracy (healthy/diseased)'), 3)], ['Sensitivity', (k) => fx(met(k, 'Sensitivity'))], ['Specificity', (k) => fx(met(k, 'Specificity'))],
  ['Balanced accuracy', (k) => fx(met(k, 'Balanced accuracy'))], ["Cohen's kappa", (k) => fx(met(k, "Cohen's kappa"))]];
const tb = [[TH('Statistic'), TH('RF detection'), TH('RF six grades'), TH('RF severity score')]];
rowsBin.forEach((r, i) => tb.push([TD(r[0], { align: 'left', bold: true, fill: { color: i % 2 ? C.background1 : C.background2 } })].concat(M3.map((k) => TD(r[1](k), { fill: { color: i % 2 ? C.background1 : C.background2 } })))));
s.addTable(tb, { x: M, y: 1.45, w: 7.9, colW: [2.5, 1.8, 1.8, 1.8], fontSize: 15, rowH: 0.55, border: { type: 'solid', pt: 0.5, color: 'C9D1CB' }, objectName: 'status table' });
card(s, 8.85, 1.45, 3.88, 2.45, C.background2, 'accuracy card');
txt(s, '0.75', { x: 9.15, y: 1.6, w: 3.3, h: 0.9, fontSize: 48, bold: true, color: C.accent3, fontFace: THEME.headFontFace, valign: 'middle', objectName: 'accuracy number' });
txt(s, 'Overall accuracy equals the share of diseased plots (36 of 48): a map that calls everything diseased scores the same.', { x: 9.15, y: 2.55, w: 3.3, h: 1.25, fontSize: 14, objectName: 'accuracy text' });
card(s, 8.85, 4.15, 3.88, 2.15, C.text2, 'kappa card');
txt(s, 'Balanced accuracy 0.50–0.54 and kappa 0–0.12: no better than chance with the 50% rule. Only the grade map got one healthy plot right (plot 6).', { x: 9.15, y: 4.3, w: 3.3, h: 1.85, fontSize: 14, color: C.background1, valign: 'middle', objectName: 'kappa text' });
txt(s, 'Plot called diseased when more than 50% of its crop pixels are diseased (pixel grade > 0 for the grade and score maps).', { x: M, y: 5.5, w: 7.9, h: 0.6, fontSize: 12, color: C.accent6, objectName: 'status note' });
s.addNotes('All 36 diseased plots are found (sensitivity 1.00), but 11 or 12 of the 12 healthy plots are also called diseased. Overall accuracy 0.75 looks reasonable but is exactly the prevalence of diseased plots, which is why balanced accuracy and kappa are reported: 0.50 and 0 for detection and score, 0.54 and 0.12 for grades. McNemar on the next slides confirms the three maps do not differ in plot status.');

// ======================= 8 AUC
s = pres.addSlide({ masterName: 'CONTENT', sectionTitle: 'Results' });
s.addText('Plot values still rank healthy below diseased', { placeholder: 'title' });
const aucL = M3.map((k) => NAME[k]);
s.addChart([
  { type: pres.charts.BAR, data: [{ name: 'AUC', labels: aucL, values: M3.map((k) => +met(k, 'AUC').toFixed(3)) }], options: { chartColors: [H.accent1], barGapWidthPct: 70, showValue: true, dataLabelPosition: 'outEnd', dataLabelFormatCode: '0.00', dataLabelColor: H.dk1, dataLabelFontFace: '+mn-lt', dataLabelFontSize: 14 } },
  { type: pres.charts.LINE, data: [{ name: 'Chance (0.5)', labels: aucL, values: [0.5, 0.5, 0.5] }], options: { chartColors: [H.dk1], lineSize: 1.5, lineDash: 'dash', lineDataSymbol: 'none' } },
], Object.assign(axisStyle(), { x: M, y: 1.35, w: 6.4, h: 5.3, showTitle: true, title: 'AUC – plot value against plot status', valAxisMinVal: 0, valAxisMaxVal: 1, valAxisMajorUnit: 0.25, valAxisLabelFormatCode: '0.00',
  catAxisLabelFontSize: 13, showLegend: true, legendPos: 'b', objectName: 'AUC chart' }));
const at = [[TH('Model'), TH('AUC'), TH('95% interval')]];
M3.forEach((k, i) => { const b = boot(k, 'AUC'); at.push([TD(NAME[k], { bold: true, align: 'left' }), TD(fx(b[0])), TD(`${fx(b[1])} – ${fx(b[2])}`)]); });
s.addTable(at, { x: 7.4, y: 1.45, w: 5.33, colW: [2.33, 1.2, 1.8], fontSize: 15, rowH: 0.5, border: { type: 'solid', pt: 0.5, color: 'C9D1CB' }, objectName: 'AUC table' });
txt(s, [
  { text: 'All three lower limits are above 0.5: the plot values carry a weak but real presence signal.', options: { breakLine: true } },
  { text: ' ', options: { breakLine: true, fontSize: 8 } },
  { text: 'The ranking is not the problem – the cut-off is. A threshold set on UAV plots, not on leaves, could use this signal (to be tested with leave-one-plot-out).', options: { color: C.text2, bold: true } },
], { x: 7.4, y: 3.75, w: 5.33, h: 2.6, fontSize: 15, objectName: 'AUC commentary' });
s.addNotes('AUC does not use the 50% rule: it is the probability that a randomly chosen diseased plot has a higher plot value than a randomly chosen healthy plot. All three are 0.73, with bootstrap intervals from about 0.56 to 0.86, so above chance. The signal is weak, but it means a UAV-specific cut-off could separate part of the healthy plots. To estimate that honestly the cut-off must be chosen without the plot being tested, for example leave-one-plot-out.');

// ======================= 9 DI scatter
s = pres.addSlide({ masterName: 'CONTENT', sectionTitle: 'Results' });
s.addText('Mapped plot DI does not follow the field DI', { placeholder: 'title' });
['grd', 'scr'].forEach((k, j) => {
  const Q = D.plots[k], x0 = M + j * 6.2;
  const yH = Q.pred_DI.map((v, i) => (Q.status[i] === 0 ? v : null)), yD = Q.pred_DI.map((v, i) => (Q.status[i] === 1 ? v : null));
  s.addChart(pres.charts.SCATTER, [{ name: 'Observed DI', values: Q.obs_DI }, { name: 'Healthy plots', values: yH }, { name: 'Diseased plots', values: yD }],
    Object.assign(axisStyle(), { x: x0, y: 1.35, w: 5.93, h: 4.15, showTitle: true, title: NAME[k] + ' – plot DI (%)', chartColors: [H.accent2, H.accent3], lineSize: 0, lineDataSymbolSize: 7,
      valAxisMinVal: 0, valAxisMaxVal: 100, valAxisMajorUnit: 20, catAxisMinVal: 0, catAxisMaxVal: 100, catAxisMajorUnit: 20, showValAxisTitle: true, valAxisTitle: 'mapped DI (%)', showCatAxisTitle: true, catAxisTitle: 'observed DI (%)',
      showLegend: true, legendPos: 'b', objectName: 'DI scatter ' + k }));
  const sm = Q.summary;
  txt(s, [
    { text: `R² ${fx(met(k, 'R² (DI)'))} · RMSE ${fx(met(k, 'RMSE (DI, %)'), 1)} · bias +${fx(met(k, 'Bias (DI, %)'), 1)} · CCC ${fx(met(k, "Lin's CCC (DI)"))}`, options: { bold: true, color: C.text2, breakLine: true } },
    { text: `Healthy plots mapped at DI ${sm.di_h[0].toFixed(0)}–${sm.di_h[1].toFixed(0)}; diseased plots ${sm.di_d[0].toFixed(0)}–${sm.di_d[1].toFixed(0)} (field 27–67).` },
  ], { x: x0 + 0.1, y: 5.6, w: 5.73, h: 1.05, fontSize: 14, objectName: 'DI stats ' + k });
});
s.addNotes('Each point is a plot: observed DI on the x axis, DI from the pixel classes on the y axis. Healthy plots (green, observed 0) are mapped at DI 36 to 55, which is the main source of the large positive bias. Diseased plots lie in a horizontal band: the mapped DI hardly changes with the field DI. R² is negative for both models, meaning the plot mean would predict better, and Lin\'s concordance is below 0.1. The score model has the smaller RMSE because it predicts a narrow mid-range band for all plots.');

// ======================= 10 Severity ranking
s = pres.addSlide({ masterName: 'CONTENT', sectionTitle: 'Results' });
s.addText('No severity ranking within the diseased plots', { placeholder: 'title' });
const rkL = M3.map((k) => NAME[k]);
s.addChart(pres.charts.BAR, [{ name: 'Spearman ρ, 36 diseased plots', labels: rkL, values: M3.map((k) => +met(k, 'Spearman ρ, diseased plots').toFixed(3)) }],
  Object.assign(axisStyle(), { x: M, y: 1.35, w: 6.4, h: 5.3, showTitle: true, title: 'Spearman ρ – plot value vs field DI, diseased plots', chartColors: [H.accent4], barGapWidthPct: 70, valAxisMinVal: -1, valAxisMaxVal: 1, valAxisMajorUnit: 0.5,
    valAxisLabelFormatCode: '0.0', showValue: true, dataLabelPosition: 'outEnd', dataLabelFormatCode: '0.00', dataLabelColor: H.dk1, dataLabelFontFace: '+mn-lt', dataLabelFontSize: 14, catAxisLabelFontSize: 13, showLegend: false, objectName: 'rho chart' }));
const rt = [[TH('Model'), TH('ρ, diseased plots (95% interval)'), TH('r, all 48 plots')]];
M3.forEach((k) => { const b = boot(k, 'Spearman ρ, diseased plots'); rt.push([TD(NAME[k], { bold: true, align: 'left' }), TD(`${fx(b[0])} (${fx(b[1])} to ${fx(b[2])})`), TD(k === 'det' ? '–' : `${fx(met(k, 'Pearson r (DI)'))} (p ${fx(met(k, 'p (r)'), 3)})`)]); });
s.addTable(rt, { x: 7.4, y: 1.45, w: 5.33, colW: [1.85, 2.03, 1.45], fontSize: 14, rowH: 0.55, border: { type: 'solid', pt: 0.5, color: 'C9D1CB' }, objectName: 'rho table' });
txt(s, [
  { text: 'All intervals include 0: where disease is present the maps do not tell mild from severe plots.', options: { breakLine: true } },
  { text: ' ', options: { breakLine: true, fontSize: 8 } },
  { text: 'The r of 0.31 over all 48 plots (grades, p 0.035) comes only from healthy plots being slightly lower – it is a presence effect, not severity.', options: { color: C.text2, bold: true } },
], { x: 7.4, y: 3.85, w: 5.33, h: 2.6, fontSize: 15, objectName: 'rho commentary' });
s.addNotes('Severity is judged where disease is present, so the correlation is repeated on the 36 diseased plots. Spearman rho is minus 0.13 to plus 0.15, and every bootstrap interval includes zero. The significant Pearson r of 0.31 for the grade model over all plots is driven by the twelve healthy plots having slightly lower DI; it disappears inside the diseased plots. Likely question: is the field DI range wide enough to test severity? It runs from 27 to 67, so yes, a moderate range.');

// ======================= 11 DI class
s = pres.addSlide({ masterName: 'CONTENT', sectionTitle: 'Results' });
s.addText('DI classes: almost every plot is High or Very high', { placeholder: 'title' });
const CN = ['Healthy', 'Very low', 'Low', 'Moderate', 'High', 'Very high'];
const shade = (v, mx) => { if (!v) return 'FFFFFF'; const t = 0.25 + 0.75 * v / mx; const a = [0xEE, 0xF3, 0xEF], b = [0x1F, 0x4D, 0x3A]; return a.map((c, i) => Math.round(c + (b[i] - c) * t).toString(16).padStart(2, '0')).join('').toUpperCase(); };
['grd', 'scr'].forEach((k, j) => {
  const cm = D.plots[k].cm, mx = Math.max(...cm.flat()), x0 = M + j * 6.2;
  txt(s, NAME[k] + ' – plots, observed (rows) × mapped (columns)', { x: x0, y: 1.4, w: 5.93, h: 0.4, fontSize: 15, bold: true, color: C.text2, objectName: 'cm heading ' + k });
  const rows = [[TH('')].concat(CN.map((c) => TH(c)))];
  cm.forEach((r, i) => rows.push([TD(CN[i], { bold: true, align: 'left', fill: { color: C.background2 } })].concat(r.map((v) => TD(v ? String(v) : '', { fill: { color: shade(v, mx) }, color: v / mx > 0.45 ? 'FFFFFF' : H.dk1, bold: v > 0 })))));
  s.addTable(rows, { x: x0, y: 1.85, w: 5.93, colW: [0.93, 0.8, 0.8, 0.8, 1.0, 0.8, 0.8], fontSize: 11, rowH: 0.36, border: { type: 'solid', pt: 0.5, color: 'C9D1CB' }, objectName: 'cm table ' + k });
  card(s, x0, 4.6, 5.93, 1.55, C.background2, 'class card ' + k);
  txt(s, [
    { text: `Exact ${fx(met(k, 'DI-class accuracy (6 classes)'))} · within one class ${fx(met(k, 'Within one DI class'))} · weighted kappa ${fx(met(k, 'Quadratic weighted kappa (DI class)'))}`, options: { bold: true, color: C.text2, breakLine: true } },
    { text: k === 'grd' ? 'Healthy plots are mapped High or Very high; Very high is over-used (27 plots mapped, 11 observed).' : 'Exact 0.50 is not skill: 47 of 48 plots are mapped High and 25 plots are High – the same as always guessing High.' },
  ], { x: x0 + 0.3, y: 4.72, w: 5.33, h: 1.3, fontSize: 14, objectName: 'class text ' + k });
});
s.addNotes('The six-class tables show where the plots go. No plot is mapped Healthy, because a pixel map almost never gives a DI of exactly 0; the healthy row therefore lands in High or Very high. The score model maps 47 of 48 plots as High, so its exact agreement of 0.50 equals the share of High plots, and weighted kappa is 0.01. The grade model spreads plots over High and Very high but not in line with the field classes (weighted kappa 0.05).');

// ======================= 12 Plot maps
s = pres.addSlide({ masterName: 'CONTENT', sectionTitle: 'Results' });
s.addText('Plot maps: ground truth and the three models', { placeholder: 'title' });
s.addImage({ path: FIG6, x: M, y: 1.4, w: CW, h: CW * 877 / 3555, altText: 'Four maps of the 48 plots: observed DI class, RF detection plot status, RF six grades DI class and RF severity score DI class', objectName: 'plot maps' });
const obs = [['Ground truth', '12 healthy plots in the south-west block; High and Very high elsewhere.'], ['Detection', 'All 48 plots mapped diseased.'], ['Grades and score', 'Classes vary from plot to plot but do not follow the field pattern; score maps nearly all High.']];
obs.forEach((o, i) => {
  const x = M + i * 4.1;
  card(s, x, 4.85, 3.85, 1.75, C.background2, 'map card ' + (i + 1));
  txt(s, o[0], { x: x + 0.25, y: 4.98, w: 3.35, h: 0.4, fontSize: 16, bold: true, color: C.text2, objectName: 'map card title ' + (i + 1) });
  txt(s, o[1], { x: x + 0.25, y: 5.42, w: 3.35, h: 1.05, fontSize: 14, objectName: 'map card text ' + (i + 1) });
});
s.addNotes('The same results as maps of the field. The ground truth shows the 12 healthy (unsprayed control) plots together in one block. The detection map turns every plot red. The grade map alternates High and Very high without matching the field, and the score map is almost uniformly High.');

// ======================= 13 Comparison tests
pres.addSection({ title: 'Comparison and conclusions' });
s = pres.addSlide({ masterName: 'CONTENT', sectionTitle: 'Comparison and conclusions' });
s.addText('Do the three models differ?', { placeholder: 'title' });
txt(s, 'Plot status – McNemar exact test', { x: M, y: 1.4, w: 6.0, h: 0.4, fontSize: 18, bold: true, color: C.text2, objectName: 'mcnemar heading' });
const mt = [[TH('Model A'), TH('Model B'), TH('A right, B wrong'), TH('A wrong, B right'), TH('p')]];
D.mcnemar.forEach((r) => mt.push([TD(r.model_A, { align: 'left' }), TD(r.model_B, { align: 'left' }), TD(String(r.A_right_B_wrong)), TD(String(r.A_wrong_B_right)), TD(fx(r.p_exact, 2))]));
s.addTable(mt, { x: M, y: 1.9, w: 6.0, colW: [1.65, 1.65, 1.0, 1.0, 0.7], fontSize: 13, rowH: 0.5, border: { type: 'solid', pt: 0.5, color: 'C9D1CB' }, objectName: 'mcnemar table' });
txt(s, 'Plot DI – Wilcoxon signed-rank test on |DI error|', { x: 6.85, y: 1.4, w: 5.88, h: 0.4, fontSize: 18, bold: true, color: C.text2, objectName: 'wilcoxon heading' });
const wr = D.wilcoxon[0];
s.addTable([[TH('Model'), TH('Median |DI error|')], [TD(wr.model_A, { align: 'left' }), TD(fx(wr.median_abs_error_A, 1))], [TD(wr.model_B, { align: 'left' }), TD(fx(wr.median_abs_error_B, 1))], [TD('p (Wilcoxon)', { bold: true, align: 'left' }), TD(fx(wr.p_wilcoxon, 3), { bold: true })]],
  { x: 6.85, y: 1.9, w: 5.88, colW: [3.5, 2.38], fontSize: 13, rowH: 0.5, border: { type: 'solid', pt: 0.5, color: 'C9D1CB' }, objectName: 'wilcoxon table' });
card(s, M, 4.6, 6.0, 1.95, C.background2, 'mcnemar card');
txt(s, 'No difference in plot status (all p = 1.00): the three maps disagree on at most one plot, because all call almost everything diseased.', { x: M + 0.3, y: 4.75, w: 5.4, h: 1.65, fontSize: 15, valign: 'middle', objectName: 'mcnemar text' });
card(s, 6.85, 4.6, 5.88, 1.95, C.text2, 'wilcoxon card');
txt(s, 'The score model has a smaller DI error than the grade model (p 0.003) – mainly because it predicts a narrow mid-range DI for every plot, not because it measures severity.', { x: 7.15, y: 4.75, w: 5.28, h: 1.65, fontSize: 15, color: C.background1, valign: 'middle', objectName: 'wilcoxon text' });
s.addNotes('McNemar compares the plot-status errors of two models on the same plots; with at most one discordant plot no difference can be shown. Wilcoxon compares the absolute DI errors plot by plot: the score model is closer to the field DI, but only because its predictions sit in a narrow band near the middle of the field range. Being less wrong is not the same as being informative, as the severity slide showed.');

// ======================= 14 Conclusions
s = pres.addSlide({ masterName: 'CLOSING_DARK', sectionTitle: 'Comparison and conclusions' });
s.addText('Conclusions and next steps', { placeholder: 'title' });
const cc = [
  ['1', 'Leaf models over-call disease on UAV pixels', 'Possible reasons: canopy pixels mix leaves, flowers, soil and shadow; illumination and sensor differ from the ASD leaf clip.'],
  ['2', 'A weak presence signal remains (AUC 0.73)', 'Test a UAV-calibrated plot cut-off with leave-one-plot-out validation.'],
  ['3', 'Severity does not transfer from leaf to plot', 'Train or calibrate at canopy level with the plot DI as target (UAV plot spectra, 2026-27 season).'],
  ['4', 'Confirm at full resolution', `Rerun the three maps with SPATIAL_STEP 1 (current maps: step ${D.info.step}) and repeat this evaluation.`],
];
cc.forEach((q, i) => {
  const x = M + (i % 2) * 6.2, y = 1.75 + Math.floor(i / 2) * 2.55;
  badge(s, x, y + 0.05, q[0], C.accent1, 'conclusion badge ' + q[0]);
  txt(s, q[1], { x: x + 0.75, y, w: 5.1, h: 0.6, fontSize: 18, bold: true, color: C.background1, valign: 'middle', objectName: 'conclusion title ' + q[0] });
  txt(s, q[2], { x: x + 0.75, y: y + 0.7, w: 5.1, h: 1.4, fontSize: 15, color: C.background2, objectName: 'conclusion text ' + q[0] });
});
s.addNotes('Four conclusions. The leaf-trained models over-call disease on canopy pixels; mixed pixels, soil and shadow, illumination and sensor differences are possible reasons, which this analysis does not separate. A weak presence signal remains and should be tested with a cut-off calibrated on the UAV plots under leave-one-plot-out validation. Severity does not transfer from leaf to plot, so the next season should train or calibrate at canopy level with plot DI as the target. Finally, the numbers must be confirmed with full-resolution maps.');

// ======================= 15 References
s = pres.addSlide({ masterName: 'CONTENT', sectionTitle: 'Comparison and conclusions' });
s.addText('References', { placeholder: 'title' });
const refs = [
  'Breiman, L. (2001). Random forests. Machine Learning 45, 5–32.',
  'Cohen, J. (1960). A coefficient of agreement for nominal scales. Educational and Psychological Measurement 20, 37–46.',
  'Cohen, J. (1968). Weighted kappa: nominal scale agreement with provision for scaled disagreement or partial credit. Psychological Bulletin 70, 213–220.',
  'Congalton, R.G. (1991). A review of assessing the accuracy of classifications of remotely sensed data. Remote Sensing of Environment 37, 35–46.',
  'Efron, B., Tibshirani, R.J. (1993). An Introduction to the Bootstrap. Chapman and Hall, New York.',
  'Foody, G.M. (2004). Thematic map comparison: evaluating the statistical significance of differences in classification accuracy. Photogrammetric Engineering and Remote Sensing 70, 627–633.',
  'Hanley, J.A., McNeil, B.J. (1982). The meaning and use of the area under a receiver operating characteristic (ROC) curve. Radiology 143, 29–36.',
  'Lin, L.I. (1989). A concordance correlation coefficient to evaluate reproducibility. Biometrics 45, 255–268.',
  'McKinney, H.H. (1923). Influence of soil temperature and moisture on infection of wheat seedlings by Helminthosporium sativum. Journal of Agricultural Research 26, 195–218.',
  'McNemar, Q. (1947). Note on the sampling error of the difference between correlated proportions or percentages. Psychometrika 12, 153–157.',
  'Wilcoxon, F. (1945). Individual comparisons by ranking methods. Biometrics Bulletin 1, 80–83.',
];
[refs.slice(0, 6), refs.slice(6)].forEach((col, j) => txt(s, col.map((r, i) => ({ text: r, options: { breakLine: i < col.length - 1, paraSpaceAfter: 8 } })), { x: M + j * 6.2, y: 1.45, w: 5.93, h: 5.2, fontSize: 12, objectName: 'references ' + (j + 1) }));
s.addNotes('Sources of the methods used. McKinney (1923) is the origin of the disease index formula used for both the leaf ratings and the pixel grades.');

(async () => {
  await pres.writeFile({ fileName: OUT });
  await applyTheme(OUT, THEME);
  console.log('written', OUT);
})();
