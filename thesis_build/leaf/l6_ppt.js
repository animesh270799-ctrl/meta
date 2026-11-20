// Leaf-level ASD analysis deck: methodology (flow charts) + results, native charts.
const pptxgen = require('pptxgenjs');
const path = require('path');
const { applyTheme } = require('/root/.claude/skills/synced/9bf50f97-a337-4b6b-8c8b-ebd229b7e0d3_d565bc3b-4006-4195-b033-a8c25dfdc114/pptx/scripts/apply_theme.js');
const D = require('./data/ppt.json');
const OUT = path.join(__dirname, '../outputs/Leaf_ASD_analysis_presentation.pptx');
const THEME = { name: 'White rust leaf', headFontFace: 'Cambria', bodyFontFace: 'Calibri',
  colors: { dk1: '1F2A2A', lt1: 'FFFFFF', dk2: '00463F', lt2: 'EEF4F2', accent1: '00695C', accent2: 'C98A00', accent3: 'AD1457', accent4: '2E7D32', accent5: '7B1FA2', accent6: 'E53935', hlink: '00695C', folHlink: '4A148C' } };
const HEX = { teal: '00695C', dark: '00463F', mustard: 'C98A00', berry: 'AD1457', green: '2E7D32', grey: '6B7B78', light: 'EEF4F2', text: '1F2A2A' };
const GC = ['2E7D32', '9CCC65', 'FDD835', 'FB8C00', 'E53935', '7B1FA2'];
const G6 = [0, 1, 3, 5, 7, 9];
const pres = new pptxgen(); pres.layout = 'LAYOUT_WIDE'; pres.theme = { headFontFace: THEME.headFontFace, bodyFontFace: THEME.bodyFontFace };
pres.title = 'Leaf-level ASD analysis of white rust in mustard'; pres.author = 'Ph.D. thesis, ICAR-IARI';
const C = pres.SchemeColor;
const FOOT = 'Leaf-level ASD analysis  |  White rust of mustard';
pres.defineSlideMaster({ title: 'TITLE', background: { color: HEX.dark }, objects: [
  { placeholder: { options: { name: 'title', type: 'title', x: 0.8, y: 2.2, w: 11.7, h: 1.6, fontSize: 40, bold: true, color: C.background1, fontFace: 'Cambria', valign: 'bottom' }, text: '' } },
  { placeholder: { options: { name: 'body', type: 'body', x: 0.8, y: 4.0, w: 11.7, h: 1.4, fontSize: 18, color: 'CADFDB', fontFace: 'Calibri', valign: 'top' }, text: '' } }] });
pres.defineSlideMaster({ title: 'SECTION', background: { color: HEX.teal }, objects: [
  { placeholder: { options: { name: 'title', type: 'title', x: 0.8, y: 2.6, w: 11.7, h: 1.2, fontSize: 40, bold: true, color: C.background1, fontFace: 'Cambria' }, text: '' } },
  { placeholder: { options: { name: 'body', type: 'body', x: 0.8, y: 3.9, w: 11.7, h: 1.2, fontSize: 18, color: 'E0F2F1', fontFace: 'Calibri' }, text: '' } }] });
pres.defineSlideMaster({ title: 'CONTENT', background: { color: 'FFFFFF' }, margin: [0.5, 0.5, 0.6, 0.5],
  slideNumber: { x: 12.4, y: 7.05, w: 0.6, h: 0.3, fontSize: 10, color: HEX.grey },
  objects: [
    { placeholder: { options: { name: 'title', type: 'title', x: 0.5, y: 0.3, w: 12.3, h: 0.8, fontSize: 30, bold: true, color: C.text2, fontFace: 'Cambria', valign: 'middle' }, text: '' } },
    { text: { text: FOOT, options: { x: 0.5, y: 7.05, w: 8, h: 0.3, fontSize: 10, color: HEX.grey } } }] });
let sec = '';
const slide = (master, title) => { const s = pres.addSlide({ masterName: master, sectionTitle: sec }); s.addText(title, { placeholder: 'title' }); return s; };
const section = (t, sub) => { sec = t; pres.addSection({ title: t }); const s = pres.addSlide({ masterName: 'SECTION', sectionTitle: t }); s.addText(t, { placeholder: 'title' }); if (sub) s.addText(sub, { placeholder: 'body' }); return s; };
const txt = (s, items, o) => s.addText(items.map((t, i) => ({ text: t, options: { bullet: true, breakLine: i < items.length - 1 } })), Object.assign({ isTextBox: true, fontSize: 15, color: HEX.text, paraSpaceAfter: 6, valign: 'top' }, o));
const card = (s, x, y, w, h, big, small, col, name) => {
  s.addShape(pres.shapes.ROUNDED_RECTANGLE, { x, y, w, h, fill: { color: HEX.light }, line: { color: HEX.light }, rectRadius: 0.12, objectName: name + ' card' });
  s.addText(big, { isTextBox: true, x: x + 0.15, y: y + 0.12, w: w - 0.3, h: h * 0.55, fontSize: 34, bold: true, color: col, fontFace: 'Cambria', valign: 'bottom', margin: 0, objectName: name + ' value' });
  s.addText(small, { isTextBox: true, x: x + 0.15, y: y + h * 0.62, w: w - 0.3, h: h * 0.34, fontSize: 13, color: HEX.text, valign: 'top', margin: 0, objectName: name + ' label' });
};
const AX = { catAxisLabelColor: HEX.grey, valAxisLabelColor: HEX.grey, catAxisLabelFontFace: '+mn-lt', valAxisLabelFontFace: '+mn-lt', catAxisLabelFontSize: 11, valAxisLabelFontSize: 11,
  valGridLine: { color: 'E3E8E7', size: 0.5 }, catGridLine: { style: 'none' }, titleFontFace: '+mn-lt', titleFontSize: 13, titleColor: HEX.text, legendFontFace: '+mn-lt', legendFontSize: 11, dataLabelFontFace: '+mn-lt', dataLabelFontSize: 10 };
