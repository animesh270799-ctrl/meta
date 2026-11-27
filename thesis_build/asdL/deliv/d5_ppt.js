// Part L ASD 2025-26 leaf analysis deck: native, editable charts (same data as the Excel workbook), step cards and references on every step slide.
const pptxgen = require('pptxgenjs'); const fs = require('fs'); const path = require('path');
const { applyTheme } = require('/root/.claude/skills/synced/9bf50f97-a337-4b6b-8c8b-ebd229b7e0d3_d565bc3b-4006-4195-b033-a8c25dfdc114/pptx/scripts/apply_theme.js');
const D = JSON.parse(fs.readFileSync(path.join(__dirname, 'pptdata.json'), 'utf8')); const OUT = process.argv[2] || path.join(__dirname, 'PartL_ASD_2025-26_leaf_analysis.pptx');
const THEME = { name: 'PartL', headFontFace: 'Cambria', bodyFontFace: 'Calibri', colors: { dk1: '1A1A1A', lt1: 'FFFFFF', dk2: '1F3864', lt2: 'F3F5F9', accent1: '1F3864', accent2: '2E7D32', accent3: 'C0392B', accent4: 'D9A400', accent5: '2F5D8A', accent6: '7F7F7F', hlink: '0563C1', folHlink: '7030A0' } };
const pres = new pptxgen(); pres.layout = 'LAYOUT_WIDE'; pres.theme = { headFontFace: 'Cambria', bodyFontFace: 'Calibri' }; pres.title = 'Part L analysis of the 2025-26 ASD leaf spectra';
const C = pres.SchemeColor; const NAVY = '1F3864', GREEN = '2E7D32', RED = 'C0392B', GREY = '595959', LIGHT = 'F3F5F9';
pres.defineSlideMaster({ title: 'TITLE', background: { color: NAVY }, objects: [], slideNumber: undefined });
pres.defineSlideMaster({ title: 'SECTION', background: { color: NAVY }, objects: [{ placeholder: { options: { name: 'title', type: 'title', x: 0.8, y: 2.6, w: 11.7, h: 1.2, fontSize: 36, bold: true, color: 'FFFFFF', fontFace: 'Cambria' }, text: '' } }] });
pres.defineSlideMaster({ title: 'CONTENT', background: { color: 'FFFFFF' }, margin: [0.3, 0.4, 0.5, 0.4],
  objects: [{ rect: { x: 0, y: 0, w: 13.333, h: 0.95, fill: { color: LIGHT } } }, { line: { x: 0.4, y: 0.95, w: 12.53, h: 0, line: { color: NAVY, width: 1.25 } } },
            { text: { text: 'Part L · ASD leaf spectra 2025-26 · white rust of mustard', options: { x: 0.4, y: 7.08, w: 8, h: 0.3, fontSize: 9, color: '7F7F7F', fontFace: 'Calibri' } } },
            { placeholder: { options: { name: 'title', type: 'title', x: 0.4, y: 0.12, w: 12.5, h: 0.75, fontSize: 24, bold: true, color: NAVY, fontFace: 'Cambria', valign: 'middle' }, text: '' } }],
  slideNumber: { x: 12.4, y: 7.06, w: 0.6, h: 0.3, fontSize: 9, color: '7F7F7F', fontFace: 'Calibri' } });
