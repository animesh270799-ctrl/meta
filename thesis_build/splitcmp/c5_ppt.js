// Slides: comparison of the validation designs LORO vs grouped 70:30 vs grouped 80:20 (ASD leaf data 2025-26).
// Every table and figure of the Word report appears here with the same number (checked at the end).
const pptxgen = require('pptxgenjs'); const fs = require('fs');
const { applyTheme } = require(process.env.SKILL_DIR + '/scripts/apply_theme.js');
const B = __dirname + '/'; const D = JSON.parse(fs.readFileSync(B + 'out/ppt_data.json', 'utf8')); const FG = B + 'fig/';
const OUT = B + '../outputs/ASD_2025-26_validation_comparison_LORO_70-30_80-20.pptx';
const THEME = { name: 'Validation design comparison', headFontFace: 'Cambria', bodyFontFace: 'Calibri',
  colors: { dk1: '1B2A1E', lt1: 'FFFFFF', dk2: '2C5F2D', lt2: 'EEF3E8', accent1: '2C5F2D', accent2: '97BC62', accent3: '7030A0', accent4: 'C98A00', accent5: 'C62828', accent6: '1565C0', hlink: '1565C0', folHlink: '7030A0' } };
const pres = new pptxgen(); pres.layout = 'LAYOUT_WIDE'; pres.theme = { headFontFace: THEME.headFontFace, bodyFontFace: THEME.bodyFontFace };
pres.title = 'Validation design comparison: LORO vs 70:30 vs 80:20'; pres.author = 'Animesh Panda';
pres.defineSlideMaster({ title: 'TITLE', background: { color: '2C5F2D' }, objects: [
  { placeholder: { options: { name: 'title', type: 'title', x: 0.7, y: 1.8, w: 11.9, h: 1.8, fontSize: 38, bold: true, color: 'FFFFFF', fontFace: 'Cambria', valign: 'middle' }, text: '' } },
  { placeholder: { options: { name: 'body', type: 'body', x: 0.7, y: 3.8, w: 11.9, h: 2.2, fontSize: 18, color: 'EEF3E8', fontFace: 'Calibri', valign: 'top' }, text: '' } }] });
pres.defineSlideMaster({ title: 'SECTION', background: { color: '1B2A1E' }, objects: [
  { placeholder: { options: { name: 'title', type: 'title', x: 0.7, y: 2.6, w: 11.9, h: 1.3, fontSize: 38, bold: true, color: 'FFFFFF', fontFace: 'Cambria' }, text: '' } },
  { placeholder: { options: { name: 'body', type: 'body', x: 0.7, y: 3.9, w: 11.9, h: 1.2, fontSize: 18, color: '97BC62', fontFace: 'Calibri' }, text: '' } }] });