const ax = (o) => Object.assign({}, AX, o);
const ref = (s, t) => s.addText(t, { isTextBox: true, x: 0.5, y: 6.6, w: 12.3, h: 0.4, fontSize: 10, italic: true, color: HEX.grey, valign: 'middle', objectName: 'source note' });
const f3 = (v) => Number(v).toFixed(2);

// ---------- 1 title ----------
sec = 'Introduction'; pres.addSection({ title: sec });
let s = pres.addSlide({ masterName: 'TITLE', sectionTitle: sec });
s.addText('Leaf-level hyperspectral analysis of white rust in mustard', { placeholder: 'title' });
s.addText('ASD leaf spectra, 4 dates (Feb–Mar 2026) — six-grade classification and plot PDI regression with the proposed tier methodology', { placeholder: 'body' });
s.addNotes('Leaf-level ASD spectra are the ground truth for the UAV analysis. This deck shows how the proposed methodology (Objective 1 tiers and Objective 2 models) was applied and what it found.');

// ---------- 2 data ----------
s = slide('CONTENT', 'Data and experimental design');
card(s, 0.5, 1.35, 2.85, 1.45, String(D.n_leaves), 'leaf spectra (ASD, 350–2500 nm)', HEX.teal, 'leaves');
card(s, 3.55, 1.35, 2.85, 1.45, '48', 'plots: 12 control + 36 inoculated (R1–R3)', HEX.mustard, 'plots');
card(s, 0.5, 3.0, 2.85, 1.45, '4', 'sampling dates, vegetative to pod formation', HEX.berry, 'dates');
card(s, 3.55, 3.0, 2.85, 1.45, String(D.n_plotdates), 'plot-dates with PDI (0–76%)', HEX.green, 'plotdates');
txt(s, ['Leaf grade 0, 1, 3, 5, 7, 9 (0–9 key; Conn et al., 1990) → classification target', 'Plot PDI = Σ score / (9 n) × 100 (Wheeler, 1969) → regression target', 'Leave-one-replication-out validation; controls split by variety'], { x: 0.5, y: 4.65, w: 5.9, h: 1.8, fontSize: 14 });
s.addChart(pres.charts.BAR, G6.map((g, k) => ({ name: 'Grade ' + g, labels: D.dates.map(d => d.slice(5)), values: D.dates.map(d => D.counts[d][k]) })),
  ax({ x: 6.7, y: 1.35, w: 6.1, h: 5.1, barDir: 'col', barGrouping: 'stacked', chartColors: GC, showLegend: true, legendPos: 'b', showTitle: true, title: 'Leaves per grade and date (month-day)', valAxisTitle: 'Leaves', showValAxisTitle: true, valAxisTitleFontSize: 11 }));
s.addNotes('Grade 0 dominates on 11 February; the disease builds up so that by 13 March grades 5 and 7 are most common. All six grades are well represented overall.');

// ---------- 3 workflow ----------
s = slide('CONTENT', 'Methodology applied to the leaf spectra');
const steps = [['Tier 0', 'Grades, PDI, folds'], ['Pre-processing', 'Splice, SG, 5 nm'], ['Tier 1', '1047 bands + 51 features'], ['Tier 2', 'Scalogram + ReliefF'], ['Tier 3', 'White Rust Index'],
  ['Tier 4', 'ANOVA + Tukey, r'], ['Tier 5', 'VIF + stepwise CDA'], ['Tier 6', 'Boruta DSF pools'], ['Objective 2', 'Nested models'], ['Outputs', 'Bands, WRI, models']];