let SEC = 'Introduction';
const section = (t, sub) => { SEC = t; pres.addSection({ title: t }); const s = pres.addSlide({ masterName: 'SECTION', sectionTitle: t }); s.addText(t, { placeholder: 'title' }); if (sub) s.addText(sub, { x: 0.8, y: 3.85, w: 11.7, h: 1.0, fontSize: 18, color: 'D6DCE5', fontFace: 'Calibri', isTextBox: true }); return s; };
const slide = (t) => { const s = pres.addSlide({ masterName: 'CONTENT', sectionTitle: SEC }); s.addText(t, { placeholder: 'title' }); return s; };
const refs = (s, t) => { if (t) s.addText([{ text: 'References: ', options: { bold: true } }, { text: t }], { x: 0.4, y: 6.62, w: 12.5, h: 0.42, fontSize: 9.5, italic: true, color: '404040', fontFace: 'Calibri', valign: 'top', isTextBox: true, margin: 0 }); };
const banner = (s, t, y = 6.12) => { s.addShape(pres.shapes.ROUNDED_RECTANGLE, { x: 0.4, y, w: 12.5, h: 0.44, fill: { color: 'E2EFDA' }, line: { color: GREEN, width: 0.75 }, rectRadius: 0.06, objectName: 'output' }); s.addText([{ text: 'Output: ', options: { bold: true, color: GREEN } }, { text: t, options: { color: '1A1A1A' } }], { x: 0.55, y, w: 12.2, h: 0.44, fontSize: 12, fontFace: 'Calibri', valign: 'middle', isTextBox: true, margin: 0 }); };
const bul = (s, items, o) => s.addText(items.map((t, i) => ({ text: t, options: { bullet: true, breakLine: i < items.length - 1, paraSpaceAfter: 4 } })), { fontSize: 13, color: '1A1A1A', fontFace: 'Calibri', valign: 'top', isTextBox: true, ...o });
const fmtLabel = (vals) => vals.every(v => v === null || Number.isInteger(v)) ? '0' : (Math.max(...vals.filter(v => v !== null).map(Math.abs)) >= 10 ? '0.0' : '0.000');
function chart(s, id, x, y, w, h, o = {}) {
  const c = D.charts[id]; if (!c) { s.addText('(chart ' + id + ' not available)', { x, y, w, h, isTextBox: true }); return; }
  const base = { x, y, w, h, showTitle: true, title: c.title, titleFontSize: 11, titleColor: NAVY, titleFontFace: 'Calibri', chartColors: c.colors, catAxisLabelFontSize: 9, valAxisLabelFontSize: 9,
    catAxisLabelColor: '404040', valAxisLabelColor: '404040', valGridLine: { color: 'E3E3E3', size: 0.5 }, catGridLine: { style: 'none' }, showLegend: c.series.length > 1, legendPos: 'b', legendFontSize: 9,
    showCatAxisTitle: !!c.xlab, catAxisTitle: c.xlab || '', showValAxisTitle: !!c.ylab, valAxisTitle: c.ylab || '', catAxisTitleFontSize: 9.5, valAxisTitleFontSize: 9.5, catAxisTitleColor: '404040', valAxisTitleColor: '404040' };
  let type, data;
  if (c.kind === 'scatter') {
    type = pres.charts.SCATTER; data = [{ name: 'X', values: c.x }].concat(c.series.map(r => ({ name: r.name, values: r.values })));
    Object.assign(base, { lineSize: 1.5, lineDataSymbol: 'circle', lineDataSymbolSize: 4, valAxisLabelFormatCode: 'General', catAxisLabelFormatCode: 'General', catAxisLabelPos: 'low', valAxisLabelPos: 'low' });
    const xs = c.x.filter(v => v !== null), lo = Math.min(...xs), hi = Math.max(...xs);
    if (lo >= 350 && hi <= 2500 && hi - lo > 300) Object.assign(base, { catAxisMinVal: Math.floor(lo / 100) * 100, catAxisMaxVal: Math.ceil(hi / 100) * 100, catAxisMajorUnit: w < 5 ? 400 : 200 });
  } else if (c.kind === 'line') {
    const xs = c.x.map(Number); type = pres.charts.SCATTER; data = [{ name: 'X', values: xs }].concat(c.series.map(r => ({ name: r.name, values: r.values })));
    Object.assign(base, { lineSize: 1.5, lineDataSymbol: c.markers ? 'circle' : 'none', lineDataSymbolSize: 5, valAxisLabelFormatCode: 'General', catAxisLabelFormatCode: 'General', catAxisLabelPos: 'low', valAxisLabelPos: 'low' });
    const lo = Math.min(...xs), hi = Math.max(...xs);
    if (lo >= 350 && hi <= 2500 && hi - lo > 300) Object.assign(base, { catAxisMinVal: Math.floor(lo / 100) * 100, catAxisMaxVal: Math.ceil(hi / 100) * 100, catAxisMajorUnit: w < 5 ? 400 : 200 });
    else Object.assign(base, { catAxisMinVal: lo, catAxisMaxVal: hi });
  } else {
    type = pres.charts.BAR; data = c.series.map(r => ({ name: r.name, labels: c.x, values: r.values }));
    Object.assign(base, { barDir: c.kind === 'bar' ? 'bar' : 'col', barGapWidthPct: 60, catAxisOrientation: c.kind === 'bar' ? 'minMax' : 'minMax' });
    if (c.point_colors && c.series.length === 1) base.chartColors = c.point_colors;
    if (c.labels_on) Object.assign(base, { showValue: true, dataLabelPosition: 'outEnd', dataLabelFontSize: 8, dataLabelColor: '404040', dataLabelFormatCode: fmtLabel(c.series.flatMap(r => r.values)) });
  }
  s.addChart(type, data, Object.assign(base, o));
}
function tbl(s, rows, x, y, w, colW, fs = 11, o = {}) {
  const hdr = rows[0].map(t => ({ text: t, options: { bold: true, color: 'FFFFFF', fill: { color: NAVY }, align: 'center', valign: 'middle' } }));
  const body = rows.slice(1).map((r, i) => r.map(t => ({ text: String(t), options: { fill: { color: i % 2 ? 'F2F2F2' : 'FFFFFF' }, valign: 'middle' } })));
  s.addTable([hdr].concat(body), { x, y, w, colW, fontSize: fs, fontFace: 'Calibri', color: '1A1A1A', border: { type: 'solid', pt: 0.5, color: 'BFBFBF' }, margin: 0.04, autoPage: false, ...o });
}
function heat(s, M, labels, x, y, cw, ch, maxv, color, title, fmt = (v) => String(v)) {
  if (title) s.addText(title, { x, y: y - 0.38, w: cw * (labels.length + 1), h: 0.34, fontSize: 11, bold: true, color: NAVY, isTextBox: true, margin: 0 });
  const rgb = (v) => { const t = Math.min(1, v / maxv); const c0 = [255, 255, 255], c1 = color; return c0.map((a, i) => Math.round(a + (c1[i] - a) * t).toString(16).padStart(2, '0')).join('').toUpperCase(); };
  const rows = [[{ text: '', options: { fill: { color: 'FFFFFF' } } }].concat(labels.map(l => ({ text: l, options: { bold: true, fill: { color: LIGHT }, align: 'center' } })))];
  M.forEach((r, i) => rows.push([{ text: labels[i], options: { bold: true, fill: { color: LIGHT }, align: 'center' } }].concat(r.map(v => ({ text: fmt(v), options: { fill: { color: rgb(v) }, align: 'center', color: v / maxv > 0.6 ? 'FFFFFF' : '1A1A1A' } })))));
  s.addTable(rows, { x, y, w: cw * (labels.length + 1), colW: Array(labels.length + 1).fill(cw), rowH: ch, fontSize: 10, fontFace: 'Calibri', border: { type: 'solid', pt: 0.5, color: 'BFBFBF' }, margin: 0.02 });
}
const ST = Object.fromEntries(D.steps.map(s => [s.code, s]));
function card(code) {
  const st = ST[code]; const s = slide('Step ' + st.code + ' – ' + st.title);
  const box = (x, y, w, h, lab, txt, col) => {
    s.addShape(pres.shapes.RECTANGLE, { x, y, w, h, fill: { color: 'FFFFFF' }, line: { color: 'BFBFBF', width: 0.75 }, objectName: 'card ' + lab });
    s.addShape(pres.shapes.RECTANGLE, { x, y, w: 0.08, h, fill: { color: col }, line: { color: col, width: 0 } });
    const items = Array.isArray(txt) ? txt : [txt];
    s.addText([{ text: lab, options: { bold: true, color: col, fontSize: 12, breakLine: true } }].concat(items.map((t, i) => ({ text: t, options: { fontSize: 10.5, color: '1A1A1A', bullet: items.length > 1 ? { indent: 10 } : false, breakLine: i < items.length - 1 } }))),
      { x: x + 0.15, y: y + 0.04, w: w - 0.22, h: h - 0.08, valign: 'top', fontFace: 'Calibri', isTextBox: true, margin: 0.02, fit: 'shrink' });
  };
  box(0.4, 1.12, 6.15, 1.55, 'Concept and justification', [st.what || st.title, 'Why: ' + st.why], NAVY);
  box(6.75, 1.12, 6.15, 1.55, 'Position and samples used', ['Position: ' + st.position, 'Samples: ' + st.samples], '2F5D8A');
  box(0.4, 2.8, 6.15, 1.75, 'Settings', st.settings, '7F7F7F');
  box(6.75, 2.8, 6.15, 1.75, 'How it was done with my data', st.mydata, GREEN);
  box(0.4, 4.68, 6.15, 1.38, 'Result', st.result.length ? st.result : ['—'], RED);
  box(6.75, 4.68, 6.15, 1.38, 'Notes, alternatives and interview question', [st.notes, st.q].filter(x => x), 'D9A400');
  banner(s, st.output); refs(s, st.refs); return s;
}
const F = D.facts, T = D.tabs, R = (c) => ST[c] ? ST[c].refs : '';
// ======================================================================= slides
pres.addSection({ title: 'Introduction' }); let s = pres.addSlide({ masterName: 'TITLE', sectionTitle: 'Introduction' });
s.addText('Part L analysis of the 2025-26 ASD leaf spectra', { x: 0.8, y: 1.6, w: 11.7, h: 1.0, fontSize: 36, bold: true, color: 'FFFFFF', fontFace: 'Cambria', isTextBox: true });
s.addText('White rust of Indian mustard – leaf disease score pooled over all dates, growth stages, varieties and leaf positions', { x: 0.8, y: 2.7, w: 11.7, h: 0.9, fontSize: 20, color: 'D6DCE5', fontFace: 'Calibri', isTextBox: true });
s.addText('Steps L1–L10 of the 2026-27 methodology applied to the four ASD FieldSpec data sets (11 Feb, 24 Feb, 3 Mar, 13 Mar 2026) · ICAR-IARI, Division of Agricultural Physics', { x: 0.8, y: 4.3, w: 11.7, h: 0.8, fontSize: 14, color: 'BFC9D9', fontFace: 'Calibri', isTextBox: true });
s = slide('The analysis at a glance');
const stat = (x, y, v, l, col) => { s.addText(v, { x, y, w: 2.9, h: 0.8, fontSize: 34, bold: true, color: col, fontFace: 'Cambria', align: 'center', isTextBox: true }); s.addText(l, { x, y: y + 0.8, w: 2.9, h: 0.6, fontSize: 12, color: GREY, align: 'center', isTextBox: true }); };
stat(0.5, 1.25, String(F.n_final), 'leaf spectra after checks (of ' + F.n_read + ' read)', NAVY); stat(3.6, 1.25, '4', 'dates · 3 stages · 3 varieties · 3 leaf positions', NAVY); stat(6.7, 1.25, F.n_train + ' / ' + F.n_test, 'training / test leaves (33 / 15 plots)', NAVY); stat(9.8, 1.25, '3', 'tasks: detection, six grades, grade score', NAVY);
if (T.best) { tbl(s, T.best, 0.5, 3.1, 12.3, [2.9, 1.6, 2.6, 5.2], 12); }
bul(s, ['Same plot split, selection chain and models as the canopy (UAV) data, so leaf and canopy results can be compared (Step L9).', 'Selection on training leaves only; test leaves predicted once; every step cross-checked (sheet Checks of the Excel file).'], { x: 0.5, y: 5.0, w: 12.3, h: 1.0 });
refs(s, 'Methodology 2026-27, Part L; Ma et al. (2026); Lv et al. (2023); Mandal et al. (2023).');
s = slide('Data and design (2025-26 season)');
bul(s, ['Field trial at ICAR-IARI: 48 plots = block C (plots 1–12, fungicide-protected, healthy) + three unsprayed replications R1–R3 (plots 13–48).', 'Treatments: 3 varieties (V1–V3) × 4 sowing dates (D1 9 Dec, D2 18 Dec, D3 27 Dec 2025, D4 9 Jan 2026); natural white rust infection.',
  'ASD FieldSpec leaf-clip spectra (350–2500 nm, 1 nm) on 11 Feb, 24 Feb, 3 Mar and 13 Mar 2026; leaves L3, L5 and the last leaf (LL); one spectrum per leaf.', 'Each leaf scored on the 0–9 white rust key (grades 0, 1, 3, 5, 7, 9) (Conn et al., 1990).',
  'Tasks: A = healthy (grade 0) vs diseased; B = six grades; C = grade as a number (regression).', 'Pooled analysis: all dates, stages, varieties and leaf positions in one data set; strata reported separately at L5.1 and L7.'], { x: 0.4, y: 1.15, w: 6.7, h: 4.9 });
