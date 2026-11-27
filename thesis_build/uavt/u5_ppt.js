// Slides: best ASD leaf models applied to the UAV hyperspectral image of 24 Feb 2026 (same theme as the ASD seminar deck).
// Every table and figure of the Word report appears here with the same number (checked at the end).
const pptxgen = require('pptxgenjs'); const fs = require('fs');
const { applyTheme } = require(process.env.SKILL_DIR + '/scripts/apply_theme.js');
const B = __dirname + '/'; const D = JSON.parse(fs.readFileSync(B + 'out/ppt_data.json', 'utf8')); const FG = B + 'fig/';
const OUT = B + '../outputs/UAV_24Feb2026_ASD_model_transfer.pptx';
const THEME = { name: 'White rust UAV transfer', headFontFace: 'Cambria', bodyFontFace: 'Calibri',
  colors: { dk1: '1B2A1E', lt1: 'FFFFFF', dk2: '2C5F2D', lt2: 'EEF3E8', accent1: '2C5F2D', accent2: '97BC62', accent3: '7030A0', accent4: 'C98A00', accent5: 'C62828', accent6: '1565C0', hlink: '1565C0', folHlink: '7030A0' } };
const pres = new pptxgen(); pres.layout = 'LAYOUT_WIDE'; pres.theme = { headFontFace: THEME.headFontFace, bodyFontFace: THEME.bodyFontFace };
pres.title = 'ASD leaf models on the UAV hyperspectral image (24 Feb 2026)'; pres.author = 'Animesh Panda';
pres.defineSlideMaster({ title: 'TITLE', background: { color: '2C5F2D' }, objects: [
  { placeholder: { options: { name: 'title', type: 'title', x: 0.7, y: 1.8, w: 11.9, h: 1.8, fontSize: 38, bold: true, color: 'FFFFFF', fontFace: 'Cambria', valign: 'middle' }, text: '' } },
  { placeholder: { options: { name: 'body', type: 'body', x: 0.7, y: 3.8, w: 11.9, h: 2.2, fontSize: 18, color: 'EEF3E8', fontFace: 'Calibri', valign: 'top' }, text: '' } }] });
pres.defineSlideMaster({ title: 'SECTION', background: { color: '1B2A1E' }, objects: [
  { placeholder: { options: { name: 'title', type: 'title', x: 0.7, y: 2.6, w: 11.9, h: 1.3, fontSize: 38, bold: true, color: 'FFFFFF', fontFace: 'Cambria' }, text: '' } },
  { placeholder: { options: { name: 'body', type: 'body', x: 0.7, y: 3.9, w: 11.9, h: 1.2, fontSize: 18, color: '97BC62', fontFace: 'Calibri' }, text: '' } }] });
pres.defineSlideMaster({ title: 'CONTENT', background: { color: 'FFFFFF' }, margin: [0.4, 0.5, 0.5, 0.5], objects: [
  { placeholder: { options: { name: 'title', type: 'title', x: 0.5, y: 0.25, w: 12.3, h: 0.8, fontSize: 26, bold: true, color: '2C5F2D', fontFace: 'Cambria', valign: 'middle' }, text: '' } },
  { text: { text: 'White rust of Indian mustard | ASD leaf models on the UAV image of 24 Feb 2026 | ICAR-IARI', options: { x: 0.5, y: 7.05, w: 9.5, h: 0.3, fontSize: 10, color: '6B7B6E', fontFace: 'Calibri' } } }],
  slideNumber: { x: 12.3, y: 7.05, w: 0.6, h: 0.3, fontSize: 10, color: '6B7B6E' } });