const bw = 2.15, bh = 1.15, gx = 0.39;
steps.forEach((st, i) => {
  const row = i < 5 ? 0 : 1, col = row === 0 ? i : 9 - i; const x = 0.55 + col * (bw + gx), y = row === 0 ? 1.55 : 3.65;
  const fill = i === 9 ? HEX.mustard : (i >= 8 ? HEX.berry : (i <= 1 ? HEX.dark : HEX.teal));
  s.addShape(pres.shapes.ROUNDED_RECTANGLE, { x, y, w: bw, h: bh, fill: { color: fill }, line: { color: fill }, rectRadius: 0.1, objectName: 'step ' + (i + 1) });
  s.addText([{ text: st[0], options: { bold: true, fontSize: 16, breakLine: true } }, { text: st[1], options: { fontSize: 13 } }], { isTextBox: true, x, y, w: bw, h: bh, align: 'center', valign: 'middle', color: 'FFFFFF', margin: 4, objectName: 'step label ' + (i + 1) });
  if (i < 9) {
    if (i === 4) s.addShape(pres.shapes.LINE, { x: x + bw / 2, y: y + bh, w: 0, h: 3.65 - (y + bh), line: { color: HEX.grey, width: 1.5, endArrowType: 'triangle' }, objectName: 'arrow ' + i });
    else if (row === 0) s.addShape(pres.shapes.LINE, { x: x + bw, y: y + bh / 2, w: gx, h: 0, line: { color: HEX.grey, width: 1.5, endArrowType: 'triangle' }, objectName: 'arrow ' + i });
    else s.addShape(pres.shapes.LINE, { x: x - gx, y: y + bh / 2, w: gx, h: 0, flipH: true, line: { color: HEX.grey, width: 1.5, endArrowType: 'triangle' }, objectName: 'arrow ' + i });
  }
});
txt(s, ['Objective 1 tiers describe which wavelengths and indices respond to white rust (Mahlein et al., 2013; Bhattacharya and Chattopadhyay, 2013)', 'Objective 2 repeats every selection step inside the training replications, so test leaves never influence the model (Ambroise and McLachlan, 2002)'], { x: 0.5, y: 5.1, w: 12.3, h: 1.3, fontSize: 15 });
s.addNotes('Same tier structure as the UAV methodology. Leaf-level classification uses the six leaf grades; regression uses plot PDI from plot-mean spectra.');

// ---------- section: pre-processing ----------
section('Pre-processing and features', 'Tier 0 and Tier 1');
s = slide('CONTENT', 'Pre-processing of the ASD spectra');
const pp = [['1', 'Splice correction at 1000 nm (step ' + D.splice[0] + ' ± ' + D.splice[1] + ') — Hueni and Bialek, 2017'], ['2', '400–2400 nm kept; 1350–1450 and 1800–1950 nm removed — Thenkabail et al., 2004'],
  ['3', 'Savitzky–Golay smoothing, 11 nm, 2nd order — Savitzky and Golay, 1964'], ['4', 'First and second derivatives — Tsai and Philpot, 1998'], ['5', '5 nm bands: 349 × (R, FD, SD) = 1047 band features'], ['6', 'Plot spectrum = mean of the leaves of a plot-date']];
pp.forEach((p, i) => {
  const y = 1.4 + i * 0.85;
  s.addShape(pres.shapes.OVAL, { x: 0.55, y: y + 0.08, w: 0.5, h: 0.5, fill: { color: HEX.teal }, line: { color: HEX.teal }, objectName: 'num ' + p[0] });
  s.addText(p[0], { isTextBox: true, x: 0.55, y: y + 0.08, w: 0.5, h: 0.5, align: 'center', valign: 'middle', fontSize: 14, bold: true, color: 'FFFFFF', margin: 0, objectName: 'num text ' + p[0] });
  s.addText(p[1], { isTextBox: true, x: 1.2, y, w: 4.6, h: 0.7, fontSize: 14, color: HEX.text, valign: 'middle', margin: 0, objectName: 'step text ' + p[0] });
});
s.addChart(pres.charts.LINE, G6.map((g, k) => ({ name: 'Grade ' + g, labels: D.wl10, values: D.spec[String(g)] })),
  ax({ x: 6.1, y: 1.3, w: 6.7, h: 5.2, chartColors: GC, lineSize: 1.5, lineDataSymbol: 'none', showLegend: true, legendPos: 'b', showTitle: true, title: 'Mean leaf reflectance by grade (10 nm; gaps joined)', catAxisLabelFrequency: 20, valAxisTitle: 'Reflectance', showValAxisTitle: true }));
s.addNotes('Diseased leaves reflect more in the visible (chlorosis) and the SWIR (water loss) and less in the NIR plateau; the red edge moves to shorter wavelengths.');

s = slide('CONTENT', 'Tier 1: features extracted from every spectrum');
card(s, 0.5, 1.35, 2.9, 1.5, '1047', 'band features: R, FD, SD at 349 bands', HEX.teal, 'bands');
card(s, 3.6, 1.35, 2.9, 1.5, '39', 'base indices (pigment, structure, water)', HEX.green, 'base');
card(s, 0.5, 3.05, 2.9, 1.5, '9', 'SWIR disease indices (DWSI-2/3/5, NDWI, MSI, NDII, RBI, NDBI)', HEX.berry, 'swir');
card(s, 3.6, 3.05, 2.9, 1.5, '3', 'red-edge parameters: REP, Dr, SDr', HEX.mustard, 'rededge');
txt(s, ['Indices on leaf spectra for classification and on plot-mean spectra for regression (Guo et al., 2021)', 'All SWIR indices use bands outside the removed water regions (Apan et al., 2004; Gao, 1996)'], { x: 0.5, y: 4.8, w: 6.0, h: 1.6, fontSize: 14 });
s.addChart(pres.charts.BAR, [{ name: 'r with PDI', labels: D.swir.map(r => r[0]), values: D.swir.map(r => r[2]) }],
  ax({ x: 6.8, y: 1.3, w: 6.0, h: 5.2, barDir: 'bar', chartColors: [HEX.berry], showValue: true, dataLabelPosition: 'outEnd', dataLabelFormatCode: '0.00', showLegend: false, showTitle: true, title: 'SWIR disease indices: Pearson r with plot PDI', valAxisMinVal: -1, valAxisMaxVal: 1, catAxisLabelPos: 'low' }));