chart(s, 'c02', 7.2, 1.1, 5.7, 4.9); refs(s, 'Conn et al. (1990); Chattopadhyay et al. (2011); methodology 2026-27, Steps A4 and L1.');
s = slide('Order of the Part L steps');
const fb = (x, y, t, col, sub) => { s.addShape(pres.shapes.ROUNDED_RECTANGLE, { x, y, w: 2.85, h: 1.05, fill: { color: col }, line: { color: '7F7F7F', width: 0.75 }, rectRadius: 0.1, objectName: 'flow ' + t });
  s.addText([{ text: t, options: { bold: true, fontSize: 12, color: NAVY, breakLine: true } }, { text: sub, options: { fontSize: 10.5, color: '1A1A1A' } }], { x: x + 0.05, y, w: 2.75, h: 1.05, align: 'center', valign: 'middle', isTextBox: true, margin: 0.02 }); };
const X4 = [0.45, 3.65, 6.85, 10.05], Y3 = [1.2, 2.85, 4.5];
const FL = [[['L1 Leaf table + checks', F.n_read + ' → ' + F.n_final + ' leaves'], ['L2 Split by plot', '33 training / 15 test plots'], ['L3 Pre-processing', 'SG 11/2, 400–2400 nm, FD, 5-nm'], ['L4 Indices', '48 indices + REP, Dr, SDr']],
            [['L5.5–L5.7', 'VIF → DSF; JM; PCA'], ['L5.3–L5.4', 'NDSI, RSI, WRI; |r| filter, ReliefF'], ['L5.2 Optimal wavelengths', 'R² maps → SHAP-CARS'], ['L5.1 Response curves', 'all leaves (description)']],
            [['L6 Models', 'ML: SFFS + grid; networks'], ['L7 Test metrics', F.n_test + ' test leaves, once'], ['L8 Covariate baseline', 'M0, M1, M2; ΔS, ΔC'], ['L9 Leaf–canopy link', 'UAV plot spectra, 24 Feb']]];