pres.defineSlideMaster({ title: 'CONTENT', background: { color: 'FFFFFF' }, margin: [0.4, 0.5, 0.5, 0.5], objects: [
  { placeholder: { options: { name: 'title', type: 'title', x: 0.5, y: 0.25, w: 12.3, h: 0.8, fontSize: 26, bold: true, color: '2C5F2D', fontFace: 'Cambria', valign: 'middle' }, text: '' } },
  { text: { text: 'White rust of Indian mustard | Validation design comparison, ASD leaf spectra 2025-26 | ICAR-IARI', options: { x: 0.5, y: 7.05, w: 9.5, h: 0.3, fontSize: 10, color: '6B7B6E', fontFace: 'Calibri' } } }],
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
function interpNotes(key) { return ''; }
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


const SU = D.summary, LABS = Object.keys(SU);
let s = pres.addSlide({ masterName: 'TITLE' });
s.addText('Does a 70:30 or 80:20 split improve the accuracy?', { placeholder: 'title' });
s.addText('Leave-one-replication-out (LORO) vs grouped 70:30 vs grouped 80:20 hold-out – leaf-level white rust models, ASD spectra, IARI 2025-26\nAnimesh Panda | Ph.D. Agricultural Physics | ICAR-IARI, New Delhi', { placeholder: 'body' });
s = slide('Answer in short');
LABS.forEach((l, i) => card(s, 0.5 + i * 6.25, 1.25, 6.05, 4.4, l + ' vs LORO', SU[l].verdict + '\n\n' + SU[l].summary_sentence.split(' ' + SU[l].verdict)[0], i ? 'C55A11' : '2E75B6', i ? 'FBE5D6' : 'DDEBF7', 14));
bullets(s, ['LORO tests all 2330 leaves once and follows the replications → main accuracy estimate.', 'Hold-out models are deployable models; read their accuracy with the split-to-split range.'], 0.5, 5.8, 12.3, 1.1, 15);
sec('1  Validation designs', 'Split types in disease studies; the three designs; train : validation : test');
tableSlides('splittypes', 'Types of split used in plant-disease studies');
figSlide('designs', 'The three designs on the field layout');
tableSlides('designs', 'The three designs');
tableSlides('balance', 'Grade balance of the 70:30 and 80:20 splits');
tableSlides('valroles', 'Which models need train : validation : test');
tableSlides('dlparts', 'Train : validation : test parts of the networks');
sec('2  How the designs were compared', 'Five steps');
['c_side', 'c_pair', 'c_rep', 'c_leak', 'c_ov'].forEach(k => {
  const t = TABS[k]; SHOWN_T.add(k); const r = Object.fromEntries(t.rows.slice(1).map(x => [x[0], x[1]]));
  const s = slide(t.rows[0][1], t.caption);
  card(s, 0.5, 1.15, 6.05, 2.5, 'Concept', r['Concept'], '2C5F2D', 'EEF3E8', 13); card(s, 6.75, 1.15, 6.05, 2.5, 'Why', r['Why (justification)'], '1565C0', 'E3F2FD', 13);
  card(s, 0.5, 3.8, 6.05, 2.6, 'How with my data', r['How with my data'], 'C98A00', 'FFF6E0', 13); card(s, 6.75, 3.8, 6.05, 2.6, 'Papers / output', r['What papers used'] + '\n\nOutput: ' + r['Output → next step'], '7030A0', 'F3E5F5', 13);
  s.addText('Table ' + t.number + ' (step card in the report).', { x: 0.5, y: 6.5, w: 12.3, h: 0.4, fontSize: 10.5, italic: true, color: '6B7B6E', isTextBox: true });
});
sec('3  Results');
figSlide('side', '1. All models side by side');
tableSlides('side', 'Main metric of every model under each design', null, 15);
tableSlides('best', 'Best model of each design');
if (FIGS.pair) { figSlide('pair', '2. Same test leaves (paired comparison)', null, LABS.map(l => l + ': ' + SU[l].summary_sentence.split(' ' + SU[l].verdict)[0]).join('\n\n'));
  LABS.forEach(l => { const k = 'pair' + l.replace(':', ''); if (TABS[k]) tableSlides(k, 'Paired comparison, ' + l, null, 15); }); }
if (FIGS.rep) { figSlide('rep', '3. How much does the answer depend on the split?'); tableSlides('rep', 'Split-to-split variability');
  s = slide('Split-to-split variability – what it means'); bullets(s, LABS.map(l => SU[l].repeat_sentence).filter(x => x), 0.5, 1.3, 12.3, 5.4, 15); }
if (FIGS.leak) { figSlide('leak', '4. Leakage check: splitting leaves instead of plots', null, LABS.map(l => SU[l].leak_sentence).filter(x => x).join('\n\n')); tableSlides('leak', 'Grouped vs random leaf-level splits'); }
figSlide('ov', '5. Do the designs choose the same features?'); tableSlides('sets', 'Features chosen in each training set', null, 7);
if (TABS.gains) tableSlides('gains', 'Gain of the spectra over the covariates under each design');
sec('4  Discussion and conclusions');
s = slide('Is the accuracy improving?'); LABS.forEach((l, i) => card(s, 0.5, 1.2 + i * 2.75, 12.3, 2.6, l, SU[l].answer, i ? 'C55A11' : '2E75B6', i ? 'FBE5D6' : 'DDEBF7', 12));
s = slide('Which design to report');
bullets(s, ['Main accuracy estimate: LORO with nested, plot-grouped inner cross-validation (Varma and Simon, 2006; Cawley and Talbot, 2010).', 'Single hold-out splits are noisy with 9–15 test plots (Kohavi, 1995; Vabalas et al., 2019); report them with the repeated-split range.',
  'Random leaf splits are inflated by plot leakage (Roberts et al., 2017; Kattenborn et al., 2022) – many published accuracies are random-split values.', 'Strongest test: an independent season or site (2026-27, Bharatpur).'], 0.5, 1.3, 12.3, 5.4, 18);
D.tables.forEach(t => { if (!SHOWN_T.has(t.key)) tableSlides(t.key, 'Table ' + t.number); });
D.figures.forEach(f => { if (!SHOWN_F.has(f.key)) figSlide(f.key, 'Figure ' + f.number); });
const nr = Math.ceil(D.refs.length / 22);
for (let i = 0; i < nr; i++) { s = slide('References' + (nr > 1 ? ' (' + (i + 1) + '/' + nr + ')' : '')); const rr = D.refs.slice(i * 22, (i + 1) * 22);
  s.addText(rr.map((r, j) => ({ text: r, options: { breakLine: j < rr.length - 1 } })), { x: 0.5, y: 1.15, w: 12.3, h: 5.8, fontSize: 9.5, color: '1B2A1E', valign: 'top', paraSpaceAfter: 2, isTextBox: true, fit: 'shrink' }); }
console.log('tables shown', SHOWN_T.size, 'of', D.tables.length, '| figures shown', SHOWN_F.size, 'of', D.figures.length);
pres.writeFile({ fileName: OUT }).then(async () => { await applyTheme(OUT, THEME); console.log('saved', OUT); });