s.addNotes('Most SWIR indices correlate moderately with PDI (|r| ≈ 0.5–0.63): water-related changes accompany white-rust infection.');

// ---------- section: objective 1 ----------
section('Objective 1: characterisation', 'Tiers 2–6 on 2339 leaves and 192 plot-dates');
s = slide('CONTENT', 'Tier 2: correlation scalogram with plot PDI');
s.addChart(pres.charts.LINE, ['R', 'FD', 'SD'].map(t => ({ name: t, labels: D.wl10, values: D.scal[t] })),
  ax({ x: 0.5, y: 1.3, w: 8.1, h: 5.2, chartColors: [HEX.green, '1565C0', HEX.berry], lineSize: 1.25, lineDataSymbol: 'none', showLegend: true, legendPos: 'b', showTitle: true, title: 'Pearson r with PDI (n = 192; 10 nm steps)', catAxisLabelFrequency: 20, valAxisMinVal: -1, valAxisMaxVal: 1 }));
card(s, 8.9, 1.35, 3.9, 1.5, f3(D.t2.max_r.FD[0]), 'max |r|: FD at ' + D.t2.max_r.FD[1] + ' nm (red edge)', HEX.teal, 'maxfd');
card(s, 8.9, 3.05, 3.9, 1.5, f3(D.t2.max_r.R[0]), 'max |r|: reflectance at ' + D.t2.max_r.R[1] + ' nm', HEX.green, 'maxr');
txt(s, [D.t2.n_scal_cand + ' candidates (p < 0.01, top 5%) → ' + D.t2.n_scal_reg + ' after one band per region', 'Method: Shukla et al. (2024)'], { x: 8.9, y: 4.75, w: 3.9, h: 1.7, fontSize: 14 });
s.addNotes('Derivatives in the red edge correlate most strongly with severity, as in Shukla et al. (2024) for mustard aphid stress.');

s = slide('CONTENT', 'Tier 2: ReliefF and the three band lists');
s.addChart(pres.charts.LINE, ['R', 'FD', 'SD'].map(t => ({ name: t, labels: D.wl10, values: D.relief[t] })),
  ax({ x: 0.5, y: 1.3, w: 6.6, h: 5.2, chartColors: [HEX.green, '1565C0', HEX.berry], lineSize: 1.25, lineDataSymbol: 'none', showLegend: true, legendPos: 'b', showTitle: true, title: 'ReliefF weights, six leaf grades (k = 10; 10 nm steps)', catAxisLabelFrequency: 20 }));
const L = Math.max(D.t2.robust.length, D.t2.regonly.length, D.t2.clsonly.length);
const hdr = ['Robust (both)', 'Regression only', 'Classification only'].map(t => ({ text: t, options: { bold: true, color: 'FFFFFF', fill: { color: HEX.teal } } }));
const rows = [hdr]; for (let i = 0; i < L; i++) rows.push([D.t2.robust[i] || '', D.t2.regonly[i] || '', D.t2.clsonly[i] || '']);
s.addTable(rows, { x: 7.4, y: 1.35, w: 5.4, colW: [1.8, 1.8, 1.8], fontSize: 11, fontFace: 'Calibri', color: HEX.text, border: { type: 'solid', pt: 0.5, color: 'D5DEDC' }, rowH: 0.27 });
ref(s, 'One band per correlated region (r ≥ 0.95; ' + D.t2.n_regions.R + ' regions in reflectance); common → robust (Tian et al., 2021; Robnik-Šikonja and Kononenko, 2003).');
s.addNotes('Robust bands are almost all red-edge derivatives (680–860 nm). Derivative bands within 10 nm of the splice or water-band edges were not eligible.');

s = slide('CONTENT', 'Tier 3: White Rust Index');
s.addShape(pres.shapes.ROUNDED_RECTANGLE, { x: 0.5, y: 1.35, w: 6.0, h: 1.9, fill: { color: HEX.light }, line: { color: HEX.light }, rectRadius: 0.12, objectName: 'wri box' });
s.addText([{ text: 'WRI = ' + D.t3.vnir.formula, options: { fontSize: 24, bold: true, color: HEX.teal, fontFace: 'Cambria', breakLine: true } },
  { text: 'Balanced accuracy (8-fold plot-grouped CV) ' + f3(D.t3.vnir.best.ba_cv) + ';  r with PDI ' + f3(D.t3.r_pdi), options: { fontSize: 15, color: HEX.text } }], { isTextBox: true, x: 0.7, y: 1.45, w: 5.6, h: 1.7, valign: 'middle', margin: 0, objectName: 'wri text' });
txt(s, [D.t3.vnir.n_cand.toLocaleString('en') + ' VNIR candidates (ND + w·R, 450–950 nm at 6 nm)', 'SWIR rerun: ' + D.t3.swir.formula + ', balanced accuracy ' + f3(D.t3.swir.best.ba_cv) + ' → VNIR index kept', 'Method: Mahlein et al. (2013)'], { x: 0.5, y: 3.5, w: 6.0, h: 2.9, fontSize: 15 });
s.addChart(pres.charts.BAR, [{ name: 'Mean WRI', labels: G6.map(g => 'Grade ' + g), values: D.wri_means }],
  ax({ x: 6.8, y: 1.3, w: 6.0, h: 5.2, barDir: 'col', chartColors: GC, showValue: true, dataLabelPosition: 'outEnd', dataLabelFormatCode: '0.000', showLegend: false, showTitle: true, title: 'Mean WRI by leaf grade' }));
