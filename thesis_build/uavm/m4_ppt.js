// Slides: best ASD leaf models applied to the UAV hyperspectral image of 24 Feb 2026 (same theme as the ASD seminar deck).
// Every table and figure of the Word report appears here with the same number (checked at the end).
const pptxgen = require('pptxgenjs'); const fs = require('fs');
const { applyTheme } = require(process.env.SKILL_DIR + '/scripts/apply_theme.js');
const B = __dirname + '/'; const D = JSON.parse(fs.readFileSync(B + 'out/ppt_data.json', 'utf8')); const FG = B + 'fig/';
const OUT = B + '../outputs/UAV_24Feb2026_disease_maps.pptx';
const THEME = { name: 'White rust disease maps', headFontFace: 'Cambria', bodyFontFace: 'Calibri',
  colors: { dk1: '1B2A1E', lt1: 'FFFFFF', dk2: '2C5F2D', lt2: 'EEF3E8', accent1: '2C5F2D', accent2: '97BC62', accent3: '7030A0', accent4: 'C98A00', accent5: 'C62828', accent6: '1565C0', hlink: '1565C0', folHlink: '7030A0' } };
const pres = new pptxgen(); pres.layout = 'LAYOUT_WIDE'; pres.theme = { headFontFace: THEME.headFontFace, bodyFontFace: THEME.bodyFontFace };
pres.title = 'White rust disease maps, UAV hyperspectral image 24 Feb 2026'; pres.author = 'Animesh Panda';
pres.defineSlideMaster({ title: 'TITLE', background: { color: '2C5F2D' }, objects: [
  { placeholder: { options: { name: 'title', type: 'title', x: 0.7, y: 1.8, w: 11.9, h: 1.8, fontSize: 38, bold: true, color: 'FFFFFF', fontFace: 'Cambria', valign: 'middle' }, text: '' } },
  { placeholder: { options: { name: 'body', type: 'body', x: 0.7, y: 3.8, w: 11.9, h: 2.2, fontSize: 18, color: 'EEF3E8', fontFace: 'Calibri', valign: 'top' }, text: '' } }] });
pres.defineSlideMaster({ title: 'SECTION', background: { color: '1B2A1E' }, objects: [
  { placeholder: { options: { name: 'title', type: 'title', x: 0.7, y: 2.6, w: 11.9, h: 1.3, fontSize: 38, bold: true, color: 'FFFFFF', fontFace: 'Cambria' }, text: '' } },
  { placeholder: { options: { name: 'body', type: 'body', x: 0.7, y: 3.9, w: 11.9, h: 1.2, fontSize: 18, color: '97BC62', fontFace: 'Calibri' }, text: '' } }] });