let SEC = '';
function sec(title, sub) { SEC = title; pres.addSection({ title }); const s = pres.addSlide({ masterName: 'SECTION', sectionTitle: title }); s.addText(title, { placeholder: 'title' }); if (sub) s.addText(sub, { placeholder: 'body' }); return s; }
function slide(title, notes) { const s = pres.addSlide({ masterName: 'CONTENT', sectionTitle: SEC }); s.addText(title, { placeholder: 'title' }); if (notes) s.addNotes(notes); return s; }
function bullets(s, items, x, y, w, h, fs = 16) {
  s.addText(items.map((t, i) => ({ text: t, options: { bullet: true, breakLine: i < items.length - 1 } })), { x, y, w, h, fontSize: fs, color: '1B2A1E', valign: 'top', paraSpaceAfter: 6, isTextBox: true, fit: 'shrink' });
}
function card(s, x, y, w, h, head, body, col = '2C5F2D', fill = 'EEF3E8', fs = 14) {
  s.addShape(pres.shapes.ROUNDED_RECTANGLE, { x, y, w, h, fill: { color: fill }, line: { color: fill }, rectRadius: 0.08, objectName: 'card' });
  s.addText(head, { x: x + 0.15, y: y + 0.08, w: w - 0.3, h: 0.42, fontSize: 15, bold: true, color: col, isTextBox: true, margin: 0 });
  s.addText(body, { x: x + 0.15, y: y + 0.52, w: w - 0.3, h: h - 0.6, fontSize: fs, color: '1B2A1E', valign: 'top', isTextBox: true, margin: 0, fit: 'shrink' });
}
function stat(s, x, y, w, big, label, col = '2C5F2D', fill = 'EEF3E8') {
  s.addShape(pres.shapes.ROUNDED_RECTANGLE, { x, y, w, h: 1.45, fill: { color: fill }, line: { color: fill }, rectRadius: 0.08, objectName: 'stat' });
  s.addText(big, { x, y: y + 0.08, w, h: 0.72, fontSize: 30, bold: true, color: col, align: 'center', isTextBox: true, margin: 0, fontFace: 'Cambria' });
  s.addText(label, { x: x + 0.1, y: y + 0.8, w: w - 0.2, h: 0.6, fontSize: 12, color: '1B2A1E', align: 'center', isTextBox: true, margin: 0, fit: 'shrink' });
}
const f2 = v => (v === null || v === undefined || Number.isNaN(v)) ? '–' : Number(v).toFixed(2);
const f3 = v => (v === null || v === undefined || Number.isNaN(v)) ? '–' : Number(v).toFixed(3);
const plain = t => String(t).replace(/\[\[F:(\w+)\]\]/g, (m, k) => 'Figure ' + (FIGN[k] || k)).replace(/\[\[T:(\w+)\]\]/g, (m, k) => 'Table ' + (TABN[k] || k)).replace(/\*\*/g, '');
const TABS = {}; const TABN = {}; D.tables.forEach(t => { TABS[t.key] = t; TABN[t.key] = t.number; });
const FIGS = {}; const FIGN = {}; D.figures.forEach(f => { FIGS[f.key] = f; FIGN[f.key] = f.number; });
const SHOWN_T = new Set(), SHOWN_F = new Set();
function interpNotes(key) { return (D.interp[key] || []).map(([l, t]) => l + ' ' + plain(t)).join('\n\n'); }
// one figure per slide, with its number and caption; interpretation result in the notes
function figSlide(key, title, interpKey, side) {
  const f = FIGS[key]; const s = slide(title, interpKey ? interpNotes(interpKey) : f.caption); SHOWN_F.add(key);
  const h = side ? 5.1 : 5.25;
  s.addImage({ path: FG + f.file, x: 0.5, y: 1.15, w: side ? 8.3 : 12.3, h, sizing: { type: 'contain', w: side ? 8.3 : 12.3, h } });
  if (side) s.addText(side, { x: 9.0, y: 1.2, w: 3.8, h: 5.1, fontSize: 13, color: '1B2A1E', valign: 'top', isTextBox: true, fit: 'shrink' });
  s.addText('Figure ' + f.number + '. ' + f.caption, { x: 0.5, y: 6.45, w: 12.3, h: 0.55, fontSize: 11, italic: true, color: '6B7B6E', isTextBox: true, fit: 'shrink' });
  return s;
}
// a report table on one or more slides (rows split when long), same number and caption as in the report
function tableSlides(key, title, interpKey, maxRows) {
  const t = TABS[key]; SHOWN_T.add(key); const rows = t.rows; const hdr = rows[0]; const body = rows.slice(1);
  const nc = hdr.length; const len = j => Math.min(48, Math.max(4, ...rows.map(r => String(r[j]).length)));
  const tot = hdr.reduce((a, _, j) => a + len(j), 0); const colW = hdr.map((_, j) => 12.3 * len(j) / tot);
  const longest = Math.max(...rows.map(r => r.reduce((a, c) => a + String(c).length, 0)));
  const per = maxRows || (body.length > 18 ? 16 : body.length);
  const fs = nc > 10 || longest > 300 ? 9 : nc > 7 || longest > 180 ? 10 : 12;
  const parts = Math.ceil(body.length / per) || 1;
  for (let p = 0; p < parts; p++) {
    const s = slide(title + (parts > 1 ? ' (' + (p + 1) + '/' + parts + ')' : ''), interpKey ? interpNotes(interpKey) : t.caption);
    const hcells = hdr.map(c => ({ text: String(c), options: { bold: true, color: 'FFFFFF', fill: { color: '2C5F2D' }, align: 'center', valign: 'middle' } }));
    const bcells = body.slice(p * per, (p + 1) * per).map((r, i) => r.map(c => ({ text: String(c), options: { fill: { color: i % 2 ? 'FFFFFF' : 'F4F7F1' }, valign: 'middle' } })));
    s.addTable([hcells, ...bcells], { x: 0.5, y: 1.15, w: 12.3, colW, fontSize: fs, fontFace: 'Calibri', color: '1B2A1E', border: { type: 'solid', pt: 0.5, color: 'C9D3C4' }, margin: 0.04, autoPage: false });
    s.addText('Table ' + t.number + '. ' + t.caption, { x: 0.5, y: 6.5, w: 12.3, h: 0.5, fontSize: 10.5, italic: true, color: '6B7B6E', isTextBox: true, fit: 'shrink' });
  }
}
const BEST = D.best, R = D.rows, U = D.uav, RN = D.rn; const KEY = { A: 'macro_F1', B: 'macro_F1', C: 'R2' };
const VAR = ['Direct', 'Healthy-reference corrected', 'Corrected + brightness-normalised']; const VSH = { 'Direct': 'Direct', 'Healthy-reference corrected': 'Corrected', 'Corrected + brightness-normalised': 'Normalised' };
const bv = RN.best_variant; const bo = t => R[t].overall[bv[t]];
const AX = { catAxisLabelColor: '444444', valAxisLabelColor: '444444', catAxisLabelFontFace: '+mn-lt', valAxisLabelFontFace: '+mn-lt', catAxisLabelFontSize: 11, valAxisLabelFontSize: 11,
  valGridLine: { color: 'DDDDDD', size: 0.5 }, catGridLine: { style: 'none' }, titleFontFace: '+mj-lt', titleFontSize: 14, titleColor: '2C5F2D', legendFontFace: '+mn-lt', legendFontSize: 11 };