s.addNotes('The index contrasts the NIR plateau (750 nm) with 948 nm and subtracts red-edge reflectance at 696 nm; it falls steadily with grade.');

s = slide('CONTENT', 'Tier 4: univariate response of the features');
s.addChart(pres.charts.BAR, [{ name: 'ANOVA F', labels: D.anova_top.map(r => r[0]), values: D.anova_top.map(r => r[1]) }],
  ax({ x: 0.5, y: 1.3, w: 6.6, h: 5.2, barDir: 'bar', chartColors: [HEX.teal], showValue: true, dataLabelPosition: 'outEnd', dataLabelFormatCode: '0', showLegend: false, showTitle: true, title: 'Top 12 features by one-way ANOVA F (six grades)', valAxisHidden: true, catAxisOrientation: 'maxMin' }));
const lk = Object.keys(D.letters).slice(0, 6);
const lrows = [[{ text: 'Feature', options: { bold: true, color: 'FFFFFF', fill: { color: HEX.teal } } }].concat(G6.map(g => ({ text: 'G' + g, options: { bold: true, color: 'FFFFFF', fill: { color: HEX.teal }, align: 'center' } })))];
lk.forEach(k => lrows.push([k].concat(G6.map(g => ({ text: D.letters[k][String(g)], options: { align: 'center' } })))));
s.addTable(lrows, { x: 7.4, y: 1.35, w: 5.4, colW: [1.5, 0.65, 0.65, 0.65, 0.65, 0.65, 0.65], fontSize: 12, color: HEX.text, border: { type: 'solid', pt: 0.5, color: 'D5DEDC' }, rowH: 0.34 });
const same01 = lk.filter(k => [...D.letters[k]['0']].some(c => D.letters[k]['1'].includes(c)));
txt(s, ['Tukey HSD letters: grades sharing a letter do not differ (Tukey, 1949)', same01.length ? 'Grades 0 and 1 not separated for ' + same01.join(', ') : 'All grades separated'], { x: 7.4, y: 4.05, w: 5.4, h: 2.4, fontSize: 14 });
s.addNotes('Red-edge first derivatives and the WRI respond most strongly; pigment indices HI and ARI follow.');

s = slide('CONTENT', 'Tier 5: stepwise canonical discriminant analysis');
const c1 = D.t5.step1, c2 = D.t5.step2;
const crow = (l, a, b) => [l, a, b];
const ctab = [[{ text: 'Quantity', options: { bold: true, color: 'FFFFFF', fill: { color: HEX.teal } } }, { text: 'Step 1: bands', options: { bold: true, color: 'FFFFFF', fill: { color: HEX.teal } } }, { text: 'Step 2: indices + WRI', options: { bold: true, color: 'FFFFFF', fill: { color: HEX.teal } } }],
  crow('Variables in → after VIF < 10', c1.n_in + ' → ' + c1.n_vif, c2.n_in + ' → ' + c2.n_vif), crow('Selected (Wilks Λ, p < 0.001)', String(c1.selected.length), String(c2.selected.length)),
  crow('Canonical r, function 1', f3(c1.cancor[0]), f3(c2.cancor[0])), crow('Share of function 1', (100 * c1.share[0]).toFixed(0) + '%', (100 * c2.share[0]).toFixed(0) + '%'),
  crow("Wilks' lambda", c1.wilks.toFixed(3), c2.wilks.toFixed(3)), crow('LORO accuracy (6 grades)', f3(c1.acc), f3(c2.acc)), crow('±1-grade accuracy', f3(c1.adj), f3(c2.adj))];
s.addTable(ctab, { x: 0.5, y: 1.35, w: 6.6, colW: [2.8, 1.9, 1.9], fontSize: 13, color: HEX.text, border: { type: 'solid', pt: 0.5, color: 'D5DEDC' }, rowH: 0.42 });
txt(s, ['Selected (step 2): ' + c2.selected.join(', '), 'Method: Bhattacharya and Chattopadhyay (2013); Klecka (1980)'], { x: 0.5, y: 5.0, w: 6.6, h: 1.4, fontSize: 14 });
const cent = c1.centroids;
s.addChart(pres.charts.SCATTER, [{ name: 'F1', values: cent.map(c => c[0]) }, { name: 'Grade centroids', values: cent.map(c => c[1]), labels: G6.map(g => 'Grade ' + g) }],
  ax({ x: 7.4, y: 1.3, w: 5.4, h: 5.2, chartColors: [HEX.berry], lineSize: 0, lineDataSymbolSize: 12, showLegend: false, showTitle: true, title: 'Step 1 grade centroids (function 1 vs 2)', valAxisTitle: 'Function 2', showValAxisTitle: true, catAxisTitle: 'Function 1: grades 0 → 9 left to right', showCatAxisTitle: true,
    showLabel: true, dataLabelFormatScatter: 'custom', dataLabelPosition: 't' }));
s.addNotes('One severity axis carries almost all separation (function 1 ≈ 88%). Six-grade accuracy is modest because neighbouring grades overlap; about 70% of leaves fall within one grade.');