pres.defineSlideMaster({ title: 'CONTENT', background: { color: 'FFFFFF' }, margin: [0.4, 0.5, 0.5, 0.5], objects: [
  { placeholder: { options: { name: 'title', type: 'title', x: 0.5, y: 0.25, w: 12.3, h: 0.8, fontSize: 26, bold: true, color: '2C5F2D', fontFace: 'Cambria', valign: 'middle' }, text: '' } },
  { text: { text: 'White rust of Indian mustard | Disease maps, UAV hyperspectral image of 24 Feb 2026 | ICAR-IARI', options: { x: 0.5, y: 7.05, w: 9.5, h: 0.3, fontSize: 10, color: '6B7B6E', fontFace: 'Calibri' } } }],
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

const MS = D.summary, BEST = MS.best;
let s = pres.addSlide({ masterName: 'TITLE' });
s.addText('Disease maps of white rust from the UAV hyperspectral image of 24 February 2026', { placeholder: 'title' });
s.addText('Plot-level maps from the best 2025-26 ASD models and the UAV-trained check\nAnimesh Panda | Ph.D. Agricultural Physics | ICAR-IARI, New Delhi', { placeholder: 'body' });
s = slide('Summary', D.findings.join('\n'));
bullets(s, D.findings, 0.5, 1.25, 12.3, 5.6, 16);
sec('1  Introduction and methodology', 'Why maps, the seven mapping steps, references');
s = slide('Why disease maps?');
card(s, 0.5, 1.2, 6.05, 5.2, 'Purpose', 'A disease map shows where disease occurs and how severe it is: it guides scouting, targeted spraying and the assessment of resistance trials (Mahlein, 2016; Zhang et al., 2019).\n\nMaps are made by applying a trained model to every mapping unit and are judged against field observations (Congalton, 1991; Foody, 2002).');
card(s, 6.75, 1.2, 6.05, 5.2, 'This report', 'Best ASD models (' + BEST.A.overall + ', ' + BEST.B.overall + ', ' + BEST.C.overall + ') applied to the 48 plots of the 24 Feb image (predictions of the transfer test).\n\nUAV-trained models shown for comparison (out-of-fold).\n\nMapping unit = plot (only plot mean spectra available); pixel maps need the image cube.', '1565C0', 'E3F2FD');
tableSlides('qs', 'Questions answered');
D.methods.forEach(st => {
  const s = slide(st.no + '  ' + st.title, [st.position, 'Likely question: ' + st.question].join('\n\n'));
  card(s, 0.5, 1.15, 4.0, 2.55, 'Concept', st.concept, '2C5F2D', 'EEF3E8', 12);
  card(s, 0.5, 3.8, 4.0, 2.6, 'Why here', st.why, '2C5F2D', 'EEF3E8', 12);
  card(s, 4.65, 1.15, 4.1, 5.25, 'How it is done', st.how.map((h, i) => (i + 1) + '. ' + h).join('\n') + (st.eqs.length ? '\n\n' + st.eqs.map(e => '(' + e[1] + ') ' + e[0].replace(/_\{([^}]*)\}/g, '$1').replace(/\^\{([^}]*)\}/g, '^$1')).join('\n') : ''), '1565C0', 'E3F2FD', 11.5);
  card(s, 8.9, 1.15, 3.9, 2.0, 'What the papers did', st.papers, '7030A0', 'F3E5F5', 11);
  card(s, 8.9, 3.25, 3.9, 1.75, 'Applied to these data', st.mine, 'C98A00', 'FFF6E0', 11);
  card(s, 8.9, 5.1, 3.9, 1.3, 'Output', st.output, '2C5F2D', 'EEF3E8', 11);
  s.addText('Notes: ' + st.notes, { x: 0.5, y: 6.45, w: 12.3, h: 0.55, fontSize: 10.5, italic: true, color: '6B7B6E', isTextBox: true, fit: 'shrink' });
});
sec('2  Maps, accuracy and interpretation');
figSlide('truth', 'True disease map of 24 Feb 2026', 'truth');
figSlide('pred', 'Maps of the best ASD models', 'pred');
figSlide('err', 'Error maps of the best ASD models', 'err');
figSlide('var', 'Score maps: three inputs and UAV-trained', 'var');
figSlide('uav', 'Maps of the UAV-trained models', 'uav');
figSlide('prob', 'Disease score maps', 'prob');
tableSlides('acc', 'Map accuracy', 'err');
tableSlides('moran', 'Spatial autocorrelation of the errors (Moran\'s I)', 'err');
figSlide('grp', 'Errors by block, sowing date and variety', 'group');
['gblock', 'gsowing', 'gvariety'].forEach(k => tableSlides(k, 'Errors by ' + ({ gblock: 'block', gsowing: 'sowing date', gvariety: 'variety' })[k], 'group'));
sec('3  Discussion and conclusions');
s = slide('Discussion');
bullets(s, ['The best ASD maps do not reproduce the true pattern; the UAV-trained detection map does for most plots, mirroring the transfer test (Mahlein, 2016; Bohnenkamp et al., 2019).',
  'Moran\'s I tests whether errors cluster in space; clustered errors point to spatial causes such as illumination or sowing strips (Legendre, 1993; Dormann et al., 2007; Aasen et al., 2018).',
  'Every map is reported with its confusion matrix and error measures (Congalton, 1991; Olofsson et al., 2014).',
  'Next: pixel maps from the image cube with UAV-trained models; severity maps with the 2026-27 subplot data (Zarco-Tejada et al., 2018).'], 0.5, 1.3, 12.3, 5.2, 18);
s = slide('Conclusions'); bullets(s, D.findings, 0.5, 1.3, 12.3, 5.4, 17);
tableSlides('qa', 'Likely questions');
sec('Appendix', 'Plot table and findings');
tableSlides('ptab', 'Appendix A  Plot table');
tableSlides('find', 'Appendix B  Findings');
D.tables.forEach(t => { if (!SHOWN_T.has(t.key)) tableSlides(t.key, 'Table ' + t.number); });
D.figures.forEach(f => { if (!SHOWN_F.has(f.key)) figSlide(f.key, 'Figure ' + f.number); });
s = slide('References');
s.addText(D.refs.map((r, i) => ({ text: r, options: { breakLine: i < D.refs.length - 1 } })), { x: 0.5, y: 1.15, w: 12.3, h: 5.8, fontSize: 9, color: '1B2A1E', valign: 'top', paraSpaceAfter: 2, isTextBox: true, fit: 'shrink' });
console.log('tables shown', SHOWN_T.size, 'of', D.tables.length, '| figures shown', SHOWN_F.size, 'of', D.figures.length);
pres.writeFile({ fileName: OUT }).then(async () => { await applyTheme(OUT, THEME); console.log('saved', OUT); });