// ---------------- title and summary
let s = pres.addSlide({ masterName: 'TITLE' });
s.addText('Do the ASD leaf models work on the UAV hyperspectral image?', { placeholder: 'title' });
s.addText('Best 2025-26 ASD white rust models applied to the UAV plot spectra of 24 February 2026\nAnimesh Panda | Ph.D. Agricultural Physics | ICAR-IARI, New Delhi', { placeholder: 'body' });
s = slide('Summary', D.findings.join('\n'));
stat(s, 0.5, 1.2, 2.9, f3(D.asd.A.overall), 'Detection macro-F1 on ASD leaves (' + BEST.A.overall + ')');
stat(s, 3.6, 1.2, 2.9, f3(bo('A').macro_F1), 'Same model on UAV plots (best input: ' + VSH[bv.A].toLowerCase() + ')', 'C62828', 'FDECEA');
stat(s, 6.7, 1.2, 2.9, f2(bo('C').R2), 'Score R² on UAV plots (' + BEST.C.overall + '; leaves ' + f2(D.asd.C.overall) + ')', 'C62828', 'FDECEA');
stat(s, 9.8, 1.2, 3.0, f3(U.A.macro_F1), U.A.model + ' trained on UAV plots: detection macro-F1 (AUC ' + f2(U.A.AUC) + ')', '1565C0', 'E3F2FD');
bullets(s, D.findings, 0.5, 2.85, 12.3, 4.0, 14);