s = slide('CONTENT', 'Tier 6: Boruta disease-specific feature pools');
const bcol = (r) => r.map(q => q[2] === 'Confirmed' ? HEX.green : (q[2] === 'Tentative' ? 'FBC02D' : 'E53935'));
s.addChart(pres.charts.BAR, [{ name: 'Importance', labels: D.boruta_c.map(r => r[0]), values: D.boruta_c.map(r => r[1]) }],
  ax({ x: 0.5, y: 1.3, w: 6.0, h: 4.9, barDir: 'bar', chartColors: [HEX.green], showLegend: false, showTitle: true, title: 'Classification (six grades): ' + D.t6.cls.confirmed.length + ' confirmed of ' + D.t6.cls.n_in, catAxisOrientation: 'maxMin', valAxisLabelFormatCode: '0.00' }));
s.addChart(pres.charts.BAR, [{ name: 'Importance', labels: D.boruta_r.map(r => r[0]), values: D.boruta_r.map(r => r[1]) }],
  ax({ x: 6.8, y: 1.3, w: 6.0, h: 4.9, barDir: 'bar', chartColors: [HEX.berry], showLegend: false, showTitle: true, title: 'Regression (PDI): ' + D.t6.reg.confirmed.length + ' confirmed of ' + D.t6.reg.n_in, catAxisOrientation: 'maxMin', valAxisLabelFormatCode: '0.00' }));
ref(s, 'Top 12 features by random-forest importance; Boruta with alpha = 0.01, up to 100 runs (Kursa and Rudnicki, 2010; Mustafa et al., 2023).');
s.addNotes('The WRI dominates the regression pool; classification needs many red-edge derivative bands plus pigment indices.');

// ---------- section: objective 2 ----------
section('Objective 2: classification and regression', 'Nested leave-one-replication-out');
s = slide('CONTENT', 'Nested model pipeline inside each training fold');
const p2 = ['Tier 2 band lists', 'Boruta', 'VIF < 10', 'ML-SFFS per model', 'Tuning', 'Test on held-out replication'];
p2.forEach((t, i) => {
  const x = 0.5 + i * 2.1;
  s.addShape(pres.shapes.ROUNDED_RECTANGLE, { x, y: 1.45, w: 1.85, h: 1.0, fill: { color: i === 5 ? HEX.mustard : HEX.berry }, line: { color: i === 5 ? HEX.mustard : HEX.berry }, rectRadius: 0.1, objectName: 'pipe ' + i });
  s.addText(t, { isTextBox: true, x, y: 1.45, w: 1.85, h: 1.0, align: 'center', valign: 'middle', fontSize: 14, bold: true, color: 'FFFFFF', margin: 3, objectName: 'pipe text ' + i });
  if (i < 5) s.addShape(pres.shapes.LINE, { x: x + 1.85, y: 1.95, w: 0.25, h: 0, line: { color: HEX.grey, width: 1.5, endArrowType: 'triangle' }, objectName: 'pipe arrow ' + i });
});
const fh = ['Test rep.', 'Boruta (C / R)', 'VIF (C / R)', 'SVM features (classification)', 'Best regressor features'].map(t => ({ text: t, options: { bold: true, color: 'FFFFFF', fill: { color: HEX.teal } } }));
const frows = [fh].concat(D.folds.map(f => [f.rep, f.boruta_cls + ' / ' + f.boruta_reg, f.vif_cls + ' / ' + f.vif_reg, f.ofc.SVM.join(', '), (f.ofc['R_' + D.best.reg] || f.ofc.R_SVR || []).join(', ')]));
s.addTable(frows, { x: 0.5, y: 2.85, w: 12.3, colW: [1.1, 1.5, 1.3, 4.2, 4.2], fontSize: 12, color: HEX.text, border: { type: 'solid', pt: 0.5, color: 'D5DEDC' }, rowH: 0.45 });
ref(s, 'ML-SFFS with grouped inner CV (Pudil et al., 1994; Tian et al., 2021); selection inside training data avoids optimistic bias (Varma and Simon, 2006).');
s.addNotes('Every selection step is repeated three times, once per training set. The features that recur across folds are the stable white-rust features.');

s = slide('CONTENT', 'Six-grade leaf classification');
const ck = Object.keys(D.cls);
s.addChart(pres.charts.BAR, [{ name: 'Macro-F1', labels: ck, values: ck.map(k => D.cls[k].macro_f1) }, { name: '±1-grade accuracy', labels: ck, values: ck.map(k => D.cls[k].adj) }],
  ax({ x: 0.5, y: 1.3, w: 8.1, h: 5.2, barDir: 'col', chartColors: [HEX.teal, HEX.mustard], showValue: true, dataLabelPosition: 'outEnd', dataLabelFormatCode: '0.00', showLegend: true, legendPos: 'b', showTitle: true, title: 'Held-out performance by model', valAxisMaxVal: 1, valAxisMinVal: 0, catAxisLabelFontSize: 10 }));
