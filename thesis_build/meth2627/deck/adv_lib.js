// Helpers for the advisory-committee deck: Times New Roman, 14 pt body text, native shapes for flow charts.
const pptxgen = require('pptxgenjs');
const F = 'Times New Roman', FS = 14;
const C = { dk: '1B2A1E', g: '2C5F2D', g2: '4E8B3A', lt: 'EEF3E8', blue: '1F4E79', lblue: 'E3EDF7', purple: '5B2C83', lpurple: 'EFE7F6', red: '9C2A2A', lred: 'F9E7E7',
  gold: '8A6100', lgold: 'FFF4D9', grey: '595959', lgrey: 'F2F2F2', teal: '1D6B6B', lteal: 'E2F1F1', white: 'FFFFFF' };
const THEME = { name: 'White rust advisory committee', headFontFace: F, bodyFontFace: F,
  colors: { dk1: '1B2A1E', lt1: 'FFFFFF', dk2: '2C5F2D', lt2: 'EEF3E8', accent1: '2C5F2D', accent2: '1F4E79', accent3: '5B2C83', accent4: '8A6100', accent5: '9C2A2A', accent6: '1D6B6B', hlink: '1F4E79', folHlink: '5B2C83' } };
const pres = new pptxgen(); pres.layout = 'LAYOUT_WIDE'; pres.theme = { headFontFace: F, bodyFontFace: F };
pres.title = 'AI-based multimodal UAV sensing of white rust in mustard: objectives, data collection and methodology'; pres.author = 'Animesh Panda';
pres.defineSlideMaster({ title: 'TITLE', background: { color: '1E3A1F' }, objects: [
  { placeholder: { options: { name: 'title', type: 'title', x: 0.8, y: 1.5, w: 11.7, h: 1.9, fontSize: 36, bold: true, color: 'FFFFFF', fontFace: F, valign: 'middle', align: 'center' }, text: '' } },
  { placeholder: { options: { name: 'body', type: 'body', x: 0.8, y: 3.6, w: 11.7, h: 2.8, fontSize: 18, color: 'E8F0E2', fontFace: F, valign: 'top', align: 'center' }, text: '' } }] });
pres.defineSlideMaster({ title: 'CONTENT', background: { color: 'FFFFFF' }, margin: [0.3, 0.5, 0.5, 0.5], objects: [
  { rect: { x: 0, y: 0, w: 13.333, h: 0.12, fill: { color: '2C5F2D' } } },
  { placeholder: { options: { name: 'title', type: 'title', x: 0.45, y: 0.22, w: 10.0, h: 0.78, fontSize: 26, bold: true, color: '1E3A1F', fontFace: F, valign: 'middle' }, text: '' } },
  { line: { x: 0.45, y: 1.03, w: 12.43, h: 0, line: { color: 'B7C9AE', width: 1 } } },
  { text: { text: 'Animesh Panda | Ph.D. (Agricultural Physics) | ICAR-IARI, New Delhi | Advisory Committee Meeting', options: { x: 0.45, y: 7.08, w: 10, h: 0.3, fontSize: 10, color: '6B7B6E', fontFace: F } } }],
  slideNumber: { x: 12.35, y: 7.08, w: 0.6, h: 0.3, fontSize: 10, color: '6B7B6E', fontFace: F } });