// ---------------- introduction and methodology
sec('1  Introduction and methodology', 'Question, workflow and the eight method steps (concept, justification, papers, how, data, output)');
s = slide('Background: leaf spectra vs canopy spectra');
card(s, 0.5, 1.2, 6.05, 5.2, 'ASD leaf spectra (2025-26)', 'One leaf, contact probe, own lamp; no soil, shadow or atmosphere.\n\nModels detected diseased leaves well (macro-F1 ' + f3(D.asd.A.overall) + ') but graded severity only moderately.\n\nWhite rust changes pigments, structure and water, and therefore reflectance (Carter and Knapp, 2001; Mahlein et al., 2013).');
card(s, 6.75, 1.2, 6.05, 5.2, 'UAV canopy spectra', 'Each pixel mixes upper leaves, flowers, stems, soil and shadow, lit by sun and sky and viewed from above.\n\nCanopy reflectance depends on leaf area, leaf angle, background and geometry as much as on leaf optics (Asner, 1998; Jacquemoud et al., 2009).\n\nModels from one scale need not hold at another (Mahlein, 2016; Thomas et al., 2018; Bohnenkamp et al., 2019).', '1565C0', 'E3F2FD');
tableSlides('qs', 'Aim and questions');
figSlide('wf', 'Workflow of the transfer test', null, 'Eight steps:\n\nM1 UAV plot spectra\nM2 same-day ground truth\nM3 best ASD models\nM4 same pre-processing\nM5 three inputs\nM6 domain check\nM7 in-domain check\nM8 accuracy and uncertainty');
D.methods.forEach(st => {
  const s = slide(st.no + '  ' + st.title, [st.position, 'Likely question: ' + st.question].join('\n\n'));
  card(s, 0.5, 1.15, 4.0, 2.55, 'Concept', st.concept, '2C5F2D', 'EEF3E8', 12);
  card(s, 0.5, 3.8, 4.0, 2.6, 'Why here', st.why, '2C5F2D', 'EEF3E8', 12);
  card(s, 4.65, 1.15, 4.1, 5.25, 'How it is done', st.how.map((h, i) => (i + 1) + '. ' + h).join('\n') + (st.eqs.length ? '\n\n' + st.eqs.map(e => '(' + e[1] + ') ' + e[0].replace(/_\{([^}]*)\}/g, '$1').replace(/\^\{([^}]*)\}/g, '^$1')).join('\n') : ''), '1565C0', 'E3F2FD', 11.5);
  card(s, 8.9, 1.15, 3.9, 2.0, 'What the papers did', st.papers, '7030A0', 'F3E5F5', 11);
  card(s, 8.9, 3.25, 3.9, 1.75, 'Applied to these data', st.mine, 'C98A00', 'FFF6E0', 11);
  card(s, 8.9, 5.1, 3.9, 1.3, 'Output', st.output, '2C5F2D', 'EEF3E8', 11);
  s.addText('Notes: ' + st.notes, { x: 0.5, y: 6.45, w: 12.3, h: 0.55, fontSize: 10.5, italic: true, color: '6B7B6E', isTextBox: true, fit: 'shrink' });
  if (st.no === 'M2') tableSlides('gts', 'M2  Ground truth of 24 Feb: summary');
  if (st.no === 'M3') tableSlides('best', 'M3  Best ASD models and their inputs');
  if (st.no === 'M8') tableSlides('acc', 'M8  Accuracy measures explained', null, 9);
});