const bc = D.cls[D.best.cls];
card(s, 8.9, 1.35, 3.9, 1.5, f3(bc.macro_f1), 'macro-F1, ' + D.best.cls + ' (best)', HEX.teal, 'bestf1');
card(s, 8.9, 3.05, 3.9, 1.5, f3(bc.detection_acc), 'healthy vs diseased accuracy', HEX.green, 'det');
txt(s, ['OA ' + f3(bc.oa) + ', kappa ' + f3(bc.kappa) + ', ±1 grade ' + f3(bc.adj), 'Cortes and Vapnik (1995); Breiman (2001)'], { x: 8.9, y: 4.75, w: 3.9, h: 1.7, fontSize: 14 });
s.addNotes('Exact six-grade accuracy is limited by overlap of neighbouring grades; about three quarters of leaves are placed within one grade, and healthy vs diseased is separated in about 78% of cases.');

s = slide('CONTENT', 'Confusion matrix of the best classifier');
const cm = bc.cm; const mx = Math.max(...cm.flat());
const shade = (v) => { const t = v / mx; const r = Math.round(255 - t * (255 - 0x2E)), g = Math.round(255 - t * (255 - 0x7D)), b = Math.round(255 - t * (255 - 0x32)); return [r, g, b].map(q => q.toString(16).padStart(2, '0')).join('').toUpperCase(); };
const mrows = [[{ text: 'Obs \\ Pred', options: { bold: true, color: 'FFFFFF', fill: { color: HEX.teal } } }].concat(G6.map(g => ({ text: String(g), options: { bold: true, color: 'FFFFFF', fill: { color: HEX.teal }, align: 'center' } })))];
cm.forEach((row, i) => mrows.push([{ text: String(G6[i]), options: { bold: true, color: 'FFFFFF', fill: { color: HEX.teal }, align: 'center' } }].concat(row.map(v => ({ text: String(v), options: { align: 'center', fill: { color: shade(v) }, color: v / mx > 0.55 ? 'FFFFFF' : HEX.text } })))));
s.addTable(mrows, { x: 0.5, y: 1.35, w: 6.6, colW: [1.2, 0.9, 0.9, 0.9, 0.9, 0.9, 0.9], fontSize: 14, border: { type: 'solid', pt: 0.5, color: 'FFFFFF' }, rowH: 0.62 });
s.addChart(pres.charts.BAR, [{ name: 'F1', labels: G6.map(g => 'Grade ' + g), values: bc.F1.map(v => Math.round(v * 100) / 100) }],
  ax({ x: 7.4, y: 1.3, w: 5.4, h: 5.2, barDir: 'col', chartColors: GC, showValue: true, dataLabelPosition: 'outEnd', dataLabelFormatCode: '0.00', showLegend: false, showTitle: true, title: 'F1 per grade', valAxisMaxVal: 1, valAxisMinVal: 0 }));
ref(s, 'Rows: observed grade; columns: predicted grade; held-out replications pooled (Sokolova and Lapalme, 2009).');
s.addNotes('Grade 0 is recognised best; grades 1–5 are confused with their neighbours and grade 9 partly with 5 and 7, which matches the overlap seen in Tier 4.');

s = slide('CONTENT', 'Plot PDI regression');
const rk = Object.keys(D.reg);
s.addChart(pres.charts.BAR, [{ name: 'R²', labels: rk, values: rk.map(k => Math.max(D.reg[k].r2, 0)) }],
  ax({ x: 0.5, y: 1.3, w: 6.4, h: 5.2, barDir: 'bar', chartColors: [HEX.berry], showValue: true, dataLabelPosition: 'outEnd', dataLabelFormatCode: '0.00', showLegend: false, showTitle: true, title: 'Held-out R² by model', valAxisMaxVal: 1, valAxisMinVal: 0, catAxisOrientation: 'maxMin', catAxisLabelFontSize: 10 }));
s.addChart(pres.charts.SCATTER, [{ name: 'Observed', values: D.obs }, { name: D.best.reg, values: D.pred_best }, { name: 'Bottom-up', values: D.pred_bu }],
  ax({ x: 7.1, y: 1.3, w: 5.7, h: 5.2, chartColors: [HEX.berry, HEX.teal], lineSize: 0, lineDataSymbolSize: 5, showLegend: true, legendPos: 'b', showTitle: true, title: 'Observed vs predicted PDI (%)', valAxisTitle: 'Predicted', showValAxisTitle: true, catAxisTitle: 'Observed', showCatAxisTitle: true, valAxisMaxVal: 90, valAxisMinVal: 0 }));
ref(s, 'Best: ' + D.best.reg + ' R² ' + f3(D.reg[D.best.reg].r2) + ', RMSE ' + D.reg[D.best.reg].rmse.toFixed(1) + ', RPD ' + f3(D.reg[D.best.reg].rpd) + '; bottom-up = PDI from predicted leaf grades (Liu et al., 2024; Wold et al., 2001).');
s.addNotes('Plot PDI is predicted better than leaf grades because averaging leaves removes within-plot noise; aggregating leaf-level grade predictions gives a somewhat weaker PDI estimate.');

s = slide('CONTENT', 'Performance by date and variety');
const dk = Object.keys(D.by_date);
s.addChart(pres.charts.BAR, [{ name: 'Macro-F1 (grades)', labels: dk, values: dk.map(d => Math.round(D.by_date[d].macro_f1 * 100) / 100) }, { name: 'R² (PDI)', labels: dk, values: dk.map(d => Math.round((D.by_date[d].r2 || 0) * 100) / 100) }],
  ax({ x: 0.5, y: 1.3, w: 7.6, h: 5.2, barDir: 'col', chartColors: [HEX.teal, HEX.berry], showValue: true, dataLabelPosition: 'outEnd', dataLabelFormatCode: '0.00', showLegend: true, legendPos: 'b', showTitle: true, title: 'Best models per sampling date', valAxisMaxVal: 1, valAxisMinVal: 0 }));
