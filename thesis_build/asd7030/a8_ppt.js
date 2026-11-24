// Seminar deck: ASD leaf spectra 2025-26 – methodology, results (Objectives 1-3), discussion. Native charts and tables; data from ppt_data.json.
const pptxgen = require('pptxgenjs');
const path = require('path'); const fs = require('fs');
const { applyTheme } = require(process.env.SKILL_DIR + '/scripts/apply_theme.js');
const B = __dirname + '/'; const DATA = JSON.parse(fs.readFileSync(B + 'data/ppt_data.json', 'utf8')); const FG = B + 'fig/'; const MF = B + '../method3/fig/';
const OUT = B + '../outputs/ASD_2025-26_70-30_leaf_analysis_seminar.pptx';
const THEME = { name: 'White rust leaf spectra', headFontFace: 'Cambria', bodyFontFace: 'Calibri',
  colors: { dk1: '1B2A1E', lt1: 'FFFFFF', dk2: '2C5F2D', lt2: 'EEF3E8', accent1: '2C5F2D', accent2: '97BC62', accent3: '7030A0', accent4: 'C98A00', accent5: 'C62828', accent6: '1565C0', hlink: '1565C0', folHlink: '7030A0' } };
const pres = new pptxgen(); pres.layout = 'LAYOUT_WIDE'; pres.theme = { headFontFace: THEME.headFontFace, bodyFontFace: THEME.bodyFontFace };
pres.title = 'White rust ASD leaf spectra 2025-26'; pres.author = 'Animesh Panda';
const C = pres.SchemeColor; const W = 13.333, H = 7.5;
const GRADE_COLS = ['2E7D32', '9CCC65', 'FDD835', 'FB8C00', 'E53935', '7B1FA2'];
// ---------------- layouts ----------------
pres.defineSlideMaster({ title: 'TITLE', background: { color: '2C5F2D' }, objects: [
  { placeholder: { options: { name: 'title', type: 'title', x: 0.7, y: 2.0, w: 11.9, h: 1.6, fontSize: 40, bold: true, color: 'FFFFFF', fontFace: 'Cambria', valign: 'middle' }, text: '' } },
  { placeholder: { options: { name: 'body', type: 'body', x: 0.7, y: 3.8, w: 11.9, h: 2.2, fontSize: 18, color: 'EEF3E8', fontFace: 'Calibri', valign: 'top' }, text: '' } }] });
pres.defineSlideMaster({ title: 'SECTION', background: { color: '1B2A1E' }, objects: [
  { placeholder: { options: { name: 'title', type: 'title', x: 0.7, y: 2.6, w: 11.9, h: 1.3, fontSize: 38, bold: true, color: 'FFFFFF', fontFace: 'Cambria' }, text: '' } },
  { placeholder: { options: { name: 'body', type: 'body', x: 0.7, y: 3.9, w: 11.9, h: 1.2, fontSize: 18, color: '97BC62', fontFace: 'Calibri' }, text: '' } }] });
pres.defineSlideMaster({ title: 'CONTENT', background: { color: 'FFFFFF' }, margin: [0.4, 0.5, 0.5, 0.5], objects: [
  { placeholder: { options: { name: 'title', type: 'title', x: 0.5, y: 0.25, w: 12.3, h: 0.8, fontSize: 28, bold: true, color: '2C5F2D', fontFace: 'Cambria', valign: 'middle' }, text: '' } },
  { text: { text: 'White rust of Indian mustard | ASD leaf spectra 2025-26 | ICAR-IARI', options: { x: 0.5, y: 7.05, w: 9, h: 0.3, fontSize: 10, color: '6B7B6E', fontFace: 'Calibri' } } }],
  slideNumber: { x: 12.3, y: 7.05, w: 0.6, h: 0.3, fontSize: 10, color: '6B7B6E' } });
// ---------------- helpers ----------------
let SEC = '';
function sec(title, sub) { SEC = title; pres.addSection({ title }); const s = pres.addSlide({ masterName: 'SECTION', sectionTitle: title }); s.addText(title, { placeholder: 'title' }); if (sub) s.addText(sub, { placeholder: 'body' }); return s; }
function slide(title, notes) { const s = pres.addSlide({ masterName: 'CONTENT', sectionTitle: SEC }); s.addText(title, { placeholder: 'title' }); if (notes) s.addNotes(notes); return s; }
function bullets(s, items, x, y, w, h, fs = 15) {
  s.addText(items.map((t, i) => (typeof t === 'string' ? { text: t, options: { bullet: true, breakLine: i < items.length - 1 } } : { text: t.text, options: Object.assign({ bullet: { indent: 18 }, indentLevel: 1, breakLine: i < items.length - 1 }, t.options || {}) })),
    { x, y, w, h, fontSize: fs, color: '1B2A1E', valign: 'top', paraSpaceAfter: 6, isTextBox: true, fit: 'shrink' });
}
function card(s, x, y, w, h, head, body, col = '2C5F2D', fill = 'EEF3E8', fs = 16) {
  s.addShape(pres.shapes.ROUNDED_RECTANGLE, { x, y, w, h, fill: { color: fill }, line: { color: fill }, rectRadius: 0.08, objectName: 'card' });
  s.addText(head, { x: x + 0.15, y: y + 0.1, w: w - 0.3, h: 0.5, fontSize: 18, bold: true, color: col, isTextBox: true, margin: 0 });
  s.addText(body, { x: x + 0.15, y: y + 0.65, w: w - 0.3, h: h - 0.75, fontSize: fs, color: '1B2A1E', valign: 'top', isTextBox: true, margin: 0, fit: 'shrink' });
}
function img(s, file, x, y, w, h) { s.addImage({ path: file, x, y, w, h, sizing: { type: 'contain', w, h } }); }
function caption(s, t, y = 6.62) { s.addText(t, { x: 0.5, y, w: 12.3, h: 0.35, fontSize: 11, italic: true, color: '6B7B6E', isTextBox: true }); }
const AX = { catAxisLabelColor: '444444', valAxisLabelColor: '444444', catAxisLabelFontFace: '+mn-lt', valAxisLabelFontFace: '+mn-lt', catAxisLabelFontSize: 11, valAxisLabelFontSize: 11,
  valGridLine: { color: 'DDDDDD', size: 0.5 }, catGridLine: { style: 'none' }, titleFontFace: '+mj-lt', titleFontSize: 14, titleColor: '2C5F2D', legendFontFace: '+mn-lt', legendFontSize: 11, dataLabelFontFace: '+mn-lt', dataLabelFontSize: 10 };
function chart(s, type, data, opt) { s.addChart(type, data, Object.assign({}, AX, opt)); }
function tbl(s, rows, x, y, w, colW, fs = 12) {
  const hdr = rows[0].map(c => ({ text: String(c), options: { bold: true, color: 'FFFFFF', fill: { color: '2C5F2D' }, align: 'center', valign: 'middle' } }));
  const body = rows.slice(1).map((r, i) => r.map(c => ({ text: String(c), options: { fill: { color: i % 2 ? 'FFFFFF' : 'F4F7F1' }, valign: 'middle' } })));
  s.addTable([hdr, ...body], { x, y, w, colW, fontSize: fs, fontFace: 'Calibri', color: '1B2A1E', border: { type: 'solid', pt: 0.5, color: 'C9D3C4' }, margin: 0.05, autoPage: false });
}
module.exports = { pres, sec, slide, bullets, card, img, caption, chart, tbl, DATA, FG, MF, GRADE_COLS, OUT, THEME, applyTheme, W, H };
if (require.main === module) { require('./a8_slides.js'); }