const FC = ['E8F1FA', 'EAF5E4', 'F6E6F0'];
FL.forEach((row, r) => row.forEach(([t, sub], i) => fb(X4[i], Y3[r], t, (r === 1 && i === 3) ? 'FFF4DC' : FC[r], sub)));
const arr = (x1, y1, x2, y2) => s.addShape(pres.shapes.LINE, { x: Math.min(x1, x2), y: Math.min(y1, y2), w: Math.abs(x2 - x1), h: Math.abs(y2 - y1), flipH: x2 < x1, line: { color: '404040', width: 1.5, endArrowType: 'triangle' } });
for (let i = 0; i < 3; i++) { arr(X4[i] + 2.85, Y3[0] + 0.52, X4[i + 1], Y3[0] + 0.52); arr(X4[i + 1], Y3[1] + 0.52, X4[i] + 2.85, Y3[1] + 0.52); arr(X4[i] + 2.85, Y3[2] + 0.52, X4[i + 1], Y3[2] + 0.52); }
arr(X4[3] + 1.42, Y3[0] + 1.05, X4[3] + 1.42, Y3[1]); arr(X4[0] + 1.42, Y3[1] + 1.05, X4[0] + 1.42, Y3[2]);
s.addText('Blue = data preparation · green = selection (training leaves only; L5.1 and L5.7 describe all leaves) · pink = models and evaluation. L10 (pre-symptomatic) is not applicable to 2025-26.', { x: 0.45, y: 5.7, w: 12.4, h: 0.4, fontSize: 11, italic: true, color: GREY, isTextBox: true });
refs(s, 'Methodology 2026-27, Part L (Steps L1–L10); Ma et al. (2026).');
s = slide('Which leaves are used in which step');
tbl(s, [['Step', 'All leaves (' + F.n_final + ')', 'Training leaves (' + F.n_train + ')', 'Test leaves (' + F.n_test + ')'], ['L1–L4 checks, pre-processing, indices', '✓ (leaf by leaf)', '', ''], ['L5.1 response curves, L5.7 PCA', '✓ description', '', ''],
  ['L5.2–L5.6 selection (OW, WRI, VI, DSF, JM)', '', '✓', 'never used'], ['L6 ML: SFFS + grid (GroupKFold(3) by plot)', '', '✓ all ' + F.n_train, 'never used'], ['L6 networks', '', '✓ fit ' + F.n_fit + ' + validation ' + F.n_val, 'never used'],
  ['L7 test metrics', '', '', '✓ once'], ['L8 covariate baseline', '', '✓ fit', '✓ once'], ['L9 leaf–canopy link (24 Feb)', '✓ plot means', 'thresholds (33 plots)', '✓ 15 plots']], 0.5, 1.2, 12.3, [4.6, 2.4, 2.9, 2.4], 13);