const vk = Object.keys(D.by_variety);
const vrows = [['Variety', 'Macro-F1', 'R² (PDI)'].map(t => ({ text: t, options: { bold: true, color: 'FFFFFF', fill: { color: HEX.teal } } }))].concat(vk.map(v => [v, f3(D.by_variety[v].macro_f1), f3(D.by_variety[v].r2)]));
s.addTable(vrows, { x: 8.4, y: 1.35, w: 4.4, colW: [1.4, 1.5, 1.5], fontSize: 14, color: HEX.text, border: { type: 'solid', pt: 0.5, color: 'D5DEDC' }, rowH: 0.45 });
txt(s, ['Early date (11 Feb) has mostly grades 0–1, so PDI varies little and R² is low', 'Accuracy is similar across varieties'], { x: 8.4, y: 3.5, w: 4.4, h: 2.9, fontSize: 14 });
s.addNotes('Per-date R² depends on the range of PDI on that date; RMSE is the better comparison across dates.');

// ---------- conclusions ----------
section('Conclusions', 'What the leaf analysis tells the UAV study');
s = slide('CONTENT', 'Key findings and their support in the literature');
const kf = [['Red-edge derivatives (690–860 nm) are the most robust white-rust features', 'Red-edge shift with chlorophyll loss (Horler et al., 1983; Shukla et al., 2024)'],
  ['A VNIR White Rust Index separates healthy and diseased leaves (BA ' + f3(D.t3.vnir.best.ba_cv) + ')', 'Disease-specific indices (Mahlein et al., 2013; Ashourloo et al., 2014)'],
  ['SWIR water indices respond (|r| up to ' + Math.max(...D.swir.map(r => Math.abs(r[2]))).toFixed(2) + ')', 'DWSI for rust (Apan et al., 2004); NDWI for blotch (Yu et al., 2018)'],
  ['Neighbouring grades overlap: six-grade macro-F1 ≈ ' + f3(D.cls[D.best.cls].macro_f1) + ', within one grade ≈ ' + f3(D.cls[D.best.cls].adj), 'Adjacent severity levels hard to separate (Mandal et al., 2023; Meng et al., 2020)'],
  ['Plot PDI is predicted from plot-mean spectra (R² ' + f3(D.reg[D.best.reg].r2) + ')', 'Severity regression from spectra (Liu et al., 2024; Feng et al., 2022)']];
const krows = [['Finding', 'Support'].map(t => ({ text: t, options: { bold: true, color: 'FFFFFF', fill: { color: HEX.teal } } }))].concat(kf);
s.addTable(krows, { x: 0.5, y: 1.35, w: 12.3, colW: [6.6, 5.7], fontSize: 14, color: HEX.text, border: { type: 'solid', pt: 0.5, color: 'D5DEDC' }, rowH: 0.8, valign: 'middle' });
s.addNotes('These leaf-level results fix the wavelengths and the index to look for in the UAV hyperspectral data.');

s = slide('CONTENT', 'Implications for the UAV analysis');
card(s, 0.5, 1.35, 3.9, 1.6, 'Red edge', 'priority region for UAV band selection and for the MS red-edge band', HEX.teal, 'imp1');
card(s, 4.7, 1.35, 3.9, 1.6, 'WRI', 'test the leaf-derived index on UAV canopy spectra', HEX.mustard, 'imp2');
card(s, 8.9, 1.35, 3.9, 1.6, 'PDI', 'regression is the more reliable severity target', HEX.berry, 'imp3');
txt(s, ['Use the same nested selection chain (Tier 2 → Boruta → VIF → ML-SFFS) on UAV data', 'Report ±1-grade accuracy with exact accuracy, since grades overlap', 'Check SWIR indices on the UAV SWIR sensor (coarser pixels; Apan et al., 2004)', 'Confirm with chlorophyll and water measurements (physiology correlation of Tier 4)'], { x: 0.5, y: 3.3, w: 12.3, h: 3.0, fontSize: 16 });
s.addNotes('Leaf results are an upper bound: canopy data add soil, shadow, flowers and illumination effects.');

// ---------- references ----------
const REFS = require('./data/refs_used.json');
const chunks = []; for (let i = 0; i < REFS.length; i += 16) chunks.push(REFS.slice(i, i + 16));
chunks.forEach((part, k) => {
  const s2 = slide('CONTENT', 'References' + (k ? ' (' + (k + 1) + '/' + chunks.length + ')' : ' (1/' + chunks.length + ')'));
  const h2 = Math.ceil(part.length / 2);
  [part.slice(0, h2), part.slice(h2)].forEach((col, j) => s2.addText(col.map((r, i) => ({ text: r, options: { breakLine: i < col.length - 1 } })),
    { isTextBox: true, x: 0.5 + j * 6.25, y: 1.3, w: 6.05, h: 5.6, fontSize: 10, color: HEX.text, valign: 'top', paraSpaceAfter: 2, objectName: 'references ' + j }));
});

pres.writeFile({ fileName: OUT }).then(async () => { await applyTheme(OUT, THEME); console.log('saved', OUT); });