// ---------------- results
sec('2  Results and interpretation', 'Spectra, domain check, detection, grades, score, all models, in-domain check, summary');
figSlide('spec', 'Leaf vs canopy spectra', 'spectra');
tableSlides('bands', 'Mean reflectance per band region', 'spectra');
figSlide('feat', 'Domain check: inputs outside the leaf range', 'domain', RN.out50.direct + ' of ' + D.dom.length + ' inputs are outside the leaf range for > 50 % of plots (direct); ' + RN.out50.corrected + ' corrected; ' + RN.out50.normalised + ' normalised.' + (RN.gapf.length ? '\n\n' + RN.gapf.join(', ') + ' lies in a UAV band gap.' : ''));
tableSlides('dom', 'Domain check: feature table', 'domain');
figSlide('pca', 'Domain check: PCA of leaves and plots', 'domain', 'UAV plots beyond the 99th-percentile Mahalanobis distance of the leaves:\n\ndirect ' + f2(RN.pca_out['UAV plot (direct)']) + ' %\nnormalised ' + f2(RN.pca_out['UAV plot (corrected + brightness-normalised)']) + ' %');
tableSlides('tA', 'Detection: results', 'detection');
figSlide('cmA', 'Detection: confusion matrices', 'detection');
tableSlides('tB', 'Six grades: results', 'grades');
figSlide('cmB', 'Six grades: confusion matrices', 'grades');
tableSlides('tC', 'Severity score: results', 'score');
figSlide('scat', 'Severity score: predicted vs true', 'score');
figSlide('heat', 'All 30 ASD models on the UAV plots', 'allmodels');
if (TABS.maxs) tableSlides('maxs', 'Best of all models vs chance (maximum-statistic test)', 'allmodels');
tableSlides('uavt', 'In-domain check: models trained on the UAV plots', 'indomain');
if (TABS.perm) tableSlides('perm', 'In-domain check: permutation test', 'indomain');
figSlide('summ', 'Summary: leaves vs UAV', 'summary');
s = slide('Summary chart (native): best models, leaves vs UAV', interpNotes('summary'));
const cats = ['A ' + BEST.A.overall, 'B ' + BEST.B.overall, 'C ' + BEST.C.overall];
const data = [{ name: 'ASD leaves (LORO)', labels: cats, values: ['A', 'B', 'C'].map(t => D.asd[t].overall) }]
  .concat(VAR.map(v => ({ name: 'UAV ' + VSH[v].toLowerCase(), labels: cats, values: ['A', 'B', 'C'].map(t => Math.max(-1, R[t].overall[v][KEY[t]])) })))
  .concat([{ name: 'UAV-trained ML (LORO)', labels: cats, values: ['A', 'B', 'C'].map(t => U[t][KEY[t]]) }]);
s.addChart(pres.charts.BAR, data, Object.assign({}, AX, { x: 0.5, y: 1.2, w: 8.4, h: 5.3, barDir: 'col', barGrouping: 'clustered', chartColors: ['999999', '4C72B0', 'DD8452', '8172B3', '2CA02C'],
  showLegend: true, legendPos: 'b', valAxisMinVal: -1, valAxisMaxVal: 1, valAxisLabelFormatCode: '0.0', showTitle: true, title: 'Macro-F1 (A, B) and R² (C); values below −1 shown as −1' }));
card(s, 9.1, 1.2, 3.7, 5.3, 'Reading the chart', 'Grey = leaf score of the best model.\nBlue, orange, purple = the same frozen model on the UAV plots (three inputs).\nGreen = the best ML type trained on the UAV plots: detection recovers, grades and score stay weak with 48 plots.');

// ---------------- discussion, conclusions
sec('3  Discussion and conclusions');
s = slide('Why the leaf models do not transfer');
card(s, 0.5, 1.2, 4.0, 2.6, 'Different measurement', 'One leaf + lamp vs a mixed canopy pixel in sunlight; canopy structure and background change reflectance (Asner, 1998).');
card(s, 4.65, 1.2, 4.0, 2.6, 'Out-of-range inputs', 'First-derivative features scale with reflectance; canopy values lie outside the leaf training range (Sahigara et al., 2012).');
card(s, 8.8, 1.2, 4.0, 2.6, 'Missing bands', (RN.gapf.length ? RN.gapf.join(', ') + ' lies in a removed water-vapour band: its UAV value is an interpolation.' : 'No input of the new best models lies in a UAV band gap, so the gaps do not explain the failure.'));
card(s, 0.5, 4.0, 6.1, 2.45, 'Brightness and illumination', 'Plot brightness varied strongly even between replications (UAV spectra workbook): radiometric, not disease (Aasen et al., 2018).');
card(s, 6.75, 4.0, 6.05, 2.45, 'Different target', 'A leaf model predicts one leaf; the plot spectrum averages the visible canopy (upper leaves, flowers), the plot score averages three tagged leaf positions.');
s = slide('What the corrections can and cannot do');
bullets(s, ['Healthy-reference correction = empirical-line calibration with the healthy plots as reference targets (Smith and Milton, 1999).', 'Brightness normalisation removes multiplicative effects (Barnes et al., 1989; Rinnan et al., 2009).',
  'Both align the mean level of the spectra, the first step of calibration transfer (Feudale et al., 2002), but cannot recreate the leaf-level healthy–diseased contrast in a mixed canopy.',
  'Full transfer (piecewise direct standardisation, domain adaptation) needs paired leaf and canopy spectra of the same plants (Feudale et al., 2002; Pan and Yang, 2010).'], 0.5, 1.3, 12.3, 5.2, 18);