banner(s, 'Hybrid design: description on all leaves, selection and training on the training plots, test plots used once.', 5.6); refs(s, 'Ma et al. (2026); Tian et al. (2021); Lv et al. (2023); methodology 2026-27 (hybrid design).');
// ---------------- L1
section('Step L1 – Leaf table and data checks', 'From four ASD files to one checked leaf table'); card('L1');
s = slide('L1 results: sample flow and checks'); chart(s, 'c01', 0.4, 1.1, 5.6, 2.6); tbl(s, T.checks.map(r => [r[0], r[1], r[2].length > 70 ? r[2].slice(0, 68) + '…' : r[2], r[3]]), 6.2, 1.1, 6.7, [0.6, 2.0, 3.4, 0.7], 9);
chart(s, 'c02', 0.4, 3.8, 5.6, 2.25); banner(s, F.n_final + ' leaves kept; ' + F.n_dup + ' duplicates and ' + F.n_L4 + ' L4 leaves removed; ' + F.n_if + ' Isolation Forest flags checked, none faulty.'); refs(s, R('L1'));
s = slide('L1 results: grades by leaf position, growth stage and variety'); chart(s, 'c03', 0.4, 1.1, 4.1, 4.9); chart(s, 'c04', 4.6, 1.1, 4.1, 4.9); chart(s, 'c05', 8.8, 1.1, 4.1, 4.9);
banner(s, 'All grades occur in every stratum; LL leaves and later stages carry the higher grades; grade 9 is the smallest class (class weights and macro-F1 needed).'); refs(s, R('L1'));
// ---------------- L2
section('Step L2 – Split by plot and inner validation', 'Same 15 test plots and 11 network validation plots as the 2026-27 plan'); card('L2');
s = slide('L2 results: grade distribution of each part'); chart(s, 'c06', 0.4, 1.1, 4.1, 4.9); chart(s, 'c07', 4.6, 1.1, 4.1, 4.9); chart(s, 'c07b', 8.8, 1.1, 4.1, 4.9);
banner(s, F.n_train + ' training leaves (fit ' + F.n_fit + ', validation ' + F.n_val + ') and ' + F.n_test + ' test leaves; folds ' + F.fold_sizes.join(' / ') + '; no plot on both sides.'); refs(s, R('L2'));
// ---------------- L3
section('Step L3 – Pre-processing', 'Savitzky–Golay smoothing, 400–2400 nm, first derivative, 5-nm bands'); card('L3');
s = slide('L3 results: smoothing, derivative and the 1000-nm detector join'); chart(s, 'c09', 0.4, 1.1, 6.2, 2.45); chart(s, 'c10', 0.4, 3.6, 6.2, 2.45); chart(s, 'c08', 6.75, 1.1, 6.15, 4.95);
banner(s, 'Noise removed (residual SD 0.00018); first derivative ready; residual join step of −0.002 handled by excluding FD 995–1005 nm from band selection (DEV-1).'); refs(s, R('L3') + '; Hueni and Bialek (2017)');
// ---------------- L4
section('Step L4 – Spectral indices', '48 published indices and three red-edge parameters'); card('L4');
s = slide('L4 results: index groups and the strongest index of each group'); tbl(s, T.l4groups, 0.4, 1.15, 7.2, [3.4, 1.0, 2.8], 12); chart(s, 'c15', 7.8, 1.1, 5.1, 4.95);
banner(s, '51 features per leaf; the red-edge and pigment indices (RVSI, HI, RR, REP) carry most of the grade information.'); refs(s, R('L4') + '; original index references in sheet L4');
// ---------------- L5.1
section('Step L5.1 – Leaf response to white rust', 'Mean spectra, differences from healthy leaves and correlation with the grade (all leaves)'); card('L5.1');
s = slide('L5.1 results: mean reflectance and first derivative of each grade'); chart(s, 'c11', 0.4, 1.1, 6.2, 4.95); chart(s, 'c12', 6.7, 1.1, 6.2, 4.95);
banner(s, 'With severity: visible reflectance rises, NIR falls, SWIR rises; the red-edge peak drops and moves to shorter wavelengths (REP ' + F.l51.REP_by_grade['0'].toFixed(1) + ' → ' + F.l51.REP_by_grade['9'].toFixed(1) + ' nm).'); refs(s, R('L5.1'));
s = slide('L5.1 results: difference from grade 0 and correlation with the grade'); chart(s, 'c13', 0.4, 1.1, 6.2, 4.95); chart(s, 'c14', 6.7, 1.1, 6.2, 4.95);
banner(s, 'Largest change in the red edge and green peak; highest |r|: FD ' + F.l51.max_abs_r_FD.toFixed(3) + ' at ' + F.l51.wl_max_r_FD + ' nm; reflectance ' + F.l51.max_abs_r_R.toFixed(3) + ' at ' + F.l51.wl_max_r_R + ' nm.'); refs(s, R('L5.1'));
s = slide('L5.1 results: is the response the same in every stratum?'); chart(s, 'c16', 0.4, 1.1, 6.2, 4.95); chart(s, 'c17', 6.7, 1.1, 6.2, 4.95);
banner(s, 'The red-edge derivative responds in every leaf position, stage, variety and date; correlations are lower within single dates (narrower grade range).'); refs(s, R('L5.1'));
// ---------------- L5.2
section('Step L5.2 – Optimal wavelengths', 'R² maps → effective ranges → SHAP → CARS (training leaves)'); card('L5.2');
s = slide('L5.2 results: NDSI and RSI R² maps with the grade');
s.addImage({ path: path.join(__dirname, 'fig', 'h01_ndsi.png'), x: 0.5, y: 1.1, w: 5.4, h: 4.7, sizing: { type: 'contain', w: 5.4, h: 4.7 }, altText: 'NDSI R2 map' });
s.addImage({ path: path.join(__dirname, 'fig', 'h02_rsi.png'), x: 6.0, y: 1.1, w: 5.4, h: 4.7, sizing: { type: 'contain', w: 5.4, h: 4.7 }, altText: 'RSI R2 map' });
tbl(s, T.ranges.map(r => [r[0], r[3]]), 11.55, 1.2, 1.4, [0.9, 0.5], 9);
banner(s, 'Max R² ' + F.l52.maxR2_ndsi.toFixed(3) + ' (< 0.5) → top-5% rule; ' + F.l52.n_eff + ' bands in both maps (white contour = threshold).'); refs(s, R('L5.2'));
s = slide('L5.2 results: SHAP importance and the number of PLS components'); chart(s, 'c21', 0.4, 1.1, 6.2, 4.95); chart(s, 'c22', 6.7, 1.1, 6.2, 4.95);
banner(s, F.l52.n_cand + ' candidate bands → ' + F.l52.n_shap + ' kept by SHAP (top 40%); MCCV chose ' + F.l52.ncomp + ' PLS components.'); refs(s, R('L5.2'));
s = slide('L5.2 results: CARS iterations and the optimal wavelengths'); chart(s, 'c23', 0.4, 1.1, 4.2, 2.45); chart(s, 'c24', 0.4, 3.6, 4.2, 2.45); chart(s, 'c25', 4.75, 1.1, 8.15, 4.95);
banner(s, F.l52.n_ow + ' optimal wavelengths at CARS iteration ' + F.l52.cars_it + ' (GroupKFold RMSE ' + F.l52.cars_rmse.toFixed(3) + '): green peak, red edge, NIR/water and SWIR derivative bands.'); refs(s, R('L5.2'));
// ---------------- L5.3
section('Step L5.3 – Leaf indices', 'Best NDSI, RSI and the White Rust Index (WRI)'); card('L5.3');
s = slide('L5.3 results: WRI search and WRI by grade'); chart(s, 'c27', 0.4, 1.1, 4.3, 3.4); tbl(s, T.wri_w, 0.5, 4.6, 4.1, [0.6, 0.8, 0.8, 0.8, 1.1], 10); chart(s, 'c26', 4.9, 1.1, 8.0, 4.95);
banner(s, 'WRI = NDSI(' + F.l53.wri.l1 + ', ' + F.l53.wri.l2 + '), r = ' + F.l53.wri.r.toFixed(3) + ' (w = 0 was best); best NDSI/RSI pair (' + F.l53.ndsi[0] + ', ' + F.l53.ndsi[1] + ') R² ' + F.l53.ndsi[2].toFixed(3) + '.'); refs(s, R('L5.3'));
// ---------------- L5.4
section('Step L5.4 – Redundancy filter and ReliefF', 'Top five indices per task (VI)'); card('L5.4');
s = slide('L5.4 results: ReliefF weights and the leaf VI'); chart(s, 'c28a', 0.4, 1.1, 4.1, 3.3); chart(s, 'c28b', 4.6, 1.1, 4.1, 3.3); chart(s, 'c28c', 8.8, 1.1, 4.1, 3.3); tbl(s, T.vi, 0.4, 4.5, 12.5, [1.0, 3.8, 3.8, 3.9], 11);
banner(s, '54 indices → ' + F.l54.n_kept + ' after the |r| ≥ 0.95 filter; RSI_best, HI, RR, REP and RVSI lead for detection and grading.'); refs(s, R('L5.4'));
// ---------------- L5.5
section('Step L5.5 – VIF and the leaf DSF', 'Pool of 32 OW + 5 VI per task, reduced until all VIF < 10'); card('L5.5');
s = slide('L5.5 results: the leaf disease-specific feature set'); tbl(s, T.dsf, 0.4, 1.15, 7.4, [0.7, 0.9, 5.8], 11); chart(s, 'c29', 8.0, 1.1, 4.9, 4.95);
banner(s, '14 features per task (13 shared first-derivative bands + RR or RARSa); all VIF < 10.'); refs(s, R('L5.5'));
// ---------------- L5.6
section('Step L5.6 – Separability of the grades', 'Jeffries–Matusita distance on the task-B DSF'); card('L5.6');
s = slide('L5.6 results: JM distance between grades'); heat(s, T.jm.slice(1).map(r => r.slice(1).map(Number)), T.jm[0].slice(1), 0.6, 1.6, 0.78, 0.55, 2, [192, 57, 43], 'JM matrix (0 = identical, 2 = separable)', v => v.toFixed(2));
chart(s, 'c30', 6.4, 1.1, 6.5, 4.95); banner(s, 'Grade 0 vs 9 nearly separable (JM 1.91); neighbouring grades overlap (JM 0.43–0.79): exact-grade errors will be between neighbours.'); refs(s, R('L5.6'));
// ---------------- L5.7
section('Step L5.7 – Principal component analysis', 'Structure of the leaf spectra (all leaves)'); card('L5.7');
s = slide('L5.7 results: variance, loadings and scores'); chart(s, 'c18', 0.4, 1.1, 4.2, 2.45); chart(s, 'c19', 0.4, 3.6, 4.2, 2.45); chart(s, 'c20', 4.75, 1.1, 8.15, 4.95);
banner(s, 'PC1 + PC2 = ' + (D.charts.c18.series[1].values[1]).toFixed(1) + '% of the variance; grades overlap strongly and shift gradually.'); refs(s, R('L5.7'));
// ---------------- L6
if (ST.L6) {
  section('Step L6 – Leaf models', 'SVM, RF, k-NN, PLS (SFFS + grid search) and five networks on the leaf DSF'); card('L6');
  s = slide('L6 results: SFFS and grid search of the ML models'); if (T.ml) tbl(s, T.ml, 0.4, 1.15, 12.5, [0.7, 1.0, 1.5, 7.2, 2.1], 10.5); banner(s, 'Each model keeps its own SFFS subset of the 14 DSF features; tuned with the same GroupKFold(3) folds.'); refs(s, R('L6'));
  s = slide('L6 results: SFFS paths (inner GroupKFold(3) score by number of features)'); chart(s, 'c31a', 0.4, 1.1, 4.1, 4.95); chart(s, 'c31b', 4.6, 1.1, 4.1, 4.95); chart(s, 'c31c', 8.8, 1.1, 4.1, 4.95);
  banner(s, 'Scores level off after about 5–10 features: more features add little.'); refs(s, R('L6'));
  s = slide('L6 results: network training (validation score by epoch)'); chart(s, 'c32a', 0.4, 1.1, 4.1, 3.0); chart(s, 'c32b', 4.6, 1.1, 4.1, 3.0); chart(s, 'c32c', 8.8, 1.1, 4.1, 3.0); if (T.dl) tbl(s, T.dl, 0.4, 4.2, 12.5, [1.0, 3.0, 2.5, 2.5, 3.5], 10);
  banner(s, 'Early stopping (patience 60) on the 11 validation plots; the epoch with the best validation OA (RMSE for task C) is kept.'); refs(s, R('L6'));
  if (D.charts.c40a) { s = slide('L6 check: stability of the SFFS selection'); chart(s, 'c40a', 0.4, 1.1, 4.1, 4.95); chart(s, 'c40b', 4.6, 1.1, 4.1, 4.95); chart(s, 'c40c', 8.8, 1.1, 4.1, 4.95);
    banner(s, 'Features chosen in most repeated divisions are stable; rarely chosen ones depend on the fold division.'); refs(s, 'Tian et al. (2021); Pudil et al. (1994)'); }
}
// ---------------- L7
if (ST.L7) {
  section('Step L7 – Test metrics', F.n_test + ' test leaves of 15 plots, predicted once'); card('L7');
  s = slide('L7 results: main metric of every model'); chart(s, 'c33a', 0.4, 1.1, 4.1, 4.95); chart(s, 'c33b', 4.6, 1.1, 4.1, 4.95); chart(s, 'c33c', 8.8, 1.1, 4.1, 4.95);
  banner(s, 'Best: task A ' + F.best.A + ', task B ' + F.best.B + ', task C ' + F.best.C + ' (95% CIs in the Excel sheet L7).'); refs(s, R('L7'));
  s = slide('L7 results: task A – detection of diseased leaves'); tbl(s, T.metA, 0.4, 1.15, 7.0, [1.6, 0.9, 0.9, 0.9, 0.9, 0.9, 0.9], 10); heat(s, T.confA.m, T.confA.labels, 0.6, 4.4, 1.15, 0.42, Math.max(...T.confA.m.flat()), [47, 93, 138], 'Confusion matrix (' + F.best.A + ')');
  chart(s, 'c36', 7.6, 1.1, 5.3, 4.95); banner(s, ST.L7.result[0]); refs(s, R('L7'));
  s = slide('L7 results: task B – six grades'); tbl(s, T.metB, 0.4, 1.15, 5.8, [1.6, 0.8, 0.8, 0.9, 0.85, 0.85], 10); heat(s, T.confB.m, T.confB.labels, 0.5, 4.2, 0.62, 0.27, Math.max(...T.confB.m.flat()), [47, 93, 138], 'Confusion matrix (' + F.best.B + ')');
  chart(s, 'c35', 6.4, 1.1, 6.5, 4.95); banner(s, ST.L7.result[1]); refs(s, R('L7') + '; Cross et al. (2024)');
  s = slide('L7 results: task C – grade as a number'); tbl(s, T.metC, 0.4, 1.15, 5.6, [1.6, 1.0, 1.0, 1.0, 1.0], 11); chart(s, 'c37', 6.2, 1.1, 6.7, 4.95); banner(s, ST.L7.result[2]); refs(s, R('L7'));
  s = slide('L7 results: performance by leaf position, stage, date and variety'); chart(s, 'c38a', 0.4, 1.1, 4.1, 4.95); chart(s, 'c38b', 4.6, 1.1, 4.1, 4.95); chart(s, 'c38c', 8.8, 1.1, 4.1, 4.95);
  banner(s, 'Strata show where the pooled model works best and where it is weak (e.g. single dates with a narrow grade range).'); refs(s, R('L7'));
  s = slide('L7 results: low-severity check'); chart(s, 'c39', 0.4, 1.1, 7.2, 4.95); tbl(s, T.low, 7.8, 1.2, 5.1, [0.5, 1.0, 2.1, 0.7, 0.8], 10); banner(s, ST.L7.result[3]); refs(s, 'Abdulridha et al. (2023); Deng et al. (2024); ' + R('L7'));
}
// ---------------- L8
if (ST.L8) {
  section('Step L8 – Covariate baseline', 'What does the leaf spectrum add to time, crop and weather?'); card('L8');
  s = slide('L8 results: M0, M1, M2 and the gains'); chart(s, 'c41', 0.4, 1.1, 6.2, 3.2); tbl(s, T.l8, 0.4, 4.4, 6.2, [1.6, 0.9, 1.0, 1.0, 0.85, 0.85], 9.5); chart(s, 'c42', 6.75, 1.1, 6.15, 4.95);
  banner(s, ST.L8.mydata.join(' ').slice(0, 220)); refs(s, R('L8') + '; Zhang et al. (2014a)');
  if (D.charts.c43) { s = slide('L8 results: covariate importance and bootstrap intervals'); chart(s, 'c43', 0.4, 1.1, 6.2, 4.95); tbl(s, T.l8ci, 6.8, 1.2, 6.1, [0.8, 1.2, 1.5, 2.6], 11); banner(s, ST.L8.result[0]); refs(s, R('L8')); }
}
// ---------------- L9
if (ST.L9) {
  section('Step L9 – Leaf–canopy link', 'Leaf features tested on the UAV hyperspectral plot spectra of 24 Feb 2026'); card('L9');
  s = slide('L9 results: leaf and canopy spectra'); chart(s, 'c44', 0.4, 1.1, 6.2, 4.95); chart(s, 'c45', 6.7, 1.1, 6.2, 4.95); banner(s, ST.L9.mydata[1]); refs(s, R('L9'));
  s = slide('L9 results: leaf indices computed from the UAV spectra'); chart(s, 'c46', 0.4, 1.1, 5.0, 4.95); tbl(s, T.l9, 5.6, 1.15, 7.3, [1.3, 1.2, 1.5, 1.0, 1.1, 1.2], 10.5); banner(s, ST.L9.result[0]); refs(s, R('L9'));
}
section('Step L10 – Pre-symptomatic leaves', 'Not applicable to 2025-26'); card('L10');
// ---------------- checks, deviations, conclusions, references
section('Cross-checks, deviations and conclusions');
s = slide('How every step was cross-checked');
bul(s, ['Excel formulas recompute the grade × date counts, split counts, mean spectra (AVERAGEIFS), band correlations (CORREL) and every test metric (confusion matrices with COUNTIFS; OA, kappa, macro-F1, sensitivity, specificity, within-one, QWK, R², RMSE, RPD) from the raw cells; the Checks sheet compares them with the Python values (all PASS).',
  'Leakage checks: no test-plot leaf in training; validation plots inside the training part; selection (L5.2–L5.6) and scalers fitted on training leaves only; test leaves predicted once per model.',
  'Selection checks: the WRI search was repeated and gave the same best index; no first-derivative band inside the 995–1005 nm detector-join guard was selected; all DSF VIF < 10; JM within 0–2.',
  'Every point estimate lies inside its plot-bootstrap 95% CI; the weather window ends the day before sampling (no look-ahead).'], { x: 0.4, y: 1.15, w: 12.5, h: 4.8, fontSize: 14 });