let SEC = '';
function S(title, tag, notes) {
  const s = pres.addSlide({ masterName: 'CONTENT', sectionTitle: SEC }); s.addText(title, { placeholder: 'title' });
  if (tag) s.addText(tag, { x: 10.5, y: 0.3, w: 2.4, h: 0.6, fontSize: 14, italic: true, color: C.g2, fontFace: F, align: 'right', valign: 'middle', isTextBox: true, margin: 0 });
  if (notes) s.addNotes(notes); return s;
}
function sec(t) { SEC = t; pres.addSection({ title: t }); }
// rich text: '**bold**' segments inside strings
function rich(str, base = {}) {
  const out = []; str.split(/(\*\*[^*]+\*\*)/).forEach(p => { if (!p) return; if (p.startsWith('**')) out.push({ text: p.slice(2, -2), options: Object.assign({}, base, { bold: true }) }); else out.push({ text: p, options: Object.assign({}, base) }); });
  return out;
}
function T(s, text, x, y, w, h, o = {}) {
  const runs = typeof text === 'string' ? rich(text) : text;
  s.addText(runs, Object.assign({ x, y, w, h, fontFace: F, fontSize: FS, color: C.dk, valign: 'top', isTextBox: true, margin: 0.04 }, o));
}
// bullets: string ('**lead** rest' allowed) or {t, lvl}
function BL(s, items, x, y, w, h, o = {}) {
  const runs = [];
  items.forEach((it, i) => {
    const t = typeof it === 'string' ? it : it.t, lvl = typeof it === 'string' ? 0 : (it.lvl || 0), last = i === items.length - 1;
    const parts = rich(t); const bo = { bullet: lvl ? { indent: 16, characterCode: '2013' } : { indent: 16 }, indentLevel: lvl, paraSpaceAfter: o.ps === undefined ? 4 : o.ps };
    parts.forEach((p, j) => { const op = Object.assign({}, j === 0 ? bo : {}, p.options); if (p.options.bold) op.color = o.lead || C.g; if (j === parts.length - 1 && !last) op.breakLine = true; runs.push({ text: p.text, options: op }); });
  });
  s.addText(runs, Object.assign({ x, y, w, h, fontFace: F, fontSize: FS, color: C.dk, valign: 'top', isTextBox: true, margin: 0.05 }, o.box || {}));
}
function box(s, x, y, w, h, head, body, col = C.g, fill = C.lt, o = {}) {
  s.addShape(o.shape || pres.shapes.ROUNDED_RECTANGLE, { x, y, w, h, fill: { color: fill }, line: { color: col, width: o.lw || 1.25 }, rectRadius: 0.06 });
  const runs = [];
  if (head) runs.push({ text: head, options: { bold: true, color: col, breakLine: !!body } });
  if (body) { const L = Array.isArray(body) ? body : [body]; L.forEach((t, i) => rich(t).forEach((p, j, a) => runs.push({ text: p.text, options: Object.assign({}, p.options, j === a.length - 1 && i < L.length - 1 ? { breakLine: true } : {}) }))); }
  s.addText(runs, { x: x + 0.04, y: y + 0.02, w: w - 0.08, h: h - 0.04, fontFace: F, fontSize: o.fs || FS, color: C.dk, align: o.align || 'center', valign: o.valign || 'middle', isTextBox: true, margin: 0.04 });
}
function arr(s, x1, y1, x2, y2, col = '595959', w = 1.5) {
  const o = { x: Math.min(x1, x2), y: Math.min(y1, y2), w: Math.abs(x2 - x1), h: Math.abs(y2 - y1), line: { color: col, width: w, endArrowType: 'triangle' } };
  if (x2 < x1) o.flipH = true; if (y2 < y1) o.flipV = true; s.addShape(pres.shapes.LINE, o);
}
function line(s, x1, y1, x2, y2, col = '8A8A8A', w = 1) { const o = { x: Math.min(x1, x2), y: Math.min(y1, y2), w: Math.abs(x2 - x1), h: Math.abs(y2 - y1), line: { color: col, width: w } }; if (x2 < x1) o.flipH = true; if (y2 < y1) o.flipV = true; s.addShape(pres.shapes.LINE, o); }
// horizontal chain of boxes with arrows
function chain(s, items, x, y, w, h, gap = 0.3, col = C.g, fill = C.lt, o = {}) {
  const n = items.length, bw = (w - gap * (n - 1)) / n;
  items.forEach((it, i) => { const bx = x + i * (bw + gap); const c = it.c || col, f = it.f || fill; box(s, bx, y, bw, h, it.h, it.b, c, f, o); if (i < n - 1) arr(s, bx + bw + 0.03, y + h / 2, bx + bw + gap - 0.03, y + h / 2); });
  return bw;
}
function tb(s, rows, x, y, w, colW, o = {}) {
  const fs = o.fs || FS; const hf = o.head || C.g;
  const hdr = rows[0].map(c => ({ text: String(c), options: { bold: true, color: 'FFFFFF', fill: { color: hf }, align: 'center', valign: 'middle' } }));
  const body = rows.slice(1).map((r, i) => r.map((c, j) => ({ text: rich(String(c)), options: { fill: { color: (o.firstCol && j === 0) ? 'E4ECDD' : (i % 2 ? 'FFFFFF' : 'F5F8F2') }, valign: 'middle', bold: !!(o.firstCol && j === 0) } })));
  s.addTable([hdr, ...body], { x, y, w, colW, fontFace: F, fontSize: fs, color: C.dk, border: { type: 'solid', pt: 0.5, color: 'B9C6B2' }, margin: [0.03, 0.06, 0.03, 0.06], autoPage: false, rowH: o.rowH });
}
function circ(s, x, y, d, t, col = C.g) { s.addShape(pres.shapes.OVAL, { x, y, w: d, h: d, fill: { color: col }, line: { color: col } }); s.addText(t, { x, y, w: d, h: d, fontFace: F, fontSize: FS, bold: true, color: 'FFFFFF', align: 'center', valign: 'middle', isTextBox: true, margin: 0 }); }
function refline(s, t, y = 6.62, h = 0.42) { T(s, [{ text: 'References: ', options: { bold: true, color: C.g, italic: true } }, { text: t, options: { italic: true } }], 0.45, y, 12.43, h, { fontSize: FS, color: '3A3A3A' }); }
module.exports = { pres, F, FS, C, THEME, S, sec, T, BL, box, arr, line, chain, tb, circ, refline, rich };