s = slide('What it means for the thesis');
card(s, 0.5, 1.2, 6.1, 5.25, 'In-domain check', U.A.model + ' trained on the UAV plots: detection macro-F1 ' + f3(U.A.macro_F1) + ', AUC ' + f2(U.A.AUC) + ' (frozen leaf model: ' + f3(bo('A').macro_F1) + ').\n\nThe disease signal is present at the canopy but must be learned from canopy data.\n\nGrades and score need more samples and a wider severity range: '
  + U.B.model + ' macro-F1 ' + f3(U.B.macro_F1) + ', ' + U.C.model + ' R² ' + f2(U.C.R2) + ' with 48 plots of one date.', '1565C0', 'E3F2FD');
card(s, 6.75, 1.2, 6.05, 5.25, 'Use in 2026-27', '• Train UAV models on UAV features with subplot scores (1536 post-symptomatic samples per camera).\n• Use the ASD results to choose and explain features (red edge, green peak, NIR plateau, water-band edges).\n• Measure leaf and canopy spectra of the same tagged plants on the same day → real calibration transfer (Feudale et al., 2002).\n• Check radiometric calibration before modelling (Aasen et al., 2018).');
s = slide('Limitations');
bullets(s, ['One UAV date and 48 plots: wide confidence intervals (Efron and Tibshirani, 1993).', 'Ground truth from three tagged leaf positions, not the whole visible canopy.', 'No paired leaf–canopy spectra, so only simple corrections could be tested.', 'Radiometric quality of the image not yet verified (Aasen et al., 2018).'], 0.5, 1.3, 12.3, 5.2, 20);
s = slide('Conclusions');
bullets(s, ['The best ASD leaf models applied unchanged to the UAV image of 24 Feb 2026 gave about chance-level detection (macro-F1 ' + f3(bo('A').macro_F1) + ') and no useful grade or score information (R² ' + f2(bo('C').R2) + ').',
  'Healthy-reference correction and brightness normalisation did not fix the leaf–canopy mismatch.',
  'The canopy spectra carry a detection signal: the same model type trained on the UAV plots reached macro-F1 ' + f3(U.A.macro_F1) + ' (AUC ' + f2(U.A.AUC) + ').',
  'Leaf models should guide, not replace, UAV models: train and validate UAV models on UAV data with same-scale ground truth (Zhang et al., 2019).'], 0.5, 1.3, 12.3, 5.2, 19);
tableSlides('qa', 'Likely questions');

// ---------------- appendix: every remaining table of the report
sec('Appendix', 'Every table of the report: ground truth, per-plot predictions, all models, confidence intervals, how to apply, findings, glossary');
tableSlides('gtab', 'Appendix A  Ground truth per plot');
tableSlides('ppA', 'Appendix B  Detection predictions per plot');
tableSlides('ppB', 'Appendix C  Grade predictions per plot');
tableSlides('ppC', 'Appendix D  Score predictions per plot');
['allA', 'allB', 'allC'].forEach((k, i) => tableSlides(k, 'Appendix E  All ASD models on the UAV plots (' + 'ABC'[i] + ')'));
if (TABS.ci) tableSlides('ci', 'Appendix F  Confidence intervals', null, 12);
tableSlides('apply', 'Appendix G  How to apply the procedure to another data set', null, 9);
tableSlides('find', 'Appendix H  Key findings');
tableSlides('gloss', 'Appendix H  Glossary');
// safety net: any report table or figure not shown above
D.tables.forEach(t => { if (!SHOWN_T.has(t.key)) tableSlides(t.key, 'Table ' + t.number); });
D.figures.forEach(f => { if (!SHOWN_F.has(f.key)) figSlide(f.key, 'Figure ' + f.number); });
s = slide('References');
s.addText(D.refs.map((r, i) => ({ text: r, options: { breakLine: i < D.refs.length - 1 } })), { x: 0.5, y: 1.15, w: 12.3, h: 5.8, fontSize: 8.5, color: '1B2A1E', valign: 'top', paraSpaceAfter: 2, isTextBox: true, fit: 'shrink' });
console.log('tables shown', SHOWN_T.size, 'of', D.tables.length, '| figures shown', SHOWN_F.size, 'of', D.figures.length);
pres.writeFile({ fileName: OUT }).then(async () => { await applyTheme(OUT, THEME); console.log('saved', OUT); });