refs(s, 'Efron and Tibshirani (1993); Sokolova and Lapalme (2009); Cohen (1960).');
s = slide('Deviations from the methodology and why'); tbl(s, T.dev, 0.4, 1.15, 12.5, [0.9, 1.0, 4.9, 5.7], 11); refs(s, 'Hueni and Bialek (2017); methodology 2026-27, Part L.');
if (ST.L7) {
  s = slide('Main findings');
  const fnd = [ST['L5.1'].result[0], ST['L5.2'].result[0], 'WRI = NDSI(' + F.l53.wri.l1 + ', ' + F.l53.wri.l2 + ') on the NIR shoulder; RSI_best, HI, RR, REP and RVSI are the strongest indices; leaf DSF = 13 first-derivative bands + one index.',
    ST.L7.result[0], ST.L7.result[1], ST.L7.result[2]].concat(ST.L8 ? [ST.L8.result[0]] : []).concat(ST.L9 ? [ST.L9.result[0]] : []);
  bul(s, fnd, { x: 0.4, y: 1.15, w: 12.5, h: 4.9, fontSize: 13.5 }); refs(s, 'Mandal et al. (2023); Cross et al. (2024); Ma et al. (2026); Liu et al. (2026).');
}
s = slide('Findings compared with the literature'); tbl(s, T.lit, 0.4, 1.12, 12.5, [2.0, 3.6, 3.6, 3.3], 9.5); refs(s, T.lit.slice(1).map(r => r[0]).join('; '));
const RL = D.refs; const half = Math.ceil(RL.length / 2);
[RL.slice(0, half), RL.slice(half)].forEach((part, k) => { s = slide('References (' + (k + 1) + '/2)'); s.addText(part.map((t, i) => ({ text: t, options: { breakLine: i < part.length - 1, paraSpaceAfter: 2 } })), { x: 0.4, y: 1.1, w: 12.5, h: 5.85, fontSize: 8.5, fontFace: 'Calibri', color: '1A1A1A', valign: 'top', isTextBox: true, fit: 'shrink' }); });
pres.writeFile({ fileName: OUT }).then(async () => { await applyTheme(OUT, THEME); console.log('written', OUT); });
